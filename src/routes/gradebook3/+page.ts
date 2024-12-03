import { faker } from '@faker-js/faker';

// Type definitions for grid data structure
interface StudentRow {
    firstName: string;
    lastName: string;
    [key: string]: string | number;  // Allow dynamic grade fields
}

// Type definition for AG Grid column configuration
interface ColumnDef {
    field?: string;              // Data field to display
    headerName: string;          // Column header text
    autoSize?: boolean;          // Enable auto-sizing for column
    width?: number;              // Fixed width (if not auto-sized)
    pinned?: string;            // Pin column to 'left' or 'right'
    children?: ColumnDef[];      // Nested columns for grouping
    valueGetter?: (params: any) => number;  // Custom value calculation
    openByDefault?: boolean;     // Default expanded state
    columnGroupShow?: string;    // Show column when group is 'open' or 'closed'
    groupId?: string;           // Identifier for column group
    valueFormatter?: (params: any) => string;  // Format displayed values
    maxWidth?: number;          // Maximum width for column
}

// Configuration settings for mock data generation
const CONFIG = {
    // Grade generation settings
    grades: {
        min: 0,
        max: 100,
        // Distribution weights for more realistic grade patterns
        distribution: {
            excellent: { min: 90, max: 100, weight: 0.2 },  // 20% excellent grades
            good: { min: 75, max: 89, weight: 0.3 },        // 30% good grades
            average: { min: 60, max: 74, weight: 0.4 },     // 40% average grades
            poor: { min: 0, max: 59, weight: 0.1 }          // 10% poor grades
        }
    },
    // Mock data size configuration
    data: {
        studentCount: 80,        // Number of students to generate
        unitsCount: 10,         // Number of units
        lessonsPerUnit: 10      // Lessons per unit
    }
};

// Names for each unit
const UNIT_NAMES = [
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

// Generate a random grade based on weighted distribution
function generateRandomGrade(): number {
    const rand = Math.random();
    let cumulativeWeight = 0;
    
    // Use distribution weights for realistic grade patterns
    for (const level of Object.values(CONFIG.grades.distribution)) {
        cumulativeWeight += level.weight;
        if (rand <= cumulativeWeight) {
            return Math.floor(Math.random() * (level.max - level.min + 1)) + level.min;
        }
    }
    
    // Fallback to simple random between min and max
    return Math.floor(Math.random() * (CONFIG.grades.max - CONFIG.grades.min + 1)) + CONFIG.grades.min;
}

// Generate mock student data
function generateMockData() {
    const rows = [];
    
    // Generate data for each student
    for (let i = 0; i < CONFIG.data.studentCount; i++) {
        const row = Object.create(null);
        row.firstName = faker.person.firstName();
        row.lastName = faker.person.lastName();
        
        // Generate grades for each lesson
        const totalLessons = CONFIG.data.unitsCount * CONFIG.data.lessonsPerUnit;
        for (let j = 1; j <= totalLessons; j++) {
            row[`grade${j}_A1`] = generateRandomGrade();
            row[`grade${j}_A2`] = generateRandomGrade();
        }
        
        rows.push(row);
    }
    
    return rows;
}

// Main load function for the page
export function load() {
    const rowData = generateMockData();
    
    // Define the column structure
    const columnDefs: ColumnDef[] = [
        // Fixed columns on the left
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
            pinned: 'left',
            sort: 'asc'
        },
        // Overall grade column
        {
            headerName: 'Grade',
            pinned: 'left',
            valueGetter: (params) => {
                // Calculate overall grade as average of unit averages
                const unitAverages = [];
                for (let unit = 0; unit < 10; unit++) {
                    const startGrade = unit * 10 + 1;
                    const endGrade = startGrade + 9;
                    const grades = [];
                    
                    // Calculate average for each lesson in unit
                    for (let grade = startGrade; grade <= endGrade; grade++) {
                        const a1 = params.data[`grade${grade}_A1`];
                        const a2 = params.data[`grade${grade}_A2`];
                        if (a1 !== undefined && a2 !== undefined) {
                            grades.push((a1 + a2) / 2);
                        }
                    }
                    
                    if (grades.length > 0) {
                        unitAverages.push(
                            grades.reduce((sum, grade) => sum + grade, 0) / grades.length
                        );
                    }
                }
                
                return unitAverages.length > 0
                    ? Math.round(unitAverages.reduce((sum, avg) => sum + avg, 0) / unitAverages.length)
                    : 0;
            },
            valueFormatter: (params) => {
                return params.value != null ? params.value + '%' : '';
            }
        }
    ];
    
    // Generate unit columns
    for (let unit = 0; unit < 10; unit++) {
        const startGrade = unit * 10 + 1;
        const endGrade = startGrade + 9;
        
        // Generate lesson columns for each unit
        const children: ColumnDef[] = [];
        for (let grade = startGrade; grade <= endGrade; grade++) {
            const lessonIndex = ((grade - 1) % 10) + 1;
            
            // Get lesson label based on index
            const lessonLabel = (() => {
                switch(lessonIndex) {
                    case 1: return 'Session 1';
                    case 2: return 'Session 2';
                    case 3: return 'Session 3';
                    case 4: return 'Session 4';
                    case 5: return 'Diagnostic Day 1';
                    case 6: return 'Session 5';
                    case 7: return 'Session 6';
                    case 8: return 'Session 7';
                    case 9: return 'Diagnostic Day 2';
                    case 10: return 'Enrichments';
                    default: return '';
                }
            })();

            // Define column structure for each lesson
            children.push({
                headerName: lessonLabel,
                autoSize: true,
                columnGroupShow: 'open',
                children: [
                    // Average grade column (shown when collapsed)
                    {
                        headerName: 'Grade',
                        valueGetter: (params) => {
                            const a1 = params.data[`grade${grade}_A1`];
                            const a2 = params.data[`grade${grade}_A2`];
                            return Math.round((a1 + a2) / 2);
                        },
                        valueFormatter: (params) => {
                            return params.value != null ? params.value + '%' : '';
                        },
                        autoSize: true,
                        columnGroupShow: 'closed'
                    },
                    // Individual assessment columns (shown when expanded)
                    {
                        field: `grade${grade}_A1`,
                        headerName: 'A1',
                        autoSize: true,
                        columnGroupShow: 'open',
                        valueFormatter: (params) => {
                            return params.value != null ? params.value + '%' : '';
                        }
                    },
                    {
                        field: `grade${grade}_A2`,
                        headerName: 'A2',
                        autoSize: true,
                        columnGroupShow: 'open',
                        valueFormatter: (params) => {
                            return params.value != null ? params.value + '%' : '';
                        }
                    }
                ]
            });
        }
        
        // Add unit column with its lessons
        columnDefs.push({
            headerName: UNIT_NAMES[unit],
            groupId: `unit${unit + 1}`,
            children: [
                // Unit average grade column
                {
                    headerName: 'Unit Grade',
                    valueGetter: (params) => {
                        const grades = [];
                        for (let grade = startGrade; grade <= endGrade; grade++) {
                            const a1 = params.data[`grade${grade}_A1`];
                            const a2 = params.data[`grade${grade}_A2`];
                            if (a1 !== undefined && a2 !== undefined) {
                                grades.push((a1 + a2) / 2);
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