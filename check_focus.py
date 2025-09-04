from app import create_app, db
from app.models import StudySession

def check_focus_levels():
    app = create_app()
    with app.app_context():
        # Get all sessions with focus level set
        sessions = StudySession.query.filter(
            StudySession.focus_level.isnot(None)
        ).all()
        
        if not sessions:
            print("No sessions with focus level found in the database.")
            return
            
        print(f"Found {len(sessions)} sessions with focus levels:")
        for i, session in enumerate(sessions[:5], 1):  # Show first 5 for brevity
            print(f"{i}. Session ID: {session.id}, Subject: {session.subject}, Focus: {session.focus_level}")
            
        # Calculate average focus level
        avg_focus = db.session.query(db.func.avg(StudySession.focus_level))\
            .filter(StudySession.focus_level.isnot(None))\
            .scalar()
            
        print(f"\nAverage focus level: {avg_focus:.1f}/5")

if __name__ == "__main__":
    check_focus_levels()
