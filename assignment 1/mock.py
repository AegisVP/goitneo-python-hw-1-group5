import random
from faker import Faker

fake = Faker()


def get_mocked_user():
    fake = Faker()
    mock = {
        "name": fake.name(),
        "birthday": fake.date_of_birth()
    }
    return mock


if __name__ == "__main__":
    mock = get_mocked_user()
    print(mock)
