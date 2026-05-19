from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('toggle/', views.toggle_habit_ajax, name='toggle_habit_ajax'),
]