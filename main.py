from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080:",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@app.get("/allposts/", response_model=List[PostResponse])
async def posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@app.get("/users/{name}/", response_model=DbUser)
async def posts(name: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == name).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.get("/allusers/", response_model=List[DbUser])
async def users(db: Session = Depends(get_db)):
    return db.query(User).all()

# class UserCreate(BaseModel):
#     name: Annotated[
#         str, Field(..., title='User name', min_length=2, max_length=20)
#     ]
#     age: Annotated[int, Field(..., title='Age of user', ge=1, le=120)]


# users = [
#     {'id': 1, 'name': 'John', 'age': 34},
#     {'id': 2, 'name': 'Alex', 'age': 12},
#     {'id': 3, 'name': 'David', 'age': 45}
# ]
#
# posts = [
#     {'id': 0, 'title': 'News 1', 'body': 'Text 1', 'author': users[0]},
#     {'id': 2, 'title': 'News 2', 'body': 'Text 1', 'author': users[1]},
#     {'id': 153, 'title': 'News 3', 'body': 'Text 1', 'author': users[2]},
# ]


# @app.get("/items")
# async def items() -> List[Post]:
#     return [Post(**post) for post in posts]
#
#
# @app.post("/items/add")
# async def add_item(post: PostCreate) -> Post:
#     author = next((user for user in users if user['id'] == post.author_id), None)
#     if not author:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     new_post_id = len(posts) + 1
#
#     new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
#     posts.append(new_post)
#     return Post(**new_post)
#
#
# @app.post("/user/add")
# async def user_add(user: Annotated[
#     UserCreate,
#     Body(..., example={
#         "name": "UserName",
#         "age": 18,
#     })
# ]) -> User:
#     new_user_id = len(users) + 1
#
#     new_user = {'id': new_user_id, 'name': user.name, 'age': user.age, }
#     users.append(new_user)
#     return User(**new_user)
#
#
# @app.get("/items/{id}")
# async def item(id: Annotated[int, Path(..., title='Tut ukazivaetsa id posta', ge=1, lt=100)]) -> Post:
#     for post in posts:
#         if post['id'] == id:
#             return Post(**post)
#
#
# @app.get("/search")
# async def search(post_id: Annotated[
#     Optional[int],
#     Query(title='ID of post to search for', ge=1, tl=50)
# ]) -> Dict[str, Optional[Post]]:
#     if post_id:
#         for post in posts:
#             if post['id'] == post_id:
#                 return {"data": Post(**post)}
#
#         raise HTTPException(status_code=404, detail="Post not found")
#     else:
#         return {"data": None}
