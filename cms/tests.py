from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Content, Category

class ContentTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.author_user = User.objects.create_user(username='author', password='authorpass', email='author@example.com')
        self.category = Category.objects.create(name='Django')
        self.content_data = {
            'title': 'Django Content',
            'body': 'Body of Django content',
            'summary': 'Summary of Django content',
            'categories': [self.category.id]
        }
        self.client.force_authenticate(user=self.admin_user)  # Authenticate as admin for most tests

    def test_create_content_as_admin(self):
        url = reverse('content-list-create')
        response = self.client.post(url, self.content_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(Content.objects.get().title, 'Django Content')

    def test_create_content_as_author(self):
        self.client.force_authenticate(user=self.author_user)  # Switch to author user
        url = reverse('content-list-create')
        response = self.client.post(url, self.content_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expecting Forbidden for non-admin

    def test_get_content_list(self):
        Content.objects.create(title='Test Content', body='Body of Test content', summary='Summary of Test content')
        url = reverse('content-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one content exists

    def test_update_content_as_admin(self):
        content = Content.objects.create(title='Initial Title', body='Initial Body', summary='Initial Summary')
        url = reverse('content-detail', kwargs={'pk': content.id})
        updated_data = {
            'title': 'Updated Title',
            'body': 'Updated Body',
            'summary': 'Updated Summary',
            'categories': [self.category.id]
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content.refresh_from_db()
        self.assertEqual(content.title, 'Updated Title')

    def test_update_content_as_author(self):
        self.client.force_authenticate(user=self.author_user)  # Switch to author user
        content = Content.objects.create(title='Initial Title', body='Initial Body', summary='Initial Summary')
        url = reverse('content-detail', kwargs={'pk': content.id})
        updated_data = {
            'title': 'Updated Title',
            'body': 'Updated Body',
            'summary': 'Updated Summary',
            'categories': [self.category.id]
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expecting Forbidden for non-admin

    def test_delete_content_as_admin(self):
        content = Content.objects.create(title='To be deleted', body='Content to be deleted', summary='Summary to be deleted')
        url = reverse('content-detail', kwargs={'pk': content.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Content.objects.count(), 0)

    def test_delete_content_as_author(self):
        self.client.force_authenticate(user=self.author_user)  # Switch to author user
        content = Content.objects.create(title='To be deleted', body='Content to be deleted', summary='Summary to be deleted')
        url = reverse('content-detail', kwargs={'pk': content.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expecting Forbidden for non-admin
        self.assertEqual(Content.objects.count(), 1)  # Ensure content still exists

    def test_search_content(self):
        Content.objects.create(title='Searchable Content', body='Content for search testing', summary='Summary for search testing')
        url = reverse('content-search') + '?q=searchable'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one content matches search term

    def test_search_content_no_results(self):
        Content.objects.create(title='Searchable Content', body='Content for search testing', summary='Summary for search testing')
        url = reverse('content-search') + '?q=nonexistent'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No content should match this search term
