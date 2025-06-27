/**
 * Advanced Juggernaut AI - Complete JavaScript Implementation
 * Features: Retractable sidebar, multiple chat tabs, real-time browser, file drop, etc.
 */

class JuggernautAI {
    constructor() {
        this.currentTab = 'chat';
        this.currentChatTab = 'default';
        this.chatTabs = new Map();
        this.sidebarCollapsed = false;
        this.browserMode = 'ai';
        this.isConnected = false;
        this.messageHistory = new Map();
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeChatTabs();
        this.setupFileDropZone();
        this.connectWebSocket();
        this.startSystemMonitoring();
        this.loadSavedState();
    }
    
    setupEventListeners() {
        // Sidebar toggle
        document.getElementById('sidebarToggle').addEventListener('click', () => {
            this.toggleSidebar();
        });
        
        document.getElementById('mobileSidebarToggle').addEventListener('click', () => {
            this.toggleMobileSidebar();
        });
        
        // Navigation items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                if (tab) {
                    this.switchTab(tab);
                }
            });
        });
        
        // Chat input
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        messageInput.addEventListener('input', () => {
            this.autoResizeTextarea(messageInput);
        });
        
        sendBtn.addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Chat tabs
        document.querySelector('.new-chat-tab').addEventListener('click', () => {
            this.createNewChatTab();
        });
        
        // Browser controls
        document.getElementById('goBtn').addEventListener('click', () => {
            this.navigateBrowser();
        });
        
        document.getElementById('urlInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.navigateBrowser();
            }
        });
        
        document.getElementById('expandBrowser').addEventListener('click', () => {
            this.expandBrowserView();
        });
        
        document.getElementById('closeBrowserOverlay').addEventListener('click', () => {
            this.closeBrowserOverlay();
        });
        
        // Browser mode switching
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mode = e.currentTarget.dataset.mode;
                this.switchBrowserMode(mode);
            });
        });
        
        // File upload
        document.getElementById('attachFile').addEventListener('click', () => {
            document.getElementById('hiddenFileInput').click();
        });
        
        document.getElementById('hiddenFileInput').addEventListener('change', (e) => {
            this.handleFileUpload(e.target.files);
        });
        
        // Tool buttons
        document.getElementById('generateImage').addEventListener('click', () => {
            this.openImageGeneration();
        });
        
        document.getElementById('voiceInput').addEventListener('click', () => {
            this.startVoiceInput();
        });
        
        // Window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Prevent default drag behaviors
        document.addEventListener('dragover', (e) => e.preventDefault());
        document.addEventListener('drop', (e) => e.preventDefault());
    }
    
    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        this.sidebarCollapsed = !this.sidebarCollapsed;
        
        if (this.sidebarCollapsed) {
            sidebar.classList.add('collapsed');
        } else {
            sidebar.classList.remove('collapsed');
        }
        
        this.saveState();
    }
    
    toggleMobileSidebar() {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.toggle('mobile-open');
    }
    
    switchTab(tabName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        // Update breadcrumb
        document.getElementById('currentTab').textContent = this.getTabDisplayName(tabName);
        
        this.currentTab = tabName;
        this.saveState();
        
        // Tab-specific initialization
        if (tabName === 'browser') {
            this.initializeBrowser();
        } else if (tabName === 'files') {
            this.loadFiles();
        } else if (tabName === 'computer') {
            this.updateSystemMetrics();
        }
    }
    
    getTabDisplayName(tabName) {
        const names = {
            'chat': 'AI Assistant',
            'browser': 'Browser Control',
            'files': 'File Management',
            'research': 'Research Assistant',
            'image-gen': 'Image Generation',
            'computer': 'Computer Monitoring',
            'communication': 'Communication',
            'plugins': 'Plugins',
            'settings': 'Settings'
        };
        return names[tabName] || tabName;
    }
    
    initializeChatTabs() {
        this.chatTabs.set('default', {
            name: 'General Chat',
            messages: [],
            active: true
        });
        
        this.chatTabs.set('research', {
            name: 'Research',
            messages: [],
            active: false
        });
        
        this.chatTabs.set('coding', {
            name: 'Coding',
            messages: [],
            active: false
        });
        
        this.updateChatTabsUI();
    }
    
    updateChatTabsUI() {
        const chatTabsContainer = document.querySelector('.chat-tabs');
        const existingTabs = chatTabsContainer.querySelectorAll('.chat-tab-item');
        
        // Remove existing tabs except new chat button
        existingTabs.forEach(tab => tab.remove());
        
        // Add tabs
        this.chatTabs.forEach((tab, id) => {
            const tabElement = document.createElement('div');
            tabElement.className = `chat-tab-item ${tab.active ? 'active' : ''}`;
            tabElement.dataset.chat = id;
            
            tabElement.innerHTML = `
                <span>${tab.name}</span>
                <button class="chat-tab-close"><i class="fas fa-times"></i></button>
            `;
            
            tabElement.addEventListener('click', (e) => {
                if (!e.target.closest('.chat-tab-close')) {
                    this.switchChatTab(id);
                }
            });
            
            tabElement.querySelector('.chat-tab-close').addEventListener('click', (e) => {
                e.stopPropagation();
                this.closeChatTab(id);
            });
            
            chatTabsContainer.insertBefore(tabElement, chatTabsContainer.lastElementChild);
        });
    }
    
    switchChatTab(tabId) {
        // Update active states
        this.chatTabs.forEach((tab, id) => {
            tab.active = (id === tabId);
        });
        
        this.currentChatTab = tabId;
        this.updateChatTabsUI();
        this.loadChatMessages(tabId);
        this.saveState();
    }
    
    createNewChatTab() {
        const tabId = `chat_${Date.now()}`;
        const tabName = `Chat ${this.chatTabs.size}`;
        
        // Deactivate all tabs
        this.chatTabs.forEach(tab => {
            tab.active = false;
        });
        
        // Create new tab
        this.chatTabs.set(tabId, {
            name: tabName,
            messages: [],
            active: true
        });
        
        this.currentChatTab = tabId;
        this.updateChatTabsUI();
        this.clearChatMessages();
        this.saveState();
    }
    
    closeChatTab(tabId) {
        if (this.chatTabs.size <= 1) {
            return; // Don't close the last tab
        }
        
        const wasActive = this.chatTabs.get(tabId).active;
        this.chatTabs.delete(tabId);
        
        if (wasActive) {
            // Activate the first available tab
            const firstTab = this.chatTabs.keys().next().value;
            this.switchChatTab(firstTab);
        } else {
            this.updateChatTabsUI();
        }
        
        this.saveState();
    }
    
    setupFileDropZone() {
        const dropZone = document.getElementById('fileDropZone');
        const chatContainer = document.querySelector('.chat-container');
        
        chatContainer.addEventListener('dragenter', (e) => {
            e.preventDefault();
            dropZone.classList.add('active');
        });
        
        chatContainer.addEventListener('dragleave', (e) => {
            e.preventDefault();
            if (!chatContainer.contains(e.relatedTarget)) {
                dropZone.classList.remove('active');
            }
        });
        
        chatContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('active');
            
            const files = Array.from(e.dataTransfer.files);
            this.handleFileUpload(files);
        });
    }
    
    async handleFileUpload(files) {
        if (files.length === 0) return;
        
        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });
        
        try {
            this.showTypingIndicator('Analyzing uploaded files...');
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.addMessage('user', `Uploaded ${files.length} file(s): ${Array.from(files).map(f => f.name).join(', ')}`);
                this.addMessage('assistant', result.analysis);
            } else {
                this.addMessage('system', `Error uploading files: ${result.error}`);
            }
        } catch (error) {
            console.error('File upload error:', error);
            this.addMessage('system', 'Error uploading files. Please try again.');
        } finally {
            this.hideTypingIndicator();
        }
    }
    
    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage('user', message);
        messageInput.value = '';
        this.autoResizeTextarea(messageInput);
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    chat_id: this.currentChatTab,
                    context: this.getChatContext()
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.addMessage('assistant', result.response, result.metadata);
            } else {
                this.addMessage('system', `Error: ${result.error}`);
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessage('system', 'Connection error. Please try again.');
        } finally {
            this.hideTypingIndicator();
        }
    }
    
    addMessage(sender, content, metadata = {}) {
        const chatMessages = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString();
        
        let messageHTML = '';
        
        if (sender === 'user') {
            messageHTML = `
                <div class="message-content">
                    <div class="message-header">
                        <span class="sender-name">You</span>
                        <span class="message-time">${timestamp}</span>
                    </div>
                    <div class="message-text">${this.formatMessage(content)}</div>
                </div>
                <div class="message-avatar">
                    <i class="fas fa-user"></i>
                </div>
            `;
        } else if (sender === 'assistant') {
            messageHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="sender-name">Juggernaut AI</span>
                        <span class="message-time">${timestamp}</span>
                        ${metadata.tokens ? `<span class="token-count">${metadata.tokens} tokens</span>` : ''}
                        ${metadata.response_time ? `<span class="response-time">${metadata.response_time}ms</span>` : ''}
                    </div>
                    <div class="message-text">${this.formatMessage(content)}</div>
                    <div class="message-actions">
                        <button class="action-btn" onclick="juggernautAI.rateMessage(this, 'good')">
                            <i class="fas fa-thumbs-up"></i>
                        </button>
                        <button class="action-btn" onclick="juggernautAI.rateMessage(this, 'bad')">
                            <i class="fas fa-thumbs-down"></i>
                        </button>
                        <button class="action-btn" onclick="juggernautAI.favoriteMessage(this)">
                            <i class="fas fa-star"></i>
                        </button>
                        <button class="action-btn" onclick="juggernautAI.copyMessage(this)">
                            <i class="fas fa-copy"></i>
                        </button>
                    </div>
                </div>
            `;
        } else if (sender === 'system') {
            messageHTML = `
                <div class="system-message">
                    <i class="fas fa-info-circle"></i>
                    <span>${content}</span>
                </div>
            `;
        }
        
        messageElement.innerHTML = messageHTML;
        chatMessages.appendChild(messageElement);
        
        // Save message to current chat tab
        const currentTab = this.chatTabs.get(this.currentChatTab);
        if (currentTab) {
            currentTab.messages.push({
                sender,
                content,
                timestamp: Date.now(),
                metadata
            });
        }
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Save state
        this.saveState();
    }
    
    formatMessage(content) {
        // Convert markdown-like formatting
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        content = content.replace(/`(.*?)`/g, '<code>$1</code>');
        content = content.replace(/\n/g, '<br>');
        
        // Convert URLs to links
        content = content.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
        
        return content;
    }
    
    showTypingIndicator(message = 'Juggernaut AI is thinking...') {
        const chatMessages = document.getElementById('chatMessages');
        const typingElement = document.createElement('div');
        typingElement.className = 'typing-indicator';
        typingElement.id = 'typingIndicator';
        
        typingElement.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="typing-content">
                <div class="typing-text">${message}</div>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    loadChatMessages(tabId) {
        const chatMessages = document.getElementById('chatMessages');
        const tab = this.chatTabs.get(tabId);
        
        if (!tab) return;
        
        // Clear current messages
        this.clearChatMessages();
        
        // Load messages for this tab
        tab.messages.forEach(msg => {
            this.addMessage(msg.sender, msg.content, msg.metadata);
        });
    }
    
    clearChatMessages() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="ai-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="welcome-content">
                    <h3>Enhanced Juggernaut AI</h3>
                    <p>Your RTX 4070 SUPER powered AI assistant with advanced learning capabilities!</p>
                    <div class="feature-tags">
                        <span class="tag">⚡ GPU Acceleration</span>
                        <span class="tag">🧠 Learning System</span>
                        <span class="tag">👁️ Context Awareness</span>
                        <span class="tag">🔄 Performance Tracking</span>
                    </div>
                    <div class="quick-actions">
                        <button class="quick-action" onclick="askCapabilities()">
                            <i class="fas fa-question-circle"></i>
                            Ask about capabilities
                        </button>
                        <button class="quick-action" onclick="viewLearningInsights()">
                            <i class="fas fa-chart-line"></i>
                            View learning insights
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    getChatContext() {
        const currentTab = this.chatTabs.get(this.currentChatTab);
        if (!currentTab) return [];
        
        // Return last 10 messages for context
        return currentTab.messages.slice(-10).map(msg => ({
            role: msg.sender === 'user' ? 'user' : 'assistant',
            content: msg.content
        }));
    }
    
    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
    
    // Browser functionality
    initializeBrowser() {
        // Initialize browser view
        console.log('Initializing browser...');
    }
    
    switchBrowserMode(mode) {
        this.browserMode = mode;
        
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        document.querySelector(`[data-mode="${mode}"]`).classList.add('active');
        
        // Update browser view based on mode
        if (mode === 'ai') {
            this.loadAIBrowser();
        } else if (mode === 'chrome') {
            this.loadChromeBrowser();
        }
    }
    
    navigateBrowser() {
        const url = document.getElementById('urlInput').value;
        if (!url) return;
        
        // Add protocol if missing
        const fullUrl = url.startsWith('http') ? url : `https://${url}`;
        
        this.loadBrowserPage(fullUrl);
    }
    
    async loadBrowserPage(url) {
        try {
            const response = await fetch('/api/browser/navigate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    mode: this.browserMode
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.updateBrowserView(result.content);
            } else {
                console.error('Browser navigation error:', result.error);
            }
        } catch (error) {
            console.error('Browser error:', error);
        }
    }
    
    updateBrowserView(content) {
        const browserView = document.getElementById('browserView');
        browserView.innerHTML = content;
    }
    
    expandBrowserView() {
        const overlay = document.getElementById('browserOverlay');
        overlay.classList.add('active');
        
        // Load current page in iframe
        const iframe = document.getElementById('browserFrame');
        const currentUrl = document.getElementById('urlInput').value;
        if (currentUrl) {
            iframe.src = currentUrl.startsWith('http') ? currentUrl : `https://${currentUrl}`;
        }
    }
    
    closeBrowserOverlay() {
        const overlay = document.getElementById('browserOverlay');
        overlay.classList.remove('active');
    }
    
    loadAIBrowser() {
        // Load AI-controlled browser view
        console.log('Loading AI browser...');
    }
    
    loadChromeBrowser() {
        // Load user's Chrome browser view
        console.log('Loading Chrome browser...');
    }
    
    // File management
    async loadFiles() {
        try {
            const response = await fetch('/api/files');
            const result = await response.json();
            
            if (result.success) {
                this.updateFilesGrid(result.files);
            }
        } catch (error) {
            console.error('Error loading files:', error);
        }
    }
    
    updateFilesGrid(files) {
        const filesGrid = document.getElementById('filesGrid');
        filesGrid.innerHTML = '';
        
        files.forEach(file => {
            const fileElement = document.createElement('div');
            fileElement.className = 'file-item';
            fileElement.innerHTML = `
                <div class="file-icon">
                    <i class="fas fa-${this.getFileIcon(file.type)}"></i>
                </div>
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${this.formatFileSize(file.size)}</div>
                    <div class="file-date">${new Date(file.modified).toLocaleDateString()}</div>
                </div>
                <div class="file-actions">
                    <button onclick="juggernautAI.openFile('${file.id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button onclick="juggernautAI.deleteFile('${file.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            
            filesGrid.appendChild(fileElement);
        });
    }
    
    getFileIcon(type) {
        const icons = {
            'pdf': 'file-pdf',
            'doc': 'file-word',
            'docx': 'file-word',
            'txt': 'file-alt',
            'jpg': 'file-image',
            'jpeg': 'file-image',
            'png': 'file-image',
            'gif': 'file-image',
            'mp4': 'file-video',
            'mp3': 'file-audio',
            'zip': 'file-archive',
            'default': 'file'
        };
        
        return icons[type] || icons.default;
    }
    
    formatFileSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Bytes';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    // System monitoring
    startSystemMonitoring() {
        this.updateSystemMetrics();
        setInterval(() => {
            this.updateSystemMetrics();
        }, 5000); // Update every 5 seconds
    }
    
    async updateSystemMetrics() {
        try {
            const response = await fetch('/api/system/metrics');
            const metrics = await response.json();
            
            if (metrics.success) {
                this.updateSystemStatus(metrics.data);
            }
        } catch (error) {
            console.error('Error updating system metrics:', error);
        }
    }
    
    updateSystemStatus(metrics) {
        // Update sidebar status
        document.getElementById('gpu-status').textContent = metrics.gpu || 'RTX 4070';
        document.getElementById('vram-status').textContent = metrics.vram || '12GB';
        document.getElementById('model-status').textContent = metrics.model || 'Gemma';
        document.getElementById('chat-count').textContent = this.chatTabs.size;
        
        // Update computer tab metrics if visible
        if (this.currentTab === 'computer') {
            const metricCards = document.querySelectorAll('.metric-value');
            if (metricCards.length >= 4) {
                metricCards[0].textContent = `${metrics.cpu_usage || 45}%`;
                metricCards[1].textContent = `${metrics.ram_usage || 8.2}GB`;
                metricCards[2].textContent = `${metrics.gpu_usage || 67}%`;
                metricCards[3].textContent = `${metrics.gpu_temp || 72}°C`;
            }
        }
    }
    
    // WebSocket connection
    connectWebSocket() {
        try {
            this.ws = new WebSocket(`ws://${window.location.host}/ws`);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.isConnected = true;
                this.updateConnectionStatus();
            };
            
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.isConnected = false;
                this.updateConnectionStatus();
                
                // Attempt to reconnect after 5 seconds
                setTimeout(() => {
                    this.connectWebSocket();
                }, 5000);
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        } catch (error) {
            console.error('WebSocket connection error:', error);
        }
    }
    
    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'system_update':
                this.updateSystemStatus(data.metrics);
                break;
            case 'chat_response':
                this.addMessage('assistant', data.message, data.metadata);
                this.hideTypingIndicator();
                break;
            case 'browser_update':
                this.updateBrowserView(data.content);
                break;
            default:
                console.log('Unknown WebSocket message:', data);
        }
    }
    
    updateConnectionStatus() {
        const indicators = document.querySelectorAll('.indicator');
        const connectionIndicator = Array.from(indicators).find(ind => 
            ind.textContent.includes('Connected') || ind.textContent.includes('Disconnected')
        );
        
        if (connectionIndicator) {
            const span = connectionIndicator.querySelector('span');
            span.textContent = this.isConnected ? 'Connected' : 'Disconnected';
            connectionIndicator.style.color = this.isConnected ? 'var(--accent-primary)' : 'var(--text-muted)';
        }
    }
    
    // State management
    saveState() {
        const state = {
            currentTab: this.currentTab,
            currentChatTab: this.currentChatTab,
            sidebarCollapsed: this.sidebarCollapsed,
            chatTabs: Array.from(this.chatTabs.entries()),
            browserMode: this.browserMode
        };
        
        localStorage.setItem('juggernaut_state', JSON.stringify(state));
    }
    
    loadSavedState() {
        try {
            const savedState = localStorage.getItem('juggernaut_state');
            if (savedState) {
                const state = JSON.parse(savedState);
                
                if (state.sidebarCollapsed) {
                    this.toggleSidebar();
                }
                
                if (state.chatTabs) {
                    this.chatTabs = new Map(state.chatTabs);
                    this.updateChatTabsUI();
                }
                
                if (state.currentChatTab && this.chatTabs.has(state.currentChatTab)) {
                    this.switchChatTab(state.currentChatTab);
                }
                
                if (state.currentTab) {
                    this.switchTab(state.currentTab);
                }
                
                if (state.browserMode) {
                    this.switchBrowserMode(state.browserMode);
                }
            }
        } catch (error) {
            console.error('Error loading saved state:', error);
        }
    }
    
    // Utility methods
    handleResize() {
        // Handle responsive behavior
        const sidebar = document.getElementById('sidebar');
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('mobile-open');
        }
    }
    
    // Message actions
    rateMessage(button, rating) {
        const messageElement = button.closest('.message');
        // Implement rating logic
        console.log('Rating message:', rating);
    }
    
    favoriteMessage(button) {
        const messageElement = button.closest('.message');
        button.classList.toggle('favorited');
        // Implement favorite logic
        console.log('Favoriting message');
    }
    
    copyMessage(button) {
        const messageElement = button.closest('.message');
        const messageText = messageElement.querySelector('.message-text').textContent;
        
        navigator.clipboard.writeText(messageText).then(() => {
            // Show copy confirmation
            const originalIcon = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                button.innerHTML = originalIcon;
            }, 1000);
        });
    }
    
    // Image generation
    openImageGeneration() {
        this.switchTab('image-gen');
        document.getElementById('imagePrompt').focus();
    }
    
    // Voice input
    startVoiceInput() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            recognition.onstart = () => {
                document.getElementById('voiceInput').classList.add('recording');
            };
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('messageInput').value = transcript;
                this.autoResizeTextarea(document.getElementById('messageInput'));
            };
            
            recognition.onend = () => {
                document.getElementById('voiceInput').classList.remove('recording');
            };
            
            recognition.start();
        } else {
            alert('Speech recognition not supported in this browser.');
        }
    }
}

// Global functions
function askCapabilities() {
    juggernautAI.addMessage('user', 'What are your capabilities and features?');
    juggernautAI.sendMessage();
}

function viewLearningInsights() {
    juggernautAI.addMessage('user', 'Show me your learning insights and performance metrics.');
    juggernautAI.sendMessage();
}

function startBrowsing() {
    juggernautAI.switchTab('browser');
}

function openCommSetup() {
    juggernautAI.switchTab('communication');
}

// Initialize the application
let juggernautAI;

document.addEventListener('DOMContentLoaded', () => {
    juggernautAI = new JuggernautAI();
});

// Add CSS for message styling
const messageStyles = `
<style>
.message {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    align-items: flex-start;
}

.user-message {
    flex-direction: row-reverse;
}

.message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.user-message .message-avatar {
    background: var(--bg-tertiary);
    color: var(--text-primary);
}

.assistant-message .message-avatar {
    background: var(--gradient-primary);
    color: var(--bg-primary);
}

.message-content {
    flex: 1;
    background: var(--bg-card);
    border-radius: 12px;
    padding: 12px 16px;
    border: 1px solid var(--border-color);
}

.user-message .message-content {
    background: var(--accent-primary);
    color: var(--bg-primary);
}

.message-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 12px;
}

.sender-name {
    font-weight: 600;
}

.message-time {
    color: var(--text-muted);
}

.user-message .message-time {
    color: rgba(0, 0, 0, 0.6);
}

.token-count, .response-time {
    background: var(--bg-secondary);
    padding: 2px 6px;
    border-radius: 10px;
    font-size: 10px;
}

.message-text {
    line-height: 1.5;
    word-wrap: break-word;
}

.message-actions {
    display: flex;
    gap: 8px;
    margin-top: 8px;
    opacity: 0;
    transition: var(--transition-fast);
}

.message:hover .message-actions {
    opacity: 1;
}

.message-actions .action-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
    transition: var(--transition-fast);
}

.message-actions .action-btn:hover {
    background: var(--bg-secondary);
    color: var(--accent-primary);
}

.typing-indicator {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    align-items: flex-start;
}

.typing-content {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 12px 16px;
    border: 1px solid var(--border-color);
}

.typing-text {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 8px;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 6px;
    height: 6px;
    background: var(--accent-primary);
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% {
        transform: scale(0);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

.system-message {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: var(--bg-tertiary);
    border-radius: 6px;
    margin-bottom: 12px;
    font-size: 14px;
    color: var(--text-secondary);
}

.system-message i {
    color: var(--accent-primary);
}

#voiceInput.recording {
    background: var(--accent-primary);
    color: var(--bg-primary);
}

.file-item {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 15px;
    transition: var(--transition-fast);
}

.file-item:hover {
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-primary);
}

.file-icon {
    font-size: 24px;
    color: var(--accent-primary);
    margin-bottom: 10px;
}

.file-info {
    margin-bottom: 10px;
}

.file-name {
    font-weight: 600;
    margin-bottom: 4px;
}

.file-size, .file-date {
    font-size: 12px;
    color: var(--text-muted);
}

.file-actions {
    display: flex;
    gap: 8px;
}

.file-actions button {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    padding: 6px 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: var(--transition-fast);
}

.file-actions button:hover {
    background: var(--bg-tertiary);
    color: var(--accent-primary);
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', messageStyles);

