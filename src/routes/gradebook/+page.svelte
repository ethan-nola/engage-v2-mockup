<script>
    import 'ag-grid-community/styles/ag-grid.css';
    import 'ag-grid-community/styles/ag-theme-balham.css';
    import { Grid } from 'ag-grid-community';
    import { onMount } from 'svelte';
    
    export let data;
    
    let gridDiv;
    let grid;
    
    onMount(() => {
        const gridOptions = {
            rowHeight: 38,
            // Default settings applied to all columns - removed filter option
            defaultColDef: {
                sortable: true,      // Keep sorting enabled
                resizable: true,     // Keep column resizing
                minWidth: 80,        // Keep minimum width
                editable: true,      // Keep cell editing
                autoSize: true       // Keep automatic column sizing
                // Removed filter: true to disable filtering
            },

            // Enable column hover highlighting
            columnHoverHighlight: true,  // This enables column highlighting on hover

            // Data configuration
            rowData: data.rowData,           // The actual grid data
            columnDefs: data.columnDefs,     // Column definitions and structure

            // Grid UI configuration
            popupParent: document.body,      // Where to render popups (filters, etc)
            groupDisplayType: 'columnGroupCells',  // How grouped columns are displayed
            columnHideDefaultValue: false,    // Default visibility state for columns

            // Auto-sizing configuration
            autoSizeStrategy: {
                type: 'fitCellContents',     // Size columns to fit their contents
                skipHeader: false,           // Include headers in size calculations
                // Specific column width constraints
                columnLimits: [
                    // Prevent name columns from getting too wide
                    { colId: 'firstName', maxWidth: 120 },
                    { colId: 'lastName', maxWidth: 120 }
                ]
            },

            // Performance configuration
            suppressColumnVirtualisation: true,  // Disable column virtualization for smoother scrolling

            // Event Handlers
            onFirstDataRendered: (params) => {
                // Auto-size all columns when grid first loads
                params.columnApi.autoSizeAllColumns();
            },

            // Handle column visibility changes (when expanding/collapsing groups)
            onColumnVisible: (params) => {
                if (params.visible) {
                    // Auto-size column when it becomes visible
                    params.columnApi.autoSizeColumn(params.column);
                }
            }
        };
        
        grid = new Grid(gridDiv, gridOptions);
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

