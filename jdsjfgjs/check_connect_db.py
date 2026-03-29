import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"

async def check_connection():
    """Проверка подключения к базе данных"""
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Подключение к базе данных успешно!")
            print(f"Результат запроса: {result.scalar()}")
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")

if __name__ == "__main__":
    asyncio.run(check_connection())
