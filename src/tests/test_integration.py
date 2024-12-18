import unittest
from VMmanagerpython import VMManager
from tag_manager import TagManager

class TestTagIntegration(unittest.TestCase):
    def setUp(self):
        self.vm_manager = VMManager()
        self.tag_manager = TagManager(self.vm_manager.file_manager)

def test_data_compatibility(self):
    # Add a tag using old system
    self.vm_manager.add_tag("TestTag")
    
    # Verify tag manager can see it
    self.assertIn("TestTag", self.tag_manager.get_all_tags())
    