from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationTests(APITestCase):
    def test_register_returns_token_and_roles(self):
        resp = self.client.post(
            "/api/auth/register/",
            {"username": "alice", "password": "longpassword1", "roles": ["founder"]},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertIn("token", resp.data)
        self.assertEqual(resp.data["roles"], ["founder"])
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_register_defaults_to_reader_role(self):
        resp = self.client.post(
            "/api/auth/register/",
            {"username": "bob", "password": "longpassword1"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["roles"], ["reader"])

    def test_duplicate_username_rejected(self):
        User.objects.create_user("carol", password="longpassword1")
        resp = self.client.post(
            "/api/auth/register/",
            {"username": "carol", "password": "longpassword1"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_short_password_rejected(self):
        resp = self.client.post(
            "/api/auth/register/",
            {"username": "dave", "password": "short"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_obtain_token_endpoint(self):
        User.objects.create_user("erin", password="longpassword1")
        resp = self.client.post(
            "/api/auth/token/",
            {"username": "erin", "password": "longpassword1"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.data)


class MeEndpointTests(APITestCase):
    def test_me_with_valid_token(self):
        user = User.objects.create_user("frank", password="longpassword1")
        from rest_framework.authtoken.models import Token

        token = Token.objects.create(user=user)
        resp = self.client.get("/api/auth/me/", HTTP_AUTHORIZATION=f"Token {token.key}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["username"], "frank")

    def test_me_anonymous_rejected(self):
        resp = self.client.get("/api/auth/me/")
        self.assertEqual(resp.status_code, 401)
