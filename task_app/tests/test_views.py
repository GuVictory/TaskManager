from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from task_app.models import Task
from task_app.serializers import TaskSerializer

# initialize the APIClient app
client = APIClient()


class GetTasksTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='TestUser')
        self.token = Token.objects.create(user=self.user)
        client.login(username='TestUser', password='TestUser')
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        fake_user = User.objects.create(username='FakeUser', password='FakeUser')

        Task.objects.create(
                creator=self.user,
                title='TestTitle_1',
                description='TestDescription_1',
                status=Task.NEW,
        )
        Task.objects.create(
                creator=fake_user,
                title='TestTitle_2',
                description='TestDescription_2',
                status=Task.PLANNED,
        )
        Task.objects.create(
                creator=self.user,
                title='TestTitle_3',
                description='TestDescription_3',
                status=Task.COMPLETED,
        )
        Task.objects.create(
                creator=self.user,
                title='TestTitle_4',
                description='TestDescription_4',
                status=Task.NEW,
        )

    def test_get_all_tasks(self):
        # get API response
        response = client.get('http://testserver/api/tasks/')

        # get data from db
        tasks = Task.objects.filter(creator=self.user)

        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_task_200(self):
        # get API response
        response = client.get('http://testserver/api/tasks/5/')

        # get data from db
        task = Task.objects.get(id=5)
        serializer = TaskSerializer(task, many=False)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_task_404(self):
        # get API response
        response = client.get('http://testserver/api/tasks/11000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostTasksTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='TestUser')
        self.token = Token.objects.create(user=self.user)
        client.login(username='TestUser', password='TestUser')
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_post_task(self):
        # get API response
        data = {
            'title': 'TestTitle',
            'description': 'TestDescription',
            'status': 'New'
        }
        response = client.post('http://testserver/api/tasks/', data, format='json')

        # get data from db
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True).data

        self.assertEqual(response.data['id'], serializer[0]['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateTasksTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='TestUser')
        self.token = Token.objects.create(user=self.user)
        client.login(username='TestUser', password='TestUser')
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        fake_user = User.objects.create(username='FakeUser', password='FakeUser')

        Task.objects.create(
                creator=self.user,
                title='TestTitle_1',
                description='TestDescription_1',
                status=Task.NEW,
        )

        Task.objects.create(
                creator=fake_user,
                title='TestTitle_2',
                description='TestDescription_2',
                status=Task.PLANNED,
        )

    def test_put_title_task(self):
        old_task = Task.objects.get(title='TestTitle_1')
        # get API response
        data = {
            'title': 'TestNewTitle',
        }
        response = client.put(f'http://testserver/api/tasks/{old_task.id}/', data, format='json')

        # get data from db
        new_task = Task.objects.get(id=old_task.id)

        self.assertEqual(new_task.title, 'TestNewTitle')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_title_description_task(self):
        old_task = Task.objects.get(title='TestTitle_1')
        # get API response
        data = {
            'title': 'TestNewTitle',
            'description': 'TestNewDescription',
        }
        response = client.put(f'http://testserver/api/tasks/{old_task.id}/', data, format='json')

        # get data from db
        new_task = Task.objects.get(id=old_task.id)

        self.assertEqual(new_task.title, 'TestNewTitle')
        self.assertEqual(new_task.description, 'TestNewDescription')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_status_task(self):
        old_task = Task.objects.get(title='TestTitle_1')
        # get API response
        data = {
            'status': 'Planned',
        }
        response = client.put(f'http://testserver/api/tasks/{old_task.id}/', data, format='json')

        # get data from db
        new_task = Task.objects.get(id=old_task.id)

        self.assertEqual(new_task.status, 'Planned')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_status_400_task(self):
        old_task = Task.objects.get(title='TestTitle_1')
        # get API response
        data = {
            'status': 'OmNomNom',
        }
        response = client.put(f'http://testserver/api/tasks/{old_task.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
