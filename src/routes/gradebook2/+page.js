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

/** @type {(isCompleteUnit: boolean, isInProgress: boolean) => Array<{completion: CompletionStatus, grade: number | null}>} */
function generateUnitData(isCompleteUnit, isInProgress) {
  const lessonCount = 10;
  
  if (isCompleteUnit) {
    // Complete unit - all lessons done with grades
    return Array.from({ length: lessonCount }, () => ({
      completion: 'Complete',
      grade: faker.number.int({ min: 60, max: 100 })
    }));
  }
  
  if (isInProgress) {
    // In Progress unit - some lessons complete, one in progress, rest not started
    const completedLessons = faker.number.int({ min: 0, max: 8 });
    
    return Array.from({ length: lessonCount }, (_, index) => {
      if (index < completedLessons) {
        return {
          completion: 'Complete',
          grade: faker.number.int({ min: 60, max: 100 })
        };
      } else if (index === completedLessons) {
        return {
          completion: 'In progress',
          grade: null
        };
      } else {
        return {
          completion: 'Not started',
          grade: null
        };
      }
    });
  }
  
  // Not started unit - all lessons not started
  return Array.from({ length: lessonCount }, () => ({
    completion: 'Not started',
    grade: null
  }));
}

/** @type {import('./$types').PageLoad} */
export function load() {
  /** @type {Array<import('./types').BaseStudent>} */
  const mockData = Array.from({ length: 20 }, () => {
    // Randomly choose how many units this student has completed (1 to 10)
    const completedUnitCount = faker.number.int({ min: 1, max: 10 });
    
    // Randomly select which units are complete (can be in any order)
    const unitIndices = Array.from({ length: unitTitles.length }, (_, i) => i);
    const shuffledUnits = faker.helpers.shuffle([...unitIndices]);
    const completedUnitIndices = shuffledUnits.slice(0, completedUnitCount);
    
    // If they haven't completed all units, pick the next unit to be in progress
    const inProgressUnitIndex = completedUnitCount < unitTitles.length ? 
      shuffledUnits[completedUnitCount] : null;
    
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
      const isInProgress = unitIndex === inProgressUnitIndex;
      
      const lessons = generateUnitData(isCompleteUnit, isInProgress);
      
      // Add lesson data to person object
      lessons.forEach((lesson, lessonIndex) => {
        const lessonNumber = lessonIndex + 1;
        const baseField = `unit${unitNumber}_lesson${lessonNumber}`;
        
        person[`${baseField}_completion`] = lesson.completion;
        person[`${baseField}_grade`] = lesson.grade;
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