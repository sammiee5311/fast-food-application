from accounts.models import Address, Client, CustomAccountManager, EmailError
from django.test import TestCase


class TestAccountsModels(TestCase):
    def setUp(self):
        self.address = Address.objects.create(zipcode="12345")
        self.client = Client.objects.create(
            username="test", password="password", email="test@test.com", address=self.address, name="test"
        )

    def test_name_of_client(self):
        self.assertEqual("test", str(self.client))

    def test_name_of_address(self):
        self.assertEqual("12345", str(self.address))

    def test_create_user(self):
        user = CustomAccountManager()
        user.model = Client.objects.create
        a = user.create_superuser(email="a@a.com", username="a", name="a", password="a")
        with self.assertRaises(EmailError):
            user.create_superuser(email="b@b", username="b", name="b", password="b")
        with self.assertRaises(EmailError):
            user.create_superuser(email="", username="b", name="b", password="b")
        with self.assertRaises(EmailError):
            user.create_user(email="", username="c", name="c", password="c")

        self.assertEqual(a.username, "a")
