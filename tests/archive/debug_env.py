"""
Debug environment variable loading
"""
import os
import sys
from dotenv import load_dotenv

def debug_environment():
    """Debug environment variable loading"""
    print("🔍 Debugging environment variables...")
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env file exists")
        
        # Read the file to see what's in it (without showing sensitive data)
        try:
            with open(env_file, 'r') as f:
                lines = f.readlines()
            print(f"📄 .env file has {len(lines)} lines")
            
            # Check for placeholder values
            placeholder_lines = [line for line in lines if "your_" in line and "=" in line]
            if placeholder_lines:
                print(f"⚠️  Found {len(placeholder_lines)} placeholder values:")
                for line in placeholder_lines[:3]:  # Show first 3
                    key = line.split('=')[0].strip()
                    print(f"   - {key}: still using placeholder")
            else:
                print("✅ No placeholder values found")
                
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    else:
        print(f"❌ .env file does not exist")
        print("💡 Create it with: cp env.example .env")
        return False
    
    # Load environment variables
    print("\n🔄 Loading environment variables...")
    load_dotenv()
    
    # Check specific variables
    test_vars = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY"),
        "COMET_API_KEY": os.getenv("COMET_API_KEY"),
        "ECHO_API_KEY": os.getenv("ECHO_API_KEY"),
    }
    
    print("\n📋 Environment Variables:")
    for var_name, var_value in test_vars.items():
        if var_value:
            if var_value.startswith("your_") or var_value.endswith("_here"):
                print(f"❌ {var_name}: Using placeholder value")
            else:
                # Show partial value for security
                masked_value = var_value[:8] + "..." + var_value[-4:] if len(var_value) > 12 else "***"
                print(f"✅ {var_name}: {masked_value}")
        else:
            print(f"❌ {var_name}: Not set")
    
    # Check if we have real API keys
    real_keys = [var for var in test_vars.values() 
                 if var and not var.startswith("your_") and not var.endswith("_here")]
    
    print(f"\n🎯 Found {len(real_keys)} real API keys")
    
    if len(real_keys) >= 2:
        print("✅ Sufficient API keys found - agents should work!")
        return True
    else:
        print("❌ Not enough real API keys - agents will fail")
        return False

if __name__ == "__main__":
    debug_environment()
