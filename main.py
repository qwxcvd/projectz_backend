from fastapi import FastAPI, HTTPException
import uvicorn

from validator import validate_email

app = FastAPI()


@app.get("/authorize")
async def authorize(email: str):
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Email not valid")
    return {"email": email}


if __name__ == "__main__":
    uvicorn.run(app)
