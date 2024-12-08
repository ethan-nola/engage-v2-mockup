import React from 'react';

const MathGradebookGrid = () => {
  // Helper function to generate realistic mock data for 20 students
  const generateMockData = () => {
    const students = [];
    for (let i = 1; i <= 20; i++) {
      students.push({
        id: i,
        name: `Student ${i}`,
        workstation: Math.ceil(i/2),
        partner: `Student ${i % 2 === 0 ? i-1 : i+1}`,
        day1: {
          moduleGuide: Math.floor(75 + Math.random() * 25),
          presentationComplete: Math.random() > 0.1
        },
        coreLearning: Array(3).fill(null).map(() => ({
          rcaScore: Math.floor(70 + Math.random() * 30),
          presentationComplete: Math.random() > 0.15,
          projectProgress: Math.random() > 0.2
        })),
        diagnostic1: Array(4).fill(null).map(() => ({
          initialScore: Math.floor(70 + Math.random() * 30),
          mastery1: Math.random() > 0.3 ? Math.floor(75 + Math.random() * 25) : null,
          mastery2: Math.random() > 0.7 ? Math.floor(80 + Math.random() * 20) : null
        })),
        advancedDays: Array(2).fill(null).map(() => ({
          score: Math.floor(75 + Math.random() * 25),
          projectProgress: Math.random() > 0.2
        })),
        diagnostic2: Array(4).fill(null).map(() => ({
          initialScore: Math.floor(75 + Math.random() * 25),
          mastery1: Math.random() > 0.3 ? Math.floor(80 + Math.random() * 20) : null,
          mastery2: Math.random() > 0.8 ? Math.floor(85 + Math.random() * 15) : null
        })),
        projectCompletion: Math.random() > 0.2 ? Math.floor(80 + Math.random() * 20) : null,
        postTest: Math.random() > 0.1 ? Math.floor(80 + Math.random() * 20) : null
      });
    }
    return students;
  };

  const students = generateMockData();

  // Helper function to determine cell background color based on score
  const getScoreColor = (score) => {
    if (score === null) return 'bg-gray-100';
    if (score >= 90) return 'bg-green-100';
    if (score >= 80) return 'bg-blue-100';
    if (score >= 70) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="w-full overflow-x-auto">
      <div className="text-xl font-bold mb-4">Math Module Gradebook - Current Module: Algebra 1</div>
      <table className="min-w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-50">
            <th className="border p-2">Student Info</th>
            <th className="border p-2">Day 1<br/>Module Guide</th>
            <th className="border p-2">Day 2<br/>Core</th>
            <th className="border p-2">Day 3<br/>Core</th>
            <th className="border p-2">Day 4<br/>Core</th>
            <th className="border p-2">Day 5<br/>Diagnostic 1</th>
            <th className="border p-2">Day 6<br/>Advanced</th>
            <th className="border p-2">Day 7<br/>Advanced</th>
            <th className="border p-2">Day 8<br/>Diagnostic 2</th>
            <th className="border p-2">Day 9<br/>Project</th>
            <th className="border p-2">Day 10<br/>Post-Test</th>
          </tr>
        </thead>
        <tbody>
          {students.map(student => (
            <tr key={student.id}>
              <td className="border p-2">
                <div className="font-medium">{student.name}</div>
                <div className="text-sm text-gray-600">
                  WS: {student.workstation} | Partner: {student.partner}
                </div>
              </td>
              <td className={`border p-2 ${getScoreColor(student.day1.moduleGuide)}`}>
                {student.day1.moduleGuide}%
                {student.day1.presentationComplete && ' ✓'}
              </td>
              {student.coreLearning.map((day, idx) => (
                <td key={idx} className={`border p-2 ${getScoreColor(day.rcaScore)}`}>
                  {day.rcaScore}%
                  {day.presentationComplete && ' ✓'}
                  {day.projectProgress && ' 📋'}
                </td>
              ))}
              <td className="border p-2">
                <div className="space-y-1">
                  {student.diagnostic1.map((group, idx) => (
                    <div key={idx} className={`text-sm ${getScoreColor(group.initialScore)}`}>
                      G{idx + 1}: {group.initialScore}%
                      {group.mastery1 && ` → ${group.mastery1}%`}
                      {group.mastery2 && ` → ${group.mastery2}%`}
                    </div>
                  ))}
                </div>
              </td>
              {student.advancedDays.map((day, idx) => (
                <td key={idx} className={`border p-2 ${getScoreColor(day.score)}`}>
                  {day.score}%
                  {day.projectProgress && ' 📋'}
                </td>
              ))}
              <td className="border p-2">
                <div className="space-y-1">
                  {student.diagnostic2.map((group, idx) => (
                    <div key={idx} className={`text-sm ${getScoreColor(group.initialScore)}`}>
                      G{idx + 1}: {group.initialScore}%
                      {group.mastery1 && ` → ${group.mastery1}%`}
                      {group.mastery2 && ` → ${group.mastery2}%`}
                    </div>
                  ))}
                </div>
              </td>
              <td className={`border p-2 ${getScoreColor(student.projectCompletion)}`}>
                {student.projectCompletion ? `${student.projectCompletion}%` : 'Not Complete'}
              </td>
              <td className={`border p-2 ${getScoreColor(student.postTest)}`}>
                {student.postTest ? `${student.postTest}%` : 'Not Taken'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MathGradebookGrid;
