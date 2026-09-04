# desenrolai-cli-template

Template para ferramentas de linha de comando — **Python 3.13 + click**, gerenciado com [uv](https://docs.astral.sh/uv/).

## Stack

| Ferramenta | Versão mínima | Papel |
|---|---|---|
| Python | 3.13 | runtime |
| `click` | 8.5.0 | parsing de argumento |
| `ruff` | 0.16.6 | lint + format |
| `mypy` | 2.3.1 | tipagem estrita |
| `pytest` + `pytest-cov` | 9.1.1 / 7.1.0 | testes e cobertura |

## Estrutura

`src/` layout de verdade — o pacote instalável fica **dentro** de `src/`:

```
src/
  cli_template/     # renomeie ao usar o template
    __init__.py
    cli.py          # entrypoint da CLI — adicione seus comandos aqui
tests/
  test_cli.py       # exercita o grupo e os comandos via CliRunner
```

### Primeiro passo: renomear o pacote

O repo é criado por cópia literal deste template (o Forge usa o `createUsingTemplate` do
GitHub, que não substitui placeholder), então o pacote chega com o nome `cli_template`.
Renomeie o diretório `src/cli_template/` para o nome do seu projeto e troque `cli_template`
nestes **três** lugares:

| Arquivo | Campo | Fica |
|---|---|---|
| `pyproject.toml` | `[project.scripts]` | `hello-cli = "<pacote>.cli:main"` |
| `pyproject.toml` | `addopts`, em `[tool.pytest.ini_options]` | `--cov=<pacote>` |
| `tests/test_cli.py` | o `import` no topo | `from <pacote>.cli import hello, main` |

O nome do executável (`hello-cli`) também é placeholder — troque na chave de
`[project.scripts]` se quiser outro.

Confira com `uv run pytest`: precisa continuar verde. Se a cobertura aparecer zerada, o
`--cov` ficou apontando para o nome antigo.

## Rodar localmente

```bash
uv sync --all-groups

uv run hello-cli hello
uv run hello-cli hello --name Desenrolai
```

## Gate de qualidade

Os comandos que o CI roda — rode-os antes de todo push:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy
uv run pytest
uv run hello-cli hello --name CI   # smoke do console script
```

- `mypy` roda em **strict** e cobre `src` e `tests`.
- `ruff` inclui `I` (ordem de import) e `S` (flake8-bandit, segurança). `S101` é ignorado só em `tests/`.
- `pytest` falha abaixo de **90%** de cobertura (`--cov-fail-under`).

## Adicionar comandos

Adicione funções `@main.command()` em `src/cli_template/cli.py`.

> Desde o click 8.2, um grupo invocado sem subcomando imprime a ajuda e sai com
> código **2** (antes era 0). O teste `test_grupo_sem_argumento_mostra_ajuda`
> fixa esse comportamento.

## Distribuição

CLIs são distribuídas como pacote (`pip install` / `pipx` / `uv tool install`),
não vão para o cluster — ver `forge.yaml`: `deploy: none`.

```bash
uv tool install .
hello-cli hello --name Mundo
```

O CI roda um smoke do console script justamente para garantir que o entrypoint
declarado em `[project.scripts]` resolve depois de instalado.

## CI

`.github/workflows/ci.yml`, um job `quality`: `ruff check`, `ruff format --check`, `mypy`,
`pytest` e o **smoke do console script** (`uv run hello-cli hello --name CI`) — este
último é o que garante que o entrypoint de `[project.scripts]` resolve depois de
instalado. Não há job de imagem: a CLI é distribuída como pacote (`forge.yaml`:
`deploy: none`).

### Runner: repo privado gerado a partir deste template precisa configurar

Este template é **público**, e em repositório público o GitHub Actions em runner hospedado
é gratuito. **O repo que você gera a partir dele é privado**, onde os minutos são cota paga
— e a cota da organização está esgotada. Por isso o `runs-on` é parametrizado por variável
de repositório, com default hospedado:

```yaml
runs-on: ${{ fromJSON(vars.CI_RUNNER || '"ubuntu-latest"') }}
```

Antes do primeiro push no repo novo, defina a variável (Settings → Secrets and variables →
Actions → Variables), ou por CLI:

```bash
gh variable set CI_RUNNER --body '["self-hosted","desenrolai"]'
```

- O valor é **JSON**, não texto solto. `'["self-hosted","desenrolai"]'` vira dois labels;
  a string `self-hosted,desenrolai` viraria **um** label só, que nenhum runner atende, e o
  job ficaria em `queued` para sempre.
- Sem a variável, tudo continua em `ubuntu-latest` — este template continua verde assim.
- Não há `CI_RUNNER_DOCKER` aqui: sem Dockerfile, não há job de imagem.

**Sintoma de não configurar:** o job morre em ~2 segundos com **`steps: 0`**, sem log de
erro que oriente. Isso é assinatura de **billing** (cota de Actions esgotada/bloqueada),
não de YAML quebrado. Não perca tempo procurando erro de sintaxe: confira a variável e o
billing da organização.

## Dependências

`uv.lock` é a fonte da verdade — commite-o. Para atualizar:

```bash
uv lock --upgrade
uv sync --all-groups
```
