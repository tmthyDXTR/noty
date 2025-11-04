# Noty - Simple Command Line Note Taking Tool

A lightweight command line tool for taking quick notes with timestamps.

## Features

- Add notes with simple commands
- List all notes with human-readable timestamps and IDs
- Remove notes by ID (using either 'remove' or 'rm' command)
- Clear all notes with safety confirmation
- Export notes to human-readable text files
- Fix duplicate IDs (maintenance command)
- ASCII-formatted list display with clean visual layout
- Automatic timestamps in human-readable format
- Persistent storage using JSON
- Lightweight and fast
- Cross-platform: Works on Linux, macOS, and Windows

## Usage

### Add a note
```bash
# Linux/macOS
./noty "Your note text here"    # Shorthand
./noty -a "Your note text here"  # With flag

# Windows
noty.bat "Your note text here"
noty.bat -a "Your note text here"
```

### List all notes
```bash
# Linux/macOS
./noty -l

# Windows  
noty.bat -l
```

### Remove a note
```bash
# Linux/macOS
./noty -r 1

# Windows
noty.bat -r 1
```

### Export notes
```bash
# Linux/macOS
./noty -e                        # Auto-generated filename
./noty -e my_backup.txt          # Custom filename

# Windows
noty.bat -e
noty.bat -e my_backup.txt
```

### Get help
```bash
# Linux/macOS
./noty -h

# Windows
noty.bat -h
```

### Clear all notes
```bash
# Linux/macOS
./noty -c

# Windows
noty.bat -c
```

## Installation

### Linux/macOS
To make `noty` available from anywhere on your system:

1. Add the noty directory to your PATH, or
2. Create a symlink in a directory that's already in your PATH:

```bash
# Option 1: Add to PATH (add this to your ~/.bashrc or ~/.zshrc)
export PATH="$PATH:/path/to/noty"

# Option 2: Create symlink (replace /usr/local/bin with any directory in your PATH)
sudo ln -s /path/to/noty /usr/local/bin/noty
```

After installation, you can use `noty` from anywhere:
```bash
noty add "This works from anywhere!"
noty list
```

### Windows
1. Add the noty directory to your PATH environment variable
2. Use `noty.bat` to run the tool:

```cmd
# Add notes
noty.bat add "Your note here"

# List notes  
noty.bat list

# Remove notes
noty.bat rm 1
```

Or run directly with Python:
```cmd
python path\to\noty\noty.py add "Your note here"
```

## Storage

Notes are stored in `~/.noty_notes.json` in your home directory.

## Available Commands

| Flag | Long Form | Description | Example |
|------|-----------|-------------|---------|
| `<text>` | - | Add a note (shorthand) | `noty "Buy groceries"` |
| `-a <text>` | `--add <text>` | Add a note | `noty -a "Buy groceries"` |
| `-l` | `--list` | List all notes with IDs and timestamps | `noty -l` |
| `-r <id>` | `--remove <id>` | Remove a note by ID | `noty -r 3` |
| `-e [file]` | `--export [file]` | Export notes to text file | `noty -e backup.txt` |
| `-c` | `--clear` | Remove all notes (with confirmation) | `noty -c` |
| `-f` | `--fix` | Fix duplicate IDs (maintenance) | `noty -f` |
| `-h` | `--help` | Show help message | `noty -h` |

## Examples

```bash
$ noty "Buy milk and eggs"
Added note: Buy milk and eggs

$ noty -a "Call dentist tomorrow"
Added note: Call dentist tomorrow

$ noty -l
Found 2 note(s):
────────────────────────────────────────────────────────────
  #1 │ 2025-11-04 10:55:08 │ Buy milk and eggs
  #2 │ 2025-11-04 10:55:16 │ Call dentist tomorrow
────────────────────────────────────────────────────────────

$ noty -r 1
Removed note #1: Buy milk and eggs

$ noty -l
Found 1 note(s):
────────────────────────────────────────────────────────────
  #2 │ 2025-11-04 10:55:16 │ Call dentist tomorrow
────────────────────────────────────────────────────────────

$ noty -e my_notes.txt
Exported 1 notes to: my_notes.txt

$ noty -h
Noty - Simple command line note-taking tool

Usage:
  noty <text>         - Add a note (shorthand)
  noty -a <text>      - Add a note
  noty -l             - List all notes
  noty -r <id>        - Remove a note by ID
  noty -e [file]      - Export notes to text file
  noty -c             - Clear all notes (with confirmation)
  noty -f             - Fix duplicate IDs (maintenance)
  noty -h             - Show this help message
```