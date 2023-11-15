from rest_framework import generics, permissions
from thereader_api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer
from django.core.exceptions import ValidationError


class FollowerList(generics.ListCreateAPIView):
    """
    List all followers, i.e. all instances of a user
    following another user.
    Create a follower, i.e. follow a user if logged in.
    Perform_create: associate the current logged in user with a follower.
    """
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        followed_user = serializer.validated_data['followed']
        if followed_user == self.request.user:
            raise serializers.ValidationError("Sorry! You can't follow yourself.")
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower
    No Update view, as we either follow or unfollow users
    Destroy a follower, i.e. unfollow someone if owner.
    """
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
