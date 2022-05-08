from django.urls import include, path
from django.urls import re_path as url
from . import rest_views

urlpatterns = [

    url(r'v1/', include([
        # Auth paths
        path('register/', rest_views.Register.as_view()),
        path('login/', rest_views.Login.as_view()),
        path('auth-user/', rest_views.AuthUser.as_view()),

        # Main todo paths
        path('todos/', rest_views.TodoList.as_view()),
        path('todos/<int:id>/', rest_views.TodoDetail.as_view()),
    ]))
]
