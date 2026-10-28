
from pathlib import Path
import importlib.util
from io import BytesIO

import pytest


# Importar nosso script de monitoramento
SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "check_webserver.py"
)

spec = importlib.util.spec_from_file_location(
    "check_webserver", SCRIPT
)

webserver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(webserver)


# Teste real: precisa acessar o servidor Nginx
@pytest.mark.integration
def test_webserver_real():
    assert webserver.verificar_webserver() == 0


# Simular uma resposta HTTP
class RespostaSimulada:
    def __init__(self, status=200, ambiente="laboratorio"):
        self.status = status
        self.headers = {"X-Lab-Environment": ambiente}

    def read(self):
        return b"<h1>Linux Automation Lab</h1>"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def preparar_teste(monkeypatch):
    # Impedir dependencia de credenciais externas
    monkeypatch.delenv("CF_ACCESS_CLIENT_ID", raising=False)
    monkeypatch.delenv("CF_ACCESS_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("LAB_URL", raising=False)


def test_resposta_valida(monkeypatch):
    preparar_teste(monkeypatch)

    monkeypatch.setattr(
        webserver,
        "urlopen",
        lambda *args, **kwargs: RespostaSimulada(),
    )

    assert webserver.verificar_webserver() == 0


def test_ambiente_incorreto(monkeypatch):
    preparar_teste(monkeypatch)

    monkeypatch.setattr(
        webserver,
        "urlopen",
        lambda *args, **kwargs: RespostaSimulada(
            ambiente="producao"
        ),
    )

    assert webserver.verificar_webserver() == 1


def test_conteudo_incorreto(monkeypatch):
    preparar_teste(monkeypatch)

    class RespostaInvalida(RespostaSimulada):
        def read(self):
            return b"<h1>Outra aplicacao</h1>"

    monkeypatch.setattr(
        webserver,
        "urlopen",
        lambda *args, **kwargs: RespostaInvalida(),
    )

    assert webserver.verificar_webserver() == 1
