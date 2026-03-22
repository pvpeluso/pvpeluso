# server_note_con_IA

Documentação completa para conexão SSH remota ao servidor Windows via **Tailscale + Python + Termux** a partir de um **tablet Android (Galaxy Tab S9)**.

---

## Visão Geral da Arquitetura

```
[Galaxy Tab S9 - Termux]
        |
    Tailscale VPN
        |
[Servidor Windows - IP Tailscale: 100.79.62.56]
  usuário: paulo
  porta SSH: 22
```

**Stack:**
- Android: Termux + Python + paramiko
- VPN: Tailscale (mantém IP fixo mesmo sem IP público)
- Protocolo: SSH / SFTP
- Script principal: `escrever_remoto.py`

---

## Pré-requisitos

### No servidor Windows (fazer uma vez só)

1. **Instalar OpenSSH Server**
   - Configurações → Aplicativos → Recursos Opcionais → Servidor OpenSSH
   - Ou via PowerShell (admin):
     ```powershell
     Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
     Start-Service sshd
     Set-Service -Name sshd -StartupType Automatic
     ```

2. **Instalar Tailscale no Windows**
   - Baixar em https://tailscale.com/download/windows
   - Fazer login com a mesma conta do tablet
   - Anotar o IP Tailscale mostrado no painel (ex: `100.79.62.56`)

3. **Liberar porta SSH no Firewall (se necessário)**
   ```powershell
   New-NetFirewallRule -Name sshd -DisplayName "OpenSSH" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
   ```

### No tablet Android (Galaxy Tab S9)

1. **Instalar Termux** (via F-Droid, não Play Store)
   - https://f-droid.org → buscar "Termux"

2. **Instalar Tailscale para Android**
   - Play Store → Tailscale
   - Login com a mesma conta do servidor

3. **Configurar Termux**
   ```bash
   # Atualizar pacotes
   pkg update && pkg upgrade -y

   # Instalar Python
   pkg install python -y

   # Instalar dependência SSH
   pip install paramiko
   ```

---

## Configuração Rápida (primeira vez)

```bash
# No Termux, clonar este repositório
pkg install git -y
git clone https://github.com/pvpeluso/server_note_con_IA.git
cd server_note_con_IA

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env com suas credenciais (não vai para o git)
cp .env.example .env
nano .env   # preencher SSH_HOST e SSH_USER
```

O arquivo `.env` fica assim:
```
SSH_HOST=100.79.62.56
SSH_USER=paulo
```

---

## Uso do Script Principal

```bash
python escrever_remoto.py
```

O script vai:
1. Pedir sua senha SSH
2. Conectar ao servidor via Tailscale
3. Listar pastas do `C:\`
4. Criar/escrever o arquivo `C:\Users\paulo\script.txt`
5. Confirmar o conteúdo gravado

---

## Conexão SSH Manual (sem script)

```bash
# Conexão básica
ssh paulo@100.79.62.56

# Com porta explícita
ssh -p 22 paulo@100.79.62.56

# Copiar arquivo para o servidor
scp meu_arquivo.txt paulo@100.79.62.56:"C:/Users/paulo/"

# Copiar arquivo do servidor para o tablet
scp paulo@100.79.62.56:"C:/Users/paulo/script.txt" ./
```

---

## Configuração SSH sem senha (chave pública)

> **Status: CONCLUIDO** — chave configurada em 22/03/2026 via `setup.sh`

### Como foi feito (para referência)

```bash
# Baixar e rodar o setup (faz tudo automaticamente)
curl -O https://raw.githubusercontent.com/pvpeluso/pvpeluso/claude/remote-python-script-tailscale-AospO/server_note_con_IA/setup.sh
bash setup.sh
# Pediu senha uma única vez → chave instalada no servidor
```

### Onde as chaves estão salvas

| Arquivo | Local no Tablet | Descrição |
|---------|----------------|-----------|
| Chave privada | `~/.ssh/id_ed25519` | Fica no tablet — NUNCA compartilhar |
| Chave pública | `~/.ssh/id_ed25519.pub` | Cópia enviada ao servidor |
| Config SSH | `~/.ssh/config` | Alias `servidor` → IP + usuário |

**No servidor Windows**, a chave pública foi instalada em:
```
C:\Users\paulo\.ssh\authorized_keys
```

### Ver a chave pública (tablet)
```bash
cat ~/.ssh/id_ed25519.pub
```

### Config SSH criada automaticamente (`~/.ssh/config`)
```
Host servidor
    HostName 100.79.62.56
    User paulo
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Resultado
```bash
ssh servidor        # conecta sem senha
scp arquivo.txt servidor:"C:/Users/paulo/"
scp servidor:"C:/server/pasta" ~/
```

### Se precisar reconfigurar (ex: novo tablet)
```bash
bash setup.sh       # gera nova chave e instala no servidor
```

---

## Referência Rápida (cola na parede)

| Ação | Comando |
|------|---------|
| Conectar ao servidor | `ssh servidor` |
| Rodar script Python | `python escrever_remoto.py` |
| Enviar arquivo | `scp arq.txt servidor:"C:/Users/paulo/"` |
| Baixar arquivo | `scp servidor:"C:/Users/paulo/arq.txt" ./` |
| Ver IP Tailscale | App Tailscale → aba Devices |
| Verificar SSH no Windows | `Get-Service sshd` (PowerShell) |

---

## Solução de Problemas

### "Connection refused"
- Verificar se OpenSSH Server está rodando no Windows
- `Start-Service sshd` no PowerShell como admin

### "Network unreachable" / timeout
- Verificar se Tailscale está **Connected** no tablet e no Windows
- Verificar se estão na mesma conta Tailscale

### "Authentication failed"
- Confirmar usuário: `paulo` (minúsculo)
- Testar senha diretamente no Windows antes de testar remoto

### Termux perdeu pacotes após reinstalar
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install paramiko
```

---

## Estrutura do Repositório

```
server_note_con_IA/
├── README.md              # Esta documentação
├── setup.sh               # Setup automático (rodar uma vez)
├── conectar.py            # Atalho Python para conexão/comandos
├── escrever_remoto.py     # Script de escrita remota via SFTP
├── requirements.txt       # Dependências Python
├── ssh_config.example     # Exemplo de config SSH
├── .env.example           # Modelo de variáveis de ambiente
└── .gitignore             # Garante que .env nunca vai ao git
```

> `.env` contém as credenciais reais e está no `.gitignore` — nunca é commitado.

---

## Informações da Infraestrutura

| Item | Valor |
|------|-------|
| IP Tailscale do servidor | `100.79.62.56` |
| Usuário SSH | `paulo` |
| Porta SSH | `22` |
| OS servidor | Windows |
| Cliente | Galaxy Tab S9 (Android) + Termux |
