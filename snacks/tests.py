from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.Snack = Snack.objects.create(
            title="pickle", description=1, purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.Snack), "pickle")

    def test_Snack_content(self):
        self.assertEqual(f"{self.Snack.title}", "pickle")
        self.assertEqual(f"{self.Snack.purchaser}", "tester")
        self.assertEqual(f"{self.Snack.description}", "1")

    def test_Snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pickle")
        self.assertTemplateUsed(response, "snack_list.html")

    # def test_Snack_detail_view(self):
    #     response = self.client.get(reverse("snack_detail", args="1"))
    #     # no_response = self.client.get("/100000/")
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertEqual(no_response.status_code, 404)
    #     self.assertContains(response, "purchaser: "tester")
    #     self.assertTemplateUsed(response, "snack_detail.html")

    def test_Snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Rake",
                "description": "2",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "2")

    def test_Snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated title","description":"3","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_Snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)
