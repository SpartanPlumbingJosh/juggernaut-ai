// JUGGERNAUT AI - INTEGRATED UI JAVASCRIPT
// Professional functionality with real API integration

class JuggernautAI {
    constructor() {
        this.currentChatId = 'general';
        this.chatHistory = {};
        this.isLoading = false;
        this.systemMetrics = {};
        this.currentRequest = null;
        this.processingCount = 0;
        
        this.init();
    }
    
    init() {
        console.log('🚀 Initializing Juggernaut AI Interface...');
        
        // Initialize components
        this.initializeNavigation();
        this.initializeChat();
        this.initializeFileHandling();
        this.initializeSystemMonitoring();
        this.initializeBrowser();
        this.initializeCommunication();
        this.initializeSettings();
        
        // Load initial data
        this.loadChatHistory();
        this.updateSystemMetrics();
        
        console.log('✅ Juggernaut AI Interface Ready!');
    }
    
    // Navigation System
    initializeNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        const contentSections = document.querySelectorAll('.content-section');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const sidebar = document.querySelector('.sidebar');
        
        // Navigation switching
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const section = item.dataset.section;
                if (section) {
                    this.switchSection(section);
                    
                    // Update active nav item
                    navItems.forEach(nav => nav.classList.remove('active'));
                    item.classList.add('active');
                }
            });
        });
        
        // Sidebar toggle for mobile
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('open');
            });
        }
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && 
                !sidebar.contains(e.target) && 
                !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }
    
    switchSection(sectionName) {
        const sections = document.querySelectorAll('.content-section');
        sections.forEach(section => section.classList.remove('active'));
        
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.classList.add('active');
        }
        
        console.log(`📍 Switched to ${sectionName} section`);
    }
    
    // Chat System
    initializeChat() {
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const chatTabs = document.querySelectorAll('.tab');
        const tabAdd = document.querySelector('.tab-add');
        
        // Send message handlers
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (chatInput) {
            chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                } else if (e.key === 'Enter' && e.shiftKey) {
                    // Allow new line
                    return;
                }
            });
            
            // Auto-resize textarea
            chatInput.addEventListener('input', () => {
                chatInput.style.height = 'auto';
                chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
            });
        }
        
        // Chat tab switching
        chatTabs.forEach(tab => {
            if (!tab.classList.contains('tab-add')) {
                tab.addEventListener('click', (e) => {
                    if (!e.target.classList.contains('tab-close')) {
                        this.switchChat(tab.dataset.chat);
                    }
                });
                
                // Tab close functionality
                const closeBtn = tab.querySelector('.tab-close');
                if (closeBtn) {
                    closeBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.closeChat(tab.dataset.chat);
                    });
                }
            }
        });
        
        // Add new chat tab
        if (tabAdd) {
            tabAdd.addEventListener('click', () => this.createNewChat());
        }
        
        // Quick action buttons
        window.sendQuickMessage = (message) => {
            this.sendMessage(message);
        };
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
        
        // Show non-blocking processing indicator
        this.showProcessingIndicator(requestId);
        
        try {
            // Get chat context
            const context = this.getChatContext();
            
            // Create AbortController for cancellation
            const controller = new AbortController();
            this.currentRequest = { controller, requestId };
            
            // Send to API with abort signal
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
    
    addMessageToChat(type, content, metadata = null) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        // Hide welcome section if it exists
        const welcomeSection = document.querySelector('.welcome-section');
        if (welcomeSection && chatMessages.children.length === 0) {
            welcomeSection.style.display = 'none';
        }
        
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = type === 'user' ? 'U' : '🤖';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        
        // Format content (support for markdown-like formatting)
        messageText.innerHTML = this.formatMessage(content);
        
        messageContent.appendChild(messageText);
        
        // Add metadata if available
        if (metadata) {
            const messageMeta = document.createElement('div');
            messageMeta.className = 'message-meta';
            messageMeta.innerHTML = `
                <span>⚡ ${metadata.response_time}ms</span>
                <span>📝 ${metadata.tokens} tokens</span>
                <span>🕒 ${new Date().toLocaleTimeString()}</span>
            `;
            messageContent.appendChild(messageMeta);
        }
        
        // Add message actions for assistant messages
        if (type === 'assistant') {
            const messageActions = document.createElement('div');
            messageActions.className = 'message-actions';
            messageActions.innerHTML = `
                <button class="message-action" onclick="juggernautAI.copyMessage(this)" title="Copy">
                    📋 Copy
                </button>
                <button class="message-action" onclick="juggernautAI.editMessage(this)" title="Edit">
                    ✏️ Edit
                </button>
                <button class="message-action" onclick="juggernautAI.deleteMessage(this)" title="Delete">
                    🗑️ Delete
                </button>
            `;
            messageContent.appendChild(messageActions);
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Store in chat history
        if (!this.chatHistory[this.currentChatId]) {
            this.chatHistory[this.currentChatId] = [];
        }
        
        this.chatHistory[this.currentChatId].push({
            type: type,
            content: content,
            timestamp: Date.now(),
            metadata: metadata
        });
    }
    
    formatMessage(content) {
        // Basic markdown-like formatting
        let formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
        
        // Format code blocks
        formatted = formatted.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        
        return formatted;
    }
    
    getChatContext() {
        const history = this.chatHistory[this.currentChatId] || [];
        return history.slice(-10); // Last 10 messages for context
    }
    
    switchChat(chatId) {
        this.currentChatId = chatId;
        
        // Update active tab
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(tab => tab.classList.remove('active'));
        
        const activeTab = document.querySelector(`[data-chat="${chatId}"]`);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        // Load chat history
        this.loadChatMessages(chatId);
        
        console.log(`💬 Switched to chat: ${chatId}`);
    }
    
    loadChatMessages(chatId) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        // Clear current messages
        chatMessages.innerHTML = '';
        
        // Load messages from history
        const history = this.chatHistory[chatId] || [];
        
        if (history.length === 0) {
            // Show welcome section for empty chats
            const welcomeSection = document.querySelector('.welcome-section');
            if (welcomeSection) {
                welcomeSection.style.display = 'block';
            }
        } else {
            history.forEach(msg => {
                this.addMessageToChat(msg.type, msg.content, msg.metadata);
            });
        }
    }
    
    createNewChat() {
        const chatName = prompt('Enter chat name:');
        if (!chatName) return;
        
        const chatId = chatName.toLowerCase().replace(/\s+/g, '-');
        
        // Create new tab
        const tabsContainer = document.querySelector('.chat-tabs');
        const addButton = document.querySelector('.tab-add');
        
        const newTab = document.createElement('div');
        newTab.className = 'tab';
        newTab.dataset.chat = chatId;
        newTab.innerHTML = `
            <span>${chatName}</span>
            <button class="tab-close">×</button>
        `;
        
        // Add event listeners
        newTab.addEventListener('click', (e) => {
            if (!e.target.classList.contains('tab-close')) {
                this.switchChat(chatId);
            }
        });
        
        const closeBtn = newTab.querySelector('.tab-close');
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.closeChat(chatId);
        });
        
        tabsContainer.insertBefore(newTab, addButton);
        
        // Switch to new chat
        this.switchChat(chatId);
        
        console.log(`➕ Created new chat: ${chatName}`);
    }
    
    closeChat(chatId) {
        if (chatId === 'general') {
            alert('Cannot close the general chat');
            return;
        }
        
        // Remove tab
        const tab = document.querySelector(`[data-chat="${chatId}"]`);
        if (tab) {
            tab.remove();
        }
        
        // Remove from history
        delete this.chatHistory[chatId];
        
        // Switch to general chat if current chat was closed
        if (this.currentChatId === chatId) {
            this.switchChat('general');
        }
        
        console.log(`❌ Closed chat: ${chatId}`);
    }
    
    // Message Actions
    copyMessage(button) {
        const messageText = button.closest('.message-content').querySelector('.message-text');
        const text = messageText.textContent;
        
        navigator.clipboard.writeText(text).then(() => {
            button.textContent = '✅ Copied';
            setTimeout(() => {
                button.innerHTML = '📋 Copy';
            }, 2000);
        });
    }
    
    editMessage(button) {
        const messageText = button.closest('.message-content').querySelector('.message-text');
        const currentText = messageText.textContent;
        
        const newText = prompt('Edit message:', currentText);
        if (newText && newText !== currentText) {
            messageText.textContent = newText;
        }
    }
    
    deleteMessage(button) {
        if (confirm('Delete this message?')) {
            const message = button.closest('.message');
            message.remove();
        }
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        const loadingOverlay = document.getElementById('loading-overlay');
        const sendBtn = document.getElementById('send-btn');
        
        if (loadingOverlay) {
            loadingOverlay.classList.toggle('active', loading);
        }
        
        if (sendBtn) {
            sendBtn.disabled = loading;
        }
    }
    
    // File Handling
    initializeFileHandling() {
        const fileInput = document.getElementById('hidden-file-input');
        const attachBtn = document.getElementById('attach-file');
        const uploadBtn = document.getElementById('upload-btn');
        const fileDropZone = document.getElementById('file-drop-zone');
        const chatContent = document.querySelector('.chat-content');
        
        // File input handlers
        if (attachBtn && fileInput) {
            attachBtn.addEventListener('click', () => fileInput.click());
        }
        
        if (uploadBtn && fileInput) {
            uploadBtn.addEventListener('click', () => fileInput.click());
        }
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                this.handleFileUpload(e.target.files);
            });
        }
        
        // Drag and drop
        if (chatContent) {
            chatContent.addEventListener('dragover', (e) => {
                e.preventDefault();
                if (fileDropZone) {
                    fileDropZone.classList.add('active');
                }
            });
            
            chatContent.addEventListener('dragleave', (e) => {
                e.preventDefault();
                if (!chatContent.contains(e.relatedTarget)) {
                    if (fileDropZone) {
                        fileDropZone.classList.remove('active');
                    }
                }
            });
            
            chatContent.addEventListener('drop', (e) => {
                e.preventDefault();
                if (fileDropZone) {
                    fileDropZone.classList.remove('active');
                }
                this.handleFileUpload(e.dataTransfer.files);
            });
        }
    }
    
    async handleFileUpload(files) {
        if (!files || files.length === 0) return;
        
        console.log(`📁 Uploading ${files.length} files...`);
        
        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });
        
        this.setLoading(true);
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add file analysis to chat
                this.addMessageToChat('assistant', data.analysis);
                console.log(`✅ Files uploaded successfully`);
            } else {
                throw new Error(data.error || 'Upload failed');
            }
            
        } catch (error) {
            console.error('❌ Upload error:', error);
            this.addMessageToChat('assistant', 
                `File upload failed: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }
    
    // System Monitoring
    initializeSystemMonitoring() {
        this.updateSystemMetrics();
        
        // Update metrics every 30 seconds
        setInterval(() => {
            this.updateSystemMetrics();
        }, 30000);
    }
    
    async updateSystemMetrics() {
        try {
            const response = await fetch('/api/system/metrics');
            const data = await response.json();
            
            if (data.success) {
                this.systemMetrics = data.data;
                this.updateSystemDisplay();
            }
            
        } catch (error) {
            console.error('❌ Failed to update system metrics:', error);
        }
    }
    
    updateSystemDisplay() {
        const metrics = this.systemMetrics;
        
        // Update sidebar status
        const elements = {
            'gpu-status': metrics.gpu || 'RTX 4070 SUPER',
            'vram-status': metrics.vram || '12GB',
            'model-status': metrics.model || 'Gemma 3',
            'chats-status': Object.keys(this.chatHistory).length.toString()
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
        
        // Update chat count badge
        const chatCount = document.getElementById('chat-count');
        if (chatCount) {
            chatCount.textContent = Object.keys(this.chatHistory).length.toString();
        }
        
        console.log('📊 System metrics updated');
    }
    
    // Browser Integration
    initializeBrowser() {
        const navigateBtn = document.getElementById('navigate-btn');
        const urlInput = document.getElementById('browser-url');
        const browserFrame = document.getElementById('browser-frame');
        
        if (navigateBtn && urlInput && browserFrame) {
            navigateBtn.addEventListener('click', () => {
                const url = urlInput.value.trim();
                if (url) {
                    this.navigateBrowser(url);
                }
            });
            
            urlInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    const url = urlInput.value.trim();
                    if (url) {
                        this.navigateBrowser(url);
                    }
                }
            });
        }
    }
    
    navigateBrowser(url) {
        const browserFrame = document.getElementById('browser-frame');
        if (!browserFrame) return;
        
        // Ensure URL has protocol
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }
        
        console.log(`🌐 Navigating to: ${url}`);
        
        try {
            browserFrame.src = url;
        } catch (error) {
            console.error('❌ Navigation error:', error);
            alert('Failed to navigate to URL. Some sites may not allow embedding.');
        }
    }
    
    // Communication Setup
    initializeCommunication() {
        const commBtns = document.querySelectorAll('.comm-btn');
        
        commBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const card = btn.closest('.comm-card');
                const title = card.querySelector('h3').textContent;
                
                this.setupCommunication(title);
            });
        });
    }
    
    setupCommunication(type) {
        console.log(`📧 Setting up ${type}...`);
        
        // Switch to chat and send setup message
        this.switchSection('chat');
        this.sendMessage(`Help me set up ${type} integration`);
    }
    
    // Settings Management
    initializeSettings() {
        const settingInputs = document.querySelectorAll('#settings-section input, #settings-section select');
        
        settingInputs.forEach(input => {
            input.addEventListener('change', () => {
                this.updateSetting(input.id, input.value, input.type);
            });
        });
        
        // Load current settings
        this.loadSettings();
    }
    
    loadSettings() {
        // Set default values based on system configuration
        const settings = {
            'model-path': 'D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf',
            'gpu-layers': '35',
            'context-window': '4096',
            'data-dir': 'D:/JUGGERNAUT_DATA',
            'auto-save': true,
            'backup-freq': 'daily'
        };
        
        Object.entries(settings).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = value;
                } else {
                    element.value = value;
                }
            }
        });
    }
    
    updateSetting(settingId, value, type) {
        console.log(`⚙️ Updated setting ${settingId}: ${value}`);
        
        // Here you would typically save to backend
        // For now, just log the change
        
        if (settingId === 'gpu-layers' || settingId === 'context-window') {
            // These would require model restart
            console.log('🔄 Model restart required for this setting');
        }
    }
    
    // Chat History Management
    async loadChatHistory() {
        try {
            const response = await fetch(`/api/chat/history?chat_id=${this.currentChatId}`);
            const data = await response.json();
            
            if (data.success && data.history) {
                this.chatHistory[this.currentChatId] = data.history.map(msg => ({
                    type: msg.type,
                    content: msg.message,
                    timestamp: new Date(msg.timestamp).getTime(),
                    metadata: msg.metadata
                }));
                
                this.loadChatMessages(this.currentChatId);
                console.log(`📚 Loaded chat history for ${this.currentChatId}`);
            }
            
        } catch (error) {
            console.error('❌ Failed to load chat history:', error);
        }
    }
    
    // Utility Methods
    formatTime(timestamp) {
        return new Date(timestamp).toLocaleTimeString();
    }
    
    formatFileSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Bytes';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '10000',
            opacity: '0',
            transform: 'translateY(-20px)',
            transition: 'all 0.3s ease'
        });
        
        // Set background color based on type
        const colors = {
            info: '#3b82f6',
            success: '#10b981',
            warning: '#f59e0b',
            error: '#ef4444'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.juggernautAI = new JuggernautAI();
});

// Global error handler
window.addEventListener('error', (e) => {
    console.error('🚨 Global error:', e.error);
});

// Service worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('📱 SW registered:', registration);
            })
            .catch(registrationError => {
                console.log('❌ SW registration failed:', registrationError);
            });
    });
}


    
    // Processing Indicator Functions (Non-blocking)
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
                            <button class="cancel-btn" onclick="juggernautAI.cancelCurrentRequest()">
                                ❌ Cancel
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            const chatMessages = document.getElementById('chat-messages');
            if (chatMessages) {
                chatMessages.appendChild(processingMsg);
            }
        }
        
        // Animate processing dots
        this.animateProcessingDots();
        
        // Scroll to bottom
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
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
        // Keep interface fully responsive - don't disable anything
        console.log(loading ? '⏳ Processing...' : '✅ Ready');
    }
}



// Add enhanced styles for non-blocking interface
const enhancedStyles = document.createElement('style');
enhancedStyles.textContent = `
/* Processing Indicator Styles */
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
`;

// Inject styles when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        document.head.appendChild(enhancedStyles);
    });
} else {
    document.head.appendChild(enhancedStyles);
}

// Initialize the enhanced Juggernaut AI
window.juggernautAI = new JuggernautAI();

console.log('🚀 Enhanced Non-blocking Juggernaut AI Interface Loaded!');
console.log('✅ You can now send messages while processing');
console.log('✅ Cancel button available during processing');
console.log('✅ Interface stays responsive');

