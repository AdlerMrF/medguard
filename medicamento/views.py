from datetime import datetime

import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from .forms import FiltroForm, MedicamentoForm, RegistroUsoForm
from .models import HorarioMedicamento, Medicamento, RegistroUso
from .traducao import (
    NAO_INFORMADO,
    traduzir_nome_para_ingles,
    traduzir_texto_para_portugues,
)


def index(request):
    total = Medicamento.objects.count()
    altos = Medicamento.objects.filter(importancia="alto").count()
    hoje = timezone.now().date()
    tomados_hoje = RegistroUso.objects.filter(data=hoje, tomado=True).count()

    context = {
        "total_medicamentos": total,
        "total_altos": altos,
        "tomados_hoje": tomados_hoje,
    }
    return render(request, "medicamento/index.html", context)


def listar(request):
    form = FiltroForm(request.GET or None)
    medicamentos = Medicamento.objects.prefetch_related("horarios").all()

    if form.is_valid():
        nome = form.cleaned_data.get("nome")
        importancia = form.cleaned_data.get("importancia")
        if nome:
            medicamentos = medicamentos.filter(nome__icontains=nome)
        if importancia:
            medicamentos = medicamentos.filter(importancia=importancia)

    return render(request, "medicamento/listar.html", {
        "medicamentos": medicamentos,
        "form": form,
    })


def cadastrar(request):
    if request.method == "POST":
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            med = form.save()
            horarios = form.cleaned_data["horarios_texto"