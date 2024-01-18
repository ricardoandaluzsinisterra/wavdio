import mysql.connector
# How do I encrypt passwords on my database?
from werkzeug.security import generate_password_hash

db = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="jese",
  database="db"
)

def register_user(username, password):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        return "Registration failed. Please try again."
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    db.commit()
    return None