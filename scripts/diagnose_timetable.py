import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, Timetable, Course

def diagnose_visibility():
    with app.app_context():
        print("--- Diagnostic: Student Timetable Visibility ---")
        
        # 1. Check Metadata Targets
        # The seeded timetable is for:
        target_year = '2025-26'
        target_sem = 4
        print(f"Targeting Timetable: Year={target_year}, Semester={target_sem}")
        
        # 2. Check Course Mapping
        courses = Course.query.all()
        print("\nAvailable Courses:")
        for c in courses:
            print(f"- {c.course_name} (ID: {c.id}, Code: {c.course_code})")
            
        # 3. Check Students
        students = Student.query.all()
        print(f"\nScanning {len(students)} Students for alignment...")
        
        matches_found = 0
        for s in students:
            # Check Semester
            if s.current_semester != target_sem:
                continue
                
            # Check Branch/Course Mapping
            # Logic in app.py: Course.course_name == student.branch OR Course.course_code == student.branch
            matching_course = Course.query.filter(
                (Course.course_name == s.branch) | (Course.course_code == s.branch)
            ).first()
            
            if not matching_course:
                # This student has a branch name that doesn't match any course!
                print(f"[WARN] Student {s.roll_number} Branch '{s.branch}' does NOT match any Course.")
                continue
                
            # Check Timetable Entries for this specific configuration
            query = Timetable.query.filter_by(
                semester=target_sem,
                academic_year=target_year,
                course_id=matching_course.id
            )
            
            # Apply Division Filter
            if s.division:
                query = query.filter((Timetable.division == s.division) | (Timetable.division == None))
                
            # Apply Batch Filter
            if s.batch:
                query = query.filter((Timetable.batch == s.batch) | (Timetable.batch == None))
                
            count = query.count()
            
            if count > 0:
                print(f"[OK] Student {s.roll_number} ({s.user.full_name}): Div {s.division}, Batch {s.batch} -> Matches {count} entries.")
                matches_found += 1
            else:
                 print(f"[FAIL] Student {s.roll_number} ({s.user.full_name}): Div {s.division}, Batch {s.batch} -> Matches 0 entries.")

        if matches_found == 0:
            print("\nCRITICAL: No students valid for the current timetable were found. You likely need to update student seeds.")
        else:
            print(f"\nFound {matches_found} students who should be able to see the timetable.")

if __name__ == '__main__':
    diagnose_visibility()
