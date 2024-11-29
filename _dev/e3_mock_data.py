# lms_mock_data.py

import psycopg2
from psycopg2 import sql
import uuid
import random
from datetime import datetime, timedelta

# Database connection parameters (replace with your actual credentials)
DB_HOST = 'your_supabase_host'
DB_PORT = 'your_supabase_port'
DB_NAME = 'your_database_name'
DB_USER = 'your_database_user'
DB_PASSWORD = 'your_database_password'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
conn.autocommit = True
cursor = conn.cursor()

# Helper functions
def generate_uuid():
    return str(uuid.uuid4())

def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

# Insert mock data
try:
    # ===========================
    # Insert Districts
    # ===========================
    district_ids = []
    for i in range(3):
        district_id = generate_uuid()
        district_ids.append(district_id)
        district_name = f"District {i+1}"
        cursor.execute("""
            INSERT INTO districts (district_id, district_name, status)
            VALUES (%s, %s, %s)
        """, (district_id, district_name, 'Active'))

    # ===========================
    # Insert Schools
    # ===========================
    school_ids = []
    for i in range(5):
        school_id = generate_uuid()
        school_ids.append(school_id)
        district_id = random.choice(district_ids)
        school_name = f"School {i+1}"
        cursor.execute("""
            INSERT INTO schools (school_id, district_id, school_name, status)
            VALUES (%s, %s, %s, %s)
        """, (school_id, district_id, school_name, 'Active'))

    # ===========================
    # Insert Users
    # ===========================
    user_ids = []
    roles = ['Student', 'Instructor', 'Educator', 'Admin', 'District Admin']
    role_ids = {}

    # Retrieve role IDs from the database
    cursor.execute("SELECT role_id, role_name FROM roles")
    roles_data = cursor.fetchall()
    for role in roles_data:
        role_ids[role[1]] = role[0]

    # Create Educators
    educator_ids = []
    for i in range(2):
        user_id = generate_uuid()
        user_ids.append(user_id)
        educator_ids.append(user_id)
        school_id = random.choice(school_ids)
        first_name = f"EducatorFirst{i+1}"
        last_name = f"EducatorLast{i+1}"
        email = f"educator{i+1}@example.com"
        password_hash = 'hashedpassword'
        cursor.execute("""
            INSERT INTO users (user_id, school_id, first_name, last_name, email, password_hash, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, school_id, first_name, last_name, email, password_hash, 'Active'))

        # Assign Educator role
        cursor.execute("""
            INSERT INTO user_roles (user_id, role_id)
            VALUES (%s, %s)
        """, (user_id, role_ids['Educator']))

    # Create Instructors
    instructor_ids = []
    for i in range(3):
        user_id = generate_uuid()
        user_ids.append(user_id)
        instructor_ids.append(user_id)
        school_id = random.choice(school_ids)
        first_name = f"InstructorFirst{i+1}"
        last_name = f"InstructorLast{i+1}"
        email = f"instructor{i+1}@example.com"
        password_hash = 'hashedpassword'
        cursor.execute("""
            INSERT INTO users (user_id, school_id, first_name, last_name, email, password_hash, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, school_id, first_name, last_name, email, password_hash, 'Active'))

        # Assign Instructor role
        cursor.execute("""
            INSERT INTO user_roles (user_id, role_id)
            VALUES (%s, %s)
        """, (user_id, role_ids['Instructor']))

    # Create Students
    student_ids = []
    for i in range(10):
        user_id = generate_uuid()
        user_ids.append(user_id)
        student_ids.append(user_id)
        school_id = random.choice(school_ids)
        first_name = f"StudentFirst{i+1}"
        last_name = f"StudentLast{i+1}"
        email = f"student{i+1}@example.com"
        password_hash = 'hashedpassword'
        cursor.execute("""
            INSERT INTO users (user_id, school_id, first_name, last_name, email, password_hash, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, school_id, first_name, last_name, email, password_hash, 'Active'))

        # Assign Student role
        cursor.execute("""
            INSERT INTO user_roles (user_id, role_id)
            VALUES (%s, %s)
        """, (user_id, role_ids['Student']))

    # ===========================
    # Insert CourseTemplates
    # ===========================
    course_template_ids = []
    for i in range(2):
        course_template_id = generate_uuid()
        course_template_ids.append(course_template_id)
        course_name = f"Course Template {i+1}"
        course_description = f"This is the description for Course Template {i+1}."
        created_by = random.choice(educator_ids)
        subject_area = "Subject Area"
        grade_level = "Grade Level"
        cursor.execute("""
            INSERT INTO course_templates (
                course_template_id, course_name, course_description, created_by,
                subject_area, grade_level, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            course_template_id, course_name, course_description, created_by,
            subject_area, grade_level, 'Active'
        ))

    # ===========================
    # Insert CourseAvailability
    # ===========================
    for course_template_id in course_template_ids:
        # Make available to a random district
        district_id = random.choice(district_ids)
        availability_id = generate_uuid()
        cursor.execute("""
            INSERT INTO course_availability (
                availability_id, course_template_id, district_id, is_available
            ) VALUES (%s, %s, %s, %s)
        """, (availability_id, course_template_id, district_id, True))

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
        cursor.execute("""
            INSERT INTO course_instances (
                course_instance_id, course_template_id, instructor_id, school_id,
                start_date, end_date, instance_code, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            course_instance_id, course_template_id, instructor_id, school_id,
            start_date, end_date, instance_code, 'Active'
        ))

    # ===========================
    # Insert Enrollments
    # ===========================
    for student_id in student_ids:
        course_instance_id = random.choice(course_instance_ids)
        enrollment_id = generate_uuid()
        enrollment_date = datetime.now()
        cursor.execute("""
            INSERT INTO enrollments (
                enrollment_id, user_id, course_instance_id, enrollment_date, enrollment_status
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            enrollment_id, student_id, course_instance_id, enrollment_date, 'Active'
        ))

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
            cursor.execute("""
                INSERT INTO units (
                    unit_id, course_template_id, unit_title, unit_description, sequence_number
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                unit_id, course_template_id, unit_title, unit_description, sequence_number
            ))

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
            cursor.execute("""
                INSERT INTO lessons (
                    lesson_id, unit_id, lesson_title, lesson_description, sequence_number
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                lesson_id, unit_id, lesson_title, lesson_description, sequence_number
            ))

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
            cursor.execute("""
                INSERT INTO slides (
                    slide_id, lesson_id, sequence_number, slide_type
                ) VALUES (%s, %s, %s, %s)
            """, (
                slide_id, lesson_id, sequence_number, slide_type
            ))

    # ===========================
    # Insert SlideMedia
    # ===========================
    for slide_id in slide_ids:
        for i in range(1):
            media_id = generate_uuid()
            sequence_number = i + 1
            media_type = random.choice(['Text', 'Image', 'Video'])
            media_content = f"Content for slide {slide_id}"
            cursor.execute("""
                INSERT INTO slide_media (
                    media_id, slide_id, media_type, media_content, sequence_number
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                media_id, slide_id, media_type, media_content, sequence_number
            ))

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
            cursor.execute("""
                INSERT INTO assessments (
                    assessment_id, unit_id, assessment_title, assessment_description,
                    due_date_offset, max_points, assessment_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                assessment_id, unit_id, assessment_title, assessment_description,
                due_date_offset, max_points, assessment_type
            ))

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
            cursor.execute("""
                INSERT INTO questions (
                    question_id, assessment_id, question_text, question_type, points
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                question_id, assessment_id, question_text, question_type, points
            ))

            # Insert QuestionOptions
            for j in range(4):
                option_id = generate_uuid()
                option_text = f"Option {j+1} for Question {i+1}"
                is_correct = True if j == 0 else False  # First option is correct
                cursor.execute("""
                    INSERT INTO question_options (
                        option_id, question_id, option_text, is_correct
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    option_id, question_id, option_text, is_correct
                ))

    # ===========================
    # Insert CourseSchedule
    # ===========================
    for course_instance_id in course_instance_ids:
        for unit_id in unit_ids:
            scheduled_date = datetime.now().date() + timedelta(days=random.randint(1, 10))
            schedule_id = generate_uuid()
            cursor.execute("""
                INSERT INTO course_schedule (
                    schedule_id, course_instance_id, unit_id, scheduled_date
                ) VALUES (%s, %s, %s, %s)
            """, (
                schedule_id, course_instance_id, unit_id, scheduled_date
            ))

    # ===========================
    # Insert AssessmentAttempts and Responses
    # ===========================
    for student_id in student_ids:
        for assessment_id in assessment_ids:
            attempt_id = generate_uuid()
            course_instance_id = random.choice(course_instance_ids)
            attempt_date = datetime.now() - timedelta(days=random.randint(1, 10))
            score = random.uniform(60, 100)
            time_taken = random.randint(300, 900)
            cursor.execute("""
                INSERT INTO assessment_attempts (
                    attempt_id, assessment_id, course_instance_id, user_id,
                    attempt_date, score, time_taken
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                attempt_id, assessment_id, course_instance_id, student_id,
                attempt_date, score, time_taken
            ))

            # Insert AssessmentResponses
            for question_id in question_ids:
                response_id = generate_uuid()
                selected_option_id = None  # For simplicity, we're not selecting actual options
                answer_text = None
                is_correct = random.choice([True, False])
                cursor.execute("""
                    INSERT INTO assessment_responses (
                        response_id, attempt_id, question_id, is_correct
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    response_id, attempt_id, question_id, is_correct
                ))

    # ===========================
    # Insert Grades
    # ===========================
    for student_id in student_ids:
        for assessment_id in assessment_ids:
            attempt_id = generate_uuid()
            grade_id = generate_uuid()
            graded_by = random.choice(instructor_ids)
            grade_value = random.uniform(60, 100)
            feedback = "Good job!"
            grade_date = datetime.now()
            cursor.execute("""
                INSERT INTO grades (
                    grade_id, attempt_id, graded_by, grade_value, feedback, grade_date
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                grade_id, attempt_id, graded_by, grade_value, feedback, grade_date
            ))

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cursor.close()
    conn.close()
