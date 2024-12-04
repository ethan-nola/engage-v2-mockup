<script>
    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
    import { createGrid } from 'ag-grid-community';
    import 'ag-grid-community/styles/ag-grid.css';
    import 'ag-grid-community/styles/ag-theme-balham.css';
    import Icon from '$lib/components/Icon.svelte';
    
    export let data;
    
    let gridDiv;
    let gridApi;
    let StudentCellRenderer;
    
    onMount(() => {
        StudentCellRenderer = function(params) {
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
        };

        const gridOptions = {
            rowHeight: 42,
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
            components: {
                studentCellRenderer: StudentCellRenderer
            },
            onGridReady: (params) => {
                gridApi = params.api;
            }
        };

        gridApi = createGrid(gridDiv, gridOptions);
    });

    onDestroy(() => {
        if (browser && gridApi) {
            gridApi.destroy();
        }
    });
</script>

<!-- Grid Container -->
<div class="h-full w-full flex flex-col relative">
    <div class="flex-grow relative">
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

