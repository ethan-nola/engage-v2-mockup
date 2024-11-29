## **Table of Contents**

1. [Introduction](#introduction)
2. [Database Overview](#database-overview)
3. [Entity Descriptions](#entity-descriptions)
   - [1. Districts](#1-districts)
   - [2. Schools](#2-schools)
   - [3. Users](#3-users)
   - [4. Roles](#4-roles)
   - [5. UserRoles](#5-userroles)
   - [6. CourseTemplates](#6-coursetemplates)
   - [7. CourseAvailability](#7-courseavailability)
   - [8. CourseInstances](#8-courseinstances)
   - [9. Enrollments](#9-enrollments)
   - [10. Units](#10-units)
   - [11. Lessons](#11-lessons)
   - [12. Slides](#12-slides)
   - [13. SlideMedia](#13-slidemedia)
   - [14. Assessments](#14-assessments)
   - [15. Questions](#15-questions)
   - [16. QuestionOptions](#16-questionoptions)
   - [17. CourseSchedule](#17-courseschedule)
   - [18. AssessmentAttempts](#18-assessmentattempts)
   - [19. AssessmentResponses](#19-assessmentresponses)
   - [20. Submissions](#20-submissions)
   - [21. Grades](#21-grades)
   - [22. Reporting Tables](#22-reporting-tables)
      - [22.1. FactAssessmentScores](#221-factassessmentscores)
      - [22.2. DimUser](#222-dimuser)
      - [22.3. DimCourse](#223-dimcourse)
      - [22.4. DimTime](#224-dimtime)
   - [23. AuditLogs](#23-auditlogs)
   - [24. Tags and EntityTags](#24-tags-and-entitytags)
4. [Database Relationships](#database-relationships)
5. [Access Control and Permissions](#access-control-and-permissions)
6. [Data Integrity and Constraints](#data-integrity-and-constraints)
7. [Indexes and Performance Optimization](#indexes-and-performance-optimization)
8. [Reporting and Analytics](#reporting-and-analytics)
9. [Data Flow and Usage Scenarios](#data-flow-and-usage-scenarios)
10. [Special Considerations](#special-considerations)
11. [Appendix](#appendix)
    - [A. Data Types and Conventions](#a-data-types-and-conventions)
    - [B. Sample Queries](#b-sample-queries)
    - [C. ER Diagram](#c-er-diagram)

---

## **Introduction**

This documentation provides a comprehensive overview of the database schema for the Learning Management System (LMS). The LMS is designed to deliver pre-built courses created by educators to schools and instructors, with limited customization capabilities. The database supports features such as course content management, user roles, enrollment, assessments, and reporting.

The purpose of this documentation is to assist developers in understanding the database structure, relationships, and the rationale behind the design decisions. It includes detailed descriptions of each table, relationships, constraints, and considerations for development and maintenance.

---

## **Database Overview**

The LMS database is built using PostgreSQL and is designed to:

- **Manage Pre-built Courses:** Courses are created by educators and distributed to schools and districts.
- **Support Hierarchical Structure:** Incorporates districts and schools to mirror real-world educational organizations.
- **Facilitate Limited Customization:** Instructors can schedule courses but cannot modify course content.
- **Enable Robust Reporting:** Provides data structures to support detailed analytics at various organizational levels.
- **Ensure Data Integrity:** Uses constraints, foreign keys, and checks to maintain consistency and reliability.

The database uses **UUIDs** as primary keys for most tables to ensure uniqueness across distributed systems.

---

## **Entity Descriptions**

### **1. Districts**

**Purpose:** Represents educational districts overseeing multiple schools.

**Fields:**

- `district_id` (UUID, PK): Unique identifier for the district.
- `district_name` (VARCHAR): Name of the district.
- `district_address` (VARCHAR): Address of the district office.
- `contact_email` (VARCHAR): Contact email.
- `phone_number` (VARCHAR): Contact phone number.
- `status` (VARCHAR): Status of the district (Active/Inactive).

**Notes:**

- **Primary Key:** `district_id`.
- **Relationships:** One-to-many with **Schools**.

---

### **2. Schools**

**Purpose:** Represents individual schools within districts.

**Fields:**

- `school_id` (UUID, PK): Unique identifier for the school.
- `district_id` (UUID, FK): References **Districts**.
- `school_name` (VARCHAR): Name of the school.
- `school_address` (VARCHAR): Address of the school.
- `contact_email` (VARCHAR): Contact email.
- `phone_number` (VARCHAR): Contact phone number.
- `status` (VARCHAR): Status of the school (Active/Inactive).

**Notes:**

- **Foreign Key:** `district_id` references **Districts**.
- **Relationships:** One-to-many with **Users**, **CourseInstances**.

---

### **3. Users**

**Purpose:** Stores information about all users, including students, instructors, educators, and administrators.

**Fields:**

- `user_id` (UUID, PK): Unique identifier for the user.
- `school_id` (UUID, FK): References **Schools**.
- `first_name` (VARCHAR): First name.
- `last_name` (VARCHAR): Last name.
- `email` (VARCHAR): Unique email address.
- `password_hash` (VARCHAR): Hashed password.
- `profile_picture` (VARCHAR): URL to profile picture.
- `date_of_birth` (DATE): Date of birth.
- `registration_date` (TIMESTAMP): Registration date.
- `status` (VARCHAR): Status of the user (Active/Inactive).

**Notes:**

- **Unique Constraint:** `email`.
- **Foreign Key:** `school_id` references **Schools**.
- **Relationships:** Many-to-many with **Roles** via **UserRoles**.

---

### **4. Roles**

**Purpose:** Defines different roles within the system.

**Fields:**

- `role_id` (SERIAL, PK): Unique identifier for the role.
- `role_name` (VARCHAR): Name of the role (e.g., Student, Instructor).

**Notes:**

- **Unique Constraint:** `role_name`.
- **Relationships:** Many-to-many with **Users** via **UserRoles**.

---

### **5. UserRoles**

**Purpose:** Associates users with their roles.

**Fields:**

- `user_id` (UUID, FK): References **Users**.
- `role_id` (INT, FK): References **Roles**.

**Notes:**

- **Primary Key:** Composite of `user_id`, `role_id`.
- **Relationships:** Links **Users** and **Roles**.

---

### **6. CourseTemplates**

**Purpose:** Stores pre-built courses created by educators.

**Fields:**

- `course_template_id` (UUID, PK): Unique identifier for the course template.
- `course_name` (VARCHAR): Name of the course.
- `course_description` (TEXT): Description of the course.
- `created_by` (UUID, FK): References **Users** (Educator).
- `creation_date` (TIMESTAMP): Date of creation.
- `subject_area` (VARCHAR): Subject area.
- `grade_level` (VARCHAR): Grade level.
- `status` (VARCHAR): Status (Active/Inactive).

**Notes:**

- **Foreign Key:** `created_by` references **Users**.
- **Relationships:** One-to-many with **Units**, **CourseAvailability**.

---

### **7. CourseAvailability**

**Purpose:** Controls availability of course templates to districts and schools.

**Fields:**

- `availability_id` (UUID, PK): Unique identifier.
- `course_template_id` (UUID, FK): References **CourseTemplates**.
- `district_id` (UUID, FK): References **Districts** (Nullable).
- `school_id` (UUID, FK): References **Schools** (Nullable).
- `is_available` (BOOLEAN): Availability status.
- `availability_date` (TIMESTAMP): Date when the course becomes available.

**Notes:**

- **Constraints:**
  - At least one of `district_id` or `school_id` must be provided.
  - `CHECK` constraint ensures only one is non-null.
- **Unique Constraint:** Combination of `course_template_id`, `district_id`, `school_id`.
- **Relationships:** Links **CourseTemplates** to **Districts** or **Schools**.

---

### **8. CourseInstances**

**Purpose:** Represents instances of course templates assigned to instructors and their students.

**Fields:**

- `course_instance_id` (UUID, PK): Unique identifier.
- `course_template_id` (UUID, FK): References **CourseTemplates**.
- `instructor_id` (UUID, FK): References **Users** (Instructor).
- `school_id` (UUID, FK): References **Schools**.
- `start_date` (DATE): Start date.
- `end_date` (DATE): End date.
- `instance_code` (VARCHAR): Unique code for the instance.
- `status` (VARCHAR): Status (Active/Completed).

**Notes:**

- **Unique Constraint:** `instance_code`.
- **Foreign Keys:** References **CourseTemplates**, **Users**, **Schools**.
- **Relationships:** One-to-many with **Enrollments**, **CourseSchedule**.

---

### **9. Enrollments**

**Purpose:** Tracks student enrollment in course instances.

**Fields:**

- `enrollment_id` (UUID, PK): Unique identifier.
- `user_id` (UUID, FK): References **Users** (Student).
- `course_instance_id` (UUID, FK): References **CourseInstances**.
- `enrollment_date` (TIMESTAMP): Date of enrollment.
- `enrollment_status` (VARCHAR): Status (Active/Completed).

**Notes:**

- **Foreign Keys:** References **Users**, **CourseInstances**.

---

### **10. Units**

**Purpose:** Organizes course templates into units.

**Fields:**

- `unit_id` (UUID, PK): Unique identifier.
- `course_template_id` (UUID, FK): References **CourseTemplates**.
- `unit_title` (VARCHAR): Title of the unit.
- `unit_description` (TEXT): Description.
- `sequence_number` (INT): Order in the course.

**Notes:**

- **Foreign Key:** `course_template_id` references **CourseTemplates**.
- **Constraints:** `sequence_number` must be positive.
- **Relationships:** One-to-many with **Lessons**, **Assessments**.

---

### **11. Lessons**

**Purpose:** Represents lessons within units.

**Fields:**

- `lesson_id` (UUID, PK): Unique identifier.
- `unit_id` (UUID, FK): References **Units**.
- `lesson_title` (VARCHAR): Title of the lesson.
- `lesson_description` (TEXT): Description.
- `sequence_number` (INT): Order in the unit.

**Notes:**

- **Foreign Key:** `unit_id` references **Units**.
- **Constraints:** `sequence_number` must be positive.
- **Relationships:** One-to-many with **Slides**.

---

### **12. Slides**

**Purpose:** Stores content for lessons, organized into slides.

**Fields:**

- `slide_id` (UUID, PK): Unique identifier.
- `lesson_id` (UUID, FK): References **Lessons**.
- `sequence_number` (INT): Order in the lesson.
- `slide_type` (VARCHAR): Type of slide (Text/Image/Video).

**Notes:**

- **Foreign Key:** `lesson_id` references **Lessons**.
- **Constraints:** `sequence_number` must be positive.
- **Relationships:** One-to-many with **SlideMedia**.

---

### **13. SlideMedia**

**Purpose:** Stores media elements associated with slides.

**Fields:**

- `media_id` (UUID, PK): Unique identifier.
- `slide_id` (UUID, FK): References **Slides**.
- `media_type` (VARCHAR): Type of media (Text/Image/Audio).
- `media_content` (TEXT): Content or URL.
- `sequence_number` (INT): Order in the slide.

**Notes:**

- **Foreign Key:** `slide_id` references **Slides**.
- **Constraints:** `sequence_number` must be positive.

---

### **14. Assessments**

**Purpose:** Represents assessments within units (e.g., quizzes).

**Fields:**

- `assessment_id` (UUID, PK): Unique identifier.
- `unit_id` (UUID, FK): References **Units**.
- `assessment_title` (VARCHAR): Title of the assessment.
- `assessment_description` (TEXT): Description.
- `due_date_offset` (INT): Days from course start date.
- `max_points` (DECIMAL): Maximum points.
- `assessment_type` (VARCHAR): Type (Quiz/Assignment).

**Notes:**

- **Foreign Key:** `unit_id` references **Units**.
- **Relationships:** One-to-many with **Questions**.

---

### **15. Questions**

**Purpose:** Stores questions for assessments.

**Fields:**

- `question_id` (UUID, PK): Unique identifier.
- `assessment_id` (UUID, FK): References **Assessments**.
- `question_text` (TEXT): The question.
- `question_type` (VARCHAR): Type (Multiple Choice/Free Text).
- `points` (DECIMAL): Points for the question.

**Notes:**

- **Foreign Key:** `assessment_id` references **Assessments**.
- **Relationships:** One-to-many with **QuestionOptions**.

---

### **16. QuestionOptions**

**Purpose:** Stores options for questions that require them.

**Fields:**

- `option_id` (UUID, PK): Unique identifier.
- `question_id` (UUID, FK): References **Questions**.
- `option_text` (TEXT): The option text.
- `is_correct` (BOOLEAN): Indicates if the option is correct.

**Notes:**

- **Foreign Key:** `question_id` references **Questions**.

---

### **17. CourseSchedule**

**Purpose:** Allows instructors to set specific dates for lessons and assessments.

**Fields:**

- `schedule_id` (UUID, PK): Unique identifier.
- `course_instance_id` (UUID, FK): References **CourseInstances**.
- `unit_id` (UUID, FK): References **Units** (Nullable).
- `lesson_id` (UUID, FK): References **Lessons** (Nullable).
- `assessment_id` (UUID, FK): References **Assessments** (Nullable).
- `scheduled_date` (DATE): The date scheduled.

**Notes:**

- **Foreign Keys:** References **CourseInstances**, **Units**, **Lessons**, **Assessments**.
- **Constraints:** `CHECK` constraint ensures only one of `unit_id`, `lesson_id`, or `assessment_id` is non-null.

---

### **18. AssessmentAttempts**

**Purpose:** Records each attempt a student makes on an assessment.

**Fields:**

- `attempt_id` (UUID, PK): Unique identifier.
- `assessment_id` (UUID, FK): References **Assessments**.
- `course_instance_id` (UUID, FK): References **CourseInstances**.
- `user_id` (UUID, FK): References **Users** (Student).
- `attempt_date` (TIMESTAMP): Date of attempt.
- `score` (DECIMAL): Score achieved.
- `time_taken` (INT): Time in seconds.

**Notes:**

- **Foreign Keys:** References **Assessments**, **CourseInstances**, **Users**.
- **Relationships:** One-to-many with **AssessmentResponses**.

---

### **19. AssessmentResponses**

**Purpose:** Stores individual responses to assessment questions.

**Fields:**

- `response_id` (UUID, PK): Unique identifier.
- `attempt_id` (UUID, FK): References **AssessmentAttempts**.
- `question_id` (UUID, FK): References **Questions**.
- `selected_option_id` (UUID, FK): References **QuestionOptions** (Nullable).
- `answer_text` (TEXT): For free-text answers.
- `is_correct` (BOOLEAN): Indicates correctness.

**Notes:**

- **Foreign Keys:** References **AssessmentAttempts**, **Questions**, **QuestionOptions**.

---

### **20. Submissions**

**Purpose:** Records student submissions for assessments requiring uploads or essays.

**Fields:**

- `submission_id` (UUID, PK): Unique identifier.
- `assessment_id` (UUID, FK): References **Assessments**.
- `course_instance_id` (UUID, FK): References **CourseInstances**.
- `user_id` (UUID, FK): References **Users**.
- `submission_date` (TIMESTAMP): Date of submission.
- `submission_content` (TEXT): Content or file path.
- `grade_id` (UUID, FK): References **Grades** (Nullable).

**Notes:**

- **Foreign Keys:** References **Assessments**, **CourseInstances**, **Users**.
- **Grade Link:** `grade_id` linked after grading.

---

### **21. Grades**

**Purpose:** Stores grades awarded for submissions or assessment attempts.

**Fields:**

- `grade_id` (UUID, PK): Unique identifier.
- `submission_id` (UUID, FK): References **Submissions** (Nullable).
- `attempt_id` (UUID, FK): References **AssessmentAttempts** (Nullable).
- `graded_by` (UUID, FK): References **Users** (Instructor).
- `grade_value` (DECIMAL): Grade awarded.
- `feedback` (TEXT): Feedback provided.
- `grade_date` (TIMESTAMP): Date graded.

**Notes:**

- **Constraints:** Only one of `submission_id` or `attempt_id` must be non-null.
- **Foreign Keys:** References **Submissions**, **AssessmentAttempts**, **Users**.

---

### **22. Reporting Tables**

#### **22.1. FactAssessmentScores**

**Purpose:** Stores quantitative data for reporting on assessment performance.

**Fields:**

- `assessment_id` (UUID): References **Assessments**.
- `course_instance_id` (UUID): References **CourseInstances**.
- `user_id` (UUID): References **Users**.
- `attempt_id` (UUID): References **AssessmentAttempts**.
- `score` (DECIMAL): Score achieved.
- `attempt_date` (TIMESTAMP): Date of attempt.
- `time_taken` (INT): Time in seconds.
- `district_id` (UUID): References **Districts**.
- `school_id` (UUID): References **Schools**.

**Notes:**

- Populated via views or ETL processes.

---

#### **22.2. DimUser**

**Purpose:** Provides user details for reporting dimensions.

**Fields:**

- `user_id` (UUID, PK): References **Users**.
- `first_name` (VARCHAR): First name.
- `last_name` (VARCHAR): Last name.
- `role` (VARCHAR): Role of the user.
- `school_id` (UUID): References **Schools**.
- `district_id` (UUID): References **Districts**.

---

#### **22.3. DimCourse**

**Purpose:** Provides course details for reporting dimensions.

**Fields:**

- `course_instance_id` (UUID, PK): References **CourseInstances**.
- `course_template_id` (UUID): References **CourseTemplates**.
- `course_name` (VARCHAR): Name of the course.
- `instructor_id` (UUID): References **Users**.
- `school_id` (UUID): References **Schools**.
- `district_id` (UUID): References **Districts**.

---

#### **22.4. DimTime**

**Purpose:** Supports time-based reporting.

**Fields:**

- `time_id` (SERIAL, PK): Unique identifier.
- `date` (DATE): The date.
- `day_of_week` (VARCHAR): Day of the week.
- `week_of_year` (INT): Week number.
- `month` (INT): Month number.
- `quarter` (INT): Quarter number.
- `year` (INT): Year.

---

### **23. AuditLogs**

**Purpose:** Keeps track of changes and access patterns for compliance and reporting.

**Fields:**

- `audit_id` (UUID, PK): Unique identifier.
- `user_id` (UUID, FK): References **Users**.
- `action` (VARCHAR): Action performed.
- `entity_id` (UUID): ID of the entity affected.
- `entity_type` (VARCHAR): Type of the entity.
- `timestamp` (TIMESTAMP): When the action occurred.

**Notes:**

- Used for security auditing and monitoring.

---

### **24. Tags and EntityTags**

**Purpose:** Allows tagging and categorization of content for more granular reporting.

#### **24.1. Tags**

**Fields:**

- `tag_id` (UUID, PK): Unique identifier.
- `tag_name` (VARCHAR): Name of the tag.

#### **24.2. EntityTags**

**Fields:**

- `entity_tag_id` (UUID, PK): Unique identifier.
- `entity_id` (UUID): ID of the tagged entity.
- `entity_type` (VARCHAR): Type of the entity (e.g., CourseTemplate).
- `tag_id` (UUID, FK): References **Tags**.

**Notes:**

- `entity_id` and `entity_type` allow tagging of different entities.

---

## **Database Relationships**

- **Hierarchical Relationships:**
  - **Districts** → **Schools** → **Users**.
- **Course Content Structure:**
  - **CourseTemplates** → **Units** → **Lessons** → **Slides** → **SlideMedia**.
- **Assessments Structure:**
  - **Assessments** → **Questions** → **QuestionOptions**.
- **Course Assignment:**
  - **CourseTemplates** → **CourseAvailability** → **CourseInstances** → **Enrollments**.
- **User Roles:**
  - **Users** ↔ **Roles** via **UserRoles**.
- **Schedules and Attempts:**
  - **CourseInstances** ↔ **CourseSchedule**, **AssessmentAttempts**, **Submissions**, **Grades**.
- **Reporting:**
  - Reporting tables and views link various entities for analytics.

---

## **Access Control and Permissions**

- **Role-Based Access Control (RBAC):**

  - **Educators:** Create and manage course templates.
  - **District Administrators:** Manage course availability and district-wide reports.
  - **School Administrators/Instructors:** Create course instances, manage enrollments.
  - **Students:** Access assigned course content and assessments.

- **Permissions Hierarchy:**

  - Permissions are enforced at the application level based on roles assigned in the **UserRoles** table.

---

## **Data Integrity and Constraints**

- **Primary Keys:** Ensure uniqueness in each table.

- **Foreign Keys:** Establish relationships between tables.

- **Unique Constraints:**

  - `email` in **Users**.
  - `instance_code` in **CourseInstances**.
  - Combination of `course_template_id`, `district_id`, `school_id` in **CourseAvailability**.

- **Check Constraints:**

  - Positive `sequence_number` in content tables.
  - Only one of `district_id` or `school_id` in **CourseAvailability**.
  - Only one of `submission_id` or `attempt_id` in **Grades**.

- **Not Null Constraints:** Critical fields are marked as NOT NULL to prevent incomplete data.

---

## **Indexes and Performance Optimization**

- **Indexes Created On:**

  - `school_id` in **Users**.
  - `course_instance_id` in **Enrollments**.
  - `user_id` in **AssessmentAttempts**.
  - Frequently queried fields to improve read performance.

- **Composite Indexes:** Used in unique constraints and for optimizing joins.

---

## **Reporting and Analytics**

- **Views:**

  - **view_dim_user:** Populates **DimUser**.
  - **view_dim_course:** Populates **DimCourse**.
  - **view_fact_assessment_scores:** Populates **FactAssessmentScores**.

- **Data Warehouse Integration:**

  - Data can be exported or transformed for use in external analytics tools.

- **Time Dimension Table:**

  - **DimTime** supports time-based reporting and analysis.

---

## **Data Flow and Usage Scenarios**

1. **Course Creation:**

   - Educators create **CourseTemplates** with associated content.

2. **Course Availability:**

   - Courses are made available to **Districts** or **Schools** via **CourseAvailability**.

3. **Course Instance Creation:**

   - Instructors create **CourseInstances** from available templates.

4. **Scheduling:**

   - Instructors schedule content via **CourseSchedule**.

5. **Enrollment:**

   - Students are enrolled in **CourseInstances** via **Enrollments**.

6. **Course Delivery:**

   - Students access content through the hierarchical structure.

7. **Assessments:**

   - Students complete assessments; attempts are recorded in **AssessmentAttempts**.

8. **Grading:**

   - Grades are assigned and stored in **Grades**.

9. **Reporting:**

   - Data is aggregated in reporting tables for analysis.

---

## **Special Considerations**

- **Content Versioning:**

  - Updates to **CourseTemplates** do not affect existing **CourseInstances** unless explicitly updated.

- **Localization and Internationalization:**

  - Content fields can be designed to support multiple languages if needed.

- **Security and Compliance:**

  - Sensitive data is stored securely.
  - Compliance with educational data regulations is ensured.

- **Error Handling:**

  - Constraints and checks prevent invalid data entry.

- **Scalability:**

  - Designed to handle a large number of users and courses.

---

## **Appendix**

### **A. Data Types and Conventions**

- **UUIDs:** Used for primary keys to ensure global uniqueness.

- **VARCHAR vs. TEXT:**

  - **VARCHAR:** Used for fields with expected length limits.
  - **TEXT:** Used for fields with potentially large content.

- **Timestamps:**

  - **TIMESTAMP:** Includes date and time.

- **Dates:**

  - **DATE:** Includes date only.

- **Decimals:**

  - Used for fields requiring precision, such as `grade_value`.

---

### **B. Sample Queries**

1. **Retrieve all active courses available to a school:**

   ```sql
   SELECT ct.course_name, ct.course_description
   FROM course_templates ct
   JOIN course_availability ca ON ct.course_template_id = ca.course_template_id
   WHERE ca.school_id = '<school_id>' AND ca.is_available = TRUE AND ct.status = 'Active';
   ```

2. **Get the enrollment count for a course instance:**

   ```sql
   SELECT COUNT(*) AS enrollment_count
   FROM enrollments
   WHERE course_instance_id = '<course_instance_id>' AND enrollment_status = 'Active';
   ```

3. **Fetch assessment attempts by a student:**

   ```sql
   SELECT aa.attempt_date, aa.score
   FROM assessment_attempts aa
   WHERE aa.user_id = '<user_id>' AND aa.course_instance_id = '<course_instance_id>';
   ```

---

### **C. ER Diagram**

An Entity-Relationship Diagram (ERD) visually represents the database schema, showing tables, fields, and relationships. It's recommended to create an ERD using tools like:

- **Visual Paradigm**
- **Lucidchart**
- **Draw.io**

Include the ERD in your project documentation to aid in understanding the database structure.

---

## **Conclusion**

This documentation provides a detailed overview of the LMS database schema, designed to support the specific requirements of delivering pre-built courses with limited customization. By understanding the entities, relationships, and constraints, developers can effectively work with the database, ensure data integrity, and build upon the system for future enhancements.

If you have any questions or need further clarification on any part of this documentation, please feel free to reach out to the database architect or project lead.

---

# **Contact Information**

- **Database Architect:** [Name], [Email]
- **Project Lead:** [Name], [Email]

---