from django.urls import path
from . import views

urlpatterns = [
    path('inicial/', views.inicial, name='inicial'),
    path('baixar/', views.baixar_arquivos, name='baixar'),
    path('planilhas-baixadas/', views.planilhas_baixadas, name='visualizar_planilhas_baixadas'),
    path('coletar_dados_planilha/<str:arquivo>/', views.coletar_dados_planilha, name='coletar_dados_planilha'),
]