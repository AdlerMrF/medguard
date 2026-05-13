import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestBulaAPIView:

    def setup_method(self):
        self.client = Client()

    @patch("medicamento.views.requests.get")
    def test_buscar_bula_sucesso(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "results": [
                {
                    "purpose": ["Alívio da dor e febre"],
                    "warnings": ["Não usar com álcool"],
                    "adverse_reactions": ["Náusea, tontura"],
                }
            ]
        }
        mock_get.return_value = mock_response

        url = reverse("medicamento:buscar_bula", kwargs={"nome_medicamento": "paracetamol"})
        response = self.client.get(url)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["nome"] == "paracetamol"
        assert data["para_qual_finalidade"] == "Alívio da dor e febre"
        assert data["avisos"] == "Não usar com álcool"
        assert data["efeitos_adversos"] == "Náusea, tontura"

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
