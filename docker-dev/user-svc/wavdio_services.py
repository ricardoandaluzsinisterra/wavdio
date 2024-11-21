import requests
from exceptions import *
from werkzeug.security import generate_password_hash, check_password_hash

def validate_user(username, password, confirm_password):
    if password != confirm_password:
        raise LoginError("Passwords do not match.")
    response = requests.get(f'http://localhost/catalog/users/{username}')
    if response.status_code == 200 and response.json():
        raise LoginError("Registration failed. Please try again.")
    return None

def register_user(username, password):
    hashed_password = generate_password_hash(password)
    user_data = {
        'username': username,
        'password': hashed_password
    }
    response = requests.post('http://localhost/catalog/users', json=user_data)
    if response.status_code != 201:
        raise LoginError(f'Failed to register user: {response.status_code}')
    return None

def check_user(username, password):
    response = requests.get(f'http://localhost/catalog/users/{username}')
    if response.status_code != 200:
        raise LoginError("Login failed. Please try again.")
    user = response.json()
    hashed_password = user.get('password')
    if hashed_password and check_password_hash(hashed_password, password):
        return None
    else:
        raise LoginError("Login failed. Please try again.")