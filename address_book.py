from collections import UserDict
from datetime import datetime
from datetime import datetime, timedelta
import re

def date_to_str(date: datetime):
    return date.strftime("%d.%m.%Y")

def str_to_date(date: str):
    try:
        return datetime.strptime(date, "%d.%m.%Y").date()
    except:
        raise ValueError("Invalid format date in contacts.")

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if len(str(value)) != 10 or not str(value).isdigit():
            raise ValueError("The number must be 10 digits long.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str):
        is_valid = re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", value)
        if not is_valid:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        day, month, year = value.split(".")
        if int(year) > datetime.today().year:
            raise ValueError("The date cannot be in the future.")
        try:
            datetime(year, month, day)
        except:
            raise ValueError("Invalid month or day.")
        self.value = value

    def __str__(self):
        return self.value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        old_p = self.find_phone(phone)
        self.phones.remove(old_p)

    def edit_phone(self, old_p, new_p):
        phone = self.find_phone(old_p)
        if not phone:
            raise ValueError("Phone not found in this contact.")
        self.add_phone(new_p)
        self.remove_phone(old_p)       

    def find_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                return el
        return None

    def add_birthday(self, value: str):
        self.birthday = Birthday(value.strip())

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, birthday: {str(self.birthday)}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}, birthday: ----------, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __str__(self):
        return str(self.data.name)

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name)

    def get_upcoming_birthdays(self):
        current_list = []
        for user in self.data:
            if self.data[user].birthday:
                current_list.append({"name": user, "birthday": str_to_date(self.data[user].birthday.value)})

        if len(current_list) < 1:
            return current_list

        res_list = []
        today = datetime.today().date()
        for user in current_list:
            user["birthday"] = user["birthday"].replace(year = today.year)

        for user in current_list:
            if user["birthday"] < today:
                user["birthday"] = user["birthday"].replace(year = today.year + 1)
            if 0 <= (user["birthday"] - today).days <= 7:
                if user["birthday"].weekday() >= 5:
                    user["birthday"] = find_next_weekday(user["birthday"], 0)
                res_list.append({"name": user["name"], "birthday": date_to_str(user["birthday"])})
        return res_list