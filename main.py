from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from email_sender import send_verification_code
from generate_code import generate_code
from models import User
from database import User as UserOrm
from validator import validate_email


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/authorize")
async def authorize(user_data: User, db: AsyncSession = Depends(get_db)):
    if not validate_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email not valid")
    code = generate_code()

    await send_verification_code(user_data.email, code)
    result = await db.execute(
        select(UserOrm).where(
            UserOrm.email == user_data.email
        )
    )

    verification = result.scalar_one_or_none()

    if verification:
        verification.code = code
    else:
        verification = UserOrm(
            email=user_data.email,
            code=code,
        )
        db.add(verification)

    await db.commit()

    return {"status": "ok", "message": f"Отправлен код на почту {user_data.email}"}


@app.post("/check_bd")
async def check_bd(user_data: User, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserOrm).where(UserOrm.email == user_data.email))
    return result.scalars().all()


if __name__ == "__main__":
    uvicorn.run(app)
