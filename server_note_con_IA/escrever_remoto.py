#!/usr/bin/env python3
"""
Conecta ao servidor Windows via Tailscale + SSH.
Execute no Termux (Android) com Tailscale ativo.

Uso: python escrever_remoto.py
"""

import getpass
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import paramiko
except ImportError:
    print("Instalando paramiko...")
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

HOST = os.getenv("SSH_HOST")
USER = os.getenv("SSH_USER")

if not HOST or not USER:
    raise SystemExit("Erro: crie um arquivo .env com SSH_HOST e SSH_USER (veja .env.example)")

REMOTE_PATH = f"C:/Users/{USER}/script.txt"
CONTEUDO = "# script.txt - criado remotamente via Tailscale + Python + SSH\r\n"


def conectar(host, user):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    senha = getpass.getpass(f"Senha SSH para {user}@{host}: ")
    client.connect(host, username=user, password=senha, timeout=15)
    print(f"Conectado como {user}@{host}")
    return client


def exec_cmd(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    return out, err


def main():
    print(f"Conectando em {USER}@{HOST}...")
    client = conectar(HOST, USER)

    print("\n--- Pastas do C:\\ ---")
    out, err = exec_cmd(client, "dir C:\\")
    print(out or err)

    sftp = client.open_sftp()
    with sftp.file(REMOTE_PATH, "w") as f:
        f.write(CONTEUDO)
    sftp.close()
    print(f"\nArquivo escrito em {REMOTE_PATH}")

    out, err = exec_cmd(client, f'type "{REMOTE_PATH.replace("/", "\\")}"')
    print("\n--- Conteudo do script.txt ---")
    print(out or err)

    client.close()
    print("Concluido!")


if __name__ == "__main__":
    main()
