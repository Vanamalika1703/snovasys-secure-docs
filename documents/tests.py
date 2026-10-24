from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Document, AuditLog

class DocumentPermissionsTests(TestCase):
    def setUp(self):
        # Create normal users and admin user
        self.user1 = User.objects.create_user(username='ravi', password='password123')
        self.user2 = User.objects.create_user(username='priya', password='password123')
        self.admin = User.objects.create_user(username='admin', password='password123', is_staff=True)

        # Create documents owned by different users
        self.doc1 = Document.objects.create(owner=self.user1, title='Ravi’s Doc', content='Content 1')
        self.doc2 = Document.objects.create(owner=self.user2, title='Priya’s Doc', content='Content 2')

    def test_owner_can_view_document(self):
        # Ravi logs in and tries to view his document
        self.client.login(username='ravi', password='password123')
        url = reverse('document_detail', args=[self.doc1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Allowed
        self.assertContains(response, 'Ravi’s Doc')

    def test_other_user_cannot_view_document(self):
        # Priya tries to view Ravi’s document
        self.client.login(username='priya', password='password123')
        url = reverse('document_detail', args=[self.doc1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Check that an audit log was created for denied access
        log = AuditLog.objects.filter(user=self.user2, document=self.doc1, action='deny').first()
        self.assertIsNotNone(log)

    def test_admin_can_view_any_document(self):
        # Admin can view any document
        self.client.login(username='admin', password='password123')
        url = reverse('document_detail', args=[self.doc1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_document_logs_audit(self):
        # Ravi creates a new document
        self.client.login(username='ravi', password='password123')
        create_url = reverse('create_document')
        response = self.client.post(create_url, {'title': 'New Doc', 'content': 'Important content'}, follow=True)
        self.assertEqual(response.status_code, 200)
        new_doc = Document.objects.get(title='New Doc')
        
        # Confirm audit log entry for creation
        log = AuditLog.objects.filter(user=self.user1, document=new_doc, action='create').first()
        self.assertIsNotNone(log)

    def test_edit_document_permission_and_audit(self):
        # Owner edits document successfully
        self.client.login(username='ravi', password='password123')
        edit_url = reverse('edit_document', args=[self.doc1.id])
        response = self.client.post(edit_url, {'title': 'Updated Title', 'content': 'Updated content'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.doc1.refresh_from_db()
        self.assertEqual(self.doc1.title, 'Updated Title')

        # Check audit log for edit
        log = AuditLog.objects.filter(user=self.user1, document=self.doc1, action='edit').first()
        self.assertIsNotNone(log)

    def test_non_owner_cannot_edit_document(self):
        # Priya tries to edit Ravi's document and is denied
        self.client.login(username='priya', password='password123')
        edit_url = reverse('edit_document', args=[self.doc1.id])
        response = self.client.post(edit_url, {'title': 'Hacked Title', 'content': 'Hacked content'})
        self.assertEqual(response.status_code, 403)

        # Audit log for denied edit
        log = AuditLog.objects.filter(user=self.user2, document=self.doc1, action='deny').first()
        self.assertIsNotNone(log)

    def test_delete_document_and_audit(self):
        # Ravi deletes his document
        self.client.login(username='ravi', password='password123')
        delete_url = reverse('delete_document', args=[self.doc1.id])
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Document.objects.filter(id=self.doc1.id).exists())

        # Confirm audit log for deletion (note document is deleted)
        log = AuditLog.objects.filter(user=self.user1, action='delete').first()
        self.assertIsNotNone(log)

    def test_non_owner_cannot_delete_document(self):
        # Priya attempts to delete Ravi's document - denied
        self.client.login(username='priya', password='password123')
        delete_url = reverse('delete_document', args=[self.doc1.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 403)

        # Audit log for denied delete
        log = AuditLog.objects.filter(user=self.user2, document=self.doc1, action='deny').first()
        self.assertIsNotNone(log)

    def test_invalid_create_fails(self):
        # Test submitting empty title/content is rejected
        self.client.login(username='ravi', password='password123')
        create_url = reverse('create_document')
        response = self.client.post(create_url, {'title': '', 'content': ''})
        self.assertEqual(response.status_code, 200)  # Form redisplayed with errors
        self.assertContains(response, 'Both title and content are required.')
