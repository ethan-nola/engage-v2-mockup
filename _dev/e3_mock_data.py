# lms_mock_data.py

from supabase import create_client
import uuid
import random
from datetime import datetime, timedelta, date

# Supabase configuration
SUPABASE_URL = "https://uyybtjxqfhxosuwngbac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5eWJ0anhxZmh4b3N1d25nYmFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyMTEzNTgsImV4cCI6MjA0Nzc4NzM1OH0.NBubYUom-rRzV7ZM74p8bvSo9zE9H8YdldcJ400_86g"  # Use the service_role key here

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# At the start of the script
confirmation = input("This will create mock data in the database. Are you sure? (yes/no): ")
if confirmation.lower() != 'yes':
    print("Operation cancelled")
    exit(0)

try:
    # Test the connection
    test = supabase.table('roles').select('role_id').limit(1).execute()
except Exception as e:
    print(f"Failed to connect to Supabase: {e}")
    exit(1)

print("Successfully connected to Supabase")

# Helper functions
def generate_uuid():
    try:
        return str(uuid.uuid4())
    except Exception as e:
        print(f"Error generating UUID: {e}")
        exit(1)

def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

def validate_email(email):
    return '@' in email and '.' in email

def serialize_date(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj

# Insert mock data
try:
    # ===========================
    # Insert Districts
    # ===========================
    print("\nCreating Districts...")
    district_ids = []
    for i in range(3):
        district_id = generate_uuid()
        district_ids.append(district_id)
        district_data = {
            "district_id": district_id,
            "district_name": f"District {i+1}",
            "status": 'Active'
        }
        supabase.table('districts').insert(district_data).execute()
    print(f"Created {len(district_ids)} districts")

    # ===========================
    # Insert Schools
    # ===========================
    print("\nCreating Schools...")
    school_ids = []
    for i in range(5):
        school_id = generate_uuid()
        school_ids.append(school_id)
        school_data = {
            "school_id": school_id,
            "district_id": random.choice(district_ids),
            "school_name": f"School {i+1}",
            "status": 'Active'
        }
        supabase.table('schools').insert(school_data).execute()
    print(f"Created {len(school_ids)} schools")

    # ===========================
    # Insert Users
    # ===========================
    print("\nRetrieving role IDs...")
    user_ids = []
    roles = ['Student', 'Instructor', 'Educator', 'Admin', 'District Admin']
    role_ids = {}

    # Retrieve role IDs from the database
    roles_data = supabase.table('roles').select('role_id', 'role_name').execute()
    if not roles_data.data:
        print("Error: No roles found in database. Please ensure roles are created first.")
        exit(1)

    for role in roles_data.data:
        role_ids[role['role_name']] = role['role_id']

    # Create Educators
    print("\nCreating Educators...")
    educator_ids = []
    for i in range(2):
        user_id = generate_uuid()
        user_ids.append(user_id)
        educator_ids.append(user_id)
        school_id = random.choice(school_ids)
        first_name = f"EducatorFirst{i+1}"
        last_name = f"EducatorLast{i+1}"
        email = f"educator{i+1}@example.com"
        if not validate_email(email):
            print(f"Invalid email format: {email}")
            continue
        password_hash = 'hashedpassword'
        user_data = {
            "user_id": user_id,
            "school_id": school_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password_hash": password_hash,
            "status": 'Active'
        }
        supabase.table('users').insert(user_data).execute()

        # Assign Educator role
        user_role_data = {
            "user_id": user_id,
            "role_id": role_ids['Educator']
        }
        supabase.table('user_roles').insert(user_role_data).execute()

    # Create Instructors
    print("\nCreating Instructors...")
    instructor_ids = []
    for i in range(3):
        user_id = generate_uuid()
        user_ids.append(user_id)
        instructor_ids.append(user_id)
        school_id = random.choice(school_ids)
        first_name = f"InstructorFirst{i+1}"
        last_name = f"InstructorLast{i+1}"
        email = f"instructor{i+1}@example.com"
        if not validate_email(email):
            print(f"Invalid email format: {email}")
            continue
        password_hash = 'hashedpassword'
        user_data = {
            "user_id": user_id,
            "school_id": school_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password_hash": password_hash,
            "status": 'Active'
        }
        supabase.table('users').insert(user_data).execute()

        # Assign Instructor role
        user_role_data = {
            "user_id": user_id,
            "role_id": role_ids['Instructor']
        }
        supabase.table('user_roles').insert(user_role_data).execute()

    # Create Students
    print("\nCreating Students...")
    student_ids = []
    for i in range(10):
        user_id = generate_uuid()
        user_ids.append(user_id)
        student_ids.append(user_id)
        school_id = random.choice(school_ids)
        first_name = f"StudentFirst{i+1}"
        last_name = f"StudentLast{i+1}"
        email = f"student{i+1}@example.com"
        if not validate_email(email):
            print(f"Invalid email format: {email}")
            continue
        password_hash = 'hashedpassword'
        user_data = {
            "user_id": user_id,
            "school_id": school_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password_hash": password_hash,
            "status": 'Active'
        }
        supabase.table('users').insert(user_data).execute()

        # Assign Student role
        user_role_data = {
            "user_id": user_id,
            "role_id": role_ids['Student']
        }
        supabase.table('user_roles').insert(user_role_data).execute()

    # ===========================
    # Insert CourseTemplates
    # ===========================
    print("\nCreating Course Templates...")
    course_template_ids = []
    for i in range(2):
        course_template_id = generate_uuid()
        course_template_ids.append(course_template_id)
        course_name = f"Course Template {i+1}"
        course_description = f"This is the description for Course Template {i+1}."
        created_by = random.choice(educator_ids)
        subject_area = "Subject Area"
        grade_level = "Grade Level"
        course_template_data = {
            "course_template_id": course_template_id,
            "course_name": course_name,
            "course_description": course_description,
            "created_by": created_by,
            "subject_area": subject_area,
            "grade_level": grade_level,
            "status": 'Active'
        }
        supabase.table('course_templates').insert(course_template_data).execute()

    # ===========================
    # Insert CourseAvailability
    # ===========================
    for course_template_id in course_template_ids:
        # Make available to a random district
        district_id = random.choice(district_ids)
        availability_id = generate_uuid()
        availability_data = {
            "availability_id": availability_id,
            "course_template_id": course_template_id,
            "district_id": district_id,
            "is_available": True
        }
        supabase.table('course_availability').insert(availability_data).execute()

    # ===========================
    # Insert CourseInstances
    # ===========================
    course_instance_ids = []
    for i in range(3):
        course_instance_id = generate_uuid()
        course_instance_ids.append(course_instance_id)
        course_template_id = random.choice(course_template_ids)
        instructor_id = random.choice(instructor_ids)
        school_id = random.choice(school_ids)
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date() + timedelta(days=60)
        instance_code = f"INST{i+1:04d}"
        course_instance_data = {
            "course_instance_id": course_instance_id,
            "course_template_id": course_template_id,
            "instructor_id": instructor_id,
            "school_id": school_id,
            "start_date": serialize_date(start_date),
            "end_date": serialize_date(end_date),
            "instance_code": instance_code,
            "status": 'Active'
        }
        supabase.table('course_instances').insert(course_instance_data).execute()

    # ===========================
    # Insert Enrollments
    # ===========================
    for student_id in student_ids:
        course_instance_id = random.choice(course_instance_ids)
        enrollment_id = generate_uuid()
        enrollment_date = datetime.now()
        enrollment_data = {
            "enrollment_id": enrollment_id,
            "user_id": student_id,
            "course_instance_id": course_instance_id,
            "enrollment_date": serialize_date(enrollment_date),
            "enrollment_status": 'Active'
        }
        supabase.table('enrollments').insert(enrollment_data).execute()

    # ===========================
    # Insert Units
    # ===========================
    unit_ids = []
    for course_template_id in course_template_ids:
        for i in range(2):
            unit_id = generate_uuid()
            unit_ids.append(unit_id)
            unit_title = f"Unit {i+1}"
            unit_description = f"Description for Unit {i+1}"
            sequence_number = i + 1
            unit_data = {
                "unit_id": unit_id,
                "course_template_id": course_template_id,
                "unit_title": unit_title,
                "unit_description": unit_description,
                "sequence_number": sequence_number
            }
            supabase.table('units').insert(unit_data).execute()

    # ===========================
    # Insert Lessons
    # ===========================
    lesson_ids = []
    for unit_id in unit_ids:
        for i in range(3):
            lesson_id = generate_uuid()
            lesson_ids.append(lesson_id)
            lesson_title = f"Lesson {i+1}"
            lesson_description = f"Description for Lesson {i+1}"
            sequence_number = i + 1
            lesson_data = {
                "lesson_id": lesson_id,
                "unit_id": unit_id,
                "lesson_title": lesson_title,
                "lesson_description": lesson_description,
                "sequence_number": sequence_number
            }
            supabase.table('lessons').insert(lesson_data).execute()

    # ===========================
    # Insert Slides
    # ===========================
    slide_ids = []
    for lesson_id in lesson_ids:
        for i in range(2):
            slide_id = generate_uuid()
            slide_ids.append(slide_id)
            sequence_number = i + 1
            slide_type = random.choice(['Text', 'Image', 'Video'])
            slide_data = {
                "slide_id": slide_id,
                "lesson_id": lesson_id,
                "sequence_number": sequence_number,
                "slide_type": slide_type
            }
            supabase.table('slides').insert(slide_data).execute()

    # ===========================
    # Insert SlideMedia
    # ===========================
    for slide_id in slide_ids:
        for i in range(1):
            media_id = generate_uuid()
            sequence_number = i + 1
            media_type = random.choice(['Text', 'Image', 'Video'])
            media_content = f"Content for slide {slide_id}"
            media_data = {
                "media_id": media_id,
                "slide_id": slide_id,
                "media_type": media_type,
                "media_content": media_content,
                "sequence_number": sequence_number
            }
            supabase.table('slide_media').insert(media_data).execute()

    # ===========================
    # Insert Assessments
    # ===========================
    assessment_ids = []
    for unit_id in unit_ids:
        for i in range(1):
            assessment_id = generate_uuid()
            assessment_ids.append(assessment_id)
            assessment_title = f"Assessment {i+1}"
            assessment_description = f"Description for Assessment {i+1}"
            due_date_offset = random.randint(1, 30)
            max_points = 100.00
            assessment_type = 'Quiz'
            assessment_data = {
                "assessment_id": assessment_id,
                "unit_id": unit_id,
                "assessment_title": assessment_title,
                "assessment_description": assessment_description,
                "due_date_offset": due_date_offset,
                "max_points": max_points,
                "assessment_type": assessment_type
            }
            supabase.table('assessments').insert(assessment_data).execute()

    # ===========================
    # Insert Questions
    # ===========================
    question_ids = []
    for assessment_id in assessment_ids:
        for i in range(5):
            question_id = generate_uuid()
            question_ids.append(question_id)
            question_text = f"Question {i+1} text"
            question_type = 'Multiple Choice'
            points = 2.00
            question_data = {
                "question_id": question_id,
                "assessment_id": assessment_id,
                "question_text": question_text,
                "question_type": question_type,
                "points": points
            }
            supabase.table('questions').insert(question_data).execute()

            # Insert QuestionOptions
            for j in range(4):
                option_id = generate_uuid()
                option_text = f"Option {j+1} for Question {i+1}"
                is_correct = True if j == 0 else False  # First option is correct
                option_data = {
                    "option_id": option_id,
                    "question_id": question_id,
                    "option_text": option_text,
                    "is_correct": is_correct
                }
                supabase.table('question_options').insert(option_data).execute()

    # ===========================
    # Insert CourseSchedule
    # ===========================
    for course_instance_id in course_instance_ids:
        for unit_id in unit_ids:
            scheduled_date = datetime.now().date() + timedelta(days=random.randint(1, 10))
            schedule_id = generate_uuid()
            schedule_data = {
                "schedule_id": schedule_id,
                "course_instance_id": course_instance_id,
                "unit_id": unit_id,
                "scheduled_date": serialize_date(scheduled_date)
            }
            supabase.table('course_schedule').insert(schedule_data).execute()

    # ===========================
    # Insert AssessmentAttempts and Responses
    # ===========================
    attempt_records = []  # List to store attempt_id and corresponding student_id and assessment_id

    for student_id in student_ids:
        for assessment_id in assessment_ids:
            attempt_id = generate_uuid()
            course_instance_id = random.choice(course_instance_ids)
            attempt_date = datetime.now() - timedelta(days=random.randint(1, 10))
            score = random.uniform(60, 100)
            time_taken = random.randint(300, 900)
            
            # Store the attempt record
            attempt_records.append({
                'attempt_id': attempt_id,
                'student_id': student_id,
                'assessment_id': assessment_id
            })
            
            attempt_data = {
                "attempt_id": attempt_id,
                "assessment_id": assessment_id,
                "course_instance_id": course_instance_id,
                "user_id": student_id,
                "attempt_date": serialize_date(attempt_date),
                "score": score,
                "time_taken": time_taken
            }
            supabase.table('assessment_attempts').insert(attempt_data).execute()

            # Insert AssessmentResponses
            for question_id in question_ids:
                response_id = generate_uuid()
                selected_option_id = None  # For simplicity, we're not selecting actual options
                answer_text = None
                is_correct = random.choice([True, False])
                response_data = {
                    "response_id": response_id,
                    "attempt_id": attempt_id,
                    "question_id": question_id,
                    "is_correct": is_correct
                }
                supabase.table('assessment_responses').insert(response_data).execute()

    # ===========================
    # Insert Grades
    # ===========================
    for attempt in attempt_records:
        grade_id = generate_uuid()
        graded_by = random.choice(instructor_ids)
        grade_value = random.uniform(60, 100)
        feedback = "Good job!"
        grade_date = datetime.now()
        grade_data = {
            "grade_id": grade_id,
            "attempt_id": attempt['attempt_id'],  # Use existing attempt_id
            "graded_by": graded_by,
            "grade_value": grade_value,
            "feedback": feedback,
            "grade_date": serialize_date(grade_date)
        }
        supabase.table('grades').insert(grade_data).execute()

    print("\nAll mock data created successfully!")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print(f"Error type: {type(e).__name__}")
    print(f"Error occurred in table creation process")
    exit(1)
