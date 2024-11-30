from supabase import create_client
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import json

# Configuration for mock data quantities
MOCK_DATA_CONFIG = {
    # Organizational structure
    'num_districts': 1,
    'schools_per_district': 2,
    
    # Users per school
    'admins_per_school': 2,
    'instructors_per_school': 2,
    'students_per_school': 200,
    
    # Classroom structure
    'classrooms_per_school': {
        'min': 2,
        'max': 2
    },
    'periods_per_classroom': {
        'min': 4,
        'max': 8
    },
    
    # Course structure
    'courses_per_instructor': {
        'min': 1,
        'max': 1
    },
    'students_per_course': {
        'min': 15,
        'max': 20
    },
    
    # Content structure
    'units_per_course': {
        'min': 2,
        'max': 4
    },
    'lessons_per_unit': {
        'min': 7,
        'max': 10
    },
    'slides_per_lesson': {
        'min': 30,
        'max': 40
    },
    
    # Assessment structure
    'assessments_per_unit': {
        'min': 1,
        'max': 2
    },
    'questions_per_assessment': {
        'min': 5,
        'max': 10
    },
    
    # Question bank
    'questions_per_subject_grade': 50,  # For each subject and grade level
    
    # Progress tracking
    'completion_rate': 0.7,  # 70% of content will be marked as completed
    'assessment_attempt_rate': 0.9,  # 90% of students attempt assessments
    'max_assessment_attempts': 3
}

# Initialize Supabase client
SUPABASE_URL = "https://uyybtjxqfhxosuwngbac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5eWJ0anhxZmh4b3N1d25nYmFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyMTEzNTgsImV4cCI6MjA0Nzc4NzM1OH0.NBubYUom-rRzV7ZM74p8bvSo9zE9H8YdldcJ400_86g"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Faker
fake = Faker()

def safe_insert(table_name, data):
    """Helper function to safely insert data and handle errors"""
    try:
        response = supabase.table(table_name).insert(data).execute()
        if response.data:
            print(f"Added record to {table_name} (id: {response.data[0].get(f'{table_name[:-1]}_id', 'N/A')})")
        return response.data if response.data else []
    except Exception as e:
        print(f"Error inserting into {table_name}: {str(e)}")
        print(f"Data attempted: {json.dumps(data, indent=2)}")
        raise

def create_districts(num_districts=None):
    """Create mock district data"""
    num_districts = num_districts or MOCK_DATA_CONFIG['num_districts']
    districts = []
    try:
        for _ in range(num_districts):
            district = {
                'district_title': f"{fake.city()} School District"
            }
            result = safe_insert('districts', district)
            if result:
                districts.extend(result)
        return districts
    except Exception as e:
        print(f"Error in create_districts: {str(e)}")
        print(f"Error type: {type(e)}")
        raise

def create_schools(districts, num_schools_per_district=None):
    """Create mock school data"""
    num_schools = num_schools_per_district or MOCK_DATA_CONFIG['schools_per_district']
    schools = []
    for district in districts:
        for _ in range(num_schools):
            school = {
                'district_id': district['district_id'],
                'school_title': f"{fake.last_name()} {random.choice(['High School', 'Middle School'])}",
                'school_address': fake.address()
            }
            result = safe_insert('schools', school)
            if result:
                schools.extend(result)
    return schools

def create_administrators(schools, num_admins_per_school=None):
    """Create mock school administrator data"""
    num_admins = num_admins_per_school or MOCK_DATA_CONFIG['admins_per_school']
    admins = []
    for school in schools:
        for _ in range(num_admins):
            admin = {
                'school_id': school['school_id'],
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'password': fake.password(length=12)
            }
            result = safe_insert('schooladministrators', admin)
            if result:
                admins.extend(result)
    return admins

def create_instructors(schools, num_instructors_per_school=None):
    """Create mock instructor data"""
    num_instructors = num_instructors_per_school or MOCK_DATA_CONFIG['instructors_per_school']
    instructors = []
    for school in schools:
        for _ in range(num_instructors):
            instructor = {
                'school_id': school['school_id'],
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'password': fake.password(length=12)
            }
            result = safe_insert('instructors', instructor)
            if result:
                instructors.extend(result)
    return instructors

def create_students(schools, num_students_per_school=None):
    """Create mock student data"""
    num_students = num_students_per_school or MOCK_DATA_CONFIG['students_per_school']
    students = []
    for school in schools:
        for _ in range(num_students):
            student = {
                'school_id': school['school_id'],
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'password': fake.password(length=12)
            }
            result = safe_insert('students', student)
            if result:
                students.extend(result)
    return students

def create_classrooms(schools, instructors):
    """Create mock classroom data"""
    classrooms = []
    for school in schools:
        school_instructors = [i for i in instructors if i['school_id'] == school['school_id']]
        if not school_instructors:
            continue
            
        num_classrooms = random.randint(MOCK_DATA_CONFIG['classrooms_per_school']['min'], MOCK_DATA_CONFIG['classrooms_per_school']['max'])
        for _ in range(num_classrooms):
            classroom = {
                'school_id': school['school_id'],
                'instructor_id': random.choice(school_instructors)['instructor_id'],
                'classroom_title': f"Room {random.randint(100, 999)}"
            }
            result = safe_insert('classrooms', classroom)
            if result:
                classrooms.extend(result)
    return classrooms

def create_class_periods(classrooms):
    """Create mock class period data"""
    class_periods = []
    for classroom in classrooms:
        num_periods = random.randint(MOCK_DATA_CONFIG['periods_per_classroom']['min'], MOCK_DATA_CONFIG['periods_per_classroom']['max'])
        for period_num in range(1, num_periods + 1):
            class_period = {
                'classroom_id': classroom['classroom_id'],
                'period_number': period_num
            }
            result = safe_insert('classperiods', class_period)
            if result:
                class_periods.extend(result)
    return class_periods

def main():
    try:
        # Test database connection first
        print("Testing database connection...")
        test = supabase.table('districts').select("*").limit(1).execute()
        print("Connection successful!")

        # Create mock data in order of dependencies
        print("\nCreating districts...")
        districts = create_districts()
        print(f"Created {len(districts)} districts")
        
        print("\nCreating schools...")
        schools = create_schools(districts)
        print(f"Created {len(schools)} schools")
        
        print("\nCreating administrators...")
        admins = create_administrators(schools)
        print(f"Created {len(admins)} administrators")
        
        print("\nCreating instructors...")
        instructors = create_instructors(schools)
        print(f"Created {len(instructors)} instructors")
        
        print("\nCreating students...")
        students = create_students(schools)
        print(f"Created {len(students)} students")
        
        print("\nCreating classrooms...")
        classrooms = create_classrooms(schools, instructors)
        print(f"Created {len(classrooms)} classrooms")
        
        print("\nCreating class periods...")
        class_periods = create_class_periods(classrooms)
        print(f"Created {len(class_periods)} class periods")
        
        print("\nMock data creation completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
