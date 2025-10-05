"""
Script to move old test files to archive
"""
import os
import shutil

def move_old_tests():
    """Move old test files to archive folder"""
    
    # Create archive directory
    archive_dir = "tests/archive"
    os.makedirs(archive_dir, exist_ok=True)
    
    # List of old test files to move
    old_test_files = [
        "test_agent_instantiation.py",
        "test_agent_outputs.py", 
        "test_agents_simple.py",
        "test_agents_with_env.py",
        "test_all_agents.py",
        "test_api_endpoints.py",
        "test_auto_language_voice.py",
        "test_comet_integration.py",
        "test_elevenlabs.py",
        "test_env_loading.py",
        "test_google_api.py",
        "test_individual_agents.py",
        "test_monetization.py",
        "test_new_structure.py",
        "test_orchestrator_fix.py",
        "test_setup.py",
        "test_tavily_output.py",
        "test_translation_agent.py",
        "debug_env.py",
        "simple_test.py"
    ]
    
    moved_files = []
    failed_files = []
    
    for filename in old_test_files:
        if os.path.exists(filename):
            try:
                # Move file to archive
                shutil.move(filename, os.path.join(archive_dir, filename))
                moved_files.append(filename)
                print(f"✅ Moved: {filename}")
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"❌ Failed to move {filename}: {e}")
        else:
            print(f"⚠️  Not found: {filename}")
    
    # Summary
    print(f"\n📊 Archive Summary:")
    print(f"✅ Successfully moved: {len(moved_files)} files")
    print(f"❌ Failed to move: {len(failed_files)} files")
    
    if failed_files:
        print(f"\n❌ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    print(f"\n📁 Old test files archived in: {archive_dir}")
    print(f"🧪 New organized tests in: tests/")
    print(f"🚀 Run new tests with: python tests/run_all_tests.py")

if __name__ == "__main__":
    move_old_tests()
