import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def reset_password():
    with app.app_context():
        username = '24002170110118' # PATEL JIMIT DINESHBHAI
        user = User.query.filter_by(username=username).first()
        if user:
            user.password_hash = generate_password_hash('password')
            db.session.commit()
            print(f"Password for {username} reset to 'password'")
        else:
            print(f"User {username} not found")

if __name__ == '__main__':
    reset_password()
