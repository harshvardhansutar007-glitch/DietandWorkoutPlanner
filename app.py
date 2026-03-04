from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dietworkoutplanner2024secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dietworkout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    weight = db.Column(db.Float)  # in kg
    height = db.Column(db.Float)  # in cm
    activity_level = db.Column(db.String(50), default='moderate')
    fitness_goal = db.Column(db.String(50), default='maintain')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    meals = db.relationship('Meal', backref='user', lazy=True)
    workouts = db.relationship('Workout', backref='user', lazy=True)
    progress = db.relationship('Progress', backref='user', lazy=True)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # breakfast, lunch, dinner, snack
    food_name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # cardio, strength, flexibility
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    intensity = db.Column(db.String(20), default='moderate')
    calories_burned = db.Column(db.Integer)
    date = db.Column(db.Date, default=date.today)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Float)
    date = db.Column(db.Date, default=date.today)
    calories_consumed = db.Column(db.Integer, default=0)
    calories_burned = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/diet')
def diet():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('diet.html')

@app.route('/workout')
def workout():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('workout.html')

@app.route('/progress')
def progress():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('progress.html')

@app.route('/bmi')
def bmi():
    return render_template('bmi.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    
    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        age=data.get('age'),
        gender=data.get('gender'),
        weight=data.get('weight'),
        height=data.get('height'),
        activity_level=data.get('activity_level', 'moderate'),
        fitness_goal=data.get('fitness_goal', 'maintain')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        session['user_name'] = user.name
        return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({'success': False, 'message': 'Invalid email or password'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/user', methods=['GET'])
def get_user():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user = User.query.get(session['user_id'])
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'age': user.age,
            'gender': user.gender,
            'weight': user.weight,
            'height': user.height,
            'activity_level': user.activity_level,
            'fitness_goal': user.fitness_goal
        }
    })

@app.route('/api/diet/add', methods=['POST'])
def add_meal():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    meal = Meal(
        user_id=session['user_id'],
        meal_type=data['meal_type'],
        food_name=data['food_name'],
        calories=data['calories'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else date.today()
    )
    
    db.session.add(meal)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Meal added successfully'})

@app.route('/api/diet/today', methods=['GET'])
def get_today_meals():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    meals = Meal.query.filter_by(user_id=session['user_id'], date=date.today()).all()
    
    meals_by_type = {
        'breakfast': [],
        'lunch': [],
        'dinner': [],
        'snack': []
    }
    
    total_calories = 0
    for meal in meals:
        meals_by_type[meal.meal_type].append({
            'id': meal.id,
            'food_name': meal.food_name,
            'calories': meal.calories
        })
        total_calories += meal.calories
    
    # Calculate recommended calories
    user = User.query.get(session['user_id'])
    recommended = calculate_bmr(user)
    
    return jsonify({
        'success': True,
        'meals': meals_by_type,
        'total_calories': total_calories,
        'recommended_calories': recommended
    })

@app.route('/api/diet/history', methods=['GET'])
def get_diet_history():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    days = request.args.get('days', 7, type=int)
    from datetime import timedelta
    start_date = date.today() - timedelta(days=days)
    
    meals = Meal.query.filter(
        Meal.user_id == session['user_id'],
        Meal.date >= start_date
    ).order_by(Meal.date.desc()).all()
    
    history = {}
    for meal in meals:
        date_str = meal.date.strftime('%Y-%m-%d')
        if date_str not in history:
            history[date_str] = {'total': 0, 'meals': []}
        history[date_str]['total'] += meal.calories
        history[date_str]['meals'].append({
            'meal_type': meal.meal_type,
            'food_name': meal.food_name,
            'calories': meal.calories
        })
    
    return jsonify({'success': True, 'history': history})

@app.route('/api/diet/delete/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    meal = Meal.query.get(meal_id)
    if meal and meal.user_id == session['user_id']:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Meal deleted'})
    
    return jsonify({'success': False, 'message': 'Meal not found'}), 404

def calculate_bmr(user):
    # Mifflin-St Jeor Equation
    if user.gender == 'male':
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
    else:
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
    
    # Activity multiplier
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    multiplier = activity_multipliers.get(user.activity_level, 1.55)
    
    # Goal adjustment
    goal_adjustments = {
        'weight_loss': -500,
        'muscle_gain': 500,
        'maintain': 0
    }
    
    adjustment = goal_adjustments.get(user.fitness_goal, 0)
    
    return int(bmr * multiplier + adjustment)

@app.route('/api/workout/add', methods=['POST'])
def add_workout():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    workout = Workout(
        user_id=session['user_id'],
        workout_name=data['workout_name'],
        category=data['category'],
        duration=data['duration'],
        intensity=data.get('intensity', 'moderate'),
        calories_burned=data.get('calories_burned', 0),
        date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else date.today()
    )
    
    db.session.add(workout)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Workout added successfully'})

@app.route('/api/workout/today', methods=['GET'])
def get_today_workouts():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    workouts = Workout.query.filter_by(user_id=session['user_id'], date=date.today()).all()
    
    workout_list = []
    total_duration = 0
    total_calories = 0
    
    for workout in workouts:
        workout_list.append({
            'id': workout.id,
            'workout_name': workout.workout_name,
            'category': workout.category,
            'duration': workout.duration,
            'intensity': workout.intensity,
            'calories_burned': workout.calories_burned,
            'completed': workout.completed
        })
        total_duration += workout.duration
        total_calories += workout.calories_burned or 0
    
    return jsonify({
        'success': True,
        'workouts': workout_list,
        'total_duration': total_duration,
        'total_calories': total_calories
    })

@app.route('/api/workout/complete/<int:workout_id>', methods=['POST'])
def complete_workout(workout_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    workout = Workout.query.get(workout_id)
    if workout and workout.user_id == session['user_id']:
        workout.completed = True
        db.session.commit()
        return jsonify({'success': True, 'message': 'Workout marked as completed'})
    
    return jsonify({'success': False, 'message': 'Workout not found'}), 404

@app.route('/api/workout/delete/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    workout = Workout.query.get(workout_id)
    if workout and workout.user_id == session['user_id']:
        db.session.delete(workout)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Workout deleted'})
    
    return jsonify({'success': False, 'message': 'Workout not found'}), 404

@app.route('/api/progress/add', methods=['POST'])
def add_progress():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    
    # Update user weight if provided
    if data.get('weight'):
        user = User.query.get(session['user_id'])
        user.weight = data['weight']
    
    progress = Progress(
        user_id=session['user_id'],
        weight=data.get('weight'),
        calories_consumed=data.get('calories_consumed', 0),
        calories_burned=data.get('calories_burned', 0),
        date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else date.today()
    )
    
    db.session.add(progress)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Progress added successfully'})

@app.route('/api/progress/history', methods=['GET'])
def get_progress_history():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    days = request.args.get('days', 30, type=int)
    from datetime import timedelta
    start_date = date.today() - timedelta(days=days)
    
    progress = Progress.query.filter(
        Progress.user_id == session['user_id'],
        Progress.date >= start_date
    ).order_by(Progress.date).all()
    
    progress_list = []
    for p in progress:
        progress_list.append({
            'date': p.date.strftime('%Y-%m-%d'),
            'weight': p.weight,
            'calories_consumed': p.calories_consumed,
            'calories_burned': p.calories_burned
        })
    
    return jsonify({'success': True, 'progress': progress_list})

@app.route('/api/bmi/calculate', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    weight = float(data['weight'])  # kg
    height = float(data['height'])  # cm
    
    height_m = height / 100
    bmi = weight / (height_m * height_m)
    bmi = round(bmi, 1)
    
    if bmi < 18.5:
        category = 'Underweight'
        recommendation = 'Focus on nutrient-rich foods and consider consulting a nutritionist for a healthy weight gain plan.'
        color = '#f4a261'
    elif bmi < 25:
        category = 'Normal'
        recommendation = 'Great job! Maintain your healthy lifestyle with balanced diet and regular exercise.'
        color = '#2ec4b6'
    elif bmi < 30:
        category = 'Overweight'
        recommendation = 'Consider a balanced diet and regular physical activity. Aim for gradual weight loss.'
        color = '#f4a261'
    else:
        category = 'Obese'
        recommendation = 'Please consult with a healthcare provider for personalized advice on achieving a healthier weight.'
        color = '#e63946'
    
    return jsonify({
        'success': True,
        'bmi': bmi,
        'category': category,
        'recommendation': recommendation,
        'color': color
    })

if __name__ == '__main__':
    app.run(debug=True)
