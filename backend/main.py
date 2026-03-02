from fastapi import Depends, FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.utils.init_db import create_tables
from app.routers.auth import authRouter
from app.routers.asset import assetRouter
from app.utils.protectRoute import get_current_user
from app.db.schema.user import UserOutput
from app.service.storageService import upload_file_to_s3

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("created")
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=authRouter, tags=["auth"], prefix="/auth")
app.include_router(router=assetRouter, tags=["asset"], prefix="/asset")
#/auth/login
#/auth/signup


@app.get("/protected")
def read_protected(user: UserOutput = Depends(get_current_user)):
    return{"message" : user}

@app.post("/test-upload")
def test_upload(file: UploadFile = File(...)):
    """
    Temporary endpoint to test S3 upload
    """
    url = upload_file_to_s3(file, user_id=1)
    return {"image_url": url}