<script lang="ts">
  import { Card, CardContent, CardHeader, CardTitle } from "$lib/components/ui/card";
  import { onMount, tick } from 'svelte';
  import 'ag-grid-enterprise';
  import { createGrid, type ColDef, type GridApi, type GridReadyEvent } from 'ag-grid-community';
  import 'ag-grid-community/styles/ag-grid.css';
  import 'ag-grid-community/styles/ag-theme-alpine.css';
  import mockData from './mock-data.json';
  import type { ICellRendererParams } from 'ag-grid-community';
  import { Button } from "$lib/components/ui/button";

  type Course = {
    id: string;
    period: number;
    title: string;
    grade_level: number;
    category: string;
    subject: string;
    classroom: string;
    instructor: string;
    enrolled_students: string[];
  };

  type Classroom = {
    id: string;
    title: string;
    instructor: string;
    courses: Course[];
    students: string[];
  };

  type Person = {
    id: string;
    firstname: string;
    lastname: string;
    email: string;
  };

  type School = {
    id: string;
    title: string;
    address: string;
    administrators: Person[];
    instructors: Person[];
    students: Person[];
    classrooms: Classroom[];
  };

  let rowData: Person[] = [];
  let isLoading = true;
  let gridApi: GridApi<Person>;
  let currentSchool: School;

  const columnDefs: ColDef<Person>[] = [
    { 
      field: 'firstname',
      headerName: 'First Name',
      cellRenderer: 'agGroupCellRenderer',
      sortable: true, 
      filter: true,
      width: 120,
      suppressMenu: true
    },
    { 
      field: 'lastname',
      headerName: 'Last Name',
      sortable: true, 
      filter: true,
      width: 120,
      suppressMenu: true,
      sort: 'asc',
      sortIndex: 0
    },
    { 
      field: 'id',
      headerName: 'Student ID',
      width: 120,
      suppressMenu: true
    },
    { 
      field: 'courses',
      headerName: 'Classes',
      valueGetter: (params) => {
        const student = params.data;
        if (!student || !currentSchool) return 0;
        
        return currentSchool.classrooms.reduce((count, classroom) => {
          return count + classroom.courses.filter(course => 
            course.enrolled_students.includes(student.id)
          ).length;
        }, 0);
      },
      width: 100,
      suppressMenu: true,
      cellRenderer: (params: ICellRendererParams<Person>) => {
        const count = params.value;
        return `<span>${count} ${count === 1 ? 'class' : 'classes'}</span>`;
      }
    },
    { 
      headerName: 'Actions',
      width: 100,
      suppressMenu: true,
      suppressSizeToFit: true,
      cellRenderer: (params: ICellRendererParams<Person>) => {
        const button = document.createElement('button');
        button.innerHTML = 'Export';
        button.className = 'px-3 py-1 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90';
        button.onclick = () => exportStudentData(params.data);
        return button;
      }
    }
  ];

  const defaultColDef: ColDef<Person> = {
    minWidth: 100,
    resizable: true,
    sortable: true,
    filter: true
  };

  const detailCellRendererParams = {
    detailGridOptions: {
      columnDefs: [
        { 
          field: 'period', 
          headerName: 'Period', 
          flex: 0.5, 
          suppressMenu: true,
          sort: 'asc',
          sortIndex: 0
        },
        { field: 'subject', headerName: 'Subject', flex: 1, suppressMenu: true },
        { field: 'title', headerName: 'Class Name', flex: 1, suppressMenu: true },
        { field: 'category', headerName: 'Category', flex: 1, suppressMenu: true },
        { field: 'grade_level', headerName: 'Grade Level', flex: 0.7, suppressMenu: true },
        { 
          field: 'classroom',
          headerName: 'Classroom',
          flex: 1,
          suppressMenu: true,
          valueGetter: (params: any) => {
            const classroom = currentSchool?.classrooms.find(c => c.id === params.data.classroom);
            return classroom?.title || params.data.classroom;
          }
        },
        { 
          field: 'instructor',
          headerName: 'Instructor',
          flex: 1,
          suppressMenu: true,
          valueGetter: (params: any) => {
            const instructor = currentSchool?.instructors.find(i => i.id === params.data.instructor);
            return instructor ? `${instructor.firstname} ${instructor.lastname}` : params.data.instructor;
          }
        }
      ],
      defaultColDef: {
        sortable: true,
        resizable: true,
        minWidth: 100
      }
    },
    getDetailRowData: (params: any) => {
      const studentCourses = currentSchool.classrooms.reduce((courses: Course[], classroom) => {
        return courses.concat(
          classroom.courses.filter(course => 
            course.enrolled_students.includes(params.data.id)
          )
        );
      }, []);
      
      params.successCallback(studentCourses);
    }
  };

  async function loadMockData() {
    await new Promise(resolve => setTimeout(resolve, 500));
    // For now, just use the first school's data
    currentSchool = mockData.schools[0];
    return currentSchool.students;
  }

  async function initializeGrid() {
    const gridDiv = document.querySelector('#myGrid');
    
    if (gridDiv && rowData.length > 0) {
      const grid = createGrid(gridDiv as HTMLElement, {
        columnDefs,
        rowData,
        defaultColDef,
        animateRows: true,
        suppressMenuHide: true,
        masterDetail: true,
        detailRowHeight: 300,
        detailCellRendererParams,
        onGridReady: (params: GridReadyEvent<Person>) => {
          gridApi = params.api;
          params.api.sizeColumnsToFit();
          params.api.applyColumnState({
            state: [{ colId: 'lastname', sort: 'asc' }]
          });
        }
      });
    }
  }

  function exportStudentData(student: Person | undefined) {
    if (!student || !currentSchool) return;
    
    const studentCourses = currentSchool.classrooms.reduce((courses: Course[], classroom) => {
      return courses.concat(
        classroom.courses.filter(course => 
          course.enrolled_students.includes(student.id)
        )
      );
    }, []);

    type ExportRow = Record<string, string | number>;
    const exportData: ExportRow[] = studentCourses.map(course => {
      const classroom = currentSchool.classrooms.find(c => c.id === course.classroom);
      const instructor = currentSchool.instructors.find(i => i.id === course.instructor);
      
      return {
        'Period': course.period,
        'Subject': course.subject,
        'Class Name': course.title,
        'Category': course.category,
        'Grade Level': course.grade_level,
        'Classroom': classroom?.title || course.classroom,
        'Instructor': instructor ? `${instructor.firstname} ${instructor.lastname}` : course.instructor
      };
    });

    const tmpGridDiv = document.createElement('div');
    tmpGridDiv.style.display = 'none';
    document.body.appendChild(tmpGridDiv);

    const currentDate = new Date().toISOString().split('T')[0];

    const tmpGrid = createGrid(tmpGridDiv, {
      columnDefs: [
        { field: 'Period', width: 100 },
        { field: 'Subject', width: 150 },
        { field: 'Class Name', width: 200 },
        { field: 'Category', width: 150 },
        { field: 'Grade Level', width: 120 },
        { field: 'Classroom', width: 150 },
        { field: 'Instructor', width: 200 }
      ],
      rowData: exportData,
      onGridReady: (params) => {
        params.api.exportDataAsExcel({
          fileName: `${student.firstname}_${student.lastname}_${student.id}_${currentDate}.xlsx`,
          sheetName: 'Class Enrollments'
        });
        
        document.body.removeChild(tmpGridDiv);
      }
    });
  }

  onMount(async () => {
    rowData = await loadMockData();
    isLoading = false;
    await tick();
    await initializeGrid();
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
        <div 
          id="myGrid" 
          class="ag-theme-alpine w-full flex-1"
        ></div>
      {/if}
    </CardContent>
  </Card>
</div>

<style>
  :global(.ag-theme-alpine) {
    --ag-header-height: 48px;
    --ag-header-foreground-color: rgb(100, 116, 139);
    --ag-header-background-color: transparent;
    --ag-row-border-color: rgb(241, 245, 249);
    --ag-border-color: transparent;
    --ag-cell-horizontal-padding: 1rem;
    --ag-borders: none;
    --ag-row-hover-color: rgb(248, 250, 252);
    
    /* Font settings */
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

  :global(.ag-theme-alpine .ag-cell) {
    padding-top: 1rem;
    padding-bottom: 1rem;
    line-height: 1.5rem;
    display: flex;
    align-items: center;
  }

  :global(.ag-theme-alpine .ag-cell-wrapper) {
    align-items: center;
  }

  :global(.ag-theme-alpine .ag-group-expanded),
  :global(.ag-theme-alpine .ag-group-contracted) {
    display: flex;
    align-items: center;
  }

  :global(.ag-theme-alpine .ag-group-value) {
    display: flex;
    align-items: center;
    height: 100%;
  }

  :global(.ag-theme-alpine .ag-cell.text-right) {
    justify-content: flex-end;
  }

  :global(.ag-theme-alpine .ag-row) {
    border-bottom-width: 1px;
  }

  :global(.ag-theme-alpine .ag-root) {
    border: none;
  }

  /* Remove default AG Grid focus outlines */
  :global(.ag-theme-alpine *:focus) {
    outline: none !important;
  }

  /* Adjust the header filter buttons */
  :global(.ag-theme-alpine .ag-header-cell-menu-button) {
    opacity: 0.7;
  }

  :global(.ag-theme-alpine .ag-header-cell-menu-button:hover) {
    opacity: 1;
  }

  :global(.ag-details-row) {
    padding: 20px;
    background: rgb(248, 250, 252);
  }

  :global(.ag-theme-alpine .ag-details-grid) {
    background-color: white;
    border: 1px solid rgb(241, 245, 249);
    border-radius: 8px;
    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  }

  :global(.ag-theme-alpine .ag-details-grid .ag-header) {
    background-color: rgb(248, 250, 252);
  }

  :global(.ag-theme-alpine .ag-row-selected) {
    background-color: rgb(243, 244, 246) !important;
  }
</style> 