from rest_framework.test import APITestCase

from shortening.models import ShortUrl
from shortening.utils import get_full_short_url, random_string


class RetrieveTestCase(APITestCase):
    def setUp(self):
        self.short_url_1 = ShortUrl.objects.create(
            real_url="https://www.google.com/",
            url=random_string(6),
            created_by="127.0.0.1"
        )
        self.short_url_2 = ShortUrl.objects.create(
            real_url="https://www.google.com/imghp",
            url=random_string(6),
            created_by="127.0.0.2"
        )

    def test_can_get_short_url_details(self):
        """Test getting short url details by author"""
        response = self.client.get("/api/short_url/{}/".format(self.short_url_1.id))
        request = response.wsgi_request

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, get_full_short_url(request=request, short_url=self.short_url_1))

    def test_cant_get_short_url_details(self):
        """Test getting short url details with different author ip"""
        response = self.client.get("/api/short_url/{}/".format(self.short_url_2.id))

        self.assertEqual(response.status_code, 404)

    def test_can_get_short_url_list(self):
        """Test getting short url list"""
        response = self.client.get("/api/short_url/")
        self.assertEqual(response.status_code, 200)


class CreateDeleteTestCase(APITestCase):
    def setUp(self):
        self.short_url = ShortUrl.objects.create(
            real_url="https://www.google.com/imghp",
            url=random_string(6),
            created_by="127.0.0.2"
        )

    def test_can_create_and_delete_short_url(self):
        """Test creating and deleting own url"""
        response = self.client.post("/api/short_url/", data={"real_url": "https://www.google.com/"})
        request = response.wsgi_request

        self.assertEqual(response.status_code, 201)
        short_url = ShortUrl.objects.get(id=response.data["id"])
        self.assertEqual(response.data, get_full_short_url(request=request, short_url=short_url))

        response = self.client.delete("/api/short_url/{}/".format(response.data["id"]))
        self.assertEqual(response.status_code, 204)

    def test_cant_delete_short_url(self):
        """Test deleting not own url"""

        response = self.client.delete("/api/short_url/{}/".format(self.short_url.id))
        self.assertEqual(response.status_code, 403)



