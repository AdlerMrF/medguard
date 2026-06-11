from unittest.mock import patch

from medicamento.traducao import (
    NAO_INFORMADO,
    traduzir_nome_para_ingles,
    traduzir_texto_para_portugues,
)


class TestTraduzirNome:
    def test_principio_ativo_conhecido(self):
        assert traduzir_nome_para_ingles("paracetamol") == "acetaminophen"

    def test_ignora_acentos_e_maiusculas(self):
        assert traduzir_nome_para_ingles("  ÁCIDO Acetilsalicílico ") == "aspirin"

    def test_marca_sem_traducao_natural_cai_no_principio_ativo(self):
        # Nome próprio que não se traduz naturalmente.
        assert traduzir_nome_para_ingles("Novalgina") == "dipyrone"

    def test_nome_desconhecido_retorna_original(self):
        assert traduzir_nome_para_ingles("xyzinexistente") == "xyzinexistente"

    def test_nome_vazio(self):
        assert traduzir_nome_para_ingles("") == ""


class TestTraduzirTexto:
    def test_nao_informado_passa_direto(self):
        assert traduzir_texto_para_portugues(NAO_INFORMADO) == NAO_INFORMADO

    def test_vazio_passa_direto(self):
        assert traduzir_texto_para_portugues("") == ""

    @patch("deep_translator.GoogleTranslator")
    def test_usa_tradutor_quando_disponivel(self, mock_translator):
        mock_translator.return_value.translate.return_value = "Alívio da dor"
        assert traduzir_texto_para_portugues("Pain relief") == "Alívio da dor"
        mock_translator.assert_called_once_with(source="en", target="pt")

    @patch("deep_translator.GoogleTranslator", side_effect=Exception("sem internet"))
    def test_falha_no_tradutor_retorna_texto_original(self, _mock):
        # Se a tradução falhar, a aplicação não quebra: devolve o original.
        assert traduzir_texto_para_portugues("Pain relief") == "Pain relief"
