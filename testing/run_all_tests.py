"""
Master Test Runner for R2R API
Executes all test suites and generates comprehensive reports
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add utils to path
sys.path.append(os.path.dirname(__file__))

from utils.api_client import R2RAPIClient
from tests.test_documents import DocumentsAPITester
from tests.test_search_rag import SearchRAGAPITester
from tests.test_collections_auth import CollectionsAuthAPITester


def print_banner(text, char="="):
    """Print formatted banner"""
    print("\n" + char * 80)
    print(text.center(80))
    print(char * 80)


def generate_html_report(client: R2RAPIClient, output_file: str):
    """Generate HTML report from test results"""
    summary = client.get_test_summary()
    results_by_category = {}

    # Group results by test name
    for result in client.test_results:
        test_name = result['test_name']
        if test_name not in results_by_category:
            results_by_category[test_name] = []
        results_by_category[test_name].append(result)

    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>R2R API Test Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
                padding: 10px;
                background-color: #ecf0f1;
                border-left: 4px solid #3498db;
            }}
            .summary {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .summary-card {{
                padding: 20px;
                border-radius: 6px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .summary-card h3 {{
                margin: 0 0 10px 0;
                font-size: 14px;
                color: #7f8c8d;
                text-transform: uppercase;
            }}
            .summary-card .value {{
                font-size: 32px;
                font-weight: bold;
                margin: 0;
            }}
            .total {{ background-color: #3498db; color: white; }}
            .passed {{ background-color: #2ecc71; color: white; }}
            .failed {{ background-color: #e74c3c; color: white; }}
            .success-rate {{ background-color: #9b59b6; color: white; }}
            .avg-time {{ background-color: #f39c12; color: white; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #34495e;
                color: white;
                font-weight: bold;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .status-success {{
                color: #2ecc71;
                font-weight: bold;
            }}
            .status-failed {{
                color: #e74c3c;
                font-weight: bold;
            }}
            .metadata {{
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 4px;
                margin: 20px 0;
            }}
            .metadata p {{
                margin: 5px 0;
                color: #34495e;
            }}
            .test-details {{
                font-size: 12px;
                color: #7f8c8d;
            }}
            .response-time {{
                color: #16a085;
                font-weight: bold;
            }}
            .category-stats {{
                margin: 15px 0;
                padding: 10px;
                background-color: #f8f9fa;
                border-left: 3px solid #3498db;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 R2R API Comprehensive Test Report</h1>

            <div class="metadata">
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>API Endpoint:</strong> {client.base_url}</p>
                <p><strong>API Version:</strong> {client.api_version}</p>
            </div>

            <h2>📈 Overall Summary</h2>
            <div class="summary">
                <div class="summary-card total">
                    <h3>Total Tests</h3>
                    <p class="value">{summary['total_tests']}</p>
                </div>
                <div class="summary-card passed">
                    <h3>Passed</h3>
                    <p class="value">{summary['passed']}</p>
                </div>
                <div class="summary-card failed">
                    <h3>Failed</h3>
                    <p class="value">{summary['failed']}</p>
                </div>
                <div class="summary-card success-rate">
                    <h3>Success Rate</h3>
                    <p class="value">{summary['success_rate']:.1f}%</p>
                </div>
                <div class="summary-card avg-time">
                    <h3>Avg Response</h3>
                    <p class="value">{summary['avg_response_time']:.2f}s</p>
                </div>
            </div>
    """

    # Add results by category
    for category, tests in results_by_category.items():
        passed = sum(1 for t in tests if t['success'])
        total = len(tests)
        success_rate = (passed / total * 100) if total > 0 else 0

        html += f"""
            <h2>🔍 {category}</h2>
            <div class="category-stats">
                <strong>Tests:</strong> {total} | <strong>Passed:</strong> {passed} |
                <strong>Failed:</strong> {total - passed} | <strong>Success Rate:</strong> {success_rate:.1f}%
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Scenario</th>
                        <th>Status</th>
                        <th>Expected</th>
                        <th>Actual</th>
                        <th>Response Time</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
        """

        for test in tests:
            status_class = "status-success" if test['success'] else "status-failed"
            status_icon = "✓" if test['success'] else "✗"

            html += f"""
                    <tr>
                        <td>{test['scenario']}</td>
                        <td class="{status_class}">{status_icon}</td>
                        <td>{test['expected_status']}</td>
                        <td>{test['actual_status']}</td>
                        <td class="response-time">{test['response_time']:.3f}s</td>
                        <td class="test-details">{test['description']}</td>
                    </tr>
            """

        html += """
                </tbody>
            </table>
        """

    html += """
        </div>
    </body>
    </html>
    """

    # Save HTML report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ HTML report generated: {output_file}")


def main():
    """Main test execution"""
    print_banner("R2R API COMPREHENSIVE TESTING SUITE", "=")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Initialize client
    client = R2RAPIClient()
    print(f"\nTarget API: {client.base_url}")
    print(f"API Version: {client.api_version}")

    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Health check
    print_banner("HEALTH CHECK", "-")
    health_result = client.health_check()
    client.log_test_result(
        "System Health",
        "API availability check",
        health_result,
        200,
        "Verify that the API is accessible and responding"
    )

    if health_result.get("status_code") != 200:
        print("\n⚠️  WARNING: API health check failed!")
        print(f"Error: {health_result.get('error', 'Unknown error')}")
        print("\nTests will continue but may encounter issues...")
    else:
        print("✓ API is healthy and accessible")

    # Run test suites
    print_banner("RUNNING TEST SUITES", "=")

    # 1. Documents API Tests
    print_banner("1. DOCUMENTS API TESTS", "-")
    try:
        docs_tester = DocumentsAPITester(client)
        docs_tester.run_all_tests()
        print("✓ Documents tests completed")
    except Exception as e:
        print(f"✗ Documents tests failed: {e}")

    # 2. Search & RAG API Tests
    print_banner("2. SEARCH & RAG API TESTS", "-")
    try:
        search_tester = SearchRAGAPITester(client)
        search_tester.run_all_tests()
        print("✓ Search & RAG tests completed")
    except Exception as e:
        print(f"✗ Search & RAG tests failed: {e}")

    # 3. Collections & Auth API Tests
    print_banner("3. COLLECTIONS & AUTH API TESTS", "-")
    try:
        coll_tester = CollectionsAuthAPITester(client)
        coll_tester.run_all_tests()
        print("✓ Collections & Auth tests completed")
    except Exception as e:
        print(f"✗ Collections & Auth tests failed: {e}")

    # Generate reports
    print_banner("GENERATING REPORTS", "=")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save JSON report
    json_report_path = reports_dir / f"r2r_api_test_results_{timestamp}.json"
    client.save_test_results(str(json_report_path))

    # Generate HTML report
    html_report_path = reports_dir / f"r2r_api_test_report_{timestamp}.html"
    generate_html_report(client, str(html_report_path))

    # Print final summary
    print_banner("FINAL TEST SUMMARY", "=")
    summary = client.get_test_summary()

    print(f"""
    Total Tests:         {summary['total_tests']}
    Passed:              {summary['passed']} ✓
    Failed:              {summary['failed']} ✗
    Success Rate:        {summary['success_rate']:.2f}%
    Avg Response Time:   {summary['avg_response_time']:.3f}s

    Reports Generated:
    - JSON: {json_report_path}
    - HTML: {html_report_path}
    """)

    print_banner(f"TESTING COMPLETED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "=")

    # Return exit code based on success rate
    return 0 if summary['success_rate'] >= 50 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
