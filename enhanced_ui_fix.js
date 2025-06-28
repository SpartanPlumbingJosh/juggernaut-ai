// ENHANCED UI FIX - Non-blocking Interface
// Allows new messages while processing, adds cancel functionality

// Override the original sendMessage function to be non-blocking
class EnhancedJuggernautAI extends JuggernautAI {
    constructor() {
        super();
        this.currentRequest = null;
        this.requestQueue = [];
        this.processingCount = 0;
    }
    
    async sendMessage(predefinedMessage = null) {
        const chatInput = document.getElementById('chat-input');
        const message = predefinedMessage || chatInput.value.trim();
        
        if (!message) return;
        
        console.log(`💬 Sending message: ${message.substring(0, 50)}...`);
        
        // Clear input if not predefined message
        if (!predefinedMessage && chatInput) {
            chatInput.value = '';
            chatInput.style.height = 'auto';
        }
        
        // Add user message to chat
        this.addMessageToChat('user', message);
        
        // Create unique request ID
        const requestId = Date.now() + Math.random();
        
        // Show processing indicator (non-blocking)
        this.showProcessingIndicator(requestId);
        
        try {
            // Get chat context
            const context = this.getChatContext();
            
            // Create AbortController for cancellation
            const controller = new AbortController();
            this.currentRequest = { controller, requestId };
            
            // Send to API with timeout and abort signal
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    chat_id: this.currentChatId,
                    context: context,
                    request_id: requestId
                }),
                signal: controller.signal
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add AI response to chat
                this.addMessageToChat('assistant', data.response, data.metadata);
                console.log(`🤖 Response received in ${data.metadata?.response_time}ms`);
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
            
        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('🛑 Request cancelled by user');
                this.addMessageToChat('assistant', 
                    '⚠️ Request cancelled. You can send a new message anytime.');
            } else {
                console.error('❌ Chat error:', error);
                this.addMessageToChat('assistant', 
                    `I encountered an error: ${error.message}. Please try again.`);
            }
        } finally {
            this.hideProcessingIndicator(requestId);
            this.currentRequest = null;
        }
    }
    
    showProcessingIndicator(requestId) {
        this.processingCount++;
        
        // Create or update processing message
        let processingMsg = document.getElementById('processing-message');
        if (!processingMsg) {
            processingMsg = document.createElement('div');
            processingMsg.id = 'processing-message';
            processingMsg.className = 'message assistant processing';
            processingMsg.innerHTML = `
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-text">
                        <div class="processing-indicator">
                            <span class="processing-dots">●●●</span>
                            <span class="processing-text">Processing your request...</span>
                            <button class="cancel-btn" onclick="enhancedJuggernautAI.cancelCurrentRequest()">
                                ❌ Cancel
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            const chatMessages = document.getElementById('chat-messages');
            chatMessages.appendChild(processingMsg);
        }
        
        // Animate processing dots
        this.animateProcessingDots();
        
        // Scroll to bottom
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    hideProcessingIndicator(requestId) {
        this.processingCount--;
        
        if (this.processingCount <= 0) {
            const processingMsg = document.getElementById('processing-message');
            if (processingMsg) {
                processingMsg.remove();
            }
            this.processingCount = 0;
        }
    }
    
    animateProcessingDots() {
        const dots = document.querySelector('.processing-dots');
        if (!dots) return;
        
        let dotCount = 1;
        const interval = setInterval(() => {
            if (!document.querySelector('.processing-dots')) {
                clearInterval(interval);
                return;
            }
            
            dots.textContent = '●'.repeat(dotCount) + '○'.repeat(3 - dotCount);
            dotCount = (dotCount % 3) + 1;
        }, 500);
    }
    
    cancelCurrentRequest() {
        if (this.currentRequest) {
            this.currentRequest.controller.abort();
            console.log('🛑 Cancelling current request...');
        }
    }
    
    // Override setLoading to be non-blocking
    setLoading(loading) {
        // Don't disable the send button or show overlay
        // Keep interface fully responsive
        console.log(loading ? '⏳ Processing...' : '✅ Ready');
    }
}

// CSS for enhanced processing indicator
const enhancedStyles = `
<style>
.processing-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    border-left: 3px solid #ff4444;
}

.processing-dots {
    font-size: 18px;
    color: #ff4444;
    font-weight: bold;
}

.processing-text {
    color: #ffffff;
    font-style: italic;
}

.cancel-btn {
    background: #ff4444;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    transition: background 0.2s;
}

.cancel-btn:hover {
    background: #ff6666;
}

.message.processing {
    opacity: 0.9;
}

/* Keep send button always enabled */
#send-btn:disabled {
    opacity: 1 !important;
    cursor: pointer !important;
    background: #ff4444 !important;
}

/* Hide the blocking overlay */
#loading-overlay {
    display: none !important;
}
</style>
`;

// Inject enhanced styles
document.head.insertAdjacentHTML('beforeend', enhancedStyles);

// Replace the original instance with enhanced version
if (typeof juggernautAI !== 'undefined') {
    // Save current state
    const currentChatId = juggernautAI.currentChatId;
    const chatHistory = juggernautAI.chatHistory;
    
    // Create enhanced instance
    window.enhancedJuggernautAI = new EnhancedJuggernautAI();
    
    // Restore state
    enhancedJuggernautAI.currentChatId = currentChatId;
    enhancedJuggernautAI.chatHistory = chatHistory;
    
    // Replace global reference
    window.juggernautAI = enhancedJuggernautAI;
    
    console.log('🚀 Enhanced non-blocking interface activated!');
    console.log('✅ You can now send messages while processing');
    console.log('✅ Cancel button available during processing');
    console.log('✅ Interface stays responsive');
}

