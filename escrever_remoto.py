#!/usr/bin/env python3
"""
Escreve script.txt no servidor remoto via Tailscale + SSH.
Execute este script na sua máquina LOCAL (que tem Tailscale configurado).
"""

import getpass

try:
    import paramiko
except ImportError:
    print("Instalando paramiko...")
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

HOST = "peluso-server.tail0a82d5.ts.net"
USER = "root"
REMOTE_PATH = "/root/script.txt"

CONTEUDO = """# script.txt - arquivo de teste
# Criado remotamente via Tailscale + Python + SSH
# Servidor: peluso-server

echo "Olá do servidor remoto!"
echo "Data: $(date)"
"""

def conectar(host, user):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Tenta primeiro com chave SSH local
    try:
        client.connect(host, username=user, timeout=10, allow_agent=True, look_for_keys=True)
        print(f"✓ Conectado via chave SSH como {user}@{host}")
        return client
    except paramiko.AuthenticationException:
        pass

    # Tenta com senha
    print(f"Chave SSH não funcionou. Informe a senha para {user}@{host}:")
    senha = getpass.getpass("Senha: ")
    client.connect(host, username=user, password=senha, timeout=10)
    print(f"✓ Conectado via senha como {user}@{host}")
    return client


def main():
    print(f"Conectando em {USER}@{HOST}...")

    client = conectar(HOST, USER)

    # Escreve o arquivo remoto via SFTP
    sftp = client.open_sftp()
    with sftp.file(REMOTE_PATH, "w") as f:
        f.write(CONTEUDO)
    sftp.close()

    print(f"✓ Arquivo escrito em {REMOTE_PATH}")

    # Confirma o conteúdo
    stdin, stdout, stderr = client.exec_command(f"cat {REMOTE_PATH}")
    print("\n--- Conteúdo do arquivo no servidor ---")
    print(stdout.read().decode())

    client.close()
    print("✓ Concluído!")


if __name__ == "__main__":
    main()
