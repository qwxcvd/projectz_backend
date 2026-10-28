from sqlalchemy import String, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedColumn

engine = create_async_engine("sqlite+aiosqlite:///db.sqlite", future=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    email = MappedColumn(String, primary_key=True)
    code = MappedColumn(Integer)


async def get_db():
    async with async_session() as session:
        yield session