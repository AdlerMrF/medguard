
from django.contrib import admin

from .models import HistoricoEvento, HorarioMedicamento, Medicamento, RegistroUso


class HorarioInline(admin.TabularInline):
    model = HorarioMedicamento
    extra = 1


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "dose", "importancia", "criado_em")
    list_filter = ("importancia",)
    search_fields = ("nome",)
    inlines = [HorarioInline]


@admin.register(HorarioMedicamento)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("medicamento", "horario")
    list_filter = ("medicamento",)


@admin.register(RegistroUso)
class RegistroUsoAdmin(admin.ModelAdmin):
    list_display = ("medicamento", "data", "horario", "tomado")
    list_filter = ("tomado", "data")


@admin.register(HistoricoEvento)
class HistoricoEventoAdmin(admin.ModelAdmin):
    list_display = ("nome_medicamento", "tipo", "importancia", "data", "horario")
    list_filter = ("tipo", "importancia", "data")
    search_fields = ("nome_medicamento",)
