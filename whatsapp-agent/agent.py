# -*- coding: utf-8 -*-
"""
HIM WhatsApp Agent
Agent IA pour réponses automatiques WhatsApp
"""

import json
import time
import os
import random
from datetime import datetime
from pathlib import Path

# Configuration
AGENT_DIR = Path(__file__).parent
CONFIG_FILE = AGENT_DIR / "config.json"
LOG_FILE = AGENT_DIR / "conversations.log"
RESPONSES_FILE = AGENT_DIR / "responses.json"


class HIMWhatsAppAgent:
    """Agent IA pour WhatsApp"""
    
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.conversations = {}
        
    def load_config(self):
        """Charge la configuration"""
        default_config = {
            "owner_name": "Williams",
            "agent_name": "HIM",
            "auto_reply": True,
            "reply_delay": 5,  # Secondes avant réponse
            "away_message": "Salut c'est {agent}, {owner} n'est pas connecté en ce moment. Veuillez patienter un moment 😉",
            "smart_reply": True,  # Réponses IA personnalisées
            "allowed_contacts": [],  # Numéros autorisés (vide = tous)
            "blocked_contacts": [],  # Numéros bloqués
            "working_hours": {
                "start": "09:00",
                "end": "18:00"
            },
            "only_when_offline": True,  # Ne répondre que quand owner est offline
            "webhook_url": None,  # URL pour recevoir messages
            "notifications": {
                "telegram": True,
                "desktop": True
            }
        }
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                default_config.update(config)
        else:
            self.save_config(default_config)
        
        return default_config
    
    def save_config(self):
        """Sauvegarde la configuration"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def log_message(self, sender, message, response=None):
        """Log une conversation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "sender": sender,
            "message": message,
            "response": response
        }
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def is_allowed_contact(self, phone_number):
        """Vérifie si le contact est autorisé"""
        if not self.config["allowed_contacts"]:
            return phone_number not in self.config["blocked_contacts"]
        return phone_number in self.config["allowed_contacts"]
    
    def is_working_hours(self):
        """Vérifie si c'est les heures de travail"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return self.config["working_hours"]["start"] <= current_time <= self.config["working_hours"]["end"]
    
    def generate_response(self, message, sender_name=""):
        """Génère une réponse intelligente"""
        message_lower = message.lower()
        
        # Réponses contextuelles
        if any(word in message_lower for word in ["salut", "bonjour", "hello", "hey"]):
            return f"Salut {sender_name} ! 👋 C\'est {self.config['agent_name']}. {self.config['owner_name']} est occupé, je prends le relais."
        
        if any(word in message_lower for word in ["ça va", "ca va", "cv", "comment tu vas"]):
            return "Je vais bien, merci ! Et toi ? 😊"
        
        if any(word in message_lower for word in ["au revoir", "bye", "à plus", "a plus"]):
            return "À plus tard ! 👋 Passe une bonne journée."
        
        if any(word in message_lower for word in ["merci", "thank", "thx"]):
            return "Avec plaisir ! 🙌"
        
        if "?" in message:
            return f"Bonne question ! 🤔 Laisse moi vérifier ça avec {self.config['owner_name']} et je te reviens."
        
        if any(word in message_lower for word in ["urgent", "important", "vite", "asap"]):
            return f"🚨 Message marqué comme urgent ! Je notifie immédiatement {self.config['owner_name']}."
        
        # Réponses génériques
        generic_responses = [
            f"Je suis là pour toi ! {self.config['owner_name']} n\\'est pas dispo, mais je peux prendre un message 📩",
            f"Message reçu ✅ Je transmets à {self.config['owner_name']} dès qu\\'il/elle est disponible.",
            f"Salut ! 👋 {self.config['owner_name']} est en mode focus. Je peux noter ton message ?",
            "D\\'accord, je note ça ! 📝",
            "Compris ! ✌️"
        ]
        
        return random.choice(generic_responses)
    
    def process_message(self, sender, message, timestamp=None):
        """Traite un message entrant"""
        if not self.is_allowed_contact(sender):
            self.log_message(sender, message, "CONTACT_BLOQUE")
            return None
        
        # Vérifie si on doit répondre
        if not self.config["auto_reply"]:
            return None
        
        if self.config["only_when_offline"] and self.is_working_hours():
            # Pendant les heures de travail, ne répond pas (owner est là)
            return None
        
        # Génère la réponse
        if self.config["smart_reply"]:
            response = self.generate_response(message, sender)
        else:
            response = self.config["away_message"].format(
                agent=self.config["agent_name"],
                owner=self.config["owner_name"]
            )
        
        # Attend avant de répondre (paraître naturel)
        time.sleep(self.config["reply_delay"])
        
        self.log_message(sender, message, response)
        return response
    
    def simulate_whatsapp_webhook(self, sender, message):
        """Simule la réception d'un message WhatsApp"""
        print(f"\\n📱 Message reçu de {sender}:")
        print(f"   💬 {message}")
        
        response = self.process_message(sender, message)
        
        if response:
            print(f"   🤖 Réponse: {response}")
            return response
        else:
            print("   ⏸️ Pas de réponse automatique")
            return None
    
    def start(self):
        """Démarre l'agent"""
        self.running = True
        print("=" * 60)
        print(f"🤖 {self.config['agent_name']} WhatsApp Agent démarré")
        print("=" * 60)
        print(f"👤 Propriétaire: {self.config['owner_name']}")
        print(f"💬 Mode: {'Auto-réponse IA' if self.config['smart_reply'] else 'Message d\'absence'}")
        print(f"⏰ Heures travail: {self.config['working_hours']['start']} - {self.config['working_hours']['end']}")
        print(f"📝 Log: {LOG_FILE}")
        print("=" * 60)
        print()
        
        # Simulation (à remplacer par webhook réel)
        print("Mode simulation activé. Envoie des messages test...")
        print("Tape 'quit' pour arrêter")
        print()
        
        # Exemples de messages
        test_messages = [
            ("+22512345678", "Salut !"),
            ("+22587654321", "Tu fais quoi ?"),
            ("+22511223344", "C\'est urgent !"),
        ]
        
        for sender, msg in test_messages:
            if not self.running:
                break
            self.simulate_whatsapp_webhook(sender, msg)
            time.sleep(2)
        
        print("\\nAgent prêt pour messages réels via webhook...")
        
        while self.running:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
    
    def stop(self):
        """Arrête l'agent"""
        self.running = False
        print("\\n🛑 Agent arrêté")


def setup_agent():
    """Configure l'agent pour la première utilisation"""
    print("🔧 Configuration de HIM WhatsApp Agent")
    print("=" * 40)
    
    config = {
        "owner_name": input("Ton nom: ") or "Williams",
        "agent_name": input("Nom de l\'agent [HIM]: ") or "HIM",
        "auto_reply": input("Réponse auto? (o/n) [o]: ").lower() != "n",
        "smart_reply": input("Mode IA intelligent? (o/n) [o]: ").lower() != "n",
    }
    
    agent = HIMWhatsAppAgent()
    agent.config.update(config)
    agent.save_config()
    
    print("\\n✅ Configuration sauvegardée!")
    print(f"Config: {CONFIG_FILE}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            setup_agent()
        elif sys.argv[1] == "start":
            agent = HIMWhatsAppAgent()
            agent.start()
        elif sys.argv[1] == "test":
            agent = HIMWhatsAppAgent()
            # Test rapide
            agent.simulate_whatsapp_webhook("+22512345678", "Salut ça va ?")
        else:
            print("Usage: python agent.py [setup|start|test]")
    else:
        agent = HIMWhatsAppAgent()
        agent.start()
