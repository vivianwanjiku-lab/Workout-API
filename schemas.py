from marshmallow import Schema, fields, validate, ValidationError, post_load, pre_load
from models import Workout, Exercise, WorkoutExercise
from datetime import datetime

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    duration_minutes = fields.Integer(required=True)
    notes = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Schema validations
    @pre_load
    def validate_date_format(self, data, **kwargs):
        if 'date' in data:
            try:
                datetime.strptime(data['date'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                raise ValidationError({'date': 'Invalid date format. Use YYYY-MM-DD'})
        return data
    
    @pre_load
    def validate_duration_minutes(self, data, **kwargs):
        if 'duration_minutes' in data:
            if data['duration_minutes'] <= 0:
                raise ValidationError({'duration_minutes': 'Duration must be greater than 0'})
            if data['duration_minutes'] > 1440:
                raise ValidationError({'duration_minutes': 'Duration cannot exceed 1440 minutes'})
        return data
    
    class Meta:
        fields = ('id', 'date', 'duration_minutes', 'notes')

class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean()
    
    # Schema validations
    @pre_load
    def validate_name(self, data, **kwargs):
        if 'name' in data:
            if not data['name'] or len(data['name'].strip()) == 0:
                raise ValidationError({'name': 'Exercise name cannot be empty'})
            if len(data['name'].strip()) < 3:
                raise ValidationError({'name': 'Exercise name must be at least 3 characters'})
        return data
    
    @pre_load
    def validate_category(self, data, **kwargs):
        if 'category' in data:
            valid_categories = ['Strength', 'Cardio', 'Flexibility', 'Balance']
            if data['category'] not in valid_categories:
                raise ValidationError({'category': f'Category must be one of: {", ".join(valid_categories)}'})
        return data
    
    class Meta:
        fields = ('id', 'name', 'category', 'equipment_needed')

class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer()
    duration_seconds = fields.Integer(allow_none=True)
    
    # Schema validations
    @pre_load
    def validate_reps_or_duration(self, data, **kwargs):
        if not data.get('reps') and not data.get('duration_seconds'):
            raise ValidationError({'error': 'Either reps or duration_seconds must be provided'})
        return data
    
    @pre_load
    def validate_reps(self, data, **kwargs):
        if 'reps' in data and data['reps'] is not None:
            if data['reps'] <= 0:
                raise ValidationError({'reps': 'Reps must be greater than 0'})
            if data['reps'] > 1000:
                raise ValidationError({'reps': 'Reps cannot exceed 1000'})
        return data
    
    @pre_load
    def validate_sets(self, data, **kwargs):
        if 'sets' in data and data['sets'] is not None:
            if data['sets'] <= 0:
                raise ValidationError({'sets': 'Sets must be greater than 0'})
            if data['sets'] > 100:
                raise ValidationError({'sets': 'Sets cannot exceed 100'})
        return data
    
    @pre_load
    def validate_duration(self, data, **kwargs):
        if 'duration_seconds' in data and data['duration_seconds'] is not None:
            if data['duration_seconds'] <= 0:
                raise ValidationError({'duration_seconds': 'Duration must be greater than 0 seconds'})
            if data['duration_seconds'] > 86400:
                raise ValidationError({'duration_seconds': 'Duration cannot exceed 86400 seconds'})
        return data
    
    class Meta:
        fields = ('id', 'workout_id', 'exercise_id', 'reps', 'sets', 'duration_seconds')

# Initialize schemas
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)