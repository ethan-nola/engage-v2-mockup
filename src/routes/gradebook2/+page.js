/** @type {import('./$types').PageLoad} */
export function load() {
  // Helper function to generate random grade between 60 and 100
  const randomGrade = () => Math.floor(Math.random() * (100 - 60 + 1)) + 60;

  // Generate mock data
  const mockData = Array.from({ length: 20 }, (_, index) => {
    const person = {
      id: `${index + 1}`,
      firstname: `First${index + 1}`, 
      lastname: `Last${index + 1}`,
    };
    
    // Add lesson scores only (unit scores will be calculated)
    for (let unit = 1; unit <= 10; unit++) {
      // Add individual lesson scores
      for (let lesson = 1; lesson <= 10; lesson++) {
        person[`unit${unit}_lesson${lesson}`] = randomGrade();
      }
    }

    return person;
  });

  return {
    people: mockData
  };
} 