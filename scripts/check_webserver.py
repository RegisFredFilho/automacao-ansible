
#!/usr/bin/env python3

import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

URL = os.getenv("LAB_URL", "http://192.168.0.35")
AMBIENTE_ESPERADO = "laboratorio"


def verificar_webserver():
    headers = {
    "User-Agent": "LinuxAutomationLab/1.0"
}

    client_id = os.getenv("CF_ACCESS_CLIENT_ID")
    client_secret = os.getenv("CF_ACCESS_CLIENT_SECRET")

    if client_id and client_secret:
        headers["CF-Access-Client-Id"] = client_id
        headers["CF-Access-Client-Secret"] = client_secret

    if URL.startswith("https://") and not (client_id and client_secret):
        print("ERRO: credenciais Cloudflare Access ausentes")
        return 1

    try:
        request = Request(URL, headers=headers)

        with urlopen(request, timeout=10) as resposta:
            status = resposta.status
            ambiente = resposta.headers.get("X-Lab-Environment")
            conteudo = resposta.read().decode("utf-8")

        print(f"Servidor: {URL}")
        print(f"HTTP: {status}")
        print(f"Ambiente: {ambiente}")

        if status != 200:
            print("ERRO: HTTP inesperado")
            return 1

        if ambiente != AMBIENTE_ESPERADO:
            print("ERRO: Ambiente incorreto")
            return 1

        if "Linux Automation Lab" not in conteudo:
            print("ERRO: Conteudo incorreto")
            return 1

        print("SUCESSO: Servidor funcionando!")
        return 0

    except (HTTPError, URLError, TimeoutError) as erro:
        print(f"ERRO: Falha ao acessar servidor: {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(verificar_webserver())
