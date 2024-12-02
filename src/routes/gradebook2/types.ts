export type GradeValue = number | string;

export interface BaseStudent {
  id: string;
  firstname: string;
  lastname: string;
  [key: string]: GradeValue;
}

export interface GridSection {
  name: string;
  field: string;
  subsections?: {
    name: string;
    field: string;
  }[];
}

export interface GridConfiguration {
  sections: GridSection[];
  calculateSectionAverage?: (sectionFields: GradeValue[]) => GradeValue;
} 