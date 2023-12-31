import argparse
import json
import random
import time
from datetime import datetime
from faker import Faker
# import psycopg2
# from psycopg2 import extras

fake = Faker()

# def connect_db():
#     """Create a connection to the PostgreSQL database."""
#     return psycopg2.connect(
#         dbname="your_dbname", user="your_username", password="your_password", host="your_host"
#     )
#
# def insert_user(cursor, user):
#     """Insert a new user into the database."""
#     query = """INSERT INTO commerce.users (user_id, name, email, location, signup_date)
#                VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
#     cursor.execute(query, (
#         user['user_id'], user['name'], user['email'], user['location'], user['signup_date']
#     ))
#     return cursor.fetchone()[0]
#
# def insert_product(cursor, product):
#     """Insert a new product into the database."""
#     query = """INSERT INTO commerce.products (product_id, name, category, price, details)
#                VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
#     cursor.execute(query, (
#         product['product_id'], product['name'], product['category'], product['price'], product['details']
#     ))
#     return cursor.fetchone()[0]

def update_record(cursor, table, record_id):
    """Update a record in the database."""
    if table == 'users':
        query = "UPDATE commerce.users SET name = %s, email = %s WHERE id = %s;"
        cursor.execute(query, (fake.name(), fake.email(), record_id))
    elif table == 'products':
        query = "UPDATE commerce.products SET details = %s WHERE id = %s;"
        cursor.execute(query, (fake.sentence(), record_id))

def generate_user_data():
    """Generate fake user data."""
    return {
        'user_id': fake.uuid4(),
        'name': fake.name(),
        'email': fake.email(),
        'location': fake.address(),
        'signup_date': fake.date_this_decade().isoformat()
    }

def generate_product_data():
    """Generate fake product data."""
    return {
        'product_id': fake.uuid4(),
        'name': fake.word(),
        'category': fake.word(),
        'price': round(random.uniform(10, 1000), 2),
        'details': fake.sentence()
    }

def generate_click_data(user_id, product_id):
    """Generate fake click event data."""
    return {
        'user_id': user_id,
        'product_id': product_id,
        'date_occured': datetime.now().isoformat(),
        'page_url': fake.url(),
        'referrer_url': fake.url(),
        'session_id': fake.uuid4(),
        'location': fake.city(),
        'ip_address': fake.ipv4(),
        'user_agent': fake.user_agent()
    }

def generate_checkout_data(user_id, product_id):
    """Generate fake checkout event data."""
    return {
        'user_id': user_id,
        'product_id': product_id,
        'date_occured': datetime.now().isoformat(),
        'item_count': random.randint(1, 5),
        'total_price': round(random.uniform(10, 1000), 2),
        'payment_method': fake.credit_card_provider(),
        'shipping_address': fake.address(),
        'billing_address': fake.address() if fake.boolean(chance_of_getting_true=50) else None
    }

def main(num_users, num_clicks):
    data_file = 'ecommerce_data.txt'

    users = [generate_user_data() for _ in range(num_users)]
    products = [generate_product_data() for _ in range(num_users)]

    with open(data_file, 'w') as file:
        # Simulate user interactions
        for _ in range(num_clicks):
            user = random.choice(users)
            product = random.choice(products)

            click_data = generate_click_data(user['user_id'], product['product_id'])
            file.write('Click Event: ' + json.dumps(click_data) + '\n')

            # Simulate checkout with a more realistic probability
            if random.random() < 0.2:  # 20% chance of checkout after click
                checkout_data = generate_checkout_data(user['user_id'], product['product_id'])
                file.write('Checkout Event: ' + json.dumps(checkout_data) + '\n')

    # conn = connect_db()
    # conn.autocommit = True
    #
    # with conn.cursor() as cursor:
    #     # Insert user and product data
    #     users = [generate_user_data() for _ in range(num_users)]
    #     products = [generate_product_data() for _ in range(num_users)]
    #
    #     user_ids = [insert_user(cursor, user) for user in users]
    #     product_ids = [insert_product(cursor, product) for product in products]
    #
    #     # Simulate user interactions
    #     for _ in range(num_clicks):
    #         user_id = random.choice(user_ids)
    #         product_id = random.choice(product_ids)
    #
    #         # Update user and product records randomly
    #         if random.random() < 0.1:
    #             update_record(cursor, 'users', user_id)
    #         if random.random() < 0.05:
    #             update_record(cursor, 'products', product_id)
    #
    #         click_data = generate_click_data(user_id, product_id)
    #         print('Click Event:', click_data)
    #
    #         # Simulate checkout with a more realistic probability
    #         if random.random() < 0.2:  # 20% chance of checkout after click
    #             checkout_data = generate_checkout_data(user_id, product_id)
    #             print('Checkout Event:', checkout_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate e-commerce user and click data.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of user records to generate.")
    parser.add_argument("--num_clicks", type=int, default=1000, help="Number of click records to generate.")
    args = parser.parse_args()

    main(args.num_users, args.num_clicks)
