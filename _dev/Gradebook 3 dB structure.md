## **Table of Contents**

1. [Introduction](#introduction)
2. [Database Overview](#database-overview)
3. [Entities and Attributes](#entities-and-attributes)
   - [1. District](#1-district)
   - [2. School](#2-school)
   - [3. SchoolAdministrator](#3-schooladministrator)
   - [4. Instructor](#4-instructor)
   - [5. Student](#5-student)
   - [6. Classroom](#6-classroom)
   - [7. ClassPeriod](#7-classperiod)
   - [8. Course](#8-course)
   - [9. Enrollment](#9-enrollment)
   - [10. UnitTemplate](#10-unittemplate)
   - [11. Unit](#11-unit)
   - [12. LessonTemplate](#12-lessontemplate)
   - [13. Lesson](#13-lesson)
   - [14. AssessmentTemplate](#14-assessmenttemplate)
   - [15. Assessment](#15-assessment)
   - [16. SlideTemplate](#16-slidetemplate)
   - [17. Slide](#17-slide)
   - [18. QuestionBank](#18-questionbank)
   - [19. AssessmentQuestion](#19-assessmentquestion)
   - [20. LessonProgress](#20-lessonprogress)
   - [21. SlideProgress](#21-slideprogress)
   - [22. AssessmentAttempt](#22-assessmentattempt)
   - [23. AssessmentQuestionResponse](#23-assessmentquestionresponse)
   - [24. CourseGrade](#24-coursegrade)
   - [25. UnitGrade](#25-unitgrade)
4. [Entity Relationships](#entity-relationships)
5. [Data Dictionary](#data-dictionary)
6. [Business Logic and Constraints](#business-logic-and-constraints)
7. [Conclusion](#conclusion)

---

## **Introduction**

### **Purpose**

This document provides a comprehensive specification of the database designed for the Gradebook component of a learning management system (LMS). The database supports the storage and management of courses, units, lessons, assessments, and tracks student progress and grades.

### **Scope**

The database schema includes:

- Entities representing the organizational hierarchy (districts, schools, classrooms).
- User accounts (students, instructors, administrators).
- Educational content structures (courses, units, lessons, assessments).
- Templates for reusable content.
- Tracking of student progress and grades.

---

## **Database Overview**

The database models the LMS with the following hierarchical and relational structure:

- **Organizational Hierarchy**: Districts → Schools → Classrooms.
- **User Accounts**: Administrators, Instructors, Students.
- **Educational Content**:
  - **Templates**: UnitTemplate, LessonTemplate, AssessmentTemplate, SlideTemplate.
  - **Instances**: Unit, Lesson, Assessment, Slide.
- **Progress Tracking**: LessonProgress, SlideProgress, AssessmentAttempt, AssessmentQuestionResponse.
- **Grades**: CourseGrade, UnitGrade.

---

## **Entities and Attributes**

Below are detailed specifications for each entity in the database.

### **1. District**

**Description**: Represents a school district.

| **Attribute**    | **Data Type** | **Constraints**                      | **Description**           |
|------------------|---------------|--------------------------------------|---------------------------|
| district_id      | INT           | PRIMARY KEY                          | Unique identifier         |
| district_title   | VARCHAR(255)  | NOT NULL                             | Name of the district      |

---

### **2. School**

**Description**: Represents a school within a district.

| **Attribute**   | **Data Type** | **Constraints**                      | **Description**             |
|-----------------|---------------|--------------------------------------|-----------------------------|
| school_id       | INT           | PRIMARY KEY                          | Unique identifier           |
| district_id     | INT           | FOREIGN KEY → District(district_id)  | Associated district         |
| school_title    | VARCHAR(255)  | NOT NULL                             | Name of the school          |
| school_address  | VARCHAR(255)  |                                      | Address of the school       |

---

### **3. SchoolAdministrator**

**Description**: Represents a school administrator.

| **Attribute** | **Data Type** | **Constraints**                        | **Description**             |
|---------------|---------------|----------------------------------------|-----------------------------|
| admin_id      | INT           | PRIMARY KEY                            | Unique identifier           |
| school_id     | INT           | FOREIGN KEY → School(school_id)        | Associated school           |
| first_name    | VARCHAR(255)  | NOT NULL                               | Administrator's first name  |
| last_name     | VARCHAR(255)  | NOT NULL                               | Administrator's last name   |
| email         | VARCHAR(255)  | NOT NULL, UNIQUE                       | Email address               |
| password      | VARCHAR(255)  | NOT NULL                               | Encrypted password          |

---

### **4. Instructor**

**Description**: Represents an instructor.

| **Attribute** | **Data Type** | **Constraints**                        | **Description**         |
|---------------|---------------|----------------------------------------|-------------------------|
| instructor_id | INT           | PRIMARY KEY                            | Unique identifier       |
| school_id     | INT           | FOREIGN KEY → School(school_id)        | Associated school       |
| first_name    | VARCHAR(255)  | NOT NULL                               | Instructor's first name |
| last_name     | VARCHAR(255)  | NOT NULL                               | Instructor's last name  |
| email         | VARCHAR(255)  | NOT NULL, UNIQUE                       | Email address           |
| password      | VARCHAR(255)  | NOT NULL                               | Encrypted password      |

---

### **5. Student**

**Description**: Represents a student.

| **Attribute** | **Data Type** | **Constraints**                        | **Description**     |
|---------------|---------------|----------------------------------------|---------------------|
| student_id    | INT           | PRIMARY KEY                            | Unique identifier   |
| school_id     | INT           | FOREIGN KEY → School(school_id)        | Associated school   |
| first_name    | VARCHAR(255)  | NOT NULL                               | Student's first name|
| last_name     | VARCHAR(255)  | NOT NULL                               | Student's last name |
| email         | VARCHAR(255)  | NOT NULL, UNIQUE                       | Email address       |
| password      | VARCHAR(255)  | NOT NULL                               | Encrypted password  |

---

### **6. Classroom**

**Description**: Represents a classroom in a school.

| **Attribute**     | **Data Type** | **Constraints**                      | **Description**         |
|-------------------|---------------|--------------------------------------|-------------------------|
| classroom_id      | INT           | PRIMARY KEY                          | Unique identifier       |
| school_id         | INT           | FOREIGN KEY → School(school_id)      | Associated school       |
| instructor_id     | INT           | FOREIGN KEY → Instructor(instructor_id)| Assigned instructor    |
| classroom_title   | VARCHAR(255)  | NOT NULL                             | Room number or name     |

---

### **7. ClassPeriod**

**Description**: Represents a class period within a classroom.

| **Attribute**     | **Data Type** | **Constraints**                      | **Description**                 |
|-------------------|---------------|--------------------------------------|---------------------------------|
| class_period_id   | INT           | PRIMARY KEY                          | Unique identifier               |
| classroom_id      | INT           | FOREIGN KEY → Classroom(classroom_id)| Associated classroom            |
| period_number     | INT           | NOT NULL, CHECK (period_number BETWEEN 1 AND 8)| Period number (1-8) |

---

### **8. Course**

**Description**: Represents a course taught in a classroom.

| **Attribute**   | **Data Type** | **Constraints**                          | **Description**             |
|-----------------|---------------|------------------------------------------|-----------------------------|
| course_id       | INT           | PRIMARY KEY                              | Unique identifier           |
| classroom_id    | INT           | FOREIGN KEY → Classroom(classroom_id)    | Associated classroom        |
| instructor_id   | INT           | FOREIGN KEY → Instructor(instructor_id)  | Course instructor           |
| course_title    | VARCHAR(255)  | NOT NULL                                 | Title of the course         |
| subject         | VARCHAR(50)   | NOT NULL, CHECK (subject IN ('Math','Science')) | Subject of the course |
| grade_level     | INT           | NOT NULL, CHECK (grade_level BETWEEN 6 AND 9)| Grade level (6-9)     |

---

### **9. Enrollment**

**Description**: Represents a student's enrollment in a course.

| **Attribute**     | **Data Type** | **Constraints**                          | **Description**         |
|-------------------|---------------|------------------------------------------|-------------------------|
| enrollment_id     | INT           | PRIMARY KEY                              | Unique identifier       |
| course_id         | INT           | FOREIGN KEY → Course(course_id)          | Enrolled course         |
| student_id        | INT           | FOREIGN KEY → Student(student_id)        | Enrolled student        |
| class_period_id   | INT           | FOREIGN KEY → ClassPeriod(class_period_id)| Class period assignment |

---

### **10. UnitTemplate**

**Description**: Pre-built unit templates for courses.

| **Attribute**       | **Data Type** | **Constraints**                      | **Description**                 |
|---------------------|---------------|--------------------------------------|---------------------------------|
| unit_template_id    | INT           | PRIMARY KEY                          | Unique identifier               |
| unit_title          | VARCHAR(255)  | NOT NULL                             | Title of the unit template      |
| subject             | VARCHAR(50)   | NOT NULL, CHECK (subject IN ('Math','Science')) | Subject area        |
| grade_level         | INT           | NOT NULL, CHECK (grade_level BETWEEN 6 AND 9)| Grade level (6-9)     |
| description         | TEXT          |                                      | Description of the unit         |

---

### **11. Unit**

**Description**: Instance of a unit within a course, based on a unit template.

| **Attribute**       | **Data Type** | **Constraints**                          | **Description**                   |
|---------------------|---------------|------------------------------------------|-----------------------------------|
| unit_id             | INT           | PRIMARY KEY                              | Unique identifier                 |
| course_id           | INT           | FOREIGN KEY → Course(course_id)          | Associated course                 |
| unit_template_id    | INT           | FOREIGN KEY → UnitTemplate(unit_template_id)| Source unit template          |
| unit_title          | VARCHAR(255)  | NOT NULL                                 | Title of the unit                 |
| order_in_course     | INT           | NOT NULL                                 | Order within the course           |

---

### **12. LessonTemplate**

**Description**: Pre-built lesson templates within a unit template.

| **Attribute**         | **Data Type** | **Constraints**                          | **Description**                 |
|-----------------------|---------------|------------------------------------------|---------------------------------|
| lesson_template_id    | INT           | PRIMARY KEY                              | Unique identifier               |
| unit_template_id      | INT           | FOREIGN KEY → UnitTemplate(unit_template_id)| Parent unit template       |
| lesson_title          | VARCHAR(255)  | NOT NULL                                 | Title of the lesson template    |
| order_in_unit         | INT           | NOT NULL                                 | Order within the unit template  |

---

### **13. Lesson**

**Description**: Instance of a lesson within a unit, based on a lesson template.

| **Attribute**       | **Data Type** | **Constraints**                          | **Description**                   |
|---------------------|---------------|------------------------------------------|-----------------------------------|
| lesson_id           | INT           | PRIMARY KEY                              | Unique identifier                 |
| unit_id             | INT           | FOREIGN KEY → Unit(unit_id)              | Associated unit                   |
| lesson_template_id  | INT           | FOREIGN KEY → LessonTemplate(lesson_template_id)| Source lesson template    |
| lesson_title        | VARCHAR(255)  | NOT NULL                                 | Title of the lesson               |
| order_in_unit       | INT           | NOT NULL                                 | Order within the unit             |

---

### **14. AssessmentTemplate**

**Description**: Pre-built assessment templates within a unit template.

| **Attribute**             | **Data Type** | **Constraints**                          | **Description**                 |
|---------------------------|---------------|------------------------------------------|---------------------------------|
| assessment_template_id    | INT           | PRIMARY KEY                              | Unique identifier               |
| unit_template_id          | INT           | FOREIGN KEY → UnitTemplate(unit_template_id)| Parent unit template       |
| assessment_title          | VARCHAR(255)  | NOT NULL                                 | Title of the assessment template|
| order_in_unit             | INT           | NOT NULL                                 | Order within the unit template  |

---

### **15. Assessment**

**Description**: Instance of an assessment within a unit, based on an assessment template.

| **Attribute**           | **Data Type** | **Constraints**                          | **Description**                   |
|-------------------------|---------------|------------------------------------------|-----------------------------------|
| assessment_id           | INT           | PRIMARY KEY                              | Unique identifier                 |
| unit_id                 | INT           | FOREIGN KEY → Unit(unit_id)              | Associated unit                   |
| assessment_template_id  | INT           | FOREIGN KEY → AssessmentTemplate(assessment_template_id)| Source assessment template |
| assessment_title        | VARCHAR(255)  | NOT NULL                                 | Title of the assessment           |
| order_in_unit           | INT           | NOT NULL                                 | Order within the unit             |

---

### **16. SlideTemplate**

**Description**: Pre-designed slide templates within a lesson template.

| **Attribute**         | **Data Type** | **Constraints**                          | **Description**                 |
|-----------------------|---------------|------------------------------------------|---------------------------------|
| slide_template_id     | INT           | PRIMARY KEY                              | Unique identifier               |
| lesson_template_id    | INT           | FOREIGN KEY → LessonTemplate(lesson_template_id)| Parent lesson template     |
| slide_title           | VARCHAR(255)  | NOT NULL                                 | Title of the slide template     |
| content_type          | VARCHAR(50)   | NOT NULL                                 | Type of content (text, video)   |
| content_data          | TEXT          |                                          | Content data (JSON, text, etc.) |
| order_in_lesson       | INT           | NOT NULL                                 | Order within the lesson template|

---

### **17. Slide**

**Description**: Instance of a slide within a lesson, based on a slide template.

| **Attribute**         | **Data Type** | **Constraints**                          | **Description**                   |
|-----------------------|---------------|------------------------------------------|-----------------------------------|
| slide_id              | INT           | PRIMARY KEY                              | Unique identifier                 |
| lesson_id             | INT           | FOREIGN KEY → Lesson(lesson_id)          | Associated lesson                 |
| slide_template_id     | INT           | FOREIGN KEY → SlideTemplate(slide_template_id)| Source slide template      |
| slide_title           | VARCHAR(255)  | NOT NULL                                 | Title of the slide                |
| custom_content        | TEXT          |                                          | Customized content                |
| order_in_lesson       | INT           | NOT NULL                                 | Order within the lesson           |

---

### **18. QuestionBank**

**Description**: Repository of assessment questions.

| **Attribute**         | **Data Type** | **Constraints**                      | **Description**               |
|-----------------------|---------------|--------------------------------------|-------------------------------|
| question_bank_id      | INT           | PRIMARY KEY                          | Unique identifier             |
| question_text         | TEXT          | NOT NULL                             | Text of the question          |
| question_type         | VARCHAR(50)   | NOT NULL                             | Type of question              |
| options               | TEXT          |                                      | Possible options (if any)     |
| correct_answer        | TEXT          |                                      | Correct answer                |

---

### **19. AssessmentQuestion**

**Description**: Links assessment questions to assessments.

| **Attribute**           | **Data Type** | **Constraints**                          | **Description**                   |
|-------------------------|---------------|------------------------------------------|-----------------------------------|
| assessment_question_id  | INT           | PRIMARY KEY                              | Unique identifier                 |
| assessment_id           | INT           | FOREIGN KEY → Assessment(assessment_id)  | Associated assessment             |
| question_bank_id        | INT           | FOREIGN KEY → QuestionBank(question_bank_id)| Source question            |
| order_in_assessment     | INT           | NOT NULL                                 | Order within the assessment       |

---

### **20. LessonProgress**

**Description**: Tracks a student's progress on lessons.

| **Attribute**       | **Data Type** | **Constraints**                          | **Description**                   |
|---------------------|---------------|------------------------------------------|-----------------------------------|
| lesson_progress_id  | INT           | PRIMARY KEY                              | Unique identifier                 |
| student_id          | INT           | FOREIGN KEY → Student(student_id)        | Student                           |
| lesson_id           | INT           | FOREIGN KEY → Lesson(lesson_id)          | Lesson                            |
| unit_id             | INT           | FOREIGN KEY → Unit(unit_id)              | Unit                              |
| course_id           | INT           | FOREIGN KEY → Course(course_id)          | Course                            |
| status              | VARCHAR(50)   | NOT NULL, CHECK (status IN ('Not Started','In Progress','Completed'))| Progress status       |
| start_date          | DATETIME      |                                          | Date started                      |
| completion_date     | DATETIME      |                                          | Date completed                    |
| time_spent          | INT           |                                          | Time spent (in seconds)           |

---

### **21. SlideProgress**

**Description**: Tracks a student's interaction with slides.

| **Attribute**       | **Data Type** | **Constraints**                          | **Description**                   |
|---------------------|---------------|------------------------------------------|-----------------------------------|
| slide_progress_id   | INT           | PRIMARY KEY                              | Unique identifier                 |
| student_id          | INT           | FOREIGN KEY → Student(student_id)        | Student                           |
| slide_id            | INT           | FOREIGN KEY → Slide(slide_id)            | Slide                             |
| lesson_id           | INT           | FOREIGN KEY → Lesson(lesson_id)          | Lesson                            |
| viewed              | BOOLEAN       | DEFAULT FALSE                            | Whether the slide was viewed      |
| viewed_date         | DATETIME      |                                          | Date viewed                       |
| time_spent          | INT           |                                          | Time spent (in seconds)           |

---

### **22. AssessmentAttempt**

**Description**: Records each attempt a student makes on an assessment.

| **Attribute**           | **Data Type** | **Constraints**                          | **Description**                   |
|-------------------------|---------------|------------------------------------------|-----------------------------------|
| assessment_attempt_id   | INT           | PRIMARY KEY                              | Unique identifier                 |
| student_id              | INT           | FOREIGN KEY → Student(student_id)        | Student                           |
| assessment_id           | INT           | FOREIGN KEY → Assessment(assessment_id)  | Assessment                        |
| unit_id                 | INT           | FOREIGN KEY → Unit(unit_id)              | Unit                              |
| course_id               | INT           | FOREIGN KEY → Course(course_id)          | Course                            |
| attempt_number          | INT           | NOT NULL                                 | Attempt count                     |
| start_time              | DATETIME      |                                          | Attempt start time                |
| end_time                | DATETIME      |                                          | Attempt end time                  |
| score                   | DECIMAL(5,2)  |                                          | Total score achieved              |
| status                  | VARCHAR(50)   | NOT NULL, CHECK (status IN ('Not Started','In Progress','Completed','Submitted'))| Attempt status     |

---

### **23. AssessmentQuestionResponse**

**Description**: Stores responses to assessment questions.

| **Attribute**             | **Data Type** | **Constraints**                          | **Description**                   |
|---------------------------|---------------|------------------------------------------|-----------------------------------|
| response_id               | INT           | PRIMARY KEY                              | Unique identifier                 |
| assessment_attempt_id     | INT           | FOREIGN KEY → AssessmentAttempt(assessment_attempt_id)| Assessment attempt   |
| assessment_question_id    | INT           | FOREIGN KEY → AssessmentQuestion(assessment_question_id)| Assessment question|
| question_bank_id          | INT           | FOREIGN KEY → QuestionBank(question_bank_id)| Question from bank        |
| student_response          | TEXT          |                                          | Student's answer                  |
| is_correct                | BOOLEAN       |                                          | Whether the answer is correct     |
| score                     | DECIMAL(5,2)  |                                          | Score for the question            |

---

### **24. CourseGrade**

**Description**: Stores final or cumulative grades for a course.

| **Attribute**     | **Data Type** | **Constraints**                          | **Description**                   |
|-------------------|---------------|------------------------------------------|-----------------------------------|
| course_grade_id   | INT           | PRIMARY KEY                              | Unique identifier                 |
| student_id        | INT           | FOREIGN KEY → Student(student_id)        | Student                           |
| course_id         | INT           | FOREIGN KEY → Course(course_id)          | Course                            |
| final_grade       | DECIMAL(5,2)  |                                          | Final grade (percentage)          |
| grade_date        | DATETIME      |                                          | Date grade was assigned           |
| comments          | TEXT          |                                          | Instructor comments               |

---

### **25. UnitGrade**

**Description**: Stores cumulative grades for a unit within a course.

| **Attribute**   | **Data Type** | **Constraints**                          | **Description**                   |
|-----------------|---------------|------------------------------------------|-----------------------------------|
| unit_grade_id   | INT           | PRIMARY KEY                              | Unique identifier                 |
| student_id      | INT           | FOREIGN KEY → Student(student_id)        | Student                           |
| unit_id         | INT           | FOREIGN KEY → Unit(unit_id)              | Unit                              |
| course_id       | INT           | FOREIGN KEY → Course(course_id)          | Course                            |
| unit_grade      | DECIMAL(5,2)  |                                          | Grade for the unit                |
| grade_date      | DATETIME      |                                          | Date grade was assigned           |
| comments        | TEXT          |                                          | Instructor comments               |

---

## **Entity Relationships**

- **District** (1) → **School** (Many)
- **School** (1) → **SchoolAdministrator**, **Instructor**, **Student**, **Classroom** (Many)
- **Classroom** (1) → **ClassPeriod**, **Course** (Many)
- **Instructor** (1) → **Course** (Many)
- **Course** (1) → **Unit** (Many)
- **UnitTemplate** (1) → **Unit** (Many)
- **UnitTemplate** (1) → **LessonTemplate**, **AssessmentTemplate** (Many)
- **Unit** (1) → **Lesson**, **Assessment** (Many)
- **LessonTemplate** (1) → **SlideTemplate** (Many)
- **Lesson** (1) → **Slide** (Many)
- **AssessmentTemplate** (1) → **AssessmentQuestion** (Many)
- **Assessment** (1) → **AssessmentQuestion** (Many)
- **AssessmentQuestion** (1) → **AssessmentQuestionResponse** (Many)
- **QuestionBank** (1) → **AssessmentQuestion** (Many)
- **Student** (1) → **Enrollment**, **LessonProgress**, **SlideProgress**, **AssessmentAttempt**, **CourseGrade**, **UnitGrade** (Many)
- **Enrollment** (Many) → **Course** (1), **Student** (1), **ClassPeriod** (1)
- **AssessmentAttempt** (1) → **AssessmentQuestionResponse** (Many)

---

## **Data Dictionary**

The data dictionary provides detailed descriptions of the data stored in each field of the database tables. It includes the table name, field name, data type, constraints, and a brief description.

Due to space constraints, please refer to the **Entities and Attributes** section for detailed field-level information.

---

## **Business Logic and Constraints**

### **User Roles and Permissions**

- **SchoolAdministrator**: Manages school-level settings, instructors, and students.
- **Instructor**: Creates and manages courses, units, and tracks student progress.
- **Student**: Accesses courses, completes lessons and assessments.

### **Course Creation**

- **Instructors** create courses by selecting **UnitTemplates** based on subject and grade level.
- **Units**, **Lessons**, and **Assessments** are copied from templates, allowing customization.

### **Progress Tracking**

- **LessonProgress** tracks student progress at the lesson level.
- **SlideProgress** tracks student interaction with slides.
- **AssessmentAttempt** records each attempt a student makes on an assessment.
- **AssessmentQuestionResponse** stores detailed responses to assessment questions.

### **Grading**

- **AssessmentAttempt.score** stores the score for each assessment attempt.
- **UnitGrade** and **CourseGrade** aggregate assessment scores to provide unit-level and course-level grades.
- **Instructors** can add comments to grades for feedback.

### **Constraints and Data Integrity**

- **Foreign Keys**: Ensure referential integrity between tables.
- **Constraints**: Enforce valid data entry (e.g., CHECK constraints on enumerated fields).
- **Unique Constraints**: Prevent duplicate entries where necessary (e.g., unique emails).

### **Version Control for Templates**

- **Templates** can include a **version_number** field to manage updates.
- **Units**, **Lessons**, **Assessments**, and **Slides** reference the specific version of the template they were copied from.

### **Data Privacy and Security**

- **Password Storage**: Passwords should be stored securely, using hashing and salting.
- **Access Control**: Implement role-based access control to restrict data access based on user roles.
