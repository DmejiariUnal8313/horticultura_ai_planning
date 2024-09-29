from django.urls import path
from . import views

urlpatterns = [
    path('', views.generar_plan, name='generar_plan'),
    path('dominio/', views.mostrar_dominio, name='mostrar_dominio'),
    path('index/', views.index, name='index'),
    path('plan/', views.generar_plan, name='generar_plan'),
    path('problema/', views.mostrar_problema, name='mostrar_problema'),
    
]