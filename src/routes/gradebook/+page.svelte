<script>
    import { onDestroy, onMount } from 'svelte';
    import { createGrid } from 'ag-grid-community';
    import 'ag-grid-community/styles/ag-grid.css';
    import 'ag-grid-community/styles/ag-theme-balham.css';
    import Icon from '$lib/components/Icon.svelte';
    
    export let data;
    
    let gridDiv;
    let gridApi;
    
    // Create a custom cell renderer for the student column
    function StudentCellRenderer(params) {
        const div = document.createElement('div');
        div.classList.add('student-cell');
        
        // Create the icon component
        const iconWrapper = document.createElement('div');
        iconWrapper.classList.add('icon-wrapper', 'text-nav-text');
        const icon = new Icon({
            target: iconWrapper,
            props: {
                name: 'person',
                size: 'sm'
            }
        });
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = params.value;
        
        div.appendChild(iconWrapper);
        div.appendChild(nameSpan);
        
        return div;
    }
    
    onMount(() => {
        const gridOptions = {
            rowHeight: 38,
            defaultColDef: {
                sortable: true,
                resizable: true,
                minWidth: 80,
                editable: true,
                wrapHeaderText: true,
                autoHeaderHeight: true
            },

            columnHoverHighlight: true,
            rowData: data.rowData,
            columnDefs: data.columnDefs,
            popupParent: document.body,
            groupDisplayType: 'columnGroupCells',

            suppressColumnVirtualisation: true,

            onFirstDataRendered: (params) => {
                // Get all lesson columns
                const lessonColumns = params.columnApi.getAllColumns().filter(col => 
                    col.getColDef().columnGroupShow === 'open'
                );
                
                // Auto-size lesson columns first
                if (lessonColumns.length > 0) {
                    params.columnApi.autoSizeColumns(
                        lessonColumns.map(col => col.getColId()),
                        { skipHeader: false }
                    );
                }
                
                // Then size remaining columns to fit
                params.api.sizeColumnsToFit();
            },

            onColumnVisible: (params) => {
                if (params.visible) {
                    const column = params.column;
                    const colDef = column.getColDef();
                    
                    // Only auto-size lesson columns
                    if (colDef.columnGroupShow === 'open') {
                        // First auto-size the newly visible column
                        params.columnApi.autoSizeColumn(column, { skipHeader: false });
                        
                        const parentGroup = column.getParent();
                        if (parentGroup) {
                            const visibleSiblings = parentGroup.getChildren()
                                .filter(col => col.isVisible());
                                
                            // Then auto-size all visible siblings
                            params.columnApi.autoSizeColumns(
                                visibleSiblings.map(col => col.getColId()),
                                { skipHeader: false }
                            );
                        }
                    }
                }
            },

            // Add the custom cell renderer to the components
            components: {
                studentCellRenderer: StudentCellRenderer
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

    /* Add styles for the student cell */
    :global(.student-cell) {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    :global(.student-cell .icon-wrapper) {
        display: flex;
        align-items: center;
    }
</style>

