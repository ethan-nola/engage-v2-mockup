import type { ColDef } from "ag-grid-community";
import type { BaseStudent, GridConfiguration, CompletionStatus } from "./types";

function calculateAverageGrade(params: any, gradeFields: string[]): number | null {
  // Get all numeric grade values from the specified fields
  const grades = gradeFields
    .map(field => params.data?.[field])
    .filter(grade => grade !== null && typeof grade === 'number') as number[];
    
  if (grades.length === 0) return null;
  
  // Calculate average
  return Math.round(grades.reduce((sum, grade) => sum + grade, 0) / grades.length);
}

function getUnitStatus(params: any, subsections: GridSubsection[] | undefined): CompletionStatus {
  if (!subsections) return 'Not started';
  
  // Check completion status of all lessons in the unit
  const lessonStatuses = subsections.map(sub => 
    params.data?.[`${sub.field}_completion`]
  );
  
  // If any lesson is complete or in progress, the unit is in progress
  if (lessonStatuses.some(status => status === 'Complete' || status === 'In progress')) {
    return 'In progress';
  }
  
  return 'Not started';
}

export function createColumnDefs<T extends BaseStudent>(config: GridConfiguration): ColDef<T>[] {
  // Base columns (pinned to left)
  const baseColumns: ColDef<T>[] = [
    {
      field: 'firstname' as keyof T,
      headerName: "First Name",
      sortable: true,
      pinned: 'left',
      suppressSizeToFit: true
    },
    {
      field: 'lastname' as keyof T,
      headerName: "Last Name",
      sortable: true,
      pinned: 'left',
      suppressSizeToFit: true
    }
  ];

  // Unit columns configuration
  const sectionColumns = config.sections.map(section => ({
    headerName: section.name,
    children: [
      {
        // Unit Grade (collapsed)
        field: section.field,
        headerName: "Grade",
        sortable: true,
        minWidth: 200,
        valueGetter: (params: any) => {
          // Get all lesson completion statuses for this unit
          const allComplete = section.subsections?.every(sub => 
            params.data?.[`${sub.field}_completion`] === 'Complete'
          ) ?? false;

          if (!allComplete) {
            return getUnitStatus(params, section.subsections);
          }

          // If all lessons are complete, calculate the average grade
          const lessonGradeFields = section.subsections?.map(sub => 
            `${sub.field}_grade`
          ) || [];
          return calculateAverageGrade(params, lessonGradeFields);
        },
        // Add cell renderer to style status messages
        cellRenderer: (params: any) => {
          if (typeof params.value === 'string') {
            return `<span class="text-slate-500 italic">${params.value}</span>`;
          }
          return params.value;
        },
        columnGroupShow: 'closed'
      },
      ...(section.subsections?.map(subsection => ({
        headerName: subsection.name,
        children: [
          {
            // Lesson Grade (collapsed)
            field: subsection.field,
            headerName: "Grade",
            sortable: true,
            valueGetter: (params: any) => {
              const completion = params.data?.[`${subsection.field}_completion`];
              const grade = params.data?.[`${subsection.field}_grade`];
              
              // If the lesson isn't complete, show the status
              if (completion !== 'Complete') {
                return completion;
              }
              
              // Otherwise show the grade
              return grade;
            },
            // Add a cell renderer to style the status text differently from grades
            cellRenderer: (params: any) => {
              if (typeof params.value === 'string') {
                return `<span class="text-slate-500 italic">${params.value}</span>`;
              }
              return params.value;
            },
            columnGroupShow: 'closed'
          },
          ...(subsection.details?.map(detail => ({
            // Detail columns (Completion & Grade)
            field: detail.field,
            headerName: detail.name,
            sortable: true,
            columnGroupShow: 'open',
            ...(detail.name === 'Status' ? {
              cellEditor: 'agSelectCellEditor',
              cellEditorParams: {
                values: ['Not started', 'In progress', 'Complete']
              }
            } : {})
          })) || [])
        ],
        columnGroupShow: 'open'
      })) || [])
    ]
  }));

  return [...baseColumns, ...sectionColumns];
} 