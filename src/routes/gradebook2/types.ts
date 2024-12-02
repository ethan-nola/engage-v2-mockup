export type GradeValue = number | string;

export interface BaseStudent {
  id: string;
  firstname: string;
  lastname: string;
  [key: string]: GradeValue;
}

export interface GridSubsectionDetail {
  name: string;
  field: string;
}

export interface GridSubsection {
  name: string;
  field: string;
  details?: GridSubsectionDetail[];
}

export interface GridSection {
  name: string;
  field: string;
  subsections?: GridSubsection[];
}

export interface GridConfiguration {
  sections: GridSection[];
  calculateSectionAverage?: (sectionFields: GradeValue[]) => GradeValue;
  calculateSubsectionAverage?: (detailFields: GradeValue[]) => GradeValue;
} 