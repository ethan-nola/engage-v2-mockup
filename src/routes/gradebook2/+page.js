// Mock data generation

import { faker } from '@faker-js/faker';

/** @type {Array<string>} */
const unitTitles = [
  "Forensic Math",
  "Environmental Math", 
  "Properties of Math",
  "Chemical Math",
  "Math Behind Your Meals",
  "Geometric Packing",
  "Factoring & Polynomials",
  "Laser Geometry",
  "Gravity of Algebra",
  "Home Makeover"
];

function generateUnitData(isCompleteUnit) {
  const lessonCount = 10;
  // If it's a complete unit, all lessons will be done
  // Otherwise, generate a random number of completed lessons (0 to 9)
  const completedLessons = isCompleteUnit ? lessonCount : faker.number.int({ min: 0, max: 9 });
  
  const lessons = [];
  for (let lesson = 1; lesson <= lessonCount; lesson++) {
    // Lessons must be completed in order
    const isLessonComplete = lesson <= completedLessons;
    // For incomplete units, the last incomplete lesson might be "in progress"
    const isInProgress = !isLessonComplete && lesson === completedLessons + 1;
    
    const status = isLessonComplete ? 'Complete' : 
                   isInProgress ? 'In progress' : 
                   'Not started';
                   
    // Only completed lessons have grades
    const grade = isLessonComplete ? faker.number.int({ min: 60, max: 100 }) : null;
    
    lessons.push({
      completion: status,
      grade: grade
    });
  }
  return lessons;
}

/** @type {import('./$types').PageLoad} */
export function load() {
  /** @type {Array<import('./types').BaseStudent>} */
  const mockData = Array.from({ length: 20 }, () => {
    // Randomly choose how many units this student has completed (1 to 10)
    const completedUnitCount = faker.number.int({ min: 1, max: 10 });
    
    // Randomly select which units are complete (can be in any order)
    const unitIndices = Array.from({ length: unitTitles.length }, (_, i) => i);
    const completedUnitIndices = faker.helpers.shuffle(unitIndices).slice(0, completedUnitCount);
    
    /** @type {import('./types').BaseStudent} */
    const person = {
      id: faker.string.uuid(),
      firstname: faker.person.firstName(),
      lastname: faker.person.lastName(),
    };
    
    // Generate data for each unit
    for (let unitIndex = 0; unitIndex < unitTitles.length; unitIndex++) {
      const unitNumber = unitIndex + 1;
      const isCompleteUnit = completedUnitIndices.includes(unitIndex);
      const lessons = generateUnitData(isCompleteUnit);
      
      // Add lesson data to person object
      lessons.forEach((lesson, lessonIndex) => {
        const lessonNumber = lessonIndex + 1;
        const baseField = `unit${unitNumber}_lesson${lessonNumber}`;
        
        person[`${baseField}_completion`] = lesson.completion;
        person[`${baseField}_grade`] = lesson.grade;
        // The lesson field itself is only populated for completed lessons
        person[`${baseField}`] = lesson.completion === 'Complete' ? lesson.grade : null;
      });
    }

    return person;
  });

  return {
    people: mockData,
    unitTitles
  };
} 