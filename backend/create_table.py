import psycopg2
from config import load_config

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_email VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL,
            user_role VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            product_description VARCHAR(255) NOT NULL,
            product_price DECIMAL(10,2) NOT NULL,
            product_quantity INT NOT NULL,
            product_image VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_products (
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, product_id),
            CONSTRAINT fk_user
                FOREIGN KEY (user_id)
                REFERENCES users (user_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            CONSTRAINT fk_product
                FOREIGN KEY (product_id)
                REFERENCES products (product_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """
    )

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error:", error)

if __name__ == '__main__':
    create_tables()
