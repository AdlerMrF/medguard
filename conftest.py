import pytest
from medicamento.models import Medicamento, HorarioMedicamento


@pytest.fixture
def medicamento_basico(db):
    med = Medicamento.objects.create(
        nome="Losartana",
        dose="50mg",
        importancia="alto",
    )
    HorarioMedicamento.objects.create(medicamento=med, horario="08:00:00")
    HorarioMedicamento.objects.create(medicamento=med, horario="20:00:00")
    return med


@pytest.fixture
def medicamento_baixo(db):
    med = Medicamento.objects.create(
        nome="Vitamina D",
        dose="1 cápsula",
        importancia="baixo",
    )
    HorarioMedicamento.objects.create(medicamento=med, horario="07:00:00")
    return med
