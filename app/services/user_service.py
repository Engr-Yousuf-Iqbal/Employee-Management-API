from app.models.user import User
from app.repositories.user_repository import Userrepository
from app.utils.password import  hash_password, verify_password

class UserService:

    @staticmethod
    def register_user(
        username, email, password
    ):
        # Check username
        existing_username = (Userrepository.get_by_username(username))
        if existing_username:
            raise ValueError(
                "Username already exists"
            )
        
        # Check email 
        existing_email = (Userrepository.get_by_email(email))
        if existing_email:
            raise ValueError(
                "Email already exists"
            )
        
        
        # Create user
        user = User(
            username = username,
            email = email,
            role = "Employee",
            password_hash=hash_password(password)
        )

        # Save user
        Userrepository.create(user)
        return user
    @staticmethod
    def authenticate_user(username, password):
        user = Userrepository.get_by_username(username)
        if not user:
            return None
        if not user.is_active:
            return None
        if not verify_password(password,user.password_hash):
            return None
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return Userrepository.get_by_id(user_id)