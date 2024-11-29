
## **Engage 3.0 dB structure Overview**

The database schema is structured to support:

- **Pre-built Course Templates** created by educators.
- **Limited Customization** by instructors, focusing on course facilitation.
- **Hierarchical Structure** of Districts, Schools, and Users.
- **Robust Reporting** capabilities for insights at various levels.

---

## **Entity-Relationship Diagram (ERD)**

While a visual ERD cannot be displayed here, the following sections detail each entity, their fields, and relationships, effectively representing the ERD in textual form.

---

## **1. Districts**

**Purpose:** Represent educational districts overseeing multiple schools.

**Fields:**

- `DistrictID` (Primary Key)
- `DistrictName`
- `DistrictAddress`
- `ContactEmail`
- `PhoneNumber`
- `Status` (Active, Inactive)

**Relationships:**

- **Districts ↔ Schools:** One-to-many relationship; a district has multiple schools.

---

## **2. Schools**

**Purpose:** Represent individual schools within districts.

**Fields:**

- `SchoolID` (Primary Key)
- `DistrictID` (Foreign Key to Districts)
- `SchoolName`
- `SchoolAddress`
- `ContactEmail`
- `PhoneNumber`
- `Status` (Active, Inactive)

**Relationships:**

- **Districts ↔ Schools:** Each school belongs to a district.
- **Schools ↔ Users:** Users (students, instructors) are associated with schools.
- **Schools ↔ CourseInstances:** Course instances are tied to schools.

---

## **3. Users**

**Purpose:** Store information about all users, including students, instructors, educators, and administrators.

**Fields:**

- `UserID` (Primary Key)
- `SchoolID` (Foreign Key to Schools)
- `FirstName`
- `LastName`
- `Email` (Unique)
- `PasswordHash`
- `ProfilePicture`
- `DateOfBirth`
- `RegistrationDate`
- `Status` (Active, Inactive)

**Relationships:**

- **Users ↔ Schools:** Users are associated with schools (and indirectly with districts).
- **Users ↔ Roles:** Users can have multiple roles.
- **Users ↔ CourseInstances:** Instructors facilitate course instances.
- **Users ↔ Enrollments:** Students enroll in course instances.
- **Users ↔ CourseTemplates:** Educators create course templates.

---

## **4. Roles**

**Purpose:** Define different roles within the system (e.g., Student, Instructor, Educator, Admin).

**Fields:**

- `RoleID` (Primary Key)
- `RoleName` (e.g., Student, Instructor, Educator, Admin)

**Relationships:**

- **Users ↔ Roles:** Many-to-many relationship via `UserRoles`.

---

## **5. UserRoles**

**Purpose:** Associate users with their roles.

**Fields:**

- `UserID` (Foreign Key to Users)
- `RoleID` (Foreign Key to Roles)

**Relationships:**

- **Users ↔ Roles:** Users can have multiple roles.

---

## **6. CourseTemplates**

**Purpose:** Store pre-built courses created by educators.

**Fields:**

- `CourseTemplateID` (Primary Key)
- `CourseName`
- `CourseDescription`
- `CreatedBy` (Foreign Key to Users with Educator role)
- `CreationDate`
- `SubjectArea`
- `GradeLevel`
- `Status` (Active, Inactive)

**Relationships:**

- **Users (Educators) ↔ CourseTemplates:** Educators create course templates.
- **CourseTemplates ↔ Units:** Course templates contain units.
- **CourseTemplates ↔ CourseAvailability:** Availability to districts and schools.

---

## **7. CourseAvailability**

**Purpose:** Control availability of course templates to districts and schools.

**Fields:**

- `CourseTemplateID` (Foreign Key to CourseTemplates)
- `DistrictID` (Foreign Key to Districts, Nullable)
- `SchoolID` (Foreign Key to Schools, Nullable)
- `IsAvailable` (Boolean)
- `AvailabilityDate`

**Constraints:**

- At least one of `DistrictID` or `SchoolID` must be set.
- `SchoolID` availability overrides `DistrictID` availability for that school.

**Relationships:**

- **CourseTemplates ↔ Districts/Schools:** Manages which districts or schools can access a course template.

---

## **8. CourseInstances**

**Purpose:** Represent instances of course templates assigned to instructors and their students at specific schools.

**Fields:**

- `CourseInstanceID` (Primary Key)
- `CourseTemplateID` (Foreign Key to CourseTemplates)
- `InstructorID` (Foreign Key to Users with Instructor role)
- `SchoolID` (Foreign Key to Schools)
- `StartDate`
- `EndDate`
- `InstanceCode` (Unique code for enrollment)
- `Status` (Active, Completed, Archived)

**Relationships:**

- **CourseTemplates ↔ CourseInstances:** A course template can have multiple instances.
- **Users (Instructors) ↔ CourseInstances:** Instructors facilitate course instances.
- **Schools ↔ CourseInstances:** Instances are tied to schools.

---

## **9. Enrollments**

**Purpose:** Track student enrollment in course instances.

**Fields:**

- `EnrollmentID` (Primary Key)
- `UserID` (Foreign Key to Users with Student role)
- `CourseInstanceID` (Foreign Key to CourseInstances)
- `EnrollmentDate`
- `EnrollmentStatus` (Active, Completed, Withdrawn)

**Relationships:**

- **Users (Students) ↔ CourseInstances:** Students enroll in course instances.

---

## **10. Units**

**Purpose:** Organize course templates into units.

**Fields:**

- `UnitID` (Primary Key)
- `CourseTemplateID` (Foreign Key to CourseTemplates)
- `UnitTitle`
- `UnitDescription`
- `SequenceNumber`

**Relationships:**

- **CourseTemplates ↔ Units:** A course template contains multiple units.
- **Units ↔ Lessons:** Units contain lessons.
- **Units ↔ Assessments:** Units contain assessments.

---

## **11. Lessons**

**Purpose:** Represent lessons within units.

**Fields:**

- `LessonID` (Primary Key)
- `UnitID` (Foreign Key to Units)
- `LessonTitle`
- `LessonDescription`
- `SequenceNumber`

**Relationships:**

- **Units ↔ Lessons:** A unit contains multiple lessons.
- **Lessons ↔ Slides:** Lessons are composed of slides.

---

## **12. Slides**

**Purpose:** Store content for lessons, organized into slides.

**Fields:**

- `SlideID` (Primary Key)
- `LessonID` (Foreign Key to Lessons)
- `SequenceNumber`
- `SlideType` (Text, Image, Video, Interactive, etc.)

**Relationships:**

- **Lessons ↔ Slides:** Lessons contain multiple slides.
- **Slides ↔ SlideMedia:** Slides may have multiple media elements.

---

## **13. SlideMedia**

**Purpose:** Store media elements associated with slides.

**Fields:**

- `MediaID` (Primary Key)
- `SlideID` (Foreign Key to Slides)
- `MediaType` (Text, Image, Audio, Video, Interactive)
- `MediaContent` (URL or embedded content)
- `SequenceNumber`

**Relationships:**

- **Slides ↔ SlideMedia:** Each slide can have multiple media elements.

---

## **14. Assessments**

**Purpose:** Represent assessments within units (e.g., quizzes, assignments).

**Fields:**

- `AssessmentID` (Primary Key)
- `UnitID` (Foreign Key to Units)
- `AssessmentTitle`
- `AssessmentDescription`
- `DueDateOffset` (Duration from course instance start date)
- `MaxPoints`
- `AssessmentType` (Quiz, Assignment, etc.)

**Relationships:**

- **Units ↔ Assessments:** Units contain multiple assessments.
- **Assessments ↔ Questions:** Assessments include questions.

---

## **15. Questions**

**Purpose:** Store questions for assessments.

**Fields:**

- `QuestionID` (Primary Key)
- `AssessmentID` (Foreign Key to Assessments)
- `QuestionText`
- `QuestionType` (Multiple Choice, Drag & Drop, Free Text, Matching, etc.)
- `Points`

**Relationships:**

- **Assessments ↔ Questions:** Assessments contain multiple questions.
- **Questions ↔ QuestionOptions:** Questions may have options.

---

## **16. QuestionOptions**

**Purpose:** Store options for questions requiring them (e.g., multiple-choice).

**Fields:**

- `OptionID` (Primary Key)
- `QuestionID` (Foreign Key to Questions)
- `OptionText`
- `IsCorrect` (Boolean)

**Relationships:**

- **Questions ↔ QuestionOptions:** Questions have multiple options where applicable.

---

## **17. CourseSchedule**

**Purpose:** Allow instructors to set specific dates for lessons and assessments in course instances.

**Fields:**

- `ScheduleID` (Primary Key)
- `CourseInstanceID` (Foreign Key to CourseInstances)
- `UnitID` (Foreign Key to Units, Nullable)
- `LessonID` (Foreign Key to Lessons, Nullable)
- `AssessmentID` (Foreign Key to Assessments, Nullable)
- `ScheduledDate` (Date when the lesson or assessment is scheduled)

**Constraints:**

- At least one of `UnitID`, `LessonID`, or `AssessmentID` must be set.

**Relationships:**

- **CourseInstances ↔ CourseSchedule:** Schedules are specific to course instances.

---

## **18. AssessmentAttempts**

**Purpose:** Record each attempt a student makes on an assessment.

**Fields:**

- `AttemptID` (Primary Key)
- `AssessmentID` (Foreign Key to Assessments)
- `CourseInstanceID` (Foreign Key to CourseInstances)
- `UserID` (Foreign Key to Users with Student role)
- `AttemptDate`
- `Score`
- `TimeTaken`

**Relationships:**

- **Users (Students) ↔ Assessments:** Students attempt assessments.
- **AssessmentAttempts ↔ AssessmentResponses:** Attempts have multiple responses.

---

## **19. AssessmentResponses**

**Purpose:** Store individual responses to assessment questions.

**Fields:**

- `ResponseID` (Primary Key)
- `AttemptID` (Foreign Key to AssessmentAttempts)
- `QuestionID` (Foreign Key to Questions)
- `SelectedOptionID` (Foreign Key to QuestionOptions, Nullable)
- `AnswerText` (For free text or matching questions)
- `IsCorrect` (Boolean)

**Relationships:**

- **AssessmentAttempts ↔ Questions:** Responses link attempts to questions.

---

## **20. Submissions**

**Purpose:** Record student submissions for assessments (if assessments require file uploads or essays).

**Fields:**

- `SubmissionID` (Primary Key)
- `AssessmentID` (Foreign Key to Assessments)
- `CourseInstanceID` (Foreign Key to CourseInstances)
- `UserID` (Foreign Key to Users with Student role)
- `SubmissionDate`
- `SubmissionContent` (Files, essays, etc.)
- `GradeID` (Foreign Key to Grades, Nullable)

**Relationships:**

- **Users (Students) ↔ Assessments:** Students submit assessments.
- **Submissions ↔ Grades:** Submissions may be graded.

---

## **21. Grades**

**Purpose:** Store grades awarded for submissions or assessment attempts.

**Fields:**

- `GradeID` (Primary Key)
- `SubmissionID` (Foreign Key to Submissions, Nullable)
- `AttemptID` (Foreign Key to AssessmentAttempts, Nullable)
- `GradedBy` (Foreign Key to Users with Instructor role)
- `GradeValue`
- `Feedback`
- `GradeDate`

**Constraints:**

- Either `SubmissionID` or `AttemptID` must be set.

**Relationships:**

- **Grades ↔ Submissions/AssessmentAttempts:** Grades are linked to submissions or attempts.

---

## **22. Reporting Tables**

**Purpose:** Support robust reporting and analytics.

### **22.1. FactAssessmentScores**

**Fields:**

- `AssessmentID`
- `CourseInstanceID`
- `UserID`
- `AttemptID`
- `Score`
- `AttemptDate`
- `TimeTaken`
- `DistrictID`
- `SchoolID`

**Relationships:**

- **Aggregates data for reporting on assessment performance.**

### **22.2. DimUser**

**Fields:**

- `UserID`
- `FirstName`
- `LastName`
- `Role`
- `SchoolID`
- `DistrictID`

**Purpose:**

- **Provides user details for reporting dimensions.**

### **22.3. DimCourse**

**Fields:**

- `CourseInstanceID`
- `CourseTemplateID`
- `CourseName`
- `InstructorID`
- `SchoolID`
- `DistrictID`

**Purpose:**

- **Provides course details for reporting dimensions.**

### **22.4. DimTime**

**Fields:**

- `TimeID` (Primary Key)
- `Date`
- `DayOfWeek`
- `WeekOfYear`
- `Month`
- `Quarter`
- `Year`

**Purpose:**

- **Supports time-based reporting.**

---

## **23. Additional Tables and Considerations**

### **23.1. AuditLogs**

**Purpose:** Keep track of changes and access patterns for compliance and reporting.

**Fields:**

- `AuditID` (Primary Key)
- `UserID` (Foreign Key to Users)
- `Action` (e.g., Login, ViewLesson, SubmitAssessment)
- `EntityID` (ID of the entity affected)
- `EntityType` (CourseInstance, Lesson, Assessment, etc.)
- `Timestamp`

---

### **23.2. Tags and EntityTags**

**Purpose:** Allow tagging and categorization of content for more granular reporting.

#### **Tags**

**Fields:**

- `TagID` (Primary Key)
- `TagName`

#### **EntityTags**

**Fields:**

- `EntityTagID` (Primary Key)
- `EntityID` (ID of the tagged entity)
- `EntityType` (CourseTemplate, Lesson, Assessment)
- `TagID` (Foreign Key to Tags)

---

## **Relationships Overview**

- **Hierarchy:**
  - **Districts** contain **Schools**.
  - **Schools** have **Users** (students, instructors) and **CourseInstances**.
  - **Users** can have multiple **Roles** via **UserRoles**.
  - **Educators (Users)** create **CourseTemplates**.
  - **CourseTemplates** are made available to **Districts** and **Schools** via **CourseAvailability**.
  - **Instructors (Users)** create **CourseInstances** from **CourseTemplates** for their **Schools**.
  - **Students (Users)** enroll in **CourseInstances** via **Enrollments**.
  - **CourseTemplates** contain **Units**, which include **Lessons** and **Assessments**.
  - **Lessons** are composed of **Slides**, which may have multiple **SlideMedia** elements.
  - **Assessments** are made up of **Questions** (with optional **QuestionOptions**).
  - **Instructors** set schedules for **Lessons** and **Assessments** in **CourseInstances** via **CourseSchedule**.
  - **Students** attempt **Assessments**, recorded in **AssessmentAttempts** and **AssessmentResponses**.
  - **Grades** are assigned to **AssessmentAttempts** or **Submissions**.

---

## **Design Considerations**

### **1. Access Control and Permissions**

- **Role-Based Access Control (RBAC):**
  - **Educators:** Can create and manage course templates.
  - **District Administrators:** Manage course availability and view district-wide reports.
  - **School Administrators/Instructors:** Create course instances, manage enrollments, and facilitate courses.
  - **Students:** Access assigned course instances and content.

### **2. Limited Customization by Instructors**

- Instructors cannot modify course content but can:
  - Set schedules via **CourseSchedule**.
  - Manage enrollments in their **CourseInstances**.

### **3. Handling Dates and Scheduling**

- **DueDateOffset:** In **Assessments**, used to calculate actual due dates based on **CourseInstance** start date.
- **CourseSchedule:** Allows instructors to adjust schedules without altering content.

### **4. Content Versioning**

- **Versioning Mechanism:** Implemented in **CourseTemplates** to handle updates without affecting existing **CourseInstances** unless desired.

### **5. Data Integrity and Constraints**

- **Foreign Key Constraints:** Ensure referential integrity between tables.
- **Unique Constraints:** On fields like `Email` in **Users** and `InstanceCode` in **CourseInstances**.
- **Not Null Constraints:** On mandatory fields to prevent incomplete records.

### **6. Reporting and Analytics**

- **Reporting Tables:** Designed to facilitate efficient querying and aggregation.
- **Indexing:** On frequently queried fields like `UserID`, `CourseInstanceID`, `DistrictID`, `SchoolID`.
- **Data Warehouse Integration:** Potential for ETL processes to feed data into a data warehouse for advanced analytics.

### **7. Scalability and Performance**

- **Normalization:** Database is normalized to reduce redundancy.
- **Partitioning:** Large tables can be partitioned by date or other keys.
- **Caching Mechanisms:** Implemented where appropriate to enhance performance.

### **8. Security and Compliance**

- **Data Protection:** Secure storage of sensitive data (e.g., password hashing).
- **Privacy Regulations:** Compliance with FERPA, GDPR, or other relevant regulations.
- **Access Logs:** Monitoring and auditing user activities for security.

---

## **Usage Flow**

1. **Course Creation:**
   - Educators create **CourseTemplates**, including all units, lessons, slides, and assessments.

2. **Course Availability:**
   - Administrators set availability of **CourseTemplates** to specific **Districts** and/or **Schools** via **CourseAvailability**.

3. **Course Instance Creation:**
   - Instructors at schools create **CourseInstances** from available **CourseTemplates**.

4. **Scheduling:**
   - Instructors use **CourseSchedule** to set specific dates for lessons and assessments.

5. **Enrollment:**
   - Students enroll in **CourseInstances** via **Enrollments**.

6. **Course Delivery:**
   - Students access lessons, view slides, and engage with content as per the schedule.

7. **Assessments:**
   - Students complete assessments; attempts and responses are recorded.

8. **Grading:**
   - Instructors grade submissions or review automated grading from assessment attempts; grades are stored.

9. **Reporting:**
   - Administrators and educators access reports generated from the reporting tables to gain insights.

---

## **Future Extensions**

- **Additional Features:** The schema is designed to be extensible for future additions like discussions, messages, and notifications.
- **Integration Points:** API endpoints can be built for integration with external systems or services.
- **Localization Support:** Tables like `Translations` can be added to support multiple languages.

---

## **Summary**

The final database design provides a robust, scalable, and secure foundation for your LMS, tailored to:

- **Support Pre-built Courses:** Allowing educators to create rich content used by instructors.
- **Maintain Controlled Access:** Through districts and schools, with fine-grained availability settings.
- **Facilitate Limited Customization:** Instructors focus on facilitation, with scheduling capabilities.
- **Enable Hierarchical Management:** Districts and schools structure reflects real-world educational systems.
- **Provide Robust Reporting:** Data structures support detailed analytics at multiple organizational levels.
- **Ensure Data Integrity and Compliance:** Through careful design and adherence to best practices.

This comprehensive schema addresses your specific requirements and is flexible enough to accommodate future needs.