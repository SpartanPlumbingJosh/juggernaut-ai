// Juggernaut AI - Frontend JavaScript

class JuggernautAI {
    constructor() {
        this.currentChatId = 'chat_1';
        this.chatTabs = new Map();
        this.currentView = 'chat';
        this.isConnected = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeChatTab('chat_1');
        this.checkSystemStatus();
        this.setupAutoResize();
    }

    setupEventListeners() {
        // Sidebar toggle
        const sidebarToggle = document.getElementById('sidebarToggle');
        const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
        
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        }
        
        if (mobileSidebarToggle) {
            mobileSidebarToggle.addEventListener('click', () => this.toggleMobileSidebar());
        }

        // Sidebar section toggles
        document.querySelectorAll('.section-title').forEach(title => {
            title.addEventListener('click', (e) => this.toggleSection(e.target));
        });

        // Sidebar item clicks
        document.querySelectorAll('.sidebar-item').forEach(item => {
            item.addEventListener('click', (e) => this.handleSidebarAction(e.target));
        });

        // Chat functionality
        const sendBtn = document.getElementById('sendBtn');
        const chatInput = document.getElementById('chatInput');
        
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (chatInput) {
            chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        // Chat tabs
        const newTabBtn = document.getElementById('newTabBtn');
        if (newTabBtn) {
            newTabBtn.addEventListener('click', () => this.createNewChatTab());
        }

        // File upload
        const fileInput = document.getElementById('fileInput');
        const uploadZone = document.getElementById('uploadZone');
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileUpload(e.target.files));
        }
        
        if (uploadZone) {
            uploadZone.addEventListener('dragover', (e) => this.handleDragOver(e));
            uploadZone.addEventListener('drop', (e) => this.handleFileDrop(e));
            uploadZone.addEventListener('click', () => fileInput?.click());
        }

        // Browser controls
        const navigateBtn = document.getElementById('navigateBtn');
        const screenshotBtn = document.getElementById('screenshotBtn');
        const scrollDownBtn = document.getElementById('scrollDownBtn');
        const scrollUpBtn = document.getElementById('scrollUpBtn');
        
        if (navigateBtn) {
            navigateBtn.addEventListener('click', () => this.handleBrowserCommand('navigate'));
        }
        if (screenshotBtn) {
            screenshotBtn.addEventListener('click', () => this.handleBrowserCommand('screenshot'));
        }
        if (scrollDownBtn) {
            scrollDownBtn.addEventListener('click', () => this.handleBrowserCommand('scroll_down'));
        }
        if (scrollUpBtn) {
            scrollUpBtn.addEventListener('click', () => this.handleBrowserCommand('scroll_up'));
        }

        // Security modal
        const confirmSecurity = document.getElementById('confirmSecurity');
        const cancelSecurity = document.getElementById('cancelSecurity');
        
        if (confirmSecurity) {
            confirmSecurity.addEventListener('click', () => this.confirmSecurity());
        }
        if (cancelSecurity) {
            cancelSecurity.addEventListener('click', () => this.cancelSecurity());
        }
    }

    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.toggle('collapsed');
        }
    }

    toggleMobileSidebar() {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.toggle('open');
        }
    }

    toggleSection(titleElement) {
        const section = titleElement.closest('.sidebar-section');
        const content = section.querySelector('.section-content');
        const icon = titleElement.querySelector('.toggle-icon');
        
        if (content && icon) {
            content.classList.toggle('collapsed');
            titleElement.classList.toggle('collapsed');
        }
    }

    handleSidebarAction(element) {
        // Remove active class from all items
        document.querySelectorAll('.sidebar-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active class to clicked item
        element.classList.add('active');
        
        const action = element.getAttribute('data-action');
        
        switch (action) {
            case 'new-chat':
                this.createNewChatTab();
                this.showView('chat');
                break;
            case 'file-upload':
                this.showView('upload');
                break;
            case 'image-gen':
                this.showImageGeneration();
                break;
            case 'browser-control':
                this.showView('browser');
                break;
            case 'system-status':
                this.showView('status');
                this.updateSystemStatus();
                break;
            case 'chat-history':
                this.showChatHistory();
                break;
            case 'file-manager':
                this.showFileManager();
                break;
            case 'settings':
                this.showSettings();
                break;
        }
    }

    showView(viewName) {
        // Hide all views
        const views = ['chatContainer', 'uploadArea', 'browserPanel', 'statusPanel'];
        views.forEach(viewId => {
            const element = document.getElementById(viewId);
            if (element) {
                element.style.display = 'none';
            }
        });

        // Show selected view
        const targetView = document.getElementById(viewName === 'chat' ? 'chatContainer' : 
                                                 viewName === 'upload' ? 'uploadArea' :
                                                 viewName === 'browser' ? 'browserPanel' :
                                                 viewName === 'status' ? 'statusPanel' : 'chatContainer');
        
        if (targetView) {
            targetView.style.display = 'flex';
        }
        
        this.currentView = viewName;
    }

    async sendMessage() {
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');
        
        if (!chatInput || !chatInput.value.trim()) return;
        
        const message = chatInput.value.trim();
        chatInput.value = '';
        sendBtn.disabled = true;
        
        // Add user message to chat
        this.addMessageToChat('user', message);
        
        try {
            const response = await fetch('/api/chat/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    chat_id: this.currentChatId,
                    user: 'Josh'
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessageToChat('ai', data.response);
            } else {
                this.addMessageToChat('ai', 'Sorry, I encountered an error processing your message.');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessageToChat('ai', 'Connection error. Please check if the server is running.');
        } finally {
            sendBtn.disabled = false;
            chatInput.focus();
        }
    }

    addMessageToChat(role, content) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        // Remove welcome message if it exists
        const welcomeMessage = chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();
        
        messageContent.appendChild(messageTime);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    initializeChatTab(chatId) {
        this.chatTabs.set(chatId, {
            id: chatId,
            messages: []
        });
        
        // Update tab display
        this.updateChatTabs();
    }

    createNewChatTab() {
        const newChatId = `chat_${Date.now()}`;
        this.initializeChatTab(newChatId);
        this.switchToChat(newChatId);
    }

    switchToChat(chatId) {
        this.currentChatId = chatId;
        
        // Update active tab
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
            if (tab.getAttribute('data-chat-id') === chatId) {
                tab.classList.add('active');
            }
        });
        
        // Load chat messages
        this.loadChatMessages(chatId);
    }

    async loadChatMessages(chatId) {
        try {
            const response = await fetch(`/api/chat/${chatId}`);
            const data = await response.json();
            
            const chatMessages = document.getElementById('chatMessages');
            if (chatMessages) {
                chatMessages.innerHTML = '';
                
                if (data.length === 0) {
                    chatMessages.innerHTML = `
                        <div class="welcome-message">
                            <i class="fas fa-robot"></i>
                            <h3>Welcome to Juggernaut AI</h3>
                            <p>Your powerful AI assistant is ready to help. Start a conversation or use the sidebar to access various features.</p>
                        </div>
                    `;
                } else {
                    data.forEach(msg => {
                        this.addMessageToChat(msg.role === 'Josh' ? 'user' : 'ai', msg.content);
                    });
                }
            }
        } catch (error) {
            console.error('Error loading chat messages:', error);
        }
    }

    updateChatTabs() {
        const chatTabs = document.getElementById('chatTabs');
        if (!chatTabs) return;
        
        // Clear existing tabs except new tab button
        const newTabBtn = chatTabs.querySelector('.new-tab-btn');
        chatTabs.innerHTML = '';
        
        // Add tabs
        this.chatTabs.forEach((chat, chatId) => {
            const tab = document.createElement('div');
            tab.className = `tab ${chatId === this.currentChatId ? 'active' : ''}`;
            tab.setAttribute('data-chat-id', chatId);
            
            tab.innerHTML = `
                <span>${chatId.replace('_', ' ').toUpperCase()}</span>
                <button class="tab-close"><i class="fas fa-times"></i></button>
            `;
            
            tab.addEventListener('click', (e) => {
                if (!e.target.closest('.tab-close')) {
                    this.switchToChat(chatId);
                }
            });
            
            const closeBtn = tab.querySelector('.tab-close');
            closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.closeChatTab(chatId);
            });
            
            chatTabs.appendChild(tab);
        });
        
        // Re-add new tab button
        if (newTabBtn) {
            chatTabs.appendChild(newTabBtn);
        }
    }

    closeChatTab(chatId) {
        if (this.chatTabs.size <= 1) return; // Don't close last tab
        
        this.chatTabs.delete(chatId);
        
        if (this.currentChatId === chatId) {
            // Switch to first available tab
            const firstChatId = this.chatTabs.keys().next().value;
            this.switchToChat(firstChatId);
        }
        
        this.updateChatTabs();
    }

    async handleFileUpload(files) {
        const fileList = document.getElementById('fileList');
        if (!fileList) return;
        
        for (const file of files) {
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch('/api/files/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.addFileToList(file.name, data.filename);
                } else {
                    console.error('Upload failed:', data.error);
                }
            } catch (error) {
                console.error('Upload error:', error);
            }
        }
    }

    addFileToList(originalName, filename) {
        const fileList = document.getElementById('fileList');
        if (!fileList) return;
        
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <span><i class="fas fa-file"></i> ${originalName}</span>
            <button onclick="app.analyzeFile('${filename}')" class="control-btn">
                <i class="fas fa-search"></i> Analyze
            </button>
        `;
        
        fileList.appendChild(fileItem);
    }

    async analyzeFile(filename) {
        try {
            const response = await fetch('/api/files/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ filename })
            });
            
            const data = await response.json();
            this.addMessageToChat('ai', `File Analysis Result: ${data.result}`);
            this.showView('chat');
        } catch (error) {
            console.error('Analysis error:', error);
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        e.target.closest('.upload-zone').classList.add('dragover');
    }

    handleFileDrop(e) {
        e.preventDefault();
        e.target.closest('.upload-zone').classList.remove('dragover');
        this.handleFileUpload(e.dataTransfer.files);
    }

    async handleBrowserCommand(command) {
        const urlInput = document.getElementById('urlInput');
        const browserOutput = document.getElementById('browserOutput');
        
        if (!browserOutput) return;
        
        const url = urlInput ? urlInput.value : '';
        
        try {
            const response = await fetch('/api/browser/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command, url })
            });
            
            const data = await response.json();
            
            browserOutput.innerHTML += `
                <div style="margin-bottom: 10px;">
                    <strong>[${new Date().toLocaleTimeString()}] ${command.toUpperCase()}:</strong><br>
                    ${data.result}
                </div>
            `;
            
            browserOutput.scrollTop = browserOutput.scrollHeight;
        } catch (error) {
            console.error('Browser command error:', error);
            browserOutput.innerHTML += `
                <div style="margin-bottom: 10px; color: var(--accent-danger);">
                    <strong>[${new Date().toLocaleTimeString()}] ERROR:</strong><br>
                    ${error.message}
                </div>
            `;
        }
    }

    async checkSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            this.updateStatusIndicator(data.system_ready);
            this.isConnected = data.system_ready;
            
        } catch (error) {
            console.error('Status check error:', error);
            this.updateStatusIndicator(false);
            this.isConnected = false;
        }
    }

    updateStatusIndicator(isReady) {
        const statusIndicator = document.getElementById('statusIndicator');
        if (!statusIndicator) return;
        
        const icon = statusIndicator.querySelector('i');
        const text = statusIndicator.querySelector('span');
        
        if (isReady) {
            icon.style.color = 'var(--accent-primary)';
            text.textContent = 'Connected';
        } else {
            icon.style.color = 'var(--accent-danger)';
            text.textContent = 'Disconnected';
        }
    }

    async updateSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            const aiStatus = document.getElementById('aiStatus');
            const browserStatus = document.getElementById('browserStatus');
            const systemStatus = document.getElementById('systemStatus');
            
            if (aiStatus) {
                aiStatus.textContent = data.ai_ready ? 'Ready' : 'Not Ready';
                aiStatus.className = `status-value ${data.ai_ready ? '' : 'error'}`;
            }
            
            if (browserStatus) {
                browserStatus.textContent = data.browser_ready ? 'Ready' : 'Not Ready';
                browserStatus.className = `status-value ${data.browser_ready ? '' : 'error'}`;
            }
            
            if (systemStatus) {
                systemStatus.textContent = data.system_ready ? 'Online' : 'Offline';
                systemStatus.className = `status-value ${data.system_ready ? '' : 'error'}`;
            }
            
        } catch (error) {
            console.error('Status update error:', error);
        }
    }

    showImageGeneration() {
        const prompt = window.prompt('Enter image generation prompt:');
        if (prompt) {
            this.generateImage(prompt);
        }
    }

    async generateImage(prompt) {
        try {
            const response = await fetch('/api/plugins/generate_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt })
            });
            
            const data = await response.json();
            this.addMessageToChat('ai', `Image generated: ${data.image_url}`);
            this.showView('chat');
        } catch (error) {
            console.error('Image generation error:', error);
        }
    }

    showChatHistory() {
        // Implementation for chat history view
        this.addMessageToChat('ai', 'Chat history feature coming soon!');
        this.showView('chat');
    }

    showFileManager() {
        // Implementation for file manager view
        this.addMessageToChat('ai', 'File manager feature coming soon!');
        this.showView('chat');
    }

    showSettings() {
        // Implementation for settings view
        this.addMessageToChat('ai', 'Settings panel coming soon!');
        this.showView('chat');
    }

    showSecurityModal() {
        const modal = document.getElementById('securityModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    confirmSecurity() {
        const securityCode = document.getElementById('securityCode');
        const modal = document.getElementById('securityModal');
        
        if (securityCode && securityCode.value === '1234') {
            modal.style.display = 'none';
            // Proceed with secure operation
        } else {
            alert('Invalid security code!');
        }
    }

    cancelSecurity() {
        const modal = document.getElementById('securityModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    setupAutoResize() {
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            });
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new JuggernautAI();
    
    // Check status periodically
    setInterval(() => {
        window.app.checkSystemStatus();
    }, 30000); // Every 30 seconds
});

// Global functions for inline event handlers
function analyzeFile(filename) {
    if (window.app) {
        window.app.analyzeFile(filename);
    }
}

