#!/usr/bin/env python3
"""
Garden Manager - Main entry point

Usage:
    python main.py                  # Interactive mode
    python main.py tomato           # Single plant mode
    python main.py plants.txt       # Batch file mode
"""

import sys
from garden_manager.cli import CommandLine


def main():
    """Main entry point"""
    cli = CommandLine()
    
    # Parse arguments (skip script name)
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    
    cli.run(args)


if __name__ == "__main__":
    main()
