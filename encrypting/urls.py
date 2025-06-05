from django.urls import path
from . import views

urlpatterns = [
    path('hash/', views.hash_view, name='hash_view'),
    path('hash/text/', views.hash_text, name='hash_text'),
    path('hash/collision/', views.find_collision_view, name='find_collision'),
] 