# -*- coding: utf-8 -*-
"""
HIM WhatsApp Agent - Connecteur Webhook
Permet de recevoir des messages via webhook HTTP
"""

from flask import Flask, request, jsonify
from agent import HIMWhatsAppAgent
import threading

app = Flask(__name__)
agent = HIMWhatsAppAgent()


@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Reçoit les messages WhatsApp et répond"""
    try:
        data = request.json
        
        sender = data.get('sender')
        message = data.get('message')
        
        if not sender or not message:
            return jsonify({"error": "Missing sender or message"}), 400
        
        # Traite le message
        response = agent.process_message(sender, message)
        
        return jsonify({
            "status": "ok",
            "response": response,
            "handled": True
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    """Status de l'agent"""
    return jsonify({
        "status": "running",
        "agent_name": agent.config['agent_name'],
        "auto_reply": agent.config['auto_reply'],
        "smart_reply": agent.config['smart_reply']
    })


@app.route('/config', methods=['GET', 'POST'])
def config():
    """Gère la configuration"""
    if request.method == 'POST':
        new_config = request.json
        agent.config.update(new_config)
        agent.save_config()
        return jsonify({"status": "updated"})
    
    return jsonify(agent.config)


def run_webhook_server(port=5000):
    """Démarre le serveur webhook"""
    print(f"🌐 Webhook server starting on port {port}")
    print(f"📍 Endpoint: http://localhost:{port}/webhook/whatsapp")
    print(f"📊 Status: http://localhost:{port}/status")
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    run_webhook_server()
