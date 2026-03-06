from functools import wraps
from src.AddressBook.address_book import AddressBook, Record, AddressBookError
from pathlib import Path
import pickle

def input_error(required_args):
    def inner_wrap(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if len(args) + len(kwargs) - 1 < required_args:
                return "Enter all the arguments for the command"
            try:
                return func(*args, **kwargs)
            except AddressBookError as e:
                return str(e)

        return inner
    return inner_wrap

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

class ContactsManager:
    book = AddressBook()

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

    # hello
    def hello(self):
        return "Hello! How can I help you?"

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


def main():
    contacts = ContactsManager()
    contacts.load("contacts.pkl")
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "quit"]:
            print("Good bye!")
            break
        elif hasattr(contacts, command):
            print(getattr(contacts, command)(*args))
        else:
            print(contacts.invalid())
    contacts.save("contacts.pkl")

if __name__ == "__main__":
    main()