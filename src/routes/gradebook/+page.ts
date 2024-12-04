/**
 * Gradebook Data Loading and Configuration
 * 
 * This module handles the data structure and configuration for a complex educational gradebook
 * that displays student progress across multiple units and lessons. The gradebook is organized as:
 * - 10 Units (Forensic Math, Environmental Math, etc.)
 * - Each unit contains 9-10 lessons/sessions
 * - Different lesson types (regular sessions, diagnostic days) have different grading structures
 * 
 * The data is displayed using AG Grid with a hierarchical column structure:
 * Student Name -> Overall Grade -> Units -> Lessons -> Individual Assignments
 */

import mockData from './mock_data.json';

// At the top of the file, add overview documentation
/**
 * Represents a row of student data in the gradebook
 * @property firstName - Student's first name
 * @property lastName - Student's last name
 * @property [key: string] - Dynamic grade fields (e.g., 'grade1_presentation', 'grade1_moduleGuide')
 */
interface StudentRow {
    firstName: string;
    lastName: string;
    [key: string]: string | number;  // Allow dynamic grade fields
}


// Type definition for AG Grid column configuration
/**
 * AG Grid column configuration interface
 * Defines the structure and behavior of grid columns
 */
interface ColumnDef {
    field?: string;              // Data field to display
    headerName: string;          // Column header text
    autoSize?: boolean;          // Enable auto-sizing for column
    width?: number;              // Fixed width (if not auto-sized)
    pinned?: string;            // Pin column to 'left' or 'right'
    children?: ColumnDef[];      // Nested columns for grouping
    valueGetter?: (params: any) => number | string | undefined;  // Updated return type
    openByDefault?: boolean;     // Default expanded state
    columnGroupShow?: string;    // Show column when group is 'open' or 'closed'
    groupId?: string;           // Identifier for column group
    valueFormatter?: (params: any) => string;  // Format displayed values
    maxWidth?: number;          // Maximum width for column
    sort?: string;  // Add missing sort property to fix linter error
    cellClass?: string;          // Add missing cellClass property to fix linter error
    headerClass?: string;        // Add missing headerClass property to fix linter error
    suppressSizeToFit?: boolean; // Add this property to fix linter error
    minWidth?: number;
    wrapHeaderText?: boolean;
    autoHeaderHeight?: boolean;
    headerComponentParams?: {
        template?: string;
    };
}

/**
 * Status types for presentation completion
 */
type PresentationStatus = 'Not Started' | 'In Progress' | 'Completed';

/**
 * Names of the educational units in the curriculum
 */
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

/**
 * Tracks the completion status of a lesson's components
 * @property presentationComplete - Whether all presentations for the lesson are marked as completed
 * @property hasAssessmentGrades - Whether all required assessment grades have been entered
 */
interface LessonCompletion {
    presentationComplete: boolean;
    hasAssessmentGrades: boolean;
}

/**
 * Determines if a lesson is complete by checking both presentations and assessments
 * @param params - AG Grid row parameters containing student data
 * @param grade - The grade number being checked
 * @param lessonIndex - The index of the lesson within its unit (1-10)
 * @returns Object containing completion status for presentations and assessments
 */
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

/**
 * Calculates the overall grade for a specific lesson
 * Different lesson types have different grade calculation methods:
 * - Diagnostic days (5, 9): Average of best scores (diagnostic or mastery)
 * - Regular sessions: Average of assessment grades if presentations are complete
 * 
 * @param params - AG Grid row parameters containing student data
 * @param grade - The grade number to calculate
 * @param lessonIndex - The index of the lesson within its unit (1-10)
 * @returns The calculated grade (0-100) or undefined if incomplete
 */
function calculateLessonGrade(params: any, grade: number, lessonIndex: number): number | undefined {
    const completion = isLessonComplete(params, grade, lessonIndex);
    
    // For diagnostic days, calculate average differently
    if (lessonIndex === 5 || lessonIndex === 9) {
        const grades: number[] = [];
        
        // Check each diagnostic set
        for (let i = 1; i <= 4; i++) {
            const diagnostic = params.data[`grade${grade}_diagnostic${i}`];
            
            if (diagnostic !== undefined) {
                if (diagnostic === 100) {
                    // If diagnostic is 100%, use that as the grade for this set
                    grades.push(100);
                } else {
                    // Otherwise, look for mastery grades
                    const mastery_a = params.data[`grade${grade}_mastery${i}a`];
                    const mastery_b = params.data[`grade${grade}_mastery${i}b`];
                    
                    // Use the highest passing grade, or the diagnostic if no passing grades
                    const passing_grade = [mastery_a, mastery_b]
                        .filter(g => g !== undefined && g > 70)
                        .sort((a, b) => b - a)[0];
                        
                    grades.push(passing_grade || diagnostic);
                }
            }
        }
        
        // Return average if we have any grades
        return grades.length > 0 
            ? Math.round(grades.reduce((sum, g) => sum + g, 0) / grades.length)
            : undefined;
    }
    
    // For non-diagnostic days, use existing logic
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

/**
 * Main data loading function for the gradebook
 * Configures the column structure and loads student data
 * 
 * Column hierarchy:
 * 1. Student Name (pinned left)
 * 2. Overall Grade (pinned left)
 * 3. Units (collapsible)
 *    - Unit Grade (visible when collapsed)
 *    - Lessons (visible when expanded)
 *      - Lesson Grade (visible when collapsed)
 *      - Individual assignments (visible when expanded)
 * 
 * @returns Object containing row data and column definitions for AG Grid
 */
export function load() {
    // Use the pre-generated mock data
    const rowData = mockData.rowData;
    
    // Define the column structure
    const columnDefs: ColumnDef[] = [
        // Single name column on the left
        { 
            headerName: 'Student',
            valueGetter: (params) => {
                return `${params.data.firstName} ${params.data.lastName}`;
            },
            suppressSizeToFit: false,
            pinned: 'left',
            sort: 'asc',
            cellClass: 'emphasized-text',
            width: 220,  // Add fixed width for student names
            minWidth: 220  // Ensure it doesn't get smaller than this
        },
        // Modified grade column
        {
            headerName: 'Grade',
            pinned: 'left',
            width: 90, // Set fixed width
            suppressSizeToFit: true, // Prevent auto-sizing
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
                    : 0;
            },
            valueFormatter: (params) => {
                return params.value !== 0 ? params.value + '%' : '';
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
                width: 150,  // Set a fixed width that accommodates "Diagnostic Day 1"
                columnGroupShow: 'open',
                children: [
                    // Average grade column (shown when collapsed)
                    {
                        headerName: 'Lesson Grade',
                        width: 150,
                        valueGetter: (params: any) => {
                            return calculateLessonGrade(params, grade, lessonIndex) ?? 0;
                        },
                        valueFormatter: (params: any) => params.value !== 0 ? params.value + '%' : '',
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
                                        columnGroupShow: 'open',
                                        width: 120,
                                        suppressSizeToFit: true
                                    },
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open',
                                        width: 120,
                                        suppressSizeToFit: true
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
                                        columnGroupShow: 'open',
                                        width: 120,
                                        suppressSizeToFit: true
                                    },
                                    {
                                        field: `grade${grade}_presentation`,
                                        headerName: 'Presentation',
                                        columnGroupShow: 'open',
                                        width: 120,
                                        suppressSizeToFit: true
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
                                            columnGroupShow: 'open',
                                            width: 120,
                                            suppressSizeToFit: true
                                        },
                                        {
                                            field: `grade${grade}_presentation${diagNum}`,
                                            headerName: `Presentation ${diagNum}`,
                                            columnGroupShow: 'open',
                                            width: 120,
                                            suppressSizeToFit: true
                                        },
                                        {
                                            field: `grade${grade}_mastery${diagNum}a`,
                                            headerName: `Mastery ${diagNum}a`,
                                            valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                            columnGroupShow: 'open',
                                            width: 120,
                                            suppressSizeToFit: true
                                        },
                                        {
                                            field: `grade${grade}_mastery${diagNum}b`,
                                            headerName: `Mastery ${diagNum}b`,
                                            valueFormatter: (params: any) => params.value != null ? params.value + '%' : '',
                                            columnGroupShow: 'open',
                                            width: 120,
                                            suppressSizeToFit: true
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
            headerClass: 'emphasized-text',
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
                            : 0;
                    },
                    valueFormatter: (params: any) => {
                        return params.value !== 0 ? params.value + '%' : '';
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