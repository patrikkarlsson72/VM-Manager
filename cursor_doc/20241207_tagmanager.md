# Tag System Refactoring - Technical Specification

## Overview
Refactor the VM Manager's tag system into a modular, maintainable component structure while maintaining all existing functionality. This is a parallel development effort - existing code will remain functional until the new implementation is fully tested.

## Objectives
- Improve code organization and maintainability
- Separate concerns (UI, business logic, data persistence)
- Maintain all existing functionality
- Enable future feature additions
- Ensure zero downtime during migration

## Component Structure

### 1. Tag Manager (`src/tag_manager.py`)
Business logic layer handling tag operations and state management.

```python
class TagManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.tags = set()
        self.machine_tags = {}
        self.active_filters = set()

    def add_tag(self, tag_name: str) -> bool
    def remove_tag(self, tag_name: str) -> bool
    def get_machine_tags(self, machine_name: str) -> List[str]
    def add_machine_tag(self, machine_name: str, tag_name: str) -> bool
    def remove_machine_tag(self, machine_name: str, tag_name: str) -> bool
    def get_machines_by_tags(self, tags: List[str]) -> List[str]
```

### 2. Tag Sidebar (`src/tag_sidebar.py`)
UI component handling tag display and user interactions.

```python
class TagSidebar(ttk.Frame):
    def __init__(self, parent, tag_manager, theme="dark"):
        self.tag_manager = tag_manager
        self.theme = theme
        self.setup_ui()

    def setup_ui(self)
    def create_tag(self, tag_name: str)
    def remove_tag(self, tag_name: str)
    def update_theme(self, theme: str)
    def handle_tag_selection(self, tag_name: str)
```

### 3. File Manager Integration
Extend existing FileManager with dedicated tag persistence methods.

## Implementation Phases

### Phase 1: Core Components (Week 1)
- [ ] Create TagManager class with core functionality
- [ ] Create TagSidebar class with basic UI
- [ ] Add file operations for tag persistence
- [ ] Write unit tests for new components

### Phase 2: Integration (Week 1-2)
- [ ] Integrate TagManager with VMManager
- [ ] Integrate TagSidebar with VMManagerUI
- [ ] Implement event handling between components
- [ ] Add integration tests

### Phase 3: Feature Parity (Week 2)
- [ ] Implement all existing tag features in new system
- [ ] Add theme support
- [ ] Migrate existing tag data
- [ ] Test all functionality

### Phase 4: Testing & Validation (Week 2-3)
- [ ] Comprehensive testing of all features
- [ ] Performance testing
- [ ] User acceptance testing
- [ ] Documentation updates

## Technical Requirements

### Event System
```python
# Custom events for tag operations
<<TagAdded>>        # When a new tag is created
<<TagRemoved>>      # When a tag is deleted
<<TagSelected>>     # When tag selection changes
<<TagsUpdated>>     # When any tag operation completes
```

### Theme Support
- Must support light/dark themes
- Theme changes must be immediate
- All UI elements must respect theme colors

### Data Persistence
- Tag data stored in dedicated files
- Automatic saving on changes
- Error handling for file operations

## Testing Strategy
1. Unit tests for TagManager
2. UI tests for TagSidebar
3. Integration tests for full system
4. Migration tests for data conversion

## Success Criteria
- [ ] All existing functionality preserved
- [ ] No regression in main application
- [ ] Successful data migration
- [ ] Performance maintained or improved
- [ ] Clean separation of concerns
- [ ] Comprehensive test coverage

## Future Considerations
- Tag categories/hierarchies
- Tag search/filtering
- Drag-and-drop reordering
- Multi-select capabilities
- Tag metadata support

## Rollback Plan
1. Keep existing code until new system is proven
2. Maintain data file compatibility
3. Include version markers in new data files
4. Document rollback procedures

## Documentation Requirements
- Update technical documentation
- Update user guide
- Add inline code documentation
- Create migration guide

## Timeline
- Week 1: Core Components & Initial Integration
- Week 2: Feature Parity & Testing
- Week 3: Final Testing & Documentation

## Dependencies
- Python 3.x
- Tkinter
- Existing VM Manager codebase
- Unit testing framework

## Team Communication
- Daily updates on progress
- Immediate notification of blocking issues
- Code review requirements
- Documentation review process

## Questions & Clarifications
For any questions or clarifications, please contact:
- Technical Lead: [Name]
- Project Manager: [Name] 