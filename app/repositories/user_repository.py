from app.config.database import db
from app.models.user import User

class Userrepository:
    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User,user_id)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(
            username=username
            ).first()
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(
            email=email
            ).first()
    
    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def update_password(username, password_hash):
        # find the user
        user = db.session.get(User,username)
        if user is None:
            return None
        user.password_hash = password_hash
        db.session.commit()
        db.session.refresh(user)
        return user
    
    @staticmethod
    def delete_user(user_id):
        user =db.session.get(User,user_id)
        if user is None:
            return None
        db.session.delete(user)
        db.session.commit()
        return user

