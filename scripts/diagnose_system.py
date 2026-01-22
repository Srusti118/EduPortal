
import os
import re
from app import app, db
from models import Student, Club

def check_css_balance(filepath):
    print(f"Checking CSS: {filepath}")
    if not os.path.exists(filepath):
        print("CSS File not found!")
        return
        
    with open(filepath, 'r') as f:
        content = f.read()
        
    open_braces = content.count('{')
    close_braces = content.count('}')
    
    print(f"  Open braces: {open_braces}")
    print(f"  Close braces: {close_braces}")
    
    if open_braces != close_braces:
        print("  [ERROR] Braces mismatch! CSS might be broken.")
    else:
        print("  [OK] Braces balanced.")

def check_api():
    print("\nChecking API Integration...")
    with app.app_context():
        # 1. Check Student
        student = Student.query.first()
        if not student:
            print("[ERROR] No students found in DB.")
            return
            
        print(f"  Found Student: {student.user.full_name} (ID: {student.id})")
        
        # 2. Check Clubs
        clubs = Club.query.all()
        print(f"  Found {len(clubs)} clubs.")
        for club in clubs:
            print(f"    - {club.name} (Instagram: {club.instagram_link})")
            
        # 3. Simulate ID Card Data Fetch (Manual Logic Check)
        try:
            id_card_data = {
                'full_name': student.user.full_name,
                'roll_number': student.roll_number,
                'enrollment_number': student.enrollment_number,
                'branch': student.branch,
                'semester': student.current_semester,
                'admission_year': student.admission_year,
                'photo_url': student.photo_url,
                'valid_until': f"{student.admission_year + 4}-12-31"
            }
            print("  [OK] ID Card logic constructs data successfully.")
        except Exception as e:
            print(f"  [ERROR] ID Card logic failed: {e}")

if __name__ == "__main__":
    check_css_balance('static/css/dashboard.css')
    check_api()
