# MedGuard




[![CI](https://github.com/AdlerMrF/medguard/actions/workflows/ci.yml/badge.svg)](https://github.com/AdlerMrF/medguard/actions/workflows/ci.yml)




## Descrição do Problema



Idosos e cuidadores frequentemente enfrentam dificuldades para controlar horários e dosagens de múltiplos medicamentos. Esquecimentos podem causar complicações graves de saúde.



## Proposta de Solução



O MedGuard é uma aplicação web simples que permite cadastrar medicamentos com suas doses e horários, e emite alertas quando está na hora de tomá-los (janela de ±10 minutos). Também registra o histórico de uso.



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

## Estrutura do Projeto:
medguard/
├── manage.py
├── db.sqlite3              # ⚙️ gerado após migrations ❌ não versionar
├── requirements.txt
├── pyproject.toml
├── README.md
├── VERSION
├── CHANGELOG.md
├── LICENSE.txt
├── CONTRIBUTING.md
├── conftest.py
├── .coverage               # ⚙️ relatório de cobertura de testes ❌ não versionar
├── .gitignore
│
├── config/                 # ⚙️ configuração principal do Django
│   ├── __init__.py
│   ├── settings.py         # 🔥 configurações principais
│   ├── urls.py             # 🔗 rotas globais
│   ├── wsgi.py             # 🚀 deploy (produção)
│
├── medicamento/            # 💊 APP PRINCIPAL
│   ├── __init__.py
│   ├── admin.py            # painel admin
│   ├── apps.py             # config do app
│   ├── models.py           # 🧠 banco de dados
│   ├── views.py            # 🎯 lógica
│   ├── urls.py             # rotas do app
│   ├── forms.py            # formulários
│   │
│   ├── migrations/         # histórico do banco
│   │   └── 0001_initial.py
│   │   └── __init__.py
│   │
│   └── templates/          # 🎨 FRONT-END (HTML)
│       └── medicamento/
│           ├── base.html
│           ├── index.html
│           ├── listar.html
│           ├── cadastrar.html
│           ├── detalhe.html
│           ├── alertas.html
│           ├── confirmar_uso.html
│           └── confirmar_exclusao.html
│
├── tests/                  # 🧪 testes automatizados
│   ├── __init__.py
│   ├── test_models.py            
│
├── __pycache__/            # cache Python ❌ não versionar
├── .pytest_cache/          # cache do pytest ❌ não versionar
├── .ruff_cache/            # cache do Ruff ❌ não versionar
├── .venv/                  # ambiente virtual local ❌ não versionar
└── .git/                   # controle de versão (não incluído em deploy)



## Instalação

# Inicialize o terminal (Prompt de Comando CMD ou PowerShell), clicando com o botão direito na pasta de preferência e selecionando "Abrir Terminal":
<img width="436" height="366" alt="1" src="https://github.com/user-attachments/assets/e13ee9a8-0b73-4762-9c82-ef5a8045cdcb" />

```bash
# No terminal que abrir Clone o repositório com o comando:
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

## Exemplo de teste

# Ao rodarmos http://127.0.0.1:8000, será apresentada a tela inicial do Programa: 
<img width="1916" height="956" alt="2" src="https://github.com/user-attachments/assets/35432764-7de8-41b8-acb2-c6022f9814e5" />

# Para fins de testes adicionamos o "Soro Nasal", para mostrar as funcionalidades de cadastro de remédios:
<img width="1908" height="976" alt="3" src="https://github.com/user-attachments/assets/25a53a26-567a-4a90-a228-704881209534" />

# Demonstração do remédio cadastrado:
<img width="1856" height="950" alt="4" src="https://github.com/user-attachments/assets/b1587022-9ff9-4b92-bd23-78fe0aaacf42" />
<img width="1898" height="616" alt="5" src="https://github.com/user-attachments/assets/49e82f63-7cda-4a11-a2ee-4aa1b8713107" />

# Como o remédio cadastrado ainda não está próximo da hora atual +- 10 minutos não haverá alarme:
<img width="1890" height="566" alt="6" src="https://github.com/user-attachments/assets/b567a7a4-1936-487f-b9ad-1eb9a84d092e" />

# Para mostrar o cadastro de um remédio que entre em alarmes, adicionamos outro:
<img width="874" height="398" alt="7" src="https://github.com/user-attachments/assets/27c6537c-b986-445d-8826-65e4a0dc172e" />

# Assim, ele automaticamente aparecerá em alarmes:
<img width="876" height="328" alt="8" src="https://github.com/user-attachments/assets/5ba236a0-7376-476f-9dd3-9f026073903a" />

# Ao confirmar o uso o medicamento aparecerá como tomado:
<img width="650" height="432" alt="9" src="https://github.com/user-attachments/assets/1fd150ed-65ec-4a2a-8aca-ae305758c53a" />
<img width="880" height="480" alt="10" src="https://github.com/user-attachments/assets/843504ae-fc4c-4cbd-a6cd-7a0d3c4c96dd" />

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

