# Math Modules Gradebook Interface Specification

## Overview
The Math Modules Gradebook employs a collapsible column interface pattern to display student progression through a comprehensive mathematics curriculum. This design allows instructors to view the entire class at a glance while selectively revealing detailed progression data through an expandable horizontal layout.

## Core Interface Elements

### Fixed Column
The leftmost section of the interface remains static during horizontal scrolling and expansion. This area displays student names and immediate status indicators. Each student row includes a color-coded status indicator showing if they are progressing normally (green), need attention (yellow), or require immediate intervention (red).

### Unit Columns
In their collapsed state, unit columns display summarized progress information. Each column header shows the unit name and number, with the main column area displaying an overall completion percentage and any alert indicators for each student. These columns can be expanded to reveal the day-by-day progression within the unit.

### Expanded Unit View
When a unit column expands, it reveals ten sub-columns representing each day of instruction. The expansion maintains the position of all other unit columns, simply pushing them horizontally to accommodate the new detail level. These daily columns follow two distinct presentation formats:

For Session Days (1-4, 6-7, 10):
- A simple two-part display showing the RCA score and presentation completion status
- Color-coding indicates score ranges and completion status
- Hovering reveals specific scores and timestamps

For Diagnostic Days (5 and 9):
- Initially shows a summary indicator of diagnostic group completion
- Can be expanded further to reveal four distinct diagnostic group progressions
- Each group displays test-out status or current position in the remediation sequence
- Clear visual indicators show which students have tested out versus those in remediation

## Progressive Disclosure
The interface supports three levels of detail:
1. All units collapsed - showing only overall progress
2. Single unit expanded - revealing daily progression
3. Diagnostic days expanded - showing detailed group progression

## Visual Hierarchy
Different types of days receive distinct visual treatment:
- Session days use a lighter background with standard grid alignment
- Diagnostic days feature a more prominent background color when collapsed
- Expanded diagnostic days use clear visual grouping to separate the four diagnostic groups

## Interactive Elements
The design incorporates several key interactive features:
- Column headers serve as expansion controls
- Hover states reveal additional detail without requiring expansion
- Alert indicators provide immediate access to relevant student information
- Horizontal scrolling maintains the fixed student column

## Data Visualization
Student progress should be immediately apparent through thoughtful use of color and iconography:
- Consistent color coding across all progress indicators
- Clear iconography for completion status
- Visual distinction between different types of assessments
- Prominent display of intervention requirements

## Responsive Considerations
While the interface primarily serves desktop users, the design should accommodate different screen sizes through:
- Horizontal scrolling with fixed student column
- Minimum column widths to maintain readability
- Collapsible sections to manage information density
- Clear touch targets for tablet users

The success of this interface relies on its ability to present complex progression data in an immediately understandable format while providing easy access to detailed information when needed. The design should prioritize quick identification of students needing intervention while maintaining the context of overall class progression.