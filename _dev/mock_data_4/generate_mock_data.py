import json
import random
from datetime import datetime, timedelta
import names
from typing import List, Dict, Any
import numpy as np

class Student:
    def __init__(self, student_id: int, start_date: datetime):
        self.student_id = student_id
        self.first_name = names.get_first_name()
        self.last_name = names.get_last_name()
        self.enrollment_date = start_date
        
    def to_dict(self) -> Dict:
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "enrollment_date": self.enrollment_date.isoformat()
        }

class UnitDefinitions:
    UNITS = [
        {"id": 1, "title": "Forensic Math", "description": "Applications of mathematics in forensic science"},
        {"id": 2, "title": "Environmental Math", "description": "Mathematical modeling of environmental systems"},
        {"id": 3, "title": "Properties of Math", "description": "Fundamental mathematical properties and principles"},
        {"id": 4, "title": "Chemical Math", "description": "Mathematics in chemical reactions and formulas"},
        {"id": 5, "title": "Math Behind Your Meals", "description": "Mathematical applications in nutrition and cooking"},
        {"id": 6, "title": "Geometric Packing", "description": "Spatial geometry and optimization"},
        {"id": 7, "title": "Factoring & Polynomials", "description": "Advanced algebraic concepts"},
        {"id": 8, "title": "Laser Geometry", "description": "Applications of geometry in optics"},
        {"id": 9, "title": "Gravity of Algebra", "description": "Mathematical modeling of gravitational forces"},
        {"id": 10, "title": "Home Makeover", "description": "Practical applications of geometry and measurement"}
    ]

class ScoreGenerator:
    @staticmethod
    def generate_correlated_score(base_score: float, correlation: float = 0.7) -> float:
        """Generate a new score correlated with the base score"""
        variance = random.uniform(-20, 20) * (1 - correlation)
        new_score = base_score + variance
        return max(min(new_score, 100), 0)
    
    @staticmethod
    def generate_initial_score() -> float:
        """Generate an initial score following a normal distribution"""
        score = random.gauss(75, 15)
        return max(min(score, 100), 0)

class DiagnosticProgressionGenerator:
    def __init__(self, base_performance: float):
        self.base_performance = base_performance
        self.score_gen = ScoreGenerator()

    def generate_group_progression(self, start_time: datetime) -> Dict:
        diagnostic_score = self.score_gen.generate_correlated_score(self.base_performance)
        
        if diagnostic_score == 100:
            return {
                "tested_out": True,
                "steps": [{
                    "type": "diagnostic",
                    "score": 100,
                    "timestamp": start_time.isoformat()
                }]
            }

        progression = [{
            "type": "diagnostic",
            "score": diagnostic_score,
            "timestamp": start_time.isoformat()
        }]

        # Add lesson completion
        lesson_time = start_time + timedelta(minutes=30)
        progression.append({
            "type": "lesson",
            "completed": True,
            "timestamp": lesson_time.isoformat()
        })

        # First mastery attempt
        mastery1_score = self.score_gen.generate_correlated_score(diagnostic_score, 0.8)
        mastery1_time = lesson_time + timedelta(minutes=20)
        progression.append({
            "type": "mastery_1",
            "score": mastery1_score,
            "timestamp": mastery1_time.isoformat()
        })

        if mastery1_score == 100:
            return {
                "tested_out": False,
                "steps": progression
            }

        # Second mastery attempt if needed
        mastery2_score = self.score_gen.generate_correlated_score(mastery1_score, 0.9)
        mastery2_time = mastery1_time + timedelta(minutes=20)
        progression.append({
            "type": "mastery_2",
            "score": mastery2_score,
            "timestamp": mastery2_time.isoformat()
        })

        return {
            "tested_out": mastery2_score == 100,
            "steps": progression,
            "requires_intervention": mastery2_score < 100
        }

class SessionGenerator:
    def __init__(self, base_performance: float):
        self.base_performance = base_performance
        self.score_gen = ScoreGenerator()

    def generate_session_day(self, day_number: int, start_time: datetime) -> Dict:
        # Regular session days (1-4)
        if 1 <= day_number <= 4:
            rca_score = self.score_gen.generate_correlated_score(self.base_performance)
            return {
                "day": day_number,
                "rca_score": rca_score,
                "presentation_complete": True,
                "timestamp": start_time.isoformat()
            }
        # Presentation only (Day 6)
        elif day_number == 6:
            return {
                "day": day_number,
                "presentation_complete": True,
                "timestamp": start_time.isoformat()
            }
        # Post-test day (Day 7)
        elif day_number == 7:
            post_test_score = self.score_gen.generate_correlated_score(self.base_performance)
            return {
                "day": day_number,
                "post_test_score": post_test_score,
                "presentation_complete": True,
                "timestamp": start_time.isoformat()
            }
        # Enrichment day (Day 10)
        elif day_number == 10:
            return {
                "day": day_number,
                "enrichment_complete": random.choice([True, False]),
                "timestamp": start_time.isoformat()
            }

class DataGenerator:
    def __init__(self, num_students: int = 80):
        self.num_students = num_students
        self.start_date = datetime.now() - timedelta(days=180)  # 6 months ago
        
    def generate_student_unit_progress(self, student: Student, unit_number: int, 
                                     start_time: datetime, base_performance: float) -> Dict:
        session_gen = SessionGenerator(base_performance)
        diagnostic_gen = DiagnosticProgressionGenerator(base_performance)
        
        unit_data = {
            "unit_id": unit_number,
            "status": "completed",
            "sessions": [],
            "diagnostic_days": []
        }

        current_time = start_time
        
        # Generate session days 1-4
        for day in range(1, 5):
            session = session_gen.generate_session_day(day, current_time)
            unit_data["sessions"].append(session)
            current_time += timedelta(days=1)

        # Generate first diagnostic day (Day 5)
        diagnostic_day = {
            "day": 5,
            "groups": []
        }
        
        for group in range(1, 5):
            group_progress = diagnostic_gen.generate_group_progression(current_time)
            diagnostic_day["groups"].append({
                "group_number": group,
                **group_progress
            })
            current_time += timedelta(hours=2)
        
        unit_data["diagnostic_days"].append(diagnostic_day)
        current_time += timedelta(days=1)

        # Generate sessions 6-7
        for day in range(6, 8):
            session = session_gen.generate_session_day(day, current_time)
            unit_data["sessions"].append(session)
            current_time += timedelta(days=1)

        # Generate second diagnostic day (Day 9)
        diagnostic_day = {
            "day": 9,
            "groups": []
        }
        
        for group in range(1, 5):
            group_progress = diagnostic_gen.generate_group_progression(current_time)
            diagnostic_day["groups"].append({
                "group_number": group,
                **group_progress
            })
            current_time += timedelta(hours=2)
            
        unit_data["diagnostic_days"].append(diagnostic_day)
        
        # Generate final enrichment day
        session = session_gen.generate_session_day(10, current_time + timedelta(days=1))
        unit_data["sessions"].append(session)

        return unit_data

    def generate_data(self) -> Dict:
        students_data = []
        
        for student_id in range(1, self.num_students + 1):
            # Generate base performance level for student
            base_performance = ScoreGenerator.generate_initial_score()
            
            # Determine how many units this student has completed/started
            units_completed = random.randint(0, 9)
            
            student = Student(student_id, self.start_date)
            student_data = student.to_dict()
            student_data["units"] = []
            
            # Generate completed units
            current_time = self.start_date
            for unit_num in range(1, units_completed + 1):
                unit_progress = self.generate_student_unit_progress(
                    student, unit_num, current_time, base_performance
                )
                student_data["units"].append(unit_progress)
                current_time += timedelta(days=random.randint(10, 15))
            
            # Generate in-progress unit if not completed all units
            if units_completed < 10:
                current_unit = units_completed + 1
                in_progress_unit = self.generate_student_unit_progress(
                    student, current_unit, current_time, base_performance
                )
                in_progress_unit["status"] = "in_progress"
                # Randomly truncate the progress data
                progress_point = random.randint(1, len(in_progress_unit["sessions"]))
                in_progress_unit["sessions"] = in_progress_unit["sessions"][:progress_point]
                if progress_point >= 5:
                    diag_progress = random.randint(0, len(in_progress_unit["diagnostic_days"]))
                    in_progress_unit["diagnostic_days"] = in_progress_unit["diagnostic_days"][:diag_progress]
                else:
                    in_progress_unit["diagnostic_days"] = []
                student_data["units"].append(in_progress_unit)
            
            students_data.append(student_data)
            
        return {
            "students": students_data,
            "units": UnitDefinitions.UNITS,
            "generated_at": datetime.now().isoformat()
        }

def main():
    generator = DataGenerator(80)
    data = generator.generate_data()
    
    with open('../../src/routes/gradebook2/mock-data.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()