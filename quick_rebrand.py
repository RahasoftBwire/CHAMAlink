"""
Quick rebranding script for Bwire Finance Cloud
This will update all text references in Python and HTML files
"""

import os
import glob

# Define text replacements
replacements = {
    'Bwire Finance Cloud': 'Bwire Finance Cloud',
    'Bwire Finance Cloud': 'Bwire Finance Cloud',
    'Bwire Finance Cloud': 'Bwire Finance Cloud',
    'bwirefinance': 'bwirefinance',
    'BWIRE FINANCE CLOUD': 'BWIRE FINANCE CLOUD',
    'bwirefinance.com': 'bwirefinance.cloud',
    'bwirefinance.co.ke': 'bwirefinance.cloud',
    '@bwirefinance': '@bwirefinance',
}

def process_file(filepath):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        pass
    return False

# Process all HTML and Python files
count = 0
for pattern in ['**/*.html', '**/*.py', '**/*.md', '**/*.txt']:
    for filepath in glob.glob(pattern, recursive=True):
        if 'venv' not in filepath and '__pycache__' not in filepath and '.git' not in filepath and 'migrations' not in filepath:
            if process_file(filepath):
                count += 1

print(f"Rebranding complete! Updated {count} files")
print("Welcome to Bwire Finance Cloud!")
