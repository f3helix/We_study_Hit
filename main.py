from fastapi import FastAPI, Query, Form, Depends
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from dataclasses import dataclass

# Для бази даних
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(debug=True)

# Статичні файли
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблони
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# Add user FORM
@app.get("/user/add/")
def add_get(request: Request):

    return templates.TemplateResponse("user_add.html", {"request": request})


# Add user POST
@app.post("/user/add/")
def add_user(login: str = Form(), name: str = Form(), surname: str = Form(), age: int = Form(), db: Session = Depends(get_db)):

    crud.create_user(db=db, user=schemas.UserCreate(login=login, name=name, surname=surname, age=age))

    return RedirectResponse("/", status_code=303)

# Edit user FORM
# @app.get("/user/edit/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     crud.get_user(user_id=user_id, db=db)

# @app.put("/user/edit/{user_id}")
# def edit_user(user_id: int, db: Session = Depends(get_db)):

#     crud.update_item(user_id=user_id, db=db)