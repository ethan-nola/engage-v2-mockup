export type GradeValue = number | string | null;

export type CompletionStatus = 'Not started' | 'In progress' | 'Complete';

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

export interface PageData {
  people: BaseStudent[];
  unitTitles: string[];
}

export interface GridValueGetter {
  field: string;
  children?: string[]; // Array of child grade fields to average
} 