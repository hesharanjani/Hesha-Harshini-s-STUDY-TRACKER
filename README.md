# Study Tracker

## Overview
Study Tracker is a comprehensive Flask-based web application that helps students and lifelong learners track their study sessions, monitor progress, and improve productivity using the Pomodoro technique. The application features user authentication, session tracking, and insightful statistics.

## Features
- **User Authentication**: Secure signup and login system
- **Study Session Tracking**: Log study sessions with duration, subject, and notes
- **Pomodoro Timer**: Built-in timer for focused study sessions with customizable work/break intervals
- **Progress Dashboard**: Visualize your study habits with charts and statistics
- **Data Export**: Export your study sessions to CSV for further analysis
- **Responsive Design**: Works on desktop and mobile devices

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- SQLite (included with Python)

## How to use our study tracker
- find and download 4 parts of Study-Trackerproj zip files and combine them together (you can ask chatgpt to combine them to a single zip file).
- extract the zip file
- open the folder in vs code
- install the requirements,flask and other packages
- run and enjoy using our study tracker

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/study-tracker.git
   cd study-tracker
   ```

2. **Create and activate a virtual environment**:
   - On Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following content:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///study_tracker.db
   ```
   Replace `your-secret-key-here` with a secure secret key.

5. **Initialize the database**:
   ```bash
   flask db upgrade
   ```

## Usage

### Running the Application
1. **Start the development server**:
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`

### Key Features

#### User Registration and Login
- Create a new account or log in with existing credentials
- Secure password hashing for account protection

#### Dashboard
- View your weekly study statistics
- See recent study sessions
- Quick access to common actions

#### Study Sessions
- Add new study sessions with duration, subject, and notes
- View and filter your study history
- Delete sessions if needed
- Export your study data to CSV

#### Pomodoro Timer
- Start, pause, and reset the timer
- Customize work and break durations
- Visual progress indicator
- Sound notifications

## Development

### Project Structure
```
study-tracker/
├── app/
│   ├── __init__.py       # Application factory
│   ├── models.py         # Database models
│   ├── auth/             # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── main/             # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── study/            # Study sessions blueprint
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── static/           # Static files (CSS, JS, images)
│   └── templates/        # HTML templates
├── migrations/           # Database migrations
├── .env                 # Environment variables
├── config.py            # Configuration
├── requirements.txt     # Dependencies
└── run.py               # Application entry point
```

### Database Migrations
When making changes to the database models:
1. Generate a migration:
   ```bash
   flask db migrate -m "description of changes"
   ```
2. Apply the migration:
   ```bash
   flask db upgrade
   ```

### Testing
Run the test suite with:
```bash
python -m pytest
```

## Contributing
Contributions are welcome! Here's how you can help:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Icons by [Font Awesome](https://fontawesome.com/)
- Charts by [Chart.js](https://www.chartjs.org/)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
