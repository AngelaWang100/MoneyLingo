#!/bin/bash

# RealityCheck Development Startup Script
# Starts both backend and frontend servers

# Set up PATH to include Homebrew and other common locations
export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"

echo "🚀 Starting RealityCheck Development Environment"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "main_new.py" ]; then
    echo "❌ Error: Please run this script from the RealityCheck root directory"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Error: Frontend directory not found. Please clone the frontend repository first:"
    echo "git clone https://github.com/aivil0/moneylingo.git frontend"
    exit 1
fi

# Function to kill background processes on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "📦 Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

echo "🐍 Starting backend server on port 8001..."
python3 main_new.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "⚛️  Starting frontend server on port 3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Development servers started!"
echo "================================================"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user to stop
wait
