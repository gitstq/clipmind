"""
Unit tests for ClipMind clipboard module.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from clipmind.clipboard import ClipboardEntry, ClipboardManager


class TestClipboardEntry(unittest.TestCase):
    """Test ClipboardEntry class."""
    
    def test_create_entry(self):
        entry = ClipboardEntry("Hello World", "text")
        self.assertEqual(entry.content, "Hello World")
        self.assertEqual(entry.entry_type, "text")
        self.assertIsNotNone(entry.timestamp)
        self.assertIsNotNone(entry.hash)
    
    def test_to_dict(self):
        entry = ClipboardEntry("test", "code")
        data = entry.to_dict()
        self.assertEqual(data["content"], "test")
        self.assertEqual(data["type"], "code")
        self.assertIn("timestamp", data)
        self.assertIn("hash", data)
    
    def test_from_dict(self):
        data = {
            "content": "test content",
            "type": "url",
            "timestamp": 1234567890,
            "hash": "abc123",
            "tags": ["important"]
        }
        entry = ClipboardEntry.from_dict(data)
        self.assertEqual(entry.content, "test content")
        self.assertEqual(entry.entry_type, "url")
        self.assertEqual(entry.timestamp, 1234567890)
        self.assertEqual(entry.hash, "abc123")
        self.assertEqual(entry.tags, ["important"])


class TestClipboardManager(unittest.TestCase):
    """Test ClipboardManager class."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_config = os.environ.get("XDG_CONFIG_HOME")
        os.environ["XDG_CONFIG_HOME"] = self.temp_dir
        self.manager = ClipboardManager()
    
    def tearDown(self):
        if self.original_config:
            os.environ["XDG_CONFIG_HOME"] = self.original_config
        else:
            del os.environ["XDG_CONFIG_HOME"]
        shutil.rmtree(self.temp_dir)
    
    def test_add_entry(self):
        result = self.manager.add("Hello World")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.history), 1)
    
    def test_add_duplicate(self):
        self.manager.add("Hello World")
        result = self.manager.add("Hello World")
        self.assertFalse(result)  # Duplicate, not added
        self.assertEqual(len(self.manager.history), 1)
    
    def test_add_empty(self):
        result = self.manager.add("")
        self.assertFalse(result)
        result = self.manager.add("   ")
        self.assertFalse(result)
    
    def test_detect_type_url(self):
        entry_type = self.manager._detect_type("https://github.com")
        self.assertEqual(entry_type, "url")
    
    def test_detect_type_code(self):
        entry_type = self.manager._detect_type("def hello(): pass")
        self.assertEqual(entry_type, "code")
    
    def test_detect_type_json(self):
        entry_type = self.manager._detect_type('{"key": "value"}')
        self.assertEqual(entry_type, "json")
    
    def test_detect_type_email(self):
        entry_type = self.manager._detect_type("test@example.com")
        self.assertEqual(entry_type, "email")
    
    def test_get_history(self):
        self.manager.add("Entry 1")
        self.manager.add("Entry 2")
        entries = self.manager.get_history(limit=1)
        self.assertEqual(len(entries), 1)
    
    def test_search(self):
        self.manager.add("Hello World")
        self.manager.add("Goodbye World")
        self.manager.add("Python Code")
        
        results = self.manager.search("World")
        self.assertEqual(len(results), 2)
        
        results = self.manager.search("Python")
        self.assertEqual(len(results), 1)
        
        results = self.manager.search("xyz")
        self.assertEqual(len(results), 0)
    
    def test_delete(self):
        self.manager.add("Entry 1")
        self.manager.add("Entry 2")
        
        result = self.manager.delete(0)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.history), 1)
        
        result = self.manager.delete(10)
        self.assertFalse(result)
    
    def test_clear(self):
        self.manager.add("Entry 1")
        self.manager.clear()
        self.assertEqual(len(self.manager.history), 0)
    
    def test_get_stats(self):
        self.manager.add("https://github.com")  # url
        self.manager.add("def hello(): pass")   # code
        self.manager.add("Hello text")          # text
        
        stats = self.manager.get_stats()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["url"], 1)
        self.assertEqual(stats["code"], 1)
        self.assertEqual(stats["text"], 1)
    
    def test_max_history(self):
        manager = ClipboardManager(max_history=3)
        manager.add("Entry 1")
        manager.add("Entry 2")
        manager.add("Entry 3")
        manager.add("Entry 4")
        
        self.assertEqual(len(manager.history), 3)


if __name__ == "__main__":
    unittest.main()
