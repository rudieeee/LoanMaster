let ws = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAY = 1000;
const client_id = Math.random().toString(36).substring(7);

// WebSocket setup
function setupWebSocket() {
    if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) {
        console.log('WebSocket connection already exists');
        return;
    }

    ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
    
    ws.onopen = function() {
        console.log('Connected to LoanMaster AI');
        reconnectAttempts = 0;
        updateConnectionStatus(true);
    };

    ws.onmessage = function(event) {
        const response = JSON.parse(event.data);
        displayMessage(response.message, 'ai');
    };

    ws.onclose = function() {
        updateConnectionStatus(false);

        if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            console.log(`WebSocket closed. Attempting to reconnect (${reconnectAttempts + 1}/${MAX_RECONNECT_ATTEMPTS})...`);
            reconnectAttempts++;
            setTimeout(setupWebSocket, RECONNECT_DELAY);
        } else {
            console.log('Maximum reconnection attempts reached. Please refresh the page.');
            displayMessage('Connection lost. Please refresh the page to reconnect.', 'ai');
        }
    };

    ws.onerror = function(error) {
        console.error('WebSocket error:', error);
        updateConnectionStatus(false);
    };
}

function updateConnectionStatus(isConnected) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');
    
    if (statusDot && statusText) {
        if (isConnected) {
            statusDot.style.backgroundColor = '#4CAF50';
            statusText.textContent = 'Online';
        } else {
            statusDot.style.backgroundColor = '#ff4444';
            statusText.textContent = 'Offline';
        }
    }
}

// Document upload toggle
function toggleDocUpload() {
    const docSection = document.getElementById('docUpload');
    if (!docSection) return;
    
    const currentDisplay = window.getComputedStyle(docSection).display;
    docSection.style.display = currentDisplay === 'none' ? 'flex' : 'none';
}

// File upload handling
function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    if (!uploadArea || !fileInput) return;

    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.backgroundColor = '#f8f9fa';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.backgroundColor = 'white';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.backgroundColor = 'white';
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

function handleFiles(files) {
    const uploadedFilesDiv = document.getElementById('uploadedFiles');
    
    Array.from(files).forEach(file => {
        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert(`File ${file.name} is too large. Maximum size is 10MB.`);
            return;
        }
        
        // Validate file type
        const validTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            alert(`File ${file.name} is not a supported format. Please upload PDF, JPG, or PNG files.`);
            return;
        }
        
        // Add file to uploaded files list
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <i class="fas fa-file-${file.type.includes('pdf') ? 'pdf' : 'image'}"></i>
            <span>${file.name}</span>
            <span class="file-size">${(file.size / 1024).toFixed(2)} KB</span>
        `;
        uploadedFilesDiv.appendChild(fileItem);
        
        // Send message about the upload
        displayMessage(`📎 Uploaded: ${file.name}`, 'user');
        
        // Simulate AI response
        setTimeout(() => {
            displayMessage(`I've received your document "${file.name}". I'll process it and let you know if I need any additional information.`, 'ai');
        }, 1000);
    });
}

// Message display with typing animation
function displayMessage(message, sender) {
    const messagesDiv = document.getElementById('messages');
    if (!messagesDiv) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'ai' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    if (sender === 'ai') {
        // Show typing indicator
        showTypingIndicator();
        
        setTimeout(() => {
            removeTypingIndicator();
            
            // Simulate typing animation
            let i = 0;
            const speed = 20;
            
            const typeWriter = () => {
                if (i < message.length) {
                    bubble.innerHTML = message.substring(0, i + 1).replace(/\n/g, '<br>');
                    i++;
                    setTimeout(typeWriter, speed);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
            };
            
            typeWriter();
        }, 800);
    } else {
        bubble.textContent = message;
    }
    
    content.appendChild(bubble);
    content.appendChild(time);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesDiv.appendChild(messageDiv);
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message ai-message';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="typing-animation">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Send message
function sendMessage() {
    const input = document.getElementById('messageInput');
    if (!input) return;

    const message = input.value.trim();
    
    if (message && ws && ws.readyState === WebSocket.OPEN) {
        displayMessage(message, 'user');
        ws.send(JSON.stringify({
            message: message,
            customer_id: null
        }));
        input.value = '';
    } else if (!ws || ws.readyState !== WebSocket.OPEN) {
        alert('Connection lost. Please wait while we reconnect...');
    }
}

function sendQuickMessage(message) {
    const input = document.getElementById('messageInput');
    if (input) {
        input.value = message;
        sendMessage();
    }
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = `
            <div class="message ai-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        Chat history cleared. How can I help you today?
                    </div>
                    <div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            </div>
        `;
    }
}

// Download chat
function downloadChat() {
    const messages = document.querySelectorAll('.message');
    let chatText = 'LoanMaster Chat Transcript\n';
    chatText += '=' .repeat(50) + '\n\n';
    
    messages.forEach(msg => {
        const sender = msg.classList.contains('ai-message') ? 'Sarah (AI)' : 'You';
        const bubble = msg.querySelector('.message-bubble');
        const time = msg.querySelector('.message-time');
        
        if (bubble && time) {
            chatText += `[${time.textContent}] ${sender}:\n${bubble.textContent}\n\n`;
        }
    });
    
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `loanmaster-chat-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Toggle settings
function toggleSettings() {
    alert('Settings feature coming soon!');
}

// Toggle emoji picker
function toggleEmojiPicker() {
    alert('Emoji picker coming soon!');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chat page loaded, initializing...');
    
    setupWebSocket();
    setupFileUpload();
    
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    
    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        messageInput.focus();
    }
    
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    // Handle page visibility
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                setupWebSocket();
            }
        }
    });
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.close();
        }
    });
});

// Add CSS for typing animation
const style = document.createElement('style');
style.textContent = `
    .typing-animation {
        display: flex;
        gap: 4px;
        padding: 5px 0;
    }
    
    .typing-animation span {
        width: 8px;
        height: 8px;
        background: var(--primary-color);
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-animation span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-animation span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    .file-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin-top: 0.8rem;
    }
    
    .file-item i {
        font-size: 1.5rem;
        color: var(--primary-color);
    }
    
    .file-size {
        margin-left: auto;
        color: #999;
        font-size: 0.85rem;
    }
`;
document.head.appendChild(style);
