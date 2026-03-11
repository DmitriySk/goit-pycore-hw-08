from pathlib import Path
import pickle

from Utils.InputError import input_error
from Utils.errors import NotesError
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table

from Utils.ParseInput import parse_input
from Notes.note import Note

def input_txt(message):
    print(Fore.BLUE+"Notes ", end="")
    return input(Style.RESET_ALL+message)

def print_message(message):
    print(Fore.BLUE+"Notes ", end="")
    print(Style.RESET_ALL+message)

class Notes:
    def __init__(self):
        self.notes = []

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.notes, f)

    def load(self, filename):
        path = Path(filename)
        if path.exists() and path.is_file():
            with path.open("rb") as f:
                self.notes = pickle.load(f)

    def loop(self):
        print_message("Enter 'q' to go back. Enter 'add' to add note")
        while True:
            user_input = input_txt("Enter a command: ")
            command, *args = parse_input(user_input)

            if command == 'add':
                self.add_note()
            elif command == 'search':
                self.search(*args)
            elif command == 'all':
                self.all()
            elif command == 'edit':
                print_message(self.edit(*args))
            elif command == 'delete':
                print_message(self.delete(*args))
            elif command == 'q':
                break
            else:
                print_message("Invalid command")

    @input_error
    def add_note(self):
        note = input_txt("Enter a note: ")
        tags = input_txt("Enter tags (separated by commas): ")
        self.notes.append(Note(note, tags))
        print_message("Note added")

    def show_all(self, term: str = ""):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim green", overflow="ellipsis")
        table.add_column("Tags", style="dim yellow")
        table.add_column("Text")

        for note in self.notes:
            if not term or note.has(term.lower()):
                table.add_row(
                    str(note.id), note.get_tags(), note.note
                )
        console = Console()
        console.print(table)

    @input_error(required_args=1)
    def search(self, term):
        self.show_all(term)

    def all(self):
        self.show_all()

    @input_error(required_args=1)
    def delete(self, id):
        if not id.isdigit():
            raise NotesError("ID must be a number")
        new_notes = list(filter(lambda n: not n.id == int(id), self.notes))
        if len(self.notes) == len(new_notes):
            raise NotesError("Note with this ID not found")
        self.notes = new_notes
        return "Note deleted"

    @input_error(required_args=1)
    def edit(self, id):
        if not id.isdigit():
            raise NotesError("ID must be a number")
        note = next((n for n in self.notes if n.id == int(id)), None)
        print_message(note.note)
        new_note = input_txt("Enter a new note: ")
        if new_note.strip() != "":
            note.note = new_note
        print_message(note.get_tags())
        new_tags = input_txt("Enter new tags (separated by commas): ")
        if new_tags.strip() != "":
            note.tags = new_tags
        return f"Note {note.id} edited."
