# ... final da sua função buscar_bula_medicamento anterior ...
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
        # 2. Passa os novos dados vindo da tela preenchendo a instância antiga (instance=med)
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
        # 5. Se for o primeiro clique (GET), abre o formulário preenchido com os dados atuais da Loratadina
        form = MedicamentoForm(instance=med)
        
    return render(request, "medicamento/cadastrar.html", {"form": form, "med": med})