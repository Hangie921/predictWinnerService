from django.urls import path, include
from . import views


urlpatterns = [
    path("weight/", views.CreateWeightView.as_view(), name="weight"),
    # path("weight/delete/<int:pk>/", views.Delete.as_view(), name="delete-weight"),
]