from app import create_app, db
from app.models import User, StudySession

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'StudySession': StudySession}

if __name__ == "__main__":
    app.run(debug=True)