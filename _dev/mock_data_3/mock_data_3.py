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
    ],
    
    # Student activity simulation
    'enrollment_rate': 0.9,  # 90% of students are enrolled in available courses
    'lesson_completion_rate': 0.8,  # 80% of enrolled students complete their lessons
    'slide_view_rate': 0.85,  # 85% of slides in completed lessons are viewed
    'assessment_completion_rate': 0.75,  # 75% of students complete assessments
    'grade_range': {
        'min': 65,
        'max': 100
    }
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

def create_assessments(assessment_templates, units):
    """Create assessment instances from templates"""
    assessments = []
    for unit in units:
        # Find matching templates for this unit's template
        unit_assessment_templates = [
            at for at in assessment_templates 
            if at['unit_template_id'] == unit['unit_template_id']
        ]
        
        for template in unit_assessment_templates:
            assessment = {
                'assessment_template_id': template['assessment_template_id'],
                'unit_id': unit['unit_id'],
                'assessment_title': template['assessment_title'],
                'order_in_unit': template['order_in_unit']
            }
            result = safe_insert('assessments', assessment)
            if result:
                # Add unit reference and template data for easier access later
                result[0].update({
                    'unit': unit,
                    'question_count': template['question_count'],
                    'subject': unit['course']['subject'],
                    'grade_level': unit['course']['grade_level']
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

def create_enrollments(courses, students, class_periods):
    """Create course enrollments for students"""
    enrollments = []
    for student in students:
        # Get courses from the same school as the student
        available_courses = [c for c in courses if c['classroom']['school_id'] == student['school_id']]
        
        # Randomly enroll in courses based on enrollment rate
        for course in available_courses:
            if random.random() < MOCK_DATA_CONFIG['enrollment_rate']:
                # Find available class periods for this course's classroom
                course_periods = [cp for cp in class_periods if cp['classroom_id'] == course['classroom_id']]
                if course_periods:
                    enrollment = {
                        'course_id': course['course_id'],
                        'student_id': student['student_id'],
                        'class_period_id': random.choice(course_periods)['class_period_id']
                    }
                    result = safe_insert('enrollments', enrollment)
                    if result:
                        enrollments.extend(result)
    return enrollments

def datetime_to_string(dt):
    """Convert datetime to ISO format string"""
    if dt is None:
        return None
    return dt.isoformat()

def create_lesson_progress(enrollments, lessons):
    """Track student progress through lessons"""
    lesson_progress = []
    current_date = datetime.now()
    
    for enrollment in enrollments:
        course_lessons = [l for l in lessons if l['unit']['course_id'] == enrollment['course_id']]
        
        for lesson in course_lessons:
            if random.random() < MOCK_DATA_CONFIG['lesson_completion_rate']:
                start_date = current_date - timedelta(days=random.randint(1, 90))
                completion_date = start_date + timedelta(hours=random.randint(1, 24))
                progress = {
                    'student_id': enrollment['student_id'],
                    'lesson_id': lesson['lesson_id'],
                    'unit_id': lesson['unit_id'],
                    'course_id': enrollment['course_id'],
                    'status': 'Completed',
                    'start_date': datetime_to_string(start_date),
                    'completion_date': datetime_to_string(completion_date),
                    'time_spent': random.randint(1800, 7200)  # 30-120 minutes
                }
                result = safe_insert('lessonprogress', progress)
                if result:
                    lesson_progress.extend(result)
    return lesson_progress

def create_slide_progress(lesson_progress, slides):
    """Track student interaction with slides"""
    slide_progress = []
    
    for progress in lesson_progress:
        lesson_slides = [s for s in slides if s['lesson_id'] == progress['lesson_id']]
        
        for slide in lesson_slides:
            if random.random() < MOCK_DATA_CONFIG['slide_view_rate']:
                # Get completion date and handle potential field name differences
                completion_date_str = progress.get('completion_date') or progress.get('completiondate')
                if completion_date_str:
                    try:
                        # Try different datetime formats
                        try:
                            completion_date = datetime.strptime(completion_date_str, '%Y-%m-%dT%H:%M:%S.%f')
                        except ValueError:
                            completion_date = datetime.strptime(completion_date_str, '%Y-%m-%dT%H:%M:%S')
                        
                        viewed_date = completion_date - timedelta(minutes=random.randint(5, 60))
                        
                        progress_record = {
                            'student_id': progress['student_id'],
                            'slide_id': slide['slide_id'],
                            'lesson_id': slide['lesson_id'],
                            'viewed': True,
                            'viewed_date': datetime_to_string(viewed_date)
                        }
                        result = safe_insert('slideprogress', progress_record)
                        if result:
                            slide_progress.extend(result)
                    except ValueError as e:
                        print(f"Warning: Could not parse completion date '{completion_date_str}': {e}")
                else:
                    print(f"Warning: No completion date found for lesson progress (student: {progress['student_id']}, lesson: {progress['lesson_id']})")
    
    return slide_progress

def create_assessment_attempts(enrollments, assessments):
    """Create assessment attempts and responses"""
    assessment_attempts = []
    
    for enrollment in enrollments:
        course_assessments = [a for a in assessments if a['unit']['course_id'] == enrollment['course_id']]
        
        for assessment in course_assessments:
            if random.random() < MOCK_DATA_CONFIG['assessment_completion_rate']:
                # Create 1-3 attempts
                num_attempts = random.randint(1, 3)
                for attempt_num in range(1, num_attempts + 1):
                    start_time = datetime.now() - timedelta(days=random.randint(1, 90))
                    end_time = start_time + timedelta(minutes=random.randint(15, 60))
                    
                    attempt = {
                        'student_id': enrollment['student_id'],
                        'assessment_id': assessment['assessment_id'],
                        'unit_id': assessment['unit_id'],
                        'course_id': enrollment['course_id'],
                        'attempt_number': attempt_num,
                        'start_time': datetime_to_string(start_time),
                        'end_time': datetime_to_string(end_time),
                        'score': random.uniform(
                            MOCK_DATA_CONFIG['grade_range']['min'],
                            MOCK_DATA_CONFIG['grade_range']['max']
                        ),
                        'status': 'Completed'
                    }
                    result = safe_insert('assessmentattempts', attempt)
                    if result:
                        assessment_attempts.extend(result)
    return assessment_attempts

def create_assessment_responses(assessment_attempts, assessment_questions, question_bank_items):
    """Create student responses to assessment questions"""
    responses = []
    
    for attempt in assessment_attempts:
        questions = [q for q in assessment_questions if q['assessment_id'] == attempt['assessment_id']]
        
        for question in questions:
            # Generate response based on question type
            question_data = next(qb for qb in question_bank_items if qb['question_bank_id'] == question['question_bank_id'])
            is_correct = random.random() > 0.3  # 70% chance of correct answer
            
            if question_data['question_type'] == 'multiple_choice':
                options = json.loads(question_data['options'])
                student_response = question_data['correct_answer'] if is_correct else random.choice(options)
            elif question_data['question_type'] == 'true_false':
                student_response = question_data['correct_answer'] if is_correct else ('True' if question_data['correct_answer'] == 'False' else 'False')
            else:  # short_answer
                student_response = question_data['correct_answer'] if is_correct else fake.sentence()
            
            response = {
                'assessment_attempt_id': attempt['assessment_attempt_id'],
                'assessment_question_id': question['assessment_question_id'],
                'question_bank_id': question['question_bank_id'],
                'student_response': student_response,
                'is_correct': is_correct,
                'score': 100 if is_correct else random.randint(0, 50)
            }
            result = safe_insert('assessmentquestionresponses', response)
            if result:
                responses.extend(result)
    return responses

def create_grades(enrollments, units):
    """Create course and unit grades"""
    course_grades = []
    unit_grades = []
    current_date = datetime.now()
    
    for enrollment in enrollments:
        # Create course grade
        course_grade = {
            'student_id': enrollment['student_id'],
            'course_id': enrollment['course_id'],
            'final_grade': random.uniform(
                MOCK_DATA_CONFIG['grade_range']['min'],
                MOCK_DATA_CONFIG['grade_range']['max']
            ),
            'grade_date': datetime_to_string(current_date),
            'comments': random.choice([
                "Excellent work throughout the course",
                "Good effort shown",
                "Needs improvement in assessment scores",
                "Consistent performance",
                None
            ])
        }
        result = safe_insert('coursegrades', course_grade)
        if result:
            course_grades.extend(result)
        
        # Create unit grades
        course_units = [u for u in units if u['course_id'] == enrollment['course_id']]
        for unit in course_units:
            unit_grade = {
                'student_id': enrollment['student_id'],
                'unit_id': unit['unit_id'],
                'course_id': enrollment['course_id'],
                'unit_grade': random.uniform(
                    MOCK_DATA_CONFIG['grade_range']['min'],
                    MOCK_DATA_CONFIG['grade_range']['max']
                ),
                'grade_date': datetime_to_string(current_date),
                'comments': random.choice([
                    "Strong understanding of concepts",
                    "Good progress",
                    "Needs review of key concepts",
                    "Excellent performance",
                    None
                ])
            }
            result = safe_insert('unitgrades', unit_grade)
            if result:
                unit_grades.extend(result)
    
    return course_grades, unit_grades

def create_courses(classrooms, instructors):
    """Create courses for each classroom"""
    courses = []
    # Use subjects and grade levels from unit templates to ensure matches
    subjects = list(set(ut['subject'] for ut in MOCK_DATA_CONFIG['unit_templates']))
    grade_levels = list(set(ut['grade_level'] for ut in MOCK_DATA_CONFIG['unit_templates']))
    
    for classroom in classrooms:
        # Get instructor for this classroom
        instructor = next(i for i in instructors if i['instructor_id'] == classroom['instructor_id'])
        
        num_courses = random.randint(
            MOCK_DATA_CONFIG['courses_per_instructor']['min'],
            MOCK_DATA_CONFIG['courses_per_instructor']['max']
        )
        
        for _ in range(num_courses):
            subject = random.choice(subjects)
            grade_level = random.choice(grade_levels)
            course = {
                'classroom_id': classroom['classroom_id'],
                'instructor_id': instructor['instructor_id'],
                'course_title': f"{subject} {grade_level}",
                'subject': subject,
                'grade_level': grade_level
            }
            result = safe_insert('courses', course)
            if result:
                # Add classroom reference for easier access later
                result[0]['classroom'] = classroom
                courses.extend(result)
    
    return courses

def create_units(courses, unit_templates):
    """Create course units from templates"""
    units = []
    
    for course in courses:
        # Find matching templates for this course's subject and grade level
        matching_templates = [
            ut for ut in unit_templates 
            if ut['subject'] == course['subject'] and ut['grade_level'] == course['grade_level']
        ]
        
        if matching_templates:
            num_units = random.randint(
                MOCK_DATA_CONFIG['units_per_course']['min'],
                MOCK_DATA_CONFIG['units_per_course']['max']
            )
            
            # Randomly select templates and create units
            selected_templates = random.sample(matching_templates, min(num_units, len(matching_templates)))
            
            for order, template in enumerate(selected_templates, 1):
                unit = {
                    'course_id': course['course_id'],
                    'unit_template_id': template['unit_template_id'],
                    'unit_title': template['unit_title'],
                    'order_in_course': order
                }
                result = safe_insert('units', unit)
                if result:
                    # Add course reference for easier access later
                    result[0]['course'] = course
                    units.extend(result)
        else:
            print(f"Warning: No matching unit templates found for course {course['course_title']} " 
                  f"(subject: {course['subject']}, grade: {course['grade_level']})")
    
    return units

def create_lessons(units, lesson_templates):
    """Create lessons for each unit from templates"""
    lessons = []
    
    for unit in units:
        # Find templates for this unit
        unit_lesson_templates = [
            lt for lt in lesson_templates 
            if lt['unit_template_id'] == unit['unit_template_id']
        ]
        
        for template in unit_lesson_templates:
            lesson = {
                'unit_id': unit['unit_id'],
                'lesson_template_id': template['lesson_template_id'],
                'lesson_title': template['lesson_title'],
                'order_in_unit': template['order_in_unit']
            }
            result = safe_insert('lessons', lesson)
            if result:
                # Add unit reference for easier access later
                result[0]['unit'] = unit
                lessons.extend(result)
    
    return lessons

def create_slides(lessons, slide_templates):
    """Create slides for each lesson from templates"""
    slides = []
    
    for lesson in lessons:
        # Find templates for this lesson
        lesson_slide_templates = [
            st for st in slide_templates 
            if st['lesson_template_id'] == lesson['lesson_template_id']
        ]
        
        for template in lesson_slide_templates:
            slide = {
                'lesson_id': lesson['lesson_id'],
                'slide_template_id': template['slide_template_id'],
                'slide_title': template['slide_title'],
                'custom_content': template['content_data'],  # Use template content initially
                'order_in_lesson': template['order_in_lesson']
            }
            result = safe_insert('slides', slide)
            if result:
                # Add lesson reference for easier access later
                result[0]['lesson'] = lesson
                slides.extend(result)
    
    return slides

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
        
        print("\nCreating courses...")
        courses = create_courses(classrooms, instructors)
        print(f"Created {len(courses)} courses")
        
        print("\nCreating units...")
        units = create_units(courses, unit_templates)
        print(f"Created {len(units)} units")
        
        print("\nCreating lessons...")
        lessons = create_lessons(units, lesson_templates)
        print(f"Created {len(lessons)} lessons")
        
        print("\nCreating slides...")
        slides = create_slides(lessons, slide_templates)
        print(f"Created {len(slides)} slides")
        
        print("\nCreating assessments...")
        assessments = create_assessments(assessment_templates, units)
        print(f"Created {len(assessments)} assessments")
        
        print("\nCreating assessment questions...")
        assessment_questions = create_assessment_questions(assessments)
        print(f"Created {len(assessment_questions)} assessment questions")
        
        print("\nCreating enrollments...")
        enrollments = create_enrollments(courses, students, class_periods)
        print(f"Created {len(enrollments)} enrollments")
        
        print("\nCreating lesson progress...")
        lesson_progress = create_lesson_progress(enrollments, lessons)
        print(f"Created {len(lesson_progress)} lesson progress records")
        
        print("\nCreating slide progress...")
        slide_progress = create_slide_progress(lesson_progress, slides)
        print(f"Created {len(slide_progress)} slide progress records")
        
        print("\nCreating assessment attempts...")
        assessment_attempts = create_assessment_attempts(enrollments, assessments)
        print(f"Created {len(assessment_attempts)} assessment attempts")
        
        # Fetch all question bank items
        print("\nFetching question bank items...")
        question_bank_response = supabase.table('questionbank').select("*").execute()
        question_bank_items = question_bank_response.data
        print(f"Found {len(question_bank_items)} question bank items")
        
        print("\nCreating assessment responses...")
        assessment_responses = create_assessment_responses(
            assessment_attempts, 
            assessment_questions,
            question_bank_items
        )
        print(f"Created {len(assessment_responses)} assessment responses")
        
        print("\nCreating grades...")
        course_grades, unit_grades = create_grades(enrollments, units)
        print(f"Created {len(course_grades)} course grades and {len(unit_grades)} unit grades")
        
        print("\nMock data creation completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
