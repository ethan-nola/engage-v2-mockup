
**Mock data schema**

Places
- Districts
	- District title
	- Schools
		- School title
		- School address
		- School Administrators
			- {School administrator accounts are attached to a School}
		- All Instructors
			- {Instructor accounts are assigned to a School}
		- All Students
			- {Student accounts are assigned to a School}
		- All Courses
			- {All courses being taught in all classrooms in this school}
		- Classrooms
			- Classroom title
			- Instructor
				- {Instructor account assigned to this classroom}
			- All Students
				- {All students that have enrollments in Courses that occupy this classroom}
			- Couses
				- Class period
					- {1 to 8}
				- Course Title
					- {String - Instructors choice}
				- Grade level
					- {int - 6, 7, 8 or 9}
				- Course category
					- {Available categories: 'Modules', Expeditions', 'IPLs', 'Math Connections', 'Steps / iLearn'}
				- Course subject
					- {'Math' and 'Science' 'flavors'}
						- {Math can be these Course categories: 'Modules', 'Expeditions', 'IPLs', 'Steps/iLearn', 'Math Connections'}
						- {Science can be these Course categories: 'Modules', 'Expeditions'}
				- Enrolled Students
					- {All students enrolled in this course}