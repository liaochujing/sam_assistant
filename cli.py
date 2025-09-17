#!/usr/bin/env python3
"""Command-line interface for the sam_assistant document repository."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from sam_assistant import DocumentRepository, Document


def create_document(args):
    """Create a new document."""
    repo = DocumentRepository(args.repo_path)
    
    # Read content from file or stdin
    if args.file:
        content = Path(args.file).read_text(encoding='utf-8')
    elif args.content:
        content = args.content
    else:
        print("Reading content from stdin (Ctrl+D to finish):")
        content = sys.stdin.read()
    
    # Parse metadata if provided
    metadata = {}
    if args.metadata:
        try:
            metadata = json.loads(args.metadata)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in metadata: {args.metadata}")
            return 1
    
    # Create and save document
    doc = Document(
        doc_id=args.doc_id,
        content=content,
        doc_type=args.type,
        metadata=metadata,
        tags=args.tags or []
    )
    
    success = repo.save_document(doc)
    if success:
        print(f"Document '{args.doc_id}' created successfully")
        return 0
    else:
        print(f"Error: Failed to create document '{args.doc_id}'")
        return 1


def get_document(args):
    """Retrieve and display a document."""
    repo = DocumentRepository(args.repo_path)
    doc = repo.get_document(args.doc_id)
    
    if not doc:
        print(f"Error: Document '{args.doc_id}' not found")
        return 1
    
    if args.format == 'json':
        print(doc.to_json())
    elif args.format == 'content':
        print(doc.content)
    else:
        print(f"Document ID: {doc.doc_id}")
        print(f"Type: {doc.doc_type}")
        print(f"Tags: {doc.tags}")
        print(f"Created: {doc.created_at}")
        print(f"Updated: {doc.updated_at}")
        print(f"Metadata: {doc.metadata}")
        print(f"Content:\n{doc.content}")
    
    return 0


def list_documents(args):
    """List all documents."""
    repo = DocumentRepository(args.repo_path)
    doc_ids = repo.list_documents()
    
    if not doc_ids:
        print("No documents found")
        return 0
    
    if args.verbose:
        for doc_id in doc_ids:
            doc = repo.get_document(doc_id)
            print(f"{doc_id}: {doc.doc_type} ({len(doc.content)} chars) - {doc.tags}")
    else:
        for doc_id in doc_ids:
            print(doc_id)
    
    return 0


def search_documents(args):
    """Search for documents."""
    repo = DocumentRepository(args.repo_path)
    
    if args.tag:
        results = repo.search_by_tag(args.tag)
    elif args.type:
        results = repo.search_by_type(args.type)
    elif args.content:
        results = repo.search_content(args.content)
    else:
        print("Error: Must specify --tag, --type, or --content for search")
        return 1
    
    if not results:
        print("No documents found")
        return 0
    
    for doc_id in results:
        if args.verbose:
            doc = repo.get_document(doc_id)
            print(f"{doc_id}: {doc.doc_type} - {doc.tags}")
        else:
            print(doc_id)
    
    return 0


def delete_document(args):
    """Delete a document."""
    repo = DocumentRepository(args.repo_path)
    
    if not args.force:
        response = input(f"Are you sure you want to delete '{args.doc_id}'? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled")
            return 0
    
    success = repo.delete_document(args.doc_id)
    if success:
        print(f"Document '{args.doc_id}' deleted successfully")
        return 0
    else:
        print(f"Error: Failed to delete document '{args.doc_id}' (not found)")
        return 1


def repository_stats(args):
    """Show repository statistics."""
    repo = DocumentRepository(args.repo_path)
    stats = repo.get_repository_stats()
    
    print(f"Repository Statistics:")
    print(f"  Storage Path: {stats['storage_path']}")
    print(f"  Total Documents: {stats['total_documents']}")
    print(f"  Document Types: {stats['document_types']}")
    print(f"  Unique Tags: {stats['unique_tags']}")
    print(f"  All Tags: {', '.join(stats['all_tags'])}")
    
    return 0


def export_documents(args):
    """Export all documents."""
    repo = DocumentRepository(args.repo_path)
    success = repo.export_documents(args.output)
    
    if success:
        print(f"Documents exported to: {args.output}")
        return 0
    else:
        print(f"Error: Failed to export documents")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Sam Assistant Document Repository CLI")
    parser.add_argument("--repo-path", default="documents", help="Repository storage path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new document")
    create_parser.add_argument("doc_id", help="Document ID")
    create_parser.add_argument("--content", help="Document content")
    create_parser.add_argument("--file", help="Read content from file")
    create_parser.add_argument("--type", default="text", help="Document type")
    create_parser.add_argument("--tags", nargs="*", help="Document tags")
    create_parser.add_argument("--metadata", help="JSON metadata")
    create_parser.set_defaults(func=create_document)
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Retrieve a document")
    get_parser.add_argument("doc_id", help="Document ID")
    get_parser.add_argument("--format", choices=["full", "json", "content"], default="full", help="Output format")
    get_parser.set_defaults(func=get_document)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all documents")
    list_parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed information")
    list_parser.set_defaults(func=list_documents)
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for documents")
    search_parser.add_argument("--tag", help="Search by tag")
    search_parser.add_argument("--type", help="Search by document type")
    search_parser.add_argument("--content", help="Search document content")
    search_parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed information")
    search_parser.set_defaults(func=search_documents)
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a document")
    delete_parser.add_argument("doc_id", help="Document ID")
    delete_parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation")
    delete_parser.set_defaults(func=delete_document)
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show repository statistics")
    stats_parser.set_defaults(func=repository_stats)
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export all documents")
    export_parser.add_argument("output", help="Output file path")
    export_parser.set_defaults(func=export_documents)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())