import random
import json
from datetime import datetime, timedelta
import pandas as pd

# Configuration object for mock data generation
CONFIG = {
    # Basic structure
    'num_students': 20,
    'num_units': 10,
    'num_workstations': 10,  # Multiple units can be assigned to same workstation
    
    # Time parameters
    'semester_start_date': '2024-01-15',
    'semester_weeks': 16,
    
    # Student progress parameters
    'min_units_completed': 3,  # Minimum units any student should have completed
    'max_concurrent_units': 1,  # Maximum units a student can be working on simultaneously
    
    # Score generation
    'score_distribution': {
        'excellent': {'mean': 95, 'std': 3, 'weight': 0.2},
        'good': {'mean': 85, 'std': 5, 'weight': 0.5},
        'struggling': {'mean': 70, 'std': 8, 'weight': 0.3}
    },
    
    # Progress patterns
    'completion_patterns': {
        'sequential': 0.4,  # Percentage of students who mostly go in sequence
        'random': 0.3,      # Percentage who jump around randomly
        'clustered': 0.3    # Percentage who complete related units together
    },
    
    # Mastery attempt patterns
    'mastery_patterns': {
        'first_attempt_success_rate': 0.7,
        'second_attempt_success_rate': 0.85,
        'require_intervention_rate': 0.15
    },
    
    # Special cases
    'include_edge_cases': True,  # Include unusual patterns
    'error_rate': 0.05,  # Rate of missing or error data
}

def generate_student_base():
    """Generate base student population with demographic info."""
    first_names = [
        "Emma", "Liam", "Olivia", "Noah", "Ava", "Elijah", "Sophia", "James",
        "Isabella", "William", "Charlotte", "Oliver", "Amelia", "Benjamin", "Mia",
        "Lucas", "Harper", "Henry", "Evelyn", "Theodore"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]
    
    students = []
    used_names = set()
    
    for _ in range(CONFIG['num_students']):
        while True:
            first = random.choice(first_names)
            last = random.choice(last_names)
            if (first, last) not in used_names:
                used_names.add((first, last))
                students.append({
                    'student_id': f'S{len(students) + 1:04d}',
                    'first_name': first,
                    'last_name': last,
                    'student_type': random.choices(
                        ['excellent', 'good', 'struggling'],
                        weights=[0.2, 0.5, 0.3]
                    )[0]
                })
                break
    
    return students

def generate_unit_structure():
    """Generate the structure of units and their workstation assignments."""
    unit_names = [
        "Forensic Math", "Environmental Math", "Properties of Math",
        "Chemical Math", "Math Behind Your Meals", "Geometric Packing",
        "Factoring & Polynomials", "Laser Geometry", "Gravity of Algebra",
        "Home Makeover"
    ]
    
    units = []
    for i in range(CONFIG['num_units']):
        workstation = f"Station {(i % CONFIG['num_workstations']) + 1}"
        units.append({
            'unit_id': f'U{i + 1:02d}',
            'name': unit_names[i],
            'workstation': workstation,
            'components': generate_unit_components()
        })
    
    return units

def generate_unit_components():
    """Generate the detailed structure of components within a unit."""
    components = []
    
    # Generate standard sessions (S1-S4)
    for session in range(1, 5):
        components.extend([
            {'type': 'module_guide', 'session': f'S{session}'},
            {'type': 'lesson', 'session': f'S{session}'},
            {'type': 'rca', 'session': f'S{session}'}
        ])
    
    # Generate diagnostic day 1 (D1)
    for group in range(1, 5):
        components.extend([
            {'type': 'diagnostic', 'session': f'D1', 'group': group},
            {'type': 'lesson', 'session': f'D1', 'group': group},
            {'type': 'mastery1', 'session': f'D1', 'group': group},
            {'type': 'mastery2', 'session': f'D1', 'group': group}
        ])
    
    # Generate sessions 5-7
    components.extend([
        {'type': 'rca', 'session': 'S5'},
        {'type': 'lesson', 'session': 'S5'},
        {'type': 'lesson', 'session': 'S6'},
        {'type': 'post_test', 'session': 'S6'},
        {'type': 'lesson', 'session': 'S7'}
    ])
    
    # Generate diagnostic day 2 (D2)
    for group in range(1, 5):
        components.extend([
            {'type': 'diagnostic', 'session': f'D2', 'group': group},
            {'type': 'lesson', 'session': f'D2', 'group': group},
            {'type': 'mastery1', 'session': f'D2', 'group': group},
            {'type': 'mastery2', 'session': f'D2', 'group': group}
        ])
    
    # Add enrichment
    components.append({'type': 'enrichment', 'session': 'E'})
    
    return components

def generate_student_progress(student, units):
    """Generate progress data for a student across all units."""
    progress = []
    student_type = student['student_type']
    score_params = CONFIG['score_distribution'][student_type]
    
    # Determine number of units this student has started/completed
    num_units_complete = random.randint(
        CONFIG['min_units_completed'],
        CONFIG['num_units']
    )
    
    # Determine unit order based on student's completion pattern
    unit_order = list(range(CONFIG['num_units']))
    pattern = random.choices(
        list(CONFIG['completion_patterns'].keys()),
        weights=list(CONFIG['completion_patterns'].values())
    )[0]
    
    if pattern == 'sequential':
        # Mostly sequential with small variations
        random.shuffle(unit_order[:2])  # Small variation at start
    elif pattern == 'clustered':
        # Cluster related units together
        unit_order = sorted(unit_order, key=lambda x: units[x]['workstation'])
    else:  # random
        random.shuffle(unit_order)
    
    for unit_idx in unit_order[:num_units_complete]:
        unit = units[unit_idx]
        unit_progress = []
        
        # Generate scores for each component
        for component in unit['components']:
            score = max(0, min(100, random.gauss(score_params['mean'], score_params['std'])))
            
            # Handle mastery attempts
            if component['type'].startswith('mastery'):
                if random.random() > CONFIG['mastery_patterns']['first_attempt_success_rate']:
                    score = max(0, min(100, random.gauss(65, 10)))  # Failed first attempt
                    
                    # Second attempt
                    if component['type'] == 'mastery2':
                        if random.random() > CONFIG['mastery_patterns']['second_attempt_success_rate']:
                            score = None  # Requires intervention
            
            # Add some missing data based on error rate
            if CONFIG['include_edge_cases'] and random.random() < CONFIG['error_rate']:
                score = None
            
            unit_progress.append({
                'component_id': f"{unit['unit_id']}_{component['type']}_{component['session']}",
                'score': score,
                'status': 'completed' if score is not None else 'pending',
                'completed_date': (datetime.strptime(CONFIG['semester_start_date'], '%Y-%m-%d') +
                                 timedelta(days=random.randint(0, CONFIG['semester_weeks'] * 7))).strftime('%Y-%m-%d')
                if score is not None else None
            })
        
        progress.append({
            'unit_id': unit['unit_id'],
            'components': unit_progress
        })
    
    return progress

def generate_mock_data():
    """Generate complete mock dataset."""
    students = generate_student_base()
    units = generate_unit_structure()
    
    dataset = {
        'metadata': {
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'config': CONFIG
        },
        'units': units,
        'students': []
    }
    
    for student in students:
        student_data = student.copy()
        student_data['progress'] = generate_student_progress(student, units)
        dataset['students'].append(student_data)
    
    return dataset

if __name__ == '__main__':
    # Generate mock data
    mock_data = generate_mock_data()
    
    # Save to JSON file
    with open('mock_gradebook_data.json', 'w') as f:
        json.dump(mock_data, f, indent=2)
    
    print(f"Generated mock data for {CONFIG['num_students']} students across {CONFIG['num_units']} units")
    print("Data saved to mock_gradebook_data.json")
