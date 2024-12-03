from faker import Faker
import json
import random
from typing import Dict, List, Union
from enum import Enum

# Initialize Faker
fake = Faker()

class StudentProgress(Enum):
    FIRST_UNIT = "first_unit"           # Working on first unit
    MULTIPLE_UNITS = "multiple_units"    # Completed some units, working on next
    COMPLETED_ALL = "completed_all"      # Completed all units

# Configuration
CONFIG = {
    "grades": {
        "min": 0,
        "max": 100,
        "distribution": {
            "excellent": {"min": 90, "max": 100, "weight": 0.2},
            "good": {"min": 75, "max": 89, "weight": 0.3},
            "average": {"min": 60, "max": 74, "weight": 0.4},
            "poor": {"min": 0, "max": 59, "weight": 0.1}
        }
    },
    "data": {
        "studentCount": 80,
        "unitsCount": 10,
        "lessonsPerUnit": 10
    },
    "progress_distribution": {
        StudentProgress.FIRST_UNIT: 0.4,        # 40% in first unit
        StudentProgress.MULTIPLE_UNITS: 0.5,    # 50% completed some units
        StudentProgress.COMPLETED_ALL: 0.1      # 10% completed all units
    }
}

def generate_random_grade() -> int:
    rand = random.random()
    cumulative_weight = 0
    
    for level in CONFIG["grades"]["distribution"].values():
        cumulative_weight += level["weight"]
        if rand <= cumulative_weight:
            return random.randint(level["min"], level["max"])
    
    return random.randint(CONFIG["grades"]["min"], CONFIG["grades"]["max"])

def get_student_progress_type() -> StudentProgress:
    rand = random.random()
    cumulative = 0
    for progress_type, weight in CONFIG["progress_distribution"].items():
        cumulative += weight
        if rand <= cumulative:
            return progress_type
    return StudentProgress.FIRST_UNIT  # Default to first unit if something goes wrong

def generate_unit_data(unit_num: int, lesson_count: int, completion_status: str) -> Dict:
    """Generate data for a single unit based on completion status"""
    unit_data = {}
    
    if completion_status == "not_started":
        return unit_data
    
    elif completion_status == "in_progress":
        # Randomly choose how many lessons are complete (at least 1)
        lessons_complete = random.randint(1, lesson_count - 1)
        
        for lesson in range(1, lesson_count + 1):
            # Fix: Adjust base_grade calculation to match TypeScript
            base_grade = ((unit_num - 1) * 10) + lesson
            
            if lesson <= lessons_complete:
                # Complete lesson
                unit_data.update(generate_lesson_data(base_grade, "completed"))
            elif lesson == lessons_complete + 1:
                # Current lesson - partially complete
                unit_data.update(generate_lesson_data(base_grade, "in_progress"))
            else:
                # Future lesson - not started
                unit_data.update(generate_lesson_data(base_grade, "not_started"))
                
    elif completion_status == "completed":
        # All lessons complete
        for lesson in range(1, lesson_count + 1):
            # Fix: Adjust base_grade calculation to match TypeScript
            base_grade = ((unit_num - 1) * 10) + lesson
            unit_data.update(generate_lesson_data(base_grade, "completed"))
    
    return unit_data

def generate_lesson_data(grade_num: int, status: str) -> Dict:
    """Generate data for a single lesson based on status"""
    data = {}
    lesson_index = ((grade_num - 1) % 10) + 1
    
    if status == "not_started":
        # Add presentation fields as "Not Started"
        if lesson_index in [5, 9]:
            for i in range(1, 5):
                data[f"grade{grade_num}_presentation{i}"] = "Not Started"
        else:
            data[f"grade{grade_num}_presentation"] = "Not Started"
        return data
    
    elif status == "in_progress":
        # Add presentation as "In Progress" and some grades
        if lesson_index in [5, 9]:
            for i in range(1, 5):
                data[f"grade{grade_num}_presentation{i}"] = "In Progress"
                if random.random() < 0.5:  # 50% chance to have started each assessment
                    data[f"grade{grade_num}_diagnostic{i}"] = generate_random_grade()
                    data[f"grade{grade_num}_mastery{i}a"] = generate_random_grade()
                    data[f"grade{grade_num}_mastery{i}b"] = generate_random_grade()
        else:
            data[f"grade{grade_num}_presentation"] = "In Progress"
            if random.random() < 0.5:  # 50% chance to have started the assessment
                if lesson_index == 1:
                    data[f"grade{grade_num}_moduleGuide"] = generate_random_grade()
                elif lesson_index in [2, 3, 4, 6]:
                    data[f"grade{grade_num}_rca"] = generate_random_grade()
                elif lesson_index == 8:
                    data[f"grade{grade_num}_posttest"] = generate_random_grade()
        return data
    
    elif status == "completed":
        # Add all data as completed
        if lesson_index in [5, 9]:
            for i in range(1, 5):
                data[f"grade{grade_num}_presentation{i}"] = "Completed"
                data[f"grade{grade_num}_diagnostic{i}"] = generate_random_grade()
                data[f"grade{grade_num}_mastery{i}a"] = generate_random_grade()
                data[f"grade{grade_num}_mastery{i}b"] = generate_random_grade()
        else:
            data[f"grade{grade_num}_presentation"] = "Completed"
            if lesson_index == 1:
                data[f"grade{grade_num}_moduleGuide"] = generate_random_grade()
            elif lesson_index in [2, 3, 4, 6]:
                data[f"grade{grade_num}_rca"] = generate_random_grade()
            elif lesson_index == 8:
                data[f"grade{grade_num}_posttest"] = generate_random_grade()
        return data
    
    return data

def generate_mock_data() -> List[Dict[str, Union[str, int]]]:
    rows = []
    
    for _ in range(CONFIG["data"]["studentCount"]):
        row = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name()
        }
        
        progress_type = get_student_progress_type()
        
        if progress_type == StudentProgress.FIRST_UNIT:
            # First unit in progress (with at least one lesson completed)
            row.update(generate_unit_data(1, CONFIG["data"]["lessonsPerUnit"], "in_progress"))
            for unit in range(2, CONFIG["data"]["unitsCount"] + 1):
                row.update(generate_unit_data(unit, CONFIG["data"]["lessonsPerUnit"], "not_started"))
        
        elif progress_type == StudentProgress.MULTIPLE_UNITS:
            # Some units complete, one in progress, rest not started
            completed_units = random.randint(1, CONFIG["data"]["unitsCount"] - 2)
            
            # Complete units
            for unit in range(1, completed_units + 1):
                row.update(generate_unit_data(unit, CONFIG["data"]["lessonsPerUnit"], "completed"))
            
            # Current unit in progress
            row.update(generate_unit_data(completed_units + 1, CONFIG["data"]["lessonsPerUnit"], "in_progress"))
            
            # Remaining units not started
            for unit in range(completed_units + 2, CONFIG["data"]["unitsCount"] + 1):
                row.update(generate_unit_data(unit, CONFIG["data"]["lessonsPerUnit"], "not_started"))
        
        elif progress_type == StudentProgress.COMPLETED_ALL:
            # All units complete
            for unit in range(1, CONFIG["data"]["unitsCount"] + 1):
                row.update(generate_unit_data(unit, CONFIG["data"]["lessonsPerUnit"], "completed"))
        
        rows.append(row)
    
    return rows

if __name__ == "__main__":
    # Generate the mock data
    mock_data = generate_mock_data()
    
    # Save to JSON file in the current directory
    with open('mock_data.json', 'w') as f:
        json.dump({"rowData": mock_data}, f, indent=2) 