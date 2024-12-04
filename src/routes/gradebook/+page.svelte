<script>
    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
    import { createGrid } from 'ag-grid-community';
    import 'ag-grid-enterprise';
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
                autoHeaderHeight: true,
                suppressMenu: true
            },
            enableRangeSelection: true,
            suppressCellSelection: false,
            allowContextMenuWithControlKey: true,
            copyHeadersToClipboard: true,
            clipboardDelimiter: ',',
            processCellForClipboard: (params) => {
                if (typeof params.value === 'number') {
                    return `${params.value}%`;
                }
                if (typeof params.value === 'string' && params.value.includes(',')) {
                    return `"${params.value}"`;
                }
                return params.value;
            },
            getContextMenuItems: (params) => {
                return [
                    'copy',
                    'copyWithHeaders',
                    'separator',
                    'export',
                    'separator',
                    'autoSizeAll'
                ];
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

<div class="h-full w-full flex flex-col relative">
    <div class="flex-grow relative">
        <div bind:this={gridDiv} class="ag-theme-balham h-full w-full"></div>
    </div>
</div>

<style>
    :global(.ag-theme-balham) {
        height: 100% !important;
        --ag-row-hover-color: rgb(33, 150, 243, 0.1);
        --ag-column-hover-color: rgb(33, 150, 243, 0.1);
        --ag-range-selection-border-color: rgb(33, 150, 243);
        --ag-range-selection-border-style: solid;
        --ag-range-selection-background-color: rgba(33, 150, 243, 0.1);
        --ag-range-selection-background-color-2: rgba(33, 150, 243, 0.19);
        --ag-range-selection-background-color-3: rgba(33, 150, 243, 0.27);
        --ag-range-selection-background-color-4: rgba(33, 150, 243, 0.34);
    }

    :global(.ag-theme-balham .ag-cell) {
        display: flex;
        align-items: center;
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }

    :global(.ag-theme-balham .ag-cell-editing) {
        user-select: text;
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
    }

    :global(.emphasized-text) {
        font-size: 13px;
        font-weight: 500;
        color: rgba(0, 0, 0, 1);
    }

    :global(.ag-header-cell.emphasized-text .ag-header-cell-text) {
        font-size: 13px;
        font-weight: 500;
    }

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

