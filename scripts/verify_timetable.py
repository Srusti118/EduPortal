import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, Timetable, Course

def verify_timetable():
    with app.app_context():
        print("Verifying Timetable Logic...")

        # 1. Find a target student (Division C, Semester 4)
        # We need to find or create one for testing.
        # Let's search for any student with Division C.
        student = Student.query.filter_by(division='C', current_semester=4).first()
        
        if not student:
            print("No student found with Division C, Semester 4. Creating a test student.")
            # We need a user first.
            from models import User
            user = User.query.filter_by(username='test_student_c').first()
            if not user:
                 # Minimal user creation (omitting details for brevity)
                 print("Please ensure a valid student exists. Skipping automatic creation to avoid side effects.")
                 # Let's try finding ANY student and temporarily patching them or just simulating the query.
                 print("Simulating query with mock student data: Division=C, Batch=C1, Branch=CSE")
                 
                 class MockStudent:
                     branch = 'CSE'
                     current_semester = 4
                     division = 'C'
                     batch = 'C1'
                 
                 student = MockStudent()
        else:
            print(f"Found Student: {student.roll_number}, Div: {student.division}, Batch: {student.batch}")

        # 2. Run the Query Logic
        current_academic_year = '2025-26'
        
        query = Timetable.query.join(Course).filter(
            (Course.course_name == student.branch) | (Course.course_code == student.branch),
            Timetable.semester == student.current_semester,
            Timetable.academic_year == current_academic_year
        )
        
        if student.division:
            query = query.filter(
                (Timetable.division == student.division) | (Timetable.division == None)
            )
            
        if student.batch:
             query = query.filter(
                (Timetable.batch == student.batch) | (Timetable.batch == None)
            )
            
        entries = query.all()
        print(f"Found {len(entries)} timetable entries.")
        
        # 3. Validation
        # Check specific entry: Monday 08:45-09:45
        target_slot = "08:45 AM-09:45 AM"
        monday_entry = next((e for e in entries if e.day_of_week == 'monday' and e.time_slot == target_slot), None)
        
        if monday_entry:
            print(f"Monday {target_slot}: {monday_entry.subject.subject_name} ({monday_entry.batch})")
            # For Batch C1, it should be FCSP-1 (Based on CSV)
            if student.batch == 'C1' and 'FCSP-1' in monday_entry.subject.subject_name:
                print("SUCCESS: Retrieved correct subject for Batch C1.")
            else:
                print(f"CHECK: Expected FCSP-1 for C1, got {monday_entry.subject.subject_name}")
        else:
            print(f"WARNING: No entry found for Monday {target_slot}")

        # Check filtering: Ensure we don't see C2 entries if we are C1
        c2_entry = next((e for e in entries if e.batch == 'C2'), None)
        if c2_entry:
             print(f"FAILURE: Found entry for Batch C2: {c2_entry.subject.subject_name}")
        else:
             print("SUCCESS: Correctly filtered out other batches.")

if __name__ == '__main__':
    verify_timetable()
