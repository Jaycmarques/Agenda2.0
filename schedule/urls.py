from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('create-meeting/', views.create_meeting, name='create_meeting'),
]
