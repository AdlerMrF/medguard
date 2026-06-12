from datetime import datetime

import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET
from requests.exceptions import Timeout

from .forms import MedicamentoForm
from .models import HorarioMedicamento, Medicamento, RegistroUso


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
    medicamentos = Medicamento.objects.prefetch_related("horarios").all()
    nome = request.GET.get("nome")
    importancia = request.GET.get("importancia")

    if nome:
        medicamentos = medicamentos.filter(nome__icontains=nome)
    if importancia:
        medicamentos = medicamentos.filter(importancia=importancia)

    return render(request, "medicamento/listar.html", {
        "medicamentos": medicamentos,
        "filtros": {"nome": nome or "", "importancia": importancia or ""},
    })


def cadastrar(request):
    if request.method == "POST":
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            med = form.save()
            horarios_raw = form.cleaned_data.get("horarios_texto", "")
            if horarios_raw:
                lista_horarios = horarios_raw.split(",") if isinstance(horarios_raw, str) else horarios_raw
                for h in lista_horarios:
                    h = h.strip()
                    if h:
                        HorarioMedicamento.objects.create(medicamento=med, horario=h)

            messages.success(request, f"Medicamento '{med.nome}' cadastrado com sucesso!")
            return redirect("medicamento:listar")
    else:
        form = MedicamentoForm()

    return render(request, "medicamento/cadastrar.html", {"form": form})


def detalhe(request, pk):
    med = get_object_or_404(Medicamento, pk=pk)
    registros = med.registros.order_by("-data")[:10]
    return render(request, "medicamento/detalhe.html", {
        "med": med,
        "registros": registros,
    })


def remover(request, pk):
    med = get_object_or_404(Medicamento, pk=pk)
    if request.method == "POST":
        name = med.nome
        med.delete()
        messages.success(request, f"Medicamento '{name}' excluído com sucesso.")
        return redirect("medicamento:listar")
    return render(request, "medicamento/confirmar_exclusao.html", {"med": med})


def alertas(request):
    agora = timezone.localtime(timezone.now()).time()
    dt_agora = datetime.combine(datetime.today(), agora)
    medicamentos_alerta = []
    for med in Medicamento.objects.prefetch_related("horarios").all():
        for h in med.horarios.all():
            dt_h = datetime.combine(datetime.today(), h.horario)
            if abs((dt_agora - dt_h).total_seconds()) <= 600:
                medicamentos_alerta.append(med)
                break
    return render(request, "medicamento/alertas.html", {
        "alertas": medicamentos_alerta,
        "agora": agora.strftime("%H:%M"),
    })


def confirmar_uso(request, pk):
    med = get_object_or_404(Medicamento, pk=pk)
    if request.method == "POST":
        tomado_status = request.POST.get("tomado") == "true" or request.POST.get("tomado") == "on"
        RegistroUso.objects.create(
            medicamento=med,
            data=timezone.now().date(),
            horario=timezone.localtime(timezone.now()).time(),
            tomado=tomado_status
        )
        status = "tomado" if tomado_status else "não tomado"
        messages.info(request, f"{med.nome} registrado as {status}.")
        return redirect("medicamento:alertas")
    return render(request, "medicamento/confirmar_uso.html", {"med": med})


@require_GET
def buscar_bula_medicamento(request, nome_medicamento):
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f'openfda.generic_name:"{nome_medicamento}" OR openfda.brand_name:"{nome_medicamento}"', "limit": 1}
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                bula = results[0]
                return JsonResponse({
                    "name": nome_medicamento,
                    "para_qual_finalidade": bula.get("purpose", ["Não informado"])[0],
                    "avisos": bula.get("warnings", ["Não informado"])[0],
                    "efeitos_adversos": bula.get("adverse_reactions", ["Não informado"])[0],
                })
        return JsonResponse({"erro": "Medicamento não encontrado na API"}, status=404)
    except Timeout:
        return JsonResponse({"erro": "Tempo de requisição esgotado (Timeout)"}, status=504)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)


def alterar(request, pk):
    med = get_object_or_404(Medicamento, pk=pk)
    if request.method == "POST":
        med.nome = request.POST.get("nome", med.nome)
        med.dose = request.POST.get("dose", med.dose)
        med.importancia = request.POST.get("importancia", med.importancia)
        med.save()
        messages.success(request, f"Medicamento '{med.nome}' alterado com sucesso!")
        return redirect("medicamento:listar")
    return redirect("medicamento:listar")


def historico_uso(request):
    registros = RegistroUso.objects.select_related("medicamento").order_by("-data", "-horario")
    return render(request, "medicamento/historico.html", {"registros": registros})


def historico_clinico(request):
    return render(request, "medicamento/historico_clinico.html")
