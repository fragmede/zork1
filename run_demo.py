#!/usr/bin/env python3
"""
Runner script for Zork I Python demo.

This script properly imports and runs the demo from the zork1_python package.
"""

import sys
from pathlib import Path

# Ensure zork1_python is importable
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the demo
from zork1_python.main import demo

if __name__ == "__main__":
    demo()
