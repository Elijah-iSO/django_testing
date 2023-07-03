from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestContentPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(
            username='Авторизированный пользователь')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.notes = Note.objects.create(
            title='Заметка автора',
            text='Просто текст',
            author=cls.author,)

    def test_notes_list_for_different_users(self):
        client_content = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for client, content in client_content:
            with self.subTest(client=client):
                url = reverse('notes:list')
                response = client.get(url)
                object_list = response.context['object_list']
                self.assertEqual(self.notes in object_list, content)

    def test_anonymous_client_has_no_form(self):
        response = self.client.get('notes:add')
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes.slug,))
        )
        for url, args in urls:
            self.client.force_login(self.author)
            with self.subTest(url=url):
                url = reverse(url, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
