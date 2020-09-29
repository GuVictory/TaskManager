from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet, TasksViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tasks', TasksViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token),
]
