"""Document Repository for managing agent documents."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Iterator
from .document import Document


class DocumentRepository:
    """Repository for storing and managing agent documents."""
    
    def __init__(self, storage_path: str = "documents"):
        """
        Initialize the document repository.
        
        Args:
            storage_path: Path where documents will be stored
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.index_file = self.storage_path / "index.json"
        self._load_index()
    
    def _load_index(self) -> None:
        """Load the document index from file."""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self._index = json.load(f)
        else:
            self._index = {}
    
    def _save_index(self) -> None:
        """Save the document index to file."""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self._index, f, indent=2)
    
    def _get_document_path(self, doc_id: str) -> Path:
        """Get the file path for a document."""
        return self.storage_path / f"{doc_id}.json"
    
    def save_document(self, document: Document) -> bool:
        """
        Save a document to the repository.
        
        Args:
            document: Document to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Save document to file
            doc_path = self._get_document_path(document.doc_id)
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(document.to_json())
            
            # Update index
            self._index[document.doc_id] = {
                "doc_type": document.doc_type,
                "tags": document.tags,
                "created_at": document.created_at.isoformat(),
                "updated_at": document.updated_at.isoformat(),
                "file_path": str(doc_path)
            }
            self._save_index()
            return True
        except Exception as e:
            print(f"Error saving document {document.doc_id}: {e}")
            return False
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """
        Retrieve a document by ID.
        
        Args:
            doc_id: Document ID to retrieve
            
        Returns:
            Document if found, None otherwise
        """
        if doc_id not in self._index:
            return None
        
        try:
            doc_path = self._get_document_path(doc_id)
            if not doc_path.exists():
                return None
            
            with open(doc_path, 'r', encoding='utf-8') as f:
                return Document.from_json(f.read())
        except Exception as e:
            print(f"Error loading document {doc_id}: {e}")
            return None
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the repository.
        
        Args:
            doc_id: Document ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        if doc_id not in self._index:
            return False
        
        try:
            doc_path = self._get_document_path(doc_id)
            if doc_path.exists():
                doc_path.unlink()
            
            del self._index[doc_id]
            self._save_index()
            return True
        except Exception as e:
            print(f"Error deleting document {doc_id}: {e}")
            return False
    
    def list_documents(self) -> List[str]:
        """
        List all document IDs in the repository.
        
        Returns:
            List of document IDs
        """
        return list(self._index.keys())
    
    def search_by_tag(self, tag: str) -> List[str]:
        """
        Search for documents by tag.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of document IDs with the specified tag
        """
        return [
            doc_id for doc_id, info in self._index.items()
            if tag in info.get("tags", [])
        ]
    
    def search_by_type(self, doc_type: str) -> List[str]:
        """
        Search for documents by type.
        
        Args:
            doc_type: Document type to search for
            
        Returns:
            List of document IDs with the specified type
        """
        return [
            doc_id for doc_id, info in self._index.items()
            if info.get("doc_type") == doc_type
        ]
    
    def search_content(self, query: str) -> List[str]:
        """
        Search for documents containing specific text.
        
        Args:
            query: Text to search for
            
        Returns:
            List of document IDs containing the query text
        """
        results = []
        for doc_id in self._index.keys():
            document = self.get_document(doc_id)
            if document and query.lower() in document.content.lower():
                results.append(doc_id)
        return results
    
    def get_documents_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[str]:
        """
        Get documents created within a date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            List of document IDs created within the date range
        """
        results = []
        for doc_id, info in self._index.items():
            created_at = datetime.fromisoformat(info["created_at"])
            if start_date <= created_at <= end_date:
                results.append(doc_id)
        return results
    
    def get_repository_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the repository.
        
        Returns:
            Dictionary with repository statistics
        """
        total_docs = len(self._index)
        doc_types = {}
        total_tags = set()
        
        for info in self._index.values():
            doc_type = info.get("doc_type", "unknown")
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            total_tags.update(info.get("tags", []))
        
        return {
            "total_documents": total_docs,
            "document_types": doc_types,
            "unique_tags": len(total_tags),
            "all_tags": sorted(list(total_tags)),
            "storage_path": str(self.storage_path)
        }
    
    def export_documents(self, export_path: str) -> bool:
        """
        Export all documents to a single JSON file.
        
        Args:
            export_path: Path to export file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "documents": {}
            }
            
            for doc_id in self._index.keys():
                document = self.get_document(doc_id)
                if document:
                    export_data["documents"][doc_id] = document.to_dict()
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting documents: {e}")
            return False
    
    def __len__(self) -> int:
        """Return the number of documents in the repository."""
        return len(self._index)
    
    def __contains__(self, doc_id: str) -> bool:
        """Check if a document exists in the repository."""
        return doc_id in self._index
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over document IDs."""
        return iter(self._index.keys())