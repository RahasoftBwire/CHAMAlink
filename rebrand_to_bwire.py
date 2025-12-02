"""
Script to rebrand Bwire Finance Cloud to Bwire Finance Cloud
This will update all references across the codebase
"""

import os
import re
from pathlib import Path

# Define replacements
REPLACEMENTS = {
    'Bwire Finance Cloud': 'Bwire Finance Cloud',
    'Bwire Finance Cloud': 'Bwire Finance Cloud',
    'Bwire Finance Cloud': 'Bwire Finance Cloud',
    'bwirefinance': 'bwirefinance',
    'BWIRE FINANCE CLOUD': 'BWIRE FINANCE CLOUD',
}

# Email and domain replacements
EMAIL_REPLACEMENTS = {
    'bwirefinance.com': 'bwirefinance.cloud',
    'bwirefinance.co.ke': 'bwirefinance.cloud',
    '@bwirefinance': '@bwirefinance',
}

# Database name replacements
DB_REPLACEMENTS = {
    'bwirefinance.db': 'bwirefinance.db',
}

# File extensions to process
EXTENSIONS = ['.py', '.html', '.js', '.css', '.md', '.txt', '.yml', '.yaml', '.json', '.sh']

# Directories to skip
SKIP_DIRS = {'venv', 'env', '.git', '__pycache__', 'node_modules', '.vscode', 'migrations'}

def should_process_file(file_path):
    """Check if file should be processed"""
    if any(skip_dir in file_path.parts for skip_dir in SKIP_DIRS):
        return False
    return file_path.suffix in EXTENSIONS

def rebrand_file(file_path):
    """Rebrand a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply text replacements
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # Apply email replacements
        for old, new in EMAIL_REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # Apply database replacements
        for old, new in DB_REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main rebranding function"""
    root_dir = Path(__file__).parent
    files_updated = 0
    files_scanned = 0
    
    print("🔄 Starting Bwire Finance Cloud Rebranding...")
    print(f"📁 Scanning directory: {root_dir}")
    print("-" * 60)
    
    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and should_process_file(file_path):
            files_scanned += 1
            if rebrand_file(file_path):
                files_updated += 1
                print(f"✅ Updated: {file_path.relative_to(root_dir)}")
    
    print("-" * 60)
    print(f"📊 Rebranding Complete!")
    print(f"   Files scanned: {files_scanned}")
    print(f"   Files updated: {files_updated}")
    print("")
    print("🎉 Welcome to Bwire Finance Cloud!")
    print("   - Modern financial ecosystem")
    print("   - Powered by Bwire Global Tech")
    print("   - Ready for regional and global deployment")

if __name__ == '__main__':
    main()
