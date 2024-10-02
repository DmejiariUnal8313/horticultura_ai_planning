from django.urls import path
from .views import index, generar_plan, ver_plan, simulacion, mostrar_dominio, mostrar_problema, heuristica_aplicada

urlpatterns = [
    path('', index, name='index'),
    path('generar_plan/', generar_plan, name='generar_plan'),
    path('ver_plan/', ver_plan, name='ver_plan'),
    path('simulacion/', simulacion, name='simulacion'),
    path('dominio/', mostrar_dominio, name='mostrar_dominio'),
    path('problema/', mostrar_problema, name='mostrar_problema'),
    path('heuristica_aplicada/', heuristica_aplicada, name='heuristica_aplicada'),
]