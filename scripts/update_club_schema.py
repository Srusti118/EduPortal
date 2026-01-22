
from app import app, db
from models import Club, User, Faculty, Notification
from datetime import datetime

# Define ClubRequest model dynamically to avoid import issues if not yet in models.py
# (But wait, I need to add it to models.py first for this to work sustainably)
# However, to mess with Schema, I should use direct SQL or alter statements if not using migration tool.
# Since we are using SQLAlchemy `db.create_all()`, adding to models.py is best.

def update_club_data():
    with app.app_context():
        # 0. Fix Schema for existing table
        try:
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE club ADD COLUMN instagram_link VARCHAR(500)"))
                conn.commit()
            print("Added instagram_link column.")
        except Exception as e:
            print(f"Schema update skipped (maybe column exists): {e}")

        # 0.5 Create ClubRequest table (db.create_all handles new tables)
        db.create_all()

        # 1. Create ClubHead User if not exists
        club_head_user = User.query.filter_by(username='ClubHead').first()
        if not club_head_user:
            from werkzeug.security import generate_password_hash
            club_head_user = User(
                username='ClubHead',
                email='clubhead@college.edu',
                password_hash=generate_password_hash('faculty123'),
                role='faculty',
                full_name='Club Coordinator',
                department='Administration'
            )
            db.session.add(club_head_user)
            db.session.flush()
            
            # Create Faculty Profile for ClubHead
            club_head_faculty = Faculty(
                user_id=club_head_user.id,
                faculty_id='CLUB001',
                designation='Coordinator',
                experience_years=5,
                specialization='Student Activities'
            )
            db.session.add(club_head_faculty)
            db.session.commit()
            print("Created ClubHead user.")
        else:
            club_head_faculty = Faculty.query.filter_by(user_id=club_head_user.id).first()

        # 2. Update/Seed Clubs
        clubs_data = [
            {
                'name': 'Binary Brains',
                'description': 'Tech news and tech events community. Stay updated with the latest in technology.',
                'category': 'technical',
                'instagram_link': 'https://www.instagram.com/binarybrains23?igsh=MTc2dGduZ2FwanRmcg==',
                'interests': 'tech news,events,technology,innovation'
            },
            {
                'name': 'Byte Club',
                'description': 'The premier coding club. Competitive programming, hackathons, and software development.',
                'category': 'technical',
                'instagram_link': '', # No link provided
                'interests': 'coding,programming,algorithms,development'
            },
            {
                'name': 'LFA',
                'description': 'Magazine publishing and literary activities. Express your creativity through words.',
                'category': 'cultural',
                'instagram_link': 'https://www.instagram.com/lfa_ljiet?igsh=dDFnNjg3YzU2eDBq',
                'interests': 'writing,journalism,magazine,literature'
            },
            {
                'name': 'Saaz Room',
                'description': 'Music club. Jam sessions, performances, and musical gatherings.',
                'category': 'cultural',
                'instagram_link': 'https://www.instagram.com/saaz._room?igsh=b3FtaGw3dWhzYzN1',
                'interests': 'music,instruments,singing,bands'
            },
            {
                'name': 'LJSC',
                'description': 'All over events and student coordination body.',
                'category': 'management',
                'instagram_link': 'https://www.instagram.com/ljsc_ljiet?igsh=bWxhYjUzMmt1Y2V3',
                'interests': 'management,events,leadership,coordination'
            }
        ]

        for data in clubs_data:
            club = Club.query.filter_by(name=data['name']).first()
            if club:
                # Update existing
                club.description = data['description']
                club.category = data['category']
                club.interests = data['interests']
                # We need to ensure the column exists first, so we might need a raw SQL for that if not dropped
                # But for now let's assume I'll update models.py and recreate/migrate
                if hasattr(club, 'instagram_link'):
                    club.instagram_link = data['instagram_link']
            else:
                # Create new
                new_club = Club(
                    name=data['name'],
                    description=data['description'],
                    category=data['category'],
                    interests=data['interests'],
                    meeting_schedule='Weekly',
                    contact_email=f"{data['name'].lower().replace(' ', '')}@college.edu",
                    faculty_coordinator=club_head_faculty.id
                )
                if hasattr(new_club, 'instagram_link'):
                    new_club.instagram_link = data['instagram_link']
                db.session.add(new_club)
        
        db.session.commit()
        print("Clubs seeded successfully.")

if __name__ == '__main__':
    update_club_data()
