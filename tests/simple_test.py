#!/usr/bin/env python3
"""
Simple test runner for the calculator without pytest dependency
"""

import subprocess
import sys
import os


def run_calculator(input_data):
    """Run the calculator with given input"""
    try:
        process = subprocess.run(
            ["../build/calculator"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5
        )
        return process.returncode, process.stdout, process.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except FileNotFoundError:
        return -1, "", "Calculator not found"


def test_basic_operations():
    """Test basic operations"""
    print("Testing basic operations...")
    
    # Test positive numbers
    ret, out, err = run_calculator("5\n3\n")
    assert ret == 0, f"Expected 0, got {ret}"
    assert "5 + 3 = 8" in out, f"Expected '5 + 3 = 8' in {out}"
    print("✓ Positive numbers: 5 + 3 = 8")
    
    # Test negative numbers
    ret, out, err = run_calculator("-10\n7\n")
    assert ret == 0, f"Expected 0, got {ret}"
    assert "-10 + 7 = -3" in out, f"Expected '-10 + 7 = -3' in {out}"
    print("✓ Negative numbers: -10 + 7 = -3")
    
    # Test both negative
    ret, out, err = run_calculator("-5\n-3\n")
    assert ret == 0, f"Expected 0, got {ret}"
    assert "-5 + -3 = -8" in out, f"Expected '-5 + -3 = -8' in {out}"
    print("✓ Both negative: -5 + -3 = -8")
    
    # Test zeros
    ret, out, err = run_calculator("0\n0\n")
    assert ret == 0, f"Expected 0, got {ret}"
    assert "0 + 0 = 0" in out, f"Expected '0 + 0 = 0' in {out}"
    print("✓ Zeros: 0 + 0 = 0")


def test_large_numbers():
    """Test large numbers"""
    print("\nTesting large numbers...")
    
    ret, out, err = run_calculator("1000000\n2000000\n")
    assert ret == 0, f"Expected 0, got {ret}"
    assert "1000000 + 2000000 = 3000000" in out
    print("✓ Large numbers: 1000000 + 2000000 = 3000000")


def test_invalid_input():
    """Test invalid input"""
    print("\nTesting invalid input...")
    
    ret, out, err = run_calculator("abc\ndef\n")
    assert ret == 1, f"Expected 1, got {ret}"
    assert "Error: Invalid input" in (out + err)
    print("✓ Invalid input handled correctly")


def test_user_interface():
    """Test user interface"""
    print("\nTesting user interface...")
    
    ret, out, err = run_calculator("1\n2\n")
    assert ret == 0, f"Expected 0, got {ret}"
    assert "Enter first number:" in out
    assert "Enter second number:" in out
    print("✓ Correct prompts displayed")


def main():
    """Run all tests"""
    print("Calculator Test Suite")
    print("=" * 40)
    
    try:
        # Ensure calculator exists
        if not os.path.exists("../build/calculator"):
            print("Building calculator...")
            subprocess.run(["make", "-C", "..", "all"], check=True)
        
        test_basic_operations()
        test_large_numbers()
        test_invalid_input()
        test_user_interface()
        
        print("\n" + "=" * 40)
        print("✅ All tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())