CREATE_TABLE_PRODUCTS = '''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        info TEXT,
        category VARCHAR(255),
        article_number TEXT UNIQUE,
        quantity INTEGER,
        price DECIMAL(10, 2)
    );
'''

PRODUCT_INSERT_QUERY = """
    INSERT INTO products
    (info, category, article_number, quantity, price)
    VALUES ($1, $2, $3, $4, $5)
    ON CONFLICT DO NOTHING;
"""

CREATE_TABLE_PHOTO_OF_PRODUCTS = '''
    CREATE TABLE IF NOT EXISTS photos (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
        photo TEXT
    );
'''

PRODUCT_PHOTO_INSERT_QUERY = """
    INSERT INTO photos
    (product_id, photo)
    VALUES ($1, $2)
    ON CONFLICT DO NOTHING;
"""


CREATE_TABLE_PREORDERS = '''
    CREATE TABLE IF NOT EXISTS preorders (
        id SERIAL PRIMARY KEY,
        info TEXT,
        category VARCHAR(255),
        product_release_date VARCHAR(255),
        price DECIMAL(10, 2),
        preorder_article TEXT UNIQUE,
        quantity INTEGER
    );
'''

PREORDERS_INSERT_QUERY = """
    INSERT INTO preorders
    (info, category, product_release_date, price, preorder_article, quantity)
    VALUES ($1, $2, $3, $4, $5, $6)
    ON CONFLICT DO NOTHING;
"""

CREATE_TABLE_PHOTO_OF_PREORDERS = '''
    CREATE TABLE IF NOT EXISTS photos_preorders (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES preorders(id) ON DELETE CASCADE,
        photo TEXT
    );
'''

PREORDERS_PHOTO_INSERT_QUERY = """
    INSERT INTO photos_preorders
    (product_id, photo)
    VALUES ($1, $2)
    ON CONFLICT DO NOTHING;
"""


CREATE_TABLE_REVIEW = '''
    CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL PRIMARY KEY,
        article_number TEXT,
        info_product TEXT,
        review TEXT,
        photo_review TEXT
    );
'''

REVIEWS_INSERT_QUERY = """
    INSERT INTO reviews
    (article_number, info_product, review, photo_review)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT DO NOTHING;
"""

ALL_REVIEWS_FOR_DIRECTORS = """
    SELECT * FROM reviews
"""

DELETE_PRODUCT_QUERY = """
    DELETE FROM products WHERE id = $1;
"""

DELETE_PREORDER_QUERY = """
    DELETE FROM preorders WHERE id = $1;
"""