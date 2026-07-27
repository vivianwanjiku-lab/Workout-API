from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, default='')
    
    # Table constraints - NO date() CHECK constraint here!
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')
    
    # Model validations
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise ValueError("Duration must be greater than 0 minutes")
        if duration > 1440:  # Max 24 hours
            raise ValueError("Duration cannot exceed 1440 minutes (24 hours)")
        return duration
    
    @validates('date')
    def validate_date(self, key, date):
        if date > datetime.now().date():
            raise ValueError("Date cannot be in the future")
        return date
    
    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    
    # Table constraints
    __table_args__ = (
        db.CheckConstraint("category IN ('Strength', 'Cardio', 'Flexibility', 'Balance')", 
                          name='check_category_valid'),
    )
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')
    
    # Model validations
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Exercise name cannot be empty")
        if len(name) < 3:
            raise ValueError("Exercise name must be at least 3 characters")
        return name.strip()
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Strength', 'Cardio', 'Flexibility', 'Balance']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category
    
    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer, default=1)
    duration_seconds = db.Column(db.Integer)
    
    # Table constraints
    __table_args__ = (
        db.CheckConstraint('reps IS NULL OR reps > 0', name='check_reps_positive'),
        db.CheckConstraint('sets IS NULL OR sets > 0', name='check_sets_positive'),
        db.CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0', name='check_duration_positive'),
        db.CheckConstraint('reps IS NOT NULL OR duration_seconds IS NOT NULL', 
                          name='check_reps_or_duration'),
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
    )
    
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    # Model validations
    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None:
            if reps <= 0:
                raise ValueError("Reps must be greater than 0")
            if reps > 1000:
                raise ValueError("Reps cannot exceed 1000")
        return reps
    
    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None:
            if sets <= 0:
                raise ValueError("Sets must be greater than 0")
            if sets > 100:
                raise ValueError("Sets cannot exceed 100")
        return sets
    
    @validates('duration_seconds')
    def validate_duration(self, key, duration):
        if duration is not None:
            if duration <= 0:
                raise ValueError("Duration must be greater than 0 seconds")
            if duration > 86400:  # Max 24 hours
                raise ValueError("Duration cannot exceed 86400 seconds (24 hours)")
        return duration
    
    def __repr__(self):
        return f'<WorkoutExercise {self.id}: Workout {self.workout_id}, Exercise {self.exercise_id}>'