#!/bin/bash

# Quick Demo Script for RealityCheck
# Demonstrates both frontend and backend capabilities

echo "🚀 RealityCheck Quick Demo"
echo "=========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "main_new.py" ]; then
    print_error "Please run this script from the RealityCheck root directory"
    exit 1
fi

echo "🎯 Demo Options:"
echo "1. Backend Demo (API testing)"
echo "2. Frontend Demo (UI showcase)"
echo "3. Integration Demo (Full system)"
echo "4. Quick Start (Start both servers)"
echo ""

read -p "Select demo option (1-4): " choice

case $choice in
    1)
        print_info "Starting Backend Demo..."
        echo ""
        print_info "Make sure backend is running: python main_new.py"
        echo ""
        read -p "Press Enter when backend is running..."
        python demo_backend.py
        ;;
    2)
        print_info "Starting Frontend Demo..."
        echo ""
        print_info "Frontend will be available at: http://localhost:3000/demo"
        echo ""
        print_info "Starting frontend server..."
        cd frontend
        npm run dev &
        FRONTEND_PID=$!
        cd ..
        print_status "Frontend started! Visit http://localhost:3000/demo"
        echo ""
        print_info "Press Ctrl+C to stop frontend server"
        wait $FRONTEND_PID
        ;;
    3)
        print_info "Starting Integration Demo..."
        echo ""
        print_info "Make sure both frontend and backend are running:"
        print_info "Backend: python main_new.py"
        print_info "Frontend: cd frontend && npm run dev"
        echo ""
        read -p "Press Enter when both servers are running..."
        python demo_integration.py
        ;;
    4)
        print_info "Starting Quick Start..."
        echo ""
        print_info "This will start both frontend and backend servers"
        echo ""
        read -p "Press Enter to continue..."
        ./start_dev.sh
        ;;
    *)
        print_error "Invalid option. Please select 1-4"
        exit 1
        ;;
esac

print_status "Demo completed!"
echo ""
print_info "For more detailed demos, see:"
print_info "- Backend: python demo_backend.py"
print_info "- Frontend: http://localhost:3000/demo"
print_info "- Integration: python demo_integration.py"
print_info "- Documentation: DEMO_GUIDE.md"
