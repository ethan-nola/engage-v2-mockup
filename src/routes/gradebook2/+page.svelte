<script lang="ts">
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
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
  import mockData from "./mock-data.json";
  import Icon from "$lib/components/Icon.svelte";
  import { cn } from "$lib/utils";

  type Unit = {
    id: number;
    title: string;
    description: string;
  };

  type UnitProgress = {
    unit_id: number;
    status: "completed" | "in_progress";
    sessions: Array<{
      day: number;
      rca_score?: number;
      post_test_score?: number;
      presentation_complete: boolean;
      enrichment_complete?: boolean;
      timestamp: string;
    }>;
    diagnostic_days: Array<{
      day: number;
      groups: Array<{
        group_number: number;
        tested_out: boolean;
        steps: Array<{
          type: string;
          score?: number;
          completed?: boolean;
          timestamp: string;
        }>;
      }>;
    }>;
  };

  type Student = {
    student_id: number;
    first_name: string;
    last_name: string;
    enrollment_date: string;
    units: UnitProgress[];
  };

  let gridApi: GridApi<Student>;
  let rowData: Student[] = [];
  let isLoading = true;

  // Helper function to get unit progress summary
  function getUnitSummary(student: Student, unitId: number): string {
    const unit = student.units.find(u => u.unit_id === unitId);
    if (!unit) return "Not Started";
    return unit.status === "completed" ? "Complete" : "In Progress";
  }

  // Helper function to get unit details
  function getUnitDetails(student: Student, unitId: number) {
    return student.units.find(u => u.unit_id === unitId);
  }

  // Helper function to get student status
  function getStudentStatus(student: Student): {
    status: 'normal' | 'attention' | 'intervention';
    label: string;
  } {
    // Check for intervention needs in diagnostic days
    const hasInterventionNeeded = student.units.some(unit =>
      unit.diagnostic_days.some(day =>
        day.groups.some(group =>
          group.steps?.length >= 4 && 
          group.steps[group.steps.length - 1].score !== 100
        )
      )
    );

    if (hasInterventionNeeded) {
      return { status: 'intervention', label: 'Needs Intervention' };
    }

    // Check for attention needs (low scores or incomplete work)
    const hasLowScores = student.units.some(unit =>
      unit.sessions.some(session =>
        (session.rca_score && session.rca_score < 70) ||
        (session.post_test_score && session.post_test_score < 70)
      )
    );

    if (hasLowScores) {
      return { status: 'attention', label: 'Needs Attention' };
    }

    return { status: 'normal', label: 'On Track' };
  }

  // Basic student info columns stay the same
  const baseColumnDefs: ColDef<Student>[] = [
    {
      field: "status",
      headerName: "Status",
      width: 120,
      cellRenderer: (params) => {
        const status = getStudentStatus(params.data);
        const container = document.createElement("div");
        container.className = "flex items-center gap-2";
        
        const dot = document.createElement("div");
        dot.className = cn(
          "w-3 h-3 rounded-full",
          status.status === 'normal' ? "bg-green-500" :
          status.status === 'attention' ? "bg-yellow-500" :
          "bg-red-500"
        );
        
        const label = document.createElement("span");
        label.className = "text-sm";
        label.textContent = status.label;
        
        container.appendChild(dot);
        container.appendChild(label);
        return container;
      },
      sortable: true,
      filter: true,
    },
    {
      field: "first_name",
      headerName: "First Name",
      cellRenderer: (params) => {
        const container = document.createElement("div");
        container.className = "flex items-center gap-4";
        
        const iconWrapper = document.createElement("div");
        iconWrapper.className = "text-star-blue";
        
        new Icon({
          target: iconWrapper,
          props: {
            name: "person",
            size: "md"
          }
        });
        
        const nameSpan = document.createElement("span");
        nameSpan.textContent = params.value;
        
        container.appendChild(iconWrapper);
        container.appendChild(nameSpan);
        
        return container;
      },
      sortable: true,
      filter: true,
      width: 120,
    },
    {
      field: "last_name",
      headerName: "Last Name",
      sortable: true,
      filter: true,
      width: 120,
      sort: "asc",
    },
    {
      field: "student_id",
      headerName: "Student ID",
      width: 120,
    },
  ];

  // Unit columns with expandable groups
  const unitColumns = mockData.units.map((unit: Unit) => ({
    headerName: unit.title,
    groupId: `unit_${unit.id}_group`,
    openByDefault: false,
    marryChildren: true,
    children: [
      {
        field: `unit_${unit.id}_status`,
        headerName: "Status",
        columnGroupShow: 'closed',
        width: 150,
        valueGetter: (params: any) => {
          const unitProgress = params.data.units.find((u: UnitProgress) => u.unit_id === unit.id);
          return unitProgress ? unitProgress.status : "Not Started";
        },
        cellRenderer: (params: any) => {
          const status = params.value;
          const container = document.createElement("div");
          container.innerHTML = `
            <span class="${status === 'completed' ? 'text-green-600' : status === 'in_progress' ? 'text-blue-600' : 'text-slate-500'}">
              ${status === 'completed' ? 'Complete' : status === 'in_progress' ? 'In Progress' : 'Not Started'}
            </span>
          `;
          return container;
        }
      },
      {
        field: `unit_${unit.id}_final`,
        headerName: "Final Score",
        columnGroupShow: 'closed',
        width: 120,
        valueGetter: (params: any) => {
          const unitProgress = params.data.units.find((u: UnitProgress) => u.unit_id === unit.id);
          if (!unitProgress) return null;
          const postTestSession = unitProgress.sessions.find(s => s.post_test_score !== undefined);
          return postTestSession?.post_test_score;
        },
        valueFormatter: (params: any) => {
          return params.value ? `${params.value.toFixed(1)}%` : '';
        }
      },
      {
        field: `unit_${unit.id}_rca`,
        headerName: "RCA Average",
        columnGroupShow: 'open',
        width: 120,
        valueGetter: (params: any) => {
          const unitProgress = params.data.units.find((u: UnitProgress) => u.unit_id === unit.id);
          if (!unitProgress) return null;
          const rcaScores = unitProgress.sessions
            .filter(s => s.rca_score !== undefined)
            .map(s => s.rca_score!);
          return rcaScores.length > 0 
            ? rcaScores.reduce((a, b) => a + b, 0) / rcaScores.length
            : null;
        },
        valueFormatter: (params: any) => {
          return params.value ? `${params.value.toFixed(1)}%` : '';
        }
      },
      {
        field: `unit_${unit.id}_diagnostic`,
        headerName: "Diagnostic Avg",
        columnGroupShow: 'open',
        width: 120,
        valueGetter: (params: any) => {
          const unitProgress = params.data.units.find((u: UnitProgress) => u.unit_id === unit.id);
          if (!unitProgress) return null;
          const scores = unitProgress.diagnostic_days.flatMap(day => 
            day.groups.flatMap(group => 
              group.steps
                .filter(step => step.type === 'diagnostic' && step.score !== undefined)
                .map(step => step.score!)
            )
          );
          return scores.length > 0 
            ? scores.reduce((a, b) => a + b, 0) / scores.length
            : null;
        },
        valueFormatter: (params: any) => {
          return params.value ? `${params.value.toFixed(1)}%` : '';
        }
      },
      {
        field: `unit_${unit.id}_diagnostic_day5`,
        headerName: "Diagnostic Day 5",
        columnGroupShow: 'open',
        width: 150,
        cellRenderer: (params: any) => {
          const unitProgress = params.data.units.find((u: UnitProgress) => u.unit_id === unit.id);
          if (!unitProgress) return null;
          
          const diagnosticDay = unitProgress.diagnostic_days.find(d => d.day === 5);
          if (!diagnosticDay) return null;

          const container = document.createElement("div");
          container.className = "flex flex-col gap-1 p-2 bg-slate-50 rounded";
          
          diagnosticDay.groups.forEach(group => {
            const groupDiv = document.createElement("div");
            groupDiv.className = cn(
              "text-sm flex items-center gap-2",
              group.tested_out ? "text-green-600" : 
              group.requires_intervention ? "text-red-600" : 
              "text-blue-600"
            );
            
            const status = group.tested_out ? "Tested Out" :
                          group.requires_intervention ? "Needs Help" :
                          "Complete";
            
            groupDiv.textContent = `Group ${group.group_number}: ${status}`;
            container.appendChild(groupDiv);
          });
          
          return container;
        }
      },
      {
        field: `unit_${unit.id}_diagnostic_day9`,
        headerName: "Diagnostic Day 9",
        columnGroupShow: 'open',
        width: 150,
        cellRenderer: (params: any) => {
          const unitProgress = params.data.units.find((u: UnitProgress) => u.unit_id === unit.id);
          if (!unitProgress) return null;
          
          const diagnosticDay = unitProgress.diagnostic_days.find(d => d.day === 9);
          if (!diagnosticDay) return null;

          const container = document.createElement("div");
          container.className = "flex flex-col gap-1 p-2 bg-slate-50 rounded diagnostic-cell";
          
          diagnosticDay.groups.forEach(group => {
            const groupDiv = document.createElement("div");
            const groupStatus = group.tested_out ? "tested-out" : 
                               group.requires_intervention ? "needs-help" : 
                               "in-progress";
            
            groupDiv.className = cn(
              "diagnostic-group",
              groupStatus
            );
            
            // Add tooltip data
            const tooltipContent = group.steps.map(step => {
              const score = step.score ? ` (${step.score}%)` : '';
              return `${step.type}${score}`;
            }).join(' → ');
            
            groupDiv.title = tooltipContent;
            
            const status = group.tested_out ? "Tested Out" :
                           group.requires_intervention ? "Needs Help" :
                           "Complete";
            
            groupDiv.textContent = `Group ${group.group_number}: ${status}`;
            container.appendChild(groupDiv);
          });
          
          return container;
        }
      }
    ]
  }));

  const columnDefs = [...baseColumnDefs, ...unitColumns];

  // Update grid options
  const gridOptions = {
    columnDefs,
    defaultColDef: {
      sortable: true,
      resizable: true,
      filter: true,
      suppressHeaderMenuButton: true,
    },
    rowData: mockData.students,
    animateRows: true,
    suppressMenuHide: true,
    groupHeaderHeight: 50,
    headerHeight: 40,
    groupDisplayType: 'multiColumn',
    suppressColumnVirtualisation: true,
    getRowStyle: (params: any) => {
      const status = getStudentStatus(params.data);
      return {
        background: status.status === 'intervention' ? 'rgba(254, 226, 226, 0.4)' :
                    status.status === 'attention' ? 'rgba(254, 243, 199, 0.4)' :
                    undefined
      };
    },
    rowHeight: 80,
  };

  onMount(async () => {
    rowData = mockData.students;
    isLoading = false;
    await tick();
    
    const gridDiv = document.querySelector("#myGrid");
    if (gridDiv) {
      gridApi = createGrid(gridDiv as HTMLElement, gridOptions);
    }
  });
</script>

<div class="h-full flex flex-col">
  <Card class="flex-1 flex flex-col">
    <CardHeader>
      <CardTitle>Gradebook</CardTitle>
    </CardHeader>
    <CardContent class="flex-1 flex flex-col">
      {#if isLoading}
        <div class="flex items-center justify-center flex-1">
          Loading gradebook data...
        </div>
      {:else}
        <div id="myGrid" class="ag-theme-alpine w-full flex-1"></div>
      {/if}
    </CardContent>
  </Card>
</div>

<style>
  :global(.ag-theme-alpine) {
    --ag-header-height: 48px;
    --ag-header-group-height: 50px;
    --ag-row-height: 60px;
    --ag-header-foreground-color: rgb(100, 116, 139);
    --ag-header-background-color: transparent;
    --ag-row-border-color: rgb(241, 245, 249);
    --ag-border-color: transparent;
    --ag-cell-horizontal-padding: 1rem;
    --ag-borders: none;
    --ag-row-hover-color: rgb(248, 250, 252);
  }

  :global(.ag-theme-alpine .ag-header-group-cell) {
    font-weight: 600;
    font-size: 0.875rem;
  }

  :global(.ag-theme-alpine .ag-header-group-cell-with-group) {
    border-bottom: 1px solid rgb(241, 245, 249);
  }

  :global(.ag-theme-alpine .diagnostic-cell) {
    background-color: rgb(248, 250, 252);
    border-radius: 0.375rem;
    padding: 0.5rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  }

  :global(.ag-theme-alpine .diagnostic-group) {
    padding: 0.5rem;
    margin: 0.25rem 0;
    border-radius: 0.25rem;
    transition: background-color 0.2s;
    cursor: help;
  }

  :global(.ag-theme-alpine .diagnostic-group:hover) {
    filter: brightness(0.95);
  }

  :global(.ag-theme-alpine .diagnostic-group.tested-out) {
    background-color: rgb(220, 252, 231);
    border-left: 3px solid rgb(34, 197, 94);
  }

  :global(.ag-theme-alpine .diagnostic-group.needs-help) {
    background-color: rgb(254, 226, 226);
    border-left: 3px solid rgb(239, 68, 68);
  }

  :global(.ag-theme-alpine .diagnostic-group.in-progress) {
    background-color: rgb(219, 234, 254);
    border-left: 3px solid rgb(59, 130, 246);
  }

  :global(.ag-theme-alpine .ag-header-group-cell) {
    background-color: rgb(248, 250, 252);
    border-bottom: 2px solid rgb(226, 232, 240);
  }

  :global(.ag-theme-alpine .ag-header-cell) {
    border-right: 1px solid rgb(241, 245, 249);
  }
</style>
