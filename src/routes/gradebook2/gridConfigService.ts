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
          // Get all lesson grade fields for this unit
          const lessonGradeFields = section.subsections?.map(sub => 
            `${sub.field}_grade`
          ) || [];
          return calculateAverageGrade(params, lessonGradeFields);
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
              // For lesson, just show the grade value
              return params.data?.[`${subsection.field}_grade`];
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