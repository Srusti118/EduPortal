import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Student

def check_distribution():
    with app.app_context():
        print("--- Student Division Distribution ---")
        query = db.session.query(Student.division, db.func.count(Student.id)).group_by(Student.division).all()
        for div, count in query:
            print(f"Division {div}: {count} students")

if __name__ == '__main__':
    check_distribution()
