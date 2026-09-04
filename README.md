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

## Dependências

`uv.lock` é a fonte da verdade — commite-o. Para atualizar:

```bash
uv lock --upgrade
uv sync --all-groups
```
