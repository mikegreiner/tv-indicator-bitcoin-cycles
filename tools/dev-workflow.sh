#!/bin/bash

# Bitcoin Cycles Development Workflow Script
# Speeds up the development process with automated checks

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
INDICATOR_FILE="bitcoin-cycles-indicator.pine"
VALIDATOR="cycle-logic-validator.py"

echo -e "${GREEN}🚀 Bitcoin Cycles Development Workflow${NC}"
echo "========================================"

# Function to check if files exist
check_files() {
    echo -e "\n📁 Checking files..."
    if [ ! -f "$INDICATOR_FILE" ]; then
        echo -e "${RED}❌ Main indicator file not found: $INDICATOR_FILE${NC}"
        exit 1
    fi

    if [ ! -f "pine-syntax-checker.py" ]; then
        echo -e "${RED}❌ Syntax checker not found${NC}"
        exit 1
    fi

    if [ ! -f "$VALIDATOR" ]; then
        echo -e "${YELLOW}⚠️  Logic validator not found - run: python3 cycle-logic-validator.py${NC}"
    fi

    echo -e "${GREEN}✅ All required files present${NC}"
}

# Function to run syntax check
syntax_check() {
    echo -e "\n🔍 Running syntax check..."
    if python3 pine-syntax-checker.py "$INDICATOR_FILE"; then
        echo -e "${GREEN}✅ Syntax check passed${NC}"
        return 0
    else
        echo -e "${RED}❌ Syntax check failed${NC}"
        return 1
    fi
}

# Function to run logic validation
logic_check() {
    if [ -f "$VALIDATOR" ]; then
        echo -e "\n🧪 Running logic validation..."
        if python3 "$VALIDATOR"; then
            echo -e "${GREEN}✅ Logic validation passed${NC}"
            return 0
        else
            echo -e "${RED}❌ Logic validation failed${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  Skipping logic validation (validator not found)${NC}"
        return 0
    fi
}

# Function to check for uncommitted changes
git_check() {
    if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "\n📝 Checking git status..."
        if git diff --quiet --exit-code; then
            echo -e "${GREEN}✅ No uncommitted changes${NC}"
        else
            echo -e "${YELLOW}⚠️  You have uncommitted changes${NC}"
            echo "   Consider committing: git add . && git commit -m 'Your changes'"
        fi
    else
        echo -e "${YELLOW}⚠️  Git not available or not a git repository${NC}"
    fi
}

# Function to show next steps
show_next_steps() {
    echo -e "\n🎯 Next Steps:"
    echo "1. Make your code changes to $INDICATOR_FILE"
    echo "2. Run this script: ./dev-workflow.sh"
    echo "3. If checks pass, copy code to TradingView"
    echo "4. Test visually in TradingView"
    echo "5. Iterate as needed"
}

# Function to show development tips
show_tips() {
    echo -e "\n💡 Development Tips:"
    echo "• Make small, incremental changes"
    echo "• Test each change individually"
    echo "• Use TradingView's 'Add to Chart' for quick testing"
    echo "• Keep backup versions of working code"
    echo "• Document your changes as you go"
}

# Main workflow
main() {
    check_files

    local syntax_ok=0
    local logic_ok=0

    if syntax_check; then
        syntax_ok=1
    fi

    if logic_check; then
        logic_ok=1
    fi

    git_check
    show_next_steps
    show_tips

    echo -e "\n========================================"
    if [ $syntax_ok -eq 1 ] && [ $logic_ok -eq 1 ]; then
        echo -e "${GREEN}🎉 Ready for TradingView testing!${NC}"
        echo "   Copy your code and test in TradingView"
    else
        echo -e "${RED}⚠️  Fix issues before TradingView testing${NC}"
    fi
}

# Help function
show_help() {
    echo "Bitcoin Cycles Development Workflow"
    echo ""
    echo "This script helps speed up development by running automated checks."
    echo ""
    echo "Usage:"
    echo "  ./dev-workflow.sh          # Run full development workflow"
    echo "  ./dev-workflow.sh --help   # Show this help"
    echo ""
    echo "Checks performed:"
    echo "  ✅ File existence validation"
    echo "  ✅ Pine Script syntax checking"
    echo "  ✅ Logic validation (if available)"
    echo "  ✅ Git status checking"
    echo ""
    echo "Requirements:"
    echo "  - Python 3 for syntax checking"
    echo "  - bitcoin-cycles-indicator.pine in current directory"
    echo "  - pine-syntax-checker.py in current directory"
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    *)
        main
        ;;
esac