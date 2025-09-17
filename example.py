#!/usr/bin/env python3
"""Example usage of the sam_assistant document repository."""

from datetime import datetime
from sam_assistant import DocumentRepository, Document


def main():
    """Demonstrate the document repository functionality."""
    print("Sam Assistant Document Repository Demo")
    print("=" * 40)
    
    # Create a repository
    repo = DocumentRepository("example_documents")
    print(f"Created repository at: {repo.storage_path}")
    
    # Create some example documents
    print("\n1. Creating sample documents...")
    
    # Text document
    text_doc = Document(
        doc_id="meeting_notes_001",
        content="Meeting with client about project requirements. Key points: budget $50k, deadline March 2024.",
        doc_type="text",
        metadata={"client": "ABC Corp", "priority": "high"},
        tags=["meeting", "client", "important"]
    )
    
    # JSON document
    json_doc = Document(
        doc_id="config_001",
        content='{"api_key": "xxx", "endpoint": "https://api.example.com", "timeout": 30}',
        doc_type="json",
        metadata={"environment": "production"},
        tags=["config", "api"]
    )
    
    # Markdown document
    markdown_doc = Document(
        doc_id="readme_001",
        content="# Project Overview\n\nThis is a document management system for AI agents.\n\n## Features\n- Save documents\n- Search by tags\n- Full-text search",
        doc_type="markdown",
        tags=["documentation", "readme"]
    )
    
    # Save documents
    repo.save_document(text_doc)
    repo.save_document(json_doc)
    repo.save_document(markdown_doc)
    
    print(f"Saved {len(repo)} documents")
    
    # List all documents
    print("\n2. Listing all documents:")
    for doc_id in repo.list_documents():
        doc = repo.get_document(doc_id)
        print(f"  - {doc_id}: {doc.doc_type} ({len(doc.content)} chars) - Tags: {doc.tags}")
    
    # Search by tags
    print("\n3. Searching by tags:")
    important_docs = repo.search_by_tag("important")
    print(f"  Documents tagged 'important': {important_docs}")
    
    config_docs = repo.search_by_tag("config")
    print(f"  Documents tagged 'config': {config_docs}")
    
    # Search by type
    print("\n4. Searching by document type:")
    text_docs = repo.search_by_type("text")
    print(f"  Text documents: {text_docs}")
    
    json_docs = repo.search_by_type("json")
    print(f"  JSON documents: {json_docs}")
    
    # Content search
    print("\n5. Content search:")
    project_docs = repo.search_content("project")
    print(f"  Documents containing 'project': {project_docs}")
    
    api_docs = repo.search_content("api")
    print(f"  Documents containing 'api': {api_docs}")
    
    # Repository statistics
    print("\n6. Repository statistics:")
    stats = repo.get_repository_stats()
    print(f"  Total documents: {stats['total_documents']}")
    print(f"  Document types: {stats['document_types']}")
    print(f"  Unique tags: {stats['unique_tags']}")
    print(f"  All tags: {stats['all_tags']}")
    
    # Update a document
    print("\n7. Updating a document:")
    meeting_doc = repo.get_document("meeting_notes_001")
    if meeting_doc:
        print(f"  Original content length: {len(meeting_doc.content)}")
        meeting_doc.update_content(meeting_doc.content + "\n\nUpdate: Client approved initial proposal.")
        meeting_doc.add_tag("approved")
        repo.save_document(meeting_doc)
        print(f"  Updated content length: {len(meeting_doc.content)}")
        print(f"  New tags: {meeting_doc.tags}")
    
    # Export documents
    print("\n8. Exporting documents:")
    export_path = "exported_documents.json"
    success = repo.export_documents(export_path)
    if success:
        print(f"  Documents exported to: {export_path}")
    
    # Demonstrate retrieval
    print("\n9. Document retrieval example:")
    retrieved_doc = repo.get_document("config_001")
    if retrieved_doc:
        print(f"  Retrieved: {retrieved_doc}")
        print(f"  Content: {retrieved_doc.content}")
        print(f"  Metadata: {retrieved_doc.metadata}")
    
    print("\n" + "=" * 40)
    print("Demo completed!")


if __name__ == "__main__":
    main()