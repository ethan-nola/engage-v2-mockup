<script lang="ts">
  import { onMount, tick } from "svelte";
  import "ag-grid-enterprise";
  import {
    createGrid,
    type ColDef,
    type GridApi,
    type GridReadyEvent,
  } from "ag-grid-community";
  import "ag-grid-community/styles/ag-grid.css";
  import "ag-grid-community/styles/ag-theme-alpine.css";

  type Person = {
    id: string;
    firstname: string;
    lastname: string;
    unit1: number;
    unit2: number;
    unit3: number;
    unit4: number;
    unit5: number;
    unit6: number;
    unit7: number;
    unit8: number;
    unit9: number;
    unit10: number;
  };

  /** @type {import('./$types').PageData} */
  export let data;
  
  let rowData: Person[] = [];
  let gridApi: GridApi<Person>;

  const columnDefs: ColDef<Person>[] = [
    { field: "firstname", headerName: "First Name", sortable: true, filter: true },
    { field: "lastname", headerName: "Last Name", sortable: true, filter: true },
    { field: "unit1", headerName: "Unit 1", sortable: true, filter: true },
    { field: "unit2", headerName: "Unit 2", sortable: true, filter: true },
    { field: "unit3", headerName: "Unit 3", sortable: true, filter: true },
    { field: "unit4", headerName: "Unit 4", sortable: true, filter: true },
    { field: "unit5", headerName: "Unit 5", sortable: true, filter: true },
    { field: "unit6", headerName: "Unit 6", sortable: true, filter: true },
    { field: "unit7", headerName: "Unit 7", sortable: true, filter: true },
    { field: "unit8", headerName: "Unit 8", sortable: true, filter: true },
    { field: "unit9", headerName: "Unit 9", sortable: true, filter: true },
    { field: "unit10", headerName: "Unit 10", sortable: true, filter: true },
  ];

  async function initializeGrid() {
    const gridDiv = document.querySelector("#myGrid");

    if (gridDiv && rowData.length > 0) {
      createGrid(gridDiv as HTMLElement, {
        columnDefs,
        rowData,
        defaultColDef: {
          sortable: true,
          resizable: true,
        },
        onGridReady: (params: GridReadyEvent<Person>) => {
          gridApi = params.api;
          params.api.sizeColumnsToFit();
        },
      });
    }
  }

  onMount(async () => {
    rowData = data.people;
    await tick();
    await initializeGrid();
  });
</script>

<div class="h-full flex flex-col">
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