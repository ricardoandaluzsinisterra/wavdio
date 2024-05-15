import redis
# How do I encrypt and check passwords on my database?
from werkzeug.security import generate_password_hash, check_password_hash

r=redis.Redis(host='users-db', port=6379, db=0)

def validate_user(username, password, confirm_password):
        if password != confirm_password:
            return "Passwords do not match."
        if r.exists(f"user:{username}:password"):
            return "Registration failed. Please try again."
        return None

def register_user(username, password):
    hashed_password = generate_password_hash(password)
    r.set(f"user:{username}:password", hashed_password)
    return None

def check_user(username, password):
    hashed_password = r.get(f"user:{username}:password")
    if hashed_password and check_password_hash(hashed_password.decode('utf-8'), password):
        return None
    else:
        return "Login failed. Please try again."
