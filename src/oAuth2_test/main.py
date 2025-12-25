import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Dummy authentication for demonstration
    if form_data.username == "user" and form_data.password == "password":
        return {"access_token": "dummy_token", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
