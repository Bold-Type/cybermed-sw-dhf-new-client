#!/usr/bin/env python3
"""
Main script to create new client workspaces.
Entry point for daily workspace creation operations.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cli import main

if __name__ == "__main__":
    main()
