document.addEventListener('DOMContentLoaded', () => {
    let currentChatId = null;
    
    // Initialize new chat on page load
    initializeNewChat();
    
    // Send message functionality
    const messageInput = document.querySelector('input[type="text"]');
    const sendButton = document.querySelector('button');
    
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (messageInput) {
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    async function initializeNewChat() {
        try {
            const response = await fetch('/api/chat/new', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({})
            });
            const data = await response.json();
            currentChatId = data.chat_id;
            console.log('New chat initialized:', currentChatId);
        } catch (error) {
            console.error('Error initializing chat:', error);
        }
    }
    
    async function sendMessage() {
        const input = document.querySelector('input[type="text"]');
        const message = input.value.trim();
        
        if (!message || !currentChatId) return;
        
        // Clear input
        input.value = '';
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        try {
            const response = await fetch(/api/chat/+currentChatId+/message, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            });
            
            const data = await response.json();
            
            // Add AI response to chat
            addMessageToChat('assistant', data.response);
            
        } catch (error) {
            console.error('Error sending message:', error);
            addMessageToChat('error', 'Error sending message. Please try again.');
        }
    }
    
    function addMessageToChat(role, content) {
        const chatArea = document.querySelector('.chat-area') || createChatArea();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + role;
        messageDiv.innerHTML = '<div class="message-content"><strong>' + (role === 'user' ? 'You' : 'Juggernaut AI') + ':</strong><p>' + content + '</p></div>';
        
        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }
    
    function createChatArea() {
        const chatArea = document.createElement('div');
        chatArea.className = 'chat-area';
        chatArea.style.cssText = 'height: 400px; overflow-y: auto; padding: 20px; margin-bottom: 20px; border: 1px solid #333; background: #1a1a1a; color: white;';
        
        const container = document.querySelector('.container') || document.body;
        const inputContainer = document.querySelector('.input-container') || document.querySelector('input').parentElement;
        
        container.insertBefore(chatArea, inputContainer);
        return chatArea;
    }
});
