from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from .models import Document, AuditLog

class DocumentAccessTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='ravi', password='pass')
        self.user2 = User.objects.create_user(username='priya', password='pass')
        self.admin = User.objects.create_user(username='admin', password='pass', is_staff=True)
        self.doc1 = Document.objects.create(owner=self.user1, title='Doc1', content='Hello Ravi')
        self.doc2 = Document.objects.create(owner=self.user2, title='Doc2', content='Hello Priya')

    def test_owner_can_view_document(self):
        self.client.login(username='ravi', password='pass')
        response = self.client.get(f'/documents/{self.doc1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_other_cannot_view_document(self):
        self.client.login(username='priya', password='pass')
        response = self.client.get(f'/documents/{self.doc1.id}/')
        self.assertEqual(response.status_code, 403)

    def test_admin_can_view_any_document(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(f'/documents/{self.doc1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_audit_log_created_on_denied_access(self):
        self.client.login(username='priya', password='pass')
        self.client.get(f'/documents/{self.doc1.id}/')
        log = AuditLog.objects.filter(user=self.user2, document=self.doc1, action='deny').first()
        self.assertIsNotNone(log)
