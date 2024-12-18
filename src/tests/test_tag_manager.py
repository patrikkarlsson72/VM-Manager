import unittest
import sys
import os

# Add parent directory to path to find tag_manager module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tag_manager import TagManager

class TestTagManager(unittest.TestCase):
    def setUp(self):
        self.tag_manager = TagManager(None)  # Mock file_manager for now
    
    def test_add_tag(self):
        self.assertTrue(self.tag_manager.add_tag("Test"))
        self.assertEqual(self.tag_manager.get_all_tags(), {"Test"})