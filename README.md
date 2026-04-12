# MedGuard




[![CI](https://github.com/AdlerMrF/medguard/actions/workflows/ci.yml/badge.svg)](https://github.com/AdlerMrF/medguard/actions/workflows/ci.yml)




## Descrição do Problema



Idosos e cuidadores frequentemente enfrentam dificuldades para controlar horários e dosagens de múltiplos medicamentos. Esquecimentos podem causar complicações graves de saúde.



## Proposta de Solução



O MedGuardian é uma aplicação web simples que permite cadastrar medicamentos com suas doses e horários, e emite alertas quando está na hora de tomá-los (janela de ±10 minutos). Também registra o histórico de uso.



## Público-alvo



Idosos, cuidadores e familiares responsáveis pela administração de medicamentos.



## Funcionalidades



* Cadastrar medicamentos com nome, dose, nível de importância e horários
* Listar e filtrar medicamentos por nome e importância
* Visualizar detalhes e histórico de uso de cada medicamento
* Receber alertas dos medicamentos a tomar no momento (±10 min)
* Confirmar ou registrar não-uso de um medicamento
* Excluir medicamentos com confirmação



## Tecnologias Utilizadas



* Python 3.10+
* Django 5.0.6
* SQLite
* pytest / pytest-django
* ruff
* GitHub Actions



## Instalação



```bash
# Clone o repositório
git clone https://github.com/AdlerMrF/medguard.git
cd medguard

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\\Scripts\\activate ou .venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# (Opcional) Crie um superusuário para o admin
python manage.py createsuperuser

# Rode o servidor
python manage.py runserver
```

Acesse em: http://127.0.0.1:8000



## Testes



```bash
pytest
```

Com cobertura:

```bash
pytest --cov=medicamento --cov-report=term-missing
```

## Lint



```bash
ruff check .
```

## Versão



1.0.0



## Autor



Adler — github.com/AdlerMrF

