#!/usr/bin/env python
"""
Quick Setup Script for Career Dashboard
Automates the setup process
"""

import os
import subprocess
import sys
import platform

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step_num, text):
    """Print step indicator"""
    print(f"[Step {step_num}] {text}")

def check_python_version():
    """Check if Python version is 3.8+"""
    print_step(1, "Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ ERROR: Python 3.8+ required. You have {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor} detected\n")
    return True

def check_requirements_file():
    """Check if requirements.txt exists"""
    print_step(2, "Locating requirements.txt...")
    
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt found\n")
        return True
    else:
        print("❌ ERROR: requirements.txt not found")
        print("Make sure you're in the correct directory")
        return False

def install_dependencies():
    """Install required packages"""
    print_step(3, "Installing dependencies...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully\n")
        return True
    except subprocess.CalledProcessError:
        print("❌ ERROR: Failed to install dependencies")
        print("Try running: pip install -r requirements.txt")
        return False

def check_data_file():
    """Check if data file exists"""
    print_step(4, "Checking for SGJobData.csv...")
    
    if os.path.exists('SGJobData.csv'):
        file_size = os.path.getsize('SGJobData.csv') / (1024*1024)  # Convert to MB
        print(f"✅ SGJobData.csv found ({file_size:.1f} MB)\n")
        return True
    else:
        print("❌ ERROR: SGJobData.csv not found")
        print("Please place SGJobData.csv in the same directory as this script")
        return False

def verify_imports():
    """Verify all imports work"""
    print_step(5, "Verifying imports...")
    
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ All imports working correctly\n")
        return True
    except ImportError as e:
        print(f"❌ ERROR: Import failed - {e}")
        return False

def suggest_next_steps():
    """Print next steps"""
    print_header("Setup Complete! 🎉")
    
    print("Next steps:")
    print("1. Run the dashboard: streamlit run dashboard.py")
    print("2. Dashboard will open in your browser (usually http://localhost:8501)")
    print("3. Start with Home & Overview to understand the market")
    print("4. Select your user type (Mid-Career Professional or Career Switcher)")
    print("5. Read the Usage Guide for detailed walkthroughs")
    print("\nTroubleshooting:")
    print("- If dashboard doesn't load, check that SGJobData.csv is in the right directory")
    print("- First load may take 1-2 minutes while data is being cached")
    print("- Clear cache with: rm -rf .streamlit/cache (or delete folder on Windows)")

def check_windows_requirements():
    """Additional checks for Windows"""
    if platform.system() == "Windows":
        print("\n[Windows Setup] Additional checks...")
        # Windows specific checks can go here
        print("✅ Windows environment detected")

def main():
    """Run setup process"""
    print_header("Career Dashboard Setup")
    
    print("This script will help you set up the Career Path & Skills Gap Analyzer")
    print("It will:")
    print("  • Check Python version")
    print("  • Install required packages")
    print("  • Verify data files")
    print("  • Test imports")
    print()
    
    # Run checks
    checks = [
        check_python_version,
        check_requirements_file,
        install_dependencies,
        check_data_file,
        verify_imports
    ]
    
    for check in checks:
        if not check():
            print_header("Setup Failed ❌")
            print("Please fix the error above and try again")
            sys.exit(1)
    
    # Platform specific checks
    check_windows_requirements()
    
    # Success
    suggest_next_steps()
    
    print_header("Ready to Go! 🚀")
    print("Type this command to start:")
    print("  streamlit run dashboard.py")
    print()

if __name__ == "__main__":
    main()
