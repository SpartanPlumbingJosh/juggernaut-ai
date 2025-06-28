class JuggernautAI {
    constructor() {
        this.currentChatId = 'general';
        this.init();
    }
    
    init() {
        console.log('Juggernaut AI Interface Ready');
        this.initializeChat();
    }
    
    initializeChat() {
        const sendBtn = document.getElementById('send-btn');
        const chatInput = document.getElementById('chat-input');
        
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
    }
    
    async sendMessage() {
        const chatInput = document.getElementById('chat-input');
        const message = chatInput.value.trim();
        
        if (!message) return;
        
        chatInput.value = '';
        this.addMessageToChat('user', message);
        this.addMessageToChat('assistant', 'Processing...');
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, chat_id: this.currentChatId })
            });
            
            const data = await response.json();
            this.updateLastMessage(data.response || 'Error occurred');
            
        } catch (error) {
            this.updateLastMessage('Error: ' + error.message);
        }
    }
    
    addMessageToChat(type, content) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerHTML = `<div class="message-content">${content}</div>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    updateLastMessage(content) {
        const messages = document.querySelectorAll('.message.assistant');
        if (messages.length > 0) {
            const lastMessage = messages[messages.length - 1];
            lastMessage.querySelector('.message-content').innerHTML = content;
        }
    }
}

window.juggernautAI = new JuggernautAI();

