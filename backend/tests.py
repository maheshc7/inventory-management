from django.test import TestCase

from django.contrib.auth import get_user_model
from djet import assertions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.test import APIClient
from django.core import mail

User = get_user_model()


def create_user(**kwargs):
    data = (
        {"username": "john", "password": "secret@123", "email": "john@beatles.com"}
    )
    data.update(kwargs)
    user = get_user_model().objects.create_user(**data)
    user.raw_password = data["password"]
    return user


class UserCreateViewTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.EmailAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self):
        self.base_url = reverse("user-list")  # /auth/users/

    def test_post_create_user_without_login(self):
        data = {"username": "john",
                "password": "secret@123", "csrftoken": "asdf"}
        response = self.client.post(self.base_url, data)

        self.assert_status_equal(response, status.HTTP_201_CREATED)
        self.assertTrue("password" not in response.data)
        self.assert_instance_exists(User, username=data["username"])
        user = User.objects.get(username=data["username"])
        self.assertTrue(user.check_password(data["password"]))

    def test_post_not_create_new_user_if_username_exists(self):
        create_user(username="john")
        data = {"username": "john",
                "password": "secret@123", "csrftoken": "asdf"}
        response = self.client.post(self.base_url, data)

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_post_not_register_if_fails_password_validation(self):
        data = {"username": "john", "password": "666", "csrftoken": "asdf"}
        response = self.client.post(self.base_url, data)

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
        response.render()
        self.assertEqual(
            str(response.data["password"][0]
                ), "This password is too short. It must contain at least 8 characters."
        )


class PasswordResetViewTest(
    APITestCase, assertions.StatusCodeAssertionsMixin, assertions.EmailAssertionsMixin
):
    def setUp(self):
        self.base_url = reverse("user-reset-password")

    def test_post_should_send_email_to_user_with_password_reset_link(self):
        user = create_user()
        data = {"email": user.email}

        response = self.client.post(self.base_url, data)
        request = response.wsgi_request

        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)
        self.assert_emails_in_mailbox(1)
        self.assert_email_exists(to=[user.email])
        site = get_current_site(request)
        self.assertIn(site.domain, mail.outbox[0].body)
        self.assertIn(site.name, mail.outbox[0].body)

    def test_post_send_email_to_user_with_request_domain_and_site_name(self):
        user = create_user()
        data = {"email": user.email}

        response = self.client.post(self.base_url, data)
        request = response.wsgi_request

        self.assertIn(request.get_host(), mail.outbox[0].body)

    def test_post_should_not_send_email_to_user_if_user_does_not_exist(self):
        data = {"email": "john@beatles.com"}

        response = self.client.post(self.base_url, data)
        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)
        self.assert_emails_in_mailbox(0)

    def test_post_should_return_no_content_if_user_does_not_exist(self):
        data = {"email": "john@beatles.com"}

        response = self.client.post(self.base_url, data)

        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)


class ItemAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.token = self.client.post(reverse(
            'jwt-create'), {'username': 'john', 'password': 'secret@123'}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

    def test_generate_jwt_tokens(self):
        url = reverse('jwt-create')
        response = self.client.post(
            url, {'username': 'john', 'password': 'secret@123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_item_dashboard(self):
        # Assuming the endpoint for item dashboard is 'item-list'
        url = reverse('item-api')
        response = self.client.get(url, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item_dashboard_without_token(self):
        self.client.credentials()  # Clear credentials to simulate no token provided
        url = reverse('item-api')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
