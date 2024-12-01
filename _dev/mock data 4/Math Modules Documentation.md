
**A 'Course' is made of 10 'Units', each unit has a unique title.**

**A 'Unit' is made of child 'Days'. 'Days' can be one of 2 categories:**
- 'Session'
- 'Diagnostic Day'

**'Days' have a unique title.**

**'Session' 'Days' can have 2 child components (either or both):**
- 'Assessment'
	- Depending on the day, either 'Module Guide', 'RCA', or 'Post test'
- 'Presentation'

**'Diagnostic Day' 'Days' are made a set of 4 Diagnostic groups, each group contains (in this order):**
- A 'Diagnostic' assessment
- A lesson presentation
- A preliminary 'Mastery' assessment
- A secondary 'Mastery' assessment

**Any 'Assessment' can be of these types:**
- 'Module Guide'
- 'RCA'
- 'Diagnostic'
- 'Mastery'
- 'Post test'

---
**Course progression logic:**

**Overview:**
- 'Courses' are generally made of 10 'Units'
- Each 'Day' take one class period
- The demo unit structure below would take 10 class periods
- The demo course below would take 10x10 class periods, or 100 school days

**Progression**
- Students start with the 1st day session and take the 'Module Guide' assessment followed by a roughly 30 min slide based lesson presentation
- Other session days (like: 2, 3, 4, and 5) are similar but starting with an 'RCA' assessment
- Session day 6 just contains a presentation
- Session day 7 starts with a 'Post test' assessment followed by a presentation
- "Diagnostic Day" (days 5 and 9) progression logic:
	- Each Diagnostic day is made of 4 Diagnostic groups, each group follows this process:
		- Diagnostic group step 1: "Diagnostic" assessment.
			- If the student scores 100% on this diagnostic they skip to step 1 of the next diagnostic group (essentially: they 'test out' of this diagnostic group)
			- If they score anything less than 100% they move to the next Diagnostic group step
		- Diagnostic group step 2: lesson presentation
			- This is a standard lesson presentation focused on remediating knowledge of this groups educational concepts (think: "just in time refresher")
		- Diagnostic group step 3: "Mastery" assessment #1
			-  If the student scores 100% on this diagnostic they skip to step 1 of the next diagnostic group (essentially: they've exhibited master and can move on)
			- If they score anything less than 100% they move to the next Diagnostic group step
		- Diagnostic group step 4: "Mastery" assessment #2
			-  If the student scores 100% on this diagnostic they skip to step 1 of the next diagnostic group (essentially: they've exhibited master and can move on)
			- If they score anything less than 100% their prgression is "Locked" until the instructor intervenes


---

The demo course called **"Math Modules"** is structured like so:

**10 total 'Units', the unit titles are:**
"Forensic Math", "Environmental Math", "Properties of Math", "Chemical Math", "Math Behind Your Meals", "Geometric Packing", "Factoring & Polynomials", "Laser Geometry", "Gravity of Algebra", "Home Makeover"

**Each 'Unit' follows this structure:**
Days:
1. "Session 1"
	1. 'RCA' Assessment
	2. 'Presentation'
2. "Session 2"
	1. 'RCA' Assessment
	2. 'Presentation'
3. "Session 3"
	1. 'RCA' Assessment
	2. 'Presentation'
4. "Session 4"
	1. 'RCA' Assessment
	2. 'Presentation'
5. "Diagnostic Day 1"
	1. "Diagnostic" assessment: "Diagnostic 1"
	2. "Lesson" presentation: "Lesson 1"
	3. "Mastery" assessment: "Mastery 1a"
	4. Mastery assessment: "Mastery 1b"
	5. "Diagnostic" assessment: "Diagnostic 2"
	6. "Lesson" presentation: "Lesson 2"
	7. "Mastery" assessment: "Mastery 2a"
	8. "Mastery" assessment: "Mastery 2b"
	9. "Diagnostic" assessment: "Diagnostic 3"
	10. "Lesson" presentation: "Lesson 3"
	11. "Mastery" assessment: "Mastery 3a"
	12. "Mastery" assessment: "Mastery 3b"
	13. "Diagnostic" assessment: "Diagnostic 4"
	14. "Lesson" presentation: "Lesson 4"
	15. "Mastery" assessment: "Mastery 4a"
	16. "Mastery" assessment: "Mastery 4b"
6. "Session 5"
	1. 'RCA' Assessment
	2. 'Presentation'
7. "Session 6"
	1. 'Presentation'
8. "Session 7"
	1. 'Post test' Assessment
	2. 'Presentation'
9. "Diagnostic Day 2"
	1. "Diagnostic" assessment: "Diagnostic 1"
	2. "Lesson" presentation: "Lesson 1"
	3. "Mastery" assessment: "Mastery 1a"
	4. Mastery assessment: "Mastery 1b"
	5. "Diagnostic" assessment: "Diagnostic 2"
	6. "Lesson" presentation: "Lesson 2"
	7. "Mastery" assessment: "Mastery 2a"
	8. "Mastery" assessment: "Mastery 2b"
	9. "Diagnostic" assessment: "Diagnostic 3"
	10. "Lesson" presentation: "Lesson 3"
	11. "Mastery" assessment: "Mastery 3a"
	12. "Mastery" assessment: "Mastery 3b"
	13. "Diagnostic" assessment: "Diagnostic 4"
	14. "Lesson" presentation: "Lesson 4"
	15. "Mastery" assessment: "Mastery 4a"
	16. "Mastery" assessment: "Mastery 4b"
10. "Enrichments Session"
	1. 'Presentation'

---
1. For regular "Session" days (1-4, 6-7), are the RCA assessments and presentations focused on new content, or are they reviewing previous material? Understanding this would help explain the learning flow better.
	1. Each 'Unit' covers roughly a 'Chapter' in a traditional textbook. Each 'Day' represents new concepts and educational content building to mastery of the concepts being taught in each Unit. Regular "Session" days (1-4, 6-7) are focused on new content within the scope of concepts being taught in that Unit.
2. During Diagnostic Days (5 and 9), if a student needs to complete all steps in a diagnostic group, approximately how long should this take? This would help set expectations for teachers planning their classroom time.
	1. Diagnostic Days last roughly 90 min
3. Is there a specific relationship between the content covered in Sessions 1-4 and what's tested in Diagnostic Day 1? Similarly, is Diagnostic Day 2 related to Sessions 6-8?
	1. Yes. The diagnostic days represent assessments on learning content taught in the previous Session days.
4. For the final "Enrichments Session" (Day 10), what is the purpose of this presentation? Is it extending the unit's concepts, reviewing, or something else?
	1. "Enrichments Sessions" are essentially "Extra credit" work for students that complete the previous days' work. Sometimes, some students may need the 10th day to complete content from days 1 to 9.