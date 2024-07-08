from sqlalchemy.orm import sessionmaker
from faker import Faker
import models

fake = Faker()

def create_user_data(session, num_records=100):
    users = []
    for _ in range(num_records):
        user = models.User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email()
        )
        users.append(user)
    session.bulk_save_objects(users)
    session.commit()

if __name__ == '__main__':
    engine = models.get_engine()
    models.create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    create_user_data(session, num_records=100)
    print("User data inserted successfully!")
