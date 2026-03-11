from pathlib import Path
import pickle
from colorama import Fore, Style

from AddressBook.address_book import AddressBook, Record, AddressBookError
from Utils.InputError import input_error
from Utils.ParseInput import parse_input


def input_txt(message):
    print(Fore.GREEN+"Notes ", end="")
    return input(Style.RESET_ALL+message)

def print_message(message):
    print(Fore.GREEN+"Notes ", end="")
    print(Style.RESET_ALL+message)

class ContactsManager:
    def __init__(self):
        self.book = AddressBook()

    @staticmethod
    def print_help():
        print_message(f"Enter {Fore.GREEN}add [name] [phone number]{Style.RESET_ALL} to add contact")
        print_message(f"Enter {Fore.GREEN}change [name] [old phone] [new phone]{Style.RESET_ALL} to change contact phone")
        print_message(f"Enter {Fore.GREEN}add_birthday [name] [birth date]{Style.RESET_ALL} to add contact birthday")
        print_message(f"Enter {Fore.GREEN}show_birthday [name]{Style.RESET_ALL} to show contact birthday")
        print_message(f"Enter {Fore.GREEN}birthdays{Style.RESET_ALL} to show all contacts birthday")
        print_message(f"Enter {Fore.GREEN}phone [name]{Style.RESET_ALL} to show contact info")
        print_message(f"Enter {Fore.GREEN}all{Style.RESET_ALL} to show all contacts")

    @staticmethod
    def hello(self):
        return "Hello! How can I help you?"

    @staticmethod
    def help():
        ContactsManager.print_help()

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.book, f)

    def load(self, filename):
        path = Path(filename)
        if path.exists() and path.is_file():
            with path.open("rb") as f:
                ContactsManager.book = pickle.load(f)

    def _check(self, name: str):
        if not name in self.book:
            raise AddressBookError("Contact not found")

    def loop(self):
        ContactsManager.print_help()
        while True:
            user_input = input_txt("Enter a command: ")
            command, *args = parse_input(user_input)

            if command == 'q':
                break
            elif hasattr(self, command):
                print(getattr(self, command)(*args))
            else:
                print_message("Invalid command")

    # add [ім'я] [телефон]
    @input_error(required_args=1)
    def add(self, name, phone = ""):
        record = self.book.find(name)
        if not record:
            record = Record(name)
            self.book.add_record(record)
        if phone:
            record.add_phone(phone)
        return "Contact added."

    # change [ім'я] [старий телефон] [новий телефон]
    @input_error(required_args=3)
    def change(self, name, old_phone, new_phone):
        contact = self.book.find(name)
        contact.edit_phone(old_phone, new_phone)
        return "Contact updated."

    # phone [ім'я]
    @input_error(required_args=1)
    def phone(self, name):
        self._check(name)
        contact = self.book.find(name)
        return str(contact)

    # all
    @input_error(required_args=0)
    def all(self):
        if len(self.book) == 0:
            return "No contacts in the list."
        return "\n".join(str(record) for record in self.book.data.values())

    # add-birthday [ім'я] [дата народження]
    @input_error(required_args=2)
    def add_birthday(self, name, birthday):
        self._check(name)
        contact = self.book.find(name)
        contact.add_birthday(birthday)
        return "Birthday added."

    # show-birthday [ім'я]
    @input_error(required_args=1)
    def show_birthday(self, name):
        self._check(name)
        contact = self.book.find(name)
        return contact.get_birthday()

    # birthdays
    @input_error(required_args=0)
    def birthdays(self):
        if len(self.book) == 0:
            return "No contacts in the list."
        return "\n".join(f"{name}: {record.get_birthday()}" for name, record in self.book.data.items())

    def invalid(self):
        return "Invalid command."

    def __repr__(self):
        return str(self.book)