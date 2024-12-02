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

/** @type {import('./$types').PageLoad} */
export function load() {
  /** @type {Array<import('./types').BaseStudent>} */
  const mockData = Array.from({ length: 20 }, () => {
    /** @type {import('./types').BaseStudent} */
    const person = {
      id: faker.string.uuid(),
      firstname: faker.person.firstName(),
      lastname: faker.person.lastName(),
    };
    
    // Add lesson scores
    for (let unit = 1; unit <= unitTitles.length; unit++) {
      for (let lesson = 1; lesson <= 10; lesson++) {
        /** @type {Array<'Not started' | 'In progress' | 'Complete'>} */
        const completionStatuses = ['Not started', 'In progress', 'Complete'];
        const completion = faker.helpers.arrayElement(completionStatuses);
        const grade = faker.number.int({ min: 40, max: 100 });
        
        person[`unit${unit}_lesson${lesson}_completion`] = completion;
        person[`unit${unit}_lesson${lesson}_grade`] = grade;
        person[`unit${unit}_lesson${lesson}`] = completion === 'Not started' ? 0 : grade;
      }
    }

    return person;
  });

  return {
    people: mockData,
    unitTitles
  };
} 