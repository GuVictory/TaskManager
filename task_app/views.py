from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import UserSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
            tasks = Task.objects.get(id=pk)

            if tasks.creator != user:
                return Response({"message": "User don't have task with that id"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(tasks, many=False)
            serializer = serializer.data
            return Response(serializer, status=status.HTTP_200_OK)
        except:
            return Response({"message": "User don't have task with that id"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user = Token.objects.get(key=request.auth.key).user
            task = Task.objects.get(id=pk)

            if task.creator != user:
                return Response({"message": "User don't have task with that id"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(request.data, many=False)
            serializer = serializer.data

            task.title = serializer['title'] if 'title' in serializer else task.title
            task.description = serializer['description'] if 'description' in serializer else task.description

            if 'finish_date' in serializer and serializer['finish_date'] is not None:
                task.finish_date = serializer['finish_date']

            if 'status' in serializer:
                status_check = len(list(filter(lambda x: x[0] == serializer['status'], Task.STATUS_CHOICES)))
                print(status_check)
                if status_check:
                    task.status = serializer['status']
                else:
                    return Response({"message": "Status is not correct!"}, status=status.HTTP_400_BAD_REQUEST)

            task.save()

            serializer = TaskSerializer(task, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "User don't have task with that id __"}, status=status.HTTP_404_NOT_FOUND)
