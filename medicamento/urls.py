from django.urls import path

from . import views

app_name = "medicamento"

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.listar, name="listar"),           
    path("cadastrar/", views.cadastrar, name="cadastrar"), 
    path("<int:pk>/", views.detalhe, name="detalhe"), 
    path("<int:pk>/remover/", views.remover, name="remover"),
    path("alertas/", views.alertas, name="alertas"),
    path("alertas/<int:pk>/confirmar/", views.confirmar_uso, name="confirmar_uso"),
    path("bula/<str:nome_medicamento>/", views.buscar_bula_medicamento, name="buscar_bula"),
]
