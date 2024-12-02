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
        field: `unit${i + 1}_lesson${j + 1}`
      }))
    })),
    calculateSectionAverage: (values) => 
      Math.round(values.reduce((sum, grade) => sum + (grade as number), 0) / values.length)
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

  :global(.ag-theme-alpine .ag-header-cell) {
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: none;
  }
</style>