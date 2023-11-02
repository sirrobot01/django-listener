from importlib import import_module

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils.text import slugify


# Create your models here.

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Source(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    url = models.URLField(max_length=1000)
    is_active = models.BooleanField(default=True)
    unique_id_field = models.CharField(max_length=255,
                                       default='id')  # use (dot) notation for nested fields, e.g. 'data.id'

    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    token_header = models.CharField(max_length=255, default='HTTP_AUTHORIZATION')

    http_method = models.CharField(max_length=255, default='POST')

    last_checked = models.DateTimeField(null=True, blank=True)
    content_type = models.CharField(max_length=255, default='application/json')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.password:
            # encrypt password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def authenticate(self, raw_password):
        if self.username and self.password:
            return check_password(raw_password, self.password)
        elif self.token:
            return raw_password == self.token
        return True

    def get_processor_class(self):
        from listener.settings import Settings
        from listener.processor import DefaultProcessor

        settings = Settings()
        processor_class = settings.PROCESSORS.get(self.slug, settings.PROCESSORS.get("default"))
        # Import the processor class
        if not processor_class:
            return DefaultProcessor
        try:
            module_name, class_name = processor_class.rsplit(".", 1)
            module = import_module(module_name)
            return getattr(module, class_name)
        except (ImportError, AttributeError):
            return DefaultProcessor


class Event(BaseModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    query_params = models.TextField(blank=True, null=True)
    unique_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.source, self.unique_id)
