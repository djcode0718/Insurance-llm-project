import bcrypt
from sqlalchemy.orm import Session
from auth.models import User
from sqlalchemy.exc import IntegrityError

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# def register_user(db: Session, username: str, email: str, password: str) -> dict:
#     user = User(username=username, email=email, password_hash=hash_password(password))
#     db.add(user)
#     try:
#         db.commit()
#         db.refresh(user)
#         return {"success": True, "user_id": user.id}
#     except IntegrityError:
#         db.rollback()
#         return {"success": False, "error": "Username or email already exists."}
def register_user(db, username, email, password):
    # Check if username or email already exists
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        if existing_user.username == username:
            return {"success": False, "error": "Username is already taken."}
        elif existing_user.email == email:
            return {"success": False, "error": "Email is already registered."}

    # Hash password and create user
    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    return {"success": True}

def authenticate_user(db: Session, username: str, password: str) -> dict:
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password_hash):
        return {"success": True, "user_id": user.id}
    return {"success": False, "error": "Invalid credentials."}
