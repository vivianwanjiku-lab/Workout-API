from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercise
from schemas import workout_schema, workouts_schema, exercise_schema, exercises_schema, workout_exercise_schema
from marshmallow import ValidationError
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# WORKOUT ROUTES

@app.route('/')
def home():
    return jsonify({"message": "Workout Tracker API is running!"})

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """Get all workouts"""
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts))

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    """Get a single workout with its exercises"""
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    
    # Include workout exercises with reps/sets/duration
    result = workout_schema.dump(workout)
    result['exercises'] = []
    for we in workout.workout_exercises:
        exercise_data = exercise_schema.dump(we.exercise)
        exercise_data['workout_exercise_id'] = we.id
        exercise_data['reps'] = we.reps
        exercise_data['sets'] = we.sets
        exercise_data['duration_seconds'] = we.duration_seconds
        result['exercises'].append(exercise_data)
    
    return jsonify(result)

@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('date'):
            return make_response(jsonify({'error': 'Date is required'}), 400)
        if not data.get('duration_minutes'):
            return make_response(jsonify({'error': 'Duration minutes is required'}), 400)
        
        # Parse date
        try:
            date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400)
        
        workout = Workout(
            date=date_obj,
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes', '')
        )
        
        db.session.add(workout)
        db.session.commit()
        
        return jsonify(workout_schema.dump(workout)), 201
    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout and its associated workout exercises"""
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    
    try:
        # Delete associated workout exercises
        WorkoutExercise.query.filter_by(workout_id=id).delete()
        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({'message': 'Workout deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)

# EXERCISE ROUTES

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """Get all exercises"""
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises))

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    """Get an exercise and its associated workouts"""
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    
    result = exercise_schema.dump(exercise)
    result['workouts'] = []
    for we in exercise.workout_exercises:
        workout_data = workout_schema.dump(we.workout)
        workout_data['workout_exercise_id'] = we.id
        workout_data['reps'] = we.reps
        workout_data['sets'] = we.sets
        workout_data['duration_seconds'] = we.duration_seconds
        result['workouts'].append(workout_data)
    
    return jsonify(result)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create a new exercise"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return make_response(jsonify({'error': 'Name is required'}), 400)
        if not data.get('category'):
            return make_response(jsonify({'error': 'Category is required'}), 400)
        
        exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data.get('equipment_needed', False)
        )
        
        db.session.add(exercise)
        db.session.commit()
        
        return jsonify(exercise_schema.dump(exercise)), 201
    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise and its associated workout exercises"""
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    
    try:
        # Delete associated workout exercises
        WorkoutExercise.query.filter_by(exercise_id=id).delete()
        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({'message': 'Exercise deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)

# WORKOUT EXERCISE ROUTE

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an exercise to a workout with reps, sets, and duration"""
    try:
        data = request.get_json()
        
        # Verify workout and exercise exist
        workout = db.session.get(Workout, workout_id)
        if not workout:
            return make_response(jsonify({'error': 'Workout not found'}), 404)
        
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            return make_response(jsonify({'error': 'Exercise not found'}), 404)
        
        # Validate required fields
        if not data.get('reps') and not data.get('duration_seconds'):
            return make_response(jsonify({'error': 'Either reps or duration_seconds is required'}), 400)
        
        # Create workout exercise
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets', 1),
            duration_seconds=data.get('duration_seconds')
        )
        
        db.session.add(workout_exercise)
        db.session.commit()
        
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)

if __name__ == '__main__':
    app.run(port=5555, debug=True)