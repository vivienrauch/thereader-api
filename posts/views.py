from rest_framework import generics
from thereader_api import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    """
    Lists all posts or creates a post if logged in.
    The perform_create method associates the post with the logged in user.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProfileDetail(APIView):
    """
    Retrieves or updates a profile if you are the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
334