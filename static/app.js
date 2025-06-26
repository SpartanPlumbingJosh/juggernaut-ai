/**
 * Juggernaut AI - Complete JavaScript Application
 * RTX 4070 SUPER Optimized Monster UI
 * Production-ready frontend with full functionality
 */

class JuggernautAI {
    constructor() {
        this.currentChatId = null;
        this.isInitialized = false;
        this.systemStatus = {};
        this.activeTab = 'chat';
        this.messageQueue = [];
        this.isProcessing = false;
        
        // Performance metrics
        this.metrics = {
            totalMessages: 0,
            totalResponseTime: 0,
            averageResponseTime: 0
        };
        
        // Initialize the application
        this.init();
    }

    async init() {
        try {
            console.log('🚀 Initializing Juggernaut AI...');
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Initialize system status
            await this.updateSystemStatus();
            
            // Initialize chat system
            await this.initializeChat();
            
            // Setup periodic updates
            this.startPeriodicUpdates();
            
            this.isInitialized = true;
            this.showToast('Juggernaut AI initialized successfully!', 'success');
            
            console.log('✅ Juggernaut AI initialized successfully');
            
        } catch (error) {
            console.error('❌ Failed to initialize Juggernaut AI:', error);
            this.showToast('Failed to initialize system', 'error');
        }
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                if (tab) this.switchTab(tab);
            });
        });

        // Chat functionality
        const sendBtn = document.getElementById('send-btn');
        const messageInput = document.getElementById('message-input');
        const newChatBtn = document.getElementById('new-chat-btn');
        const clearChatBtn = document.getElementById('clear-chat-btn');
        const attachmentBtn = document.getElementById('attachment-btn');

        if (sendBtn) sendBtn.addEventListener('click', () => this.sendMessage());
        if (newChatBtn) newChatBtn.addEventListener('click', () => this.createNewChat());
        if (clearChatBtn) clearChatBtn.addEventListener('click', () => this.clearChat());
        if (attachmentBtn) attachmentBtn.addEventListener('click', () => this.handleFileUpload());

        if (messageInput) {
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                } else if (e.key === 'Enter' && e.shiftKey) {
                    // Allow new line
                }
            });

            messageInput.addEventListener('input', () => {
                this.autoResizeTextarea(messageInput);
            });
        }

        // Browser functionality
        const navigateBtn = document.getElementById('navigate-btn');
        const urlInput = document.getElementById('url-input');

        if (navigateBtn) navigateBtn.addEventListener('click', () => this.navigateBrowser());
        if (urlInput) {
            urlInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.navigateBrowser();
            });
        }

        // File management
        const uploadBtn = document.getElementById('upload-btn');
        const fileInput = document.getElementById('file-input');

        if (uploadBtn) uploadBtn.addEventListener('click', () => fileInput?.click());
        if (fileInput) fileInput.addEventListener('change', (e) => this.handleFileSelection(e));

        // Research functionality
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) analyzeBtn.addEventListener('click', () => this.analyzeResearch());

        // Settings functionality
        this.setupSettingsListeners();

        // Plugin functionality
        const refreshPluginsBtn = document.getElementById('refresh-plugins-btn');
        if (refreshPluginsBtn) refreshPluginsBtn.addEventListener('click', () => this.refreshPlugins());
    }

    setupSettingsListeners() {
        // Temperature slider
        const temperatureSlider = document.getElementById('temperature');
        const temperatureValue = document.getElementById('temperature-value');
        
        if (temperatureSlider && temperatureValue) {
            temperatureSlider.addEventListener('input', (e) => {
                temperatureValue.textContent = e.target.value;
            });
        }

        // Settings buttons
        const exportSettingsBtn = document.getElementById('export-settings-btn');
        const resetSettingsBtn = document.getElementById('reset-settings-btn');

        if (exportSettingsBtn) exportSettingsBtn.addEventListener('click', () => this.exportSettings());
        if (resetSettingsBtn) resetSettingsBtn.addEventListener('click', () => this.resetSettings());
    }

    switchTab(tabName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');

        // Update content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`)?.classList.add('active');

        this.activeTab = tabName;
        console.log(`📑 Switched to ${tabName} tab`);
    }

    async updateSystemStatus() {
        try {
            const response = await fetch('/api/status');
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            this.systemStatus = await response.json();
            this.updateStatusDisplay();
            
        } catch (error) {
            console.error('Failed to update system status:', error);
            this.updateStatusDisplay(false);
        }
    }

    updateStatusDisplay(isOnline = true) {
        const statusIndicator = document.getElementById('status-indicator');
        const statusText = statusIndicator?.querySelector('.status-text');
        const statusDot = statusIndicator?.querySelector('.status-dot');

        if (statusText && statusDot) {
            if (isOnline && this.systemStatus.status === 'ready') {
                statusText.textContent = 'System Ready';
                statusDot.style.background = 'var(--success)';
            } else if (isOnline) {
                statusText.textContent = 'Initializing...';
                statusDot.style.background = 'var(--warning)';
            } else {
                statusText.textContent = 'Offline';
                statusDot.style.background = 'var(--error)';
            }
        }

        // Update system stats
        if (this.systemStatus.metrics) {
            const chatCount = document.getElementById('chat-count');
            const modelStatus = document.getElementById('model-status');
            const gpuStatus = document.getElementById('gpu-status');

            if (chatCount) chatCount.textContent = this.systemStatus.active_chats || 0;
            if (modelStatus) modelStatus.textContent = this.systemStatus.components?.ai_engine ? 'Ready' : 'Demo';
            if (gpuStatus) gpuStatus.textContent = this.systemStatus.gpu_ready ? 'Ready' : 'Offline';
        }
    }

    async initializeChat() {
        try {
            const response = await fetch('/api/chat/new', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.currentChatId = data.chat_id;
            
            console.log('💬 Chat initialized:', this.currentChatId);
            
        } catch (error) {
            console.error('Failed to initialize chat:', error);
            this.showToast('Failed to initialize chat', 'error');
        }
    }

    async sendMessage() {
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        
        if (!messageInput || !sendBtn) return;

        const message = messageInput.value.trim();
        if (!message || !this.currentChatId || this.isProcessing) return;

        this.isProcessing = true;
        const startTime = Date.now();

        try {
            // Disable input
            messageInput.disabled = true;
            sendBtn.disabled = true;
            
            // Clear input and add user message
            messageInput.value = '';
            this.autoResizeTextarea(messageInput);
            this.addMessageToChat('user', message);

            // Show loading
            this.showLoading(true);

            // Send to API
            const response = await fetch(`/api/chat/${this.currentChatId}/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            
            // Add AI response
            this.addMessageToChat('assistant', data.response);
            
            // Update metrics
            const responseTime = Date.now() - startTime;
            this.updateMetrics(responseTime, data.response);
            
            console.log(`💬 Message processed in ${responseTime}ms`);

        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessageToChat('error', 'Failed to send message. Please try again.');
            this.showToast('Failed to send message', 'error');
        } finally {
            // Re-enable input
            messageInput.disabled = false;
            sendBtn.disabled = false;
            messageInput.focus();
            this.showLoading(false);
            this.isProcessing = false;
        }
    }

    addMessageToChat(role, content) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        // Remove welcome message if it exists
        const welcomeMessage = messagesContainer.querySelector('.welcome-message');
        if (welcomeMessage) welcomeMessage.remove();

        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const roleLabel = role === 'user' ? 'You' : 
                         role === 'assistant' ? 'Juggernaut AI' : 
                         role === 'error' ? 'Error' : 'System';
        
        // Format content with basic markdown support
        const formattedContent = this.formatMessageContent(content);
        messageContent.innerHTML = `<strong>${roleLabel}</strong>${formattedContent}`;
        
        messageDiv.appendChild(messageContent);
        messagesContainer.appendChild(messageDiv);
        
        // Auto-scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    formatMessageContent(content) {
        // Basic markdown formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    updateMetrics(responseTime, response) {
        this.metrics.totalMessages++;
        this.metrics.totalResponseTime += responseTime;
        this.metrics.averageResponseTime = this.metrics.totalResponseTime / this.metrics.totalMessages;

        // Update UI
        const responseTimeElement = document.getElementById('response-time');
        const tokenCountElement = document.getElementById('token-count');

        if (responseTimeElement) {
            responseTimeElement.textContent = `${responseTime}ms`;
        }

        if (tokenCountElement) {
            const tokenCount = response.split(' ').length;
            tokenCountElement.textContent = `${tokenCount} tokens`;
        }
    }

    async createNewChat() {
        try {
            const response = await fetch('/api/chat/new', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.currentChatId = data.chat_id;
            
            // Clear messages
            this.clearChatMessages();
            
            this.showToast('New chat created', 'success');
            console.log('💬 New chat created:', this.currentChatId);
            
        } catch (error) {
            console.error('Failed to create new chat:', error);
            this.showToast('Failed to create new chat', 'error');
        }
    }

    clearChat() {
        this.clearChatMessages();
        this.showToast('Chat cleared', 'info');
    }

    clearChatMessages() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        messagesContainer.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">🤖</div>
                <h3>Welcome to Juggernaut AI</h3>
                <p>Your RTX 4070 SUPER is ready for GPU-accelerated AI responses. Start a conversation below!</p>
                <div class="welcome-features">
                    <div class="feature-item">⚡ GPU Acceleration</div>
                    <div class="feature-item">🧠 Advanced AI Models</div>
                    <div class="feature-item">💬 Natural Conversations</div>
                </div>
            </div>
        `;
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    async navigateBrowser() {
        const urlInput = document.getElementById('url-input');
        if (!urlInput) return;

        const url = urlInput.value.trim();
        if (!url) {
            this.showToast('Please enter a URL', 'warning');
            return;
        }

        try {
            this.showLoading(true);

            const response = await fetch('/api/browser/navigate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.showToast('Navigation successful', 'success');
            console.log('🌐 Browser navigation:', data);

        } catch (error) {
            console.error('Browser navigation failed:', error);
            this.showToast('Navigation failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    handleFileUpload() {
        const fileInput = document.getElementById('hidden-file-input');
        if (fileInput) fileInput.click();
    }

    async handleFileSelection(event) {
        const files = event.target.files;
        if (!files || files.length === 0) return;

        try {
            this.showLoading(true);

            const formData = new FormData();
            for (let file of files) {
                formData.append('files', file);
            }

            const response = await fetch('/api/files/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.showToast(`${data.total_uploaded} files uploaded successfully`, 'success');
            console.log('📁 Files uploaded:', data);

        } catch (error) {
            console.error('File upload failed:', error);
            this.showToast('File upload failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async analyzeResearch() {
        const researchInput = document.getElementById('research-input');
        const analysisType = document.getElementById('analysis-type');
        const researchOutput = document.getElementById('research-output');

        if (!researchInput || !analysisType || !researchOutput) return;

        const content = researchInput.value.trim();
        if (!content) {
            this.showToast('Please enter content to analyze', 'warning');
            return;
        }

        try {
            this.showLoading(true);

            const response = await fetch('/api/research/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content: content,
                    type: analysisType.value
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            
            // Display analysis results
            researchOutput.innerHTML = `
                <div class="analysis-result">
                    <h3>Analysis Results</h3>
                    <div class="analysis-meta">
                        <span>Type: ${data.analysis_type}</span>
                        <span>•</span>
                        <span>Length: ${data.content_length} chars</span>
                        <span>•</span>
                        <span>Time: ${data.response_time}s</span>
                    </div>
                    <div class="analysis-content">
                        ${this.formatMessageContent(data.analysis)}
                    </div>
                </div>
            `;

            this.showToast('Analysis completed', 'success');
            console.log('🔬 Research analysis completed:', data);

        } catch (error) {
            console.error('Research analysis failed:', error);
            this.showToast('Analysis failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async refreshPlugins() {
        try {
            this.showLoading(true);

            const response = await fetch('/api/plugins');
            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.showToast(`${data.total} plugins found`, 'info');
            console.log('🔌 Plugins refreshed:', data);

        } catch (error) {
            console.error('Failed to refresh plugins:', error);
            this.showToast('Failed to refresh plugins', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    exportSettings() {
        const settings = {
            maxTokens: document.getElementById('max-tokens')?.value,
            temperature: document.getElementById('temperature')?.value,
            contextLength: document.getElementById('context-length')?.value,
            gpuEnabled: document.getElementById('gpu-enabled')?.checked,
            gpuLayers: document.getElementById('gpu-layers')?.value,
            exportDate: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(settings, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'juggernaut-settings.json';
        a.click();
        URL.revokeObjectURL(url);

        this.showToast('Settings exported', 'success');
    }

    resetSettings() {
        if (confirm('Are you sure you want to reset all settings to default?')) {
            // Reset form values
            const maxTokens = document.getElementById('max-tokens');
            const temperature = document.getElementById('temperature');
            const temperatureValue = document.getElementById('temperature-value');
            const contextLength = document.getElementById('context-length');
            const gpuEnabled = document.getElementById('gpu-enabled');
            const gpuLayers = document.getElementById('gpu-layers');

            if (maxTokens) maxTokens.value = '150';
            if (temperature) temperature.value = '0.7';
            if (temperatureValue) temperatureValue.textContent = '0.7';
            if (contextLength) contextLength.value = '4096';
            if (gpuEnabled) gpuEnabled.checked = true;
            if (gpuLayers) gpuLayers.value = '35';

            this.showToast('Settings reset to default', 'info');
        }
    }

    showLoading(show) {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            if (show) {
                loadingOverlay.classList.add('active');
            } else {
                loadingOverlay.classList.remove('active');
            }
        }
    }

    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <strong>${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                <p>${message}</p>
            </div>
        `;

        toastContainer.appendChild(toast);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);

        // Add click to dismiss
        toast.addEventListener('click', () => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        });
    }

    startPeriodicUpdates() {
        // Update system status every 30 seconds
        setInterval(() => {
            this.updateSystemStatus();
        }, 30000);

        // Update metrics every 10 seconds
        setInterval(() => {
            if (this.metrics.totalMessages > 0) {
                console.log('📊 Metrics:', this.metrics);
            }
        }, 10000);
    }

    // Utility methods
    formatTime(ms) {
        if (ms < 1000) return `${ms}ms`;
        return `${(ms / 1000).toFixed(1)}s`;
    }

    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Public API for external access
    getMetrics() {
        return this.metrics;
    }

    getSystemStatus() {
        return this.systemStatus;
    }

    getCurrentChatId() {
        return this.currentChatId;
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Starting Juggernaut AI Monster UI...');
    window.juggernautAI = new JuggernautAI();
});

// Add global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    if (window.juggernautAI) {
        window.juggernautAI.showToast('An unexpected error occurred', 'error');
    }
});

// Add unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    if (window.juggernautAI) {
        window.juggernautAI.showToast('An unexpected error occurred', 'error');
    }
});

