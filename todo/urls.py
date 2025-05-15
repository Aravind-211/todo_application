from django.urls import path
from .views import (
    custom_login_view,
    TaskListView,
    TaskCreateView,
    TaskDeleteView,
    TaskCompleteView,
    login_view,
    register_view,
    logout_view
)

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('add/', TaskCreateView.as_view(), name='add'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='complete'),
    path('login/', custom_login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
