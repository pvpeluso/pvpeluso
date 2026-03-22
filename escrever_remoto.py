#!/usr/bin/env python3
"""
Conecta ao servidor Windows remoto via Tailscale + SSH (paramiko).
Execute na sua maquina local (que tem Tailscale ativo).

- Lista pastas do C:
- Escreve script.txt em C:/Users/root/
"""

import getpass

try:
    import paramiko
except ImportError:
    print("Instalando paramiko...")
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

HOST = "100.79.62.56"
USER = "root"
REMOTE_PATH = "C:/Users/root/script.txt"

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

    # Lista pastas do C:
    print("\n--- Pastas do C:\\ ---")
    out, err = exec_cmd(client, "dir C:\\")
    print(out or err)

    # Escreve script.txt via SFTP
    sftp = client.open_sftp()
    with sftp.file(REMOTE_PATH, "w") as f:
        f.write(CONTEUDO)
    sftp.close()
    print(f"Arquivo escrito em {REMOTE_PATH}")

    # Confirma o conteudo
    out, err = exec_cmd(client, 'type "C:\\Users\\root\\script.txt"')
    print("\n--- Conteudo do script.txt ---")
    print(out or err)

    client.close()
    print("Concluido!")


if __name__ == "__main__":
    main()
