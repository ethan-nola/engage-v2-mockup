# Math Modules Gradebook Data Schema Specification

## Core Tables

### Students
```sql
student_id (primary key)
first_name
last_name
enrollment_date
active_status
current_unit
```

### Units
```sql
unit_id (primary key)
unit_number (1-10)
unit_title
description
```

### Session_Days
```sql
session_day_id (primary key)
unit_id (foreign key)
day_number (1-10)
day_type (enum: 'session', 'diagnostic')
```

### Student_Progress
```sql
progress_id (primary key)
student_id (foreign key)
unit_id (foreign key)
session_day_id (foreign key)
date_started
date_completed
locked_status
instructor_intervention_required
```

### Assessments
```sql
assessment_id (primary key)
progress_id (foreign key)
assessment_type (enum: 'module_guide', 'rca', 'diagnostic', 'mastery', 'post_test')
score
attempt_number
date_completed
```

### Diagnostic_Groups
```sql
diagnostic_group_id (primary key)
session_day_id (foreign key)
group_number (1-4)
```

### Student_Diagnostic_Progress
```sql
diagnostic_progress_id (primary key)
student_id (foreign key)
diagnostic_group_id (foreign key)
current_step (enum: 'diagnostic', 'lesson', 'mastery_1', 'mastery_2')
tested_out
date_started
date_completed
```

## Sample Data Parameters

The mock dataset should include:
- A classroom of 20-30 students
- All 10 units populated with appropriate titles and descriptions
- Various progression scenarios:
  - Students progressing normally through sessions
  - Students testing out of diagnostic groups
  - Students requiring multiple mastery attempts
  - Students needing instructor intervention
  - Students working on enrichment content
- Realistic date ranges showing typical progression timing
- Score distributions that reflect normal classroom performance patterns

## Data Relationships

Each student record connects to multiple progress records, one for each unit they've started. Progress records link to individual assessment scores and diagnostic group progression data. This structure allows tracking of both overall progress and detailed performance metrics while maintaining data integrity and enabling efficient querying of student status.

## Mock Data Generation Guidelines

The mock data should represent realistic scenarios including:
1. Varied progression rates between students
2. Clusters of difficulty around specific diagnostic groups
3. Correlation between performance in related units
4. Natural patterns of improvement over time
5. Realistic completion timeframes for assessments
6. Typical patterns of intervention requirements

This schema enables tracking of both individual student journeys and class-wide performance patterns while supporting the collapsible column interface design. Would you like me to provide specific value ranges or distribution patterns for the mock data generation?