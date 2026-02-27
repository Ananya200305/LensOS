from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from app.utils.init_db import create_tables
from app.routers.auth import authRouter
from app.utils.protectRoute import get_current_user
from app.db.schema.user import UserOutput

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("created")
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")
#/auth/login
#/auth/signup


@app.get("/protected")
def read_protected(user: UserOutput = Depends(get_current_user)):
    return{"message" : user}

