from functools import wraps
from AddressBook.address_book import AddressBookError
from colorama import Fore, Style

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
            except Exception:
                return Fore.RED+"Something went wrong. Try again"+Style.RESET_ALL

        return inner
    return inner_wrap