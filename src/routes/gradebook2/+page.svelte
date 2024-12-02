<script lang="ts">
  import { onMount, tick } from "svelte";
  import "ag-grid-enterprise";
  import { createGrid, type GridApi, type GridReadyEvent } from "ag-grid-community";
  import { createColumnDefs } from "./gridConfigService";
  import type { BaseStudent, GridConfiguration } from "./types";
  import "ag-grid-community/styles/ag-grid.css";
  import "ag-grid-community/styles/ag-theme-alpine.css";

  /** @type {import('./$types').PageData} */
  export let data;
  
  let rowData: BaseStudent[] = [];
  let gridApi: GridApi<BaseStudent>;

  // Example configuration for units/lessons structure
  const gridConfig: GridConfiguration = {
    sections: Array.from({ length: 10 }, (_, i) => ({
      name: `Unit ${i + 1}`,
      field: `unit${i + 1}`,
      subsections: Array.from({ length: 10 }, (_, j) => ({
        name: `Lesson ${j + 1}`,
        field: `unit${i + 1}_lesson${j + 1}`,
        details: [
          {
            name: "Completion",
            field: `unit${i + 1}_lesson${j + 1}_completion`
          },
          {
            name: "Grade",
            field: `unit${i + 1}_lesson${j + 1}_grade`
          }
        ]
      }))
    })),
    calculateSectionAverage: (values) => 
      Math.round(values.reduce((sum, grade) => sum + (grade as number), 0) / values.length),
    calculateSubsectionAverage: (values) => {
      const [completion, grade] = values;
      return completion === 'Not started' ? 0 : grade as number;
    }
  };

  const columnDefs = createColumnDefs(gridConfig);

  async function initializeGrid() {
    const gridDiv = document.querySelector("#myGrid");

    if (gridDiv && rowData.length > 0) {
      createGrid(gridDiv as HTMLElement, {
        columnDefs,
        rowData,
        defaultColDef: {
          sortable: true,
          resizable: true,
          suppressSizeToFit: false,
          suppressHeaderMenuButton: true
        },
        groupDisplayType: 'multiColumn',
        onGridReady: (params: GridReadyEvent<BaseStudent>) => {
          gridApi = params.api;
          params.api.autoSizeAllColumns();
        },
        autoSizeStrategy: {
          type: 'fitCellContents'
        }
      });
    }
  }

  onMount(async () => {
    rowData = data.people;
    await tick();
    await initializeGrid();
  });
</script>

<div class="h-full flex flex-col overflow-x-auto">
  <div class="ag-theme-alpine w-full flex-1" id="myGrid"></div>
</div>

<style>
  :global(.ag-theme-alpine) {
    --ag-header-height: 48px;
    --ag-row-height: 60px;
    --ag-header-foreground-color: rgb(100, 116, 139);
    --ag-header-background-color: transparent;
    --ag-row-border-color: rgb(241, 245, 249);
    --ag-border-color: transparent;
    --ag-cell-horizontal-padding: 1rem;
    --ag-borders: none;
    --ag-row-hover-color: rgb(248, 250, 252);
    --ag-font-size: 14px;
    --ag-font-family: inherit;
  }

  :global(.ag-theme-alpine .ag-header) {
    border-bottom: 1px solid rgb(241, 245, 249);
  }

  /* Top level - Unit headers */
  :global(.ag-theme-alpine .ag-header-row-column-group:first-child .ag-header-group-cell) {
    font-size: 1.125rem;
    font-weight: 700;
  }

  /* Middle level - Lesson headers */
  :global(.ag-theme-alpine .ag-header-row-column-group:nth-child(2) .ag-header-group-cell) {
    font-size: 1rem;
    font-weight: 600;
  }

  /* Bottom level - Detail headers (Completion, Grade) */
  :global(.ag-theme-alpine .ag-header-cell:not(.ag-header-group-cell)) {
    font-size: 0.875rem;
    font-weight: 500;
  }

  /* Update these styles */
  :global(.ag-theme-alpine .ag-header-cell-label) {
    height: 100%;
    padding: 0 !important;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  :global(.ag-theme-alpine .ag-header-group-cell-label) {
    height: 100%;
    padding: 0 !important;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  /* Add these new styles for the chevron alignment */
  :global(.ag-theme-alpine .ag-header-expand-icon) {
    margin-bottom: 0.5rem;
  }

  :global(.ag-theme-alpine .ag-header-cell-comp-wrapper) {
    height: 100%;
    display: flex;
    align-items: flex-end;
  }

  /* Adjust bottom padding to fine-tune the spacing */
  :global(.ag-theme-alpine .ag-header-cell-text),
  :global(.ag-theme-alpine .ag-header-group-text) {
    padding-bottom: 0.5rem;
  }
</style>