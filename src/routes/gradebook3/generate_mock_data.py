from faker import Faker
import json
import random
from typing import Dict, List, Union

# Initialize Faker
fake = Faker()

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

def generate_random_presentation_status() -> str:
    return random.choice(['Not Started', 'In Progress', 'Completed'])

def generate_mock_data() -> List[Dict[str, Union[str, int]]]:
    rows = []
    
    for _ in range(CONFIG["data"]["studentCount"]):
        row = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name()
        }
        
        total_lessons = CONFIG["data"]["unitsCount"] * CONFIG["data"]["lessonsPerUnit"]
        for j in range(1, total_lessons + 1):
            lesson_index = ((j - 1) % 10) + 1
            
            # Generate data based on lesson type
            if lesson_index == 1:  # Session 1
                row[f"grade{j}_moduleGuide"] = generate_random_grade()
                row[f"grade{j}_presentation"] = generate_random_presentation_status()
            
            elif lesson_index in [2, 3, 4]:  # Sessions 2-4
                row[f"grade{j}_rca"] = generate_random_grade()
                row[f"grade{j}_presentation"] = generate_random_presentation_status()
            
            elif lesson_index in [5, 9]:  # Diagnostic Days
                for diag_num in range(1, 5):
                    row[f"grade{j}_diagnostic{diag_num}"] = generate_random_grade()
                    row[f"grade{j}_presentation{diag_num}"] = generate_random_presentation_status()
                    row[f"grade{j}_mastery{diag_num}a"] = generate_random_grade()
                    row[f"grade{j}_mastery{diag_num}b"] = generate_random_grade()
            
            elif lesson_index == 6:  # Session 5
                row[f"grade{j}_rca"] = generate_random_grade()
                row[f"grade{j}_presentation"] = generate_random_presentation_status()
            
            elif lesson_index == 7:  # Session 6
                row[f"grade{j}_presentation"] = generate_random_presentation_status()
            
            elif lesson_index == 8:  # Session 7
                row[f"grade{j}_posttest"] = generate_random_grade()
                row[f"grade{j}_presentation"] = generate_random_presentation_status()
            
            elif lesson_index == 10:  # Enrichments
                row[f"grade{j}_presentation"] = generate_random_presentation_status()
        
        rows.append(row)
    
    return rows

if __name__ == "__main__":
    # Generate the mock data
    mock_data = generate_mock_data()
    
    # Save to JSON file in the current directory
    with open('mock_data.json', 'w') as f:
        json.dump({"rowData": mock_data}, f, indent=2) 