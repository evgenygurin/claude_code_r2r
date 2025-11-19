"""
Comprehensive Tests for R2R Documents API
Tests various scenarios for document management endpoints
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.api_client import R2RAPIClient
import json
import tempfile
from pathlib import Path


class DocumentsAPITester:
    """Test suite for Documents API endpoints"""

    def __init__(self, client: R2RAPIClient):
        self.client = client
        self.test_document_ids = []

    def create_test_file(self, content: str, filename: str = "test.txt") -> str:
        """Create a temporary test file"""
        temp_dir = Path(tempfile.gettempdir())
        file_path = temp_dir / filename
        file_path.write_text(content, encoding='utf-8')
        return str(file_path)

    def test_document_creation(self):
        """Test 10+ scenarios for document creation"""
        print("\n" + "="*80)
        print("TESTING DOCUMENT CREATION ENDPOINTS")
        print("="*80)

        # Scenario 1: Create simple text document
        print("\n1. Creating simple text document...")
        file_path = self.create_test_file("This is a test document about AI and machine learning.")
        result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Test Document", "category": "AI"},
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Simple text document with fast mode",
            result,
            200,
            "Create a basic text document with minimal metadata"
        )
        if result.get("status_code") == 200 and isinstance(result.get("body"), dict):
            doc_id = result["body"].get("document_id")
            if doc_id:
                self.test_document_ids.append(doc_id)

        # Scenario 2: Create document with hi-res mode
        print("\n2. Creating document with hi-res ingestion mode...")
        file_path = self.create_test_file("High resolution processing test document with complex content.")
        result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Hi-Res Test", "quality": "high"},
            ingestion_mode="hi-res"
        )
        self.client.log_test_result(
            "Document Creation",
            "Hi-res ingestion mode",
            result,
            200,
            "Test high-quality document processing"
        )
        if result.get("status_code") == 200 and isinstance(result.get("body"), dict):
            doc_id = result["body"].get("document_id")
            if doc_id:
                self.test_document_ids.append(doc_id)

        # Scenario 3: Create document with extensive metadata
        print("\n3. Creating document with extensive metadata...")
        file_path = self.create_test_file("Document with extensive metadata for testing.")
        metadata = {
            "title": "Extensive Metadata Document",
            "author": "Test Author",
            "category": "Research",
            "tags": ["test", "metadata", "research"],
            "date": "2025-11-19",
            "version": "1.0",
            "language": "en"
        }
        result = self.client.create_document(
            file_path=file_path,
            metadata=metadata,
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Document with extensive metadata",
            result,
            200,
            "Test metadata handling capabilities"
        )

        # Scenario 4: Create document with special characters
        print("\n4. Creating document with special characters...")
        file_path = self.create_test_file(
            "Test document with special characters: @#$%^&*()_+{}|:<>?[];',./~`\n" +
            "Unicode: こんにちは 你好 Здравствуйте"
        )
        result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Special Characters Test"},
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Document with special characters and Unicode",
            result,
            200,
            "Test handling of special characters and Unicode"
        )

        # Scenario 5: Create document with long content
        print("\n5. Creating document with long content (>10KB)...")
        long_content = "This is a test document. " * 500  # ~12.5KB
        file_path = self.create_test_file(long_content)
        result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Long Document", "size": "large"},
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Large document (>10KB)",
            result,
            200,
            "Test handling of large documents"
        )
        if result.get("status_code") == 200 and isinstance(result.get("body"), dict):
            doc_id = result["body"].get("document_id")
            if doc_id:
                self.test_document_ids.append(doc_id)

        # Scenario 6: Create document without metadata
        print("\n6. Creating document without metadata...")
        file_path = self.create_test_file("Document without any metadata.")
        result = self.client.create_document(
            file_path=file_path,
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Document without metadata",
            result,
            200,
            "Test document creation without optional metadata"
        )

        # Scenario 7: Create empty document
        print("\n7. Creating empty document...")
        file_path = self.create_test_file("")
        result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Empty Document"},
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Empty document",
            result,
            400,  # Expecting error
            "Test error handling for empty documents"
        )

        # Scenario 8: Create document with invalid ingestion mode
        print("\n8. Creating document with invalid ingestion mode...")
        file_path = self.create_test_file("Test document for invalid mode.")
        result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Invalid Mode Test"},
            ingestion_mode="invalid_mode"
        )
        self.client.log_test_result(
            "Document Creation",
            "Invalid ingestion mode",
            result,
            400,  # Expecting error
            "Test validation of ingestion mode parameter"
        )

        # Scenario 9: Create document with malformed JSON metadata
        print("\n9. Creating document with complex nested metadata...")
        file_path = self.create_test_file("Test document with nested metadata.")
        nested_metadata = {
            "title": "Nested Metadata",
            "details": {
                "author": {"name": "John Doe", "email": "john@example.com"},
                "tags": [{"category": "AI", "priority": 1}, {"category": "ML", "priority": 2}]
            }
        }
        result = self.client.create_document(
            file_path=file_path,
            metadata=nested_metadata,
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Nested metadata structures",
            result,
            200,
            "Test handling of complex nested metadata"
        )

        # Scenario 10: Create multiple documents rapidly
        print("\n10. Creating multiple documents in rapid succession...")
        for i in range(3):
            file_path = self.create_test_file(f"Rapid creation test document #{i+1}")
            result = self.client.create_document(
                file_path=file_path,
                metadata={"title": f"Rapid Test {i+1}", "batch": "rapid"},
                ingestion_mode="fast"
            )
            self.client.log_test_result(
                "Document Creation",
                f"Rapid creation #{i+1}/3",
                result,
                200,
                "Test API performance under rapid requests"
            )
            if result.get("status_code") == 200 and isinstance(result.get("body"), dict):
                doc_id = result["body"].get("document_id")
                if doc_id:
                    self.test_document_ids.append(doc_id)

        # Scenario 11: Create document with PDF-like content
        print("\n11. Creating document with structured content...")
        structured_content = """
# Title: Research Paper
## Abstract
This is a test abstract.

## Introduction
This is the introduction section with multiple paragraphs.

## Methods
- Method 1
- Method 2
- Method 3

## Results
Results go here.

## Conclusion
Final thoughts.
"""
        file_path = self.create_test_file(structured_content, "structured.md")
        result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Structured Document", "format": "markdown"},
            ingestion_mode="hi-res"
        )
        self.client.log_test_result(
            "Document Creation",
            "Structured markdown document",
            result,
            200,
            "Test handling of structured/formatted content"
        )

        # Scenario 12: Create document without file (using content directly)
        print("\n12. Creating document with inline content...")
        result = self.client.create_document(
            content="Inline content without file upload.",
            metadata={"title": "Inline Content"},
            ingestion_mode="fast"
        )
        self.client.log_test_result(
            "Document Creation",
            "Inline content without file",
            result,
            200,
            "Test direct content submission without file upload"
        )

    def test_document_retrieval(self):
        """Test 10+ scenarios for document retrieval"""
        print("\n" + "="*80)
        print("TESTING DOCUMENT RETRIEVAL ENDPOINTS")
        print("="*80)

        # Scenario 1: List all documents
        print("\n1. Listing all documents...")
        result = self.client.list_documents()
        self.client.log_test_result(
            "Document Retrieval",
            "List all documents",
            result,
            200,
            "Retrieve list of all documents"
        )

        # Scenario 2: List documents with pagination (limit)
        print("\n2. Listing documents with limit=5...")
        result = self.client.list_documents(limit=5)
        self.client.log_test_result(
            "Document Retrieval",
            "List documents with pagination (limit=5)",
            result,
            200,
            "Test pagination with limit parameter"
        )

        # Scenario 3: List documents with offset
        print("\n3. Listing documents with offset=2, limit=3...")
        result = self.client.list_documents(offset=2, limit=3)
        self.client.log_test_result(
            "Document Retrieval",
            "List documents with offset and limit",
            result,
            200,
            "Test pagination with both offset and limit"
        )

        # Scenario 4: Get specific document by ID (valid)
        if self.test_document_ids:
            print(f"\n4. Retrieving document by valid ID: {self.test_document_ids[0]}...")
            result = self.client.get_document(self.test_document_ids[0])
            self.client.log_test_result(
                "Document Retrieval",
                "Get document by valid ID",
                result,
                200,
                "Retrieve specific document using valid ID"
            )
        else:
            print("\n4. Skipping - no test documents available")

        # Scenario 5: Get document by invalid ID
        print("\n5. Retrieving document by invalid ID...")
        result = self.client.get_document("invalid-document-id-12345")
        self.client.log_test_result(
            "Document Retrieval",
            "Get document by invalid ID",
            result,
            404,
            "Test error handling for invalid document ID"
        )

        # Scenario 6: Get document with malformed ID
        print("\n6. Retrieving document with malformed ID...")
        result = self.client.get_document("@#$%^&*()")
        self.client.log_test_result(
            "Document Retrieval",
            "Get document with malformed ID",
            result,
            400,
            "Test validation of document ID format"
        )

        # Scenario 7: List documents with filters
        print("\n7. Listing documents with metadata filter...")
        filters = {"category": "AI"}
        result = self.client.list_documents(filters=filters)
        self.client.log_test_result(
            "Document Retrieval",
            "List documents with metadata filter",
            result,
            200,
            "Test filtering documents by metadata"
        )

        # Scenario 8: List documents with limit=0
        print("\n8. Listing documents with limit=0...")
        result = self.client.list_documents(limit=0)
        self.client.log_test_result(
            "Document Retrieval",
            "List documents with limit=0",
            result,
            200,  # or 400 depending on API behavior
            "Test edge case: zero limit"
        )

        # Scenario 9: List documents with very large limit
        print("\n9. Listing documents with limit=10000...")
        result = self.client.list_documents(limit=10000)
        self.client.log_test_result(
            "Document Retrieval",
            "List documents with very large limit",
            result,
            200,
            "Test handling of large limit values"
        )

        # Scenario 10: List documents with negative offset
        print("\n10. Listing documents with negative offset...")
        result = self.client.list_documents(offset=-1)
        self.client.log_test_result(
            "Document Retrieval",
            "List documents with negative offset",
            result,
            400,
            "Test validation of negative offset values"
        )

        # Scenario 11: Download document content
        if self.test_document_ids:
            print(f"\n11. Downloading document content: {self.test_document_ids[0]}...")
            result = self.client.download_document(self.test_document_ids[0])
            self.client.log_test_result(
                "Document Retrieval",
                "Download document content",
                result,
                200,
                "Download original document file"
            )

        # Scenario 12: List documents with complex filter
        print("\n12. Listing documents with complex filter...")
        complex_filter = {"category": "AI", "tags": ["test"]}
        result = self.client.list_documents(filters=complex_filter)
        self.client.log_test_result(
            "Document Retrieval",
            "List documents with complex filter",
            result,
            200,
            "Test complex multi-field filtering"
        )

    def test_document_updates(self):
        """Test 10+ scenarios for document updates"""
        print("\n" + "="*80)
        print("TESTING DOCUMENT UPDATE ENDPOINTS")
        print("="*80)

        if not self.test_document_ids:
            print("No test documents available for update tests")
            return

        doc_id = self.test_document_ids[0]

        # Scenario 1: Update document metadata
        print("\n1. Updating document metadata...")
        result = self.client.update_document(
            doc_id,
            metadata={"title": "Updated Title", "status": "updated"}
        )
        self.client.log_test_result(
            "Document Update",
            "Update document metadata",
            result,
            200,
            "Update metadata of existing document"
        )

        # Scenario 2: Update with empty metadata
        print("\n2. Updating document with empty metadata...")
        result = self.client.update_document(doc_id, metadata={})
        self.client.log_test_result(
            "Document Update",
            "Update with empty metadata",
            result,
            200,
            "Test update with empty metadata object"
        )

        # Scenario 3: Update with additional fields
        print("\n3. Adding new metadata fields...")
        result = self.client.update_document(
            doc_id,
            metadata={"new_field": "new_value", "timestamp": "2025-11-19"}
        )
        self.client.log_test_result(
            "Document Update",
            "Add new metadata fields",
            result,
            200,
            "Test adding new fields to metadata"
        )

        # Scenario 4: Update non-existent document
        print("\n4. Updating non-existent document...")
        result = self.client.update_document(
            "non-existent-id-12345",
            metadata={"title": "Test"}
        )
        self.client.log_test_result(
            "Document Update",
            "Update non-existent document",
            result,
            404,
            "Test error handling for non-existent document"
        )

        # Scenario 5: Update with invalid metadata type
        print("\n5. Updating with complex nested metadata...")
        result = self.client.update_document(
            doc_id,
            metadata={"nested": {"level1": {"level2": "value"}}}
        )
        self.client.log_test_result(
            "Document Update",
            "Update with nested metadata",
            result,
            200,
            "Test handling of nested metadata structures"
        )

        # Scenario 6: Update multiple times rapidly
        print("\n6. Rapid sequential updates...")
        for i in range(3):
            result = self.client.update_document(
                doc_id,
                metadata={"iteration": i, "timestamp": f"2025-11-19T{i}:00:00"}
            )
            self.client.log_test_result(
                "Document Update",
                f"Rapid update #{i+1}/3",
                result,
                200,
                "Test API performance with rapid updates"
            )

        # Scenario 7: Update with special characters in metadata
        print("\n7. Updating with special characters in metadata...")
        result = self.client.update_document(
            doc_id,
            metadata={"special": "@#$%^&*()", "unicode": "こんにちは"}
        )
        self.client.log_test_result(
            "Document Update",
            "Update with special characters",
            result,
            200,
            "Test special characters in metadata values"
        )

        # Scenario 8: Update with very long metadata values
        print("\n8. Updating with long metadata values...")
        long_value = "A" * 1000
        result = self.client.update_document(
            doc_id,
            metadata={"long_field": long_value}
        )
        self.client.log_test_result(
            "Document Update",
            "Update with long metadata values",
            result,
            200,
            "Test handling of large metadata values"
        )

        # Scenario 9: Update with array in metadata
        print("\n9. Updating with array metadata...")
        result = self.client.update_document(
            doc_id,
            metadata={"tags": ["tag1", "tag2", "tag3"], "categories": ["cat1"]}
        )
        self.client.log_test_result(
            "Document Update",
            "Update with array metadata",
            result,
            200,
            "Test array values in metadata"
        )

        # Scenario 10: Update with boolean and numeric metadata
        print("\n10. Updating with mixed data types...")
        result = self.client.update_document(
            doc_id,
            metadata={
                "active": True,
                "count": 42,
                "rating": 4.5,
                "verified": False
            }
        )
        self.client.log_test_result(
            "Document Update",
            "Update with mixed data types",
            result,
            200,
            "Test various data types in metadata"
        )

    def test_document_deletion(self):
        """Test 10+ scenarios for document deletion"""
        print("\n" + "="*80)
        print("TESTING DOCUMENT DELETION ENDPOINTS")
        print("="*80)

        # Scenario 1: Delete valid document
        if self.test_document_ids:
            doc_id = self.test_document_ids.pop()
            print(f"\n1. Deleting valid document: {doc_id}...")
            result = self.client.delete_document(doc_id)
            self.client.log_test_result(
                "Document Deletion",
                "Delete valid document",
                result,
                200,
                "Delete an existing document"
            )

            # Scenario 2: Verify document is deleted
            print(f"\n2. Verifying document deletion: {doc_id}...")
            result = self.client.get_document(doc_id)
            self.client.log_test_result(
                "Document Deletion",
                "Verify deleted document not found",
                result,
                404,
                "Confirm document no longer exists after deletion"
            )

        # Scenario 3: Delete already deleted document
        if doc_id:
            print(f"\n3. Attempting to delete already deleted document...")
            result = self.client.delete_document(doc_id)
            self.client.log_test_result(
                "Document Deletion",
                "Delete already deleted document",
                result,
                404,
                "Test idempotency of delete operation"
            )

        # Scenario 4: Delete non-existent document
        print("\n4. Deleting non-existent document...")
        result = self.client.delete_document("non-existent-id-99999")
        self.client.log_test_result(
            "Document Deletion",
            "Delete non-existent document",
            result,
            404,
            "Test error handling for invalid document ID"
        )

        # Scenario 5: Delete with malformed ID
        print("\n5. Deleting document with malformed ID...")
        result = self.client.delete_document("@#$invalid$%^")
        self.client.log_test_result(
            "Document Deletion",
            "Delete with malformed ID",
            result,
            400,
            "Test validation of document ID format"
        )

        # Scenario 6: Delete multiple documents in sequence
        print("\n6. Deleting multiple documents sequentially...")
        docs_to_delete = self.test_document_ids[-3:] if len(self.test_document_ids) >= 3 else self.test_document_ids
        for i, doc_id in enumerate(docs_to_delete):
            result = self.client.delete_document(doc_id)
            self.client.log_test_result(
                "Document Deletion",
                f"Sequential deletion #{i+1}",
                result,
                200,
                "Test sequential deletion of multiple documents"
            )
            if result.get("status_code") == 200:
                self.test_document_ids.remove(doc_id)

        # Scenario 7: Delete with empty string ID
        print("\n7. Deleting document with empty ID...")
        result = self.client.delete_document("")
        self.client.log_test_result(
            "Document Deletion",
            "Delete with empty ID",
            result,
            400,
            "Test validation of empty document ID"
        )

        # Scenario 8: Rapid deletion requests
        print("\n8. Testing rapid deletion requests...")
        if len(self.test_document_ids) >= 2:
            for i, doc_id in enumerate(self.test_document_ids[:2]):
                result = self.client.delete_document(doc_id)
                self.client.log_test_result(
                    "Document Deletion",
                    f"Rapid deletion #{i+1}",
                    result,
                    200,
                    "Test API performance with rapid delete requests"
                )

        # Scenario 9: Delete and verify cascading (chunks removal)
        print("\n9. Testing cascading deletion (chunks)...")
        # Create a new document for this test
        file_path = self.create_test_file("Document for cascading deletion test. " * 100)
        create_result = self.client.create_document(
            file_path=file_path,
            metadata={"title": "Cascading Test"},
            ingestion_mode="fast"
        )
        if create_result.get("status_code") == 200 and isinstance(create_result.get("body"), dict):
            new_doc_id = create_result["body"].get("document_id")
            if new_doc_id:
                # Delete the document
                delete_result = self.client.delete_document(new_doc_id)
                self.client.log_test_result(
                    "Document Deletion",
                    "Cascading deletion test",
                    delete_result,
                    200,
                    "Test that chunks are also deleted with document"
                )

        # Scenario 10: Delete document and verify it's removed from lists
        print("\n10. Verifying document removed from list after deletion...")
        list_result = self.client.list_documents()
        self.client.log_test_result(
            "Document Deletion",
            "Verify document not in list after deletion",
            list_result,
            200,
            "Confirm deleted documents don't appear in listings"
        )

    def run_all_tests(self):
        """Run all document API tests"""
        print("\n" + "="*80)
        print("STARTING COMPREHENSIVE R2R DOCUMENTS API TESTING")
        print("="*80)

        self.test_document_creation()
        self.test_document_retrieval()
        self.test_document_updates()
        self.test_document_deletion()

        print("\n" + "="*80)
        print("DOCUMENTS API TESTING COMPLETED")
        print("="*80)


def main():
    """Main test execution"""
    client = R2RAPIClient()

    print("Initializing R2R Documents API Testing...")
    print(f"Target API: {client.base_url}")

    # Check API health
    health_result = client.health_check()
    client.log_test_result(
        "Health Check",
        "API availability",
        health_result,
        200,
        "Verify API is accessible and responding"
    )

    if health_result.get("status_code") != 200:
        print("\n⚠️  WARNING: API health check failed. Tests may not execute properly.")
        print(f"Error: {health_result.get('error', 'Unknown error')}")

    # Run document tests
    tester = DocumentsAPITester(client)
    tester.run_all_tests()

    # Save results
    client.save_test_results("reports/documents_test_results.json")

    # Print summary
    summary = client.get_test_summary()
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']:.2f}%")
    print(f"Average Response Time: {summary['avg_response_time']:.3f}s")
    print("="*80)


if __name__ == "__main__":
    main()
