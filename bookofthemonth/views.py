from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import BookOfTheMonth
from .serializers import BookOfTheMonthSerializer


class IsAdminOrReadOnlyOrUserRetrieve(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class BookOfTheMonthList(generics.ListCreateAPIView):
    serializer_class = BookOfTheMonthSerializer
    permission_classes = [IsAdminOrReadOnlyOrUserRetrieve]
    queryset = BookOfTheMonth.objects.all()

    filter_backends = [
        DjangoFilterBackend,
    ]


class BookOfTheMonthDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookOfTheMonthSerializer
    permission_classes = [IsAdminOrReadOnlyOrUserRetrieve]
    queryset = BookOfTheMonth.objects.all()
