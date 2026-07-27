#!/usr/bin/env python3

from app import app
from models import db, Workout, Exercise, WorkoutExercise
from datetime import datetime, timedelta

with app.app_context():
    # Clear existing data
    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()
    db.session.commit()
    
    # Create exercises
    exercises = [
        Exercise(name='Push-ups', category='Strength', equipment_needed=False),
        Exercise(name='Squats', category='Strength', equipment_needed=False),
        Exercise(name='Plank', category='Strength', equipment_needed=False),
        Exercise(name='Running', category='Cardio', equipment_needed=False),
        Exercise(name='Jumping Jacks', category='Cardio', equipment_needed=False),
        Exercise(name='Yoga Sun Salutation', category='Flexibility', equipment_needed=False),
        Exercise(name='Single Leg Stand', category='Balance', equipment_needed=False),
        Exercise(name='Dumbbell Curls', category='Strength', equipment_needed=True),
        Exercise(name='Bench Press', category='Strength', equipment_needed=True),
        Exercise(name='Cycling', category='Cardio', equipment_needed=True),
    ]
    
    db.session.add_all(exercises)
    db.session.commit()
    print(f'Created {len(exercises)} exercises')
    
    # Create workouts
    today = datetime.now().date()
    workouts = [
        Workout(date=today - timedelta(days=2), duration_minutes=45, notes='Good workout, felt strong'),
        Workout(date=today - timedelta(days=1), duration_minutes=30, notes='Quick cardio session'),
        Workout(date=today, duration_minutes=60, notes='Full body workout'),
    ]
    
    db.session.add_all(workouts)
    db.session.commit()
    print(f'Created {len(workouts)} workouts')
    
    # Create workout exercises (join table entries)
    workout_exercises = [
        WorkoutExercise(workout_id=1, exercise_id=1, reps=20, sets=3),
        WorkoutExercise(workout_id=1, exercise_id=2, reps=15, sets=3),
        WorkoutExercise(workout_id=1, exercise_id=3, duration_seconds=60, sets=2),
        WorkoutExercise(workout_id=2, exercise_id=4, duration_seconds=1800),  # 30 minutes running
        WorkoutExercise(workout_id=2, exercise_id=5, duration_seconds=300, sets=3),
        WorkoutExercise(workout_id=3, exercise_id=1, reps=25, sets=4),
        WorkoutExercise(workout_id=3, exercise_id=8, reps=12, sets=3),
        WorkoutExercise(workout_id=3, exercise_id=9, reps=10, sets=3),
        WorkoutExercise(workout_id=3, exercise_id=6, duration_seconds=120, sets=1),
    ]
    
    db.session.add_all(workout_exercises)
    db.session.commit()
    print(f'Created {len(workout_exercises)} workout-exercise associations')
    
    print('Seed data loaded successfully!')
    
    # Test validations
    print('\nTesting validations...')
    try:
        invalid_workout = Workout(date=today + timedelta(days=1), duration_minutes=-10)
        db.session.add(invalid_workout)
        db.session.commit()
    except Exception as e:
        print(f'Validation caught: {e}')
        db.session.rollback()
    
    try:
        invalid_exercise = Exercise(name='A', category='Invalid')
        db.session.add(invalid_exercise)
        db.session.commit()
    except Exception as e:
        print(f'Validation caught: {e}')
        db.session.rollback()
    
    print('Validation tests completed!')