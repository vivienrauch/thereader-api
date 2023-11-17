from django.urls import path
from bookofthemonth import views


urlpatterns = [
    path('bookofthemonth/', views.BookOfTheMonthList.as_view()),
    path('bookofthemonth/<int:pk>/', views.BookOfTheMonthDetail.as_view()),
]