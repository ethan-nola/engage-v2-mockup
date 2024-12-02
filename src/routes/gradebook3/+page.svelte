<script>
    import 'ag-grid-community/styles/ag-grid.css';
    import 'ag-grid-community/styles/ag-theme-alpine.css';
    import { Grid } from 'ag-grid-community';
    import { onMount } from 'svelte';
    
    export let data;
    
    let gridDiv;
    let grid;
    
    onMount(() => {
        const gridOptions = {
            defaultColDef: {
                sortable: true,
                filter: true,
                resizable: true,
                minWidth: 80,
                editable: true
            },
            rowData: data.rowData,
            columnDefs: data.columnDefs,
            popupParent: document.body,
            autoSizeStrategy: {
                type: 'fitCellContents',
                skipHeader: false,
                columnLimits: [
                    { colId: 'firstName' },
                    { colId: 'lastName' }
                ]
            },
            suppressColumnVirtualisation: true,
            onFirstDataRendered: (params) => {
                const nameColumns = ['firstName', 'lastName'];
                params.columnApi.autoSizeColumns(nameColumns);
            }
        };
        
        grid = new Grid(gridDiv, gridOptions);
    });
</script>

<div class="h-full w-full flex flex-col relative">
    <div class="flex-grow relative">
        <div bind:this={gridDiv} class="ag-theme-alpine h-full w-full"></div>
    </div>
</div>

<style>
    :global(.ag-theme-alpine) {
        height: 100% !important;
    }
</style>

