import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, Course
from werkzeug.security import generate_password_hash

def careful_update():
    with app.app_context():
        print("--- Careful Update: Sem=4, Pass=Student@123, Branch=CSE ---")
        
        students = Student.query.all()
        password_hash = generate_password_hash('Student@123')
        
        # Target Branch Name for Timetable Mapping
        # content of Course ID 1
        cse = Course.query.get(1)
        target_branch = cse.course_name if cse else 'Computer Science Engineering'
        print(f"Target Branch: {target_branch}")
        
        count = 0
        for s in students:
            s.current_semester = 4
            s.user.password_hash = password_hash
            s.branch = target_branch 
            # Note: We are NOT touching s.division or s.batch
            
            count += 1
            if count % 200 == 0:
                print(f"Updated {count} students...")
                
        db.session.commit()
        print(f"Successfully updated {count} students.")
        print("Preserved original Batch and Division assignments.")

if __name__ == '__main__':
    careful_update()
