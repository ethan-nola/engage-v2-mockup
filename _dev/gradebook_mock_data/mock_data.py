import json
import random
from datetime import datetime, timedelta
import names  # you'll need to pip install names

# Configuration settings
CONFIG = {
    "district": {
        "title": "Sample School District",
        "num_schools": 2,
        "school_name_prefix": ["North", "South", "East", "West", "Central"],
        "school_name_suffix": ["Middle School", "High School", "Academy"]
    },
    "courses": {
        "periods_range": (1, 8),
        "grade_levels": [6, 7, 8, 9],
        "categories": ["Modules", "Expeditions", "IPLs", "Math Connections", "Steps / iLearn"],
        "subjects": {
            "Math": ["Modules", "Expeditions", "IPLs", "Steps/iLearn", "Math Connections"],
            "Science": ["Modules", "Expeditions"]
        }
    },
    "classroom_prefix": ["Room", "Lab", "Studio"],
    "num_students_per_school": 40,
    "num_instructors_per_school": 8,
    "num_administrators_per_school": 2,
    "enrollments_per_student": (2, 4),
    "start_dates": [
        datetime(2024, 1, 15),
        datetime(2024, 1, 16),
        datetime(2024, 1, 17),
        datetime(2024, 1, 18)
    ],
    "output_path": "../../src/routes/gradebook/mock-data.json",
    "grades": {
        "progress_range": (0, 100),
        "grade_range": (60, 100)
    }
}

def generate_email(firstname, lastname, domain="school.edu"):
    return f"{firstname.lower()}.{lastname[0].lower()}@{domain}"

def generate_person():
    firstname = names.get_first_name()
    lastname = names.get_last_name()
    username = f"{firstname.lower()}.{lastname.lower()}"
    
    # Generate a mock password that looks like "Word####"
    password_word = random.choice(['Blue', 'Red', 'Green', 'Yellow', 'Purple', 'Orange', 'Silver', 'Gold'])
    password_numbers = ''.join([str(random.randint(0,9)) for _ in range(4)])
    password = f"{password_word}{password_numbers}"
    
    return {
        "id": f"{random.choice('abcdefghijklmnopqrstuvwxyz')}{random.choice('abcdefghijklmnopqrstuvwxyz')}{random.randint(100,999)}",
        "firstname": firstname,
        "lastname": lastname,
        "email": generate_email(firstname, lastname),
        "username": username,
        "password": password
    }

def generate_course(classroom, instructor, period):
    subject = random.choice(list(CONFIG["courses"]["subjects"].keys()))
    allowed_categories = CONFIG["courses"]["subjects"][subject]
    category = random.choice(allowed_categories)
    
    return {
        "id": f"c{random.randint(1000,9999)}",
        "period": period,
        "title": f"{subject} {category} {random.randint(1,5)}",
        "grade_level": random.choice(CONFIG["courses"]["grade_levels"]),
        "category": category,
        "subject": subject,
        "classroom": classroom["id"],
        "instructor": instructor["id"],
        "enrolled_students": [],
        "student_progress": {},
        "student_grades": {}
    }

def generate_classroom(school_id):
    prefix = random.choice(CONFIG["classroom_prefix"])
    number = random.randint(100, 999)
    return {
        "id": f"{school_id}-{prefix}{number}",
        "title": f"{prefix} {number}",
        "instructor": None,
        "courses": [],
        "students": []
    }

def generate_school():
    name = f"{random.choice(CONFIG['district']['school_name_prefix'])} {random.choice(CONFIG['district']['school_name_suffix'])}"
    school_id = f"s{random.randint(1000,9999)}"
    
    # Generate staff
    administrators = [generate_person() for _ in range(CONFIG["num_administrators_per_school"])]
    instructors = [generate_person() for _ in range(CONFIG["num_instructors_per_school"])]
    students = [generate_person() for _ in range(CONFIG["num_students_per_school"])]
    
    # Create a mapping of subjects to instructors
    subject_instructors = {}
    available_instructors = instructors.copy()
    for subject in CONFIG["courses"]["subjects"].keys():
        if available_instructors:
            instructor = random.choice(available_instructors)
            subject_instructors[subject] = instructor
            available_instructors.remove(instructor)
    
    # Generate classrooms
    classrooms = [generate_classroom(school_id) for _ in range(CONFIG["num_instructors_per_school"])]
    
    # Assign instructors to classrooms and generate courses
    for classroom in classrooms:
        # Pick a subject that still needs courses
        available_subjects = [subject for subject, instructor in subject_instructors.items() 
                            if not any(c["subject"] == subject for c in classroom["courses"])]
        
        if not available_subjects:
            continue
            
        subject = random.choice(available_subjects)
        instructor = subject_instructors[subject]
        classroom["instructor"] = instructor["id"]
        
        # Generate courses for each period
        available_periods = list(range(1, CONFIG["courses"]["periods_range"][1] + 1))
        random.shuffle(available_periods)
        num_courses = random.randint(2, 4)  # Reduced number of courses per classroom
        
        for period in available_periods[:num_courses]:
            course = generate_course(classroom, instructor, period)
            # Override the random subject to match the assigned subject
            course["subject"] = subject
            course["category"] = random.choice(CONFIG["courses"]["subjects"][subject])
            course["title"] = f"{subject} {course['category']} {random.randint(1,5)}"
            classroom["courses"].append(course)
    
    # Create lists of available Math and Science courses
    math_courses = [(classroom, course) 
                   for classroom in classrooms 
                   for course in classroom["courses"]
                   if course["subject"] == "Math"]
    
    science_courses = [(classroom, course) 
                      for classroom in classrooms 
                      for course in classroom["courses"]
                      if course["subject"] == "Science"]
    
    # Assign students to exactly one Math and one Science course
    for student in students:
        # Select one Math course
        if math_courses:
            math_classroom, math_course = random.choice(math_courses)
            math_course["enrolled_students"].append(student["id"])
            math_course["student_progress"][student["id"]] = random.randint(
                CONFIG["grades"]["progress_range"][0],
                CONFIG["grades"]["progress_range"][1]
            )
            math_course["student_grades"][student["id"]] = random.randint(
                CONFIG["grades"]["grade_range"][0],
                CONFIG["grades"]["grade_range"][1]
            )
            if student["id"] not in math_classroom["students"]:
                math_classroom["students"].append(student["id"])
        
        # Select one Science course
        if science_courses:
            science_classroom, science_course = random.choice(science_courses)
            science_course["enrolled_students"].append(student["id"])
            science_course["student_progress"][student["id"]] = random.randint(
                CONFIG["grades"]["progress_range"][0],
                CONFIG["grades"]["progress_range"][1]
            )
            science_course["student_grades"][student["id"]] = random.randint(
                CONFIG["grades"]["grade_range"][0],
                CONFIG["grades"]["grade_range"][1]
            )
            if student["id"] not in science_classroom["students"]:
                science_classroom["students"].append(student["id"])
    
    return {
        "id": school_id,
        "title": name,
        "address": f"{random.randint(100,9999)} Education Ave",
        "administrators": administrators,
        "instructors": instructors,
        "students": students,
        "classrooms": classrooms
    }

def generate_mock_data():
    district = {
        "title": CONFIG["district"]["title"],
        "schools": [generate_school() for _ in range(CONFIG["district"]["num_schools"])]
    }
    
    return district

if __name__ == "__main__":
    # Generate the mock data
    mock_data = generate_mock_data()
    
    # Write to file
    with open(CONFIG["output_path"], 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, indent=2)
    
    print(f"Generated mock data for {len(mock_data['schools'])} schools")
    print(f"Data written to {CONFIG['output_path']}")
