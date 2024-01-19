import mysql.connector
# How do I encrypt and check passwords on my database?
from werkzeug.security import generate_password_hash, check_password_hash

db = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="jese",
  database="db"
)

def validate_user(username, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match."
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        return "Registration failed. Please try again."
    return None

def register_user(username, password):
    cursor = db.cursor()
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    db.commit()
    return None

def check_user(username, password):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user and check_password_hash(user[2], password):
        return None
    return "Invalid username or password."