import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, Timetable, Course
import json

def debug_api():
    with app.app_context():
        # Target: PATEL JIMIT DINESHBHAI (Batch A1)
        username = '24002170110118'
        student = Student.query.filter(Student.enrollment_number == username).first()
        
        current_academic_year = '2025-26'
        
        query = Timetable.query.join(Course).filter(
            (Course.course_name == student.branch) | (Course.course_code == student.branch),
            Timetable.semester == student.current_semester,
            Timetable.academic_year == current_academic_year
        )
        
        if student.division:
            query = query.filter((Timetable.division == student.division) | (Timetable.division == None))
            
        if student.batch:
             query = query.filter((Timetable.batch == student.batch) | (Timetable.batch == None))
             
        timetable_entries = query.all()
        
        timetable = {}
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        for day in days:
            timetable[day] = {}
        
        for entry in timetable_entries:
            day = entry.day_of_week.lower()
            time_slot = entry.time_slot
            
            timetable[day][time_slot] = {
                'subject_name': entry.subject.subject_name,
                'subject_code': entry.subject.subject_code,
                'faculty_name': entry.faculty.user.full_name,
                'room_number': entry.room_number
            }
            
        print(json.dumps(timetable, indent=2))

if __name__ == '__main__':
    debug_api()
