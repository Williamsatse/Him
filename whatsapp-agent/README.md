# HIM WhatsApp Agent 🤖

Agent IA personnel pour répondre automatiquement à tes messages WhatsApp.

## 🎯 Fonctionnalités

- ✅ **Réponses automatiques** intelligentes
- ✅ **Mode Away** quand tu es offline
- ✅ **Heures de travail** configurables
- ✅ **Liste blanche/noire** de contacts
- ✅ **Logs** de toutes les conversations
- ✅ **Notifications** Telegram/Desktop

---

## 🚀 Démarrage rapide

### 1. Configuration initiale

```bash
cd whatsapp-agent
python agent.py setup
```

Réponds aux questions :
- Ton nom
- Nom de l'agent (HIM)
- Mode réponse auto (oui/non)
- Mode IA intelligent (oui/non)

### 2. Lance l'agent

```bash
python agent.py start
```

### 3. Test rapide

```bash
python agent.py test
```

---

## ⚙️ Configuration

Édite `config.json` :

```json
{
  "owner_name": "Williams",
  "agent_name": "HIM",
  "auto_reply": true,
  "reply_delay": 5,
  "away_message": "Salut c'est {agent}, {owner} n'est pas connecté...",
  "smart_reply": true,
  "allowed_contacts": ["+22512345678", "+22587654321"],
  "blocked_contacts": [],
  "working_hours": {
    "start": "09:00",
    "end": "18:00"
  },
  "only_when_offline": true,
  "notifications": {
    "telegram": true,
    "desktop": true
  }
}
```

### Options :

| Option | Description |
|--------|-------------|
| `owner_name` | Ton nom |
| `agent_name` | Nom qui signe les messages |
| `auto_reply` | Réponses automatiques activées |
| `smart_reply` | IA qui adapte les réponses |
| `only_when_offline` | Ne répond que quand tu es offline |
| `working_hours` | Heures où tu es "online" |

---

## 🧠 Types de réponses

### Mode Smart Reply (IA)
L'agent analyse le message et répond contextuellement :

- **Salutations** → "Salut ! 👋 C'est HIM..."
- **Questions** → "Bonne question ! 🤔"
- **Urgences** → "🚨 Je notifie immédiatement !"
- **Merci** → "Avec plaisir ! 🙌"
- **Messages génériques** → Réponses adaptées

### Mode Away Simple
Message fixe : *"Salut c'est HIM, Williams n'est pas connecté..."*

---

## 📱 Intégration WhatsApp réelle

Pour connecter à WhatsApp (pas seulement simulation) :

### Option 1 : Webhook n8n
1. Crée un workflow n8n
2. Reçoit les messages WhatsApp
3. Appelle cet agent via API

### Option 2 : whatsapp-web.js
```javascript
const { Client } = require('whatsapp-web.js');
const client = new Client();

client.on('message', async msg => {
    // Appelle l'agent Python
    const response = await callAgent(msg.from, msg.body);
    msg.reply(response);
});
```

### Option 3 : API WhatsApp Business
Pour usage professionnel (nécessite Meta Business)

---

## 📝 Logs

Toutes les conversations sont loggées :
```
whatsapp-agent/
├── conversations.log  📄 Historique
└── config.json        ⚙️ Configuration
```

Format : `{"timestamp": "...", "sender": "...", "message": "...", "response": "..."}`

---

## 🔔 Notifications

### Telegram
L'agent peut notifier sur Telegram quand :
- Quelqu'un te contacte
- Message urgent reçu
- Erreur dans le système

### Desktop (Windows/Mac/Linux)
Notifications système natives

---

## 🛠️ Commandes

```bash
# Démarrer
python agent.py start

# Configuration
python agent.py setup

# Test rapide
python agent.py test

# Voir les logs
tail -f conversations.log
```

---

## ⚠️ Limitations

- ⚠️ Simulation uniquement sans WhatsApp connecté
- ⚠️ Pour réel : besoin de webhook/API
- ⚠️ Respecte les CGU WhatsApp

---

## 🎯 Utilisations

1. **Réponse auto vacances** → "Je suis en vacances jusqu'au..."
2. **Hors ligne travail** → Répond quand tu es en réunion
3. **Nuit/dodo** → "Je dors, je réponds demain 💤"
4. **Focus mode** → "Mode concentré, je réponds plus tard"

---

Créé le 22 février 2026 par HIM 🤖
