#!/usr/bin/env python3
"""
Config File Sherlock - Because finding configs shouldn't be harder than debugging them.
"""

import os
import sys
from pathlib import Path

# The usual suspects - config files that love to play hide and seek
CONFIG_PATTERNS = [
    '.env*',           # Environment files (the shy ones)
    'config*',         # Generic configs (trying to be helpful)
    '*.conf',          # Unix-style (old but reliable)
    '*.cfg',           # Windows-style (trying to fit in)
    '*.yml',           # YAML (because why use JSON?)
    '*.yaml',          # YAML's twin
    '*.json',          # JSON (the sensible one)
    '*.toml',          # TOML (the new kid)
    '*.ini',           # INI (grandpa config)
    'settings*',       # Django's favorite
]

def find_configs(root_dir='.', max_depth=3):
    """
    Hunt down those elusive config files.
    Returns a list of (depth, file_path) tuples.
    """
    found = []
    root = Path(root_dir).resolve()
    
    # Walk the directory tree like a detective on a case
    for dirpath, dirnames, filenames in os.walk(root):
        # Calculate how deep we've gone (for sorting)
        depth = Path(dirpath).relative_to(root).parts
        if len(depth) > max_depth:
            dirnames.clear()  # Don't go deeper than we promised
            continue
        
        for filename in filenames:
            for pattern in CONFIG_PATTERNS:
                # Match patterns with wildcards
                if pattern.startswith('*'):
                    if filename.endswith(pattern[1:]):
                        found.append((len(depth), Path(dirpath) / filename))
                elif pattern.endswith('*'):
                    if filename.startswith(pattern[:-1]):
                        found.append((len(depth), Path(dirpath) / filename))
                elif filename == pattern:
                    found.append((len(depth), Path(dirpath) / filename))
    
    return found

def main():
    """Main investigation routine."""
    if len(sys.argv) > 1:
        search_dir = sys.argv[1]
    else:
        search_dir = '.'
    
    print(f"🔍 Investigating: {search_dir}")
    print("Looking for config files that are definitely not hiding...\n")
    
    try:
        results = find_configs(search_dir)
        
        if not results:
            print("Case closed: No configs found. Are you sure this is a project?")
            return
        
        # Sort by depth (shallow first) then alphabetically
        results.sort(key=lambda x: (x[0], str(x[1])))
        
        print(f"Found {len(results)} suspicious files:\n")
        for depth, filepath in results:
            indent = '  ' * depth
            rel_path = filepath.relative_to(Path(search_dir).resolve())
            print(f"{indent}📄 {rel_path}")
            
    except Exception as e:
        print(f"Investigation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
