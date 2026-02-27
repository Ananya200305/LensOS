from app.db.repository.userRepo import UserRepository
from app.db.schema.user import UserInCreate, UserInLogin, UserOutput, UserWithToken
from app.core.security.hashhelper import Hashhelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserService:
    def __init__(self, session: Session):
        self.__userRepo = UserRepository(session=session)

    def signup(self, user_data: UserInCreate) -> UserOutput:
        if self.__userRepo.user_exist_by_email(email=user_data.email):
            raise HTTPException(status_code=400, detail="User with this email already exist")
        
        hashed_password = Hashhelper.get_password_hash(plain_password=user_data.password)
        user_data.password = hashed_password

        return self.__userRepo.create_user(user_data=user_data)
    
    def login(self, login_data: UserInLogin) -> UserWithToken:
        if not self.__userRepo.user_exist_by_email(email=login_data.email):
            raise HTTPException(status_code=400, detail="Please create an Account first")
        
        user = self.__userRepo.get_user_by_email(email=login_data.email)
        if Hashhelper.verify_password(plain_password=login_data.password, hashed_password=user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="Error while generating token")
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    def get_user_by_id(self, user_id: int):
        user = self.__userRepo.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")

