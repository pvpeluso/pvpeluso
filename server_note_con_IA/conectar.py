#!/usr/bin/env python3
"""
Conexao interativa ao servidor Windows.
Uso: python conectar.py
     python conectar.py "dir C:\\"
     python conectar.py "type C:\\Users\\paulo\\script.txt"
"""

import sys
import subprocess

HOST = "servidor"  # usa o alias do ~/.ssh/config


def main():
    if len(sys.argv) > 1:
        # Executar comando direto
        cmd = " ".join(sys.argv[1:])
        subprocess.run(["ssh", HOST, cmd])
    else:
        # Abrir terminal interativo
        subprocess.run(["ssh", HOST])


if __name__ == "__main__":
    main()
