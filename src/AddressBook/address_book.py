from collections import UserDict
from datetime import datetime

class AddressBookError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return f"Name: {self.value}"

class Phone(Field):
    @staticmethod
    def process_phone(phone: str):
        if len(phone) == 10 and phone.isdigit():
            return phone
        raise AddressBookError(f"Phone number {phone} is invalid")

    def __init__(self, phone: str):
        super().__init__(phone)
        self.value = Phone.process_phone(phone)

    def __repr__(self):
        return self.value

class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(value)
        try:
            self.birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise AddressBookError("Invalid date format. Use DD.MM.YYYY")

    def get_birthday(self):
        return self.birthday.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def get_phone_index(self, phone: str):
        return [phone.value for phone in self.phones].index(phone)

    def edit_phone(self, old_phone: str, new_phone: str):
        index = self.get_phone_index(old_phone)
        if index != -1:
            self.phones[index] = Phone(new_phone)
        else:
            raise AddressBookError(f"Phone number {old_phone} not found")

    def remove_phone(self, phone: str):
        index = self.get_phone_index(phone)
        self.phones.pop(index)

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def get_birthday(self):
        return self.birthday.get_birthday() if self.birthday else "Birthday is empty"

    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: [{', '.join(p.value for p in self.phones)}]"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return "Record deleted"
        return "Record not found"

    def __repr__(self):
        return str(self.data)
