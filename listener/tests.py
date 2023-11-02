import base64

from django.test import TestCase

from listener.models import Source, Event


# Create your tests here.
# Path: listener/tests.py


class SourceModelTestCase(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Test Source",
            slug="test-source",
            url="https://example.com/webhooks/test-source/",
            is_active=True,
            unique_id_field="id",
            username="test",
            password="test",
            token="test",
            token_header="HTTP_AUTHORIZATION",
            http_method="POST",
            content_type="application/json",
        )

    def test_source_str(self):
        self.assertEqual(str(self.source), "Test Source")

    def test_source_save(self):
        self.assertEqual(self.source.slug, "test-source")
        self.assertTrue(self.source.authenticate("test"))
        self.assertFalse(self.source.authenticate("invalid"))

    def test_source_authenticate(self):
        self.assertTrue(self.source.authenticate("test"))
        self.assertFalse(self.source.authenticate("invalid"))

    def test_source_authenticate_token(self):
        self.source.username = None
        self.source.password = None
        self.source.save()
        self.assertTrue(self.source.authenticate("test"))
        self.assertFalse(self.source.authenticate("invalid"))

    def test_source_authenticate_no_auth(self):
        self.source.username = None
        self.source.password = None
        self.source.token = None
        self.source.save()
        self.assertTrue(self.source.authenticate("test"))
        self.assertTrue(self.source.authenticate("invalid"))
    
    def test_get_processor_class(self):
        from listener.settings import Settings
        from listener.processor import DefaultProcessor
        self.assertEqual(self.source.get_processor_class(), DefaultProcessor)


class WebhookViewTestCase(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Test Source",
            slug="test-source",
            url="https://example.com/webhooks/test-source/",
            is_active=True,
            unique_id_field="id",
            username="test",
            password="test",
            token="test",
            token_header="HTTP_AUTHORIZATION",
            http_method="POST",
            content_type="application/json",
        )

    def test_webhook_view(self):
        response = self.client.get("/webhooks/test-source/")
        self.assertEqual(response.status_code, 405)
        response = self.client.post("/webhooks/test-source/")
        self.assertEqual(response.status_code, 401)
        credentials = base64.b64encode(b"test:test").decode("utf-8")
        headers = {"Host": "testserver", "Connection": "close", "Content-Type": "application/json"}
        response = self.client.post(
            "/webhooks/test-source/", HTTP_AUTHORIZATION="Basic %s" % credentials, content_type="application/json",
            data={"test": "test", "id": "test"}, headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.source, self.source)
        self.assertEqual(event.name, "Test Source")
        self.assertEqual(event.body, '{"test": "test", "id": "test"}')
        self.assertEqual(event.query_params, '{}')
        self.assertEqual(event.unique_id, "test")

    def test_webhook_view_token(self):
        self.source.username = None
        self.source.password = None
        self.source.save()
        response = self.client.post("/webhooks/test-source/", HTTP_AUTHORIZATION="Bearer dGVzdDp0ZXN0",
                                    content_type="application/json", data={"test": "test", "id": "test"})
        self.assertEqual(response.status_code, 401)
        response = self.client.post("/webhooks/test-source/", HTTP_AUTHORIZATION="test",
                                    content_type="application/json", data='{"test": "test", "id": "test"}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.source, self.source)
        self.assertEqual(event.name, "Test Source")
        self.assertEqual(event.body, '{"test": "test", "id": "test"}')
        self.assertEqual(event.query_params, '{}')
        self.assertEqual(event.unique_id, "test")
        

class DefaultProcessorTestCase(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Test Source",
            slug="test-source",
            url="https://example.com/webhooks/test-source/",
            is_active=True,
            unique_id_field="id",
            username="test",
            password="test",
            token="test",
            token_header="HTTP_AUTHORIZATION",
            http_method="POST",
            content_type="application/json",
        )
        self.event = Event.objects.create(
            source=self.source,
            name="Test Source",
            body='{"test": "test", "id": "test"}',
            headers='{"Host": "testserver", "Connection": "close", "Content-Type": "application/json"}',
            query_params='{}',
            unique_id="test",
        )

    def test_process(self):
        processor = self.source.get_processor_class()(self.event)
        self.assertEqual(processor.process(), None)
        self.event.refresh_from_db()
        self.assertEqual(self.event.processed, True)
        self.assertNotEqual(self.event.processed_at, None)
