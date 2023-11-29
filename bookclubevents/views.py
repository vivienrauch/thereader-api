from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from thereader_api.permissions import IsOwnerOrReadOnly
from .models import BookClubEvent
from .serializers import BookClubEventSerializer


class BookClubEventList(generics.ListCreateAPIView):
    """
    Lists book related events or allows to create an
    event if authenticated.
    """
    serializer_class = BookClubEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = BookClubEvent.objects.annotate(
        response_count=Count('responses', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    ordering_fields = [
        'response_count',
        'responses__created_at',
        'owner__followed__owner__profile'
    ]
    filterset_fields = [
        'owner__profile',
        'owner__followed__owner__profile'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookClubEventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a book related event,
    if authenticated and owning the event, you can modify or delete it.
    """
    serializer_class = BookClubEventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = BookClubEvent.objects.annotate(
        response_count=Count('responses', distinct=True),
    ).order_by('created_at')
