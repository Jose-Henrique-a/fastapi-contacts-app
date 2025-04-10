
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# adiciona middleware cors
from fastapi.middleware.cors import CORSMiddleware

# comentar aqui para quebrar o deploy
from . import models, database

# Rodar com : python -m uvicorn app.main:app --reload

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # Permite todas as origens + null explicitamente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para gerenciar as sessões do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao aplicativo FastAPI Contacts!"}



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


# Atualizacao abaixo para CRUD
#atualização do API <<<<<<<<<<<
# Atualizar um usuário
# Substitua os endpoints PUT existentes por estes
@app.put("/users/{user_id}")
async def update_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data = await request.json()
    if "name" in data and data["name"]:
        user.name = data["name"]
    if "email" in data and data["email"]:
        user.email = data["email"]
    db.commit()
    db.refresh(user)
    return user

@app.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, request: Request, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    data = await request.json()
    if "name" in data and data["name"]:
        contact.name = data["name"]
    if "phone" in data and data["phone"]:
        contact.phone = data["phone"]
    if "email" in data and data["email"]:
        contact.email = data["email"]
    if "user_id" in data and data["user_id"]:
        contact.user_id = data["user_id"]
    db.commit()
    db.refresh(contact)
    return contact

# Deletar um usuário
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Deletar um contato
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}
