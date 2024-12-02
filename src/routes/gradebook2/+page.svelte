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
    unit1_lesson1: number;
    unit1_lesson2: number;
    unit1_lesson3: number;
    unit1_lesson4: number;
    unit1_lesson5: number;
    unit1_lesson6: number;
    unit1_lesson7: number;
    unit1_lesson8: number;
    unit1_lesson9: number;
    unit1_lesson10: number;
    unit2: number;
    unit2_lesson1: number;
    unit2_lesson2: number;
    unit2_lesson3: number;
    unit2_lesson4: number;
    unit2_lesson5: number;
    unit2_lesson6: number;
    unit2_lesson7: number;
    unit2_lesson8: number;
    unit2_lesson9: number;
    unit2_lesson10: number;
    unit3: number;
    unit3_lesson1: number;
    unit3_lesson2: number;
    unit3_lesson3: number;
    unit3_lesson4: number;
    unit3_lesson5: number;
    unit3_lesson6: number;
    unit3_lesson7: number;
    unit3_lesson8: number;
    unit3_lesson9: number;
    unit3_lesson10: number;
    unit4: number;
    unit4_lesson1: number;
    unit4_lesson2: number;
    unit4_lesson3: number;
    unit4_lesson4: number;
    unit4_lesson5: number;
    unit4_lesson6: number;
    unit4_lesson7: number;
    unit4_lesson8: number;
    unit4_lesson9: number;
    unit4_lesson10: number;
    unit5: number;
    unit5_lesson1: number;
    unit5_lesson2: number;
    unit5_lesson3: number;
    unit5_lesson4: number;
    unit5_lesson5: number;
    unit5_lesson6: number;
    unit5_lesson7: number;
    unit5_lesson8: number;
    unit5_lesson9: number;
    unit5_lesson10: number;
    unit6: number;
    unit6_lesson1: number;
    unit6_lesson2: number;
    unit6_lesson3: number;
    unit6_lesson4: number;
    unit6_lesson5: number;
    unit6_lesson6: number;
    unit6_lesson7: number;
    unit6_lesson8: number;
    unit6_lesson9: number;
    unit6_lesson10: number;
    unit7: number;
    unit7_lesson1: number;
    unit7_lesson2: number;
    unit7_lesson3: number;
    unit7_lesson4: number;
    unit7_lesson5: number;
    unit7_lesson6: number;
    unit7_lesson7: number;
    unit7_lesson8: number;
    unit7_lesson9: number;
    unit7_lesson10: number;
    unit8: number;
    unit8_lesson1: number;
    unit8_lesson2: number;
    unit8_lesson3: number;
    unit8_lesson4: number;
    unit8_lesson5: number;
    unit8_lesson6: number;
    unit8_lesson7: number;
    unit8_lesson8: number;
    unit8_lesson9: number;
    unit8_lesson10: number;
    unit9: number;
    unit9_lesson1: number;
    unit9_lesson2: number;
    unit9_lesson3: number;
    unit9_lesson4: number;
    unit9_lesson5: number;
    unit9_lesson6: number;
    unit9_lesson7: number;
    unit9_lesson8: number;
    unit9_lesson9: number;
    unit9_lesson10: number;
    unit10: number;
    unit10_lesson1: number;
    unit10_lesson2: number;
    unit10_lesson3: number;
    unit10_lesson4: number;
    unit10_lesson5: number;
    unit10_lesson6: number;
    unit10_lesson7: number;
    unit10_lesson8: number;
    unit10_lesson9: number;
    unit10_lesson10: number;
  };

  /** @type {import('./$types').PageData} */
  export let data;
  
  let rowData: Person[] = [];
  let gridApi: GridApi<Person>;

  function createUnitColumn(unitNumber: number): ColDef<Person> {
    return {
      headerName: `Unit ${unitNumber}`,
      marryChildren: true,
      children: [
        {
          field: `unit${unitNumber}`,
          headerName: "Overall",
          sortable: true,
          minWidth: 90,
          valueGetter: (params) => {
            const lessonGrades = Array.from({ length: 10 }, (_, i) => 
              params.data?.[`unit${unitNumber}_lesson${i + 1}`] as number
            );
            return Math.round(lessonGrades.reduce((sum, grade) => sum + grade, 0) / lessonGrades.length);
          }
        },
        ...Array.from({ length: 10 }, (_, i) => ({
          field: `unit${unitNumber}_lesson${i + 1}`,
          headerName: `Lesson ${i + 1}`,
          sortable: true,
          minWidth: 90,
          columnGroupShow: 'open'
        }))
      ]
    };
  }

  const columnDefs: ColDef<Person>[] = [
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
    },
    ...Array.from({ length: 10 }, (_, i) => createUnitColumn(i + 1))
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
          suppressSizeToFit: false,
          suppressMenu: true
        },
        onGridReady: (params: GridReadyEvent<Person>) => {
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