import json
from pathlib import Path

phonebook = dict()
phonebook_file = Path(__file__).parent / "phonebook.json"
SAVE_TO_FILE = False
help_text='''
hi/hello - Вітаємось з чат-ботом
help - Виводить перелік команд
add/new <name> <phone> - Додати до телефонної книжки запис
change/edit/modify <name> <new phone> - Змінити телефон запис в телефонній книжці
phone/show <name> - Показати телефон контакта
all/list - Показати всі контакти
close/quit/exit/bye - Завершити роботу
'''


def write_phonebook_to_file():
    if SAVE_TO_FILE and phonebook_file.exists():
        phonebook_file.write_text(json.dumps(phonebook))
#end def


def read_phonebook_from_file():
    if phonebook_file.exists():
        return json.loads(phonebook_file.read_text())
#end def


def add_contact(name, phone):
    phonebook[name] = phone
    write_phonebook_to_file()
    return "Contact added"
# end def


def change_contact(name, phone):
    if name not in phonebook:
        return "Contact doesn't exist"
    # end if

    phonebook[name] = phone
    write_phonebook_to_file()
    return "Contact changed"
# end def


def show_phone(name):
    if name not in phonebook:
        return "Contact not found"
    # end if

    return phonebook[name]
# end def


def show_all():
    if len(phonebook) == 0:
        return "Phonebook is empty"
    # end if

    return '\n'.join([f"{name}: {phone}" for name, phone in phonebook.items()])
# end def


def is_phone_entered(phone):
    return len(phone) == 0
# end def


def run_bot():
    global phonebook
    phonebook = read_phonebook_from_file()
    print("Welcome! What can I do for you?")
    while True:
        user_input = input(">>> ")
        if len(user_input) == 0:
            continue
        # end if

        command, *data = user_input.strip().split()
        command = command.casefold()

        if command in ["hello", "hi"]:
            print("How can I help you?")
        elif command in ["add", "new"]:
            if len(data) == 0:
                print("No data entered")
                continue
            # end if

            name, *phone = data
            if is_phone_entered(phone):
                print(add_contact(name, phone[0]))
            else:
                print("Phone number empty, try again")
            # end if
        elif command in ["edit", "change", "modify"]:
            if len(data) == 0:
                print("No data entered")
                continue
            # end if

            name, *phone = data
            if is_phone_entered(phone):
                print(change_contact(name, phone[0]))
            else:
                print("Phone number empty, try again")
            # end if
        elif command in ["phone", "show"]:
            if len(data):
                print(show_phone(data[0]))
            else:
                print("Name not entered")
            # end if
        elif command in ["all", "list"]:
            print(show_all())
        elif command in ["help"]:
            print(help_text)
        elif command in ['close', 'quit', 'exit', 'bye']:
            print("Good bye!")
            break
        else:
            print("I didn't understand you. Try asking something else or typing 'help' (Invalid command)")
        # end if
    # end while
# end def


if __name__ == "__main__":
    run_bot()
# end if
