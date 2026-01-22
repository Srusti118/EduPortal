import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Faculty
from werkzeug.security import generate_password_hash

def fix_aks_user():
    with app.app_context():
        print("Fixing AKS User mapping...")
        
        # Find AKS
        aks = Faculty.query.filter_by(faculty_id='AKS').first()
        if not aks:
            print("AKS not found.")
            return

        print(f"Current AKS: ID={aks.id}, UserID={aks.user_id}")
        
        # Check if user is being shared
        shared_count = Faculty.query.filter_by(user_id=aks.user_id).count()
        print(f"User ID {aks.user_id} is shared by {shared_count} faculty.")
        
        if shared_count > 1:
            # Create new user for AKS
            print("Creating unique user for AKS...")
            new_user = User(
                username='prof.aks',
                email='aks@college.edu',
                password_hash=generate_password_hash('password'),
                role='faculty',
                full_name='Prof. AKS',
                department='Computer Science'
            )
            db.session.add(new_user)
            db.session.flush()
            
            # Update AKS
            aks.user_id = new_user.id
            db.session.commit()
            print(f"Updated AKS to use User ID {new_user.id}")
            
        else:
            print("AKS already has a unique user (or shared count is 1).")

if __name__ == '__main__':
    fix_aks_user()
