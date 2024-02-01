import asyncpg
from db import sql_queries
from config import POSTGRES_URL

async def create_tables():
    global pool
    pool = await asyncpg.create_pool(POSTGRES_URL)
    async with pool.acquire() as connection:
        try:
            await connection.execute(sql_queries.CREATE_TABLE_PRODUCTS)
            await connection.execute(sql_queries.CREATE_TABLE_PHOTO_OF_PRODUCTS)
            await connection.execute(sql_queries.CREATE_TABLE_PREORDERS)
            await connection.execute(sql_queries.CREATE_TABLE_PHOTO_OF_PREORDERS)
            await connection.execute(sql_queries.CREATE_TABLE_REVIEW)

            print("База данных успешно подключена и таблицы созданы")
        finally:
            await pool.release(connection)

async def save_product_info(state):
    async with pool.acquire() as connection:
        async with state.proxy() as data:
            values = (
                data['info'],
                data['category'],
                data['article_number'],
                data['quantity'],
                data['price'],
            )
            await connection.execute(sql_queries.PRODUCT_INSERT_QUERY, *values)

async def save_product_photo(product_id, photo):
    async with pool.acquire() as connection:
        values = (
            product_id,
            photo,
        )
        await connection.execute(sql_queries.PRODUCT_PHOTO_INSERT_QUERY, *values)

async def save_preorder_info(state):
    async with pool.acquire() as connection:
        async with state.proxy() as data:
            values = (
                data['info'],
                data['category'],
                data['product_release_date'],
                data['price'],
                data['preorder_article'],
                data['quantity'],
            )
            await connection.execute(sql_queries.PREORDERS_INSERT_QUERY, *values)


async def save_preorder_photo(product_id, photo):
    async with pool.acquire() as connection:
        values = (
            product_id,
            photo,
        )
        await connection.execute(sql_queries.PREORDERS_PHOTO_INSERT_QUERY, *values)

async def get_last_inserted_product_id():
    async with pool.acquire() as connection:
        return await connection.fetchval("SELECT lastval()")

async def save_reviews_info(state):
    async with pool.acquire() as connection:
        async with state.proxy() as data:
            values = (
                data['article_number'],
                data['info_product'],
                data['review'],
                data['photo_review'],
            )
            await connection.execute(sql_queries.REVIEWS_INSERT_QUERY, *values)

async def get_all_reviews(pool):
    async with pool.acquire() as connection:
        return await connection.fetch(sql_queries.ALL_REVIEWS_FOR_DIRECTORS)

async def delete_product(product_id):
    product_id = int(product_id)
    async with pool.acquire() as connection:
        await connection.execute(sql_queries.DELETE_PRODUCT_QUERY, product_id)