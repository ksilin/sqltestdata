from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Outbox, get_engine, create_tables
# import models
import uuid

fake = Faker()

def generate_user_payload():
    return {
        "id": str(uuid.uuid4()),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address()
    }

def generate_product_payload():
    return {
        "id": str(uuid.uuid4()),
        "name": fake.word(),
        "price": round(fake.random_number(digits=2), 2)
    }

def generate_purchase_payload(user_id, product_ids):
    return {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "product_ids": product_ids,
        "total": sum(fake.random_number(digits=2) for _ in product_ids),
        "timestamp": fake.date_time_between(start_date='-1y', end_date='now').isoformat()
    }

def create_test_data(session, num_records=10):
    users = []
    products = []

    # Generate users
    for _ in range(num_records):
        payload = generate_user_payload()
        user = Outbox(
            aggregatetype='user',
            aggregateid=payload['id'],
            type='create',
            payload=payload
        )
        users.append(user)
    session.bulk_save_objects(users)
    session.commit()

    # Generate products
    for _ in range(num_records):
        payload = generate_product_payload()
        product = Outbox(
            aggregatetype='product',
            aggregateid=payload['id'],
            type='create',
            payload=payload
        )
        products.append(product)
    session.bulk_save_objects(products)
    session.commit()

    # Generate purchases
    for _ in range(num_records):
        user_id = fake.random_element(elements=[user.payload['id'] for user in users])
        product_ids = fake.random_elements(elements=[product.payload['id'] for product in products], unique=True, length=3)
        payload = generate_purchase_payload(user_id, product_ids)
        purchase = Outbox(
            aggregatetype='purchase',
            aggregateid=payload['id'],
            type='create',
            payload=payload
        )
        session.add(purchase)
    session.commit()

if __name__ == '__main__':
    engine = get_engine()
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    create_test_data(session, num_records=10)
    print("Outbox data inserted successfully!")
