import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Faculty, Subject, Course

with app.app_context():
    print("Courses:")
    for c in Course.query.all():
        print(f"ID: {c.id}, Name: {c.course_name}, Code: {c.course_code}")
    
    print("\nSubjects:")
    for s in Subject.query.all():
        print(f"ID: {s.id}, Name: {s.subject_name}, Code: {s.subject_code}, Sem: {s.semester}")

    print("\nFaculties:")
    for f in Faculty.query.all():
        # Access user.full_name through relationship
        print(f"ID: {f.id}, Faculty ID: {f.faculty_id}, Name: {f.user.full_name}, Designation: {f.designation}")
