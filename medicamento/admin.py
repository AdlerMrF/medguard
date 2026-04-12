
from django.contrib import admin
from .models import Medicamento, HorarioMedicamento, RegistroUso


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
