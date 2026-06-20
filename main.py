import pickle
from functools import wraps
from address_book import AddressBook, Record

comands = ['"hello" - to start',
          '"exit" or "close" - to close programm',
          '"help" - return valid comands',
          '"add [name] [phone]" - to add contacts',
          '"change [name] [phone]" - to change contact',
          '"phone [name]" - to get phone',
          '"all" - to get all contacts',
          '"add-birthday [name] [date]" - add birthday for contact, format "DD.MM.YYYY"',
          '"show-birthday [name]" - show birthday this contact',
          '"birthdays" - returns a list of birthdays for next week']

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"{e}"
        except IndexError:
            return "Invalid command. Use the 'help' command to get valid commands."
        except KeyError:
            return "Contact not found."
        except AttributeError:
            return "Contact not found."
        except Exception as e:
            return f"Error: {e}"

    return inner

def parse_comand(user_input: str):
    if not user_input:
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, args


@input_error
def add_contact(args: list, contacts: AddressBook):
    if len(args) != 2:
        raise ValueError("Must be name and phone")
    name, phone = args
    record = contacts.find(name)
    if not record:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        return "Contact added"
    record.add_phone(phone)
    return "Phone added"

@input_error
def change_contact(args: list, contacts: AddressBook):
    if len(args) != 3:
        raise ValueError("Must be a name, old phone and new phone")
    name, old_p, new_p = args
    if len(old_p) != 10 or not old_p.isdigit():
        raise ValueError("Invalid old number. The number must be 10 digits long.")
    recorrd = contacts.find(name)
    recorrd.edit_phone(old_p, new_p)
    return "Contact changed"
    
@input_error
def get_phone(args: list, contacts: AddressBook):
    if len(args) != 1:
        raise ValueError("Must be a name.")
    name = args[0]
    record = contacts.find(name)
    str_phones = []
    for phone in record.phones:
        str_phones.append(str(phone))
    phones = ", ".join(str_phones)
    return f"Name: {name}, Phones: {phones}."

def get_all(contacts: AddressBook):
    if len(contacts) > 0:
        contact_list = []
        for user in contacts:
            contact_list.append(f"{str(contacts[user])} \n")
        return "".join(contact_list)
    else:
        return "Your contacts is empty..."

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Must be a name and date DD.MM.YYYY.")
    name, date = args
    record = book.find(name)
    if not record:
        record = Record(name)
        record.add_birthday(date)
        book.add_record(record)
        return "Birthday added."
    if record.birthday:
        record.add_birthday(date)
        return "Birthday changed."
    record.add_birthday(date)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        return "Must be a name."
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return "This contact does not have a birthday listed."
    return f"Name: {name}, Birthday: {str(record.birthday)}"

@input_error
def birthdays(book: AddressBook):
    birt_list = book.get_upcoming_birthdays()
    if not birt_list:
        return "There are no birthdays for the next week."
    res_list = []
    for user in birt_list:
        res_list.append(f"Name: {user["name"]}, Birthday: {user["birthday"]}\n")
    return "".join(res_list)

def main():
    contacts = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_inp = input("Enter a command: ").strip()
        comand, list_arg = parse_comand(user_inp)

        if comand in ["exit", "close"]:
            save_data(contacts)
            print("Good bye!")
            break
        elif comand == "hello":
            print("How can I help you?")
        elif comand == "help":
            for comand in comands:
                print(comand)
        elif comand == "all":
            print(get_all(contacts))
        elif comand == "add":
            print(add_contact(list_arg, contacts))
        elif comand == "phone":
            print(get_phone(list_arg, contacts))
        elif comand == "change":
            print(change_contact(list_arg, contacts))
        elif comand == "add-birthday":
            print(add_birthday(list_arg, contacts))
        elif comand == "show-birthday":
            print(show_birthday(list_arg, contacts))
        elif comand == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command. Use the 'help' command to get valid commands.")

if __name__ == "__main__":
    main()
