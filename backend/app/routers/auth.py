from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.db.schema.user import UserInCreate, UserInLogin, UserWithToken, UserOutput
from sqlalchemy.orm import Session
from app.service.userService import UserService

authRouter = APIRouter()

@authRouter.post("/login", status_code=200, response_model=UserWithToken)
def login(loginDetail: UserInLogin, session: Session = Depends(get_db)):
    try:
        return UserService(session=session).login(login_data=loginDetail)
    except Exception as error:
        print(error)
        raise error


@authRouter.post("/signup", status_code=201, response_model=UserOutput)
def signup(signupDetail: UserInCreate, session: Session = Depends(get_db)):
    try:
        return UserService(session=session).signup(user_data=signupDetail)
    except Exception as error:
        print(error)
        raise error

#router -> services -> repository -> db 
#router <- services <- repository <- db 