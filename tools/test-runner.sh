#!/bin/bash

# Pine Script Test Runner
# Helps run local tests and validation before committing changes

set -e  # Exit on any error

echo "🐍 Pine Script Test Runner"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3 to run syntax checks.${NC}"
    exit 1
fi

# Function to run syntax check
run_syntax_check() {
    local file="$1"
    local name="$2"

    echo -e "\n📄 Checking $name..."
    if python3 pine-syntax-checker.py "$file"; then
        echo -e "${GREEN}✅ $name syntax OK${NC}"
        return 0
    else
        echo -e "${RED}❌ $name syntax FAILED${NC}"
        return 1
    fi
}

# Function to check file exists and is readable
check_file() {
    local file="$1"
    local name="$2"

    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ $name not found: $file${NC}"
        return 1
    fi

    if [ ! -r "$file" ]; then
        echo -e "${RED}❌ $name not readable: $file${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ $name found: $file${NC}"
    return 0
}

# Main test suite
main() {
    local failed_tests=0

    echo "🔍 Running pre-commit tests..."
    echo

    # Check main files exist
    check_file "bitcoin-cycles-indicator.pine" "Main Indicator" || ((failed_tests++))
    check_file "bitcoin-cycles-test-framework.pine" "Test Framework" || ((failed_tests++))
    check_file "bitcoin-cycles-validation-strategy.pine" "Validation Strategy" || ((failed_tests++))
    check_file "bitcoin-cycles-visual-verification.pine" "Visual Verification" || ((failed_tests++))
    check_file "bitcoin-cycles-testing-guide.md" "Testing Guide" || ((failed_tests++))
    check_file "pine-syntax-checker.py" "Syntax Checker" || ((failed_tests++))

    # Run syntax checks
    if [ -f "pine-syntax-checker.py" ]; then
        run_syntax_check "bitcoin-cycles-indicator.pine" "Main Indicator" || ((failed_tests++))
        run_syntax_check "bitcoin-cycles-test-framework.pine" "Test Framework" || ((failed_tests++))
        run_syntax_check "bitcoin-cycles-validation-strategy.pine" "Validation Strategy" || ((failed_tests++))
        run_syntax_check "bitcoin-cycles-visual-verification.pine" "Visual Verification" || ((failed_tests++))
    else
        echo -e "${YELLOW}⚠️  Syntax checker not found, skipping syntax validation${NC}"
    fi

    # Check for uncommitted changes
    if git diff --quiet --exit-code; then
        echo -e "\n${GREEN}✅ No uncommitted changes in working directory${NC}"
    else
        echo -e "\n${YELLOW}⚠️  Uncommitted changes detected${NC}"
        echo "   Consider committing your changes:"
        echo "   git add ."
        echo "   git commit -m 'Your commit message'"
    fi

    # Summary
    echo
    echo "=========================="
    if [ $failed_tests -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed! Ready for commit.${NC}"
        echo
        echo "Next steps:"
        echo "1. Commit your changes: git commit -m 'Your message'"
        echo "2. Push to remote: git push"
        echo "3. Test in TradingView with the test framework"
        exit 0
    else
        echo -e "${RED}❌ $failed_tests test(s) failed. Please fix before committing.${NC}"
        exit 1
    fi
}

# Show usage if requested
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Pine Script Test Runner"
    echo
    echo "This script runs local validation tests before committing changes."
    echo
    echo "Usage:"
    echo "  ./test-runner.sh          # Run all tests"
    echo "  ./test-runner.sh --help   # Show this help"
    echo
    echo "Tests performed:"
    echo "  ✅ File existence checks"
    echo "  ✅ Basic syntax validation"
    echo "  ✅ Git status check"
    echo
    echo "Requirements:"
    echo "  - Python 3 for syntax checking"
    echo "  - All Pine Script files in current directory"
    echo "  - Git repository initialized"
    exit 0
fi

# Run main tests
main