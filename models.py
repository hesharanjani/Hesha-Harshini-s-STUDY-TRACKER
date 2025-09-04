from datetime import datetime, timezone
from flask_login import UserMixin
from app import db, login_manager, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    study_sessions = db.relationship('StudySession', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class StudySession(db.Model):
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)  # in hours
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # New fields for insights
    mood = db.Column(db.String(20), nullable=True)  # happy, tired, focused, etc.
    focus_level = db.Column(db.Integer, nullable=True)  # 1-5 scale
    distractions = db.Column(db.Integer, default=0)  # number of distractions
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'duration': self.duration,
            'date': self.date.isoformat(),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'notes': self.notes,
            'mood': self.mood,
            'focus_level': self.focus_level,
            'distractions': self.distractions
        }

    @property
    def duration_hours(self):
        return round(self.duration, 2)

    @duration_hours.setter
    def duration_hours(self, hours):
        self.duration = hours

    def __repr__(self):
        return f"StudySession('{self.subject}', '{self.date}', {self.duration}h)"


class ScheduledSession(db.Model):
    __tablename__ = 'scheduled_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(20), default='#3b82f6')  # Default blue color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('scheduled_sessions', lazy=True))

    @property
    def duration_minutes(self):
        return int((self.end_datetime - self.start_datetime).total_seconds() / 60)

    @property
    def duration_hours(self):
        return round(self.duration_minutes / 60, 2)

    @property
    def weekday(self):
        """Return the weekday as an integer where Monday is 0 and Sunday is 6"""
        return self.start_datetime.weekday()
        
    def to_dict(self):
        """Convert the session to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.subject,
            'start': self.start_datetime.isoformat(),
            'end': self.end_datetime.isoformat(),
            'color': self.color,
            'notes': self.notes,
            'user_id': self.user_id,
            'duration_minutes': self.duration_minutes,
            'duration_hours': self.duration_hours,
            'extendedProps': {
                'notes': self.notes or ''
            }
        }

    def __repr__(self):
        return f"ScheduledSession('{self.subject}', '{self.start_datetime}' to '{self.end_datetime}')"