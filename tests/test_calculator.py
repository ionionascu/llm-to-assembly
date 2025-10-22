#!/usr/bin/env python3
"""
Comprehensive test suite for the Calculator Application
Supports multiple test scenarios with captured input/output validation
"""

import subprocess
import sys
import os
import pytest
from typing import Tuple, Optional


class CalculatorTester:
    """Test harness for the calculator application"""
    
    def __init__(self, executable_path: str = "../build/calculator"):
        self.executable_path = executable_path
        self.ensure_executable_exists()
    
    def ensure_executable_exists(self):
        """Ensure the calculator executable exists"""
        if not os.path.exists(self.executable_path):
            # Try to build it
            build_dir = os.path.dirname(self.executable_path)
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)
            
            # Try to compile
            try:
                subprocess.run(
                    ["make", "-C", "..", "all"],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Failed to build calculator: {e}")
    
    def run_calculator(self, input_data: str, timeout: int = 5) -> Tuple[int, str, str]:
        """
        Run the calculator with given input
        
        Args:
            input_data: String to send to stdin
            timeout: Maximum time to wait for completion
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        try:
            process = subprocess.run(
                [self.executable_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=timeout
            )
            return process.returncode, process.stdout, process.stderr
        except subprocess.TimeoutExpired:
            pytest.fail(f"Calculator timed out after {timeout} seconds")
        except FileNotFoundError:
            pytest.fail(f"Calculator executable not found at {self.executable_path}")


# Test fixture
@pytest.fixture
def calculator():
    """Fixture to provide calculator tester instance"""
    return CalculatorTester()


# Basic functionality tests
class TestBasicOperations:
    """Test basic addition operations"""
    
    def test_positive_numbers(self, calculator):
        """Test addition of positive numbers"""
        return_code, stdout, stderr = calculator.run_calculator("5\n3\n")
        
        assert return_code == 0, f"Expected exit code 0, got {return_code}"
        assert "5 + 3 = 8" in stdout, f"Expected '5 + 3 = 8' in output, got: {stdout}"
    
    def test_negative_numbers(self, calculator):
        """Test addition with negative numbers"""
        return_code, stdout, stderr = calculator.run_calculator("-10\n7\n")
        
        assert return_code == 0, f"Expected exit code 0, got {return_code}"
        assert "-10 + 7 = -3" in stdout, f"Expected '-10 + 7 = -3' in output, got: {stdout}"
    
    def test_both_negative(self, calculator):
        """Test addition of two negative numbers"""
        return_code, stdout, stderr = calculator.run_calculator("-5\n-3\n")
        
        assert return_code == 0, f"Expected exit code 0, got {return_code}"
        assert "-5 + -3 = -8" in stdout, f"Expected '-5 + -3 = -8' in output, got: {stdout}"
    
    def test_zero_values(self, calculator):
        """Test addition with zero"""
        test_cases = [
            ("0\n0\n", "0 + 0 = 0"),
            ("0\n5\n", "0 + 5 = 5"),
            ("5\n0\n", "5 + 0 = 5"),
        ]
        
        for input_data, expected in test_cases:
            return_code, stdout, stderr = calculator.run_calculator(input_data)
            assert return_code == 0, f"Expected exit code 0, got {return_code}"
            assert expected in stdout, f"Expected '{expected}' in output, got: {stdout}"


class TestLargeNumbers:
    """Test with large numbers and edge cases"""
    
    def test_large_positive_numbers(self, calculator):
        """Test addition of large positive numbers"""
        return_code, stdout, stderr = calculator.run_calculator("1000000\n2000000\n")
        
        assert return_code == 0, f"Expected exit code 0, got {return_code}"
        assert "1000000 + 2000000 = 3000000" in stdout
    
    def test_max_int_safe(self, calculator):
        """Test addition that's close to but doesn't exceed limits"""
        # Use numbers that won't cause overflow
        return_code, stdout, stderr = calculator.run_calculator("1000000000\n1000000000\n")
        
        assert return_code == 0, f"Expected exit code 0, got {return_code}"
        assert "1000000000 + 1000000000 = 2000000000" in stdout


class TestUserInterface:
    """Test user interface and prompts"""
    
    def test_prompts_displayed(self, calculator):
        """Test that correct prompts are displayed"""
        return_code, stdout, stderr = calculator.run_calculator("1\n2\n")
        
        assert "Enter first number:" in stdout, "First prompt not found"
        assert "Enter second number:" in stdout, "Second prompt not found"
        assert return_code == 0, f"Expected exit code 0, got {return_code}"


class TestInputValidation:
    """Test input validation and error handling"""
    
    def test_invalid_first_input(self, calculator):
        """Test invalid input"""
        return_code, stdout, stderr = calculator.run_calculator("abc\ndef\n")
        
        assert return_code == 1, f"Expected exit code 1 for invalid input, got {return_code}"
        assert "Error: Invalid input" in stderr or "Error: Invalid input" in stdout
    
    def test_invalid_second_input(self, calculator):
        """Test invalid input for second number"""
        return_code, stdout, stderr = calculator.run_calculator("5\nabc\n")
        
        assert return_code == 1, f"Expected exit code 1 for invalid input, got {return_code}"
        assert "Error: Invalid input" in stderr or "Error: Invalid input" in stdout
    
    def test_empty_input(self, calculator):
        """Test empty input"""
        return_code, stdout, stderr = calculator.run_calculator("\n\n")
        
        assert return_code == 1, f"Expected exit code 1 for empty input, got {return_code}"


class TestPerformance:
    """Test performance requirements"""
    
    def test_execution_time(self, calculator):
        """Test that execution completes within reasonable time"""
        import time
        
        start_time = time.time()
        return_code, stdout, stderr = calculator.run_calculator("100\n200\n")
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < 1.0, f"Execution took {execution_time:.2f}s, expected < 1.0s"
        assert return_code == 0, f"Expected exit code 0, got {return_code}"


class TestEdgeCases:
    """Test various edge cases"""
    
    def test_whitespace_input(self, calculator):
        """Test input with leading/trailing whitespace"""
        test_cases = [
            ("  5   3  \n", "5 + 3 = 8"),
            (" -5  3 \n", "-5 + 3 = -2"),
        ]
        
        for input_data, expected in test_cases:
            return_code, stdout, stderr = calculator.run_calculator(input_data)
            assert return_code == 0, f"Expected exit code 0 for input '{input_data.strip()}', got {return_code}"
            assert expected in stdout, f"Expected '{expected}' in output for input '{input_data.strip()}', got: {stdout}"
    
    def test_single_digit_numbers(self, calculator):
        """Test single digit numbers"""
        return_code, stdout, stderr = calculator.run_calculator("1 2\n")
        
        assert return_code == 0, f"Expected exit code 0, got {return_code}"
        assert "1 + 2 = 3" in stdout


# Test suite runner and reporting
class TestSuiteRunner:
    """Custom test runner with detailed reporting"""
    
    @staticmethod
    def run_all_tests():
        """Run all tests and provide summary"""
        print("Calculator Application Test Suite")
        print("=" * 50)
        
        # Run pytest with verbose output
        exit_code = pytest.main([
            __file__,
            "-v",
            "--tb=short",
            "--color=yes"
        ])
        
        return exit_code


if __name__ == "__main__":
    # Can be run directly or via pytest
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        # Run with pytest
        sys.exit(pytest.main([__file__, "-v"]))
    else:
        # Run custom test runner
        runner = TestSuiteRunner()
        sys.exit(runner.run_all_tests())