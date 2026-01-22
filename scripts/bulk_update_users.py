import sys
import os
import random

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, User, Faculty, Course
from werkzeug.security import generate_password_hash

def bulk_update_data():
    with app.app_context():
        print("--- Global Data Update ---")
        
        # 1. Update Student Passwords & Metadata
        print("Updating Students...")
        students = Student.query.all()
        student_password_hash = generate_password_hash('Student@123')
        
        # Ensure Course "Computer Science Engineering" exists
        cse_course = Course.query.filter(Course.course_name.like('%Computer Science%')).first()
        target_branch = cse_course.course_name if cse_course else 'Computer Science Engineering'
        
        divisions = ['A', 'B', 'C']
        
        for idx, s in enumerate(students):
            # Update Password
            s.user.password_hash = student_password_hash
            
            # Update Timetable Metadata (Distribute evenly)
            s.current_semester = 4
            s.branch = target_branch
            
            # Assign Division (Round Robin)
            div = divisions[idx % 3]
            s.division = div
            
            # Assign Batch (Simple logic: Div + '1')
            # The CSV has C1..C9, A1..A?, etc. We'll just put everyone in Batch 1 of their div for simplicity to ensure matches.
            s.batch = f"{div}1"
            
            if idx % 50 == 0:
                print(f"Processed {idx} students...")
                
        db.session.commit()
        print(f"Updated {len(students)} students: Password='Student@123', Sem=4, Div=A/B/C, Batch=X1")

        # 2. Update Faculty Passwords
        print("\nUpdating Faculty...")
        faculties = Faculty.query.all()
        faculty_password_hash = generate_password_hash('faculty123')
        
        for f in faculties:
            f.user.password_hash = faculty_password_hash
            
        db.session.commit()
        print(f"Updated {len(faculties)} faculties: Password='faculty123'")

if __name__ == '__main__':
    bulk_update_data()
