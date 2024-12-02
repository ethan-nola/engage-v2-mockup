import type { ColDef } from "ag-grid-community";
import type { BaseStudent, GridConfiguration } from "./types";

export function createColumnDefs<T extends BaseStudent>(config: GridConfiguration): ColDef<T>[] {
  const baseColumns: ColDef<T>[] = [
    {
      field: "firstname",
      headerName: "First Name",
      sortable: true,
      minWidth: 120,
      pinned: 'left'
    },
    {
      field: "lastname",
      headerName: "Last Name",
      sortable: true,
      minWidth: 120,
      pinned: 'left'
    }
  ];

  const sectionColumns = config.sections.map(section => ({
    headerName: section.name,
    children: [
      {
        field: section.field,
        headerName: "Overall",
        sortable: true,
        minWidth: 90,
        valueGetter: (params: any) => {
          if (!section.subsections || !config.calculateSectionAverage) return null;
          const values = section.subsections.map(sub => 
            params.data?.[sub.field] as number
          );
          return config.calculateSectionAverage(values);
        },
        columnGroupShow: 'closed'
      },
      ...(section.subsections?.map(subsection => ({
        headerName: subsection.name,
        children: [
          {
            field: subsection.field,
            headerName: "Overall",
            sortable: true,
            minWidth: 90,
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
            field: detail.field,
            headerName: detail.name,
            sortable: true,
            minWidth: 90,
            columnGroupShow: 'open'
          })) || [])
        ],
        columnGroupShow: 'open'
      })) || [])
    ]
  }));

  return [...baseColumns, ...sectionColumns];
} 