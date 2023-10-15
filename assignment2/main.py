phonebook = dict()


def add_contact(name, phone):
    phonebook[name] = phone
    return "Contact added"
# end def


def change_contact(name, phone):
    if name not in phonebook:
        return "Contact doesn't exist"
    # end if

    phonebook[name] = phone
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


def phone_entered(phone):
    if len(phone) == 0:
        print("Phone number empty, try again")
        return False
    return True
    # end if
# end def


def run_code():
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
            if phone_entered(phone):
                print(add_contact(name, phone[0]))
        elif command in ["edit", "change", "modify"]:
            if len(data) == 0:
                print("No data entered")
                continue
            # end if

            name, *phone = data
            if phone_entered(phone):
                print(change_contact(name, phone[0]))
            # end if
        elif command in ["phone", "show"]:
            if len(data):
                print(show_phone(data[0]))
            else:
                print("Name not entered")
            # end if
        elif command in ["all", "list"]:
            print(show_all())
        elif command in ['close', 'quit', 'exit', 'bye']:
            print("Good bye!")
            break
        else:
            print("I didn't understand you. Try asking something else (Invalid command)")
        # end if
    # end while
# end def


if __name__ == "__main__":
    run_code()
# end if
