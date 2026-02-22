#!/usr/bin/env python3
"""
HIM Remote Agent
Agent qui tourne sur ton PC et se connecte à OpenClaw
Permet l'exécution de commandes à distance de façon sécurisée
"""

import socketio
import subprocess
import json
import os
import sys
import platform
import psutil
from datetime import datetime
from pathlib import Path
import threading
import time

# Configuration
AGENT_DIR = Path(__file__).parent
CONFIG_FILE = AGENT_DIR / "remote-config.json"
LOG_FILE = AGENT_DIR / "remote-agent.log"

# Serveur OpenClaw (à configurer)
DEFAULT_SERVER = "wss://your-openclaw-server.com"
AGENT_VERSION = "1.0.0"


class HIMRemoteAgent:
    """Agent distant pour contrôle PC"""
    
    def __init__(self):
        self.sio = socketio.Client()
        self.config = self.load_config()
        self.connected = False
        self.agent_id = self.get_agent_id()
        self.setup_handlers()
        
    def load_config(self):
        """Charge la configuration"""
        default_config = {
            "server_url": DEFAULT_SERVER,
            "agent_name": "HIM-PC-Agent",
            "owner": "Williams",
            "allowed_commands": ["ls", "dir", "docker", "python", "node", "npm", "git"],
            "blocked_commands": ["rm -rf /", "format", "del /f"],
            "auto_connect": True,
            "heartbeat_interval": 30
        }
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        else:
            self.save_config(default_config)
            
        return default_config
    
    def save_config(self):
        """Sauvegarde la configuration"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_agent_id(self):
        """Génère un ID unique pour cet agent"""
        import uuid
        machine_id_file = AGENT_DIR / ".machine_id"
        
        if machine_id_file.exists():
            return machine_id_file.read_text().strip()
        
        new_id = str(uuid.uuid4())[:8]
        machine_id_file.write_text(new_id)
        return new_id
    
    def log(self, message):
        """Log un message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry + "\n")
    
    def get_system_info(self):
        """Récupère les infos système"""
        return {
            "agent_id": self.agent_id,
            "agent_version": AGENT_VERSION,
            "hostname": platform.node(),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            "timestamp": datetime.now().isoformat()
        }
    
    def setup_handlers(self):
        """Configure les gestionnaires d'événements"""
        
        @self.sio.event
        def connect():
            self.connected = True
            self.log("✅ Connecté au serveur OpenClaw")
            
            # Envoie les infos système
            self.sio.emit('register', {
                'agent_id': self.agent_id,
                'agent_name': self.config['agent_name'],
                'owner': self.config['owner'],
                'system_info': self.get_system_info()
            })
        
        @self.sio.event
        def disconnect():
            self.connected = False
            self.log("❌ Déconnecté du serveur")
        
        @self.sio.on('execute_command')
        def on_execute_command(data):
            """Reçoit une commande à exécuter"""
            command = data.get('command')
            request_id = data.get('request_id')
            
            self.log(f"📥 Commande reçue: {command}")
            
            # Vérifie si la commande est autorisée
            if not self.is_command_allowed(command):
                result = {
                    'success': False,
                    'error': 'Commande non autorisée',
                    'request_id': request_id
                }
            else:
                # Exécute la commande
                result = self.execute_command(command)
                result['request_id'] = request_id
            
            # Envoie le résultat
            self.sio.emit('command_result', result)
        
        @self.sio.on('get_status')
        def on_get_status():
            """Envoie le statut système"""
            self.sio.emit('status', self.get_system_info())
        
        @self.sio.on('ping')
        def on_ping():
            """Répond au ping"""
            self.sio.emit('pong', {'agent_id': self.agent_id, 'timestamp': datetime.now().isoformat()})
    
    def is_command_allowed(self, command):
        """Vérifie si une commande est autorisée"""
        # Vérifie les commandes bloquées
        for blocked in self.config['blocked_commands']:
            if blocked in command.lower():
                return False
        
        # Si allowed_commands est vide, tout est autorisé (sauf bloqué)
        if not self.config['allowed_commands']:
            return True
        
        # Vérifie si la commande est dans la liste blanche
        cmd_first = command.split()[0].lower()
        return cmd_first in self.config['allowed_commands']
    
    def execute_command(self, command):
        """Exécute une commande système"""
        try:
            self.log(f"Exécution: {command}")
            
            # Exécute avec timeout
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(Path.home())
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout[:10000],  # Limite la taille
                'stderr': result.stderr[:10000],
                'returncode': result.returncode,
                'command': command,
                'timestamp': datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout - commande trop longue',
                'command': command,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': command,
                'timestamp': datetime.now().isoformat()
            }
    
    def connect(self):
        """Se connecte au serveur"""
        try:
            self.log(f"🔗 Connexion à {self.config['server_url']}...")
            self.sio.connect(self.config['server_url'])
            return True
        except Exception as e:
            self.log(f"❌ Erreur de connexion: {e}")
            return False
    
    def run(self):
        """Boucle principale"""
        self.log("=" * 60)
        self.log(f"🚀 HIM Remote Agent v{AGENT_VERSION}")
        self.log(f"🆔 Agent ID: {self.agent_id}")
        self.log("=" * 60)
        
        # Connexion
        if not self.connect():
            self.log("⚠️  Connexion impossible, nouvelle tentative dans 10s...")
            time.sleep(10)
            return self.run()
        
        # Boucle de maintien de connexion
        try:
            while True:
                if not self.connected:
                    self.log("🔌 Déconnecté, tentative de reconnexion...")
                    if not self.connect():
                        time.sleep(10)
                        continue
                
                # Heartbeat
                time.sleep(self.config['heartbeat_interval'])
                
        except KeyboardInterrupt:
            self.log("🛑 Arrêt demandé")
            self.sio.disconnect()


def setup_agent():
    """Configuration initiale"""
    print("🔧 Configuration de HIM Remote Agent")
    print("=" * 40)
    
    config = {
        "server_url": input(f"URL du serveur [{DEFAULT_SERVER}]: ") or DEFAULT_SERVER,
        "agent_name": input("Nom de l'agent [HIM-PC-Agent]: ") or "HIM-PC-Agent",
        "owner": input("Ton nom [Williams]: ") or "Williams",
    }
    
    agent = HIMRemoteAgent()
    agent.config.update(config)
    agent.save_config()
    
    print("\n✅ Configuration sauvegardée!")
    print(f"Fichier: {CONFIG_FILE}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            setup_agent()
        elif sys.argv[1] == "start":
            agent = HIMRemoteAgent()
            agent.run()
        else:
            print("Usage: python remote_agent.py [setup|start]")
    else:
        agent = HIMRemoteAgent()
        agent.run()
