## 📜 Sistema de Histórico de Medicamentos e Ações do Usuário

### Descrição

Implementar um sistema de histórico que registra todos os eventos relevantes relacionados aos medicamentos — confirmação de uso (tomado / não tomado) e exclusão de medicamentos — preservando os dados mesmo após o registro original ser removido.

### Motivação

Atualmente o usuário não tem como consultar o que aconteceu ao longo do tempo: quais medicamentos foram tomados, quais foram ignorados e quais foram excluídos. Como a exclusão de um `Medicamento` apaga os registros em cascata (`on_delete=CASCADE`), foi necessário um modelo independente que funcionasse como **snapshot** e sobrevivesse à exclusão do registro original.

### O que foi feito

- **Novo modelo `HistoricoEvento`** (`medicamento/models.py`) — armazena um snapshot dos dados do medicamento (nome, dose, importância, observações), o tipo do evento (`tomado`, `nao_tomado`, `excluido`), a observação do registro, data e horário. Independente de `Medicamento`, portanto não é afetado por exclusões em cascata.
- **Registro automático de eventos** (`medicamento/views.py`):
  - `confirmar_uso` → cria evento `tomado` ou `nao_tomado` ao registrar o uso.
  - `remover` → cria evento `excluido` antes de apagar o medicamento.
- **Tela de histórico** (`medicamento/templates/medicamento/historico.html`) — listagem com data, horário, medicamento, dose, importância, status (com badges visuais) e observação.
- **Filtros de busca** via `FiltroHistoricoForm` (`medicamento/forms.py`) — por nome, importância e intervalo de datas (de/até).
- **Nova rota** `historico/` (`medicamento/urls.py`) e link no menu de navegação (`base.html`).
- **Migração** `0002_historicoevento.py` para criação da tabela.

### Critérios de aceitação

- [x] Eventos de "tomado" e "não tomado" são registrados ao confirmar o uso.
- [x] Exclusão de medicamento gera um evento de histórico antes da remoção.
- [x] Histórico permanece acessível mesmo após o medicamento ser excluído.
- [x] É possível filtrar o histórico por nome, importância e período.
