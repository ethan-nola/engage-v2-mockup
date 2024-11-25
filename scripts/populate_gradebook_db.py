import os
from datetime import datetime, timedelta
from typing import Dict, List
import random
from faker import Faker
from supabase import create_client, Client
from dotenv import load_dotenv

# Configuration object for all generation variables
GENERATION_CONFIG = {
    # Numbers of entities to generate
    'num_instructors': 4,
    'students_per_class': 20,
    'units_per_course': 10,
    'lessons_per_unit': 8,
    'enrollments_per_student': (2, 3),
    
    # Time ranges
    'enrollment_date_range': ('-6m', 'today'),
    'progress_date_range': ('-6m', 'now'),
    
    # Course configuration
    'subjects': ['Mathematics', 'Science', 'History', 'English'],
    'levels': ['101', '201', '301'],
    'class_times': ['9:00 AM', '10:30 AM', '1:00 PM', '2:30 PM'],
    'students_enrolled_per_class': (15, 20),
    
    # Grade ranges
    'score_range': (60, 100),  # (min, max) for random grades
    
    # Status options (matching DB enum types)
    'participation_status_options': ['Not Started', 'In Progress', 'Completed'],
    'lesson_status_options': ['Not Started', 'In Progress', 'Completed'],
    
    # Unit types
    'unit_types': [
        {
            'typename': 'Core Concept Unit',
            'description': 'Fundamental concepts and principles',
            'lessonstructure': {
                'presentation_required': True,
                'assessment_required': True,
                'recommended_lessons': 4
            }
        },
        {
            'typename': 'Practice Unit',
            'description': 'Hands-on practice and application',
            'lessonstructure': {
                'presentation_required': True,
                'assessment_required': True,
                'recommended_lessons': 3
            }
        }
    ],
    
    # Lesson types
    'lesson_types': [
        {
            'typename': 'Lecture',
            'haspresentation': True,
            'hasassessment': True,
            'description': 'Traditional lecture format with presentation and quiz'
        },
        {
            'typename': 'Workshop',
            'haspresentation': True,
            'hasassessment': False,
            'description': 'Interactive workshop with hands-on activities'
        }
    ],
    
    # Assessment types
    'assessment_types': [
        {
            'typename': 'Quiz',
            'description': 'Short assessment to test basic understanding'
        },
        {
            'typename': 'Project',
            'description': 'Comprehensive project to demonstrate mastery'
        }
    ]
}

# Load environment variables
load_dotenv()

# Initialize Faker
fake = Faker()

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def test_connection():
    try:
        result = supabase.table('instructors').select("*").execute()
        print("Successfully connected to Supabase!")
        return True
    except Exception as e:
        print(f"Failed to connect to Supabase: {str(e)}")
        return False

def create_instructors() -> List[Dict]:
    """Create mock instructors"""
    instructors = []
    for _ in range(GENERATION_CONFIG['num_instructors']):
        instructor = {
            'firstname': fake.first_name(),
            'lastname': fake.last_name(),
            'email': fake.email()
        }
        try:
            result = supabase.table('instructors').insert(instructor).execute()
            print(f"Created instructor: {instructor['firstname']} {instructor['lastname']}")
            instructors.append(result.data[0])
        except Exception as e:
            print(f"Failed to create instructor: {str(e)}")
            raise
    return instructors

def create_students() -> List[Dict]:
    """Create mock students"""
    students = []
    total_students = GENERATION_CONFIG['students_per_class'] * GENERATION_CONFIG['num_instructors']
    
    for _ in range(total_students):
        student = {
            'firstname': fake.first_name(),
            'lastname': fake.last_name(),
            'email': fake.email()
        }
        result = supabase.table('students').insert(student).execute()
        students.append(result.data[0])
    return students

def create_unit_types() -> List[Dict]:
    """Create mock unit types"""
    results = []
    for unit_type in GENERATION_CONFIG['unit_types']:
        result = supabase.table('unittypes').insert(unit_type).execute()
        results.append(result.data[0])
    return results

def create_lesson_types() -> List[Dict]:
    """Create mock lesson types"""
    results = []
    for lesson_type in GENERATION_CONFIG['lesson_types']:
        result = supabase.table('lessontypes').insert(lesson_type).execute()
        results.append(result.data[0])
    return results

def create_assessment_types() -> List[Dict]:
    """Create mock assessment types"""
    results = []
    for assessment_type in GENERATION_CONFIG['assessment_types']:
        result = supabase.table('assessmenttypes').insert(assessment_type).execute()
        results.append(result.data[0])
    return results

def create_courses(instructors: List[Dict]) -> List[Dict]:
    """Create mock courses"""
    courses = []
    for instructor in instructors:
        course = {
            'instructorid': instructor['instructorid'],
            'coursename': f"{random.choice(GENERATION_CONFIG['subjects'])} {random.choice(GENERATION_CONFIG['levels'])}",
            'coursedescription': fake.text(max_nb_chars=200)
        }
        result = supabase.table('courses').insert(course).execute()
        courses.append(result.data[0])
    return courses

def create_class_periods(courses: List[Dict]) -> List[Dict]:
    """Create mock class periods"""
    periods = []
    for course in courses:
        for i, time in enumerate(GENERATION_CONFIG['class_times'], 1):
            period = {
                'courseid': course['courseid'],
                'periodname': f"Period {i}",
                'schedule': f"MWF {time}"
            }
            result = supabase.table('classperiods').insert(period).execute()
            periods.append(result.data[0])
    return periods

def create_units(courses: List[Dict], unit_types: List[Dict]) -> List[Dict]:
    """Create mock units"""
    units = []
    for course in courses:
        for i in range(1, GENERATION_CONFIG['units_per_course'] + 1):
            unit = {
                'courseid': course['courseid'],
                'unittypeid': random.choice(unit_types)['unittypeid'],
                'unitname': f"Unit {i}: {fake.catch_phrase()}",
                'unitorder': i
            }
            result = supabase.table('units').insert(unit).execute()
            units.append(result.data[0])
    return units

def create_lessons(units: List[Dict], lesson_types: List[Dict]) -> List[Dict]:
    """Create mock lessons"""
    lessons = []
    for unit in units:
        for i in range(1, GENERATION_CONFIG['lessons_per_unit'] + 1):
            lesson = {
                'unitid': unit['unitid'],
                'lessontypeid': random.choice(lesson_types)['lessontypeid'],
                'lessonname': f"Lesson {i}: {fake.bs()}",
                'lessonorder': i
            }
            result = supabase.table('lessons').insert(lesson).execute()
            lessons.append(result.data[0])
    return lessons

def create_presentations_and_assessments(lessons: List[Dict], assessment_types: List[Dict]) -> tuple[List[Dict], List[Dict]]:
    """Create mock presentations and assessments"""
    presentations = []
    assessments = []
    
    for lesson in lessons:
        # Create presentation
        presentation = {
            'lessonid': lesson['lessonid'],
            'presentationname': f"Presentation: {fake.catch_phrase()}",
            'presentationorder': 1
        }
        pres_result = supabase.table('presentations').insert(presentation).execute()
        presentations.append(pres_result.data[0])
        
        # Create assessment
        assessment = {
            'lessonid': lesson['lessonid'],
            'assessmenttypeid': random.choice(assessment_types)['assessmenttypeid'],
            'assessmentname': f"Assessment: {fake.catch_phrase()}",
            'assessmentorder': 1
        }
        assess_result = supabase.table('assessments').insert(assessment).execute()
        assessments.append(assess_result.data[0])
    
    return presentations, assessments

def create_enrollments(students: List[Dict], periods: List[Dict]) -> List[Dict]:
    """Create mock enrollments"""
    enrollments = []
    min_enrollments, max_enrollments = GENERATION_CONFIG['enrollments_per_student']
    for student in students:
        # Enroll each student in 2-3 random periods
        for period in random.sample(periods, random.randint(min_enrollments, max_enrollments)):
            enrollment = {
                'studentid': student['studentid'],
                'periodid': period['periodid'],
                'enrollmentdate': fake.date_between(
                    start_date=GENERATION_CONFIG['enrollment_date_range'][0],
                    end_date=GENERATION_CONFIG['enrollment_date_range'][1]
                ).isoformat(),
                'status': 'Active'
            }
            result = supabase.table('enrollments').insert(enrollment).execute()
            enrollments.append(result.data[0])
    return enrollments

def create_student_progress(students: List[Dict], presentations: List[Dict], 
                          assessments: List[Dict], lessons: List[Dict]) -> None:
    """Create mock student progress data"""
    for student in students:
        # Create presentation progress
        for presentation in presentations:
            student_presentation = {
                'studentid': student['studentid'],
                'presentationid': presentation['presentationid'],
                'participationstatus': random.choice(GENERATION_CONFIG['participation_status_options'])
                # lastupdated will use DB default
            }
            supabase.table('studentpresentations').insert(student_presentation).execute()
        
        # Create assessment progress
        for assessment in assessments:
            student_assessment = {
                'studentid': student['studentid'],
                'assessmentid': assessment['assessmentid'],
                'scorepercentage': random.uniform(*GENERATION_CONFIG['score_range'])
                # datetaken will use DB default
            }
            supabase.table('studentassessments').insert(student_assessment).execute()
        
        # Create lesson progress
        for lesson in lessons:
            student_lesson = {
                'studentid': student['studentid'],
                'lessonid': lesson['lessonid'],
                'lessonstatus': random.choice(GENERATION_CONFIG['lesson_status_options']),
                'lessongrade': random.uniform(*GENERATION_CONFIG['score_range'])
                # lastupdated will use DB default
            }
            supabase.table('studentlessons').insert(student_lesson).execute()

def main():
    """Main function to populate the database"""
    try:
        print("Starting database population...")
        
        if not test_connection():
            return
            
        print("Creating instructors...")
        instructors = create_instructors()
        print(f"Created {len(instructors)} instructors")
        
        print("Creating students...")
        students = create_students()
        print(f"Created {len(students)} students")
        
        print("Creating unit types...")
        unit_types = create_unit_types()
        print(f"Created {len(unit_types)} unit types")
        
        print("Creating lesson types...")
        lesson_types = create_lesson_types()
        print(f"Created {len(lesson_types)} lesson types")
        
        print("Creating assessment types...")
        assessment_types = create_assessment_types()
        print(f"Created {len(assessment_types)} assessment types")
        
        print("Creating courses...")
        courses = create_courses(instructors)
        print(f"Created {len(courses)} courses")
        
        print("Creating class periods...")
        periods = create_class_periods(courses)
        print(f"Created {len(periods)} class periods")
        
        print("Creating units...")
        units = create_units(courses, unit_types)
        print(f"Created {len(units)} units")
        
        print("Creating lessons...")
        lessons = create_lessons(units, lesson_types)
        print(f"Created {len(lessons)} lessons")
        
        print("Creating presentations and assessments...")
        presentations, assessments = create_presentations_and_assessments(lessons, assessment_types)
        print(f"Created {len(presentations)} presentations and {len(assessments)} assessments")
        
        print("Creating enrollments...")
        enrollments = create_enrollments(students, periods)
        print(f"Created {len(enrollments)} enrollments")
        
        print("Creating student progress...")
        create_student_progress(students, presentations, assessments, lessons)
        print("Completed creating student progress")
        
        print("Database population completed successfully!")
        
    except Exception as e:
        print(f"Error populating database: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 