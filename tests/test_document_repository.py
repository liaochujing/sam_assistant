"""Tests for the sam_assistant document repository."""

import unittest
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

from sam_assistant.document import Document
from sam_assistant.document_repository import DocumentRepository


class TestDocument(unittest.TestCase):
    """Test cases for the Document class."""
    
    def test_document_creation(self):
        """Test basic document creation."""
        doc = Document("test_doc", "This is test content", "text")
        
        self.assertEqual(doc.doc_id, "test_doc")
        self.assertEqual(doc.content, "This is test content")
        self.assertEqual(doc.doc_type, "text")
        self.assertEqual(doc.tags, [])
        self.assertIsInstance(doc.created_at, datetime)
    
    def test_document_with_metadata(self):
        """Test document creation with metadata and tags."""
        metadata = {"author": "test_agent", "importance": "high"}
        tags = ["important", "test"]
        
        doc = Document("test_doc", "Content", "text", metadata, tags)
        
        self.assertEqual(doc.metadata, metadata)
        self.assertEqual(doc.tags, tags)
    
    def test_document_serialization(self):
        """Test document to/from JSON conversion."""
        doc = Document("test_doc", "Content", "text", {"key": "value"}, ["tag1"])
        
        # Test to_dict
        doc_dict = doc.to_dict()
        self.assertIn("doc_id", doc_dict)
        self.assertIn("content", doc_dict)
        self.assertIn("created_at", doc_dict)
        
        # Test to_json and from_json
        json_str = doc.to_json()
        restored_doc = Document.from_json(json_str)
        
        self.assertEqual(doc.doc_id, restored_doc.doc_id)
        self.assertEqual(doc.content, restored_doc.content)
        self.assertEqual(doc.doc_type, restored_doc.doc_type)
        self.assertEqual(doc.metadata, restored_doc.metadata)
        self.assertEqual(doc.tags, restored_doc.tags)
    
    def test_document_update_content(self):
        """Test updating document content."""
        doc = Document("test_doc", "Original content")
        original_updated_at = doc.updated_at
        
        doc.update_content("New content")
        
        self.assertEqual(doc.content, "New content")
        self.assertGreater(doc.updated_at, original_updated_at)
    
    def test_tag_operations(self):
        """Test adding and removing tags."""
        doc = Document("test_doc", "Content")
        
        doc.add_tag("new_tag")
        self.assertIn("new_tag", doc.tags)
        
        doc.add_tag("new_tag")  # Should not duplicate
        self.assertEqual(doc.tags.count("new_tag"), 1)
        
        doc.remove_tag("new_tag")
        self.assertNotIn("new_tag", doc.tags)


class TestDocumentRepository(unittest.TestCase):
    """Test cases for the DocumentRepository class."""
    
    def setUp(self):
        """Set up test repository."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo = DocumentRepository(self.temp_dir)
    
    def tearDown(self):
        """Clean up test repository."""
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_get_document(self):
        """Test saving and retrieving documents."""
        doc = Document("test_doc", "Test content", "text", {"key": "value"}, ["tag1"])
        
        # Save document
        success = self.repo.save_document(doc)
        self.assertTrue(success)
        
        # Retrieve document
        retrieved_doc = self.repo.get_document("test_doc")
        self.assertIsNotNone(retrieved_doc)
        self.assertEqual(retrieved_doc.doc_id, "test_doc")
        self.assertEqual(retrieved_doc.content, "Test content")
        self.assertEqual(retrieved_doc.metadata, {"key": "value"})
        self.assertEqual(retrieved_doc.tags, ["tag1"])
    
    def test_delete_document(self):
        """Test deleting documents."""
        doc = Document("test_doc", "Test content")
        
        self.repo.save_document(doc)
        self.assertTrue("test_doc" in self.repo)
        
        success = self.repo.delete_document("test_doc")
        self.assertTrue(success)
        self.assertFalse("test_doc" in self.repo)
        
        retrieved_doc = self.repo.get_document("test_doc")
        self.assertIsNone(retrieved_doc)
    
    def test_list_documents(self):
        """Test listing all documents."""
        doc1 = Document("doc1", "Content 1")
        doc2 = Document("doc2", "Content 2")
        
        self.repo.save_document(doc1)
        self.repo.save_document(doc2)
        
        doc_list = self.repo.list_documents()
        self.assertIn("doc1", doc_list)
        self.assertIn("doc2", doc_list)
        self.assertEqual(len(doc_list), 2)
    
    def test_search_by_tag(self):
        """Test searching documents by tag."""
        doc1 = Document("doc1", "Content 1", tags=["important", "work"])
        doc2 = Document("doc2", "Content 2", tags=["personal"])
        doc3 = Document("doc3", "Content 3", tags=["important", "personal"])
        
        self.repo.save_document(doc1)
        self.repo.save_document(doc2)
        self.repo.save_document(doc3)
        
        important_docs = self.repo.search_by_tag("important")
        self.assertIn("doc1", important_docs)
        self.assertIn("doc3", important_docs)
        self.assertNotIn("doc2", important_docs)
        
        personal_docs = self.repo.search_by_tag("personal")
        self.assertIn("doc2", personal_docs)
        self.assertIn("doc3", personal_docs)
        self.assertNotIn("doc1", personal_docs)
    
    def test_search_by_type(self):
        """Test searching documents by type."""
        doc1 = Document("doc1", "Text content", "text")
        doc2 = Document("doc2", '{"key": "value"}', "json")
        doc3 = Document("doc3", "# Markdown", "markdown")
        
        self.repo.save_document(doc1)
        self.repo.save_document(doc2)
        self.repo.save_document(doc3)
        
        text_docs = self.repo.search_by_type("text")
        self.assertIn("doc1", text_docs)
        self.assertNotIn("doc2", text_docs)
        self.assertNotIn("doc3", text_docs)
        
        json_docs = self.repo.search_by_type("json")
        self.assertIn("doc2", json_docs)
        self.assertEqual(len(json_docs), 1)
    
    def test_search_content(self):
        """Test searching documents by content."""
        doc1 = Document("doc1", "This is a test document")
        doc2 = Document("doc2", "Another document with different content")
        doc3 = Document("doc3", "Test content for searching")
        
        self.repo.save_document(doc1)
        self.repo.save_document(doc2)
        self.repo.save_document(doc3)
        
        test_docs = self.repo.search_content("test")
        self.assertIn("doc1", test_docs)
        self.assertIn("doc3", test_docs)
        self.assertNotIn("doc2", test_docs)
        
        content_docs = self.repo.search_content("content")
        self.assertIn("doc2", content_docs)
        self.assertIn("doc3", content_docs)
    
    def test_repository_stats(self):
        """Test repository statistics."""
        doc1 = Document("doc1", "Content", "text", tags=["tag1", "tag2"])
        doc2 = Document("doc2", "Content", "json", tags=["tag2", "tag3"])
        
        self.repo.save_document(doc1)
        self.repo.save_document(doc2)
        
        stats = self.repo.get_repository_stats()
        
        self.assertEqual(stats["total_documents"], 2)
        self.assertEqual(stats["document_types"]["text"], 1)
        self.assertEqual(stats["document_types"]["json"], 1)
        self.assertEqual(stats["unique_tags"], 3)
        self.assertIn("tag1", stats["all_tags"])
        self.assertIn("tag2", stats["all_tags"])
        self.assertIn("tag3", stats["all_tags"])
    
    def test_repository_operators(self):
        """Test repository special methods."""
        doc = Document("test_doc", "Content")
        self.repo.save_document(doc)
        
        # Test __len__
        self.assertEqual(len(self.repo), 1)
        
        # Test __contains__
        self.assertTrue("test_doc" in self.repo)
        self.assertFalse("nonexistent" in self.repo)
        
        # Test __iter__
        doc_ids = list(self.repo)
        self.assertIn("test_doc", doc_ids)


if __name__ == "__main__":
    unittest.main()