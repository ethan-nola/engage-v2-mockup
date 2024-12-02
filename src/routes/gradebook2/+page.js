/** @type {import('./$types').PageLoad} */
export function load() {
  // Helper function to generate random grade between 60 and 100
  const randomGrade = () => Math.floor(Math.random() * (100 - 60 + 1)) + 60;

  // Generate mock data
  const mockData = Array.from({ length: 20 }, (_, index) => ({
    id: `${index + 1}`,
    firstname: `First${index + 1}`, 
    lastname: `Last${index + 1}`,
    unit1: randomGrade(),
    unit2: randomGrade(),
    unit3: randomGrade(),
    unit4: randomGrade(),
    unit5: randomGrade(),
    unit6: randomGrade(),
    unit7: randomGrade(),
    unit8: randomGrade(),
    unit9: randomGrade(),
    unit10: randomGrade()
  }));

  return {
    people: mockData
  };
} 