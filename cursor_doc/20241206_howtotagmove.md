# Tag System Refactoring - Testing Guide

## Prerequisites
- Working copy of VM Manager
- Python development environment
- Git for version control

## Testing Steps

### 1. Prepare Development Environment

```bash
# Create a new branch
git checkout -b feature/tag-system-refactor

# Create backup of current files
cp src/VMmanagerpython.py src/VMmanagerpython.py.backup
```

### 2. Create Initial Test Structure

1. Create new files:
```powershell
# Create directories and files
New-Item -ItemType Directory -Path "src\tests" -Force
New-Item -ItemType File -Path "src\tag_manager.py" -Force
New-Item -ItemType File -Path "src\tests\test_tag_manager.py" -Force
```

2. Create minimal TagManager implementation:
```python:src/tag_manager.py
class TagManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.tags = set()
        self.machine_tags = {}
    
    def add_tag(self, tag_name: str) -> bool:
        if not tag_name or tag_name in self.tags:
            return False
        self.tags.add(tag_name)
        return True

    def get_all_tags(self) -> set:
        return self.tags.copy()
```

3. Create basic test:
```python:src/tests/test_tag_manager.py
import unittest
from tag_manager import TagManager

class TestTagManager(unittest.TestCase):
    def setUp(self):
        self.tag_manager = TagManager(None)  # Mock file_manager for now
    
    def test_add_tag(self):
        self.assertTrue(self.tag_manager.add_tag("Test"))
        self.assertEqual(self.tag_manager.get_all_tags(), {"Test"})
```

### 3. Run Initial Tests

```bash
# From project root
python -m unittest src/tests/test_tag_manager.py -v
```

### 4. Test Integration Points

1. Create a test file for VM Manager integration:
```python:src/tests/test_integration.py
import unittest
from VMmanagerpython import VMManager
from tag_manager import TagManager

class TestTagIntegration(unittest.TestCase):
    def setUp(self):
        self.vm_manager = VMManager()
        self.tag_manager = TagManager(self.vm_manager.file_manager)
```

2. Test data compatibility:
```python
def test_data_compatibility(self):
    # Add a tag using old system
    self.vm_manager.add_tag("TestTag")
    
    # Verify tag manager can see it
    self.assertIn("TestTag", self.tag_manager.get_all_tags())
```

### 5. Manual Testing Checklist

1. Basic Tag Operations:
- [x] Create new tag
- [x] Delete existing tag
- [x] Assign tag to machine
- [x] Remove tag from machine
- [x] Filter machines by tag

2. UI Verification:
- [ ] Tags display correctly in sidebar
- [ ] Theme switching works
- [ ] Context menus work
- [ ] Tag count updates

3. Data Persistence:
- [ ] Tags save correctly
- [ ] Tags load on restart
- [ ] Machine-tag assignments persist

### 6. Performance Testing

1. Load Testing:
```python
def test_large_tag_set():
    # Add 1000 tags
    for i in range(1000):
        self.tag_manager.add_tag(f"Tag_{i}")
    
    # Verify performance
    import time
    start = time.time()
    tags = self.tag_manager.get_all_tags()
    end = time.time()
    
    # Should be under 0.1 seconds
    self.assertLess(end - start, 0.1)
```

### 7. Error Cases to Test

1. Invalid Inputs:
- Empty tag names
- Duplicate tags
- Special characters in tags
- Very long tag names

2. Error Conditions:
- File system errors
- Memory constraints
- Concurrent modifications

### 8. Rollback Testing

1. Prepare rollback:
```powershell
# Create backup of data files
$appData = $env:LOCALAPPDATA
Copy-Item "$appData\VmManager\tags.txt" -Destination "$appData\VmManager\tags.txt.backup"
Copy-Item "$appData\VmManager\machine_tags.txt" -Destination "$appData\VmManager\machine_tags.txt.backup"
```

2. Test rollback procedure:
- [ ] Stop application
- [ ] Restore original files
- [ ] Verify application works with old system

### 9. Success Criteria Verification

For each test phase, verify:
- [ ] No errors in application log
- [ ] All features working as expected
- [ ] Performance metrics within acceptable range
- [ ] Data integrity maintained
- [ ] UI responsive and consistent

### 10. Report Issues

For any issues found:
1. Document exact steps to reproduce
2. Capture relevant logs
3. Note expected vs actual behavior
4. Take screenshots if UI-related
5. Create GitHub issue with findings

## Next Steps After Testing

1. If all tests pass:
- [ ] Update documentation
- [ ] Create pull request
- [ ] Schedule code review

2. If issues found:
- [ ] Document issues
- [ ] Prioritize fixes
- [ ] Update test cases
- [ ] Retest after fixes

## Notes
- Keep original code until new system is fully validated
- Document any workarounds or special cases discovered
- Track performance metrics for comparison
- Maintain list of any manual test cases added 