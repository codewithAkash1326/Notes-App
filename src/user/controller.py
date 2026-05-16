
from fastapi import Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserPayload , CreateNotePayload
from pwdlib import PasswordHash
from src.user.models import User , Note , SharedNote
from src.utils.settings import settings
from datetime import datetime , timedelta
import jwt


password_hash = PasswordHash.recommended()
 
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

def share_note(note_id:int , email: str, user: User, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Note not found"
            }
        )

    if note.owner_id != user.id:
        return JSONResponse(
            status_code=403,
            content={
                "message": "You are not authorized to share this note"
            }
        )
    
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        return JSONResponse(
            status_code=404,
            content={
                "message": "User not found with this email"
            }
        )
    
    is_shared = db.query(SharedNote).filter(SharedNote.note_id == note_id, SharedNote.user_id == db_user.id).first()

    if is_shared:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Note already shared with this user"
            }
        )
    
    new_share = SharedNote(
        note_id=note_id,
        user_id=db_user.id
    )


    db.add(new_share)
    db.commit()
    db.refresh(new_share)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Note shared successfully"
        }
    )
     
    


def get_note_by_id(id:int , user:User , db:Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == id).first()

    if not db_note:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Note not found"
            }
        )
    
    is_shared = db.query(SharedNote).filter(SharedNote.note_id == id, SharedNote.user_id == user.id).first()
    
    if db_note.owner_id != user.id and not is_shared:
        return JSONResponse(
            status_code=403,
            content={
                "message": "You are not authorized to view this note"
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "id": db_note.id,
            "title": db_note.title,
            "content": db_note.content,
            "created_at": str(db_note.created_at),
            "updated_at": str(db_note.updated_at)
        }
    )



def delete_note(id:int , user:User , db:Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == id).first()

    if not db_note:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Note not found"
            }
        )
    
    if db_note.owner_id != user.id:
        return JSONResponse(
            status_code=403,
             content = {
                "message": "You are not authorized to delete this note"
            }
        )
    
    db.delete(db_note)
    db.commit()

    return JSONResponse(
        status_code=204,
        content = {
            "message": "Note deleted successfully"
        }
    )


def update_note(id:int , note:CreateNotePayload , user:User , db:Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == id).first()

    if not db_note:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Note not found"
            }
        )
    
   
    if db_note.owner_id != user.id:
        return JSONResponse(
            status_code=403,
            content={
                "message": "You are not authorized to update this note"
            }
        )
    
    db_note.title = note.title
    db_note.content = note.content
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
             "title": db_note.title,
            "content": db_note.content,
            
        }
    )




 

def get_notes(user: User, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.owner_id == user.id).all()

    if not notes:
        return JSONResponse(
            status_code=200,
            content={
                "message": "No notes found",
                "data": []
            }
        )

    response = []

    for note in notes:
        response.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": str(note.created_at),
            "updated_at": str(note.updated_at)
        })

    return JSONResponse(
        status_code=200,
        content=  response
        
    )
 

def register_user(user:UserPayload, db: Session = Depends(get_db)):
    email_exist = db.query(User).filter(User.email == user.email).first()

    if email_exist:
        return JSONResponse(
            status_code = 409,
            content = {
                "message": "Email already exist"
            
            }
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email = user.email,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        status_code = 201,
        content = {
            "message": "User created successfully"
        }
    )


def login_user(user: UserPayload, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid email or password"
            }
        )
    
    if not verify_password(user.password, db_user.password):
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid email or password"
            }
        )
    
    exp_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token = jwt.encode({"_id":db_user.id , "exp":exp_time.timestamp() } , settings.TOKEN_SECRET_KEY , settings.ALGORITHM)
    

    return {
        "token":token
    }
    
    


def create_note(note: CreateNotePayload, db: Session, current_user: User):
    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )

    db.add(new_note)

    db.commit()

    db.refresh(new_note)

    return JSONResponse(
        status_code=201,
        content={
            "id": new_note.id,
            "title": new_note.title,
            "content": new_note.content,
            "created_at": str(new_note.created_at),
            "updated_at": str(new_note.updated_at)
        }
    )