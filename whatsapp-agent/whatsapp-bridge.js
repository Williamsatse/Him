const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Configuration
const AGENT_WEBHOOK_URL = process.env.AGENT_WEBHOOK_URL || 'http://localhost:5000/webhook/whatsapp';
const LOG_FILE = path.join(__dirname, 'whatsapp-bridge.log');

// Logger
function log(message) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] ${message}`;
    console.log(logEntry);
    fs.appendFileSync(LOG_FILE, logEntry + '\n');
}

// Initialiser le client WhatsApp
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Afficher le QR code
client.on('qr', (qr) => {
    console.log('\n=== SCANNE CE QR CODE AVEC TON WHATSAPP ===\n');
    qrcode.generate(qr, { small: true });
    console.log('\n==========================================\n');
    log('QR Code généré - En attente du scan');
});

// Client prêt
client.on('ready', () => {
    console.log('\n✅ HIM WhatsApp Agent est connecté !');
    console.log('🤖 Prêt à répondre automatiquement\n');
    log('Client WhatsApp connecté et prêt');
});

// Erreur de connexion
client.on('disconnected', (reason) => {
    console.log('\n❌ Déconnecté :', reason);
    log('Déconnecté : ' + reason);
    client.destroy();
    process.exit(0);
});

// Recevoir un message
client.on('message_create', async (msg) => {
    // Ne pas répondre à tes propres messages (si tu écris en tant que Williams)
    if (msg.fromMe) return;
    
    // Ne pas répondre aux messages de groupes (optionnel, décommente si tu veux)
    // if (msg.from.includes('@g.us')) return;
    
    const sender = msg.from;
    const messageText = msg.body;
    const senderName = msg._data.notifyName || msg.from;
    
    console.log('\n📱 Message reçu :');
    console.log(`   De : ${senderName} (${sender})`);
    console.log(`   💬 ${messageText}`);
    
    log(`Message reçu de ${senderName} (${sender}) : ${messageText}`);
    
    // Ne pas répondre si c'est toi (pour éviter les boucles)
    // Tu peux ajouter ton propre numéro ici pour exclure
    const ownerNumber = process.env.OWNER_NUMBER;
    if (ownerNumber && sender.includes(ownerNumber)) {
        console.log('   ℹ️ Message du propriétaire - Pas de réponse auto');
        return;
    }
    
    try {
        // Appeler l'agent Python
        console.log('   🤖 Génération de la réponse...');
        
        const response = await axios.post(AGENT_WEBHOOK_URL, {
            sender: sender,
            message: messageText,
            sender_name: senderName,
            timestamp: new Date().toISOString()
        }, {
            timeout: 10000
        });
        
        if (response.data && response.data.response) {
            const replyText = response.data.response;
            
            // Attendre un peu avant de répondre (paraître naturel)
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Envoyer la réponse
            await msg.reply(replyText);
            
            console.log('   ✅ Réponse envoyée :');
            console.log(`      ${replyText}`);
            log(`Réponse envoyée : ${replyText}`);
        } else {
            console.log('   ⏸️ Pas de réponse (agent silencieux)');
        }
        
    } catch (error) {
        console.error('   ❌ Erreur :', error.message);
        log(`Erreur : ${error.message}`);
        
        // Message d'erreur par défaut
        try {
            await msg.reply("🇩🇪 Message reçu, mais je rencontre un problème technique. Williams te répondra bientôt !");
        } catch (e) {
            console.error('   ❌ Impossible d\'envoyer le message d\'erreur');
        }
    }
});

// Démarrer
console.log('\n🚀 Démarrage de HIM WhatsApp Bridge...');
console.log(`📡 Agent webhook : ${AGENT_WEBHOOK_URL}`);
console.log('⏳ En attente du QR code...\n');

client.initialize().catch(err => {
    console.error('Erreur d\'initialisation :', err);
    process.exit(1);
});

// Gérer l'arrêt propre
process.on('SIGINT', async () => {
    console.log('\n🛑 Arrêt en cours...');
    await client.destroy();
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('\n🛑 Arrêt en cours...');
    await client.destroy();
    process.exit(0);
});
