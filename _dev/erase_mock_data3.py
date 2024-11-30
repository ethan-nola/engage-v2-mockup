from supabase import create_client

# Initialize Supabase client
SUPABASE_URL = "https://uyybtjxqfhxosuwngbac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5eWJ0anhxZmh4b3N1d25nYmFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyMTEzNTgsImV4cCI6MjA0Nzc4NzM1OH0.NBubYUom-rRzV7ZM74p8bvSo9zE9H8YdldcJ400_86g"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def safe_delete(table_name):
    """Safely delete all records from a table"""
    # Map tables to their primary key columns
    primary_keys = {
        'districts': 'district_id',
        'schools': 'school_id',
        'schooladministrators': 'admin_id',
        'instructors': 'instructor_id',
        'students': 'student_id',
        'classrooms': 'classroom_id',
        'classperiods': 'class_period_id',
        'courses': 'course_id',
        'enrollments': 'enrollment_id',
        'unittemplates': 'unit_template_id',
        'units': 'unit_id',
        'lessontemplates': 'lesson_template_id',
        'lessons': 'lesson_id',
        'assessmenttemplates': 'assessment_template_id',
        'assessments': 'assessment_id',
        'slidetemplates': 'slide_template_id',
        'slides': 'slide_id',
        'questionbank': 'question_bank_id',
        'assessmentquestions': 'assessment_question_id',
        'lessonprogress': 'lesson_progress_id',
        'slideprogress': 'slide_progress_id',
        'assessmentattempts': 'assessment_attempt_id',
        'assessmentquestionresponses': 'response_id',
        'coursegrades': 'course_grade_id',
        'unitgrades': 'unit_grade_id'
    }
    
    try:
        print(f"Deleting from {table_name}...")
        pk = primary_keys.get(table_name)
        if not pk:
            print(f"Warning: No primary key mapping found for {table_name}")
            return
            
        supabase.table(table_name).delete().neq(pk, 0).execute()
    except Exception as e:
        print(f"Error deleting from {table_name}: {str(e)}")

def delete_all_data():
    """Delete all data from tables in reverse order of dependencies"""
    try:
        # Delete grades and progress tracking data first
        print("Deleting grades and progress data...")
        safe_delete('assessmentquestionresponses')
        safe_delete('assessmentattempts')
        safe_delete('slideprogress')
        safe_delete('lessonprogress')
        safe_delete('unitgrades')
        safe_delete('coursegrades')

        # Delete content-related data
        print("Deleting content-related data...")
        safe_delete('assessmentquestions')
        safe_delete('questionbank')
        safe_delete('slides')
        safe_delete('slidetemplates')
        safe_delete('assessments')
        safe_delete('assessmenttemplates')
        safe_delete('lessons')
        safe_delete('lessontemplates')
        safe_delete('units')
        safe_delete('unittemplates')

        # Delete enrollment and course data
        print("Deleting enrollment and course data...")
        safe_delete('enrollments')
        safe_delete('courses')
        safe_delete('classperiods')
        safe_delete('classrooms')

        # Delete user data
        print("Deleting user data...")
        safe_delete('students')
        safe_delete('instructors')
        safe_delete('schooladministrators')

        # Delete organizational structure
        print("Deleting organizational structure...")
        safe_delete('schools')
        safe_delete('districts')

        print("All mock data has been successfully deleted!")

    except Exception as e:
        print(f"An error occurred while deleting data: {str(e)}")

def main():
    user_input = input("This will delete ALL data from ALL tables. Are you sure? (yes/no): ")
    if user_input.lower() == 'yes':
        delete_all_data()
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main() 