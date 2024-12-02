# Gradebook Component Specification

## Overview
The Gradebook component is an interactive grid system that displays student progress and assessment data across mathematical course units. The component utilizes expandable/collapsible columns to show varying levels of detail, from unit-level summaries to individual assessments, while supporting flexible unit progression through a workstation-based classroom model.

## Unit Access and Progression

### Workstation Organization
- Each unit is assigned to a specific physical workstation in the classroom
- Students rotate between workstations throughout the semester
- Multiple students can work on different units simultaneously
- Workstation assignments are clearly displayed in the UI

### Progression Rules
- Units can be completed in any order based on workstation availability
- Components within each unit must be completed sequentially
- No prerequisites between different units
- All students must complete all units by semester end

## Interactive Column Management

### Expansion Levels
1. **Unit Summary (Most Collapsed)**
   - Shows overall unit completion percentage
   - One column per unit
   - Workstation assignment
   - Quick overview of progress

2. **Session Level (Partially Expanded)**
   - Expands to show session-level data (S1-S7)
   - Includes diagnostic days (D1-D2)
   - Displays enrichment column (E)
   - Maintains percentage scores for each session

3. **Assessment Detail (Fully Expanded)**
   - Shows all individual assessments within sessions
   - Displays specific scores and completion status
   - Includes RCA components, lessons, diagnostics, and mastery assessments
   - Maintains sequential progression requirements

### Expansion Behavior
- Column groups expand/collapse together within a unit
- Multiple units can be expanded simultaneously
- Expansion state persists during grid interactions
- Smooth transitions between expansion states

## Core Component Features

### Fixed Elements
- Student information columns (first name, last name) remain fixed during horizontal scrolling
- Column headers stay visible when scrolling vertically
- Workstation assignments visible at all expansion levels

### Unit Independence
- No visual hierarchy implying required unit order
- Workstation identifier displayed with unit name
- Clear visual distinction between:
  - Available units (any incomplete unit)
  - In-progress units (started but not completed)
  - Completed units (all components finished)
  - Locked components within units (maintaining sequential progression)

### Progress Indicators
- Percentage scores displayed numerically
- Status indicators:
  - Filled circle with checkmark (✓): Completed successfully
  - Empty circle (⚪): Not yet available or pending
  - Other indicators for various states (partial completion, needs attention)
- Workstation status (occupied/available)

### Column Headers
- Hierarchical structure showing:
  - Unit name and workstation (always visible)
  - Session/Assessment type (visible when expanded)
  - Specific component names (visible in full detail)
- Headers adapt to current expansion state

## Data Display

### Cell Content
- Numerical scores shown as percentages
- Status indicators provide visual completion state
- Clear visual distinction between:
  - Completed assessments
  - In-progress work
  - Unavailable components
  - Required remediation
- Workstation availability status

### Unit Organization
- Clear visual separation between units
- Consistent column widths within expansion levels
- Logical grouping of related assessments
- Optional filtering/sorting by workstation

## User Interactions

### Column Expansion Controls
- Intuitive expand/collapse triggers
- Visual indicators showing available expansion levels
- Clear affordances for interactive elements
- Workstation-based filtering options

### Navigation
- Horizontal scrolling with fixed student information
- Keyboard navigation support
- Maintained context during expansion/collapse
- Quick jumps to specific workstations

## State Management

### Persistence Requirements
- Track expansion state per unit
- Track expansion state per session
- Maintain scroll position during transitions
- Remember workstation filters/sorts
- Store completion status of unit components

### Data Loading
- Unit summary data always loaded
- Session data loaded on Level 2 expansion
- Detailed assessment data loaded on Level 3 expansion
- Workstation status updates in real-time

## Accessibility Requirements
- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast
- Clear focus indicators
- Semantic HTML structure
- ARIA attributes for dynamic content
- Alternative text for status icons
- Workstation information clearly announced

## Technical Considerations
- Efficient handling of expand/collapse actions
- Smooth scrolling with many expanded columns
- Graceful loading of detailed data
- Real-time workstation status updates
- Browser compatibility for grid features
- Mobile/tablet responsive design

## Performance Optimization
- Progressive loading of detailed data
- Efficient handling of multiple expanded units
- Optimized rendering for large datasets
- Caching of frequently accessed data
- Minimal re-renders during state changes

## Implementation Notes

### Data Requirements
- Student information
- Unit/workstation assignments
- Component completion status
- Assessment scores
- Workstation availability
- Session progress tracking
- Real-time status updates

### Visual Hierarchy
- Clear indentation showing relationships
- Consistent styling across expansion levels
- Visual separators between units
- Distinct workstation identifiers
- Status indicator consistency

### Error Handling
- Graceful degradation for missing data
- Clear error states
- Fallback displays
- Network error recovery
- Data validation messaging
