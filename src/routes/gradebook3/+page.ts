interface StudentRow {
    firstName: string;
    lastName: string;
    [key: string]: string | number;  // Allow dynamic grade properties
}

interface ColumnDef {
    field: string;
    headerName: string;
    autoSize?: boolean;
    width?: number;
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
    
    // Generate column definitions
    const columnDefs: ColumnDef[] = [
        { 
            field: 'firstName', 
            headerName: 'First Name',
            autoSize: true,
            pinned: 'left'  // Freeze column to the left
        },
        { 
            field: 'lastName', 
            headerName: 'Last Name',
            autoSize: true,
            pinned: 'left'  // Freeze column to the left
        }
    ];
    
    // Add numbered grade columns
    for (let i = 1; i <= 100; i++) {
        columnDefs.push({
            field: `grade${i}`,
            headerName: `${i}`,
            width: 100
        });
    }
    
    return {
        rowData,
        columnDefs
    };
}