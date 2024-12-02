import { faker } from '@faker-js/faker';

/** @type {import('./$types').PageLoad} */
export function load() {
  // Generate mock data
  const mockData = Array.from({ length: 20 }, () => {
    const person = {
      id: faker.string.uuid(),
      firstname: faker.person.firstName(),
      lastname: faker.person.lastName(),
    };
    
    // Add lesson scores
    for (let unit = 1; unit <= 10; unit++) {
      // Add individual lesson scores
      for (let lesson = 1; lesson <= 10; lesson++) {
        // Generate scores between 60-100
        person[`unit${unit}_lesson${lesson}`] = faker.number.int({ min: 60, max: 100 });
      }
    }

    return person;
  });

  return {
    people: mockData
  };
} 