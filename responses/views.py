from rest_framework import generics, permissions
from thereader_api.permissions import IsOwnerOrReadOnly
from .models import Response
from .serializers import ResponseSerializer


class ResponseList(generics.ListCreateAPIView):
    """
    Lists responses or creates a reply if
    authenticated.
    """
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Response.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ResponseDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieves a reply or deletes it
    if user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ResponseSerializer
    queryset = Response.objects.all()
