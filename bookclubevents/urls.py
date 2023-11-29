from django.urls import path
from bookclubevents import views


urlpatterns = [
    path('bookclubevents/', views.BookClubEventList.as_view()),
    path('bookclubevents/<int:pk>/', views.BookClubEventDetail.as_view()),
]
