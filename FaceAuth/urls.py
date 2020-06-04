from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login'),
    path('face_detect', views.face_detect_view, name='face_detect'),
    path('face_auth', views.face_auth_view, name='face_auth'),
    
]