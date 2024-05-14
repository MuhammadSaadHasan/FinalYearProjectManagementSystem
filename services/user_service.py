from models.models import db, User
from werkzeug.security import generate_password_hash

def create_user(username, email, password,type):
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password, type=type)
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        print(str(e))  
        return None
