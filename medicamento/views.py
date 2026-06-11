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
    # O usuário digita em português; a openFDA só entende o termo em inglês.
    nome_ingles = traduzir_nome_para_ingles(nome_medicamento)
    url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": (
            f'openfda.generic_name:"{nome_ingles}" '
            f'OR openfda.brand_name:"{nome_ingles}"'
        ),
        "limit": 1,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return JsonResponse({"erro": "Esse medicamento não foi encontrado"}, status=404)
        bula = results[0]
        # A bula vem em inglês; traduzimos cada campo de volta para português.
        info = {
            "nome": nome_medicamento,
            "nome_consultado": nome_ingles,
            "para_qual_finalidade": traduzir_texto_para_portugues(
                bula.get("purpose", [NAO_INFORMADO])[0]
            ),
            "avisos": traduzir_texto_para_portugues(
                bula.get("warnings", [NAO_INFORMADO])[0]
            ),
            "efeitos_adversos": traduzir_texto_para_portugues(
                bula.get("adverse_reactions", [NAO_INFORMADO])[0]
            ),
        }
        return JsonResponse(info)
    except requests.exceptions.Timeout:
        return JsonResponse({"erro": "Tempo de resposta da API excedido"}, status=504)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"erro": f"Erro ao consultar a API: {str(e)}"}, status=502)


# =====================================================================
# 🛠️ NOVA FUNCIONALIDADE: ALTERAR / EDITAR CADASTRO DE MEDICAMENTO
# =====================================================================
def alterar(request, pk):
    """Busca um medicamento existente e altera seus dados e horários associados."""
    # 1. Puxa do banco o medicamento antigo pelo ID (pk)
    med = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == "POST":
        # 2. Passa os novos dados preenchendo a instância antiga (instance=med)
        form = MedicamentoForm(request.POST, instance=med)
        
        if form.is_valid():
            # Salva as atualizações do nome, dose e importância do medicamento
            med = form.save()
            
            # 3. Limpa os horários antigos associados a ele para não acumular lixo no banco
            HorarioMedicamento.objects.filter(medicamento=med).delete()
            
            # 4. Processa e adiciona a nova lista de horários enviados
            horarios = form.cleaned_data.get("horarios_texto", [])
            for h in horarios:
                if ":" in h:
                    hora, minuto = h.split(":")
                    HorarioMedicamento.objects.create(
                        medicamento=med,
                        horario=f"{hora}:{minuto}",
                    )
            
            messages.success(request, f"Medicamento '{med.nome}' alterado com sucesso!")
            return redirect("medicamento:listar")
    else:
        # 5. Se for o primeiro clique (GET), abre o formulário preenchido com os dados atuais
        form = MedicamentoForm(instance=med)
        
    return render(request, "medicamento/cadastrar.html", {"form": form, "med": med})