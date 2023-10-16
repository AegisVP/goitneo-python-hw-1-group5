import calendar
import json
from faker import Faker
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Names of weekdays
weekday_name = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday"
}

# File for storage of users data
USERS_FILE = Path(__file__).parent / "data.json"

# If USERS_FILE is not present, do you want to save mock data to file?
SAVE_DATA_TO_FILE = True

# If USERS_FILE is not present, number of generated mock users
NUMBER_OF_GENERATED_USERS = 300

# If no birthday is on said day, should the day be printed in the report?
PRINT_EMPTY_DAYS = False

# Do you want to show turning age of the person?
SHOW_AGE = False


def get_mocked_user():
    # fake = Faker()
    return {
        "name": Faker().name(),
        "birthday": Faker().date_of_birth()
    }


def populate_users(amount=NUMBER_OF_GENERATED_USERS):
    users = list()
    if (USERS_FILE.exists()):
        users = [{
            "name": user['name'],
            "birthday": datetime.strptime(user['birthday'], '%d-%m-%Y').date()
        } for user in json.loads(USERS_FILE.read_text())[:amount]]
    else:
        users = [get_mocked_user() for _ in range(amount)]
        if SAVE_DATA_TO_FILE:
            USERS_FILE.write_text(json.dumps([{
                "name": user['name'],
                "birthday": datetime.strftime(user['birthday'], '%d-%m-%Y')
            } for user in users]))
    # end if
    return users
# end def


def get_next_birthdays(users):
    current_date = datetime.now().date()
    is_leap = calendar.isleap(current_date.year)

    next_birthdays = defaultdict(list)
    for user in users:
        birthday = user['birthday']

        # can not do birthday.replace(year=current_date.year) because
        # if birthday is on feb 29 on a leap year and now is not a leap year,
        # it will throw an error "ValueError: day is out of range for month"
        month = birthday.month
        day = birthday.day
        if (month == 2 and day == 29 and not is_leap):
            day = 28
        # end if

        celebrate_day = datetime(
            year=current_date.year,
            month=month,
            day=day
        ).date()

        if (celebrate_day > current_date and (celebrate_day - current_date).days <= 7):
            weekday: int = int(birthday.strftime('%w'))
            if weekday == 0 or weekday == 6:
                weekday = 1
            # end if
            user['age_str'] = f" ({(current_date.year - birthday.year)})" if SHOW_AGE else ""
            next_birthdays[weekday_name[weekday]].append(user)
        # end if
    # end for
    return next_birthdays
# end def

# Get a sorted list of next working days for next 7 calendar days
def next_seven_workdays():
    cur = datetime.now().date()
    next_days = list()
    for i in range(6+1):
        cur_day = int(cur.strftime('%w')) + i
        if cur_day > 6:
            cur_day -= 7
        # end if
        if cur_day != 0 and cur_day != 6:
            next_days.append(weekday_name[cur_day])
        # end if
    # end for
    return next_days
# end def


def print_upcoming_birthdays(next_birthdays):
    print("")
    print("Upcoming birtdays:")

    for next_workday in next_seven_workdays():
        output_string = f"{next_workday}: "

        if len(next_birthdays[next_workday]) == 0:
            if not PRINT_EMPTY_DAYS:
                continue
            
            output_string += "- - -"
            # end if
        else:
            cur = datetime.now().date()
            output_string += ", ".join(
                [f"{user['name']}{user['age_str']}" for user in next_birthdays[next_workday]]
            )
        # end if

        print(output_string)
        # end if
    # end for
# end def


def get_birthdays_per_week():
    # get list of users. Can pass an int as parameter to generate the specified number of users if not data.json is present (default = NUMBER_OF_GENERATED_USERS)
    users = populate_users()

    # get list of birthdays within the next 7 days
    next_birthdays = get_next_birthdays(users)

    # print (sorted by date from today) a list of upcoming birthdays.
    print_upcoming_birthdays(next_birthdays)
# end def


if __name__ == "__main__":
    get_birthdays_per_week()
# end if
