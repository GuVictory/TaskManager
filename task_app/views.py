import time

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task, TaskHistory
from .serializers import UserSerializer, TaskSerializer, TaskHistorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_user_tasks(self, request):
        try:
            user = Token.objects.get(key=request.auth.key).user
            tasks = Task.objects.filter(creator=user)
            return tasks
        except:
            return []

    def create_history_note(self, task, field, old_value, new_value):
        task_note = f'{field} value has been changed: {old_value} -> {new_value}'
        task_note = TaskHistory(task=task, note=task_note)
        task_note.save()

    def list(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.auth.key).user
        tasks = Task.objects.filter(creator=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.auth.key).user
        serializer = TaskSerializer(request.data, many=False)
        serializer = serializer.data
        task = Task(
                creator=user,
                title=serializer['title'],
                description=serializer['description'],
                status=serializer['status'],
                finish_date=serializer['finish_date']
        )
        task.save()
        serializer['id'] = task.id
        return Response(serializer, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            user = Token.objects.get(key=request.auth.key).user
            all_t = Task.objects.all()
            all_t = TaskSerializer(all_t, many=True)
            all_t = all_t.data
            tasks = Task.objects.get(id=pk)

            if tasks.creator != user:
                return Response({"message": "User don't have task with that id"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(tasks, many=False)
            serializer = serializer.data
            return Response(serializer, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Error while trying to found task with that id"},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user = Token.objects.get(key=request.auth.key).user
            task = Task.objects.get(id=pk)

            if task.creator != user:
                return Response({"message": "User don't have task with that id"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(request.data, many=False)
            serializer = serializer.data

            if 'title' in serializer:
                self.create_history_note(task, 'title', task.title, serializer['title'])
                task.title = serializer['title']

            if 'description' in serializer:
                self.create_history_note(task, 'description', task.description, serializer['description'])
                task.description = serializer['description']

            if 'finish_date' in serializer and serializer['finish_date'] is not None:
                try:
                    time.strptime(serializer['finish_date'], '%Y-%m-%d')
                    self.create_history_note(task, 'finish_date', task.finish_date, serializer['finish_date'])
                    task.finish_date = serializer['finish_date']
                except ValueError:
                    return Response({"message": "Date format is not correct use YYYY-MM-DD"},
                                    status=status.HTTP_400_BAD_REQUEST)

            if 'status' in serializer:
                status_check = len(list(filter(lambda x: x[0] == serializer['status'], Task.STATUS_CHOICES)))
                if status_check:
                    self.create_history_note(task, 'status', task.status, serializer['status'])
                    task.status = serializer['status']
                else:
                    return Response({"message": "Status is not correct!"}, status=status.HTTP_400_BAD_REQUEST)

            task.save()

            serializer = TaskSerializer(task, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "User don't have task with that id"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def new_tasks(self, request):
        try:
            tasks = self.get_user_tasks(request).filter(status=Task.NEW)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def planned_tasks(self, request):
        try:
            tasks = self.get_user_tasks(request).filter(status=Task.PLANNED)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def in_work_tasks(self, request):
        try:
            tasks = self.get_user_tasks(request).filter(status=Task.IN_WORK)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def compleated_tasks(self, request):
        try:
            tasks = self.get_user_tasks(request).filter(status=Task.COMPLETED)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def sort_by_date_tasks(self, request):
        try:
            tasks = self.get_user_tasks(request).order_by('finish_date')
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def sort_by_date_desc_tasks(self, request):
        try:
            tasks = self.get_user_tasks(request).order_by('-finish_date')
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def task_history(self, request, pk=None):
        try:
            user = Token.objects.get(key=request.auth.key).user
            task = Task.objects.get(id=pk)

            if task.creator != user:
                return Response({"message": "User don't have task with that id"}, status=status.HTTP_404_NOT_FOUND)

            task_history = TaskHistory.objects.filter(task=task)
            serializer = TaskHistorySerializer(task_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
