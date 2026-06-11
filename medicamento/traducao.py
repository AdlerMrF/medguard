"""Traducao de medicamentos entre portugues e ingles.

Fluxo:
1. O usuario digita o nome do medicamento em portugues.
2. `traduzir_nome_para_ingles` converte para o termo em ingles reconhecido
   pela openFDA, usando o arquivo de dados `data/medicamentos_pt_en.json`.
   Nomes proprios/marcas sem traducao natural caem no principio ativo;
   se nao houver correspondencia, devolve o proprio nome digitado.
3. A openFDA responde a bula em ingles e `traduzir_texto_para_portugues`
   traduz os textos de volta para o portugues antes de exibir ao usuario.
"""

import json
import unicodedata
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "medicamentos_pt_en.json"

# Valor sentinela usado pela view quando um campo da bula nao foi informado.
NAO_INFORMADO = "Não informado"

# Limite de caracteres por requisicao do tradutor (GoogleTranslator aceita 5000).
_LIMITE_TRADUCAO = 4900


def _normalizar(texto):
    """Minusculas, sem acentos e sem espacos nas pontas, para casar as chaves."""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


@lru_cache(maxsize=1)
def _carregar_mapa():
    with open(DATA_FILE, encoding="utf-8") as f:
        bruto = json.load(f)
    # Ignora chaves de metadados (ex.: "_comentario") e normaliza as demais.
    return {
        _normalizar(chave): valor
        for chave, valor in bruto.items()
        if not chave.startswith("_")
    }


def traduzir_nome_para_ingles(nome):
    """Converte o nome PT de um medicamento para o termo em ingles da openFDA.

    Quando nao existe traducao conhecida (nome proprio/marca sem equivalente),
    devolve o proprio nome original para que a busca ainda seja tentada.
    """
    if not nome:
        return nome
    return _carregar_mapa().get(_normalizar(nome), nome)


def traduzir_texto_para_portugues(texto):
    """Traduz um trecho da bula (ingles) para portugues.

    Usa `deep-translator` (GoogleTranslator) quando disponivel. Em caso de
    falha (sem internet, biblioteca ausente, etc.) devolve o texto original,
    de modo que a aplicacao nunca quebra por causa da traducao.
    """
    if not texto or texto == NAO_INFORMADO:
        return texto
    try:
        from deep_translator import GoogleTranslator

        return GoogleTranslator(source="en", target="pt").translate(
            texto[:_LIMITE_TRADUCAO]
        )
    except Exception:
        return texto
