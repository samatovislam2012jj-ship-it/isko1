from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Task


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            title='Первая задача',
            description='Описание первой задачи',
            completed=False
        )

    def test_get_tasks(self):
        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        data = {
            'title': 'Новая задача',
            'description': 'Описание новой задачи',
            'completed': False
        }

        response = self.client.post('/api/tasks/', data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(Task.objects.count(), 2)

    def test_get_task(self):
        response = self.client.get(
            f'/api/tasks/{self.task.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_task(self):
        data = {
            'title': 'Измененная задача',
            'description': 'Новое описание',
            'completed': True
        }

        response = self.client.put(
            f'/api/tasks/{self.task.id}/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_delete_task(self):
        response = self.client.delete(
            f'/api/tasks/{self.task.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(Task.objects.count(), 0)

    def test_filter_completed_tasks(self):
        Task.objects.create(
            title='Завершенная',
            description='Готово',
            completed=True
        )

        response = self.client.get(
            '/api/tasks/?completed=true'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(response.data['results']), 1)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)

        response = self.client.get('/api/tasks/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )