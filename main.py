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
    if len(sys.argv) == 1:
        # Interactive mode
        cli.run_single_plant_mode()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        # Check if it's a file (ends with .txt) or a plant name
        if arg.endswith('.txt') or '/' in arg or '\\' in arg:
            cli.run_batch_mode(arg)
        else:
            # Single plant mode
            cli.display_header()
            cli.display_weather()
            cli.process_single_plant(arg)
    else:
        print("Usage: python main.py [plant_name|file.txt]")
        sys.exit(1)


if __name__ == "__main__":
    main()
