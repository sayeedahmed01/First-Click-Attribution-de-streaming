import argparse
import random
from datetime import datetime

from faker import Faker

from db_operations import connect_db, insert_user, insert_product, update_record

fake = Faker()

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

    conn = connect_db()
    conn.autocommit = True

    with conn.cursor() as cursor:
        # Insert user and product data
        users = [generate_user_data() for _ in range(num_users)]
        products = [generate_product_data() for _ in range(num_users)]

        user_ids = [insert_user(cursor, user) for user in users]
        product_ids = [insert_product(cursor, product) for product in products]

        # Simulate user interactions
        for _ in range(num_clicks):
            user_id = random.choice(user_ids)
            product_id = random.choice(product_ids)

            # Update user and product records randomly
            if random.random() < 0.1:
                update_record(cursor, 'users', user_id)
            if random.random() < 0.05:
                update_record(cursor, 'products', product_id)

            click_data = generate_click_data(user_id, product_id)
            print('Click Event:', click_data)

            # Simulate checkout with a more realistic probability
            if random.random() < 0.2:  # 20% chance of checkout after click
                checkout_data = generate_checkout_data(user_id, product_id)
                print('Checkout Event:', checkout_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate e-commerce user and click data.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of user records to generate.")
    parser.add_argument("--num_clicks", type=int, default=1000, help="Number of click records to generate.")
    args = parser.parse_args()

    main(args.num_users, args.num_clicks)
