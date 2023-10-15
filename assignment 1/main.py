import calendar
import json
from collections import defaultdict
from datetime import datetime, timedelta
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


def populate_users(amount=200):
    users = list()
    if (users_file.exists()):
        for user in json.loads(users_file.read_text())[:amount]:
            user['birthday'] = datetime.strptime(user['birthday'], '%d-%m-%Y')
            users.append(user)
    else:
        for i in range(amount):
            user = get_mocked_user()
            user['birthday'] = datetime.strftime(user['birthday'], '%d-%m-%Y')
            users.append(user)
        # end for
    # end if
    return users
# end def


def get_next_birthdays(users):
    current_date = datetime.now().date()
    is_leap = calendar.isleap(current_date.year)

    next_birthdays = defaultdict(list)
    for user in users:
        birthday = user['birthday'].date()

        month = birthday.month
        day = birthday.day

        # can not do birthday.replace(year=current_date.year) because if bday is on feb 29 in a leap year and now is not a leap year, it will throw an error "ValueError: day is out of range for month"
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
            # $end if
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
        if cur_day != 0 and cur_day != 6:
            next_days.append(weekday_name[cur_day])
    return next_days


if __name__ == "__main__":
    # get list of users. Can pass an int as parameter to generate the specified number of users if not data.json is present (default = 200)
    users = populate_users()

    # get list of birthdays within the next 7 days
    next_birthdays = get_next_birthdays(users)

    # print (sorted by date from today) a list of upcoming birthdays.

    # Skip days with no birthdays?
    skip_empty_days = False

    print("Upcoming birtdays:")
    for next_workday in next_seven_workdays():
        output_string = f"{next_workday}: "
        if len(next_birthdays[next_workday]) == 0:
            if skip_empty_days:
                output_string = None
            else:
                output_string += "- - -"
        else:
            cur = datetime.now().date()
            bday_people = list()
            for user in next_birthdays[next_workday]:
                name = user['name']
                bday = user['birthday'].date()
                age = (cur.year - bday.year)
                bday_people.append(f"{name} ({age})")
            output_string += ", ".join(bday_people)

        if output_string:
            print(output_string)
