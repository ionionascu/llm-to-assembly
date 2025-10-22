#!/bin/bash
# Quick test runner for the calculator application

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Calculator Application - Quick Test Runner${NC}"
echo "================================================="

# Change to the tests directory
cd "$(dirname "$0")"

# Check if the calculator executable exists
if [ ! -f "../build/calculator" ]; then
    echo -e "${YELLOW}Calculator executable not found. Building...${NC}"
    make -C .. all
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to build calculator${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Running quick manual tests...${NC}"
echo

# Test 1: Basic positive addition
echo -e "${BLUE}Test 1: Basic positive addition (5 + 3)${NC}"
printf "5\n3\n" | ../build/calculator
echo

# Test 2: Negative numbers
echo -e "${BLUE}Test 2: Negative numbers (-10 + 7)${NC}"
printf "%s\n%s\n" "-10" "7" | ../build/calculator
echo

# Test 3: Both negative
echo -e "${BLUE}Test 3: Both negative (-5 + -3)${NC}"
printf "%s\n%s\n" "-5" "-3" | ../build/calculator
echo

# Test 4: Zero values
echo -e "${BLUE}Test 4: Zero values (0 + 0)${NC}"
printf "0\n0\n" | ../build/calculator
echo

# Test 5: Large numbers
echo -e "${BLUE}Test 5: Large numbers (1000000 + 2000000)${NC}"
printf "1000000\n2000000\n" | ../build/calculator
echo

# Test 6: Invalid input (should show error)
echo -e "${BLUE}Test 6: Invalid input (should show error)${NC}"
printf "abc\ndef\n" | ../build/calculator
echo

echo -e "${GREEN}Quick tests completed!${NC}"
echo
echo -e "${YELLOW}To run comprehensive tests with pytest:${NC}"
echo "python3 test_calculator.py"
echo
echo -e "${YELLOW}To install test dependencies:${NC}"
echo "pip3 install pytest"