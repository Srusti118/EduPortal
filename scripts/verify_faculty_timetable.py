import sys
import os
import json
from datetime import date

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Faculty, Timetable, User, LectureSwapRequest

def verify_faculty_timetable():
    with app.app_context():
        print("Verifying Faculty Timetable Logic...")

        # 1. Find a Faculty with timetable entries (e.g., AKS from created seed)
        faculty_code = 'AKS'
        faculty = Faculty.query.filter_by(faculty_id=faculty_code).first()
        
        if not faculty:
            print(f"Error: Faculty {faculty_code} not found. Seeding might have failed or verify on different data.")
            return

        print(f"Testing for Faculty: {faculty.user.full_name} ({faculty.faculty_id})")

        # 2. Call the API Logic (Simulated)
        # /api/faculty/timetable/<user_id>
        # We pass user_id usually in frontend
        
        # Simulate Request
        with app.test_client() as client:
            resp = client.get(f'/api/faculty/timetable/{faculty.user_id}')
            if resp.status_code != 200:
                print(f"Error: API returned {resp.status_code}")
                return
            
            data = resp.json
            print("API Response Received.")
            
            # Check for Monday 08:45 AM (Based on Img 1 / Division C seed)
            # AKS is teaching FCSP-1 to C1 on Mon 08:45
            target_time_start = "08:45"
            mon_data = data.get('monday', {})
            print(f"Available slots for Monday: {list(mon_data.keys())}")
            
            # Simple fuzzy match
            entry = next((v for k, v in mon_data.items() if target_time_start in k), None)
            
            if entry:
                # Iterate or just pick the first one found
                found_slot = next((k for k in mon_data.keys() if target_time_start in k), "Unknown Slot")
                print(f"Monday {found_slot}: {entry['subject_name']} (Batch: {entry['batch']})")
                if entry['batch'] == 'C1' and 'FCSP-1' in entry['subject_name']:
                    print("SUCCESS: Retrieved specific lecture correctly.")
                else:
                    print(f"CHECK: Expected C1/FCSP-1, got {entry['batch']}/{entry['subject_name']}")
            else:
                 print(f"WARNING: No entry found for Monday around 08:45 AM. Check seed data.")

            # 3. Test Swap Request
            if entry:
                print("Testing Swap Request...")
                timetable_id = entry['original_id']
                payload = {
                    'timetable_id': timetable_id,
                    'new_faculty_id': 'BNS', # Assuming BNS exists
                    'change_type': 'temporary',
                    'reason': 'Urgent work',
                    'date': '2026-02-10'
                }
                
                resp_swap = client.post('/api/faculty/timetable/change', json=payload)
                print(f"Swap Response: {resp_swap.json}")
                
                if resp_swap.json.get('success'):
                    print("SUCCESS: Swap request created.")
                    # Verify DB
                    req = LectureSwapRequest.query.filter_by(timetable_id=timetable_id).order_by(LectureSwapRequest.created_at.desc()).first()
                    if req:
                        print(f"DB Verification: Request ID {req.id} created for date {req.date}.")
                else:
                    print("FAILURE: Swap request failed.")

if __name__ == '__main__':
    verify_faculty_timetable()
