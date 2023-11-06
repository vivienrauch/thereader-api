from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import BookOfTheMonth
from .serializers import BookOfTheMonthSerializer


class BookOfTheMonthList(generics.ListCreateAPIView):
    serializer_class = BookOfTheMonthSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = BookOfTheMonth.objects.all()

    filter_backends = [
        DjangoFilterBackend,
    ]


class BookOfTheMonthDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookOfTheMonthSerializer
    queryset = BookOfTheMonth.objects.all()
