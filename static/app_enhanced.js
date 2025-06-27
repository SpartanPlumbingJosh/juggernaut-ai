/**
 * Enhanced Juggernaut AI - Complete JavaScript Application
 * RTX 4070 SUPER Optimized Monster UI with Advanced Features
 * Real Gemma Integration with Learning Capabilities
 */

class JuggernautAI {
    constructor() {
        this.currentChatId = this.generateChatId();
        this.isInitialized = false;
        this.systemStatus = {};
        this.activeTab = 'chat';
        this.messageQueue = [];
        this.isProcessing = false;
        this.learningEnabled = true;
        
        // Enhanced features
        this.chatHistory = new Map();
        this.userPreferences = {};
        this.performanceMetrics = {
            totalMessages: 0,
            totalResponseTime: 0,
            averageResponseTime: 0,
            tokensPerSecond: 0,
            learningRate: 0
        };
        
        // Learning system
        this.feedbackHistory = [];
        this.conversationPatterns = {};
        this.learningInsights = {};
        
        // UI state
        this.isDarkMode = true;
        this.isFullscreen = false;
        this.notifications = [];
        
        // Initialize the application
        this.init();
    }

    async init() {
        try {
            console.log('🚀 Initializing Enhanced Juggernaut AI...');
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Initialize system status
            await this.updateSystemStatus();
            
            // Initialize chat system
            await this.initializeChat();
            
            // Load learning data
            await this.loadLearningData();
            
            // Setup periodic updates
            this.startPeriodicUpdates();
            
            // Initialize advanced features
            this.initializeAdvancedFeatures();
            
            this.isInitialized = true;
            this.showNotification('🤖 Enhanced Juggernaut AI initialized with learning capabilities!', 'success');
            
            console.log('✅ Enhanced Juggernaut AI initialized successfully');
            
        } catch (error) {
            console.error('❌ Failed to initialize Enhanced Juggernaut AI:', error);
            this.showNotification('Failed to initialize system', 'error');
        }
    }

    setupEventListeners() {
        // Tab navigation with enhanced features
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                if (tab) this.switchTab(tab);
            });
        });

        // Enhanced chat functionality
        const sendBtn = document.getElementById('send-btn');
        const messageInput = document.getElementById('message-input');
        const newChatBtn = document.getElementById('new-chat-btn');
        const clearChatBtn = document.getElementById('clear-chat-btn');
        const attachBtn = document.getElementById('attach-btn');

        if (sendBtn) sendBtn.addEventListener('click', () => this.sendMessage());
        if (newChatBtn) newChatBtn.addEventListener('click', () => this.createNewChat());
        if (clearChatBtn) clearChatBtn.addEventListener('click', () => this.clearChat());
        if (attachBtn) attachBtn.addEventListener('click', () => this.handleFileUpload());

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
                this.handleTypingIndicator();
            });
        }

        // Enhanced browser functionality
        const navigateBtn = document.getElementById('navigate-btn');
        const urlInput = document.getElementById('url-input');

        if (navigateBtn) navigateBtn.addEventListener('click', () => this.navigateBrowser());
        if (urlInput) {
            urlInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.navigateBrowser();
            });
        }

        // Learning and feedback system
        this.setupFeedbackListeners();
        
        // Advanced UI features
        this.setupAdvancedUIListeners();
    }

    setupFeedbackListeners() {
        // Add feedback buttons to messages
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('feedback-btn')) {
                const messageId = e.target.dataset.messageId;
                const feedback = e.target.dataset.feedback;
                this.submitFeedback(messageId, feedback);
            }
        });
    }

    setupAdvancedUIListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'n':
                        e.preventDefault();
                        this.createNewChat();
                        break;
                    case 'k':
                        e.preventDefault();
                        this.clearChat();
                        break;
                    case 'l':
                        e.preventDefault();
                        this.showLearningInsights();
                        break;
                }
            }
        });

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Fullscreen toggle
        const fullscreenToggle = document.getElementById('fullscreen-toggle');
        if (fullscreenToggle) {
            fullscreenToggle.addEventListener('click', () => this.toggleFullscreen());
        }
    }

    generateChatId() {
        return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async updateSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            this.systemStatus = status;
            this.updateStatusDisplay(status);
            
            // Update learning metrics if available
            if (status.learning_stats) {
                this.performanceMetrics.learningRate = status.learning_stats.learning_rate || 0;
            }
            
        } catch (error) {
            console.error('Status update failed:', error);
            this.showNotification('Failed to update system status', 'warning');
        }
    }

    updateStatusDisplay(status) {
        // Update status indicators
        const statusIndicator = document.getElementById('status-indicator');
        const gpuStatus = document.getElementById('gpu-status');
        const vramStatus = document.getElementById('vram-status');
        const modelStatus = document.getElementById('model-status');
        const chatCount = document.getElementById('chat-count');

        if (statusIndicator) {
            const statusDot = statusIndicator.querySelector('.status-dot');
            const statusText = statusIndicator.querySelector('.status-text');
            
            if (status.ready) {
                statusDot.className = 'status-dot status-ready';
                statusText.textContent = status.model_loaded ? 'Gemma Ready' : 'Demo Mode';
            } else {
                statusDot.className = 'status-dot status-loading';
                statusText.textContent = 'Initializing...';
            }
        }

        if (gpuStatus) {
            gpuStatus.textContent = status.gpu_optimization || 'CPU Mode';
        }

        if (vramStatus) {
            vramStatus.textContent = status.model_loaded ? '12GB' : 'N/A';
        }

        if (modelStatus) {
            modelStatus.textContent = status.model_loaded ? 'Loaded' : 'Demo';
        }

        if (chatCount) {
            chatCount.textContent = this.chatHistory.size.toString();
        }

        // Update performance metrics display
        this.updatePerformanceDisplay();
    }

    updatePerformanceDisplay() {
        const avgResponseTime = document.getElementById('avg-response-time');
        const tokensPerSec = document.getElementById('tokens-per-sec');
        const learningRate = document.getElementById('learning-rate');

        if (avgResponseTime) {
            avgResponseTime.textContent = `${this.performanceMetrics.averageResponseTime.toFixed(2)}s`;
        }

        if (tokensPerSec) {
            tokensPerSec.textContent = `${this.performanceMetrics.tokensPerSecond.toFixed(1)} t/s`;
        }

        if (learningRate) {
            learningRate.textContent = `${this.performanceMetrics.learningRate.toFixed(1)}%`;
        }
    }

    async initializeChat() {
        try {
            // Load existing chats
            const response = await fetch('/api/chats');
            const chats = await response.json();
            
            if (chats.chats) {
                Object.entries(chats.chats).forEach(([chatId, messages]) => {
                    this.chatHistory.set(chatId, messages);
                });
            }
            
            // Create initial chat if none exist
            if (this.chatHistory.size === 0) {
                await this.createNewChat();
            } else {
                // Load the most recent chat
                const lastChatId = Array.from(this.chatHistory.keys()).pop();
                this.currentChatId = lastChatId;
                this.loadChatMessages(lastChatId);
            }
            
        } catch (error) {
            console.error('Chat initialization failed:', error);
            await this.createNewChat();
        }
    }

    async loadLearningData() {
        try {
            const response = await fetch('/api/learning/insights');
            if (response.ok) {
                this.learningInsights = await response.json();
                this.updateLearningDisplay();
            }
        } catch (error) {
            console.log('Learning data not available yet');
        }
    }

    updateLearningDisplay() {
        const learningStats = document.getElementById('learning-stats');
        if (learningStats && this.learningInsights) {
            learningStats.innerHTML = `
                <div class="learning-metric">
                    <span class="metric-label">Interactions:</span>
                    <span class="metric-value">${this.learningInsights.total_interactions || 0}</span>
                </div>
                <div class="learning-metric">
                    <span class="metric-label">Satisfaction:</span>
                    <span class="metric-value">${(this.learningInsights.satisfaction_rate || 0).toFixed(1)}%</span>
                </div>
                <div class="learning-metric">
                    <span class="metric-label">Patterns:</span>
                    <span class="metric-value">${this.learningInsights.conversation_patterns || 0}</span>
                </div>
            `;
        }
    }

    async sendMessage() {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();
        
        if (!message || this.isProcessing) return;
        
        this.isProcessing = true;
        const startTime = Date.now();
        
        try {
            // Clear input and show user message
            messageInput.value = '';
            this.autoResizeTextarea(messageInput);
            
            const messageId = this.addMessageToChat('user', message);
            
            // Show typing indicator
            const typingId = this.showTypingIndicator();
            
            // Send to backend
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
            
            const result = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            if (result.success) {
                // Add AI response
                const aiMessageId = this.addMessageToChat('assistant', result.response, {
                    model: result.model,
                    responseTime: result.response_time,
                    tokens: result.tokens,
                    tokensPerSecond: result.tokens_per_second,
                    learningEnabled: result.learning_enabled,
                    gpuAccelerated: result.gpu_accelerated
                });
                
                // Update performance metrics
                this.updatePerformanceMetrics(result);
                
                // Add feedback buttons
                this.addFeedbackButtons(aiMessageId);
                
                // Update chat history
                this.updateChatHistory();
                
                this.showNotification('✅ Response generated successfully', 'success');
                
            } else {
                this.showNotification('❌ Failed to get response', 'error');
            }
            
        } catch (error) {
            console.error('Send message failed:', error);
            this.showNotification('❌ Message sending failed', 'error');
        } finally {
            this.isProcessing = false;
            messageInput.focus();
        }
    }

    addMessageToChat(role, content, metadata = {}) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageId = 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        messageDiv.dataset.messageId = messageId;
        
        const timestamp = new Date().toLocaleTimeString();
        
        let metadataHtml = '';
        if (metadata.responseTime) {
            metadataHtml = `
                <div class="message-metadata">
                    <span class="metadata-item">⏱️ ${metadata.responseTime.toFixed(2)}s</span>
                    <span class="metadata-item">📊 ${metadata.tokens} tokens</span>
                    <span class="metadata-item">⚡ ${(metadata.tokensPerSecond || 0).toFixed(1)} t/s</span>
                    ${metadata.gpuAccelerated ? '<span class="metadata-item gpu-badge">🎯 GPU</span>' : ''}
                    ${metadata.learningEnabled ? '<span class="metadata-item learning-badge">🧠 Learning</span>' : ''}
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-role">${role === 'user' ? '👤 You' : '🤖 Juggernaut'}</span>
                <span class="message-time">${timestamp}</span>
            </div>
            <div class="message-content">${this.formatMessageContent(content)}</div>
            ${metadataHtml}
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        return messageId;
    }

    formatMessageContent(content) {
        // Enhanced message formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    addFeedbackButtons(messageId) {
        const messageDiv = document.querySelector(`[data-message-id="${messageId}"]`);
        if (messageDiv && !messageDiv.querySelector('.feedback-buttons')) {
            const feedbackDiv = document.createElement('div');
            feedbackDiv.className = 'feedback-buttons';
            feedbackDiv.innerHTML = `
                <button class="feedback-btn feedback-positive" data-message-id="${messageId}" data-feedback="good" title="Good response">
                    👍
                </button>
                <button class="feedback-btn feedback-negative" data-message-id="${messageId}" data-feedback="bad" title="Poor response">
                    👎
                </button>
                <button class="feedback-btn feedback-excellent" data-message-id="${messageId}" data-feedback="excellent" title="Excellent response">
                    ⭐
                </button>
            `;
            messageDiv.appendChild(feedbackDiv);
        }
    }

    async submitFeedback(messageId, feedback) {
        try {
            const response = await fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message_id: messageId,
                    chat_id: this.currentChatId,
                    feedback: feedback
                })
            });
            
            if (response.ok) {
                // Visual feedback
                const feedbackButtons = document.querySelector(`[data-message-id="${messageId}"] .feedback-buttons`);
                if (feedbackButtons) {
                    feedbackButtons.innerHTML = `<span class="feedback-submitted">✅ Feedback: ${feedback}</span>`;
                }
                
                this.showNotification(`📝 Feedback submitted: ${feedback}`, 'success');
                
                // Update learning data
                await this.loadLearningData();
                
            } else {
                this.showNotification('❌ Failed to submit feedback', 'error');
            }
            
        } catch (error) {
            console.error('Feedback submission failed:', error);
            this.showNotification('❌ Feedback submission failed', 'error');
        }
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const typingId = 'typing_' + Date.now();
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant-message typing-indicator';
        typingDiv.id = typingId;
        typingDiv.innerHTML = `
            <div class="message-header">
                <span class="message-role">🤖 Juggernaut</span>
                <span class="message-time">thinking...</span>
            </div>
            <div class="message-content">
                <div class="typing-animation">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        return typingId;
    }

    removeTypingIndicator(typingId) {
        const typingDiv = document.getElementById(typingId);
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    updatePerformanceMetrics(result) {
        this.performanceMetrics.totalMessages++;
        this.performanceMetrics.totalResponseTime += result.response_time || 0;
        this.performanceMetrics.averageResponseTime = this.performanceMetrics.totalResponseTime / this.performanceMetrics.totalMessages;
        this.performanceMetrics.tokensPerSecond = result.tokens_per_second || 0;
        
        this.updatePerformanceDisplay();
    }

    async createNewChat() {
        try {
            this.currentChatId = this.generateChatId();
            this.chatHistory.set(this.currentChatId, []);
            
            // Clear chat display
            const messagesContainer = document.getElementById('chat-messages');
            if (messagesContainer) {
                messagesContainer.innerHTML = this.getWelcomeMessage();
            }
            
            this.showNotification('📝 New chat created', 'success');
            
        } catch (error) {
            console.error('Create new chat failed:', error);
            this.showNotification('❌ Failed to create new chat', 'error');
        }
    }

    getWelcomeMessage() {
        return `
            <div class="welcome-message">
                <div class="welcome-icon">🤖</div>
                <h3>Enhanced Juggernaut AI</h3>
                <p>Your RTX 4070 SUPER powered AI assistant with advanced learning capabilities!</p>
                <div class="feature-badges">
                    <span class="feature-badge">⚡ GPU Acceleration</span>
                    <span class="feature-badge">🧠 Learning System</span>
                    <span class="feature-badge">💬 Context Awareness</span>
                    <span class="feature-badge">📈 Performance Tracking</span>
                </div>
                <div class="quick-actions">
                    <button class="quick-action-btn" onclick="juggernautAI.sendQuickMessage('Hello! Tell me about your capabilities.')">
                        💬 Ask about capabilities
                    </button>
                    <button class="quick-action-btn" onclick="juggernautAI.showLearningInsights()">
                        📊 View learning insights
                    </button>
                </div>
            </div>
        `;
    }

    async sendQuickMessage(message) {
        const messageInput = document.getElementById('message-input');
        if (messageInput) {
            messageInput.value = message;
            await this.sendMessage();
        }
    }

    showLearningInsights() {
        const modal = this.createModal('Learning Insights', this.generateLearningInsightsHTML());
        document.body.appendChild(modal);
    }

    generateLearningInsightsHTML() {
        const insights = this.learningInsights;
        
        return `
            <div class="learning-insights">
                <div class="insights-grid">
                    <div class="insight-card">
                        <h4>📊 Interaction Stats</h4>
                        <p>Total Interactions: <strong>${insights.total_interactions || 0}</strong></p>
                        <p>Positive Feedback: <strong>${insights.positive_feedback || 0}</strong></p>
                        <p>Satisfaction Rate: <strong>${(insights.satisfaction_rate || 0).toFixed(1)}%</strong></p>
                    </div>
                    
                    <div class="insight-card">
                        <h4>🧠 Learning Progress</h4>
                        <p>Learning Rate: <strong>${(insights.learning_rate || 0).toFixed(1)}%</strong></p>
                        <p>Patterns Identified: <strong>${insights.conversation_patterns || 0}</strong></p>
                        <p>Successful Responses: <strong>${insights.successful_responses || 0}</strong></p>
                    </div>
                    
                    <div class="insight-card">
                        <h4>⚡ Performance</h4>
                        <p>Avg Response Time: <strong>${this.performanceMetrics.averageResponseTime.toFixed(2)}s</strong></p>
                        <p>Tokens/Second: <strong>${this.performanceMetrics.tokensPerSecond.toFixed(1)}</strong></p>
                        <p>Total Messages: <strong>${this.performanceMetrics.totalMessages}</strong></p>
                    </div>
                </div>
                
                <div class="learning-tips">
                    <h4>💡 Learning Tips</h4>
                    <ul>
                        <li>Provide feedback using 👍 👎 ⭐ buttons to help me improve</li>
                        <li>I learn from conversation patterns and adapt to your preferences</li>
                        <li>The more we interact, the better I become at understanding you</li>
                        <li>I remember context within conversations for better responses</li>
                    </ul>
                </div>
            </div>
        `;
    }

    createModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
            </div>
        `;
        
        // Close on overlay click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        return modal;
    }

    switchTab(tabName) {
        // Remove active class from all tabs and nav items
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active class to selected tab and nav item
        const targetTab = document.getElementById(`${tabName}-tab`);
        const targetNav = document.querySelector(`[data-tab="${tabName}"]`);
        
        if (targetTab) targetTab.classList.add('active');
        if (targetNav) targetNav.classList.add('active');
        
        this.activeTab = tabName;
        
        // Load tab-specific content
        this.loadTabContent(tabName);
    }

    async loadTabContent(tabName) {
        switch (tabName) {
            case 'chat':
                // Chat is always loaded
                break;
            case 'files':
                await this.loadFilesTab();
                break;
            case 'browser':
                await this.loadBrowserTab();
                break;
            case 'research':
                await this.loadResearchTab();
                break;
            case 'plugins':
                await this.loadPluginsTab();
                break;
            case 'settings':
                await this.loadSettingsTab();
                break;
        }
    }

    async loadFilesTab() {
        try {
            const response = await fetch('/api/files');
            const result = await response.json();
            
            const filesContainer = document.getElementById('files-container');
            if (filesContainer && result.files) {
                this.displayFiles(result.files);
            }
        } catch (error) {
            console.error('Failed to load files:', error);
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        const container = document.getElementById('notifications-container') || document.body;
        container.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
        
        // Add to notifications array
        this.notifications.push({
            message,
            type,
            timestamp: new Date()
        });
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }

    handleTypingIndicator() {
        // Could add typing indicator to other users in future
    }

    startPeriodicUpdates() {
        // Update system status every 30 seconds
        setInterval(() => {
            this.updateSystemStatus();
        }, 30000);
        
        // Update learning data every 60 seconds
        setInterval(() => {
            this.loadLearningData();
        }, 60000);
    }

    initializeAdvancedFeatures() {
        // Initialize keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        // Initialize drag and drop
        this.setupDragAndDrop();
        
        // Initialize context menus
        this.setupContextMenus();
    }

    setupKeyboardShortcuts() {
        // Already implemented in setupAdvancedUIListeners
    }

    setupDragAndDrop() {
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.addEventListener('dragover', (e) => {
                e.preventDefault();
                chatMessages.classList.add('drag-over');
            });
            
            chatMessages.addEventListener('dragleave', () => {
                chatMessages.classList.remove('drag-over');
            });
            
            chatMessages.addEventListener('drop', (e) => {
                e.preventDefault();
                chatMessages.classList.remove('drag-over');
                this.handleFileUpload(e.dataTransfer.files);
            });
        }
    }

    setupContextMenus() {
        document.addEventListener('contextmenu', (e) => {
            if (e.target.closest('.message')) {
                e.preventDefault();
                this.showMessageContextMenu(e, e.target.closest('.message'));
            }
        });
    }

    showMessageContextMenu(event, messageElement) {
        // Implementation for message context menu
        console.log('Context menu for message:', messageElement);
    }

    async handleFileUpload(files) {
        // Implementation for file upload
        console.log('File upload:', files);
        this.showNotification('📁 File upload feature coming soon!', 'info');
    }

    async navigateBrowser() {
        const urlInput = document.getElementById('url-input');
        const url = urlInput?.value.trim();
        
        if (!url) {
            this.showNotification('Please enter a URL', 'warning');
            return;
        }
        
        try {
            const response = await fetch('/api/browser/navigate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showNotification('🌐 Navigation successful', 'success');
            } else {
                this.showNotification('❌ Navigation failed', 'error');
            }
            
        } catch (error) {
            console.error('Browser navigation failed:', error);
            this.showNotification('❌ Navigation failed', 'error');
        }
    }

    clearChat() {
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            messagesContainer.innerHTML = this.getWelcomeMessage();
        }
        
        // Clear current chat history
        this.chatHistory.set(this.currentChatId, []);
        
        this.showNotification('🗑️ Chat cleared', 'success');
    }

    async updateChatHistory() {
        // Save current chat to backend
        try {
            const messages = this.chatHistory.get(this.currentChatId) || [];
            // Implementation to save chat history
        } catch (error) {
            console.error('Failed to update chat history:', error);
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.juggernautAI = new JuggernautAI();
});

// Export for global access
window.JuggernautAI = JuggernautAI;

