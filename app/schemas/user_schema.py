import re

class UserSchema:
    @staticmethod
    def validate_registration(data):

        errors = {}

        if not data:
            return {
                "error":"Request body is required"
            }
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        #user name validation
        if not username:
            errors["username"]="Username is required"

        elif len(username)<3:
            errors["username"]= (
                "Username must contain at least 3 characters"
            )

        # Email validation
        if not email:
            errors["email"]="Email is required"

        elif not re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email
        ):
            errors["email"]= "Invalid Email address"
        
        # Password
        if not password:
            errors["password"] = "Password is required"
        
        elif len(password) < 8:
            errors["password"] = (
                "Password must contain at least 8 characters"
            )
        return errors
    
    @staticmethod
    def validate_login(data):
        errors = {}

        if not data:
            return {
                "error":"Request body is required"
            }
        username = data.get("username")
        password = data.get("password")

        if not username:
            errors["username"] = "Username is required"

        if not password:
            errors["password"] = "Password is required"
        
        return errors
