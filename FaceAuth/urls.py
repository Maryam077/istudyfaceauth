from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('face_detect', views.face_detect_view, name='face_detect'),
]