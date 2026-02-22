# HIM Remote Agent 🔌

Agent qui tourne sur ton PC et se connecte à OpenClaw pour exécuter des commandes à distance.

---

## 🎯 Fonctionnalités

- ✅ **Connexion sécurisée** au serveur OpenClaw
- ✅ **Exécution de commandes** à distance
- ✅ **Liste blanche/noire** de commandes
- ✅ **Monitoring système** (CPU, RAM, disque)
- ✅ **Reconnexion automatique**
- ✅ **Logs** de toutes les actions

---

## 🚀 Installation

### 1. Prérequis

```bash
# Python 3.8+
python --version

# pip installé
pip --version
```

### 2. Installation

```bash
cd remote-agent

# Installe les dépendances
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Étape 1 : Configure l'agent

```bash
python remote_agent.py setup
```

Réponds aux questions :
- **URL du serveur** : L'URL de ton OpenClaw
- **Nom de l'agent** : Identifiant
- **Ton nom** : Propriétaire

### Étape 2 : Édite la config (optionnel)

`remote-config.json` :

```json
{
  "server_url": "wss://ton-serveur.com",
  "agent_name": "HIM-PC-Agent",
  "owner": "Williams",
  "allowed_commands": ["ls", "dir", "docker", "python", "git"],
  "blocked_commands": ["rm -rf /", "format"],
  "auto_connect": true,
  "heartbeat_interval": 30
}
```

---

## 🎮 Démarrage

### Lancer l'agent

```bash
python remote_agent.py start
```

Tu verras :
```
============================================================
🚀 HIM Remote Agent v1.0.0
🆔 Agent ID: abc12345
============================================================
🔗 Connexion à wss://ton-serveur.com...
✅ Connecté au serveur OpenClaw
```

---

## 📡 Comment ça marche

### Architecture

```
Ton PC (Agent)          Serveur OpenClaw          Moi (HIM)
     │                         │                      │
     ├─── WebSocket ──────────>│                      │
     │    (connexion)          │                      │
     │                         │<── Je demande cmd ───┤
     │<── Commande à exec ─────│                      │
     │                         │                      │
     ├─── Exécute localement ──│                      │
     │                         │                      │
     ├─── Résultat ───────────>│                      │
     │                         │─── Je vois le ──────>│
     │                         │     résultat         │
```

### Sécurité

- 🔐 Connexion WebSocket sécurisée (WSS)
- 🛡️ Liste blanche de commandes autorisées
- ⛔ Liste noire de commandes dangereuses
- 📜 Logs de toutes les commandes exécutées
- 🆔 ID unique par machine

---

## 🖥️ Windows : Démarrage automatique

Crée `start-remote-agent.bat` :

```batch
@echo off
cd /d "%~dp0"
:loop
python remote_agent.py start
if errorlevel 1 (
    echo Reconnexion dans 10 secondes...
    timeout /t 10 /nobreak >nul
    goto loop
)
```

### Démarrage avec Windows

1. Crée un raccourci de `start-remote-agent.bat`
2. Appuie sur `Win + R`
3. Tape `shell:startup`
4. Colle le raccourci dans le dossier

L'agent démarrera automatiquement avec Windows !

---

## 🐧 Linux/Mac : Service systemd

Crée `/etc/systemd/system/him-agent.service` :

```ini
[Unit]
Description=HIM Remote Agent
After=network.target

[Service]
Type=simple
User=ton-user
WorkingDirectory=/chemin/vers/remote-agent
ExecStart=/usr/bin/python3 /chemin/vers/remote-agent/remote_agent.py start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Active le service :

```bash
sudo systemctl enable him-agent
sudo systemctl start him-agent
sudo systemctl status him-agent
```

---

## 📋 Commandes disponibles

Une fois connecté, je peux exécuter sur ton PC :

```bash
# Voir les fichiers
ls -la
dir

# Docker
docker ps
docker-compose up -d

# Git
git status
git pull

# Python
python --version
pip list

# Système
whoami
pwd
```

---

## 🔒 Sécurité

### Commandes bloquées par défaut

- `rm -rf /` - Suppression racine
- `format` - Formatage disque
- `del /f` - Suppression forcée Windows

### Ajouter des commandes autorisées

Édite `remote-config.json` :

```json
{
  "allowed_commands": [
    "ls", "dir", "docker", "python", "git", 
    "npm", "node", "mkdir", "echo"
  ]
}
```

---

## 📊 Monitoring

L'agent envoie automatiquement :
- CPU usage (%)
- RAM usage (%)
- Disque usage (%)
- Uptime
- Timestamp

---

## 🐛 Dépannage

### "Connexion impossible"

1. Vérifie l'URL dans `remote-config.json`
2. Vérifie ta connexion internet
3. Vérifie que le serveur OpenClaw tourne

### "Module non trouvé"

```bash
pip install -r requirements.txt
```

### L'agent se déconnecte tout le temps

```bash
# Vérifie les logs
tail -f remote-agent.log

# Augmente le heartbeat
echo '{"heartbeat_interval": 60}' > remote-config.json
```

---

## 📝 Logs

Toutes les actions sont loggées dans :
- `remote-agent.log` - Activité de l'agent
- `remote-config.json` - Configuration

---

## 🎯 Utilisations

1. **Gestion à distance** - Exécuter des commandes sur ton PC depuis ailleurs
2. **Monitoring** - Voir l'état de ton PC en temps réel
3. **Automatisation** - Lancer des scripts automatiquement
4. **Support** - Je peux t'aider en exécutant des commandes sur ton PC

---

Tu es prêt ? Lance `python remote_agent.py setup` puis `start` ! 🚀
