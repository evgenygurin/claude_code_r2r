"""
DEMO: Simulated test run showing how the framework would work
This demonstrates the testing framework with mock responses
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path

# Create reports directory
Path("reports").mkdir(exist_ok=True)

class MockR2RAPIClient:
    """Mock client simulating R2R API responses"""

    def __init__(self):
        self.test_results = []
        self.base_url = "http://136.119.36.216:7272"
        self.api_version = "v3"

    def _mock_response(self, success_rate=0.85, response_time_range=(0.05, 0.5)):
        """Generate mock response"""
        time.sleep(random.uniform(0.01, 0.05))  # Simulate network delay

        is_success = random.random() < success_rate
        status_code = 200 if is_success else random.choice([400, 404, 500])

        return {
            "status_code": status_code,
            "response_time": random.uniform(*response_time_range),
            "body": {"result": "success"} if is_success else {"error": "mock error"},
            "url": f"{self.base_url}/v3/endpoint",
            "method": "POST"
        }

    def log_test_result(self, test_name, scenario, result, expected_status, description):
        """Log test results"""
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
            "method": result.get("method")
        }

        self.test_results.append(test_record)

        status_icon = "✓" if success else "✗"
        status_color = "\033[92m" if success else "\033[91m"
        reset_color = "\033[0m"

        print(f"{status_color}{status_icon}{reset_color} {test_name} - {scenario}: {result.get('status_code')} ({result.get('response_time', 0):.3f}s)")

        return success

    def get_test_summary(self):
        """Generate test summary"""
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

    def save_test_results(self, filename):
        """Save results to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": self.get_test_summary(),
                "results": self.test_results
            }, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to {filename}")


def run_demo_tests():
    """Run demonstration tests"""
    print("\n" + "="*80)
    print("R2R API TESTING FRAMEWORK - DEMONSTRATION")
    print("="*80)
    print("\nNOTE: This is a SIMULATED test run showing framework capabilities")
    print("Real API at http://136.119.36.216:7272 is currently inaccessible (403 Forbidden)")
    print("="*80)

    client = MockR2RAPIClient()

    # Simulate different test categories
    test_categories = [
        {
            "name": "Health Check & System",
            "tests": [
                ("API Health Check", "Basic connectivity"),
                ("System Status", "Get system information"),
                ("System Stats", "Retrieve statistics"),
            ],
            "success_rate": 0.95
        },
        {
            "name": "Document Management",
            "tests": [
                ("Create document (fast mode)", "Simple text file"),
                ("Create document (hi-res mode)", "PDF with metadata"),
                ("List all documents", "No filters"),
                ("List documents with pagination", "limit=10, offset=0"),
                ("Get document by ID", "Valid document ID"),
                ("Get document by ID", "Invalid document ID"),
                ("Update document metadata", "Add new fields"),
                ("Update document metadata", "Complex nested structure"),
                ("Delete document", "Valid document ID"),
                ("Delete document", "Already deleted (idempotency)"),
            ],
            "success_rate": 0.90
        },
        {
            "name": "Search Operations",
            "tests": [
                ("Semantic search", "Basic query"),
                ("Semantic search", "With custom settings"),
                ("Hybrid search", "Semantic + full-text"),
                ("Hybrid search", "With filters"),
                ("Search with filters", "Metadata filtering"),
                ("Search with special chars", "Unicode query"),
                ("Search with short query", "2 characters"),
                ("Search with long query", "500+ words"),
                ("Search with empty query", "Validation test"),
                ("Knowledge graph search", "Entity-based"),
            ],
            "success_rate": 0.88
        },
        {
            "name": "RAG Generation",
            "tests": [
                ("Basic RAG query", "Simple question"),
                ("RAG with custom model", "GPT-4o-mini"),
                ("RAG with temperature=0", "Deterministic"),
                ("RAG with temperature=1.5", "Creative"),
                ("RAG with HyDE strategy", "Advanced retrieval"),
                ("RAG with RAG-Fusion", "Multi-query"),
                ("RAG with hybrid search", "Combined approach"),
                ("RAG with KG search", "Graph-enhanced"),
                ("RAG with filters", "Metadata filtering"),
                ("RAG with custom prompt", "System prompt override"),
            ],
            "success_rate": 0.85
        },
        {
            "name": "Collections Management",
            "tests": [
                ("Create collection", "Basic collection"),
                ("Create collection", "With long name"),
                ("List all collections", "No pagination"),
                ("List collections", "With limit=5"),
                ("Get collection by ID", "Valid ID"),
                ("Get collection by ID", "Invalid ID"),
                ("Update collection", "Name and description"),
                ("Delete collection", "Valid collection"),
            ],
            "success_rate": 0.92
        },
        {
            "name": "Authentication",
            "tests": [
                ("Register user", "Valid credentials"),
                ("Register user", "Weak password"),
                ("Register user", "Invalid email"),
                ("Login user", "Valid credentials"),
                ("Login user", "Wrong password"),
                ("Get user profile", "Authenticated"),
                ("Get user profile", "Unauthenticated"),
                ("Refresh token", "Valid refresh token"),
            ],
            "success_rate": 0.87
        }
    ]

    total_start = time.time()

    for category in test_categories:
        print(f"\n{'='*80}")
        print(f"TESTING: {category['name']}")
        print(f"{'='*80}\n")

        for i, (scenario, description) in enumerate(category['tests'], 1):
            # Simulate API call
            result = client._mock_response(
                success_rate=category['success_rate'],
                response_time_range=(0.05, 0.8)
            )

            # Expected status based on scenario
            if "Invalid" in scenario or "empty" in description or "Weak" in scenario:
                expected_status = 400
            elif "Already deleted" in scenario or "Unauthenticated" in scenario:
                expected_status = 404 if "deleted" in scenario else 401
            else:
                expected_status = 200

            client.log_test_result(
                test_name=category['name'],
                scenario=f"{i}. {scenario}",
                result=result,
                expected_status=expected_status,
                description=description
            )

            # Small delay between tests
            time.sleep(0.02)

    total_time = time.time() - total_start

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    summary = client.get_test_summary()

    # Group by category
    category_stats = {}
    for result in client.test_results:
        cat = result['test_name']
        if cat not in category_stats:
            category_stats[cat] = {'total': 0, 'passed': 0}
        category_stats[cat]['total'] += 1
        if result['success']:
            category_stats[cat]['passed'] += 1

    # Print category breakdown
    print("\nResults by Category:")
    print("-" * 80)
    for cat, stats in category_stats.items():
        success_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        status = "✓" if success_rate >= 80 else "!"
        print(f"  {status} {cat:30s}: {stats['passed']:3d}/{stats['total']:3d} passed ({success_rate:5.1f}%)")

    print("\n" + "-" * 80)
    print(f"Total Tests:          {summary['total_tests']}")
    print(f"Passed:               {summary['passed']} ✓")
    print(f"Failed:               {summary['failed']} ✗")
    print(f"Success Rate:         {summary['success_rate']:.2f}%")
    print(f"Avg Response Time:    {summary['avg_response_time']:.3f}s")
    print(f"Total Execution Time: {total_time:.2f}s")
    print("="*80)

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = f"reports/demo_test_results_{timestamp}.json"
    client.save_test_results(json_file)

    # Generate simple text report
    report_file = f"reports/demo_test_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("R2R API TESTING FRAMEWORK - DEMONSTRATION REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"API Endpoint: {client.base_url}\n")
        f.write(f"API Version: {client.api_version}\n\n")

        f.write("SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Tests:       {summary['total_tests']}\n")
        f.write(f"Passed:            {summary['passed']}\n")
        f.write(f"Failed:            {summary['failed']}\n")
        f.write(f"Success Rate:      {summary['success_rate']:.2f}%\n")
        f.write(f"Avg Response Time: {summary['avg_response_time']:.3f}s\n\n")

        f.write("RESULTS BY CATEGORY\n")
        f.write("-"*80 + "\n")
        for cat, stats in category_stats.items():
            success_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            f.write(f"{cat}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)\n")

        f.write("\n" + "="*80 + "\n")
        f.write("This was a SIMULATED test run.\n")
        f.write("Actual API access requires proper network configuration.\n")
        f.write("="*80 + "\n")

    print(f"✓ Text report saved to {report_file}")

    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nThe framework is ready to use when API access is available!")
    print(f"\nTo use with real API:")
    print(f"  1. Ensure network access to {client.base_url}")
    print(f"  2. Configure proper authentication (if required)")
    print(f"  3. Run: python run_all_tests.py")
    print("="*80 + "\n")

    return summary


if __name__ == "__main__":
    summary = run_demo_tests()

    # Exit code based on results
    exit_code = 0 if summary['success_rate'] >= 50 else 1
    exit(exit_code)
