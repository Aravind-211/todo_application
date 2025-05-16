from django.urls import path
from .views import (
    custom_login_view,
    TaskListView,
    TaskCreateView,
    delete_task,
    TaskCompleteView,
    TaskUpdateView,
    TaskIncompleteView,
    login_view,
    register_view,
    logout_view
)

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('add/', TaskCreateView.as_view(), name='add'),
    path('delete/<int:pk>/', delete_task, name='delete'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='complete'),
    path('incomplete/<int:pk>/', TaskIncompleteView.as_view(), name='incomplete'),  
    path('edit/<int:pk>/', TaskUpdateView.as_view(), name='edit'),                  
    path('login/', custom_login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]

