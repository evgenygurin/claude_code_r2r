#!/bin/bash

# R2R API Quick Test
# Quick bash-based testing of R2R API endpoints
# Doesn't require Python, works with curl and jq

set -e

# Configuration
API_URL="${1:-http://localhost:7272}"
USERNAME="admin@example.com"
PASSWORD="change_me_immediately"
TIMEOUT=10

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================================${NC}"
}

print_test() {
    echo -e "${YELLOW}→ $1${NC}"
}

print_pass() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_fail() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check dependencies
check_deps() {
    local missing=0

    if ! command -v curl &> /dev/null; then
        print_fail "curl is required but not installed"
        missing=1
    fi

    if ! command -v jq &> /dev/null; then
        print_fail "jq is required but not installed"
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        exit 1
    fi
}

# Test health endpoint
test_health() {
    print_test "Health Check"

    RESPONSE=$(curl -s --max-time $TIMEOUT "$API_URL/v3/health" 2>&1) || {
        print_fail "Health check failed (connection error)"
        return 1
    }

    if echo "$RESPONSE" | jq . &>/dev/null; then
        print_pass "API is healthy"
        return 0
    else
        print_fail "Health check failed (invalid response): $RESPONSE"
        return 1
    fi
}

# Test login
test_login() {
    print_test "User Login"

    RESPONSE=$(curl -s --max-time $TIMEOUT \
        -X POST "$API_URL/v3/users/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$USERNAME&password=$PASSWORD" 2>&1) || {
        print_fail "Login failed (connection error)"
        return 1
    }

    ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.results.access_token.token' 2>/dev/null)

    if [ -n "$ACCESS_TOKEN" ] && [ "$ACCESS_TOKEN" != "null" ]; then
        TOKEN_PREVIEW="${ACCESS_TOKEN:0:30}..."
        print_pass "Login successful"
        print_info "Token: $TOKEN_PREVIEW"
        echo "$ACCESS_TOKEN" > /tmp/r2r_test_token.txt
        return 0
    else
        print_fail "Login failed: $RESPONSE"
        return 1
    fi
}

# Test get user info
test_user_info() {
    print_test "Get User Info"

    if [ ! -f /tmp/r2r_test_token.txt ]; then
        print_fail "No access token available (login first)"
        return 1
    fi

    TOKEN=$(cat /tmp/r2r_test_token.txt)

    RESPONSE=$(curl -s --max-time $TIMEOUT \
        -X GET "$API_URL/v3/users/me" \
        -H "Authorization: Bearer $TOKEN" 2>&1) || {
        print_fail "Get user info failed (connection error)"
        return 1
    }

    EMAIL=$(echo "$RESPONSE" | jq -r '.results.email' 2>/dev/null)

    if [ -n "$EMAIL" ] && [ "$EMAIL" != "null" ]; then
        print_pass "Retrieved user info"
        print_info "Email: $EMAIL"
        return 0
    else
        print_fail "Failed to get user info: $RESPONSE"
        return 1
    fi
}

# Test list collections
test_collections() {
    print_test "List Collections"

    if [ ! -f /tmp/r2r_test_token.txt ]; then
        print_fail "No access token available (login first)"
        return 1
    fi

    TOKEN=$(cat /tmp/r2r_test_token.txt)

    RESPONSE=$(curl -s --max-time $TIMEOUT \
        -X GET "$API_URL/v3/collections" \
        -H "Authorization: Bearer $TOKEN" 2>&1) || {
        print_fail "List collections failed (connection error)"
        return 1
    }

    COUNT=$(echo "$RESPONSE" | jq '.results | length' 2>/dev/null) || COUNT="0"

    if [ -n "$COUNT" ] && [ "$COUNT" != "null" ]; then
        print_pass "Listed collections"
        print_info "Found $COUNT collection(s)"
        return 0
    else
        print_fail "Failed to list collections: $RESPONSE"
        return 1
    fi
}

# Test search
test_search() {
    print_test "Search Documents"

    if [ ! -f /tmp/r2r_test_token.txt ]; then
        print_fail "No access token available (login first)"
        return 1
    fi

    TOKEN=$(cat /tmp/r2r_test_token.txt)

    RESPONSE=$(curl -s --max-time $TIMEOUT \
        -X POST "$API_URL/v3/retrieval/search" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"query":"test","limit":5}' 2>&1) || {
        print_fail "Search failed (connection error)"
        return 1
    }

    if echo "$RESPONSE" | jq . &>/dev/null; then
        print_pass "Search request successful"
        return 0
    else
        print_fail "Search failed: $RESPONSE"
        return 1
    fi
}

# Main test runner
run_tests() {
    check_deps

    print_header "R2R API Tests"
    echo ""
    print_info "Testing against: $API_URL"
    echo ""

    local passed=0
    local total=0

    # Run tests
    for test_func in test_health test_login test_user_info test_collections test_search; do
        ((total++))
        if $test_func; then
            ((passed++))
        fi
        echo ""
    done

    # Summary
    print_header "Test Summary"
    echo "Passed: $passed / $total"

    if [ $passed -eq $total ]; then
        print_pass "All tests passed!"
        rm -f /tmp/r2r_test_token.txt
        return 0
    else
        print_fail "Some tests failed"
        rm -f /tmp/r2r_test_token.txt
        return 1
    fi
}

# Display usage
usage() {
    cat << EOF
R2R API Quick Test

Usage: $0 [API_URL]

Arguments:
  API_URL          API endpoint URL (default: http://localhost:7272)

Examples:
  $0                                    # Test localhost tunnel
  $0 http://localhost:7272              # Explicit localhost
  $0 http://136.119.36.216:7272         # Direct IP (requires network access)

Requirements:
  - curl
  - jq

Environment:
  API_URL can also be set via environment variable:
    export API_URL=http://localhost:7272
    $0

Tests:
  1. Health Check     - Verify API is responding
  2. User Login       - Authenticate with default credentials
  3. Get User Info    - Retrieve user information
  4. List Collections - List document collections
  5. Search Documents - Test search functionality

EOF
}

# Main
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    usage
    exit 0
fi

run_tests
exit $?
