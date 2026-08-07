import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Fetch DATABASE_URL from Render Environment Variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Render postgres URLs sometimes start with "postgres://", which psycopg2 requires as "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


def get_db():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set on Render.")
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


def init_db():
    if not DATABASE_URL:
        print("DATABASE_URL not found, skipping database initialization.")
        return

    conn = get_db()
    cursor = conn.cursor()

    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            gender VARCHAR(20),
            age INTEGER,
            income REAL,
            spending INTEGER,
            cluster INTEGER,
            label VARCHAR(100),
            description TEXT,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    init_db()
