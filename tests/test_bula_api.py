import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestBulaAPIView:

    def setup_method(self):
        self.client = Client()

    # A traducao do texto da bula é isolada (identidade) para o teste não
    # depender de rede; a logica de traducao tem testes próprios.
    @patch("medicamento.views.traduzir_texto_para_portugues", side_effect=lambda t: t)
    @patch("medicamento.views.requests.get")
    def test_buscar_bula_sucesso(self, mock_get, _mock_traduz):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "results": [
                {
                    "purpose": ["Pain and fever relief"],
                    "warnings": ["Do not use with alcohol"],
                    "adverse_reactions": ["Nausea, dizziness"],
                }
            ]
        }
        mock_get.return_value = mock_response

        url = reverse("medicamento:buscar_bula", kwargs={"nome_medicamento": "paracetamol"})
        response = self.client.get(url)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["nome"] == "paracetamol"
        # O nome PT foi convertido para o termo em inglês usado na consulta.
        assert data["nome_consultado"] == "acetaminophen"
        assert data["para_qual_finalidade"] == "Pain and fever relief"
        assert data["avisos"] == "Do not use with alcohol"
        assert data["efeitos_adversos"] == "Nausea, dizziness"

        # A openFDA foi consultada com o termo traduzido, não com o português.
        _, kwargs = mock_get.call_args
        assert "acetaminophen" in kwargs["params"]["search"]

    @patch("medicamento.views.requests.get")
    def test_buscar_bula_nao_encontrado(self, mock_get):
        """Deve retornar 404 quando medicamento não é encontrado na API."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        url = reverse("medicamento:buscar_bula", kwargs={"nome_medicamento": "xyzinexistente"})
        response = self.client.get(url)

        assert response.status_code == 404
        data = json.loads(response.content)
        assert "erro" in data

    @patch("medicamento.views.requests.get")
    def test_buscar_bula_timeout(self, mock_get):
        """Deve retornar 504 quando a API externa demorar demais."""
        import requests as req_lib
        mock_get.side_effect = req_lib.exceptions.Timeout()

        url = reverse("medicamento:buscar_bula", kwargs={"nome_medicamento": "paracetamol"})
        response = self.client.get(url)

        assert response.status_code == 504
        data = json.loads(response.content)
        assert "erro" in data
