interface StudentRow {
    firstName: string;
    lastName: string;
    [key: string]: string | number;
}

interface ColumnDef {
    field?: string;
    headerName: string;
    autoSize?: boolean;
    width?: number;
    pinned?: string;
    children?: ColumnDef[];
    valueGetter?: (params: any) => number;
    openByDefault?: boolean;
    columnGroupShow?: string;
    groupId?: string;
    valueFormatter?: (params: any) => string;
}

// Configuration options for mock data generation
const CONFIG = {
    // Grade generation settings
    grades: {
        min: 0,
        max: 100,
        // Optionally add some randomness to make data more realistic
        distribution: {
            excellent: { min: 90, max: 100, weight: 0.1 },  // 10% of grades
            good: { min: 75, max: 89, weight: 0.3 },        // 30% of grades
            average: { min: 60, max: 74, weight: 0.4 },     // 40% of grades
            poor: { min: 0, max: 59, weight: 0.2 }          // 20% of grades
        }
    },
    // Data size settings
    data: {
        studentCount: 80,
        unitsCount: 10,
        lessonsPerUnit: 10
    },
    // Sample names for generation
    names: {
        first: ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'James', 'Emma', 'William', 'Olivia'],
        last: ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    }
};

function generateRandomGrade(): number {
    const rand = Math.random();
    let cumulativeWeight = 0;
    
    // Use the distribution weights to generate more realistic grades
    for (const level of Object.values(CONFIG.grades.distribution)) {
        cumulativeWeight += level.weight;
        if (rand <= cumulativeWeight) {
            return Math.floor(Math.random() * (level.max - level.min + 1)) + level.min;
        }
    }
    
    // Fallback to simple random between min and max
    return Math.floor(Math.random() * (CONFIG.grades.max - CONFIG.grades.min + 1)) + CONFIG.grades.min;
}

function generateMockData() {
    const { first: firstNames, last: lastNames } = CONFIG.names;
    const rows = [];
    
    for (let i = 0; i < CONFIG.data.studentCount; i++) {
        const row = Object.create(null);
        row.firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
        row.lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
        
        // Generate grades for all units and lessons
        const totalGrades = CONFIG.data.unitsCount * CONFIG.data.lessonsPerUnit;
        for (let j = 1; j <= totalGrades; j++) {
            row[`grade${j}`] = generateRandomGrade();
        }
        
        rows.push(row);
    }
    
    return rows;
}

export function load() {
    const rowData = generateMockData();
    
    const columnDefs: ColumnDef[] = [
        { 
            field: 'firstName', 
            headerName: 'First Name',
            autoSize: true,
            pinned: 'left'
        },
        { 
            field: 'lastName', 
            headerName: 'Last Name',
            autoSize: true,
            pinned: 'left'
        },
        {
            headerName: 'Grade',
            pinned: 'left',
            valueGetter: (params) => {
                const unitAverages = [];
                // Calculate average for each unit (10 units, 10 grades each)
                for (let unit = 0; unit < 10; unit++) {
                    const startGrade = unit * 10 + 1;
                    const endGrade = startGrade + 9;
                    const grades = [];
                    
                    for (let grade = startGrade; grade <= endGrade; grade++) {
                        const value = params.data[`grade${grade}`];
                        if (value !== undefined) {
                            grades.push(value);
                        }
                    }
                    
                    if (grades.length > 0) {
                        unitAverages.push(
                            grades.reduce((sum, grade) => sum + grade, 0) / grades.length
                        );
                    }
                }
                
                // Calculate overall average from unit averages
                return unitAverages.length > 0
                    ? Math.round(unitAverages.reduce((sum, avg) => sum + avg, 0) / unitAverages.length)
                    : 0;
            },
            valueFormatter: (params) => {
                return params.value != null ? params.value + '%' : '';
            }
        }
    ];
    
    for (let unit = 0; unit < 10; unit++) {
        const startGrade = unit * 10 + 1;
        const endGrade = startGrade + 9;
        
        const children: ColumnDef[] = [];
        for (let grade = startGrade; grade <= endGrade; grade++) {
            const lessonIndex = ((grade - 1) % 10) + 1;
            const lessonLabel = (() => {
                switch(lessonIndex) {
                    case 1: return 'S1';
                    case 2: return 'S2';
                    case 3: return 'S3';
                    case 4: return 'S4';
                    case 5: return 'D1';
                    case 6: return 'S5';
                    case 7: return 'S6';
                    case 8: return 'S7';
                    case 9: return 'D2';
                    case 10: return 'E';
                    default: return '';
                }
            })();

            children.push({
                field: `grade${grade}`,
                headerName: lessonLabel,
                width: 100,
                columnGroupShow: 'open',
                valueFormatter: (params) => {
                    return params.value != null ? params.value + '%' : '';
                }
            });
        }
        
        columnDefs.push({
            headerName: `Unit ${unit + 1}`,
            groupId: `unit${unit + 1}`,
            children: [
                {
                    headerName: 'Average',
                    valueGetter: (params) => {
                        const grades = [];
                        for (let grade = startGrade; grade <= endGrade; grade++) {
                            const value = params.data[`grade${grade}`];
                            if (value !== undefined) {
                                grades.push(value);
                            }
                        }
                        return grades.length > 0 
                            ? Math.round(grades.reduce((sum, grade) => sum + grade, 0) / grades.length)
                            : 0;
                    },
                    valueFormatter: (params) => {
                        return params.value != null ? params.value + '%' : '';
                    },
                    columnGroupShow: 'closed'
                },
                ...children
            ]
        });
    }
    
    return {
        rowData,
        columnDefs
    };
}