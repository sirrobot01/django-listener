# Description: This file contains the EventProcessor class which is used to process the event
# received from the listener.
from django.utils import timezone


class DefaultProcessor:
    def __init__(self, event, force_process=False):
        self.event = event
        self.force_process = force_process

    def process(self):
        event = self.event
        if self.event.processed and not self.force_process:
            return
        event.processed = True
        event.processed_at = timezone.now()
        event.save()
