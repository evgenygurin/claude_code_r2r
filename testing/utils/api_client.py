"""
R2R API Testing Client
Provides comprehensive testing capabilities for R2R API endpoints
"""

import requests
import json
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class R2RAPIClient:
    """Client for testing R2R API endpoints"""

    def __init__(self, config_path: str = "configs/api_config.json"):
        """Initialize the API client with configuration"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.base_url = self.config['api_base_url']
        self.api_version = self.config['api_version']
        self.timeout = self.config['timeout']
        self.retry_attempts = self.config['retry_attempts']
        self.endpoints = self.config['endpoints']
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = []

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        retry: int = 0
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}{endpoint}"

        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if self.auth_token:
            default_headers["Authorization"] = f"Bearer {self.auth_token}"

        if headers:
            default_headers.update(headers)

        # Remove Content-Type for file uploads
        if files:
            default_headers.pop("Content-Type", None)

        try:
            start_time = time.time()

            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    params=params,
                    headers=default_headers,
                    timeout=self.timeout
                )
            elif method.upper() == "POST":
                if files:
                    response = self.session.post(
                        url,
                        data=data,
                        files=files,
                        headers=default_headers,
                        timeout=self.timeout
                    )
                else:
                    response = self.session.post(
                        url,
                        json=data,
                        headers=default_headers,
                        timeout=self.timeout
                    )
            elif method.upper() == "PUT":
                response = self.session.put(
                    url,
                    json=data,
                    headers=default_headers,
                    timeout=self.timeout
                )
            elif method.upper() == "DELETE":
                response = self.session.delete(
                    url,
                    headers=default_headers,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            elapsed_time = time.time() - start_time

            result = {
                "status_code": response.status_code,
                "response_time": elapsed_time,
                "headers": dict(response.headers),
                "url": url,
                "method": method.upper()
            }

            try:
                result["body"] = response.json()
            except:
                result["body"] = response.text

            return result

        except requests.exceptions.RequestException as e:
            if retry < self.retry_attempts:
                logger.warning(f"Request failed, retrying ({retry + 1}/{self.retry_attempts}): {e}")
                time.sleep(2 ** retry)  # Exponential backoff
                return self._make_request(method, endpoint, data, files, params, headers, retry + 1)
            else:
                return {
                    "status_code": 0,
                    "error": str(e),
                    "url": url,
                    "method": method.upper(),
                    "response_time": 0
                }

    def log_test_result(
        self,
        test_name: str,
        scenario: str,
        result: Dict[str, Any],
        expected_status: int,
        description: str = ""
    ):
        """Log test results for reporting"""
        success = result.get("status_code") == expected_status

        test_record = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "scenario": scenario,
            "description": description,
            "success": success,
            "expected_status": expected_status,
            "actual_status": result.get("status_code"),
            "response_time": result.get("response_time", 0),
            "url": result.get("url"),
            "method": result.get("method"),
            "error": result.get("error"),
            "response_body": result.get("body")
        }

        self.test_results.append(test_record)

        status_icon = "✓" if success else "✗"
        logger.info(f"{status_icon} {test_name} - {scenario}: {result.get('status_code')} ({result.get('response_time', 0):.2f}s)")

        return success

    def save_test_results(self, output_file: str):
        """Save test results to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        logger.info(f"Test results saved to {output_file}")

    def get_test_summary(self) -> Dict[str, Any]:
        """Generate test summary statistics"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for t in self.test_results if t['success'])
        failed_tests = total_tests - passed_tests
        avg_response_time = sum(t['response_time'] for t in self.test_results) / total_tests if total_tests > 0 else 0

        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "avg_response_time": avg_response_time
        }

    # Health Check
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        return self._make_request("GET", self.endpoints["health"])

    # Authentication
    def register_user(self, email: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        data = {"email": email, "password": password}
        return self._make_request("POST", self.endpoints["users_register"], data=data)

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user and get token"""
        data = {"email": email, "password": password}
        result = self._make_request("POST", self.endpoints["users_login"], data=data)

        if result.get("status_code") == 200 and isinstance(result.get("body"), dict):
            self.auth_token = result["body"].get("access_token")

        return result

    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        return self._make_request("GET", self.endpoints["users_profile"])

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh authentication token"""
        data = {"refresh_token": refresh_token}
        return self._make_request("POST", self.endpoints["users_refresh"], data=data)

    # Documents
    def create_document(
        self,
        file_path: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict] = None,
        ingestion_mode: str = "fast"
    ) -> Dict[str, Any]:
        """Create/upload a document"""
        if file_path:
            files = {"file": open(file_path, "rb")}
            data = {
                "metadata": json.dumps(metadata) if metadata else "{}",
                "ingestion_mode": ingestion_mode
            }
            result = self._make_request("POST", self.endpoints["documents_create"], data=data, files=files)
            files["file"].close()
            return result
        elif content:
            data = {
                "content": content,
                "metadata": metadata or {},
                "ingestion_mode": ingestion_mode
            }
            return self._make_request("POST", self.endpoints["documents_create"], data=data)
        else:
            raise ValueError("Either file_path or content must be provided")

    def list_documents(
        self,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """List all documents"""
        params = {"offset": offset, "limit": limit}
        if filters:
            params["filters"] = json.dumps(filters)
        return self._make_request("GET", self.endpoints["documents_list"], params=params)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document by ID"""
        endpoint = self.endpoints["documents_retrieve"].format(id=document_id)
        return self._make_request("GET", endpoint)

    def update_document(self, document_id: str, metadata: Dict) -> Dict[str, Any]:
        """Update document metadata"""
        endpoint = self.endpoints["documents_update"].format(id=document_id)
        return self._make_request("PUT", endpoint, data={"metadata": metadata})

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document"""
        endpoint = self.endpoints["documents_delete"].format(id=document_id)
        return self._make_request("DELETE", endpoint)

    def download_document(self, document_id: str) -> Dict[str, Any]:
        """Download document content"""
        endpoint = self.endpoints["documents_download"].format(id=document_id)
        return self._make_request("GET", endpoint)

    # Chunks
    def list_chunks(
        self,
        document_id: Optional[str] = None,
        offset: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """List document chunks"""
        params = {"offset": offset, "limit": limit}
        if document_id:
            params["document_id"] = document_id
        return self._make_request("GET", self.endpoints["chunks_list"], params=params)

    def get_chunk(self, chunk_id: str) -> Dict[str, Any]:
        """Get chunk by ID"""
        endpoint = self.endpoints["chunks_retrieve"].format(id=chunk_id)
        return self._make_request("GET", endpoint)

    # Search
    def search(
        self,
        query: str,
        search_settings: Optional[Dict] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Perform semantic/hybrid search"""
        data = {
            "query": query,
            "limit": limit
        }
        if search_settings:
            data["search_settings"] = search_settings

        return self._make_request("POST", self.endpoints["retrieval_search"], data=data)

    # RAG
    def rag_query(
        self,
        query: str,
        search_settings: Optional[Dict] = None,
        rag_generation_config: Optional[Dict] = None,
        task_prompt_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """Perform RAG query"""
        data = {"query": query}

        if search_settings:
            data["search_settings"] = search_settings
        if rag_generation_config:
            data["rag_generation_config"] = rag_generation_config
        if task_prompt_override:
            data["task_prompt_override"] = task_prompt_override

        return self._make_request("POST", self.endpoints["retrieval_rag"], data=data)

    # Collections
    def create_collection(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new collection"""
        data = {"name": name, "description": description}
        return self._make_request("POST", self.endpoints["collections_create"], data=data)

    def list_collections(self, offset: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List all collections"""
        params = {"offset": offset, "limit": limit}
        return self._make_request("GET", self.endpoints["collections_list"], params=params)

    def get_collection(self, collection_id: str) -> Dict[str, Any]:
        """Get collection by ID"""
        endpoint = self.endpoints["collections_retrieve"].format(id=collection_id)
        return self._make_request("GET", endpoint)

    def update_collection(self, collection_id: str, name: str = None, description: str = None) -> Dict[str, Any]:
        """Update collection"""
        endpoint = self.endpoints["collections_update"].format(id=collection_id)
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self._make_request("PUT", endpoint, data=data)

    def delete_collection(self, collection_id: str) -> Dict[str, Any]:
        """Delete a collection"""
        endpoint = self.endpoints["collections_delete"].format(id=collection_id)
        return self._make_request("DELETE", endpoint)

    # Graphs
    def create_graph(self, document_ids: List[str]) -> Dict[str, Any]:
        """Create knowledge graph from documents"""
        data = {"document_ids": document_ids}
        return self._make_request("POST", self.endpoints["graphs_create"], data=data)

    def get_graph(self, graph_id: str) -> Dict[str, Any]:
        """Get graph by ID"""
        endpoint = self.endpoints["graphs_retrieve"].format(id=graph_id)
        return self._make_request("GET", endpoint)

    def get_graph_entities(self, graph_id: str) -> Dict[str, Any]:
        """Get entities from graph"""
        endpoint = self.endpoints["graphs_entities"].format(id=graph_id)
        return self._make_request("GET", endpoint)

    def get_graph_relationships(self, graph_id: str) -> Dict[str, Any]:
        """Get relationships from graph"""
        endpoint = self.endpoints["graphs_relationships"].format(id=graph_id)
        return self._make_request("GET", endpoint)

    # System
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return self._make_request("GET", self.endpoints["system_status"])

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return self._make_request("GET", self.endpoints["system_stats"])
