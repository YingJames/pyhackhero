# from werkzeug.security import generate_password_hash

# username = "admin1"
# email = "admin1@example.com"
# password = "password"

# hashed_password = generate_password_hash(password)

# print(f"INSERT INTO Users (Username, Email, HashPW) VALUES ('{username}', '{email}', '{hashed_password}');")


"""
This file is used to generate hashed password so the database admin user can manually insert hashed passwords
when creating an admin's account on hackhero db.
"""
import uuid
from werkzeug.security import generate_password_hash

def hash_password(password):
    hashed_pass = generate_password_hash(password)
    return hashed_pass

if __name__ == "__main__":
    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password to hash: ")
    uid = uuid.uuid4()
    hashed_password_input = hash_password(password)
    print("Hashed Password:", hashed_password_input)
    print(f"INSERT INTO Users (UID, Username, Email, HashPW) VALUES ('{uid}', '{username}', '{email}', '{hashed_password_input}');")
    print(f"INSERT INTO Admins (UID) VALUES ('{uid}');")