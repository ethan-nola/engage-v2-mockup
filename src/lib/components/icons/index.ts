// This file will export all SVG paths
import article from './svg/article_wght700gradN25fill1_48px.svg?raw';
import business_center from './svg/business_center_wght700gradN25fill1_48px.svg?raw';
import dashboard from './svg/dashboard_wght300gradN25fill1_48px.svg?raw';
import domain from './svg/domain_wght700gradN25fill1_48px.svg?raw';
import group from './svg/group_wght600gradN25fill1_48px.svg?raw';
import help from './svg/help_wght600gradN25fill1_48px.svg?raw';
import library_books from './svg/library_books_wght300gradN25fill1_48px.svg?raw';
import location_city from './svg/location_city_wght500grad200fill1_48px.svg?raw';
import person from './svg/person_wght700gradN25fill1_48px.svg?raw';
import verified_user from './svg/verified_user_wght600gradN25fill1_48px.svg?raw';
import widgets from './svg/widgets_wght700gradN25fill1_48px.svg?raw';
import work from './svg/work_wght600gradN25fill1_48px.svg?raw';
import insert_chart from './svg/insert_chart_grad200fill1_48px.svg?raw';

export const icons = {
  article,
  business_center,
  dashboard,
  domain,
  group,
  help,
  library_books,
  location_city,
  person,
  verified_user,
  widgets,
  work,
  insert_chart
} as const;

export type IconName = keyof typeof icons; 