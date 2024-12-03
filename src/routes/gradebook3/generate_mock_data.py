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
        # Pick a random lesson to be watching presentation (1-based index)
        current_lesson = random.randint(1, lesson_count)
        
        for lesson in range(1, lesson_count + 1):
            base_grade = ((unit_num - 1) * 10) + lesson
            
            if lesson < current_lesson:
                # Previous lessons are complete
                unit_data.update(generate_lesson_data(base_grade, "completed"))
            elif lesson == current_lesson:
                # Current lesson - must be watching presentation
                unit_data.update(generate_lesson_data(base_grade, "watching_presentation"))
            else:
                # Future lessons not started
                unit_data.update(generate_lesson_data(base_grade, "not_started"))
    
    elif completion_status == "completed":
        # All lessons complete
        for lesson in range(1, lesson_count + 1):
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
    
    elif status == "in_progress":
        if lesson_index in [2, 3, 4, 6]:
            # For RCA lessons, either RCA is in progress or presentation is
            data[f"grade{grade_num}_presentation"] = random.choice(["Not Started", "In Progress"])
            if data[f"grade{grade_num}_presentation"] == "In Progress":
                # If presentation is in progress, RCA must be completed
                data[f"grade{grade_num}_rca"] = generate_random_grade()
            else:
                # If presentation not started, RCA might be in progress
                if random.random() < 0.7:  # 70% chance to have RCA grade if in progress
                    data[f"grade{grade_num}_rca"] = generate_random_grade()
        
        elif lesson_index == 1:
            # Module Guide lessons
            data[f"grade{grade_num}_presentation"] = random.choice(["Not Started", "In Progress"])
            if data[f"grade{grade_num}_presentation"] == "In Progress":
                data[f"grade{grade_num}_moduleGuide"] = generate_random_grade()
            else:
                if random.random() < 0.7:
                    data[f"grade{grade_num}_moduleGuide"] = generate_random_grade()
        
        elif lesson_index in [5, 9]:
            # Diagnostic Days - 4 sets of diagnostic/mastery/presentation
            # Randomly choose which set is in progress (1-4)
            current_set = random.randint(1, 4)
            
            for i in range(1, 5):
                if i < current_set:
                    # Previous sets are completed
                    data[f"grade{grade_num}_presentation{i}"] = "Completed"
                    data[f"grade{grade_num}_diagnostic{i}"] = generate_random_grade()
                    data[f"grade{grade_num}_mastery{i}a"] = generate_random_grade()
                    data[f"grade{grade_num}_mastery{i}b"] = generate_random_grade()
                elif i == current_set:
                    # Current set is in progress
                    # Determine which part is in progress
                    parts = ["diagnostic", "mastery_a", "mastery_b", "presentation"]
                    current_part_index = random.randint(0, len(parts) - 1)
                    
                    for j, part in enumerate(parts):
                        if j < current_part_index:
                            # Previous parts are completed
                            if part == "presentation":
                                data[f"grade{grade_num}_presentation{i}"] = "Completed"
                            else:
                                data[f"grade{grade_num}_{part}{i}"] = generate_random_grade()
                        elif j == current_part_index:
                            # This part is in progress
                            if part == "presentation":
                                data[f"grade{grade_num}_presentation{i}"] = "In Progress"
                            else:
                                # For assessments, in progress means having a grade
                                data[f"grade{grade_num}_{part}{i}"] = generate_random_grade()
                        else:
                            # Future parts are not started
                            if part == "presentation":
                                data[f"grade{grade_num}_presentation{i}"] = "Not Started"
                else:
                    # Future sets are not started
                    data[f"grade{grade_num}_presentation{i}"] = "Not Started"
        
        elif lesson_index == 8:
            # Post-test lessons
            data[f"grade{grade_num}_presentation"] = random.choice(["Not Started", "In Progress"])
            if data[f"grade{grade_num}_presentation"] == "In Progress":
                data[f"grade{grade_num}_posttest"] = generate_random_grade()
            else:
                if random.random() < 0.7:
                    data[f"grade{grade_num}_posttest"] = generate_random_grade()
        
        elif lesson_index == 7:
            # Presentation-only lessons
            data[f"grade{grade_num}_presentation"] = "In Progress"
    
    elif status == "completed":
        # All components are completed with grades
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
    
    elif status == "watching_presentation":
        if lesson_index in [5, 9]:
            # Diagnostic Days
            current_set = random.randint(1, 4)
            
            for i in range(1, 5):
                if i < current_set:
                    # Previous sets are completed
                    data[f"grade{grade_num}_presentation{i}"] = "Completed"
                    data[f"grade{grade_num}_diagnostic{i}"] = generate_random_grade()
                    data[f"grade{grade_num}_mastery{i}a"] = generate_random_grade()
                    data[f"grade{grade_num}_mastery{i}b"] = generate_random_grade()
                elif i == current_set:
                    # Current set - watching presentation
                    data[f"grade{grade_num}_presentation{i}"] = "In Progress"
                    # Only include diagnostic grade since it comes before presentation
                    data[f"grade{grade_num}_diagnostic{i}"] = generate_random_grade()
                    # Don't generate mastery grades since they come after presentation
                else:
                    # Future sets not started
                    data[f"grade{grade_num}_presentation{i}"] = "Not Started"
        else:
            # Regular lessons
            data[f"grade{grade_num}_presentation"] = "In Progress"
            # Ensure assessment is completed
            if lesson_index == 1:
                data[f"grade{grade_num}_moduleGuide"] = generate_random_grade()
            elif lesson_index in [2, 3, 4, 6]:
                data[f"grade{grade_num}_rca"] = generate_random_grade()
            elif lesson_index == 8:
                data[f"grade{grade_num}_posttest"] = generate_random_grade()
            # Lesson 7 only has presentation, no assessment needed
    
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
            # Pick a random unit to be the student's first unit
            current_unit = random.randint(1, CONFIG["data"]["unitsCount"])
            
            # Generate data for the current unit
            row.update(generate_unit_data(current_unit, CONFIG["data"]["lessonsPerUnit"], "in_progress"))
            
            # All other units are not started
            for unit in range(1, CONFIG["data"]["unitsCount"] + 1):
                if unit != current_unit:
                    row.update(generate_unit_data(unit, CONFIG["data"]["lessonsPerUnit"], "not_started"))
        
        elif progress_type == StudentProgress.MULTIPLE_UNITS:
            # Decide how many units are complete
            units_to_complete = random.randint(1, CONFIG["data"]["unitsCount"] - 2)
            
            # Randomly select which units are complete
            available_units = list(range(1, CONFIG["data"]["unitsCount"] + 1))
            completed_units = random.sample(available_units, units_to_complete)
            
            # Pick one of the remaining units to be in progress
            remaining_units = [u for u in available_units if u not in completed_units]
            current_unit = random.choice(remaining_units)
            remaining_units.remove(current_unit)
            
            # Generate the data
            for unit in range(1, CONFIG["data"]["unitsCount"] + 1):
                if unit in completed_units:
                    row.update(generate_unit_data(unit, CONFIG["data"]["lessonsPerUnit"], "completed"))
                elif unit == current_unit:
                    row.update(generate_unit_data(unit, CONFIG["data"]["lessonsPerUnit"], "in_progress"))
                else:
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