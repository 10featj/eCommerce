from rest_framework import routers
from .viewsets import UserViewSet

api_router = routers.SimpleRouter()
api_router.register('users', UserViewSet)