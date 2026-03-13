#!/bin/bash

# LoanMaster Enhanced Chatbot - Quick Start Script
# This script starts the backend server with the conversational AI

echo "🚀 Starting LoanMaster Enhanced Chatbot Server..."
echo ""

# Add Python user bin to PATH
export PATH="/Users/rudrayadav/Library/Python/3.13/bin:$PATH"

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Start the server
echo "✅ Server starting on http://localhost:8000"
echo "📱 Access the chat at: http://localhost:8000/frontend/chat.html"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python3 main.py
