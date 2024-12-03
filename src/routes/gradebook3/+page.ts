import mockData from './mock_data.json';

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
    sort?: string;  // Add missing sort property to fix linter error
}

// Add this near the top with other interfaces
type PresentationStatus = 'Not Started' | 'In Progress' | 'Completed';

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

// Add new helper interfaces
interface LessonCompletion {
    presentationComplete: boolean;
    hasAssessmentGrades: boolean;
}

// Add helper functions at the top of the file
function isLessonComplete(params: any, grade: number, lessonIndex: number): LessonCompletion {
    const presentationFields = (() => {
        switch(lessonIndex) {
            case 5:
            case 9:
                return Array.from({length: 4}, (_, i) => `grade${grade}_presentation${i + 1}`);
            default:
                return [`grade${grade}_presentation`];
        }
    })();

    // Check if all presentations are completed
    const presentationComplete = presentationFields.every(
        field => params.data[field] === 'Completed'
    );

    // Get assessment fields for this lesson
    const assessmentFields = (() => {
        switch(lessonIndex) {
            case 1: return [`grade${grade}_moduleGuide`];
            case 2:
            case 3:
            case 4:
            case 6: return [`grade${grade}_rca`];
            case 5:
            case 9: return [
                ...Array.from({length: 4}, (_, i) => [
                    `grade${grade}_diagnostic${i + 1}`,
                    `grade${grade}_mastery${i + 1}a`,
                    `grade${grade}_mastery${i + 1}b`
                ]).flat()
            ];
            case 8: return [`grade${grade}_posttest`];
            default: return [];
        }
    })();

    // Check if all assessment grades exist
    const hasAssessmentGrades = assessmentFields.every(
        field => params.data[field] !== undefined
    );

    return { presentationComplete, hasAssessmentGrades };
}

function calculateLessonGrade(params: any, grade: number, lessonIndex: number): number | undefined {
    const completion = isLessonComplete(params, grade, lessonIndex);
    
    // Only calculate grade if lesson is complete
    if (!completion.presentationComplete || !completion.hasAssessmentGrades) {
        return undefined;
    }

    // Get assessment fields for this lesson
    const fields = (() => {
        switch(lessonIndex) {
            case 1: return [`grade${grade}_moduleGuide`];
            case 2:
            case 3:
            case 4:
            case 6: return [`grade${grade}_rca`];
            case 5:
            case 9: return [
                ...Array.from({length: 4}, (_, i) => [
                    `grade${grade}_diagnostic${i + 1}`,
                    `grade${grade}_mastery${i + 1}a`,
                    `grade${grade}_mastery${i + 1}b`
                ]).flat()
            ];
            case 8: return [`grade${grade}_posttest`];
            default: return [];
        }
    })();

    const grades = fields
        .map(field => params.data[field])
        .filter(value => value !== undefined);
    
    return grades.length > 0
        ? Math.round(grades.reduce((sum, grade) => sum + grade, 0) / grades.length)
        : undefined;
}

// Main load function for the page
export function load() {
    // Use the pre-generated mock data
    const rowData = mockData.rowData;
    
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
            headerName: 'Course Grade',
            pinned: 'left',
            valueGetter: (params) => {
                const unitGrades = [];
                for (let unit = 0; unit < 10; unit++) {
                    const startGrade = unit * 10 + 1;
                    const endGrade = startGrade + 9;
                    const grades = [];
                    
                    for (let grade = startGrade; grade <= endGrade; grade++) {
                        const lessonIndex = ((grade - 1) % 10) + 1;
                        const lessonGrade = calculateLessonGrade(params, grade, lessonIndex);
                        if (lessonGrade !== undefined) {
                            grades.push(lessonGrade);
                        }
                    }
                    
                    if (grades.length > 0) {
                        unitGrades.push(
                            grades.reduce((sum, grade) => sum + grade, 0) / grades.length
                        );
                    }
                }
                
                return unitGrades.length > 0
                    ? Math.round(unitGrades.reduce((sum, avg) => sum + avg, 0) / unitGrades.length)
                    : undefined;
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
                        headerName: 'Lesson Grade',
                        valueGetter: (params: any) => {
                            return calculateLessonGrade(params, grade, lessonIndex);
                        },
                        valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                        columnGroupShow: 'closed'
                    },
                    // Detailed columns (shown when expanded)
                    ...(() => {
                        switch(lessonIndex) {
                            case 1: // Session 1
                                return [
                                    {
                                        field: `grade${grade}_moduleGuide`,
                                        headerName: 'Module Guide',
                                        valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                        columnGroupShow: 'open'
                                    },
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open'
                                    }
                                ];
                            case 2: // Session 2
                            case 3: // Session 3
                            case 4: // Session 4
                                return [
                                    {
                                        field: `grade${grade}_rca`,
                                        headerName: 'RCA',
                                        valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                        columnGroupShow: 'open'
                                    },
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open'
                                    }
                                ];
                            case 5: // Diagnostic Day 1
                            case 9: // Diagnostic Day 2
                                return [
                                    ...[1, 2, 3, 4].flatMap(diagNum => [
                                        {
                                            field: `grade${grade}_diagnostic${diagNum}`,
                                            headerName: `Diagnostic ${diagNum}`,
                                            valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                            columnGroupShow: 'open'
                                        },
                                        {
                                            field: `grade${grade}_presentation${diagNum}`,
                                            headerName: `Presentation ${diagNum}`,
                                            columnGroupShow: 'open'
                                        },
                                        {
                                            field: `grade${grade}_mastery${diagNum}a`,
                                            headerName: `Mastery ${diagNum}a`,
                                            valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                            columnGroupShow: 'open'
                                        },
                                        {
                                            field: `grade${grade}_mastery${diagNum}b`,
                                            headerName: `Mastery ${diagNum}b`,
                                            valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                            columnGroupShow: 'open'
                                        }
                                    ])
                                ];
                            case 6: // Session 5
                                return [
                                    {
                                        field: `grade${grade}_rca`,
                                        headerName: 'RCA',
                                        valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                        columnGroupShow: 'open'
                                    },
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open'
                                    }
                                ];
                            case 7: // Session 6
                                return [
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open'
                                    }
                                ];
                            case 8: // Session 7
                                return [
                                    {
                                        field: `grade${grade}_posttest`,
                                        headerName: 'Post-test',
                                        valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                        columnGroupShow: 'open'
                                    },
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open'
                                    }
                                ];
                            case 10: // Enrichments
                                return [
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open'
                                    }
                                ];
                            default:
                                return [];
                        }
                    })()
                ]
            });
        }
        
        // Add unit column with its lessons
        columnDefs.push({
            headerName: UNIT_NAMES[unit],
            groupId: `unit${unit + 1}`,
            openByDefault: false,  // Make sure unit starts collapsed
            children: [
                // Unit average grade column
                {
                    headerName: 'Unit Grade',
                    valueGetter: (params: any) => {
                        const grades = [];
                        for (let grade = startGrade; grade <= endGrade; grade++) {
                            const lessonIndex = ((grade - 1) % 10) + 1;
                            const lessonGrade = calculateLessonGrade(params, grade, lessonIndex);
                            if (lessonGrade !== undefined) {
                                grades.push(lessonGrade);
                            }
                        }
                        return grades.length > 0 
                            ? Math.round(grades.reduce((sum, grade) => sum + grade, 0) / grades.length)
                            : undefined;
                    },
                    valueFormatter: (params: any) => {
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