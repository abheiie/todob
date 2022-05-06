from django.urls import path
from . import rest_views

urlpatterns = [

    # Auth paths
    path('register/', rest_views.Register.as_view()),
    path('login/', rest_views.Login.as_view()),

    # Main paths
    path('todos/', rest_views.TodoList.as_view()),
    path('todos/<int:id>/', rest_views.TodoDetail.as_view()),
]