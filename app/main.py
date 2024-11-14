
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Contacts App!"}

# Função para gerenciar as sessões do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar um novo usuário
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Criar um novo contato
@app.post("/contacts/")
def create_contact(name: str, phone: str, email: str, user_id: int, db: Session = Depends(get_db)):
    contact = models.Contact(name=name, phone=phone, email=email, user_id=user_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

# Listar todos os usuários
@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Listar todos os contatos
@app.get("/contacts/")
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

# Obter os detalhes de um usuário específico pelo ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Obter os detalhes de um contato específico pelo ID
@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


