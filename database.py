import mysql.connector
from werkzeug.security import generate_password_hash

db = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="jese",
  database="users"
)

def register_user(username, password):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, generate_password_hash(password)))
    db.commit()