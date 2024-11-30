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
    'schools_per_district': 1,
    
    # Users per school
    'admins_per_school': 1,
    'instructors_per_school': 2,
    'students_per_school': 80,
    
    # Classroom structure
    'classrooms_per_school': {
        'min': 2,
        'max': 2
    },
    'periods_per_classroom': {
        'min': 4,
        'max': 4
    },
    
    # Course structure
    'courses_per_instructor': {
        'min': 1,
        'max': 1
    },
    'students_per_course': {
        'min': 20,
        'max': 20
    },
    
    # Content structure
    'units_per_course': {
        'min': 2,
        'max': 2
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
    'max_assessment_attempts': 3,
    
    # New template configurations
    'unit_templates': [
        {
            'unit_title': 'Introduction to Algebra',
            'subject': 'Math',
            'grade_level': 7,
            'description': 'Foundational concepts of algebraic thinking',
            'items': [
                {
                    'type': 'Lesson',
                    'title': 'Variables and Expressions',
                    'slide_count': 5
                },
                {
                    'type': 'Assessment',
                    'title': 'Variables Quiz',
                    'question_count': 10
                },
                {
                    'type': 'Lesson',
                    'title': 'Evaluating Expressions',
                    'slide_count': 4
                },
                {
                    'type': 'Assessment',
                    'title': 'Unit Final Test',
                    'question_count': 15
                }
            ]
        },
        {
            'unit_title': 'Forces and Motion',
            'subject': 'Science',
            'grade_level': 7,
            'description': 'Understanding Newton\'s laws of motion and forces',
            'items': [
                {
                    'type': 'Lesson',
                    'title': 'Newton\'s First Law',
                    'slide_count': 6
                },
                {
                    'type': 'Lesson',
                    'title': 'Newton\'s Second Law',
                    'slide_count': 5
                },
                {
                    'type': 'Assessment',
                    'title': 'Newton\'s Laws Quiz',
                    'question_count': 8
                },
                {
                    'type': 'Lesson',
                    'title': 'Newton\'s Third Law',
                    'slide_count': 4
                },
                {
                    'type': 'Assessment',
                    'title': 'Forces and Motion Final',
                    'question_count': 12
                }
            ]
        }
    ],
    
    # Content type configurations
    'slide_types': [
        {'type': 'text', 'weight': 0.4},
        {'type': 'video', 'weight': 0.3},
        {'type': 'interactive', 'weight': 0.2},
        {'type': 'exercise', 'weight': 0.1}
    ],
    
    'question_types': [
        {'type': 'multiple_choice', 'weight': 0.6},
        {'type': 'true_false', 'weight': 0.2},
        {'type': 'short_answer', 'weight': 0.2}
    ]
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

def create_unit_templates():
    """Create unit templates from configuration"""
    unit_templates = []
    for unit in MOCK_DATA_CONFIG['unit_templates']:
        template = {
            'unit_title': unit['unit_title'],
            'subject': unit['subject'],
            'grade_level': unit['grade_level'],
            'description': unit['description']
        }
        result = safe_insert('unittemplates', template)
        if result:
            result[0]['items'] = unit['items']
            unit_templates.extend(result)
    return unit_templates

def create_lesson_and_assessment_templates(unit_templates):
    """Create lesson and assessment templates with their child items"""
    lesson_templates = []
    assessment_templates = []
    
    for unit_template in unit_templates:
        order = 1
        for item in unit_template['items']:
            if item['type'] == 'Lesson':
                lesson = {
                    'unit_template_id': unit_template['unit_template_id'],
                    'lesson_title': item['title'],
                    'order_in_unit': order
                }
                result = safe_insert('lessontemplates', lesson)
                if result:
                    result[0]['slide_count'] = item['slide_count']
                    lesson_templates.extend(result)
            else:  # Assessment
                assessment = {
                    'unit_template_id': unit_template['unit_template_id'],
                    'assessment_title': item['title'],
                    'order_in_unit': order
                }
                result = safe_insert('assessmenttemplates', assessment)
                if result:
                    # Add subject and grade level from parent unit template
                    result[0].update({
                        'question_count': item['question_count'],
                        'subject': unit_template['subject'],
                        'grade_level': unit_template['grade_level']
                    })
                    assessment_templates.extend(result)
            order += 1
            
    return lesson_templates, assessment_templates

def generate_slide_content(slide_type, lesson_title):
    """Generate appropriate content based on slide type"""
    content = {
        'title': f"{lesson_title} - Slide Content",
        'type': slide_type
    }
    
    if slide_type == 'text':
        content['content'] = fake.paragraph(nb_sentences=3)
    elif slide_type == 'video':
        content['content'] = {
            'url': f"https://example.com/videos/{fake.uuid4()}",
            'duration': random.randint(180, 600)  # 3-10 minutes
        }
    elif slide_type == 'interactive':
        content['content'] = {
            'type': random.choice(['drag_and_drop', 'matching', 'fill_in_blank']),
            'elements': [{'id': i, 'text': fake.word()} for i in range(4)]
        }
    else:  # exercise
        content['content'] = {
            'problem': fake.sentence(),
            'solution': fake.sentence()
        }
    
    return json.dumps(content)

def create_slide_templates(lesson_templates):
    """Create slide templates for each lesson template"""
    slide_templates = []
    slide_types = [t['type'] for t in MOCK_DATA_CONFIG['slide_types']]
    weights = [t['weight'] for t in MOCK_DATA_CONFIG['slide_types']]
    
    for lesson_template in lesson_templates:
        for order in range(1, lesson_template['slide_count'] + 1):
            slide_type = random.choices(slide_types, weights=weights)[0]
            template = {
                'lesson_template_id': lesson_template['lesson_template_id'],
                'slide_title': f"Slide {order}",
                'content_type': slide_type,
                'content_data': generate_slide_content(slide_type, lesson_template['lesson_title']),
                'order_in_lesson': order
            }
            result = safe_insert('slidetemplates', template)
            if result:
                slide_templates.extend(result)
    return slide_templates

def generate_question(subject, grade_level):
    """Generate a question based on subject and grade level"""
    question_type = random.choices(
        [t['type'] for t in MOCK_DATA_CONFIG['question_types']],
        weights=[t['weight'] for t in MOCK_DATA_CONFIG['question_types']]
    )[0]
    
    question = {
        'question_text': fake.sentence(),
        'question_type': question_type,
        'correct_answer': None,
        'options': None
    }
    
    if question_type == 'multiple_choice':
        options = [fake.word() for _ in range(4)]
        correct_answer = random.choice(options)
        question['options'] = json.dumps(options)
        question['correct_answer'] = correct_answer
    elif question_type == 'true_false':
        question['options'] = json.dumps(['True', 'False'])
        question['correct_answer'] = random.choice(['True', 'False'])
    else:  # short_answer
        question['correct_answer'] = fake.sentence()
    
    return question

def create_assessments(assessment_templates):
    """Create assessment instances from templates"""
    assessments = []
    for template in assessment_templates:
        assessment = {
            'assessment_template_id': template['assessment_template_id'],
            'assessment_title': template['assessment_title'],
            'order_in_unit': template['order_in_unit']
            # unit_id will be set later when units are created
        }
        result = safe_insert('assessments', assessment)
        if result:
            result[0].update({
                'question_count': template['question_count'],
                'subject': template['subject'],
                'grade_level': template['grade_level']
            })
            assessments.extend(result)
    return assessments

def create_assessment_questions(assessments):
    """Create questions for each assessment"""
    assessment_questions = []
    
    for assessment in assessments:
        for order in range(1, assessment['question_count'] + 1):
            # First create question in question bank
            question = generate_question(
                assessment['subject'],
                assessment['grade_level']
            )
            question_result = safe_insert('questionbank', question)
            
            if question_result:
                # Link question to assessment
                assessment_question = {
                    'assessment_id': assessment['assessment_id'],
                    'question_bank_id': question_result[0]['question_bank_id'],
                    'order_in_assessment': order
                }
                result = safe_insert('assessmentquestions', assessment_question)
                if result:
                    assessment_questions.extend(result)
    
    return assessment_questions

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
        
        print("\nCreating unit templates...")
        unit_templates = create_unit_templates()
        print(f"Created {len(unit_templates)} unit templates")
        
        print("\nCreating lesson templates...")
        lesson_templates, assessment_templates = create_lesson_and_assessment_templates(unit_templates)
        print(f"Created {len(lesson_templates)} lesson templates and {len(assessment_templates)} assessment templates")
        
        print("\nCreating slide templates...")
        slide_templates = create_slide_templates(lesson_templates)
        print(f"Created {len(slide_templates)} slide templates")
        
        print("\nCreating assessments...")
        assessments = create_assessments(assessment_templates)
        print(f"Created {len(assessments)} assessments")
        
        print("\nCreating assessment questions...")
        assessment_questions = create_assessment_questions(assessments)
        print(f"Created {len(assessment_questions)} assessment questions")
        
        print("\nMock data creation completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
