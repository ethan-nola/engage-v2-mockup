import { faker } from '@faker-js/faker';

/** @type {import('./$types').PageLoad} */
export function load() {
  const mockData = Array.from({ length: 20 }, () => {
    const person = {
      id: faker.string.uuid(),
      firstname: faker.person.firstName(),
      lastname: faker.person.lastName(),
    };
    
    // Add lesson scores
    for (let unit = 1; unit <= 10; unit++) {
      for (let lesson = 1; lesson <= 10; lesson++) {
        // Replace numeric completion with status
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
    people: mockData
  };
} 