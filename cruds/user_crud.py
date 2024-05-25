from models import db, User
from sqlalchemy.exc import SQLAlchemyError

def create_user(data):
    try:
        new_user = User(
            Username=data['Username'],
            Email=data['Email'],
            PhoneNumber=data['PhoneNumber'],
            ProfilePicture=data.get('ProfilePicture', ''),  
            Bio=data.get('Bio', '')  
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")

def get_users():
    try:
        return User.query.all()
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")

def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")

def update_user(user_id, data):
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        user.Username = data.get('Username', user.Username)
        user.Email = data.get('Email', user.Email)
        user.PhoneNumber = data.get('PhoneNumber', user.PhoneNumber)
        user.ProfilePicture = data.get('ProfilePicture', user.ProfilePicture)
        user.Bio = data.get('Bio', user.Bio)

        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")

def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        db.session.delete(user)
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")
