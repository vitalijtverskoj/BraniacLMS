import pickle
from http import HTTPStatus
from unittest import mock

from config import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail as django_mail
from django.test import TestCase, Client
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from authapp.models import CustomUser
from mainapp.models import News, Courses
from mainapp import tasks as mainapp_tasks


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


class TestCoursesWithMock(TestCase):
    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/002_courses.json",
        "mainapp/fixtures/003_lessons.json",
        "mainapp/fixtures/004_teachers.json",
    )

    def test_page_open_detail(self):
        course_obj = Courses.objects.get(pk=2)
        path = reverse("mainapp:courses_detail", args=[course_obj.pk])
        with open(
            "mainapp/fixtures/006_feedback_list_2.bin", "rb"
        ) as inpf, mock.patch("django.core.cache.cache.get") as mocked_cache:
            mocked_cache.return_value = pickle.load(inpf)
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)
            self.assertTrue(mocked_cache.called)


class TestTaskMailSend(TestCase):
    fixtures = ("authapp/fixtures/001_user_admin.json",)

    def test_mail_send(self):
        message_text = "test_message_text"
        user_obj = CustomUser.objects.first()
        mainapp_tasks.send_feedback_mail(
        {"user_id": user_obj.id, "message": message_text}
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)


class TestNewsSelenium(StaticLiveServerTestCase):
    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/001_news.json",
    )

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver(
            executable_path=settings.SELENIUM_DRIVER_PATH_FF
        )
        self.selenium.implicitly_wait(10)
        # Login
        self.selenium.get(f"{self.live_server_url}{reverse('authapp:login')}")
        button_enter = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[type="submit"]')
            )
        )
        self.selenium.find_element_by_id("id_username").send_keys("admin")
        self.selenium.find_element_by_id("id_password").send_keys("admin")
        button_enter.click()
        # Wait for footer
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto"))
        )

    def test_create_button_clickable(self):
        path_list = f"{self.live_server_url}{reverse('mainapp:news')}"
        path_add = reverse("mainapp:news_create")
        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f'[href="{path_add}"]')
            )
        )
        print("Trying to click button ...")
        button_create.click()  # Test that button clickable
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.ID, "id_title"))
        )
        print("Button clickable!")
        # With no element - test will be failed
        # WebDriverWait(self.selenium, 5).until(
        # EC.visibility_of_element_located((By.ID, "id_title111"))
        # )

        def test_pick_color(self):
            path = f"{self.live_server_url}{reverse('mainapp:main')}"
            self.selenium.get(path)
            navbar_el = WebDriverWait(self.selenium, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "navbar"))
            )
            try:
                self.assertEqual(
                    navbar_el.value_of_css_property("background-color"),
                    "rgb(255, 255, 155)",
                )
            except AssertionError:
                with open(
                        "var/screenshots/001_navbar_el_scrnsht.png", "wb"
                ) as outf:
                    outf.write(navbar_el.screenshot_as_png)
                raise

        def tearDown(self):
            # Close browser
            self.selenium.quit()
            super().tearDown()
