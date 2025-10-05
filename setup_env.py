"""
Setup script to help create .env file with Echo API keys
"""
import os

def create_env_file():
    """Create .env file with Echo API configuration"""
    
    print("🔑 Echo AI SDK Environment Setup")
    print("=" * 50)
    print()
    print("To complete the Echo AI integration, you need to:")
    print()
    print("1. Sign up for Echo AI SDK at: https://merit.systems/echo")
    print("2. Get your API credentials from the Echo dashboard")
    print("3. Create a .env file with your actual API keys")
    print()
    print("Required Echo API Keys:")
    print("- ECHO_API_KEY: Your main Echo API key")
    print("- ECHO_CLIENT_ID: Your Echo client ID")
    print("- ECHO_CLIENT_SECRET: Your Echo client secret")
    print("- ECHO_MERCHANT_ID: Your Echo merchant ID")
    print()
    print("Example .env file content:")
    print("-" * 30)
    print("# API Keys")
    print("GOOGLE_API_KEY=AIzaSyBgwX8QZQZQZQZQZQZQZQZQZQZQZQZQZQZQ")
    print("COMET_API_KEY=your_comet_api_key_here")
    print("COMET_WORKSPACE=mihir-agarwal")
    print("ELEVENLABS_API_KEY=sk_eb8f1fa7a20cfa5ee17ebedd0a6eeb81144c6c032dd887aa")
    print()
    print("# Echo AI SDK (Merit Systems)")
    print("ECHO_API_KEY=your_actual_echo_api_key_here")
    print("ECHO_ENVIRONMENT=development")
    print("ECHO_CLIENT_ID=your_actual_echo_client_id_here")
    print("ECHO_CLIENT_SECRET=your_actual_echo_client_secret_here")
    print("ECHO_MERCHANT_ID=your_actual_echo_merchant_id_here")
    print()
    print("Once you have your Echo API keys:")
    print("1. Create a .env file in your project root")
    print("2. Copy the content above and replace with your actual keys")
    print("3. Run: python3 test_monetization.py")
    print()
    print("🎉 Your RealityCheck system will be ready for Echo AI monetization!")

if __name__ == "__main__":
    create_env_file()
