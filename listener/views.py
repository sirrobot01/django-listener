import json

from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from listener.models import Source
from listener.utils import authenticate


# Create your views here.


class WebhookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        if slug:
            source = Source.objects.filter(slug=slug).first()
            if source:
                return self.process_webhook(request, source, *args, **kwargs)
        return HttpResponseNotFound("Invalid webhook slug")

    def process_webhook(self, request, source, *args, **kwargs):
        method = request.method.lower()
        if method != source.http_method.lower():
            return HttpResponseNotAllowed([source.http_method.lower()], "Invalid HTTP method")

        if not authenticate(request, source):
            return HttpResponse("Unauthorized", status=401)

        source.last_checked = timezone.now()
        source.save()

        body = request.body
        if hasattr(body, "decode"):
            body = body.decode("utf-8")
        try:
            data = json.loads(body)
            unique_id_field = source.unique_id_field
            if unique_id_field:
                unique_id = data
                for field in unique_id_field.split('.'):
                    unique_id = unique_id.get(field)
            else:
                unique_id = data.get('id')
            if unique_id:
                event = source.events.filter(unique_id=unique_id).first()
                if not event:
                    event = source.events.create(
                        name=source.name,
                        body=body,
                        headers=json.dumps(dict(request.headers)),
                        query_params=json.dumps(dict(request.GET)),
                        unique_id=unique_id,
                    )
                    event.save()
                if not event.processed:
                    processor_class = source.get_processor_class()
                    processor = processor_class(event)
                    processor.process()
            return HttpResponse("OK")
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON payload", status=400)
