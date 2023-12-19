from datetime import datetime, timedelta 
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()


class TestHomePage(TestCase):
    NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем заметки с указанием автора
        all_notes = [
            Note(
                title=f'Новость {index}',
                text='Просто текст.',
                author=cls.user,
                slug=f'note-{index}'  # Уникальный slug
            )
            for index in range(settings.NOTES_COUNT_ON_HOME_PAGE + 1)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_count(self):
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['notes']
        notes_count = len(object_list)
        self.assertEqual(notes_count, settings.NOTES_COUNT_ON_HOME_PAGE)