# HIM WhatsApp Bridge 🌉

Pont entre **whatsapp-web.js** et l'**Agent HIM Python**.

Connecte ton WhatsApp à l'agent IA pour réponses automatiques.

---

## 🚀 Installation rapide

### 1. Prérequis

```bash
# Node.js installé (v16+)
node --version

# npm installé
npm --version
```

### 2. Installation

```bash
cd whatsapp-agent

# Installe les dépendances
npm install

# OU si déjà fait
npm install whatsapp-web.js qrcode-terminal axios
```

---

## 🎯 Démarrage

### Étape 1 : Lancer l'agent Python (dans un autre terminal)

```bash
# Terminal 1
python webhook_server.py
```
Attends le message : `Webhook server starting on port 5000`

### Étape 2 : Lancer le bridge WhatsApp (dans un autre terminal)

```bash
# Terminal 2
node whatsapp-bridge.js
```

### Étape 3 : Scanner le QR Code

```
=== SCANNE CE QR CODE AVEC TON WHATSAPP ===

[QR CODE ICI]

==========================================
```

1. Ouvres WhatsApp sur ton téléphone
2. Paramètres → Appareils liés → Lier un appareil
3. Scannes le QR code affiché
4. ✅ Connecté !

---

## 📁 Structure des fichiers

```
whatsapp-agent/
├── agent.py              🤖 Agent IA Python
├── webhook_server.py     🌐 Serveur Flask (port 5000)
├── whatsapp-bridge.js    📱 Pont WhatsApp (ce fichier)
├── package.json          📦 Config Node.js
├── config.json           ⚙️ Config agent
└── README.md            📖 Documentation
```

---

## 🔄 Flux de fonctionnement

```
Message WhatsApp reçu
       ↓
whatsapp-web.js (bridge.js)
       ↓
HTTP POST → http://localhost:5000/webhook/whatsapp
       ↓
Flask Server (webhook_server.py)
       ↓
Agent Python (agent.py)
       ↓
Génère réponse intelligente
       ↓
Retour via HTTP
       ↓
whatsapp-web.js envoie la réponse
       ↓
Message reçu sur WhatsApp
```

---

## 🖥️ Démarrage automatique (Windows)

Crée un fichier `start-him.bat` :

```batch
@echo off
echo ===================================
echo HIM WhatsApp Agent
echo ===================================
echo.

cd /d "%~dp0"

:: Lancer le serveur Python (nouvelle fenêtre)
start "Agent Python" python webhook_server.py

:: Attendre 5 secondes
timeout /t 5 /nobreak > nul

:: Lancer le bridge WhatsApp
node whatsapp-bridge.js

pause
```

Double-clique → Les deux services démarrent !

---

## 🖥️ Démarrage automatique (Linux/Mac)

Crée `start-him.sh` :

```bash
#!/bin/bash
echo "==================================="
echo "HIM WhatsApp Agent"
echo "==================================="
echo ""

cd "$(dirname "$0")"

# Lancer le serveur Python en arrière-plan
python webhook_server.py &
PYTHON_PID=$!

# Attendre
echo "Démarrage du serveur Python..."
sleep 5

# Lancer le bridge
node whatsapp-bridge.js

# Nettoyer à l'arrêt
kill $PYTHON_PID 2>/dev/null
```

Rends exécutable : `chmod +x start-him.sh`

Lance : `./start-him.sh`

---

## ⚙️ Configuration avancée

### Variables d'environnement

```bash
# URL du webhook (par défaut: localhost:5000)
export AGENT_WEBHOOK_URL="http://localhost:5000/webhook/whatsapp"

# Ton numéro (pour qu'il ne réponde pas à tes propres messages)
export OWNER_NUMBER="225XXXXXXXX"

# Lancer avec les variables
node whatsapp-bridge.js
```

### Fichier .env

Crée un fichier `.env` :

```
AGENT_WEBHOOK_URL=http://localhost:5000/webhook/whatsapp
OWNER_NUMBER=225XXXXXXXX
```

Installe dotenv : `npm install dotenv`

Modifie `whatsapp-bridge.js` : Ajoute au début :
```javascript
require('dotenv').config();
```

---

## 🐛 Dépannage

### Erreur "Cannot find module"

```bash
npm install
```

### Erreur de connexion à l'agent

Vérifie que le serveur Python tourne :
```bash
curl http://localhost:5000/status
```

Doit retourner : `{"status": "running"...}`

### QR Code ne s'affiche pas

Vérifie : `npm install qrcode-terminal`

### Session expire

Supprime le dossier `.wwebjs_auth` :
```bash
rm -rf .wwebjs_auth
```

Relance → Re-scanne le QR code

---

## 📊 Logs

Les logs sont dans : `whatsapp-bridge.log`

Voir en temps réel :
```bash
tail -f whatsapp-bridge.log
```

---

## ⚠️ Important

1. **Ne ferme pas** les terminaux quand ça tourne
2. **Première connexion** : Doit scanner le QR code
3. **Sessions** : Sauvegardées dans `.wwebjs_auth/`
4. **WhatsApp Web** : Ne pas utiliser en même temps sur le même appareil

---

## 🎯 Test rapide

Une fois démarré :
1. Envoie un message WhatsApp à un ami
2. Demande à l'ami de te répondre
3. Le bot devrait répondre automatiquement !

---

Tu es prêt ? Lance les commandes ! 🚀
