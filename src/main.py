import os
from colorama import Fore, Style
from ContactsManager.contact_manager import ContactsManager
from Notes.notes import Notes
from Utils.ParseInput import parse_input


def main():
    current_dir = os.getcwd()
    contacts = ContactsManager()
    contacts.load(f"{current_dir}/contacts.pkl")
    notes = Notes()
    notes.load(f"{current_dir}/notes.pkl")
    print("Welcome to the assistant bot!")
    while True:
        print(f"Print {Fore.GREEN}contacts{Style.RESET_ALL} to work with contacts")
        print(f"Print {Fore.BLUE}notes{Style.RESET_ALL} to work with notes")
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "quit"]:
            print("Good bye!")
            break
        elif command == "contacts":
            contacts.loop()
        elif command == "notes":
            notes.loop()
        elif hasattr(contacts, command):
            print(getattr(contacts, command)(*args))
        else:
            print(contacts.invalid())
    contacts.save(f"{current_dir}/contacts.pkl")
    notes.save(f"{current_dir}/notes.pkl")

if __name__ == "__main__":
    main()