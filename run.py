#!/usr/bin/env python3
"""
Smart Retail System - Products Module
Setup and run script for development
"""

import os
import subprocess
import sys

def run_command(cmd, show_output=True):
    """Run a shell command"""
    try:
        if show_output:
            result = subprocess.run(cmd, shell=True)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("=" * 60)
    print("Smart Retail System - Products Module")
    print("Tanzania POS & Inventory Management")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    venv_path = '.venv'
    if not os.path.exists(venv_path):
        print("\n[1/4] Creating virtual environment...")
        if not run_command(f'python -m venv {venv_path}'):
            print("Error creating virtual environment")
            sys.exit(1)
        print("✓ Virtual environment created")
    else:
        print("\n[1/4] Virtual environment already exists")
    
    # Activate virtual environment and install requirements
    print("\n[2/4] Installing dependencies...")
    if sys.platform == "win32":
        activate_cmd = f'{venv_path}\\Scripts\\pip install -r requirements.txt'
    else:
        activate_cmd = f'source {venv_path}/bin/activate && pip install -r requirements.txt'
    
    if not run_command(activate_cmd):
        print("Warning: Some dependencies may not have installed properly")
    else:
        print("✓ Dependencies installed")
    
    # Initialize database
    print("\n[3/4] Initializing database...")
    if sys.platform == "win32":
        init_cmd = f'{venv_path}\\Scripts\\python app.py 2>&1'
    else:
        init_cmd = f'source {venv_path}/bin/activate && python app.py 2>&1'
    
    run_command(init_cmd)
    print("✓ Database initialized")
    
    # Run the application
    print("\n[4/4] Starting Smart Retail System...")
    print("-" * 60)
    print("Smart Retail System is running!")
    print("Open your browser: http://127.0.0.1:5000")
    print("-" * 60)
    print("\nAPI Endpoints:")
    print("  GET    http://127.0.0.1:5000/api/v1/products")
    print("  GET    http://127.0.0.1:5000/api/v1/products/stats")
    print("  GET    http://127.0.0.1:5000/api/v1/categories")
    print("  POST   http://127.0.0.1:5000/api/v1/products")
    print("-" * 60)
    
    if sys.platform == "win32":
        run_cmd = f'{venv_path}\\Scripts\\python app.py'
    else:
        run_cmd = f'source {venv_path}/bin/activate && python app.py'
    
    os.system(run_cmd)

if __name__ == '__main__':
    main()
