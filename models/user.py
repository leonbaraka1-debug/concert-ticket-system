import hashlib
import json
import os

# Path to the JSON database file
USERS_FILE = "data/users.json"

# This is the main user class
class User:
    def __init__(self, username, password, role="User"):
        self.username = username
        self.password_hash = self._hash_password(password) # Securely hash the password using SHA-256 for data protection (turns it into mixed words and letters)
        self.role = role # Supports role-based access control ("Admin" or "User")

    @staticmethod
    # Transforms plain text passwords into a secure hexadecimal hash string.
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hex_digest() if hasattr(hashlib.sha256(password.encode()), 'hex_digest') else hashlib.sha256(password.encode()).hexdigest()
    
    # This validates an incoming password to the stored hash.
    def check_password(self, password):
        return self.password_hash == self._hash_password(password)
    
    # Serializes the User object into a dictionary for JSON storage.
    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role
        }

    # Deserializes dictionary records from JSON back into a User object.
    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"], "", data.get("role", "User"))
        user.password_hash = data["password_hash"]
        return user


# Reads all user records from the JSON storage file into memory.
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            return {username: User.from_dict(info) for username, info in data.items()}
    except json.JSONDecodeError:
        return {}

# Writes the current dictionary of users back to the JSON file.
def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    data = {username: user.to_dict() for username, user in users.items()}
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Handles new user sign-up and prevents duplicate usernames.
def register_user(username, password, role="User"):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = User(username, password, role)
    save_users(users)
    return True, "User registered successfully."

# Authenticates a user by verifying their credentials against saved data.
def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."
    user = users[username]
    if user.check_password(password):
        return True, user
    return False, "Incorrect password."