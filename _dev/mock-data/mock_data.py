import json
import random
from datetime import datetime, timedelta
import names  # you'll need to pip install names

# Configuration settings
CONFIG = {
    "num_students": 80,
    "enrollment_range": (2, 4),  # min and max enrollments per student
    "periods_range": (1, 8),     # available periods
    "grade_range": (65, 98),     # min and max grades
    "progress_range": (30, 100), # min and max progress values
    "start_dates": [
        datetime(2024, 1, 15),
        datetime(2024, 1, 16),
        datetime(2024, 1, 17),
        datetime(2024, 1, 18)
    ],
    "subjects": {
        "IPL": ["IPL Series"],
        "Expedition": ["Expedition Rotational Schedule"],
        "Science": ["Science Module Rotational Schedule"],
        "Mathematics": ["Math Module Rotational Schedule"],
        "Module": ["Module / Expedition Rotational Schedule", 
                  "Whole Class Assignment - Module"],
        "Assignment": ["Whole Class Assignment - Expedition"],
        "Dyad": ["Dyad Schedule"]
    },
    "output_path": "../../src/routes/gradebook/mock-data.json"
}

# After the existing CONFIG definition, add these fixed mappings
CONFIG["subject_mappings"] = {
    "IPL": {
        "classroom": "Room 201",
        "instructor": "John Smith"
    },
    "Expedition": {
        "classroom": "Lab A",
        "instructor": "Marie Curie"
    },
    "Science": {
        "classroom": "Room 301",
        "instructor": "Albert Einstein"
    },
    "Mathematics": {
        "classroom": "Room 101",
        "instructor": "Ada Lovelace"
    },
    "Module": {
        "classroom": "Room 401",
        "instructor": "Grace Hopper"
    },
    "Assignment": {
        "classroom": "Room 501",
        "instructor": "Richard Feynman"
    },
    "Dyad": {
        "classroom": "Room 601",
        "instructor": "Katherine Johnson"
    }
}

# Generate classroom numbers and special rooms
CONFIG["classrooms"] = [f"Room {i}" for i in range(100, 400)] + ["Lab A", "Lab B", "Studio 1", "Studio 2"]

def generate_email(firstname, lastname):
    return f"{firstname.lower()}.{lastname[0].lower()}@school.edu"

def generate_enrollment(enrollment_id, start_date):
    subject = random.choice(list(CONFIG["subjects"].keys()))
    classname = random.choice(CONFIG["subjects"][subject])
    subject_info = CONFIG["subject_mappings"][subject]
    return {
        "enrollmentid": enrollment_id,
        "period": random.randint(*CONFIG["periods_range"]),
        "subject": subject,
        "classname": classname,
        "classroom": subject_info["classroom"],  # Use fixed classroom for this subject
        "instructor": subject_info["instructor"],  # Use fixed instructor for this subject
        "progress": random.randint(*CONFIG["progress_range"]),
        "averageGrade": random.randint(*CONFIG["grade_range"]),
        "enrollmentdate": start_date.strftime("%Y-%m-%d"),
        "status": "Active"
    }

def generate_mock_data():
    current_enrollment_id = 1
    students = []

    for i in range(CONFIG["num_students"]):
        firstname = names.get_first_name()
        lastname = names.get_last_name()
        
        # Generate random number of enrollments for each student
        num_enrollments = random.randint(*CONFIG["enrollment_range"])
        enrollments = []
        
        start_date = random.choice(CONFIG["start_dates"])
        
        # Create a list of available periods and randomly select from it
        available_periods = list(range(CONFIG["periods_range"][0], CONFIG["periods_range"][1] + 1))
        random.shuffle(available_periods)
        
        # Get a random selection of subjects (no duplicates)
        available_subjects = list(CONFIG["subjects"].keys())
        random.shuffle(available_subjects)
        selected_subjects = available_subjects[:num_enrollments]
        
        # Take only the first num_enrollments periods
        selected_periods = available_periods[:num_enrollments]
        
        # Create enrollments using unique subjects and periods
        for period, subject in zip(selected_periods, selected_subjects):
            subject_info = CONFIG["subject_mappings"][subject]
            enrollment = {
                "enrollmentid": current_enrollment_id,
                "period": period,
                "subject": subject,
                "classname": random.choice(CONFIG["subjects"][subject]),
                "classroom": subject_info["classroom"],  # Use fixed classroom for this subject
                "instructor": subject_info["instructor"],  # Use fixed instructor for this subject
                "progress": random.randint(*CONFIG["progress_range"]),
                "averageGrade": random.randint(*CONFIG["grade_range"]),
                "enrollmentdate": start_date.strftime("%Y-%m-%d"),
                "status": "Active"
            }
            enrollments.append(enrollment)
            current_enrollment_id += 1

        student = {
            "studentid": f"{random.choice('abcdefghijklmnopqrstuvwxyz')}{random.choice('abcdefghijklmnopqrstuvwxyz')}{random.randint(100,999)}",
            "firstname": firstname,
            "lastname": lastname,
            "email": generate_email(firstname, lastname),
            "enrollments": enrollments
        }
        
        students.append(student)

    return {"students": students}

if __name__ == "__main__":
    # Generate the mock data
    mock_data = generate_mock_data()
    
    # Write to file
    with open(CONFIG["output_path"], 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, indent=2)
    
    print(f"Generated mock data for {len(mock_data['students'])} students")
    print(f"Data written to {CONFIG['output_path']}")
