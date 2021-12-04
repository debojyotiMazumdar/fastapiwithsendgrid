import jwt
from datetime import datetime, timedelta
#import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
security_algo = os.getenv("SECURITY_ALGO")


def generate_token(email):
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60   # Expired after 1 hour
    )
    to_encode = {
        "exp": expire, "email": email
    }

    encoded = jwt.encode(to_encode, secret_key, security_algo)
    return encoded


def decode_token(token):
    decoded = jwt.decode(token, secret_key, security_algo)
    return decoded
