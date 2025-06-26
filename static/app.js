document.addEventListener('DOMContentLoaded', function() {
    var currentChatId = null;
    
    // Initialize new chat on page load
    initializeNewChat();
    
    // Send message functionality
    var messageInput = document.querySelector('input[type="text"]');
    var sendButton = document.querySelector('button');
    
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    function initializeNewChat() {
        fetch('/api/chat/new', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({})
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            currentChatId = data.chat_id;
            console.log('New chat initialized:', currentChatId);
        })
        .catch(function(error) {
            console.error('Error initializing chat:', error);
        });
    }
    
    function sendMessage() {
        var input = document.querySelector('input[type="text"]');
        var message = input.value.trim();
        
        if (!message || !currentChatId) return;
        
        // Clear input
        input.value = '';
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        fetch('/api/chat/' + currentChatId + '/message', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            // Add AI response to chat
            addMessageToChat('assistant', data.response);
        })
        .catch(function(error) {
            console.error('Error sending message:', error);
            addMessageToChat('error', 'Error sending message. Please try again.');
        });
    }
    
    function addMessageToChat(role, content) {
        var chatArea = document.querySelector('.chat-area') || createChatArea();
        
        var messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + role;
        
        var messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = '<strong>' + (role === 'user' ? 'You' : 'Juggernaut AI') + ':</strong><p>' + content + '</p>';
        
        messageDiv.appendChild(messageContent);
        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }
    
    function createChatArea() {
        var chatArea = document.createElement('div');
        chatArea.className = 'chat-area';
        chatArea.style.cssText = 'height: 400px; overflow-y: auto; padding: 20px; margin-bottom: 20px; border: 1px solid #333; background: #1a1a1a; color: white;';
        
        var container = document.querySelector('.container') || document.body;
        var inputContainer = document.querySelector('.input-container') || document.querySelector('input').parentElement;
        
        container.insertBefore(chatArea, inputContainer);
        return chatArea;
    }
});
