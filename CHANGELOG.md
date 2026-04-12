# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.0.0] — 2026-04-12

### Adicionado
- Interface GUI para controle de medicamentos e horários
- Funcionalidade de cadastro de medicamentos com nome, dose e horário
- Funcionalidade de listagem de medicamentos cadastrados
- Funcionalidade de remoção de medicamentos
- Alertas de horário de medicação
- Persistência de dados em arquivo db.sqlite3
- Testes automatizados cobrindo cenários válidos, inválidos e limites
- Linting configurado com Ruff
- Pipeline de CI com GitHub Actions (lint + testes automáticos)
- README completo com instruções de instalação, execução e uso
- Arquivo de dependências (`requirements.txt` / `pyproject.toml`)
- Licença MIT
