from django.urls import path
from . import views

urlpatterns = [
    path('plot_response/', views.plot_response_api, name='plot_response'),
]