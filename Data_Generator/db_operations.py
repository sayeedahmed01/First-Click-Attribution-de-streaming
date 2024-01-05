import psycopg2
from faker import Faker

fake = Faker()
def connect_db():
    """Create a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname="your_dbname", user="your_username", password="your_password", host="your_host"
    )

def insert_user(cursor, user):
    """Insert a new user into the database."""
    query = """INSERT INTO commerce.users (user_id, name, email, location, signup_date)
               VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
    cursor.execute(query, (
        user['user_id'], user['name'], user['email'], user['location'], user['signup_date']
    ))
    return cursor.fetchone()[0]

def insert_product(cursor, product):
    """Insert a new product into the database."""
    query = """INSERT INTO commerce.products (product_id, name, category, price, details)
               VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
    cursor.execute(query, (
        product['product_id'], product['name'], product['category'], product['price'], product['details']
    ))
    return cursor.fetchone()[0]

def update_record(cursor, table, record_id):
    """Update a record in the database."""
    if table == 'users':
        query = "UPDATE commerce.users SET name = %s, email = %s WHERE id = %s;"
        cursor.execute(query, (fake.name(), fake.email(), record_id))
    elif table == 'products':
        query = "UPDATE commerce.products SET details = %s WHERE id = %s;"
        cursor.execute(query, (fake.sentence(), record_id))