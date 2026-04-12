
import pytest
from django.core.exceptions import ValidationError

from medicamento.models import HorarioMedicamento, Medicamento, RegistroUso


@pytest.mark.django_db
class TestMedicamentoCriacao:
    def test_criar_medicamento_valido(self):
        med = Medicamento.objects.create(
            nome="Metformina",
            dose="850mg",
            importancia="medio",
        )
        assert med.pk is not None
        assert med.nome == "Metformina"
        assert med.dose == "850mg"
        assert med.importancia == "medio"

    def test_str_retorna_nome_e_dose(self):
        med = Medicamento(nome="Aspirina", dose="100mg", importancia="baixo")
        assert "Aspirina" in str(med)
        assert "100mg" in str(med)

    def test_criar_horario_associado(self, medicamento_basico):
        horarios = medicamento_basico.horarios.all()
        assert horarios.count() == 2

    def test_str_horario(self, medicamento_basico):
        h = medicamento_basico.horarios.first()
        assert "Losartana" in str(h)

    def test_criar_registro_uso_tomado(self, medicamento_basico):
        registro = RegistroUso.objects.create(
            medicamento=medicamento_basico,
            horario="08:00:00",
            tomado=True,
        )
        assert registro.tomado is True
        assert "✅" in str(registro)

    def test_criar_registro_uso_nao_tomado(self, medicamento_basico):
        registro = RegistroUso.objects.create(
            medicamento=medicamento_basico,
            horario="08:00:00",
            tomado=False,
        )
        assert registro.tomado is False
        assert "❌" in str(registro)


@pytest.mark.django_db
class TestMedicamentoValidacao:
    def test_nome_vazio_levanta_validation_error(self):
        med = Medicamento(nome="", dose="1 comprimido", importancia="alto")
        with pytest.raises(ValidationError):
            med.full_clean()

    def test_nome_espacos_levanta_validation_error(self):
        med = Medicamento(nome="   ", dose="1 comprimido", importancia="alto")
        with pytest.raises(ValidationError):
            med.full_clean()

    def test_dose_vazia_levanta_validation_error(self):
        med = Medicamento(nome="Dipirona", dose="", importancia="medio")
        with pytest.raises(ValidationError):
            med.full_clean()

    def test_importancia_invalida_levanta_validation_error(self):
        med = Medicamento(nome="Ibuprofeno", dose="400mg", importancia="urgente")
        with pytest.raises(ValidationError):
            med.full_clean()


@pytest.mark.django_db
class TestMedicamentoCasosLimite:
    def test_multiplos_horarios(self, medicamento_basico):
        HorarioMedicamento.objects.create(
            medicamento=medicamento_basico, horario="12:00:00"
        )
        assert medicamento_basico.horarios.count() == 3

    def test_todos_niveis_importancia_validos(self):
        for nivel in ("baixo", "medio", "alto"):
            med = Medicamento(nome="Teste", dose="1x", importancia=nivel)
            med.full_clean()

    def test_remover_medicamento_cascateia_horarios(self, medicamento_basico):
        pk = medicamento_basico.pk
        medicamento_basico.delete()
        assert HorarioMedicamento.objects.filter(medicamento_id=pk).count() == 0

    def test_observacoes_opcional(self):
        med = Medicamento.objects.create(
            nome="Vitamina C",
            dose="500mg",
            importancia="baixo",
        )
        assert med.observacoes == ""

    def test_busca_por_nome_parcial(self, medicamento_basico, medicamento_baixo):
        resultado = Medicamento.objects.filter(nome__icontains="losar")
        assert resultado.count() == 1
        assert resultado.first().nome == "Losartana"

    def test_filtro_por_importancia(self, medicamento_basico, medicamento_baixo):
        altos = Medicamento.objects.filter(importancia="alto")
        baixos = Medicamento.objects.filter(importancia="baixo")
        assert altos.count() == 1
        assert baixos.count() == 1
