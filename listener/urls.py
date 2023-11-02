from django.urls import path

from listener.views import WebhookView

urlpatterns = [
    path("webhooks/<str:slug>/", WebhookView.as_view(), name="event"),
]
