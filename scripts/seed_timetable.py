import sys
import os
import csv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Faculty, Subject, Course, Timetable

def seed_timetable():
    with app.app_context():
        print("Starting Timetable Seeding...")
        
        # Clear existing timetable for this specific import (optional, but good for cleanup)
        # For safety, let's just clear for the specific course/sem we are targeting or just append.
        # Given this is a fresh setup for this data, let's assume we want to clear previous entries for this academic year/sem to avoid duplicates.
        # But to be safe, I'll valid check before inserting.

        # Configuration
        ACADEMIC_YEAR = "2025-26"
        SEMESTER = 4
        # CSV Files mapping to Division
        files = {
            'A': 'data/timetable_div_a.csv',
            'B': 'data/timetable_div_b.csv',
            'C': 'data/timetable_div_c.csv'
        }

        # Day Mapping
        day_map = {
            'MON': 'monday',
            'TUE': 'tuesday',
            'WED': 'wednesday',
            'THU': 'thursday',
            'FRI': 'friday',
            'SAT': 'saturday'
        }

        # Ensure Course exists (Mapping "CE" or "CSE" generally)
        # We need a course for these subjects. Let's assume 'Computer Science Engineering' (ID 1 from inspection)
        course = Course.query.filter(Course.course_name.like('%Computer Science%')).first()
        if not course:
            print("Error: Course not found. Please ensure 'Computer Science' course exists.")
            return

        for division, filepath in files.items():
            print(f"Processing Division {division} from {filepath}...")
            
            if not os.path.exists(filepath):
                print(f"File not found: {filepath}")
                continue

            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    # Extract Data
                    day_short = row['Day'].strip().upper()
                    if day_short not in day_map:
                        continue # Skip header repetitions or invalid rows
                    
                    day = day_map[day_short]
                    start_time = row['Start_Time'].strip()
                    end_time = row['End_Time'].strip()
                    time_slot = f"{start_time}-{end_time}"
                    
                    batch_id = row['Batch_ID'].strip() # e.g., C1, A1
                    subject_code_raw = row['Subject'].strip() # e.g., FCSP-1
                    faculty_code = row['Faculty'].strip() # e.g., AKS
                    room_no = row['Room_No'].strip()

                    # Handle Batch: If batch ID matches Division (e.g. just 'C', doesn't happen here usually), or if it represents full class?
                    # In CSV, C1..C9 are batches.
                    # If we want to represent a "Lecture" for the whole class, usually batch is null or unique.
                    # But here, even lectures have Batch_ID 'C1' repeated 8 times for C1..C9?
                    # Let's look at the CSV.
                    # Row 1: Batch C1, FCSP-1...
                    # Row 2: Batch C2, PS...
                    # Oh, these are LABS/TUTORIALS mostly, or maybe lectures are listed per batch?
                    # Wait, look at "MON 11:30 AM".
                    # C1: DE, C2: FSD-1... It looks like parallel sessions.
                    # Look at "THU 12:30". C1..C9 have different subjects.
                    # BUT, look at "MON 08:45 - 09:45" in Img 1 (Division C).
                    # C1: FCSP-1, C2: PS, etc.
                    # These look like PRACTICAL sessions because different batches have different subjects.
                    
                    # Is there any FULL CLASS lecture?
                    # Division C, TUE 11:30.
                    # C1: FCSP-1, C2: PS... Still different.
                    
                    # It seems almost EVERYTHING is batch-wise in this dataset?
                    # Or maybe I am misinterpreting.
                    # If the user says "fetch their division... show respective timetable",
                    # and if I am Student Batch C1, I simply want to see rows where Batch_ID is C1.
                    # If there's a row where Batch_ID is 'ALL' or 'C', I want that too.
                    # In this CSV, it seems explicitly broken down by batch.
                    # So I will store the Batch exactly as is.

                    # 1. Get/Create Subject
                    # We use the raw subject code as the name for now if not found, or try to match nicely.
                    subject_code = f"{subject_code_raw}-SEM{SEMESTER}" # Unique code per sem to avoid clashes
                    subject = Subject.query.filter_by(subject_code=subject_code).first()
                    if not subject:
                        subject = Subject(
                            subject_code=subject_code,
                            subject_name=subject_code_raw, # Use the code as name (e.g. FCSP-1)
                            semester=SEMESTER,
                            course_id=course.id,
                            credits=4 # Default
                        )
                        db.session.add(subject)
                        db.session.flush()

                    # 2. Get Faculty
                    faculty = Faculty.query.filter_by(faculty_id=faculty_code).first()
                    if not faculty:
                        # Create a placeholder faculty if strictly needed, or skip?
                        # Creating placeholder is safer to avoid foreign key errors.
                        # We need a user for the faculty first.
                        # Check if user exists?
                        default_email = f"{faculty_code.lower()}@college.edu"
                        user = Faculty.query.filter(Faculty.faculty_id == faculty_code).first()
                        if not user:
                             # Create base User first
                             from models import User
                             from werkzeug.security import generate_password_hash
                             new_user = User(
                                 username=faculty_code.lower(),
                                 email=default_email,
                                 password_hash=generate_password_hash('password'),
                                 role='faculty',
                                 full_name=f"Prof. {faculty_code}",
                                 department='Computer Science'
                             )
                             db.session.add(new_user)
                             db.session.flush()
                             
                             faculty = Faculty(
                                 user_id=new_user.id,
                                 faculty_id=faculty_code,
                                 designation='Assistant Professor'
                             )
                             db.session.add(faculty)
                             db.session.flush()
                    
                    # 3. Create Timetable Entry
                    # Check if exists to avoid dupes
                    existing = Timetable.query.filter_by(
                        day_of_week=day,
                        time_slot=time_slot,
                        batch=batch_id,
                        division=division,
                        semester=SEMESTER
                    ).first()

                    if not existing:
                        entry = Timetable(
                            course_id=course.id,
                            semester=SEMESTER,
                            day_of_week=day,
                            time_slot=time_slot,
                            subject_id=subject.id,
                            faculty_id=faculty.id,
                            room_number=room_no,
                            academic_year=ACADEMIC_YEAR,
                            division=division,
                            batch=batch_id
                        )
                        db.session.add(entry)
                        count += 1
                
                db.session.commit()
                print(f"Imported {count} entries for Division {division}.")
        
        print("Timetable seeding completed successfully.")

if __name__ == '__main__':
    seed_timetable()
