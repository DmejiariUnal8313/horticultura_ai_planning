from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generar_plan', views.generar_plan, name='generar_plan'),
    path('ver_plan', views.ver_plan, name='ver_plan'),
    path('mostrar_dominio_y_problemas', views.mostrar_dominio_y_problemas, name='mostrar_dominio_y_problemas'),
    path('heuristica', views.heuristica, name='heuristica'),
]

