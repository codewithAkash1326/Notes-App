from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller
from src.user.models import User
from src.utils.helpers import is_authenticated
from src.user.dtos import UserPayload , CreateNotePayload , ShareNotePayload

api_router = APIRouter()

@api_router.post('/register')
def register_user(user : UserPayload , db : Session = Depends(get_db)):
    return controller.register_user(user , db)


@api_router.post('/login')
def login_user(user: UserPayload, db: Session = Depends(get_db)):
    return controller.login_user(user , db)
     

@api_router.post('/notes')
def create_note( note: CreateNotePayload, db: Session = Depends(get_db), current_user: User = Depends(is_authenticated)):
    return controller.create_note(note, db, current_user)

@api_router.get('/notes')
def get_notes(user: User = Depends(is_authenticated) , db: Session = Depends(get_db)):
    return controller.get_notes(user,db)

@api_router.get('/notes/{id}')
def get_note_by_id(id:int ,user:User = Depends(is_authenticated) , db:Session = Depends(get_db)):
    return controller.get_note_by_id(id,user,db);

@api_router.put('/notes/{id}')
def update_note(id:int , note:CreateNotePayload , user:User = Depends(is_authenticated) , db:Session = Depends(get_db)):
    return controller.update_note(id,note,user,db);

@api_router.delete('/notes/{id}')
def delete_note(id:int , user:User = Depends(is_authenticated) , db:Session = Depends(get_db)):
    return controller.delete_note(id,user,db);

@api_router.post('/notes/{note_id}/share')
def share_note(note_id:int , body: ShareNotePayload, user: User = Depends(is_authenticated), db: Session = Depends(get_db)):
    return controller.share_note(note_id, body.email, user, db)
