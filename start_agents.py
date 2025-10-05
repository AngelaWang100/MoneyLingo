#!/usr/bin/env python3
"""
Startup script for RealityCheck Agent System
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        "GOOGLE_API_KEY",
        "COMET_API_KEY", 
        "COMET_WORKSPACE"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.info("Please set these in your .env file or environment")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        logger.info("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def start_agent_system():
    """Start the agent system"""
    try:
        logger.info("Starting RealityCheck Agent System...")
        
        # Check if we should run in demo mode
        if len(sys.argv) > 1 and sys.argv[1] == "demo":
            logger.info("Running in demo mode...")
            subprocess.run([sys.executable, "demo/test_agents.py"], check=True)
        else:
            # Start the FastAPI server
            logger.info("Starting FastAPI server on port 8001...")
            subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"], 
                          check=True)
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start agent system: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("Agent system stopped by user")
        return True

def main():
    """Main startup function"""
    logger.info("RealityCheck Agent System Startup")
    logger.info("=" * 40)
    
    # Check environment
    if not check_environment():
        logger.error("Environment check failed. Please set required variables.")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Dependency installation failed.")
        return 1
    
    # Start the system
    if not start_agent_system():
        logger.error("Failed to start agent system.")
        return 1
    
    logger.info("Agent system started successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
