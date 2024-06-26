async def get_product_from_category(pool, category):
    try:
        async with pool.acquire() as connection:
            products = await connection.fetch(
                """SELECT * FROM products
                WHERE category = $1""", category
            )
            return products
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None

async def get_product_photos(pool, product_id):
    try:
        async with pool.acquire() as connection:
            photos = await connection.fetch(
                """SELECT * FROM photos
                WHERE product_id = $1""", product_id
            )
            return photos
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return []

# =======================================================================================================================

async def get_preorder_from_category(pool, category):
    try:
        async with pool.acquire() as connection:
            products = await connection.fetch(
                """SELECT * FROM preorders
                WHERE category = $1""", category
            )
            return products
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None

async def get_preorder_photos(pool, product_id):
    try:
        async with pool.acquire() as connection:
            photos = await connection.fetch(
                """SELECT * FROM photos_preorders
                WHERE product_id = $1""", product_id
            )
            return photos
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return []

async def get_product_from_article(pool, article_number):
    try:
        async with pool.acquire() as connection:
            products = await connection.fetch(
                """SELECT * FROM products
                WHERE article_number = $1""", article_number
            )
            return products
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None

async def get_preorder_from_article(pool, preorder_article):
    try:
        async with pool.acquire() as connection:
            products = await connection.fetch(
                """SELECT * FROM preorders
                WHERE preorder_article = $1""", preorder_article
            )
            return products
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None