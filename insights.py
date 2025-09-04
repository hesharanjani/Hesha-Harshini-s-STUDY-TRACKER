from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy import func, extract
from .models import StudySession, db

def get_study_analytics(user_id, days=30):
    """Generate analytics for the user's study sessions"""
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    
    # Get all sessions in the date range
    sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.date >= start_date,
        StudySession.date <= end_date
    ).all()
    
    if not sessions:
        return {"status": "no_data", "message": "No study data available for analysis"}
    
    # Basic stats
    total_hours = sum(session.duration for session in sessions)
    avg_hours_per_day = total_hours / days
    sessions_count = len(sessions)
    
    # Subject distribution
    subject_hours = defaultdict(float)
    for session in sessions:
        subject_hours[session.subject] += session.duration
    
    # Find most productive time of day
    time_slots = defaultdict(float)
    for session in sessions:
        if session.start_time:
            hour = session.start_time.hour
            time_slot = f"{hour:02d}:00-{hour+1:02d}:00"
            time_slots[time_slot] += session.duration
    
    most_productive_time = max(time_slots.items(), key=lambda x: x[1]) if time_slots else (None, 0)
    
    # Mood and focus analysis
    moods = defaultdict(int)
    focus_total = 0
    focus_count = 0
    
    for session in sessions:
        if session.mood:
            moods[session.mood.lower()] += 1
        if session.focus_level:
            focus_total += session.focus_level
            focus_count += 1
    
    avg_focus = round(focus_total / focus_count, 1) if focus_count > 0 else None
    
    # Weekly progress
    weekly_hours = defaultdict(float)
    for session in sessions:
        week_num = session.date.isocalendar()[1]
        weekly_hours[week_num] += session.duration
    
    # Generate insights
    insights = []
    
    if most_productive_time[0]:
        insights.append(f"You are most productive between {most_productive_time[0]}")
    
    if subject_hours:
        top_subject = max(subject_hours.items(), key=lambda x: x[1])
        subject_percentage = int((top_subject[1] / total_hours) * 100)
        insights.append(f"You spent {subject_percentage}% of your time on {top_subject[0]}")
    
    if len(weekly_hours) > 1:
        weeks = sorted(weekly_hours.items())
        last_week = weeks[-1][1]
        second_last_week = weeks[-2][1] if len(weeks) > 1 else last_week
        if last_week > second_last_week and second_last_week > 0:
            improvement = int(((last_week - second_last_week) / second_last_week) * 100)
            insights.append(f"Your study time increased by {improvement}% compared to the previous week!")
    
    if moods:
        best_mood = max(moods.items(), key=lambda x: x[1])
        insights.append(f"You were most {best_mood[0]} during {best_mood[1]} study sessions")
    
    return {
        "status": "success",
        "total_hours": round(total_hours, 1),
        "avg_hours_per_day": round(avg_hours_per_day, 1),
        "sessions_count": sessions_count,
        "subject_distribution": dict(subject_hours),
        "most_productive_time": most_productive_time[0],
        "weekly_progress": dict(weekly_hours),
        "moods": dict(moods),
        "average_focus": avg_focus,
        "insights": insights
    }
