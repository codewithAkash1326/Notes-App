import jwt
from fastapi import Depends, Header, HTTPException , Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.settings import settings
from src.user.models import User
from jwt import ExpiredSignatureError , InvalidTokenError


def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("Authorization")

        print("step1")

        if not token:
            raise HTTPException(status_code=401, detail="Missing token")


        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        payload = jwt.decode(
            token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        print("step2")

        user_id = payload.get("_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")