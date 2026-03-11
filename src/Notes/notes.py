from pathlib import Path
import pickle
from colorama import Fore, Style

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
                self.search()
            elif command == 'q':
                break
            else:
                print_message("Invalid command")

    def add_note(self):
        note = input_txt("Enter a note: ")
        tags = input_txt("Enter tags (separated by commas): ")
        self.notes.append(Note(note, tags))
        print_message("Note added")

    def search(self):
        search_term = input_txt("Enter a search term: ")
        for index, note in enumerate(self.notes):
            if note.has(search_term):
                print_message(Fore.YELLOW+str(index)+" "+Style.RESET_ALL+note.note)
