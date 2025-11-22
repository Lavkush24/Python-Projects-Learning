#!/usr/bin/env python3
"""
Course Data Validator - Launcher Script
Simple script to run the main application
"""

import sys
import os

def main():
    """Main launcher function"""
    try:
        # Import and run the main application
        from main import main as run_app
        run_app()
    except ImportError as e:
        print(f"Error: Could not import required modules. {e}")
        print("Please make sure all required packages are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
