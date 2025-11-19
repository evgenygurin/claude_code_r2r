#!/usr/bin/env python3
"""
R2R API Login Testing

Tests for user authentication and API access.
"""

import requests
import json
import sys
from typing import Optional, Dict, Any
from dataclasses import dataclass
import time

# Configuration
API_BASE_URL = "http://localhost:7272"
API_REMOTE_URL = "http://136.119.36.216:7272"  # Direct access via GCP IP
DEFAULT_USERNAME = "admin@example.com"
DEFAULT_PASSWORD = "change_me_immediately"
REQUEST_TIMEOUT = 10


@dataclass
class TestResult:
    """Test result data class"""
    name: str
    passed: bool
    message: str
    duration: float = 0.0


class R2RAPITester:
    """R2R API Testing Client"""

    def __init__(self, base_url: Optional[str] = None, timeout: int = REQUEST_TIMEOUT,
                 use_remote: bool = False):
        # Auto-detect best available URL
        if base_url is None:
            if use_remote:
                self.base_url = API_REMOTE_URL
            else:
                # Try localhost first, fall back to remote
                try:
                    response = requests.head(API_BASE_URL, timeout=2)
                    self.base_url = API_BASE_URL
                except:
                    self.base_url = API_REMOTE_URL
        else:
            self.base_url = base_url

        self.base_url = self.base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        # Disable proxy for remote URL to bypass environment proxy settings
        if self.base_url == API_REMOTE_URL:
            self.session.trust_env = False
            # Explicitly set no proxies
            self.session.proxies = {}
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.results = []

    def add_result(self, result: TestResult):
        """Add test result"""
        self.results.append(result)

    def print_results(self):
        """Print test results summary"""
        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)

        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{status} | {result.name:30} | {result.duration:.2f}s")
            if not result.passed and result.message:
                print(f"       └─ {result.message}")

        print("="*60)
        print(f"Summary: {passed}/{total} tests passed")
        print("="*60)

        return passed == total

    def test_health(self) -> bool:
        """Test API health endpoint"""
        start = time.time()
        try:
            response = self.session.get(
                f"{self.base_url}/v3/health",
                timeout=self.timeout
            )
            duration = time.time() - start

            if response.status_code == 200:
                self.add_result(TestResult(
                    name="Health Check",
                    passed=True,
                    message="API is healthy",
                    duration=duration
                ))
                return True
            else:
                self.add_result(TestResult(
                    name="Health Check",
                    passed=False,
                    message=f"Status code: {response.status_code}",
                    duration=duration
                ))
                return False
        except Exception as e:
            duration = time.time() - start
            self.add_result(TestResult(
                name="Health Check",
                passed=False,
                message=f"Exception: {str(e)}",
                duration=duration
            ))
            return False

    def test_login(self, username: str = DEFAULT_USERNAME,
                   password: str = DEFAULT_PASSWORD) -> bool:
        """Test user login"""
        start = time.time()
        try:
            data = {
                "username": username,
                "password": password
            }

            response = self.session.post(
                f"{self.base_url}/v3/users/login",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self.timeout
            )
            duration = time.time() - start

            if response.status_code == 200:
                resp_data = response.json()

                # Extract tokens
                access_token = resp_data.get("results", {}).get("access_token", {}).get("token")
                refresh_token = resp_data.get("results", {}).get("refresh_token", {}).get("token")

                if access_token and refresh_token:
                    self.access_token = access_token
                    self.refresh_token = refresh_token

                    self.add_result(TestResult(
                        name="User Login",
                        passed=True,
                        message=f"Token length: {len(access_token)} chars",
                        duration=duration
                    ))
                    return True
                else:
                    self.add_result(TestResult(
                        name="User Login",
                        passed=False,
                        message="Tokens missing in response",
                        duration=duration
                    ))
                    return False
            else:
                self.add_result(TestResult(
                    name="User Login",
                    passed=False,
                    message=f"Status code: {response.status_code} - {response.text[:100]}",
                    duration=duration
                ))
                return False
        except Exception as e:
            duration = time.time() - start
            self.add_result(TestResult(
                name="User Login",
                passed=False,
                message=f"Exception: {str(e)}",
                duration=duration
            ))
            return False

    def test_get_user_info(self) -> bool:
        """Test getting current user info"""
        if not self.access_token:
            self.add_result(TestResult(
                name="Get User Info",
                passed=False,
                message="No access token available",
                duration=0
            ))
            return False

        start = time.time()
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            response = self.session.get(
                f"{self.base_url}/v3/users/me",
                headers=headers,
                timeout=self.timeout
            )
            duration = time.time() - start

            if response.status_code == 200:
                resp_data = response.json()
                email = resp_data.get("results", {}).get("email")

                self.add_result(TestResult(
                    name="Get User Info",
                    passed=True,
                    message=f"User: {email}",
                    duration=duration
                ))
                return True
            else:
                self.add_result(TestResult(
                    name="Get User Info",
                    passed=False,
                    message=f"Status code: {response.status_code}",
                    duration=duration
                ))
                return False
        except Exception as e:
            duration = time.time() - start
            self.add_result(TestResult(
                name="Get User Info",
                passed=False,
                message=f"Exception: {str(e)}",
                duration=duration
            ))
            return False

    def test_list_collections(self) -> bool:
        """Test listing collections"""
        if not self.access_token:
            self.add_result(TestResult(
                name="List Collections",
                passed=False,
                message="No access token available",
                duration=0
            ))
            return False

        start = time.time()
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            response = self.session.get(
                f"{self.base_url}/v3/collections",
                headers=headers,
                timeout=self.timeout
            )
            duration = time.time() - start

            if response.status_code == 200:
                resp_data = response.json()
                collections = resp_data.get("results", [])

                if isinstance(collections, list):
                    self.add_result(TestResult(
                        name="List Collections",
                        passed=True,
                        message=f"Found {len(collections)} collection(s)",
                        duration=duration
                    ))
                    return True
                else:
                    self.add_result(TestResult(
                        name="List Collections",
                        passed=False,
                        message="Invalid response format",
                        duration=duration
                    ))
                    return False
            else:
                self.add_result(TestResult(
                    name="List Collections",
                    passed=False,
                    message=f"Status code: {response.status_code}",
                    duration=duration
                ))
                return False
        except Exception as e:
            duration = time.time() - start
            self.add_result(TestResult(
                name="List Collections",
                passed=False,
                message=f"Exception: {str(e)}",
                duration=duration
            ))
            return False

    def test_search(self, query: str = "test") -> bool:
        """Test document search"""
        if not self.access_token:
            self.add_result(TestResult(
                name="Search Documents",
                passed=False,
                message="No access token available",
                duration=0
            ))
            return False

        start = time.time()
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

            data = {
                "query": query,
                "limit": 5
            }

            response = self.session.post(
                f"{self.base_url}/v3/retrieval/search",
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            duration = time.time() - start

            if response.status_code == 200:
                self.add_result(TestResult(
                    name="Search Documents",
                    passed=True,
                    message=f"Query: '{query}' - Status: {response.status_code}",
                    duration=duration
                ))
                return True
            else:
                self.add_result(TestResult(
                    name="Search Documents",
                    passed=False,
                    message=f"Status code: {response.status_code}",
                    duration=duration
                ))
                return False
        except Exception as e:
            duration = time.time() - start
            self.add_result(TestResult(
                name="Search Documents",
                passed=False,
                message=f"Exception: {str(e)}",
                duration=duration
            ))
            return False

    def run_all_tests(self) -> bool:
        """Run all tests"""
        print(f"\nRunning R2R API tests against {self.base_url}...\n")

        # Test sequence
        tests = [
            ("Health Check", lambda: self.test_health()),
            ("Login", lambda: self.test_login()),
            ("Get User Info", lambda: self.test_get_user_info()),
            ("List Collections", lambda: self.test_list_collections()),
            ("Search", lambda: self.test_search()),
        ]

        for name, test_func in tests:
            print(f"Running: {name}...", end=" ", flush=True)
            success = test_func()
            print("✅" if success else "❌")

        # Print summary
        return self.print_results()


def main():
    """Main entry point"""
    print("R2R API Testing Tool")
    print("=" * 60)

    # Check for --use-remote flag
    use_remote = "--use-remote" in sys.argv or "--remote" in sys.argv

    # Get custom URL if provided
    custom_url = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg.startswith("--url="):
            custom_url = arg.split("=", 1)[1]

    tester = R2RAPITester(base_url=custom_url, use_remote=use_remote)
    print(f"Testing against: {tester.base_url}\n")

    success = tester.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
