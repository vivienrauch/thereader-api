from therader_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions
from .models import Contact
from .serializers import ContactSerializer