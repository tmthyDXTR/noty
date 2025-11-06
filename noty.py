#!/usr/bin/env python3
"""
Noty - A simple command line note-taking tool

Usage:
    noty <text>         - Add a note (shorthand)
    noty -a <text>      - Add a note with the given text
    noty -l             - List all notes with timestamps
    noty -r <id>        - Remove a note by ID
    noty -e [file]      - Export notes to text file
    noty -c             - Clear all notes (with confirmation)
    noty -f             - Fix duplicate IDs (maintenance)
    noty -h             - Show help message
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path


class NotyManager:
    def __init__(self):
        # Store notes in user's home directory
        self.notes_file = Path.home() / '.noty_notes.json'
        
    def load_notes(self):
        """Load notes from the JSON file"""
        if not self.notes_file.exists():
            return []
        
        try:
            with open(self.notes_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_notes(self, notes):
        """Save notes to the JSON file"""
        with open(self.notes_file, 'w') as f:
            json.dump(notes, f, indent=2)
    
    def add_note(self, text):
        """Add a new note with timestamp"""
        notes = self.load_notes()
        
        # Find the next available ID
        if not notes:
            next_id = 1
        else:
            existing_ids = [note['id'] for note in notes]
            next_id = max(existing_ids) + 1
        
        note = {
            'text': text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'id': next_id
        }
        
        notes.append(note)
        self.save_notes(notes)
        print(f"Added note: {text}")
    
    def list_notes(self):
        """List all notes with timestamps and IDs"""
        notes = self.load_notes()
        
        if not notes:
            print("No notes found.")
            return
        
        print(f"Found {len(notes)} note(s):")
        print("─" * 60)
        
        for i, note in enumerate(notes):
            print(f"  #{note['id']} │ {note['timestamp']} │ {note['text']}")
            # Add a visual separator between notes (but not after the last one)
            if i < len(notes) - 1:
                print("   " + "·" * 58)
        
        print("─" * 60)
    
    def remove_note(self, note_id):
        """Remove a note by ID"""
        try:
            note_id = int(note_id)
        except ValueError:
            print(f"Error: '{note_id}' is not a valid ID number")
            return
        
        notes = self.load_notes()
        
        # Find the note with the given ID
        note_to_remove = None
        for note in notes:
            if note['id'] == note_id:
                note_to_remove = note
                break
        
        if note_to_remove is None:
            print(f"Error: No note found with ID #{note_id}")
            return
        
        # Remove the note
        notes.remove(note_to_remove)
        self.save_notes(notes)
        print(f"Removed note #{note_id}: {note_to_remove['text']}")
    
    def fix_duplicate_ids(self):
        """Fix any duplicate IDs in existing notes"""
        notes = self.load_notes()
        
        if not notes:
            print("No notes to fix.")
            return
        
        # Reassign IDs sequentially
        for i, note in enumerate(notes):
            note['id'] = i + 1
        
        self.save_notes(notes)
        print(f"Fixed IDs for {len(notes)} notes.")
    
    def export_notes(self, filename=None):
        """Export notes to a human-readable text file"""
        notes = self.load_notes()
        
        if not notes:
            print("No notes to export.")
            return
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"noty_export_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("NOTY - Exported Notes\n")
                f.write("=" * 50 + "\n")
                f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total notes: {len(notes)}\n\n")
                
                for note in notes:
                    f.write(f"#{note['id']} - {note['timestamp']}\n")
                    f.write(f"{note['text']}\n")
                    f.write("-" * 40 + "\n\n")
            
            print(f"Exported {len(notes)} notes to: {filename}")
            
        except IOError as e:
            print(f"Error writing to file: {e}")
    
    def clear_all_notes(self):
        """Clear all notes with confirmation"""
        notes = self.load_notes()
        
        if not notes:
            print("No notes to clear.")
            return
        
        print(f"Warning: This will permanently delete all {len(notes)} notes!")
        print("This action cannot be undone.")
        
        # Get user confirmation
        while True:
            response = input("Are you sure you want to delete all notes? (y/N): ").lower().strip()
            
            if response in ['y', 'yes']:
                # Clear all notes
                self.save_notes([])
                print(f"Cleared all {len(notes)} notes.")
                break
            elif response in ['n', 'no', '']:
                print("Operation cancelled.")
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  noty <text>         - Add a note (shorthand)")
        print("  noty -a <text>      - Add a note")
        print("  noty -l             - List all notes")
        print("  noty -r <id>        - Remove a note by ID")
        print("  noty -e [file]      - Export notes to text file")
        print("  noty -c             - Clear all notes (with confirmation)")
        print("  noty -f             - Fix duplicate IDs (maintenance)")
        print("  noty -h             - Show help message")
        return
    
    noty = NotyManager()
    command = sys.argv[1]
    
    if command == '-a' or command == '--add':
        if len(sys.argv) < 3:
            print("Error: Please provide text to add")
            print("Usage: noty -a <text>")
            return
        
        # Join all remaining arguments as the note text
        note_text = ' '.join(sys.argv[2:])
        noty.add_note(note_text)
    
    elif command == '-l' or command == '--list':
        noty.list_notes()
    
    elif command == '-r' or command == '--remove':
        if len(sys.argv) < 3:
            print("Error: Please provide the ID of the note to remove")
            print("Usage: noty -r <id>")
            return
        
        noty.remove_note(sys.argv[2])
    
    elif command == '-h' or command == '--help':
        print("Noty - Simple command line note-taking tool")
        print()
        print("Usage:")
        print("  noty <text>         - Add a note (shorthand)")
        print("  noty -a <text>      - Add a note")
        print("  noty --add <text>   - Add a note")
        print("  noty -l             - List all notes")
        print("  noty --list         - List all notes")
        print("  noty -r <id>        - Remove a note by ID")
        print("  noty --remove <id>  - Remove a note by ID")
        print("  noty -e [file]      - Export notes to text file")
        print("  noty --export [file] - Export notes to text file")
        print("  noty -c             - Clear all notes (with confirmation)")
        print("  noty --clear        - Clear all notes (with confirmation)")
        print("  noty -f             - Fix duplicate IDs (maintenance)")
        print("  noty --fix          - Fix duplicate IDs (maintenance)")
        print("  noty -h             - Show this help message")
        print("  noty --help         - Show this help message")
        print()
        print("Note: To add text starting with '-', use: noty -a \"-- your text\"")
    
    elif command == '-f' or command == '--fix':
        noty.fix_duplicate_ids()
    
    elif command == '-e' or command == '--export':
        # Optional filename argument
        if len(sys.argv) > 2:
            filename = sys.argv[2]
            noty.export_notes(filename)
        else:
            noty.export_notes()
    
    elif command == '-c' or command == '--clear':
        noty.clear_all_notes()
    
    else:
        # Check if it looks like a flag (starts with -)
        if command.startswith('-'):
            print(f"Error: Unknown flag '{command}'")
            print("Use 'noty -h' to see available flags.")
            return
        
        # If the command is not recognized and doesn't start with -, treat it as note text
        # This allows "noty <text>" to work as shorthand for "noty add <text>"
        note_text = ' '.join(sys.argv[1:])
        noty.add_note(note_text)


if __name__ == '__main__':
    main()