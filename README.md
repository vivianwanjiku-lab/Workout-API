# 💪 Workout Tracker API

A comprehensive backend API for a workout tracking application built with Flask, SQLAlchemy, and Marshmallow. This API enables personal trainers to manage workouts and exercises for their clients.

---

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Validation Rules](#validation-rules)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- ✅ Complete CRUD operations for workouts and exercises
- ✅ Many-to-many relationships between workouts and exercises
- ✅ Comprehensive validations at database, model, and schema levels
- ✅ Detailed tracking of sets, reps, and duration for each exercise
- ✅ RESTful API endpoints following best practices
- ✅ Automatic cascade deletion of related records
- ✅ Error handling with meaningful messages

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12.3 | Programming language |
| Flask | 2.2.2 | Web framework |
| Flask-SQLAlchemy | 3.0.3 | ORM for database operations |
| Flask-Migrate | 3.1.0 | Database migrations |
| Marshmallow | 3.20.1 | Serialization and validation |
| SQLite | - | Development database |
| Pipenv | - | Dependency management |

---

## 📁 Project Structure
Workout-Tracker-API/
├── server/
│ ├── app.py # Flask application & routes
│ ├── models.py # Database models & relationships
│ ├── schemas.py # Marshmallow schemas
│ ├── seed.py # Seed data for testing
│ ├── migrations/ # Database migrations
│ └── app.db # SQLite database
├── Pipfile # Dependencies
├── .gitignore # Git ignore rules
└── README.md # Project documentation

text

---

## 🚀 Installation

### Prerequisites

- Python 3.12.3 or higher
- Pipenv or pip
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/vivianwanjiku-lab/Workout-Tracker-API.git
cd Workout-Tracker-API
Step 2: Install Dependencies
Option A: Using Pipenv (Recommended)
bash
# Install pipenv if you don't have it
pip install pipenv

# Install all dependencies
pipenv install

# Activate the virtual environment
pipenv shell
Option B: Using pip with virtualenv
bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install flask==2.2.2 flask-sqlalchemy==3.0.3 flask-migrate==3.1.0 werkzeug==2.2.2 marshmallow==3.20.1 importlib-metadata==6.0.0 importlib-resources==5.10.0 ipdb==0.13.9
Step 3: Verify Installation
bash
# Check installed packages
pip list | grep flask
You should see:

flask 2.2.2

flask-sqlalchemy 3.0.3

flask-migrate 3.1.0

marshmallow 3.20.1

🗄️ Database Setup
Step 1: Initialize Database
bash
cd server

# Initialize migrations folder
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations to database
flask db upgrade head
Step 2: Seed Database with Sample Data
bash
python seed.py
Expected output:

text
Created 10 exercises
Created 3 workouts
Created 9 workout-exercise associations
Seed data loaded successfully!
Testing validations...
Validation caught: ...
Validation tests completed!
Step 3: Verify Data (Optional)
bash
flask shell
python
from models import Workout, Exercise

# Check workouts
print(f"Workouts: {Workout.query.count()}")
for w in Workout.query.all():
    print(f"  - {w.date}: {w.duration_minutes} minutes")

# Check exercises
print(f"Exercises: {Exercise.query.count()}")
for e in Exercise.query.all():
    print(f"  - {e.name} ({e.category})")

exit()
▶️ Running the Application
Start the Server
bash
cd server
python app.py
You should see:

text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5555
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
Server Options
Port: 5555 (default)

Debug Mode: Enabled for development

Auto-reload: Enabled (changes auto-detected)

📡 API Endpoints
Base URL
text
http://localhost:5555
Health Check
Method	Endpoint	Description
GET	/	API health check
Example Request
bash
curl http://localhost:5555/
Example Response
json
{
  "message": "Workout Tracker API is running!"
}
Workouts
Method	Endpoint	Description
GET	/workouts	List all workouts
GET	/workouts/<id>	Get a specific workout with exercises
POST	/workouts	Create a new workout
DELETE	/workouts/<id>	Delete a workout
GET /workouts - List All Workouts
bash
curl http://localhost:5555/workouts
GET /workouts/<id> - Get Single Workout
bash
curl http://localhost:5555/workouts/1
POST /workouts - Create Workout
bash
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-07-27",
    "duration_minutes": 45,
    "notes": "Morning workout session"
  }'
DELETE /workouts/<id> - Delete Workout
bash
curl -X DELETE http://localhost:5555/workouts/1
Exercises
Method	Endpoint	Description
GET	/exercises	List all exercises
GET	/exercises/<id>	Get a specific exercise with workouts
POST	/exercises	Create a new exercise
DELETE	/exercises/<id>	Delete an exercise
GET /exercises - List All Exercises
bash
curl http://localhost:5555/exercises
GET /exercises/<id> - Get Single Exercise
bash
curl http://localhost:5555/exercises/1
POST /exercises - Create Exercise
bash
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pull-ups",
    "category": "Strength",
    "equipment_needed": true
  }'
DELETE /exercises/<id> - Delete Exercise
bash
curl -X DELETE http://localhost:5555/exercises/1
Workout-Exercise Associations
Method	Endpoint	Description
POST	/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises	Add exercise to workout
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Request Body Options:

For strength exercises (with reps/sets):

bash
curl -X POST http://localhost:5555/workouts/1/exercises/2/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{
    "reps": 15,
    "sets": 3
  }'
For cardio exercises (with duration):

bash
curl -X POST http://localhost:5555/workouts/1/exercises/4/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{
    "duration_seconds": 1800
  }'
With both reps and duration:

bash
curl -X POST http://localhost:5555/workouts/1/exercises/2/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{
    "reps": 15,
    "sets": 3,
    "duration_seconds": 120
  }'
🧪 Testing the API
Using curl Commands
bash
# 1. Check if API is running
curl http://localhost:5555/

# 2. Get all workouts
curl http://localhost:5555/workouts

# 3. Get all exercises
curl http://localhost:5555/exercises

# 4. Create a workout (using today's date)
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d "{\"date\": \"$(date +%Y-%m-%d)\", \"duration_minutes\": 30, \"notes\": \"Test workout\"}"

# 5. Create an exercise
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Planks", "category": "Strength", "equipment_needed": false}'

# 6. Get a specific workout
curl http://localhost:5555/workouts/1

# 7. Add exercise to workout
curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 20, "sets": 3}'
Using Python Requests
python
import requests
import json

BASE_URL = "http://localhost:5555"

# Get all workouts
response = requests.get(f"{BASE_URL}/workouts")
print(json.dumps(response.json(), indent=2))

# Create a workout
data = {
    "date": "2024-07-27",
    "duration_minutes": 45,
    "notes": "Test workout"
}
response = requests.post(f"{BASE_URL}/workouts", json=data)
print(response.json())

# Get specific workout
response = requests.get(f"{BASE_URL}/workouts/1")
print(json.dumps(response.json(), indent=2))
Using Postman
Import the collection (create one manually)

Set base URL: http://localhost:5555

Test each endpoint with appropriate HTTP methods

Use JSON body for POST requests

✅ Validation Rules
Workout
Field	Validation	Example
date	Must be in past or present	"2024-07-27"
duration_minutes	Must be > 0 and ≤ 1440	30
notes	Optional text	"Morning workout"
Exercise
Field	Validation	Example
name	Required, at least 3 chars, unique	"Push-ups"
category	Must be: Strength, Cardio, Flexibility, Balance	"Strength"
equipment_needed	Boolean (true/false)	false
WorkoutExercise
Field	Validation	Example
reps	If provided, must be > 0 and ≤ 1000	15
sets	If provided, must be > 0 and ≤ 100	3
duration_seconds	If provided, must be > 0 and ≤ 86400	1800
Constraint	Either reps OR duration_seconds must be provided	
📊 Database Schema
Workout
text
+-----------------+-----------+----------+----------+
| Column          | Type      | Nullable | Default  |
+-----------------+-----------+----------+----------+
| id              | INTEGER   | NO       | Auto-inc |
| date            | DATE      | NO       | -        |
| duration_minutes| INTEGER   | NO       | -        |
| notes           | TEXT      | YES      | ''       |
+-----------------+-----------+----------+----------+
Exercise
text
+------------------+----------+----------+----------+
| Column           | Type     | Nullable | Default  |
+------------------+----------+----------+----------+
| id               | INTEGER  | NO       | Auto-inc |
| name             | STRING   | NO       | -        |
| category         | STRING   | NO       | -        |
| equipment_needed | BOOLEAN  | YES      | false    |
+------------------+----------+----------+----------+
WorkoutExercise (Join Table)
text
+------------------+----------+----------+----------+
| Column           | Type     | Nullable | Default  |
+------------------+----------+----------+----------+
| id               | INTEGER  | NO       | Auto-inc |
| workout_id       | INTEGER  | NO       | -        |
| exercise_id      | INTEGER  | NO       | -        |
| reps             | INTEGER  | YES      | NULL     |
| sets             | INTEGER  | YES      | 1        |
| duration_seconds | INTEGER  | YES      | NULL     |
+------------------+----------+----------+----------+
Relationships
text
Workout ---has many---> WorkoutExercise <---has many--- Exercise
    |                        |                            |
    |                        |                            |
    +--------has many through WorkoutExercise-----------+
🔧 Troubleshooting
Common Issues
1. "ModuleNotFoundError: No module named 'flask_migrate'"
Solution: Activate virtual environment and install packages

bash
cd ~/Documents/Workout-Tracker-API
pipenv shell
cd server
pip install flask-migrate==3.1.0
2. "non-deterministic use of date() in a CHECK constraint"
Solution: Reset database with corrected models

bash
cd server
rm -rf migrations/
rm -f app.db
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head
python seed.py
3. "Port 5555 already in use"
Solution: Kill the process or use different port

bash
# Kill process on port 5555
kill $(lsof -t -i:5555)

# Or change port in app.py
# app.run(port=5556, debug=True)
4. "Connection refused" when testing
Solution: Make sure server is running

bash
# In server directory
python app.py
5. Validation errors when creating data
Solution: Check validation rules above

Date must be in YYYY-MM-DD format

Duration must be positive

Category must be valid

Either reps or duration_seconds required

Quick Reset Script
bash
#!/bin/bash
# save as reset.sh and run: bash reset.sh

cd ~/Documents/Workout-Tracker-API/server

# Stop server
pkill -f "python app.py" 2>/dev/null

# Reset database
rm -rf migrations/
rm -f app.db *.sqlite

# Setup fresh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head

# Seed
python seed.py

# Start
python app.py
📝 Development Commands Reference
Pipenv Commands
bash
pipenv install              # Install dependencies
pipenv shell                # Activate virtual environment
pipenv run python app.py    # Run without entering shell
pipenv graph                # Show dependency tree
pipenv --rm                 # Remove virtual environment
Flask Commands
bash
flask db init               # Initialize migrations
flask db migrate -m "msg"   # Create migration
flask db upgrade head       # Apply migrations
flask db downgrade          # Revert migration
flask shell                 # Open Flask shell
flask routes                # Show all routes
Database Commands
bash
python seed.py              # Seed database
flask shell                 # Enter database shell
Git Commands
bash
git add .                   # Stage changes
git commit -m "message"     # Commit changes
git push                    # Push to GitHub
git status                  # Check status
git log --oneline           # View commit history
🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature-name

Make your changes

Commit: git commit -m "Add feature"

Push: git push origin feature-name

Create a Pull Request

📄 License
This project is for educational purposes as part of the Flatiron School curriculum.

📞 Support
For issues or questions:

GitHub Issues: Create an issue in the repository

Documentation: Refer to this README

Flask Documentation: https://flask.palletsprojects.com/

🎯 Quick Start Summary
bash
# 1. Clone and enter project
git clone https://github.com/vivianwanjiku-lab/Workout-Tracker-API.git
cd Workout-Tracker-API

# 2. Install and activate environment
pipenv install
pipenv shell

# 3. Setup database
cd server
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head

# 4. Seed and run
python seed.py
python app.py

# 5. Test in another terminal
curl http://localhost:5555/
curl http://localhost:5555/workouts