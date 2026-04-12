from django import forms

from .models import Medicamento, HorarioMedicamento, RegistroUso


class MedicamentoForm(forms.ModelForm):
    """Formulário para criação e edição de medicamentos."""

    horarios_texto = forms.CharField(
        label="Horários de uso",
        help_text="Informe cada um dos horários separados por vírgula",
        widget=forms.TextInput(attrs={"placeholder": "08:00, 14:00, 20:00"}),
    )

    class Meta:
        model = Medicamento
        fields = ["nome", "dose", "importancia", "observacoes"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex: Losartana"}),
            "dose": forms.TextInput(attrs={"placeholder": "Ex: 1 comprimido, 5ml"}),
            "observacoes": forms.Textarea(attrs={"rows": 3, "placeholder": "Observações opcionais..."}),
        }
        labels = {
            "nome": "Nome do Medicamento",
            "dose": "Dose",
            "importancia": "Nível de Importância",
            "observacoes": "Observações",
        }

    def clean_horarios_texto(self):
        valor = self.cleaned_data.get("horarios_texto", "")
        horarios = [h.strip() for h in valor.split(",") if h.strip()]
        if not horarios:
            raise forms.ValidationError("Informe ao menos um horário.")
        for h in horarios:
            try:
                hora, minuto = h.split(":")
                assert 0 <= int(hora) <= 23
                assert 0 <= int(minuto) <= 59
            except Exception:
                raise forms.ValidationError(f"Horário inválido '{h}', use o formato HH:MM")
        return horarios

    def clean_nome(self):
        nome = self.cleaned_data.get("nome", "").strip()
        if not nome:
            raise forms.ValidationError("O nome não pode ser vazio.")
        return nome

    def clean_dose(self):
        dose = self.cleaned_data.get("dose", "").strip()
        if not dose:
            raise forms.ValidationError("A dose não pode ser vazia.")
        return dose


class FiltroForm(forms.Form):
    nome = forms.CharField(
        required=False,
        label="Buscar por nome",
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome..."}),
    )

    importancia = forms.ChoiceField(
        required=False,
        label="Buscar por importância",
        choices=[
            ("", "Todos"),
            ("baixo", "Baixo"),
            ("medio", "Médio"),
            ("alto", "Alto"),
        ],
    )


class RegistroUsoForm(forms.ModelForm):
    class Meta:
        model = RegistroUso
        fields = ["tomado", "observacao"]
        labels = {
            "tomado": "Tomou o medicamento?",
            "observacao": "Observação",
        }
        widgets = {
            "observacao": forms.Textarea(attrs={"rows": 2}),
        }
