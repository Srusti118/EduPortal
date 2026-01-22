import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student, Timetable

def verify_batches():
    with app.app_context():
        print("--- Batch Verification ---")
        
        # Get Timetable Batches
        tt_batches = db.session.query(Timetable.batch).distinct().all()
        tt_batches = set([b[0] for b in tt_batches if b[0]])
        print(f"Timetable Batches: {sorted(list(tt_batches))}")
        
        # Get Student Batches
        st_batches = db.session.query(Student.batch).distinct().all()
        st_batches = set([b[0] for b in st_batches if b[0]])
        print(f"Student Batches: {sorted(list(st_batches))}")
        
        # Find Gap
        missing = st_batches - tt_batches
        print(f"Batches in Students but NOT in Timetable: {sorted(list(missing))}")
        
        if missing:
            print("\nCRITICAL: These students will likely see NO batched lectures.")
            # Count affected students
            count = Student.query.filter(Student.batch.in_(missing)).count()
            print(f"Affected Students Count: {count}")

if __name__ == '__main__':
    verify_batches()
