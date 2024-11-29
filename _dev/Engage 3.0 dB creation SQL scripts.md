```
-- Enable UUID extension for universally unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===========================
-- 1. Districts Table
-- ===========================
CREATE TABLE districts (
    district_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district_name VARCHAR(255) NOT NULL,
    district_address VARCHAR(255),
    contact_email VARCHAR(255),
    phone_number VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'Active'
);

-- ===========================
-- 2. Schools Table
-- ===========================
CREATE TABLE schools (
    school_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district_id UUID NOT NULL,
    school_name VARCHAR(255) NOT NULL,
    school_address VARCHAR(255),
    contact_email VARCHAR(255),
    phone_number VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE
);

-- ===========================
-- 3. Users Table
-- ===========================
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    school_id UUID NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(255),
    date_of_birth DATE,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE CASCADE
);

-- ===========================
-- 4. Roles Table
-- ===========================
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- ===========================
-- 5. UserRoles Table
-- ===========================
CREATE TABLE user_roles (
    user_id UUID NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
);

-- ===========================
-- 6. CourseTemplates Table
-- ===========================
CREATE TABLE course_templates (
    course_template_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_name VARCHAR(255) NOT NULL,
    course_description TEXT,
    created_by UUID NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subject_area VARCHAR(100),
    grade_level VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL
);

-- ===========================
-- 7. CourseAvailability Table (Updated)
-- ===========================
CREATE TABLE course_availability (
    availability_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_template_id UUID NOT NULL,
    district_id UUID,
    school_id UUID,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    availability_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_template_id) REFERENCES course_templates(course_template_id) ON DELETE CASCADE,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE,
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE CASCADE,
    CHECK (
        (district_id IS NOT NULL AND school_id IS NULL) OR
        (district_id IS NULL AND school_id IS NOT NULL)
    ),
    UNIQUE (course_template_id, district_id, school_id)
);

-- ===========================
-- 8. CourseInstances Table
-- ===========================
CREATE TABLE course_instances (
    course_instance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_template_id UUID NOT NULL,
    instructor_id UUID NOT NULL,
    school_id UUID NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    instance_code VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (course_template_id) REFERENCES course_templates(course_template_id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE CASCADE
);

-- ===========================
-- 9. Enrollments Table
-- ===========================
CREATE TABLE enrollments (
    enrollment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    course_instance_id UUID NOT NULL,
    enrollment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    enrollment_status VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_instance_id) REFERENCES course_instances(course_instance_id) ON DELETE CASCADE
);

-- ===========================
-- 10. Units Table
-- ===========================
CREATE TABLE units (
    unit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_template_id UUID NOT NULL,
    unit_title VARCHAR(255) NOT NULL,
    unit_description TEXT,
    sequence_number INT NOT NULL CHECK (sequence_number > 0),
    FOREIGN KEY (course_template_id) REFERENCES course_templates(course_template_id) ON DELETE CASCADE
);

-- ===========================
-- 11. Lessons Table
-- ===========================
CREATE TABLE lessons (
    lesson_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_id UUID NOT NULL,
    lesson_title VARCHAR(255) NOT NULL,
    lesson_description TEXT,
    sequence_number INT NOT NULL CHECK (sequence_number > 0),
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE
);

-- ===========================
-- 12. Slides Table
-- ===========================
CREATE TABLE slides (
    slide_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lesson_id UUID NOT NULL,
    sequence_number INT NOT NULL CHECK (sequence_number > 0),
    slide_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE
);

-- ===========================
-- 13. SlideMedia Table
-- ===========================
CREATE TABLE slide_media (
    media_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slide_id UUID NOT NULL,
    media_type VARCHAR(50) NOT NULL,
    media_content TEXT NOT NULL,
    sequence_number INT NOT NULL CHECK (sequence_number > 0),
    FOREIGN KEY (slide_id) REFERENCES slides(slide_id) ON DELETE CASCADE
);

-- ===========================
-- 14. Assessments Table
-- ===========================
CREATE TABLE assessments (
    assessment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_id UUID NOT NULL,
    assessment_title VARCHAR(255) NOT NULL,
    assessment_description TEXT,
    due_date_offset INT, -- Number of days from course start date
    max_points DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    assessment_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE
);

-- ===========================
-- 15. Questions Table
-- ===========================
CREATE TABLE questions (
    question_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    points DECIMAL(5,2) NOT NULL DEFAULT 1.00,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE
);

-- ===========================
-- 16. QuestionOptions Table
-- ===========================
CREATE TABLE question_options (
    option_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

-- ===========================
-- 17. CourseSchedule Table
-- ===========================
CREATE TABLE course_schedule (
    schedule_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_instance_id UUID NOT NULL,
    unit_id UUID,
    lesson_id UUID,
    assessment_id UUID,
    scheduled_date DATE NOT NULL,
    FOREIGN KEY (course_instance_id) REFERENCES course_instances(course_instance_id) ON DELETE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE,
    CHECK (
        (unit_id IS NOT NULL AND lesson_id IS NULL AND assessment_id IS NULL) OR
        (unit_id IS NOT NULL AND lesson_id IS NOT NULL AND assessment_id IS NULL) OR
        (unit_id IS NOT NULL AND lesson_id IS NULL AND assessment_id IS NOT NULL)
    )
);

-- ===========================
-- 18. AssessmentAttempts Table
-- ===========================
CREATE TABLE assessment_attempts (
    attempt_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID NOT NULL,
    course_instance_id UUID NOT NULL,
    user_id UUID NOT NULL,
    attempt_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    score DECIMAL(5,2),
    time_taken INT, -- Time in seconds
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE,
    FOREIGN KEY (course_instance_id) REFERENCES course_instances(course_instance_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ===========================
-- 19. AssessmentResponses Table
-- ===========================
CREATE TABLE assessment_responses (
    response_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    attempt_id UUID NOT NULL,
    question_id UUID NOT NULL,
    selected_option_id UUID,
    answer_text TEXT,
    is_correct BOOLEAN,
    FOREIGN KEY (attempt_id) REFERENCES assessment_attempts(attempt_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (selected_option_id) REFERENCES question_options(option_id)
);

-- ===========================
-- 20. Submissions Table
-- ===========================
CREATE TABLE submissions (
    submission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID NOT NULL,
    course_instance_id UUID NOT NULL,
    user_id UUID NOT NULL,
    submission_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    submission_content TEXT, -- Could be file paths or text entries
    grade_id UUID,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE,
    FOREIGN KEY (course_instance_id) REFERENCES course_instances(course_instance_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    -- grade_id will be linked after the grade is assigned
);

-- ===========================
-- 21. Grades Table
-- ===========================
CREATE TABLE grades (
    grade_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    submission_id UUID,
    attempt_id UUID,
    graded_by UUID NOT NULL,
    grade_value DECIMAL(5,2) NOT NULL,
    feedback TEXT,
    grade_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id) ON DELETE SET NULL,
    FOREIGN KEY (attempt_id) REFERENCES assessment_attempts(attempt_id) ON DELETE SET NULL,
    FOREIGN KEY (graded_by) REFERENCES users(user_id) ON DELETE SET NULL,
    CHECK (
        (submission_id IS NOT NULL AND attempt_id IS NULL) OR
        (submission_id IS NULL AND attempt_id IS NOT NULL)
    )
);

-- Update Submissions Table to add foreign key to Grades
ALTER TABLE submissions
    ADD FOREIGN KEY (grade_id) REFERENCES grades(grade_id);

-- ===========================
-- 22. FactAssessmentScores Table (For Reporting)
-- ===========================
CREATE TABLE fact_assessment_scores (
    assessment_id UUID NOT NULL,
    course_instance_id UUID NOT NULL,
    user_id UUID NOT NULL,
    attempt_id UUID NOT NULL,
    score DECIMAL(5,2),
    attempt_date TIMESTAMP NOT NULL,
    time_taken INT,
    district_id UUID NOT NULL,
    school_id UUID NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE,
    FOREIGN KEY (course_instance_id) REFERENCES course_instances(course_instance_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (attempt_id) REFERENCES assessment_attempts(attempt_id) ON DELETE CASCADE,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE,
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE CASCADE
);

-- ===========================
-- 23. DimUser Table (For Reporting)
-- ===========================
CREATE TABLE dim_user (
    user_id UUID PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50),
    school_id UUID,
    district_id UUID,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE CASCADE,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE
);

-- ===========================
-- 24. DimCourse Table (For Reporting)
-- ===========================
CREATE TABLE dim_course (
    course_instance_id UUID PRIMARY KEY,
    course_template_id UUID,
    course_name VARCHAR(255),
    instructor_id UUID,
    school_id UUID,
    district_id UUID,
    FOREIGN KEY (course_instance_id) REFERENCES course_instances(course_instance_id) ON DELETE CASCADE,
    FOREIGN KEY (course_template_id) REFERENCES course_templates(course_template_id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE CASCADE,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE
);

-- ===========================
-- 25. DimTime Table (For Reporting)
-- ===========================
CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    day_of_week VARCHAR(15),
    week_of_year INT,
    month INT,
    quarter INT,
    year INT
);

-- ===========================
-- 26. AuditLogs Table
-- ===========================
CREATE TABLE audit_logs (
    audit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    action VARCHAR(100) NOT NULL,
    entity_id UUID,
    entity_type VARCHAR(50),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ===========================
-- 27. Tags Table
-- ===========================
CREATE TABLE tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tag_name VARCHAR(100) NOT NULL UNIQUE
);

-- ===========================
-- 28. EntityTags Table
-- ===========================
CREATE TABLE entity_tags (
    entity_tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    tag_id UUID NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
    -- entity_id and entity_type will refer to different tables, handled in application logic
);

-- ===========================
-- Indexes for Performance Optimization
-- ===========================
CREATE INDEX idx_users_school_id ON users(school_id);
CREATE INDEX idx_course_instances_school_id ON course_instances(school_id);
CREATE INDEX idx_enrollments_user_id ON enrollments(user_id);
CREATE INDEX idx_enrollments_course_instance_id ON enrollments(course_instance_id);
CREATE INDEX idx_assessment_attempts_user_id ON assessment_attempts(user_id);
CREATE INDEX idx_assessment_attempts_assessment_id ON assessment_attempts(assessment_id);

-- ===========================
-- Views for Reporting
-- ===========================

-- View to populate DimUser Table
CREATE OR REPLACE VIEW view_dim_user AS
SELECT
    u.user_id,
    u.first_name,
    u.last_name,
    r.role_name AS role,
    u.school_id,
    s.district_id
FROM
    users u
JOIN
    user_roles ur ON u.user_id = ur.user_id
JOIN
    roles r ON ur.role_id = r.role_id
JOIN
    schools s ON u.school_id = s.school_id;

-- View to populate DimCourse Table
CREATE OR REPLACE VIEW view_dim_course AS
SELECT
    ci.course_instance_id,
    ci.course_template_id,
    ct.course_name,
    ci.instructor_id,
    ci.school_id,
    s.district_id
FROM
    course_instances ci
JOIN
    course_templates ct ON ci.course_template_id = ct.course_template_id
JOIN
    schools s ON ci.school_id = s.school_id;

-- View to populate FactAssessmentScores Table
CREATE OR REPLACE VIEW view_fact_assessment_scores AS
SELECT
    aa.assessment_id,
    aa.course_instance_id,
    aa.user_id,
    aa.attempt_id,
    aa.score,
    aa.attempt_date,
    aa.time_taken,
    s.district_id,
    s.school_id
FROM
    assessment_attempts aa
JOIN
    course_instances ci ON aa.course_instance_id = ci.course_instance_id
JOIN
    schools s ON ci.school_id = s.school_id;

-- ===========================
-- Insert Default Roles
-- ===========================
INSERT INTO roles (role_name) VALUES ('Student'), ('Instructor'), ('Educator'), ('Admin'), ('District Admin');

-- ===========================
-- Additional Constraints and Checks
-- ===========================

-- Ensure that email addresses are unique across users
ALTER TABLE users
    ADD CONSTRAINT unique_email UNIQUE (email);

-- Ensure that instance codes are unique across course instances
ALTER TABLE course_instances
    ADD CONSTRAINT unique_instance_code UNIQUE (instance_code);

-- ===========================
-- End of SQL Script
-- ===========================

```