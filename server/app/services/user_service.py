from ..database import users_collection
from .auth_service import auth_service
from bson import ObjectId

class UserService:
    @staticmethod
    def create_user(email: str, password: str) -> dict:
        """Create a new user"""
        hashed_password = auth_service.hash_password(password)
        user = {
            "email": email,
            "hashed_password": hashed_password
        }
        result = users_collection.insert_one(user)
        return {"id": str(result.inserted_id), "email": email}
    
    @staticmethod
    def get_user_by_email(email: str) -> dict | None:
        """Get user by email"""
        user = users_collection.find_one({"email": email})
        if user:
            user["id"] = str(user["_id"])
        return user
    
    @staticmethod
    def get_user_by_id(user_id: str) -> dict | None:
        """Get user by ID"""
        try:
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
            return user
        except:
            return None
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> dict | None:
        """Authenticate user with email and password"""
        user = UserService.get_user_by_email(email)
        if not user:
            return None
        if not auth_service.verify_password(password, user["hashed_password"]):
            return None
        return user

user_service = UserService()