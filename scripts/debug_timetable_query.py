import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, Timetable, Course

def debug_student_query():
    with app.app_context():
        # Target: PATEL JIMIT DINESHBHAI (Batch A1?)
        username = '24002170110118' 
        print(f"--- Debugging Timetable Query for User {username} ---")
        
        student = Student.query.filter(Student.enrollment_number == username).first()
        if not student:
            print("Student not found!")
            return
            
        print(f"Student Profile:")
        print(f"  ID: {student.id}")
        print(f"  Branch: '{student.branch}'")
        print(f"  Semester: {student.current_semester}")
        print(f"  Division: '{student.division}'")
        print(f"  Batch: '{student.batch}'")
        
        current_year = '2025-26'
        
        # 1. Check Course Match
        print("\nChecking Course Match...")
        course_matches = Course.query.filter(
            (Course.course_name == student.branch) | (Course.course_code == student.branch)
        ).all()
        
        if not course_matches:
            print(f"  [FAIL] No Course found matching branch '{student.branch}'")
        else:
            for c in course_matches:
                print(f"  [OK] Matches Course: {c.course_name} (ID: {c.id})")

        # 2. Build Query Incrementally
        print("\nBuilding Query...")
        base_query = Timetable.query.join(Course)
        
        # Filter by Course
        q1 = base_query.filter(
             (Course.course_name == student.branch) | (Course.course_code == student.branch)
        )
        c1 = q1.count()
        print(f"  Entries matching Course: {c1}")
        
        # Filter by Semester
        q2 = q1.filter(Timetable.semester == student.current_semester)
        c2 = q2.count()
        print(f"  Entries matching Sem {student.current_semester}: {c2}")
        
        # Filter by Year
        q3 = q2.filter(Timetable.academic_year == current_year)
        c3 = q3.count()
        print(f"  Entries matching Year {current_year}: {c3}")
        
        # Filter by Division
        if student.division:
            q4 = q3.filter((Timetable.division == student.division) | (Timetable.division == None))
            c4 = q4.count()
            print(f"  Entries matching Div {student.division}: {c4}")
        else:
            q4 = q3
            
        # Filter by Batch
        if student.batch:
            q5 = q4.filter((Timetable.batch == student.batch) | (Timetable.batch == None))
            c5 = q5.count()
            print(f"  Entries matching Batch {student.batch}: {c5}")
        else:
            q5 = q4
            
        final_entries = q5.all()
        print(f"\nFinal Result: {len(final_entries)} entries found.")
        
        if len(final_entries) == 0:
            print("  Likely cause: The filter step where count dropped to 0.")

if __name__ == '__main__':
    debug_student_query()
