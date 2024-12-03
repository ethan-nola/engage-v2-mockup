<script>
    import { onDestroy, onMount } from 'svelte';
    import { createGrid } from 'ag-grid-community';
    import 'ag-grid-community/styles/ag-grid.css';
    import 'ag-grid-community/styles/ag-theme-balham.css';
    
    export let data;
    
    let gridDiv;
    let gridApi;
    
    onMount(() => {
        const gridOptions = {
            rowHeight: 38,
            defaultColDef: {
                sortable: true,
                resizable: true,
                minWidth: 80,
                editable: true,
                suppressSizeToFit: false
            },

            columnHoverHighlight: true,
            rowData: data.rowData,
            columnDefs: data.columnDefs,
            popupParent: document.body,
            groupDisplayType: 'columnGroupCells',

            autoSizeStrategy: {
                type: 'fitCellContents',
                skipHeader: false,
                columnLimits: [
                    { colId: 'firstName', maxWidth: 120 },
                    { colId: 'lastName', maxWidth: 120 }
                ]
            },

            suppressColumnVirtualisation: true,

            onFirstDataRendered: (params) => {
                params.api.sizeColumnsToFit();
            },

            onColumnVisible: (params) => {
                if (params.visible) {
                    params.api.sizeColumnsToFit();
                }
            }
        };
        
        gridApi = createGrid(gridDiv, gridOptions);
    });

    onDestroy(() => {
        if (gridApi) {
            gridApi.destroy();
        }
    });
</script>

<!-- Grid Container -->
<div class="h-full w-full flex flex-col relative">
    <div class="flex-grow relative">
        <!-- AG Grid container with Balham theme -->
        <div bind:this={gridDiv} class="ag-theme-balham h-full w-full"></div>
    </div>
</div>

<style>
    /* Ensure grid takes full height of container */
    :global(.ag-theme-balham) {
        height: 100% !important;
        /* Set hover colors to standard AG Grid light blue */
        --ag-row-hover-color: rgb(33, 150, 243, 0.1);  /* Light blue with 10% opacity */
        --ag-column-hover-color: rgb(33, 150, 243, 0.1);  /* Light blue with 10% opacity */
    }

    /* Center cell contents vertically */
    :global(.ag-theme-balham .ag-cell) {
        display: flex;
        align-items: center;
    }

    /* Replace the student-name-cell style with emphasized-text */
    :global(.emphasized-text) {
        font-size: 13px;
        font-weight: 500;
        color: rgba(0, 0, 0, 1);
    }

    /* Ensure the header class is applied correctly */
    :global(.ag-header-cell.emphasized-text .ag-header-cell-text) {
        font-size: 13px;
        font-weight: 500;
    }
</style>

