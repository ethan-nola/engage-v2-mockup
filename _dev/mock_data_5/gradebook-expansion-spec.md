# Gradebook Expansion Levels Specification

## Level 1: Unit Summary View
The most condensed view of the gradebook, providing quick unit-level progress overview.

### Column Structure
- Fixed columns:
  - Student First Name
  - Student Last Name
- Per unit:
  - Single column showing overall unit completion percentage

### Data Display
- Unit completion shown as percentage (e.g., "98%", "100%")
- No status indicators at this level
- Column header shows only unit name (e.g., "Unit 1: Forensic Math")

### Expansion Trigger
- Expansion control visible in unit column header
- Expands to Level 2 (Session View)

## Level 2: Session View
Mid-level expansion showing session-by-session progress within units.

### Column Structure
Per unit:
1. Sessions (S1-S7)
   - Each session consolidated into single column
   - Shows overall session completion percentage
2. Diagnostic Days (D1-D2)
   - Consolidated view of diagnostic day completion
3. Enrichment (E)
   - Single column for enrichment activities

### Data Display
- Percentage scores for each session
- Column headers show:
  - Unit name
  - Session identifiers (S1-S7, D1-D2, E)
- Status indicators may appear at session level

### Expansion Controls
- Unit-level collapse returns to Level 1
- Session-level expansion reveals Level 3 detail
- Individual sessions can be expanded/collapsed independently

## Level 3: Assessment Detail View
Fully expanded view showing individual assessment components.

### Column Structure
Per session:
1. Standard Sessions (S1-S4, S6-S7):
   - Module Guide (where applicable)
   - Lesson
   - RCA (Research, Challenge, and Assess)
   - Additional session-specific components

2. Diagnostic Days (D1, D2):
   - Initial Diagnostic Assessment
   - Remedial Lesson components:
     - Lesson presentation
     - First mastery assessment
     - Second mastery assessment
   - Four diagnostic groups shown separately

3. Post-Test Session:
   - Post-test assessment
   - Associated lesson components

4. Enrichment:
   - Enrichment activities
   - Extra credit opportunities

### Data Display
- Individual assessment scores shown as percentages
- Status indicators:
  - Completed (� with percentage)
  - Not yet available (⚪)
  - Other states as needed
- Full component names in column headers

### Column Header Hierarchy
1. Top level: Unit name
2. Mid level: Session identifier
3. Bottom level: Component name

## Common Features Across Levels

### State Persistence
- Expansion state maintained during:
  - Horizontal scrolling
  - Page refresh
  - Grid sorting/filtering

### Visual Hierarchy
- Clear indentation or grouping showing relationships
- Consistent styling across expansion levels
- Visual separators between units

### Transitions
- Smooth animations between levels
- Logical expansion/collapse behavior
- Maintained context during transitions

### Performance Considerations
- Progressive loading of detailed data
- Efficient handling of multiple expanded units
- Optimized rendering for large datasets

## Implementation Notes

### Data Requirements
- Unit summary data always loaded
- Session data loaded on Level 2 expansion
- Detailed assessment data loaded on Level 3 expansion

### State Management
- Track expansion state per unit
- Track expansion state per session
- Maintain scroll position during transitions

### Accessibility
- ARIA attributes for expansion controls
- Keyboard navigation between levels
- Screen reader announcements for state changes
