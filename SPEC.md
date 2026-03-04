# Diet and Workout Planner - Project Specification

## 1. Project Overview

**Project Name:** Diet and Workout Planner
**Project Type:** Full-stack Web Application
**Core Functionality:** A comprehensive fitness management platform that helps users plan their diets and workouts, track progress, and achieve their fitness goals.
**Target Users:** Fitness enthusiasts, beginners looking to start their fitness journey, and anyone wanting to maintain a healthy lifestyle.

## 2. Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python with Flask
- **Database:** SQLite
- **External Libraries:** Font Awesome (icons), Google Fonts

## 3. UI/UX Specification

### Layout Structure

**Pages:**
1. Home/Landing Page
2. User Registration/Login
3. Dashboard (after login)
4. Diet Planner
5. Workout Planner
6. Progress Tracking
7. BMI Calculator

### Visual Design

**Color Palette:**
- Primary: `#0d1b2a` (Deep Navy)
- Secondary: `#1b263b` (Dark Blue)
- Accent: `#e63946` (Vibrant Red)
- Accent Secondary: `#2ec4b6` (Teal)
- Background: `#0d1b2a`
- Card Background: `#1b263b`
- Text Primary: `#ffffff`
- Text Secondary: `#a8dadc`
- Success: `#2ec4b6`
- Warning: `#f4a261`

**Typography:**
- Primary Font: 'Outfit' (Google Fonts) - Modern, clean
- Secondary Font: 'Poppins' (Google Fonts)
- Headings: Outfit Bold
- Body: Poppins Regular

**Spacing System:**
- Section padding: 80px vertical
- Card padding: 30px
- Element margins: 20px
- Border radius: 15px (cards), 50px (buttons)

**Visual Effects:**
- Glassmorphism cards with backdrop-filter
- Gradient overlays on hero sections
- Smooth hover transitions (0.3s ease)
- Animated gradient backgrounds
- Floating particles animation on hero
- Staggered reveal animations

### Components

**Navigation Bar:**
- Fixed top navigation
- Logo on left
- Menu items on right (Home, Diet, Workout, Progress, BMI)
- Login/Register buttons or User profile dropdown
- Transparent to solid on scroll

**Hero Section:**
- Full viewport height
- Animated gradient background
- Floating fitness icons
- Main headline with typewriter effect
- Call-to-action buttons
- Scroll indicator

**Cards:**
- Glassmorphism effect
- Icon with circular background
- Title and description
- Hover: scale up, glow effect

**Forms:**
- Floating labels
- Input validation
- Animated submit buttons
- Error/success states

**Buttons:**
- Primary: Gradient red (#e63946 to #ff6b6b)
- Secondary: Outlined teal
- Hover: Glow effect, scale

## 4. Functionality Specification

### Core Features

**1. User Authentication:**
- User registration (name, email, password, age, gender, weight, height)
- User login/logout
- Session management
- Password hashing for security

**2. Diet Planner:**
- Daily calorie calculator based on user stats (BMR + activity level)
- Meal planning (Breakfast, Lunch, Dinner, Snacks)
- Calorie tracking per meal
- Custom meal suggestions
- Water intake tracking

**3. Workout Planner:**
- Workout goal setting (Weight Loss, Muscle Gain, Maintain)
- Exercise categories (Cardio, Strength, Flexibility)
- Pre-defined workout routines
- Custom workout creation
- Workout duration and intensity tracking

**4. Progress Tracking:**
- Weight tracking over time
- Workout completion history
- Calorie intake history
- Visual charts/graphs
- Weekly/Monthly summaries

**5. BMI Calculator:**
- Input: Weight (kg), Height (cm)
- Output: BMI value, Category (Underweight/Normal/Overweight/Obese)
- Personalized recommendations

### Database Schema

**Users Table:**
- id (PRIMARY KEY)
- name, email, password_hash
- age, gender, weight, height
- activity_level
- fitness_goal
- created_at

**Meals Table:**
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- meal_type (breakfast/lunch/dinner/snack)
- food_name, calories
- date

**Workouts Table:**
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- workout_name
- category, duration, intensity
- date, completed

**Progress Table:**
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- weight, date
- calories_consumed, calories_burned

### API Endpoints

- POST /api/register
- POST /api/login
- POST /api/logout
- GET /api/user
- POST /api/diet/add
- GET /api/diet/today
- POST /api/workout/add
- GET /api/workout/today
- POST /api/progress/add
- GET /api/progress/history
- POST /api/bmi/calculate

## 5. Acceptance Criteria

1. User can register and login successfully
2. Dashboard displays personalized information
3. Diet planner allows adding meals and tracks calories
4. Workout planner allows adding workouts
5. Progress page shows weight and workout history
6. BMI calculator provides accurate results with recommendations
7. All pages are responsive (mobile, tablet, desktop)
8. Animations and transitions are smooth
9. Data persists in SQLite database
10. No console errors on page load
