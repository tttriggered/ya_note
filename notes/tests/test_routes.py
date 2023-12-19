from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()

class TestNoteCreateView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.create_url = reverse('notes:add')  # Замените 'note_create' на имя вашего URL-паттерна для создания заметки

    def test_anonymous_user_redirect(self):
        response = self.client.get(self.create_url)
        login_url = reverse('users:login')  # Замените 'users:login' на имя вашего URL-паттерна для входа
        expected_redirect_url = f'{login_url}?next={self.create_url}'
        self.assertRedirects(response, expected_redirect_url)

    def test_authenticated_user_access(self):
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_note(self):
        self.client.force_login(self.user)
        data = {'title': 'Test Title', 'text': 'Test Text'}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        created_note = Note.objects.first()
        self.assertEqual(created_note.title, 'Test Title')
        self.assertEqual(created_note.text, 'Test Text')
        self.assertEqual(created_note.author, self.user)
