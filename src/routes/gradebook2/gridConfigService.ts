import type { ColDef } from "ag-grid-community";
import type { BaseStudent, GridConfiguration, CompletionStatus } from "./types";

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
        // TOP LEVEL - Unit Grade Column (shown when collapsed)
        field: section.field,
        headerName: "Grade",
        sortable: true,
        minWidth: 200,  // Minimum width for collapsed unit view
        valueGetter: (params: any) => {
          if (!section.subsections || !config.calculateSectionAverage) return null;
          const values = section.subsections.map(sub => ({
            grade: params.data?.[`${sub.field}_grade`]
          }));
          return config.calculateSectionAverage(values);
        },
        columnGroupShow: 'closed'
      },
      ...(section.subsections?.map(subsection => ({
        // MIDDLE LEVEL - Lesson headers
        headerName: subsection.name,
        children: [
          {
            // Lesson Grade Column (shown when lesson is collapsed)
            field: subsection.field,
            headerName: "Grade",
            sortable: true,
            // No minWidth here - will auto-size to content
            valueGetter: (params: any) => {
              if (!subsection.details || !config.calculateSubsectionAverage) return null;
              const values = subsection.details.map(detail => 
                params.data?.[detail.field] as number
              );
              return config.calculateSubsectionAverage(values);
            },
            columnGroupShow: 'closed'
          },
          ...(subsection.details?.map(detail => ({
            // BOTTOM LEVEL - Detail columns (Completion & Grade)
            field: detail.field,
            headerName: detail.name,
            sortable: true,
            // No minWidth here - will auto-size to content
            columnGroupShow: 'open',
            ...(detail.name === 'Completion' ? {
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