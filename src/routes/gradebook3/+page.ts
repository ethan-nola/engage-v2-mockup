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
}

function generateMockData() {
    const firstNames = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'James', 'Emma', 'William', 'Olivia'];
    const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
    
    const rows = [];
    
    // Generate 80 rows
    for (let i = 0; i < 80; i++) {
        // Create row as a plain object without type constraints
        const row = Object.create(null);
        row.firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
        row.lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
        
        // Add 100 grade columns
        for (let j = 1; j <= 100; j++) {
            row[`grade${j}`] = Math.floor(Math.random() * 101);
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
        }
    ];
    
    // Create grouped grade columns
    for (let unit = 0; unit < 10; unit++) {
        const startGrade = unit * 10 + 1;
        const endGrade = startGrade + 9;
        
        const children: ColumnDef[] = [];
        for (let grade = startGrade; grade <= endGrade; grade++) {
            children.push({
                field: `grade${grade}`,
                headerName: `${grade}`,
                width: 100,
                columnGroupShow: 'open'
            });
        }
        
        columnDefs.push({
            headerName: `Unit ${unit + 1}`,
            groupId: `unit${unit + 1}`,
            children: children,
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