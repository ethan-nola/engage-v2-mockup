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
    marryChildren: true,
    children: [
      ...(section.subsections ? [{
        field: section.field,
        headerName: "Overall",
        sortable: true,
        minWidth: 90,
        valueGetter: (params) => {
          if (!section.subsections || !config.calculateSectionAverage) return null;
          const values = section.subsections.map(sub => 
            params.data?.[sub.field] as number
          );
          return config.calculateSectionAverage(values);
        }
      }] : []),
      ...(section.subsections?.map(subsection => ({
        field: subsection.field,
        headerName: subsection.name,
        sortable: true,
        minWidth: 90,
        columnGroupShow: 'open'
      })) || [{
        field: section.field,
        headerName: section.name,
        sortable: true,
        minWidth: 90
      }])
    ]
  }));

  return [...baseColumns, ...sectionColumns];
} 