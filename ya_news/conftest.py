import pytest

from datetime import datetime, timedelta
from django.conf import settings

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_list():
    news_list = News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1))
    return news_list


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        text='Текст комментария',
        author=author,
        news=news,
    )
    return comment


@pytest.fixture
def comment_list(author, news):
    comment_list = Comment.objects.bulk_create(
        Comment(
            text=f'Текст комментария {index}',
            author=author,
            news=news,
        ) for index in range(2)
    )
    return comment_list


@pytest.fixture
def id_for_args(news):
    return news.id,


@pytest.fixture
def form_data(news, author):
    return {
        'text': 'Новый текст комментария',
        'author': author,
        'news': news,
    }
