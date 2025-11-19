"""
Comprehensive Tests for R2R Collections and Authentication API
Tests various scenarios for collections and auth endpoints
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.api_client import R2RAPIClient
import random
import string


class CollectionsAuthAPITester:
    """Test suite for Collections and Authentication API endpoints"""

    def __init__(self, client: R2RAPIClient):
        self.client = client
        self.test_collection_ids = []
        self.test_users = []

    def generate_random_email(self):
        """Generate random email for testing"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"test_{random_string}@example.com"

    def test_authentication_endpoints(self):
        """Test 10+ scenarios for authentication"""
        print("\n" + "="*80)
        print("TESTING AUTHENTICATION ENDPOINTS")
        print("="*80)

        # Scenario 1: Register new user
        print("\n1. Registering new user...")
        email = self.generate_random_email()
        password = "TestPassword123!"
        result = self.client.register_user(email, password)
        self.client.log_test_result(
            "Authentication",
            "Register new user",
            result,
            200,
            "Create new user account"
        )
        if result.get("status_code") == 200:
            self.test_users.append({"email": email, "password": password})

        # Scenario 2: Register with weak password
        print("\n2. Registering with weak password...")
        result = self.client.register_user(
            self.generate_random_email(),
            "weak"
        )
        self.client.log_test_result(
            "Authentication",
            "Register with weak password",
            result,
            400,
            "Test password validation"
        )

        # Scenario 3: Register with invalid email
        print("\n3. Registering with invalid email...")
        result = self.client.register_user(
            "invalid-email",
            "TestPassword123!"
        )
        self.client.log_test_result(
            "Authentication",
            "Register with invalid email",
            result,
            400,
            "Test email format validation"
        )

        # Scenario 4: Register duplicate user
        if self.test_users:
            print("\n4. Registering duplicate user...")
            user = self.test_users[0]
            result = self.client.register_user(user["email"], user["password"])
            self.client.log_test_result(
                "Authentication",
                "Register duplicate user",
                result,
                400,
                "Test duplicate email prevention"
            )

        # Scenario 5: Login with valid credentials
        if self.test_users:
            print("\n5. Login with valid credentials...")
            user = self.test_users[0]
            result = self.client.login_user(user["email"], user["password"])
            self.client.log_test_result(
                "Authentication",
                "Login with valid credentials",
                result,
                200,
                "Successful authentication"
            )

        # Scenario 6: Login with wrong password
        if self.test_users:
            print("\n6. Login with wrong password...")
            user = self.test_users[0]
            result = self.client.login_user(user["email"], "WrongPassword123!")
            self.client.log_test_result(
                "Authentication",
                "Login with wrong password",
                result,
                401,
                "Test authentication failure"
            )

        # Scenario 7: Login with non-existent user
        print("\n7. Login with non-existent user...")
        result = self.client.login_user(
            "nonexistent@example.com",
            "SomePassword123!"
        )
        self.client.log_test_result(
            "Authentication",
            "Login with non-existent user",
            result,
            401,
            "Test login for unknown user"
        )

        # Scenario 8: Get user profile (authenticated)
        if self.client.auth_token:
            print("\n8. Get user profile (authenticated)...")
            result = self.client.get_user_profile()
            self.client.log_test_result(
                "Authentication",
                "Get authenticated user profile",
                result,
                200,
                "Retrieve current user information"
            )

        # Scenario 9: Get user profile (unauthenticated)
        print("\n9. Get user profile without authentication...")
        old_token = self.client.auth_token
        self.client.auth_token = None
        result = self.client.get_user_profile()
        self.client.log_test_result(
            "Authentication",
            "Get profile without auth",
            result,
            401,
            "Test authentication requirement"
        )
        self.client.auth_token = old_token

        # Scenario 10: Login with empty credentials
        print("\n10. Login with empty credentials...")
        result = self.client.login_user("", "")
        self.client.log_test_result(
            "Authentication",
            "Login with empty credentials",
            result,
            400,
            "Test validation of empty inputs"
        )

        # Scenario 11: Register with special characters in email
        print("\n11. Registering with special characters in email...")
        result = self.client.register_user(
            "test+special@example.com",
            "TestPassword123!"
        )
        self.client.log_test_result(
            "Authentication",
            "Register with special chars in email",
            result,
            200,
            "Test valid special characters in email"
        )

        # Scenario 12: Register with very long password
        print("\n12. Registering with very long password...")
        long_password = "A" * 100 + "1!"
        result = self.client.register_user(
            self.generate_random_email(),
            long_password
        )
        self.client.log_test_result(
            "Authentication",
            "Register with long password",
            result,
            200,
            "Test password length handling"
        )

    def test_collections_endpoints(self):
        """Test 15+ scenarios for collections"""
        print("\n" + "="*80)
        print("TESTING COLLECTIONS ENDPOINTS")
        print("="*80)

        # Scenario 1: Create basic collection
        print("\n1. Creating basic collection...")
        result = self.client.create_collection(
            name="Test Collection",
            description="A test collection for API testing"
        )
        self.client.log_test_result(
            "Collections",
            "Create basic collection",
            result,
            200,
            "Create new document collection"
        )
        if result.get("status_code") == 200 and isinstance(result.get("body"), dict):
            coll_id = result["body"].get("collection_id")
            if coll_id:
                self.test_collection_ids.append(coll_id)

        # Scenario 2: Create collection with only name
        print("\n2. Creating collection with only name...")
        result = self.client.create_collection(name="Minimal Collection")
        self.client.log_test_result(
            "Collections",
            "Create collection without description",
            result,
            200,
            "Test minimal required fields"
        )

        # Scenario 3: Create collection with empty name
        print("\n3. Creating collection with empty name...")
        result = self.client.create_collection(name="", description="No name")
        self.client.log_test_result(
            "Collections",
            "Create collection with empty name",
            result,
            400,
            "Test name validation"
        )

        # Scenario 4: Create collection with long name
        print("\n4. Creating collection with long name...")
        long_name = "Collection " * 50
        result = self.client.create_collection(
            name=long_name,
            description="Long name test"
        )
        self.client.log_test_result(
            "Collections",
            "Create collection with long name",
            result,
            200,
            "Test name length handling"
        )

        # Scenario 5: Create collection with special characters
        print("\n5. Creating collection with special characters...")
        result = self.client.create_collection(
            name="Test @#$ Collection (特殊)",
            description="Special characters test"
        )
        self.client.log_test_result(
            "Collections",
            "Create collection with special chars",
            result,
            200,
            "Test special character support"
        )

        # Scenario 6: List all collections
        print("\n6. Listing all collections...")
        result = self.client.list_collections()
        self.client.log_test_result(
            "Collections",
            "List all collections",
            result,
            200,
            "Retrieve all collections"
        )

        # Scenario 7: List collections with pagination
        print("\n7. Listing collections with limit=2...")
        result = self.client.list_collections(limit=2)
        self.client.log_test_result(
            "Collections",
            "List collections with pagination",
            result,
            200,
            "Test pagination functionality"
        )

        # Scenario 8: List collections with offset
        print("\n8. Listing collections with offset=1, limit=3...")
        result = self.client.list_collections(offset=1, limit=3)
        self.client.log_test_result(
            "Collections",
            "List collections with offset",
            result,
            200,
            "Test offset pagination"
        )

        # Scenario 9: Get collection by ID
        if self.test_collection_ids:
            print(f"\n9. Retrieving collection by ID: {self.test_collection_ids[0]}...")
            result = self.client.get_collection(self.test_collection_ids[0])
            self.client.log_test_result(
                "Collections",
                "Get collection by valid ID",
                result,
                200,
                "Retrieve specific collection"
            )

        # Scenario 10: Get collection with invalid ID
        print("\n10. Retrieving collection with invalid ID...")
        result = self.client.get_collection("invalid-collection-id")
        self.client.log_test_result(
            "Collections",
            "Get collection with invalid ID",
            result,
            404,
            "Test error handling for invalid ID"
        )

        # Scenario 11: Update collection name
        if self.test_collection_ids:
            print("\n11. Updating collection name...")
            result = self.client.update_collection(
                self.test_collection_ids[0],
                name="Updated Collection Name"
            )
            self.client.log_test_result(
                "Collections",
                "Update collection name",
                result,
                200,
                "Modify collection name"
            )

        # Scenario 12: Update collection description
        if self.test_collection_ids:
            print("\n12. Updating collection description...")
            result = self.client.update_collection(
                self.test_collection_ids[0],
                description="Updated description for testing"
            )
            self.client.log_test_result(
                "Collections",
                "Update collection description",
                result,
                200,
                "Modify collection description"
            )

        # Scenario 13: Update both name and description
        if self.test_collection_ids:
            print("\n13. Updating both name and description...")
            result = self.client.update_collection(
                self.test_collection_ids[0],
                name="Fully Updated Collection",
                description="Both fields updated"
            )
            self.client.log_test_result(
                "Collections",
                "Update name and description",
                result,
                200,
                "Modify multiple fields"
            )

        # Scenario 14: Update non-existent collection
        print("\n14. Updating non-existent collection...")
        result = self.client.update_collection(
            "non-existent-id",
            name="Test"
        )
        self.client.log_test_result(
            "Collections",
            "Update non-existent collection",
            result,
            404,
            "Test error for missing collection"
        )

        # Scenario 15: Create multiple collections rapidly
        print("\n15. Creating multiple collections rapidly...")
        for i in range(3):
            result = self.client.create_collection(
                name=f"Rapid Test Collection {i+1}",
                description=f"Rapid creation test #{i+1}"
            )
            self.client.log_test_result(
                "Collections",
                f"Rapid creation #{i+1}/3",
                result,
                200,
                "Test API performance"
            )
            if result.get("status_code") == 200 and isinstance(result.get("body"), dict):
                coll_id = result["body"].get("collection_id")
                if coll_id:
                    self.test_collection_ids.append(coll_id)

        # Scenario 16: Delete collection
        if self.test_collection_ids:
            coll_id = self.test_collection_ids.pop()
            print(f"\n16. Deleting collection: {coll_id}...")
            result = self.client.delete_collection(coll_id)
            self.client.log_test_result(
                "Collections",
                "Delete collection",
                result,
                200,
                "Remove collection"
            )

        # Scenario 17: Delete already deleted collection
        if coll_id:
            print("\n17. Deleting already deleted collection...")
            result = self.client.delete_collection(coll_id)
            self.client.log_test_result(
                "Collections",
                "Delete already deleted collection",
                result,
                404,
                "Test idempotency of delete"
            )

        # Scenario 18: Delete non-existent collection
        print("\n18. Deleting non-existent collection...")
        result = self.client.delete_collection("non-existent-id-12345")
        self.client.log_test_result(
            "Collections",
            "Delete non-existent collection",
            result,
            404,
            "Test error handling"
        )

    def run_all_tests(self):
        """Run all collections and auth tests"""
        print("\n" + "="*80)
        print("STARTING COMPREHENSIVE R2R COLLECTIONS & AUTH API TESTING")
        print("="*80)

        self.test_authentication_endpoints()
        self.test_collections_endpoints()

        print("\n" + "="*80)
        print("COLLECTIONS & AUTH API TESTING COMPLETED")
        print("="*80)


def main():
    """Main test execution"""
    client = R2RAPIClient()

    print("Initializing R2R Collections & Auth API Testing...")
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
    tester = CollectionsAuthAPITester(client)
    tester.run_all_tests()

    # Save results
    client.save_test_results("reports/collections_auth_test_results.json")

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
