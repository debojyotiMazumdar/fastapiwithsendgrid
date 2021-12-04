from typing import Optional
from fastapi import FastAPI, Header
import fastapi
import jwt
from sqlmodel.orm.session import Session
from db import get_session, init_db
from models import User, User_Input, User_SignIn_Input
from fastapi.param_functions import Depends
from passlib.context import CryptContext
from utils.email import send_mail
from fastapi.security import OAuth2PasswordBearer

from utils.tokens import decode_token, generate_token


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
async def on_startup():
    init_db()


@app.get("/check_database/")
async def check():
    return "see pgadmin"


@app.post("/create_user/")
async def create_user(user_in: User_Input, session: Session = Depends(get_session)):
    hashed_password = pwd_context.hash(user_in.password)
    token = generate_token(user_in.email)
    user = User(name=user_in.name,
                email=user_in.email,
                password=hashed_password,
                verification_token=token,
                is_verified=False,
                session_token="")
    session.add(user)
    session.commit()
    session.refresh(user)
    verification_url = "http://127.0.0.1:8000/verifyuser/{}".format(token)
    subject = "to register for the demo application"
    message = "Hello <b>{}</b> please verify by clicking this ==> <a style='width: 100%; text-align: center;' href={}><button>Verify</button> <b><b> or please go to {}".format(
        user_in.name, verification_url, verification_url)
    send_mail(user_in.email, message, subject)
    return "verification email sent"


@app.put("/verifyuser/{token}/")
async def verify_user(token: str, session: Session = Depends(get_session)):
    print(token)
    decoded = decode_token(token)
    print("your decoded is:")
    print(decoded)
    user = session.query(User).filter(User.email == decoded["email"]).first()

    if user.is_verified == True:
        return True

    if user.verification_token == token:
        updated_user = session.query(User).filter(User.email == user.email).update(
            {User.is_verified: True, User.verification_token: ""}, synchronize_session="fetch")
        session.commit()
        return True
    return False


@app.post("/signin_user/")
async def signin_user(user_signin_input: User_SignIn_Input, session: Session = Depends(get_session)):
    user = session.query(User).filter(
        User.email == user_signin_input.email).first()
    if(user == None):
        return "Email does not exist"
    if user.is_verified == False:
        return "Your are not verified"

    if pwd_context.verify(user_signin_input.password, user.password):
        token = generate_token(user.email)
        updated_user = session.query(User).filter(User.email == user.email).update(
            {User.session_token: token}, synchronize_session="fetch")
        session.commit()
        return token
    else:
        return "Email and password do not match"


@app.put("/details_of_user/{token}")
async def details_of_user(token: str, session: Session = Depends(get_session), header_token: str = Header(None)):
    print("your token appears below:-")
    print(header_token)
    decoded = decode_token(token)
    user = session.query(User).filter(User.email == decoded["email"]).first()
    return user
