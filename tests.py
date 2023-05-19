from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from social_link_aggregator.models import Link

class LinkTests(APITestCase):
    def test_create_link(self):
        """
        Ensure we can create a new link object.
        """
        url = reverse('links-list')
        data = {'url': 'https://www.google.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(Link.objects.get().url, 'https://www.google.com')

    def test_upvote_a_link(self):
        """
        Ensure we can upvote a link.
        """
        url = reverse('links-list')
        data = {'url': 'https://www.google.com'}
        created_link = self.client.post(url, data, format='json')

        url = reverse('links-upvote', kwargs={"pk": created_link.data["id"]})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.get().upvotes, 1)
        self.assertEqual(Link.objects.get().score, 1)

    def test_downvote_a_link(self):
        """
        Ensure we can downvote a link.
        """
        url = reverse('links-list')
        data = {'url': 'https://www.google.com'}
        created_link = self.client.post(url, data, format='json')

        url = reverse('links-downvote', kwargs={"pk": created_link.data["id"]})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.get().downvotes, 1)
        self.assertEqual(Link.objects.get().score, -1)

    def test_create_invalid_link(self):
        """
        Ensure we cannot create a link that doesn't look like one.
        """
        url = reverse('links-list')
        data = {'url': 'Old MacDonald Had A Farm'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_links_order(self):
        """
        Ensure we can create a new link object.
        """
        url = reverse('links-list')
        data = {'url': 'https://www.google.com'}
        first_link = self.client.post(url, data, format='json')
        data = {'url': 'https://www.youtube.com'}
        second_link = self.client.post(url, data, format='json')

        url = reverse('links-upvote', kwargs={"pk": second_link.data["id"]})
        self.client.post(url, {}, format='json')

        url = reverse('links-downvote', kwargs={"pk": first_link.data["id"]})
        self.client.post(url, {}, format='json')


        url = reverse('links-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            [link["url"] for link in response.data],
            ['https://www.youtube.com', 'https://www.google.com']
        )
