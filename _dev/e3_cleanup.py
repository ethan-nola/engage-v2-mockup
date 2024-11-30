from supabase import create_client
import uuid

# Supabase configuration
SUPABASE_URL = "https://uyybtjxqfhxosuwngbac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5eWJ0anhxZmh4b3N1d25nYmFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyMTEzNTgsImV4cCI6MjA0Nzc4NzM1OH0.NBubYUom-rRzV7ZM74p8bvSo9zE9H8YdldcJ400_86g"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Generate a dummy UUID for comparison
DUMMY_UUID = str(uuid.uuid4())

# Confirmation prompt
confirmation = input("This will DELETE ALL MOCK DATA from the database. Are you sure? (yes/no): ")
if confirmation.lower() != 'yes':
    print("Operation cancelled")
    exit(0)

try:
    # Delete in reverse order of dependencies
    print("Cleaning up tables...")
    
    # Delete grades
    supabase.table('grades').delete().filter('grade_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned grades")
    
    # Delete assessment responses
    supabase.table('assessment_responses').delete().filter('response_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned assessment responses")
    
    # Delete assessment attempts
    supabase.table('assessment_attempts').delete().filter('attempt_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned assessment attempts")
    
    # Delete question options
    supabase.table('question_options').delete().filter('option_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned question options")
    
    # Delete questions
    supabase.table('questions').delete().filter('question_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned questions")
    
    # Delete assessments
    supabase.table('assessments').delete().filter('assessment_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned assessments")
    
    # Delete slide media
    supabase.table('slide_media').delete().filter('media_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned slide media")
    
    # Delete slides
    supabase.table('slides').delete().filter('slide_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned slides")
    
    # Delete lessons
    supabase.table('lessons').delete().filter('lesson_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned lessons")
    
    # Delete units
    supabase.table('units').delete().filter('unit_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned units")
    
    # Delete course schedule
    supabase.table('course_schedule').delete().filter('schedule_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned course schedule")
    
    # Delete enrollments
    supabase.table('enrollments').delete().filter('enrollment_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned enrollments")
    
    # Delete course instances
    supabase.table('course_instances').delete().filter('course_instance_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned course instances")
    
    # Delete course availability
    supabase.table('course_availability').delete().filter('availability_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned course availability")
    
    # Delete course templates
    supabase.table('course_templates').delete().filter('course_template_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned course templates")
    
    # Delete user roles
    supabase.table('user_roles').delete().filter('user_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned user roles")
    
    # Delete users
    supabase.table('users').delete().filter('user_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned users")
    
    # Delete schools
    supabase.table('schools').delete().filter('school_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned schools")
    
    # Delete districts
    supabase.table('districts').delete().filter('district_id', 'neq', DUMMY_UUID).execute()
    print("Cleaned districts")

    print("\nCleanup completed successfully!")

except Exception as e:
    print(f"An error occurred during cleanup: {e}")
    print(f"Error type: {type(e).__name__}")
    exit(1) 