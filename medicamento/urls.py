from django.urls import path
from . import views

app_name = "medicamento"

urlpatterns = [
    path("", views.index, name="index"),
    path("medicamentos/", views.listar, name="listar"),
    path("medicamentos/cadastrar/", views.cadastrar, name="cadastrar"),
    path("medicamentos/<int:pk>/", views.detalhe, name="detalhe"),
    path("medicamentos/<int:pk>/remover/", views.remover, name="remover"),
    path("alertas/", views.alertas, name="alertas"),
    path("medicamentos/<int:pk>/confirmar/", views.confirmar_uso, name="confirmar_uso"),
    path("medicamentos/bula/<str:nome_medicamento>/", views.buscar_bula_medicamento, name="buscar_bula"),
    path("medicamentos/<int:pk>/alterar/", views.alterar, name="alterar"),
    path("medicamentos/historico/", views.historico_uso, name="historico_uso"),
    
    # Nova rota para o Prontuário / Histórico Clínico
    path("historico-clinico/", views.historico_clinico, name="historico_clinico"),
]