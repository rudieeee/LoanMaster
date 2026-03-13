let ws = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAY = 1000;
const client_id = Math.random().toString(36).substring(7);

// Websocket setup
function setupWebSocket() {
    if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) {
        console.log('WebSocket connection already exists');
        return;
    }

    ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
    
    ws.onopen = function() {
        console.log('Connected to LoanMaster AI');
        reconnectAttempts = 0; // Reset reconnect attempts on successful connection
        const statusDot = document.querySelector('.status-dot');
        if (statusDot) {
            statusDot.style.backgroundColor = '#4CAF50'; // Green when connected
        }
    };

    ws.onmessage = function(event) {
        const response = JSON.parse(event.data);
        displayMessage(response.message, 'ai');
    };

    ws.onclose = function() {
        const statusDot = document.querySelector('.status-dot');
        if (statusDot) {
            statusDot.style.backgroundColor = '#ff4444'; // Red when disconnected
        }

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
        const statusDot = document.querySelector('.status-dot');
        if (statusDot) {
            statusDot.style.backgroundColor = '#ff4444'; // Red on error
        }
    };
}

// Chat visibility toggle
function toggleChat() {
    const chat = document.getElementById('chat');
    if (!chat) {
        console.error('Chat element not found');
        return;
    }
    
    const currentDisplay = window.getComputedStyle(chat).display;
    const willShow = currentDisplay === 'none';
    chat.style.display = willShow ? 'flex' : 'none';
    
    if (willShow) {
        // Ensure WebSocket connection when showing chat
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            setupWebSocket();
        }
        
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.focus();
        }
    } else {
        // Optionally close WebSocket when hiding chat
        // Uncomment the following lines if you want to close connection when chat is hidden
        /*if (ws && ws.readyState === WebSocket.OPEN) {
            ws.close();
        }*/
    }
}

// Document upload section toggle
function toggleDocUpload() {
    const docSection = document.getElementById('docUpload');
    if (!docSection) {
        console.error('Document upload section not found');
        return;
    }
    const currentDisplay = window.getComputedStyle(docSection).display;
    docSection.style.display = currentDisplay === 'none' ? 'block' : 'none';
}

// Handle file uploads
function setupFileUpload() {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('fileInput');
    
    if (!uploadArea || !fileInput) {
        console.error('File upload elements not found');
        return;
    }

    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#ddd';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ddd';
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

function handleFiles(files) {
    Array.from(files).forEach(file => {
        displayMessage(`📎 Uploaded: ${file.name}`, 'user');
    });
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('messages');
    if (!messagesDiv) return;

    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message typing-indicator';
    typingDiv.id = 'typing';
    
    typingDiv.innerHTML = `
        <div class="message-bubble">
            <div class="typing-dots">
                <span>●</span><span>●</span><span>●</span>
            </div>
        </div>
    `;
    
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Message display with typing animation
function displayMessage(message, sender) {
    removeTypingIndicator();
    
    const messagesDiv = document.getElementById('messages');
    if (!messagesDiv) {
        console.error('Messages container not found');
        return;
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    if (sender === 'ai') {
        // Show typing indicator before message
        showTypingIndicator();
        
        // Simulate typing for AI messages
        setTimeout(() => {
            removeTypingIndicator();
            
            let i = 0;
            const speed = 30; // typing speed in milliseconds
            
            const typeWriter = () => {
                if (i < message.length) {
                    bubble.innerHTML = message.substring(0, i + 1);
                    i++;
                    setTimeout(typeWriter, speed);
                }
            };
            
            typeWriter();
        }, 500);
    } else {
        bubble.textContent = message;
    }
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(time);
    messagesDiv.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    if (!input) {
        console.error('Message input not found');
        return;
    }

    const message = input.value.trim();
    
    if (message && ws && ws.readyState === WebSocket.OPEN) {
        displayMessage(message, 'user');
        ws.send(JSON.stringify({
            message: message,
            customer_id: null
        }));
        input.value = '';
    }
}

function sendQuickMessage(message) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        displayMessage(message, 'user');
        ws.send(JSON.stringify({
            message: message,
            customer_id: null
        }));
    }
}

// Initialize everything when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Document loaded, initializing chat...');
    
    // Setup file upload first
    setupFileUpload();
    
    // Initialize chat visibility before WebSocket connection
    const chat = document.getElementById('chat');
    if (chat) {
        chat.style.display = 'none';
    }
    
    // Setup event listeners
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatToggleBtn = document.querySelector('.chat-toggle-btn');
    
    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); // Prevent default to avoid newline
                sendMessage();
            }
        });
        
        // Add input event to handle message length
        messageInput.addEventListener('input', function() {
            const maxLength = 500; // Maximum message length
            if (this.value.length > maxLength) {
                this.value = this.value.substring(0, maxLength);
            }
        });
    }
    
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (chatToggleBtn) {
        chatToggleBtn.addEventListener('click', toggleChat);
    }
    
    // Handle visibility changes
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            // Reconnect WebSocket if needed when page becomes visible
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                setupWebSocket();
            }
        }
    });
    
    // Handle before unload
    window.addEventListener('beforeunload', () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.close();
        }
    });
});

function sendQuickMessage(message) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = message;
    chat.sendMessage();
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chat = new LoanMasterChat();
});
