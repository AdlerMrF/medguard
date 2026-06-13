from django.core.exceptions import ValidationError
from django.db import models

IMPORTANCIA = [
    ("baixo", "Baixo"),
    ("medio", "Médio"),
    ("alto", "Alto"),
]


class Medicamento(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Medicamento")
    dose = models.CharField(max_length=200, verbose_name="Dose")
    importancia = models.CharField(
        max_length=10,
        choices=IMPORTANCIA,
        default="medio",
        verbose_name="Nível de Importância",
    )
    observacoes = models.TextField(blank=True, default="", verbose_name="Observações")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ["-importancia", "nome"]

    def __str__(self):
        return f"{self.nome} — {self.dose}"

    def clean(self):
        if not self.nome or not self.nome.strip():
            raise ValidationError({"nome": "O nome do medicamento não pode ser vazio."})
        if not self.dose or not self.dose.strip():
            raise ValidationError({"dose": "A dose não pode ser vazia."})
        if self.importancia not in ("baixo", "medio", "alto"):
            raise ValidationError({"importancia": "Importância inválida."})


class HorarioMedicamento(models.Model):
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        related_name="horarios",
    )
    horario = models.TimeField(verbose_name="Horário")

    class Meta:
        verbose_name = "Horário"
        verbose_name_plural = "Horários"
        ordering = ["horario"]

    def __str__(self):
        return f"{self.medicamento.nome} às {self.horario.strftime('%H:%M')}"


class HistoricoEvento(models.Model):
    """Snapshot de eventos do medicamento: sobrevive à exclusão do registro original."""

    TIPO_EVENTO = [
        ("tomado", "Tomado"),
        ("nao_tomado", "Não tomado"),
        ("excluido", "Excluído"),
    ]

    tipo = models.CharField(
        max_length=12,
        choices=TIPO_EVENTO,
        verbose_name="Tipo de Evento",
    )
    nome_medicamento = models.CharField(max_length=200, verbose_name="Nome do Medicamento")
    dose = models.CharField(max_length=200, verbose_name="Dose")
    importancia = models.CharField(
        max_length=10,
        choices=IMPORTANCIA,
        verbose_name="Nível de Importância",
    )
    observacoes = models.TextField(blank=True, default="", verbose_name="Observações do Medicamento")
    observacao_registro = models.TextField(blank=True, default="", verbose_name="Observação do Registro")
    data = models.DateField(auto_now_add=True, verbose_name="Data")
    horario = models.TimeField(verbose_name="Horário")

    class Meta:
        verbose_name = "Evento do Histórico"
        verbose_name_plural = "Eventos do Histórico"
        ordering = ["-data", "-horario"]

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.nome_medicamento} - {self.data}"


class RegistroUso(models.Model):
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        related_name="registros",
    )
    horario = models.TimeField(verbose_name="Horário")
    tomado = models.BooleanField(default=False, verbose_name="Tomado?")
    data = models.DateField(auto_now_add=True)
    observacao = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Registro de Uso"
        verbose_name_plural = "Registros de Uso"
        ordering = ["-data", "horario"]

    def __str__(self):
        status = "✅" if self.tomado else "❌"
        return f"{status} {self.medicamento.nome} - {self.data}"
