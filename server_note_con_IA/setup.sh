#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# SETUP SSH - Galaxy Tab S9 → Servidor Windows via Tailscale
# Execute UMA VEZ. Depois: ssh servidor
# ============================================================

HOST="100.79.62.56"
USER="paulo"

echo "=== Setup SSH para $USER@$HOST ==="
echo ""

# 1. Instalar dependências
echo "[1/4] Instalando pacotes..."
pkg install -y openssh python 2>/dev/null
pip install -q paramiko

# 2. Gerar chave SSH se não existir
echo "[2/4] Configurando chave SSH..."
if [ ! -f ~/.ssh/id_ed25519 ]; then
    ssh-keygen -t ed25519 -C "tab_s9" -N "" -f ~/.ssh/id_ed25519
    echo "     Chave gerada."
else
    echo "     Chave ja existe."
fi

# 3. Criar config SSH
echo "[3/4] Criando config SSH..."
mkdir -p ~/.ssh
cat > ~/.ssh/config << EOF
Host servidor
    HostName $HOST
    User $USER
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF
chmod 600 ~/.ssh/config
echo "     Config criada."

# 4. Copiar chave para o servidor (pede senha só desta vez)
echo "[4/4] Copiando chave para o servidor..."
echo "      => Vai pedir sua senha SSH UMA ULTIMA VEZ"
echo ""
ssh-copy-id -i ~/.ssh/id_ed25519.pub $USER@$HOST

echo ""
echo "=============================="
echo "  SETUP CONCLUIDO!"
echo "  Agora conecte com:"
echo ""
echo "    ssh servidor"
echo ""
echo "  Sem precisar de senha."
echo "=============================="
