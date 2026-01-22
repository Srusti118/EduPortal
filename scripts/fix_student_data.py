import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, User, Course

def fix_student_data():
    with app.app_context():
        print("--- Fixing Student Data for Timetable Verification ---")
        
        # 1. Find a target student user
        # Let's try to find a user 'student' or create/pick one.
        # We'll just pick the student with ID 1 or the first one we find.
        student = Student.query.first()
        
        if not student:
            print("No students found in DB. Please seed students first.")
            return

        print(f"Updating Student: {student.user.full_name} (Roll: {student.roll_number})")
        print(f"Old Data: Sem={student.current_semester}, Div={student.division}, Batch={student.batch}, Branch={student.branch}")
        
        # 2. Update to match Timetable
        # Timetable is for: Sem 4, Div C, Batch C1, Course 'Computer Science Engineering'
        
        # Ensure 'Computer Science Engineering' course exists to get exact name
        cse_course = Course.query.filter(Course.course_name.like('%Computer Science%')).first()
        target_branch = cse_course.course_name if cse_course else 'Computer Science Engineering'
        
        student.current_semester = 4
        student.division = 'C'
        student.batch = 'C1'
        student.branch = target_branch 
        
        db.session.commit()
        
        print(f"New Data: Sem={student.current_semester}, Div={student.division}, Batch={student.batch}, Branch={student.branch}")
        print("Student updated successfully. Please log in as this student to verify.")
        
        # Print login info if possible
        print(f"Login Username: {student.user.username}")

if __name__ == '__main__':
    fix_student_data()
