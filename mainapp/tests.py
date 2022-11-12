from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from authapp.models import CustomUser
from mainapp.models import News


class StaticPagesSmokeTest(TestCase):
    def test_page_main_open(self):
        path = reverse("mainapp:main")
        result = self.client.get(path)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_contacts_open(self):
        path = reverse("mainapp:contacts")
        result = self.client.get(path)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_courses_open(self):
        path = reverse("mainapp:courses")
        result = self.client.get(path)

        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        for i in range(10):
            News.objects.create(
                title=f"News{i}",
                preambule=f"Intro{i}",
                body=f"Body{i}",
            )
        CustomUser.objects.create_superuser(username='admin', password='admin')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'admin', 'password': 'admin'}
        )

    def test_open_page(self):
        url = reverse('mainapp:news')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_detail(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_detail", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonim(self):
        url = reverse('mainapp:news_create')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_item_by_admin(self):

        news_count = News.objects.all().count()

        url = reverse('mainapp:news_create')
        result = self.client_with_auth.post(
            url,
            data={
                'title': 'Test news',
                'preambule': 'Test preambule',
                'body': 'Test body'
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(News.objects.all().count(), news_count + 1)

    def test_create_in_web(self):
        counter_before = News.objects.count()
        path = reverse("mainapp:news_create")

        self.client_with_auth.post(
            path,
            data={
                "title": "NewTestNews001",
                "preambule": "NewTestNews001",
                "body": "NewTestNews001",
            },
        )
        self.assertGreater(News.objects.count(), counter_before)

    def test_page_open_update_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client.get(path)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.get(path)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_in_web(self):
        new_title = "NewTestTitle001"
        news_obj = News.objects.first()

        self.assertNotEqual(news_obj.title, new_title)
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.post(
            path,
            data={
                "title": new_title,
                "preambule": news_obj.preambule,
                "body": news_obj.body,
            },
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        result = self.client.post(path)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])

        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)

