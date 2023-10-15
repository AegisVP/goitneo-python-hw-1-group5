import calendar
import json
from collections import defaultdict
from datetime import datetime
from mock import get_mocked_user
from pathlib import Path

users_file = Path(__file__).parent / "data.json"
weekday_name = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday"
}

NUMBER_GENERATED_OF_USERS = 300
SKIP_EMPTY_DAYS = False


def populate_users(amount=NUMBER_GENERATED_OF_USERS):
    users = list()
    if (users_file.exists()):
        users = [{
            "name": user['name'],
            "birthday": datetime.strptime(user['birthday'], '%d-%m-%Y').date()
        } for user in json.loads(users_file.read_text())[:amount]]
    else:
        users = [get_mocked_user() for _ in range(amount)]
        users_file.write_text(json.dumps([{
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
        # if birthday is on feb 29 in a leap year and now is not a leap year,
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
            next_birthdays[weekday_name[weekday]].append(user)
        # end if
    # end for
    return next_birthdays
# end def


def next_seven_workdays():
    cur = datetime.now().date()
    next_days = list()
    for i in range(6):
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
    print("Upcoming birtdays:")

    for next_workday in next_seven_workdays():
        output_string = f"{next_workday}: "

        if len(next_birthdays[next_workday]) == 0:
            if SKIP_EMPTY_DAYS:
                continue
            else:
                output_string += "- - -"
            # end if
        else:
            cur = datetime.now().date()
            output_string += ", ".join(
                [f"{user['name']} ({cur.year - user['birthday'].year})" for user in next_birthdays[next_workday]]
            )
        # end if

        print(output_string)
        # end if
    # end for
# end def


def run_code():
    # get list of users. Can pass an int as parameter to generate the specified number of users if not data.json is present (default = NUMBER_GENERATED_OF_USERS)
    users = populate_users()

    # get list of birthdays within the next 7 days
    next_birthdays = get_next_birthdays(users)

    # print (sorted by date from today) a list of upcoming birthdays.
    print_upcoming_birthdays(next_birthdays)
# end def


if __name__ == "__main__":
    run_code()
# end if
