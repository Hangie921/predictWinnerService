from django.urls import path, include, register_converter
from . import views, converters

register_converter(converters.FloatUrlParameterConverter, 'float')

urlpatterns = [
    path("weight/", views.CreateWeightView.as_view(), name="weight"),
    # path("weight/delete/<int:pk>/", views.Delete.as_view(), name="delete-weight"),
    # path("history/", views.CreateHistoryView.as_view(), name="history"),
    path("prediction", views.get_prediction, name="prediction"),
]