# Sam Assistant - Document Repository

A Python-based document repository system designed for AI agents to save, manage, and search documents efficiently.

## Features

- **Document Storage**: Save documents with metadata, tags, and different content types
- **Search Capabilities**: Search by tags, document type, content, and date ranges
- **CRUD Operations**: Create, read, update, and delete documents
- **Metadata Management**: Track creation/update timestamps and custom metadata
- **Export/Import**: Export all documents to JSON format
- **Tag System**: Organize documents with flexible tagging
- **Multiple Content Types**: Support for text, JSON, markdown, and custom types

## Installation

1. Clone the repository:
```bash
git clone https://github.com/liaochujing/sam_assistant.git
cd sam_assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Quick Start

```python
from sam_assistant import DocumentRepository, Document

# Create a repository
repo = DocumentRepository("my_documents")

# Create a document
doc = Document(
    doc_id="my_first_doc",
    content="This is my first document",
    doc_type="text",
    tags=["example", "first"]
)

# Save the document
repo.save_document(doc)

# Retrieve the document
retrieved_doc = repo.get_document("my_first_doc")
print(retrieved_doc.content)

# Search documents
docs_with_tag = repo.search_by_tag("example")
text_docs = repo.search_by_type("text")
content_search = repo.search_content("first")
```

## API Reference

### Document Class

The `Document` class represents a single document in the repository.

#### Constructor
```python
Document(doc_id, content, doc_type="text", metadata=None, tags=None, created_at=None)
```

- `doc_id`: Unique identifier for the document
- `content`: The document content (string)
- `doc_type`: Type of document (text, json, markdown, etc.)
- `metadata`: Dictionary of additional metadata
- `tags`: List of tags for categorization
- `created_at`: Creation timestamp (defaults to now)

#### Methods
- `update_content(content)`: Update document content
- `add_tag(tag)`: Add a tag to the document
- `remove_tag(tag)`: Remove a tag from the document
- `update_metadata(key, value)`: Update metadata field
- `to_dict()`: Convert to dictionary
- `to_json()`: Convert to JSON string
- `from_json(json_str)`: Create document from JSON

### DocumentRepository Class

The `DocumentRepository` class manages document storage and retrieval.

#### Constructor
```python
DocumentRepository(storage_path="documents")
```

- `storage_path`: Directory where documents will be stored

#### Methods

**Document Management:**
- `save_document(document)`: Save a document
- `get_document(doc_id)`: Retrieve a document by ID
- `delete_document(doc_id)`: Delete a document
- `list_documents()`: Get list of all document IDs

**Search Operations:**
- `search_by_tag(tag)`: Find documents with specific tag
- `search_by_type(doc_type)`: Find documents of specific type
- `search_content(query)`: Search document content
- `get_documents_by_date_range(start, end)`: Find documents by date

**Repository Operations:**
- `get_repository_stats()`: Get statistics about the repository
- `export_documents(export_path)`: Export all documents to JSON

## Examples

### Basic Usage

```python
from sam_assistant import DocumentRepository, Document

# Create repository
repo = DocumentRepository("agent_documents")

# Create different types of documents
meeting_notes = Document(
    "meeting_001", 
    "Meeting with client about requirements",
    "text",
    {"client": "ABC Corp", "priority": "high"},
    ["meeting", "client"]
)

config_doc = Document(
    "config_001",
    '{"api_key": "xxx", "timeout": 30}',
    "json",
    {"environment": "production"},
    ["config", "api"]
)

# Save documents
repo.save_document(meeting_notes)
repo.save_document(config_doc)

# Search and retrieve
important_docs = repo.search_by_tag("client")
config_docs = repo.search_by_type("json")
```

### Advanced Search

```python
from datetime import datetime, timedelta

# Search by content
api_docs = repo.search_content("api")

# Search by date range
yesterday = datetime.now() - timedelta(days=1)
today = datetime.now()
recent_docs = repo.get_documents_by_date_range(yesterday, today)

# Get repository statistics
stats = repo.get_repository_stats()
print(f"Total documents: {stats['total_documents']}")
print(f"Document types: {stats['document_types']}")
```

### Document Updates

```python
# Retrieve and update a document
doc = repo.get_document("meeting_001")
if doc:
    doc.update_content(doc.content + "\n\nUpdate: Project approved")
    doc.add_tag("approved")
    doc.update_metadata("status", "completed")
    repo.save_document(doc)
```

## File Structure

The repository creates the following structure:

```
storage_path/
├── index.json          # Document index with metadata
├── doc_id1.json        # Individual document files
├── doc_id2.json
└── ...
```

## Testing

Run the test suite:

```bash
python -m unittest tests.test_document_repository -v
```

## Example Demo

Run the included example script to see the system in action:

```bash
python example.py
```

This will create sample documents and demonstrate all major features.

## License

This project is open source and available under the MIT License.