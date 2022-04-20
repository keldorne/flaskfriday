import random
import sys
from faker import Faker
from main import db, Users


def create_fake_users(n):
    """Generate fake users."""
    faker = Faker()
    for i in range(n):
        user = Users(id="",
                    name=faker.name(),
                    email=faker.email(),
                    date_added="010203")
        db.session.add(user)
    db.session.commit()
    print(f'Added {n} fake users to the database.')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Pass the number of users you want to create as an argument.')
        sys.exit(1)
    create_fake_users(int(sys.argv[1]))
