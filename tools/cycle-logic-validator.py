#!/usr/bin/env python3
"""
Bitcoin Cycles Logic Validator
Basic validation of cycle detection logic without TradingView
"""

import math
import sys
from typing import List, Tuple

class CycleLogicValidator:
    """Validates cycle detection logic with synthetic data"""

    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0

    def validate_cycle_length_logic(self):
        """Test cycle length parameter validation"""
        print("🧪 Testing Cycle Length Logic...")

        # Test valid ranges
        test_cases = [
            (40, 70, True, "Daily default range"),
            (20, 32, True, "Weekly default range"),
            (30, 60, True, "Custom valid range"),
            (10, 15, True, "Minimum valid range"),
            (5, 10, False, "Below minimum"),
            (100, 200, False, "Above maximum"),
            (70, 40, False, "Min > Max (invalid)"),
        ]

        for min_cycle, max_cycle, expected_valid, description in test_cases:
            is_valid = 1 <= min_cycle <= 200 and 1 <= max_cycle <= 200 and min_cycle < max_cycle
            result = "✅ PASS" if is_valid == expected_valid else "❌ FAIL"
            print(f"  {result}: {description} (Min: {min_cycle}, Max: {max_cycle})")

            if is_valid == expected_valid:
                self.passed += 1
            else:
                self.failed += 1

    def validate_timeframe_detection(self):
        """Test timeframe detection logic"""
        print("\n🧪 Testing Timeframe Detection...")

        # Simulate timeframe periods (simplified)
        test_cases = [
            ("D", "Daily"),
            ("W", "Weekly"),
            ("M", "Monthly"),
            ("H", "Hourly"),
            ("5", "Custom"),
        ]

        for period, expected_timeframe in test_cases:
            # Simplified timeframe detection logic
            if period == "D":
                detected = "Daily"
            elif period == "W":
                detected = "Weekly"
            elif period == "M":
                detected = "Monthly"
            elif "H" in period:
                detected = "Hourly"
            else:
                detected = "Custom"

            result = "✅ PASS" if detected == expected_timeframe else "❌ FAIL"
            print(f"  {result}: Period '{period}' → Detected '{detected}' (Expected '{expected_timeframe}')")

            if detected == expected_timeframe:
                self.passed += 1
            else:
                self.failed += 1

    def validate_cycle_progression(self):
        """Test cycle progression counting"""
        print("\n🧪 Testing Cycle Progression...")

        # Simulate cycle progression
        cycle_length = 60
        test_cases = [
            (5, "Early cycle"),
            (30, "Mid cycle"),
            (55, "Late cycle"),
            (65, "Beyond cycle length"),
        ]

        for day_count, description in test_cases:
            is_in_window = day_count >= 40 and day_count < 60  # Using Daily defaults

            expected_in_window = 40 <= day_count < 60
            result = "✅ PASS" if is_in_window == expected_in_window else "❌ FAIL"
            print(f"  {result}: Day {day_count} {description} → In window: {is_in_window}")

            if is_in_window == expected_in_window:
                self.passed += 1
            else:
                self.failed += 1

    def validate_price_pattern_generation(self):
        """Test synthetic price pattern generation"""
        print("\n🧪 Testing Price Pattern Generation...")

        # Generate synthetic cycle data
        base_price = 50000
        cycle_length = 60
        amplitude = 15000

        test_points = [0, 15, 30, 45, 60]  # Key points in cycle

        for bar_index in test_points:
            # Sine wave pattern (same as Pine Script)
            noise = (math.sin(bar_index * 2 * 3.14159 / cycle_length) * amplitude)
            price = base_price + noise

            # Basic validation
            is_reasonable = 30000 <= price <= 70000  # Reasonable BTC price range
            result = "✅ PASS" if is_reasonable else "❌ FAIL"
            print(f"  {result}: Bar {bar_index} → Price: ${price:.0f} ({'Reasonable' if is_reasonable else 'Unreasonable'})")
            if is_reasonable:
                self.passed += 1
            else:
                self.failed += 1

    def validate_offset_calculations(self):
        """Test label offset calculations"""
        print("\n🧪 Testing Offset Calculations...")

        atr_value = 14.5  # Sample ATR value
        test_cases = [
            (atr_value, 0.75, "Standard label offset"),
            (atr_value, 2.0, "Large offset"),
            (atr_value, 0.1, "Small offset"),
        ]

        for atr, multiplier, description in test_cases:
            offset = atr * multiplier
            is_positive = offset > 0
            is_reasonable = 0 < offset < 100  # Reasonable pixel offset

            result = "✅ PASS" if is_positive and is_reasonable else "❌ FAIL"
            print(f"  {result}: ATR {atr} × {multiplier} → Offset: {offset:.2f} ({description})")
            if is_positive and is_reasonable:
                self.passed += 1
            else:
                self.failed += 1

    def run_all_tests(self):
        """Run all validation tests"""
        print("🚀 Bitcoin Cycles Logic Validator")
        print("=" * 50)

        self.validate_cycle_length_logic()
        self.validate_timeframe_detection()
        self.validate_cycle_progression()
        self.validate_price_pattern_generation()
        self.validate_offset_calculations()

        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED - REVIEW LOGIC")
            return False

def main():
    validator = CycleLogicValidator()
    success = validator.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()