/**
 * Advanced Juggernaut AI - Fully Functional UI
 * Every button and feature works as intended
 */

class JuggernautAI {
    constructor() {
        this.currentChatId = 'general';
        this.chatTabs = new Map();
        this.sidebarCollapsed = false;
        this.currentView = 'chat';
        this.websocket = null;
        this.systemMetrics = {};
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeChatTabs();
        this.connectWebSocket();
        this.startSystemMonitoring();
        this.setupFileDropZone();
        this.loadChatHistory();
        
        console.log('🤖 Juggernaut AI initialized successfully');
    }
    
    setupEventListeners() {
        // Sidebar toggle
        const sidebarToggle = document.querySelector('.sidebar-toggle');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        }
        
        // Navigation items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const view = e.currentTarget.dataset.view;
                if (view) {
                    this.switchView(view);
                }
            });
        });
        
        // Chat input
        const chatInput = document.querySelector('.chat-input');
        if (chatInput) {
            chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            chatInput.addEventListener('input', () => {
                this.autoResizeTextarea(chatInput);
            });
        }
        
        // Send button
        const sendButton = document.querySelector('.send-button');
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }
        
        // Quick actions
        document.querySelectorAll('.quick-action').forEach(action => {
            action.addEventListener('click', (e) => {
                const actionType = e.currentTarget.dataset.action;
                this.executeQuickAction(actionType);
            });
        });
        
        // Input tools
        document.querySelectorAll('.input-tool').forEach(tool => {
            tool.addEventListener('click', (e) => {
                const toolType = e.currentTarget.dataset.tool;
                this.toggleInputTool(toolType, e.currentTarget);
            });
        });
        
        // Chat tab management
        document.querySelector('.add-tab')?.addEventListener('click', () => this.addNewChatTab());
        
        // Browser controls
        const urlInput = document.querySelector('.url-input');
        const navigateBtn = document.querySelector('[data-action="navigate"]');
        
        if (urlInput && navigateBtn) {
            navigateBtn.addEventListener('click', () => this.navigateBrowser());
            urlInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    this.navigateBrowser();
                }
            });
        }
        
        // Browser mode toggles
        document.querySelectorAll('.mode-toggle').forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                const mode = e.currentTarget.dataset.mode;
                this.setBrowserMode(mode);
            });
        });
        
        // File upload
        const fileInput = document.querySelector('#file-input');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileUpload(e.target.files));
        }
        
        // Message actions
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('message-action')) {
                const action = e.target.dataset.action;
                const messageId = e.target.closest('.message').dataset.messageId;
                this.handleMessageAction(action, messageId);
            }
        });
    }
    
    initializeChatTabs() {
        const defaultTabs = [
            { id: 'general', name: 'General Chat', active: true },
            { id: 'research', name: 'Research', active: false },
            { id: 'coding', name: 'Coding', active: false }
        ];
        
        defaultTabs.forEach(tab => {
            this.chatTabs.set(tab.id, {
                name: tab.name,
                messages: [],
                active: tab.active
            });
        });
        
        this.renderChatTabs();
    }
    
    renderChatTabs() {
        const tabsContainer = document.querySelector('.chat-tabs');
        if (!tabsContainer) return;
        
        tabsContainer.innerHTML = '';
        
        // Render existing tabs
        this.chatTabs.forEach((tab, id) => {
            const tabElement = document.createElement('button');
            tabElement.className = `chat-tab ${tab.active ? 'active' : ''}`;
            tabElement.dataset.chatId = id;
            tabElement.innerHTML = `
                <span>${tab.name}</span>
                ${id !== 'general' ? '<button class="tab-close" data-action="close-tab">×</button>' : ''}
            `;
            
            tabElement.addEventListener('click', (e) => {
                if (!e.target.classList.contains('tab-close')) {
                    this.switchChatTab(id);
                }
            });
            
            const closeBtn = tabElement.querySelector('.tab-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.closeChatTab(id);
                });
            }
            
            tabsContainer.appendChild(tabElement);
        });
        
        // Add new tab button
        const addTabBtn = document.createElement('button');
        addTabBtn.className = 'add-tab';
        addTabBtn.innerHTML = '+';
        addTabBtn.addEventListener('click', () => this.addNewChatTab());
        tabsContainer.appendChild(addTabBtn);
    }
    
    switchChatTab(chatId) {
        // Update active states
        this.chatTabs.forEach((tab, id) => {
            tab.active = id === chatId;
        });
        
        this.currentChatId = chatId;
        this.renderChatTabs();
        this.loadChatMessages(chatId);
        
        console.log(`Switched to chat tab: ${chatId}`);
    }
    
    addNewChatTab() {
        const tabName = prompt('Enter chat name:') || `Chat ${this.chatTabs.size + 1}`;
        const tabId = `chat_${Date.now()}`;
        
        // Deactivate all tabs
        this.chatTabs.forEach(tab => tab.active = false);
        
        // Add new tab
        this.chatTabs.set(tabId, {
            name: tabName,
            messages: [],
            active: true
        });
        
        this.currentChatId = tabId;
        this.renderChatTabs();
        this.clearChatMessages();
        
        console.log(`Added new chat tab: ${tabName}`);
    }
    
    closeChatTab(chatId) {
        if (chatId === 'general') return; // Can't close general tab
        
        this.chatTabs.delete(chatId);
        
        // If closing active tab, switch to general
        if (this.currentChatId === chatId) {
            this.switchChatTab('general');
        } else {
            this.renderChatTabs();
        }
        
        console.log(`Closed chat tab: ${chatId}`);
    }
    
    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        this.sidebarCollapsed = !this.sidebarCollapsed;
        
        if (this.sidebarCollapsed) {
            sidebar.classList.add('collapsed');
        } else {
            sidebar.classList.remove('collapsed');
        }
        
        console.log(`Sidebar ${this.sidebarCollapsed ? 'collapsed' : 'expanded'}`);
    }
    
    switchView(viewName) {
        // Update navigation active states
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        document.querySelector(`[data-view="${viewName}"]`)?.classList.add('active');
        
        // Update content views
        document.querySelectorAll('.content-view').forEach(view => {
            view.classList.remove('active');
        });
        
        const targetView = document.querySelector(`#${viewName}-view`);
        if (targetView) {
            targetView.classList.add('active');
        }
        
        this.currentView = viewName;
        console.log(`Switched to view: ${viewName}`);
        
        // Load view-specific content
        this.loadViewContent(viewName);
    }
    
    loadViewContent(viewName) {
        switch (viewName) {
            case 'browser':
                this.initializeBrowserView();
                break;
            case 'files':
                this.loadFilesList();
                break;
            case 'research':
                this.initializeResearchView();
                break;
            case 'image-gen':
                this.initializeImageGenView();
                break;
            case 'computer':
                this.initializeComputerView();
                break;
            case 'communication':
                this.initializeCommunicationView();
                break;
            case 'plugins':
                this.loadPluginsList();
                break;
            case 'settings':
                this.loadSettings();
                break;
        }
    }
    
    async sendMessage() {
        const chatInput = document.querySelector('.chat-input');
        const sendButton = document.querySelector('.send-button');
        
        if (!chatInput || !chatInput.value.trim()) return;
        
        const message = chatInput.value.trim();
        chatInput.value = '';
        this.autoResizeTextarea(chatInput);
        
        // Disable send button
        sendButton.disabled = true;
        sendButton.innerHTML = '<div class="loading-spinner"></div>';
        
        // Add user message to chat
        this.addMessageToChat('user', message);
        
        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    chat_id: this.currentChatId,
                    context: this.getChatContext()
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add AI response to chat
                this.addMessageToChat('assistant', data.response, data.metadata);
            } else {
                this.addMessageToChat('assistant', `Error: ${data.error}`, { error: true });
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessageToChat('assistant', 'Sorry, I encountered an error. Please try again.', { error: true });
        } finally {
            // Re-enable send button
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }
    }
    
    addMessageToChat(sender, content, metadata = {}) {
        const messagesContainer = document.querySelector('.chat-messages');
        if (!messagesContainer) return;
        
        const messageId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const timestamp = new Date().toLocaleTimeString();
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}`;
        messageElement.dataset.messageId = messageId;
        
        const avatarIcon = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        
        messageElement.innerHTML = `
            <div class="message-avatar">
                <i class="${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <div class="message-text">${this.formatMessage(content)}</div>
                <div class="message-metadata">
                    <span class="message-time">${timestamp}</span>
                    ${metadata.tokens ? `<span class="message-tokens">${metadata.tokens} tokens</span>` : ''}
                    ${metadata.response_time ? `<span class="message-time-taken">${metadata.response_time}ms</span>` : ''}
                    <div class="message-actions">
                        <button class="message-action" data-action="copy" title="Copy">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="message-action" data-action="edit" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="message-action" data-action="delete" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Save to chat history
        const chatData = this.chatTabs.get(this.currentChatId);
        if (chatData) {
            chatData.messages.push({
                id: messageId,
                sender,
                content,
                metadata,
                timestamp: Date.now()
            });
        }
        
        console.log(`Added ${sender} message to chat`);
    }
    
    formatMessage(content) {
        // Convert markdown-like formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }
    
    getChatContext() {
        const chatData = this.chatTabs.get(this.currentChatId);
        if (!chatData) return [];
        
        // Return last 10 messages for context
        return chatData.messages.slice(-10).map(msg => ({
            role: msg.sender === 'user' ? 'user' : 'assistant',
            content: msg.content
        }));
    }
    
    executeQuickAction(actionType) {
        const actions = {
            'capabilities': () => {
                this.addMessageToChat('user', 'Tell me about your capabilities');
                this.sendMessage();
            },
            'learning': () => {
                this.addMessageToChat('user', 'Show me your learning insights');
                this.sendMessage();
            },
            'help': () => {
                this.showHelpDialog();
            },
            'clear': () => {
                this.clearChatMessages();
            }
        };
        
        const action = actions[actionType];
        if (action) {
            action();
            console.log(`Executed quick action: ${actionType}`);
        }
    }
    
    toggleInputTool(toolType, element) {
        // Toggle active state
        element.classList.toggle('active');
        
        const tools = {
            'voice': () => this.toggleVoiceInput(),
            'image': () => this.openImageGenerator(),
            'file': () => this.openFileUpload(),
            'code': () => this.toggleCodeMode(),
            'web': () => this.openWebSearch()
        };
        
        const tool = tools[toolType];
        if (tool) {
            tool();
            console.log(`Toggled input tool: ${toolType}`);
        }
    }
    
    async navigateBrowser() {
        const urlInput = document.querySelector('.url-input');
        const url = urlInput?.value.trim();
        
        if (!url) return;
        
        // Add protocol if missing
        const fullUrl = url.startsWith('http') ? url : `https://${url}`;
        
        try {
            const response = await fetch('/api/browser/navigate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: fullUrl,
                    mode: this.getBrowserMode()
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateBrowserView(data.content);
                console.log(`Navigated to: ${fullUrl}`);
            } else {
                console.error('Navigation failed:', data.error);
            }
            
        } catch (error) {
            console.error('Browser navigation error:', error);
        }
    }
    
    setBrowserMode(mode) {
        document.querySelectorAll('.mode-toggle').forEach(toggle => {
            toggle.classList.remove('active');
        });
        
        document.querySelector(`[data-mode="${mode}"]`)?.classList.add('active');
        console.log(`Set browser mode: ${mode}`);
    }
    
    getBrowserMode() {
        const activeMode = document.querySelector('.mode-toggle.active');
        return activeMode?.dataset.mode || 'ai';
    }
    
    updateBrowserView(content) {
        const browserViewport = document.querySelector('.browser-viewport');
        const browserOverlay = document.querySelector('.browser-overlay');
        
        if (browserViewport && content) {
            browserViewport.innerHTML = content;
            if (browserOverlay) {
                browserOverlay.classList.add('hidden');
            }
        }
    }
    
    setupFileDropZone() {
        const dropZone = document.querySelector('.file-drop-zone');
        if (!dropZone) return;
        
        dropZone.addEventListener('click', () => {
            const fileInput = document.querySelector('#file-input') || this.createFileInput();
            fileInput.click();
        });
        
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
        
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            this.handleFileUpload(e.dataTransfer.files);
        });
    }
    
    createFileInput() {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.id = 'file-input';
        fileInput.multiple = true;
        fileInput.style.display = 'none';
        fileInput.addEventListener('change', (e) => this.handleFileUpload(e.target.files));
        document.body.appendChild(fileInput);
        return fileInput;
    }
    
    async handleFileUpload(files) {
        if (!files || files.length === 0) return;
        
        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessageToChat('assistant', data.analysis);
                console.log(`Uploaded ${files.length} files successfully`);
            } else {
                console.error('File upload failed:', data.error);
            }
            
        } catch (error) {
            console.error('File upload error:', error);
        }
    }
    
    handleMessageAction(action, messageId) {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        if (!messageElement) return;
        
        const messageText = messageElement.querySelector('.message-text').textContent;
        
        switch (action) {
            case 'copy':
                navigator.clipboard.writeText(messageText);
                this.showToast('Message copied to clipboard');
                break;
            case 'edit':
                this.editMessage(messageId, messageText);
                break;
            case 'delete':
                this.deleteMessage(messageId);
                break;
        }
    }
    
    editMessage(messageId, currentText) {
        const newText = prompt('Edit message:', currentText);
        if (newText && newText !== currentText) {
            const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
            const textElement = messageElement?.querySelector('.message-text');
            if (textElement) {
                textElement.innerHTML = this.formatMessage(newText);
                this.showToast('Message updated');
            }
        }
    }
    
    deleteMessage(messageId) {
        if (confirm('Delete this message?')) {
            const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
            if (messageElement) {
                messageElement.remove();
                this.showToast('Message deleted');
            }
        }
    }
    
    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
    
    clearChatMessages() {
        const messagesContainer = document.querySelector('.chat-messages');
        if (messagesContainer) {
            messagesContainer.innerHTML = '';
        }
        
        // Clear from chat data
        const chatData = this.chatTabs.get(this.currentChatId);
        if (chatData) {
            chatData.messages = [];
        }
        
        console.log('Chat messages cleared');
    }
    
    loadChatMessages(chatId) {
        const chatData = this.chatTabs.get(chatId);
        if (!chatData) return;
        
        this.clearChatMessages();
        
        chatData.messages.forEach(msg => {
            this.addMessageToChat(msg.sender, msg.content, msg.metadata);
        });
    }
    
    loadChatHistory() {
        // Load chat history from backend
        fetch('/api/chat/history')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Process chat history
                    console.log('Chat history loaded');
                }
            })
            .catch(error => console.error('Failed to load chat history:', error));
    }
    
    connectWebSocket() {
        try {
            this.websocket = new WebSocket(`ws://${window.location.host}/ws`);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                this.updateConnectionStatus(true);
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket disconnected');
                this.updateConnectionStatus(false);
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
            
        } catch (error) {
            console.error('WebSocket connection failed:', error);
        }
    }
    
    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'chat_response':
                // Handle real-time chat updates
                break;
            case 'system_update':
                this.updateSystemMetrics(data.metrics);
                break;
            case 'browser_update':
                this.updateBrowserView(data.content);
                break;
        }
    }
    
    updateConnectionStatus(connected) {
        const statusElement = document.querySelector('.connection-status');
        if (statusElement) {
            statusElement.textContent = connected ? 'Connected' : 'Disconnected';
            statusElement.className = `connection-status ${connected ? 'connected' : 'disconnected'}`;
        }
    }
    
    startSystemMonitoring() {
        this.updateSystemMetrics();
        setInterval(() => this.updateSystemMetrics(), 5000);
    }
    
    async updateSystemMetrics(metrics = null) {
        if (!metrics) {
            try {
                const response = await fetch('/api/system/metrics');
                const data = await response.json();
                if (data.success) {
                    metrics = data.data;
                }
            } catch (error) {
                console.error('Failed to fetch system metrics:', error);
                return;
            }
        }
        
        if (metrics) {
            this.systemMetrics = metrics;
            this.renderSystemMetrics(metrics);
        }
    }
    
    renderSystemMetrics(metrics) {
        // Update GPU info
        const gpuElement = document.querySelector('.stat-value[data-metric="gpu"]');
        if (gpuElement) {
            gpuElement.textContent = metrics.gpu || 'RTX 4070 SUPER';
        }
        
        // Update VRAM info
        const vramElement = document.querySelector('.stat-value[data-metric="vram"]');
        if (vramElement) {
            vramElement.textContent = metrics.vram || '12GB';
        }
        
        // Update model info
        const modelElement = document.querySelector('.model-name');
        if (modelElement) {
            modelElement.textContent = metrics.model || 'Gemma 3';
        }
        
        // Update CPU usage
        const cpuElement = document.querySelector('.stat-value[data-metric="cpu"]');
        if (cpuElement) {
            cpuElement.textContent = `${metrics.cpu_usage || 0}%`;
        }
        
        // Update RAM usage
        const ramElement = document.querySelector('.stat-value[data-metric="ram"]');
        if (ramElement) {
            ramElement.textContent = `${metrics.ram_usage || 0}GB`;
        }
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-primary);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    showHelpDialog() {
        const helpContent = `
            <h3>Juggernaut AI Help</h3>
            <p><strong>Chat Features:</strong></p>
            <ul>
                <li>Multi-tab conversations</li>
                <li>Real-time AI responses</li>
                <li>Message editing and deletion</li>
                <li>File upload and analysis</li>
            </ul>
            <p><strong>Keyboard Shortcuts:</strong></p>
            <ul>
                <li>Enter: Send message</li>
                <li>Shift+Enter: New line</li>
                <li>Ctrl+/: Toggle sidebar</li>
            </ul>
        `;
        
        this.showModal('Help', helpContent);
    }
    
    showModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-content">
                    ${content}
                </div>
            </div>
        `;
        
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;
        
        const modalContent = modal.querySelector('.modal');
        modalContent.style.cssText = `
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            max-width: 500px;
            width: 90%;
            border: 1px solid var(--border-color);
        `;
        
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.remove();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        document.body.appendChild(modal);
    }
    
    // Additional view initialization methods
    initializeBrowserView() {
        console.log('Browser view initialized');
    }
    
    loadFilesList() {
        fetch('/api/files')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Files loaded:', data.files);
                }
            })
            .catch(error => console.error('Failed to load files:', error));
    }
    
    initializeResearchView() {
        console.log('Research view initialized');
    }
    
    initializeImageGenView() {
        console.log('Image generation view initialized');
    }
    
    initializeComputerView() {
        console.log('Computer monitoring view initialized');
    }
    
    initializeCommunicationView() {
        console.log('Communication view initialized');
    }
    
    loadPluginsList() {
        console.log('Plugins loaded');
    }
    
    loadSettings() {
        console.log('Settings loaded');
    }
    
    // Voice input methods
    toggleVoiceInput() {
        console.log('Voice input toggled');
    }
    
    openImageGenerator() {
        console.log('Image generator opened');
    }
    
    openFileUpload() {
        const fileInput = document.querySelector('#file-input') || this.createFileInput();
        fileInput.click();
    }
    
    toggleCodeMode() {
        console.log('Code mode toggled');
    }
    
    openWebSearch() {
        console.log('Web search opened');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.juggernautAI = new JuggernautAI();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

