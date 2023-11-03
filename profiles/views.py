from rest_framework import generics
from thereader_api import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    """
    Lists all profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(APIView):
    """
    Retrieves or updates a profile if you are the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
