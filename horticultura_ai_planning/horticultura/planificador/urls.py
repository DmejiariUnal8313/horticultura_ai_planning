from django.urls import path
from . import views

urlpatterns = [
    path('', views.generar_plan, name='generar_plan'),
]