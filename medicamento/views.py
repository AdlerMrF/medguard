import requests

from datetime import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_GET


from .forms import FiltroForm, MedicamentoForm, RegistroUsoForm
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
            horarios = form.cleaned_data["horarios_texto"]
            for h in horarios:
                hora, minuto = h.split(":")
                HorarioMedicamento.objects.create(
                    medicamento=med,
                    horario=f"{hora}:{minuto}",
                )
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
        nome = med.nome
        med.delete()
        messages.success(request, f"Medicamento '{nome}' excluído com sucesso.")
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
        form = RegistroUsoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.medicamento = med
            registro.horario = timezone.localtime(timezone.now()).time()
            registro.save()
            status = "tomado" if registro.tomado else "não tomado"
            messages.info(request, f"{med.nome} registrado como {status}.")
            return redirect("medicamento:alertas")
    else:
        form = RegistroUsoForm()

    return render(request, "medicamento/confirmar_uso.html", {"med": med, "form": form})

@require_GET
def buscar_bula_medicamento(request, nome_medicamento):
    url = "http://api.fda.gov/drug/label.json"
    params = {
        "search": f"openfda.brand_name:{nome_medicamento}",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return JsonResponse({"erro": "Esse medicamento não foi encontrado"}, status=404)

        bula = results[0]
        info = {
            "nome": nome_medicamento,
            "para_qual_finalidade": bula.get("purpose", ["Não informado"])[0],
            "avisos": bula.get("warnings", ["Não informado"])[0],
            "efeitos_adversos": bula.get("adverse_reactions", ["Não informado"])[0],
        }
        return JsonResponse(info)

    except requests.exceptions.Timeout:
        return JsonResponse({"erro": "Tempo de resposta da API excedido"}, status=504)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"erro": f"Erro ao consultar a API: {str(e)}"}, status=502)