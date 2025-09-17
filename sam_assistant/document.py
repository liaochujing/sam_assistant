"""Document class for representing documents in the repository."""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path


class Document:
    """Represents a document stored in the repository."""
    
    def __init__(
        self,
        doc_id: str,
        content: str,
        doc_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        created_at: Optional[datetime] = None
    ):
        """
        Initialize a Document.
        
        Args:
            doc_id: Unique identifier for the document
            content: The document content
            doc_type: Type of document (text, json, markdown, etc.)
            metadata: Additional metadata for the document
            tags: List of tags for categorization
            created_at: Creation timestamp (defaults to now)
        """
        self.doc_id = doc_id
        self.content = content
        self.doc_type = doc_type
        self.metadata = metadata or {}
        self.tags = tags or []
        self.created_at = created_at or datetime.now()
        self.updated_at = self.created_at
    
    def update_content(self, content: str) -> None:
        """Update the document content and timestamp."""
        self.content = content
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the document."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the document."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update a metadata field."""
        self.metadata[key] = value
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary representation."""
        return {
            "doc_id": self.doc_id,
            "content": self.content,
            "doc_type": self.doc_type,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create Document from dictionary representation."""
        doc = cls(
            doc_id=data["doc_id"],
            content=data["content"],
            doc_type=data.get("doc_type", "text"),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data["created_at"])
        )
        if "updated_at" in data:
            doc.updated_at = datetime.fromisoformat(data["updated_at"])
        return doc
    
    def to_json(self) -> str:
        """Convert document to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "Document":
        """Create Document from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __str__(self) -> str:
        """String representation of the document."""
        return f"Document(id={self.doc_id}, type={self.doc_type}, tags={self.tags})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the document."""
        return (f"Document(doc_id='{self.doc_id}', doc_type='{self.doc_type}', "
                f"content_length={len(self.content)}, tags={self.tags}, "
                f"created_at='{self.created_at.isoformat()}')")