from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContentPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author_1 = User.objects.create(username='Автор 1')
        cls.author_2 = User.objects.create(username='Автор 2')
        cls.users = [cls.author_1, cls.author_2]
        cls.notes = Note.objects.create(
            title='Заметка автора',
            text='Просто текст',
            author=cls.author_1,
            )

    def test_list_context(self):
        for user in self.users:
            self.client.force_login(user)
            url = reverse('notes:list')
            response = self.client.get(url)
            object_list = response.context['object_list']
            if user == self.notes.author:
                self.assertIn(self.notes, object_list)
            else:
                self.assertNotIn(self.notes, object_list)

    def test_anonymous_client_has_no_form(self):
        response = self.client.get('notes:add')
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes.slug,))
        )
        for url, args in urls:
            self.client.force_login(self.author_1)
            with self.subTest(url=url):
                url = reverse(url, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
