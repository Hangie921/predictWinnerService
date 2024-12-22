from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/resource', views.get_resource, name='get_resource'),
    path('api/resource', views.post_resource, name='post_resource'),
    path('api/resource', views.put_resource, name='put_resource'),
    path('api/resource', views.delete_resource, name='delete_resource'),
]