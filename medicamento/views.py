from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Medicamento  # Certifique-se de que o nome do modelo está correto

def alterar_medicamento(request, pk):
    """Busca o medicamento pelo ID (pk) e altera seus dados no banco."""
    # 1. Busca o medicamento atual no banco de dados
    medicamento = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == "POST":
        # 2. Pega os dados novos que o usuário digitou no formulário HTML
        novo_nome = request.POST.get("nome")
        nova_dose = request.POST.get("dose")
        nova_importancia = request.POST.get("importancia")
        
        # Validação simples
        if not novo_nome or not nova_dose:
            messages.error(request, "Nome e Dose são obrigatórios!")
            return redirect('alterar_medicamento', pk=pk)
            
        # 3. ATUALIZAÇÃO NO BANCO DE DADOS: Altera as propriedades do objeto
        medicamento.nome = novo_nome
        medicamento.dose = nova_dose
        medicamento.importancia = nova_importancia
        
        # 4. Salva de fato no arquivo db.sqlite3
        medicamento.save()
        
        messages.success(request, "Medicamento alterado com sucesso!")
        return redirect('lista_medicamentos') # Redireciona de volta para a tabela
        
    return render(request, 'medicamento/alterar_medicamento.html', {'medicamento': medicamento})