"""Testes da CLI via CliRunner — exercitam o grupo e o comando."""

from click.testing import CliRunner

from cli_template.cli import hello, main


def test_hello_saudacao_padrao() -> None:
    result = CliRunner().invoke(hello, [])

    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_hello_com_nome() -> None:
    result = CliRunner().invoke(hello, ["--name", "Desenrolai"])

    assert result.exit_code == 0
    assert "Hello, Desenrolai!" in result.output


def test_grupo_expoe_o_comando_hello() -> None:
    """O comando precisa estar registrado no grupo, não só existir solto."""
    result = CliRunner().invoke(main, ["hello", "--name", "Forge"])

    assert result.exit_code == 0
    assert "Hello, Forge!" in result.output


def test_grupo_sem_argumento_mostra_ajuda() -> None:
    result = CliRunner().invoke(main, [])

    # Desde o click 8.2, grupo sem subcomando imprime a ajuda e sai com 2.
    assert result.exit_code == 2
    assert "Usage:" in result.output
    assert "hello" in result.output


def test_comando_inexistente_falha() -> None:
    result = CliRunner().invoke(main, ["nao-existe"])

    assert result.exit_code != 0
