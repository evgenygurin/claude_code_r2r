"""
Comprehensive Tests for R2R Search and RAG API
Tests various scenarios for search and RAG endpoints
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.api_client import R2RAPIClient


class SearchRAGAPITester:
    """Test suite for Search and RAG API endpoints"""

    def __init__(self, client: R2RAPIClient):
        self.client = client

    def test_search_endpoints(self):
        """Test 15+ scenarios for search functionality"""
        print("\n" + "="*80)
        print("TESTING SEARCH ENDPOINTS")
        print("="*80)

        # Scenario 1: Basic semantic search
        print("\n1. Basic semantic search...")
        result = self.client.search(
            query="What is artificial intelligence?",
            limit=10
        )
        self.client.log_test_result(
            "Search",
            "Basic semantic search",
            result,
            200,
            "Simple semantic search with default settings"
        )

        # Scenario 2: Search with semantic search enabled
        print("\n2. Search with explicit semantic search settings...")
        result = self.client.search(
            query="machine learning algorithms",
            search_settings={
                "use_semantic_search": True,
                "chunk_settings": {
                    "index_measure": "l2_distance",
                    "limit": 5
                }
            }
        )
        self.client.log_test_result(
            "Search",
            "Semantic search with custom settings",
            result,
            200,
            "Test semantic search with specific configuration"
        )

        # Scenario 3: Hybrid search
        print("\n3. Hybrid search (semantic + full-text)...")
        result = self.client.search(
            query="deep learning neural networks",
            search_settings={
                "use_hybrid_search": True,
                "hybrid_settings": {
                    "full_text_weight": 1.0,
                    "semantic_weight": 5.0,
                    "full_text_limit": 200,
                    "rrf_k": 50
                }
            }
        )
        self.client.log_test_result(
            "Search",
            "Hybrid search (semantic + full-text)",
            result,
            200,
            "Test hybrid search combining multiple strategies"
        )

        # Scenario 4: Search with filters
        print("\n4. Search with metadata filters...")
        result = self.client.search(
            query="AI research",
            search_settings={
                "filters": {
                    "category": "AI",
                    "verified": True
                }
            },
            limit=10
        )
        self.client.log_test_result(
            "Search",
            "Search with metadata filters",
            result,
            200,
            "Test filtered search by metadata"
        )

        # Scenario 5: Search with different distance measures
        print("\n5. Search with cosine similarity...")
        result = self.client.search(
            query="natural language processing",
            search_settings={
                "chunk_settings": {
                    "index_measure": "cosine_distance",
                    "limit": 10
                }
            }
        )
        self.client.log_test_result(
            "Search",
            "Search with cosine similarity",
            result,
            200,
            "Test alternative distance measure"
        )

        # Scenario 6: Search with very short query
        print("\n6. Search with very short query...")
        result = self.client.search(query="AI", limit=5)
        self.client.log_test_result(
            "Search",
            "Search with short query (2 chars)",
            result,
            200,
            "Test handling of minimal query length"
        )

        # Scenario 7: Search with very long query
        print("\n7. Search with very long query...")
        long_query = "What are the implications of artificial intelligence and machine learning " * 20
        result = self.client.search(query=long_query, limit=5)
        self.client.log_test_result(
            "Search",
            "Search with very long query",
            result,
            200,
            "Test handling of extensive query text"
        )

        # Scenario 8: Search with empty query
        print("\n8. Search with empty query...")
        result = self.client.search(query="", limit=5)
        self.client.log_test_result(
            "Search",
            "Search with empty query",
            result,
            400,
            "Test validation of empty query"
        )

        # Scenario 9: Search with special characters
        print("\n9. Search with special characters...")
        result = self.client.search(
            query="What is AI? (Deep Learning & NLP)",
            limit=10
        )
        self.client.log_test_result(
            "Search",
            "Search with special characters",
            result,
            200,
            "Test handling of punctuation and special chars"
        )

        # Scenario 10: Search with Unicode characters
        print("\n10. Search with Unicode characters...")
        result = self.client.search(
            query="人工智能 и машинное обучение",
            limit=5
        )
        self.client.log_test_result(
            "Search",
            "Search with Unicode/multilingual query",
            result,
            200,
            "Test multilingual search capabilities"
        )

        # Scenario 11: Search with limit variations
        print("\n11. Search with limit=1...")
        result = self.client.search(query="neural networks", limit=1)
        self.client.log_test_result(
            "Search",
            "Search with limit=1",
            result,
            200,
            "Test minimal result limit"
        )

        # Scenario 12: Search with large limit
        print("\n12. Search with limit=100...")
        result = self.client.search(query="AI applications", limit=100)
        self.client.log_test_result(
            "Search",
            "Search with large limit (100)",
            result,
            200,
            "Test large result set retrieval"
        )

        # Scenario 13: Search with knowledge graph
        print("\n13. Search with knowledge graph enabled...")
        result = self.client.search(
            query="Who was Aristotle?",
            search_settings={
                "use_graph_search": True,
                "kg_search_type": "local"
            }
        )
        self.client.log_test_result(
            "Search",
            "Search with knowledge graph",
            result,
            200,
            "Test knowledge graph-enhanced search"
        )

        # Scenario 14: Search with custom probes and ef_search
        print("\n14. Search with advanced vector settings...")
        result = self.client.search(
            query="quantum computing",
            search_settings={
                "chunk_settings": {
                    "index_measure": "l2_distance",
                    "probes": 25,
                    "ef_search": 100,
                    "limit": 10
                }
            }
        )
        self.client.log_test_result(
            "Search",
            "Search with advanced vector settings",
            result,
            200,
            "Test fine-tuned vector search parameters"
        )

        # Scenario 15: Rapid sequential searches
        print("\n15. Rapid sequential searches...")
        queries = ["AI ethics", "machine learning", "deep learning", "neural networks"]
        for i, query in enumerate(queries):
            result = self.client.search(query=query, limit=5)
            self.client.log_test_result(
                "Search",
                f"Rapid search #{i+1}/4: '{query}'",
                result,
                200,
                "Test API performance under load"
            )

    def test_rag_endpoints(self):
        """Test 15+ scenarios for RAG functionality"""
        print("\n" + "="*80)
        print("TESTING RAG ENDPOINTS")
        print("="*80)

        # Scenario 1: Basic RAG query
        print("\n1. Basic RAG query...")
        result = self.client.rag_query(query="What is artificial intelligence?")
        self.client.log_test_result(
            "RAG",
            "Basic RAG query",
            result,
            200,
            "Simple RAG with default settings"
        )

        # Scenario 2: RAG with custom model
        print("\n2. RAG with custom model configuration...")
        result = self.client.rag_query(
            query="Explain machine learning",
            rag_generation_config={
                "model": "openai/gpt-4o-mini",
                "temperature": 0.7
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with custom model config",
            result,
            200,
            "Test RAG with specific LLM configuration"
        )

        # Scenario 3: RAG with hybrid search
        print("\n3. RAG with hybrid search...")
        result = self.client.rag_query(
            query="What are neural networks?",
            search_settings={
                "use_hybrid_search": True,
                "limit": 10
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with hybrid search",
            result,
            200,
            "Combine RAG with hybrid search strategy"
        )

        # Scenario 4: RAG with low temperature (deterministic)
        print("\n4. RAG with low temperature (deterministic)...")
        result = self.client.rag_query(
            query="Define deep learning",
            rag_generation_config={
                "temperature": 0.0
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with deterministic generation",
            result,
            200,
            "Test deterministic response generation"
        )

        # Scenario 5: RAG with high temperature (creative)
        print("\n5. RAG with high temperature (creative)...")
        result = self.client.rag_query(
            query="Describe AI applications",
            rag_generation_config={
                "temperature": 1.5
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with high creativity",
            result,
            200,
            "Test creative response generation"
        )

        # Scenario 6: RAG with custom prompt override
        print("\n6. RAG with custom prompt override...")
        custom_prompt = "You are a technical expert. Provide a detailed, technical answer."
        result = self.client.rag_query(
            query="How does backpropagation work?",
            task_prompt_override=custom_prompt
        )
        self.client.log_test_result(
            "RAG",
            "RAG with custom prompt",
            result,
            200,
            "Test custom system prompt functionality"
        )

        # Scenario 7: RAG with HyDE strategy
        print("\n7. RAG with HyDE (Hypothetical Document Embeddings)...")
        result = self.client.rag_query(
            query="What are transformer models?",
            search_settings={
                "search_strategy": "hyde",
                "limit": 10
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with HyDE strategy",
            result,
            200,
            "Test advanced HyDE retrieval strategy"
        )

        # Scenario 8: RAG with RAG-Fusion
        print("\n8. RAG with RAG-Fusion strategy...")
        result = self.client.rag_query(
            query="Explain convolutional neural networks",
            search_settings={
                "search_strategy": "rag_fusion",
                "limit": 20
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with RAG-Fusion strategy",
            result,
            200,
            "Test RAG-Fusion multi-query strategy"
        )

        # Scenario 9: RAG with knowledge graph
        print("\n9. RAG with knowledge graph search...")
        result = self.client.rag_query(
            query="Who invented the transistor?",
            search_settings={
                "use_graph_search": True,
                "kg_search_type": "local"
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with knowledge graph",
            result,
            200,
            "Test knowledge graph-enhanced RAG"
        )

        # Scenario 10: RAG with metadata filters
        print("\n10. RAG with metadata filters...")
        result = self.client.rag_query(
            query="AI research findings",
            search_settings={
                "filters": {"category": "research"},
                "limit": 5
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with filtered search",
            result,
            200,
            "Test RAG with metadata filtering"
        )

        # Scenario 11: RAG with very short query
        print("\n11. RAG with minimal query...")
        result = self.client.rag_query(query="AI?")
        self.client.log_test_result(
            "RAG",
            "RAG with minimal query",
            result,
            200,
            "Test RAG with very short input"
        )

        # Scenario 12: RAG with complex question
        print("\n12. RAG with complex multi-part question...")
        complex_query = """
        What is the difference between supervised and unsupervised learning,
        and how do they compare to reinforcement learning in terms of
        data requirements and practical applications?
        """
        result = self.client.rag_query(query=complex_query)
        self.client.log_test_result(
            "RAG",
            "RAG with complex question",
            result,
            200,
            "Test handling of complex multi-part questions"
        )

        # Scenario 13: RAG with empty query
        print("\n13. RAG with empty query...")
        result = self.client.rag_query(query="")
        self.client.log_test_result(
            "RAG",
            "RAG with empty query",
            result,
            400,
            "Test validation of empty query"
        )

        # Scenario 14: RAG with special characters
        print("\n14. RAG with special characters...")
        result = self.client.rag_query(
            query="What is AI/ML & DL? (Explain)",
        )
        self.client.log_test_result(
            "RAG",
            "RAG with special characters",
            result,
            200,
            "Test handling of special characters in query"
        )

        # Scenario 15: RAG with multilingual query
        print("\n15. RAG with multilingual query...")
        result = self.client.rag_query(
            query="¿Qué es inteligencia artificial?",
        )
        self.client.log_test_result(
            "RAG",
            "RAG with multilingual query",
            result,
            200,
            "Test multilingual RAG capabilities"
        )

        # Scenario 16: Rapid sequential RAG queries
        print("\n16. Rapid sequential RAG queries...")
        queries = [
            "What is machine learning?",
            "Explain deep learning",
            "Define neural networks"
        ]
        for i, query in enumerate(queries):
            result = self.client.rag_query(query=query)
            self.client.log_test_result(
                "RAG",
                f"Rapid RAG #{i+1}/3",
                result,
                200,
                "Test API performance under sequential load"
            )

        # Scenario 17: RAG with maximum context retrieval
        print("\n17. RAG with maximum context...")
        result = self.client.rag_query(
            query="Comprehensive overview of AI",
            search_settings={
                "limit": 50
            }
        )
        self.client.log_test_result(
            "RAG",
            "RAG with large context window",
            result,
            200,
            "Test RAG with maximum retrieved context"
        )

    def run_all_tests(self):
        """Run all search and RAG tests"""
        print("\n" + "="*80)
        print("STARTING COMPREHENSIVE R2R SEARCH & RAG API TESTING")
        print("="*80)

        self.test_search_endpoints()
        self.test_rag_endpoints()

        print("\n" + "="*80)
        print("SEARCH & RAG API TESTING COMPLETED")
        print("="*80)


def main():
    """Main test execution"""
    client = R2RAPIClient()

    print("Initializing R2R Search & RAG API Testing...")
    print(f"Target API: {client.base_url}")

    # Check API health
    health_result = client.health_check()
    client.log_test_result(
        "Health Check",
        "API availability",
        health_result,
        200,
        "Verify API is accessible"
    )

    if health_result.get("status_code") != 200:
        print("\n⚠️  WARNING: API health check failed.")
        print(f"Error: {health_result.get('error', 'Unknown error')}")

    # Run tests
    tester = SearchRAGAPITester(client)
    tester.run_all_tests()

    # Save results
    client.save_test_results("reports/search_rag_test_results.json")

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
