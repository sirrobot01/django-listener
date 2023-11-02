from django.conf import settings


class Settings:
    # Contains the settings for the listener app, check django.conf.settings first
    PROCESSORS = {
        "default": "listener.processor.DefaultProcessor",
    }

    def __init__(self):
        django_settings = getattr(settings, "LISTENER", {})
        for key, value in django_settings.items():
            setattr(self, key, value)
