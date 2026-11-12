import math
import os
import subprocess
import sys
import unittest

from retry_policy import next_delay


class ValidResults(unittest.TestCase):
    CASES = [
        ((0, 1, 10, 10), 1),
        ((3, 0.25, 10, 10), 2),
        ((4, 1, 10, 10), 10),
        ((0, 8, 3, 3), 3),
        ((0, 3, 3, 3), 3),
        ((3, 1, 8, 8), 8),
        ((1, 0.25, 0.5, 0.5), 0.5),
        ((3, 1, 10, 8), 8),
        ((3, 1, 10, 7), None),
        ((4, 1, 10, 9), None),
        ((0, 1, 10, 0), None),
        ((0, 1, 10, -0.0), None),
        ((0, 0.5, 10, 0.5), 0.5),
        ((0, 0.5, 10, 0.49), None),
        ((2, 1, 5.0, 4.5), 4),
    ]

    def test_table(self):
        for args, expected in self.CASES:
            with self.subTest(args=args):
                result = next_delay(*args)
                if expected is None:
                    self.assertIsNone(result)
                else:
                    self.assertEqual(result, expected)


class InvalidArguments(unittest.TestCase):
    NON_NUMERIC = [True, False, None, "1", 1 + 2j, [1],
                   float("nan"), float("inf"), float("-inf")]

    def assert_invalid(self, *args):
        with self.assertRaises(ValueError):
            next_delay(*args)

    def test_attempt_values(self):
        for value in self.NON_NUMERIC + [-1, 0.0, 1.5]:
            with self.subTest(attempt=value):
                self.assert_invalid(value, 1, 10, 10)

    def test_base_delay_values(self):
        for value in self.NON_NUMERIC + [0, 0.0, -0.0, -1, -0.5]:
            with self.subTest(base_delay=value):
                self.assert_invalid(0, value, 10, 10)

    def test_max_delay_values(self):
        for value in self.NON_NUMERIC + [0, 0.0, -0.0, -1, -0.5]:
            with self.subTest(max_delay=value):
                self.assert_invalid(0, 1, value, 10)

    def test_remaining_values(self):
        for value in self.NON_NUMERIC + [-1, -0.5]:
            with self.subTest(remaining=value):
                self.assert_invalid(0, 1, 10, value)

    def test_invalid_arguments_win_over_zero_budget(self):
        for value in [True, False, None, "1", 1 + 2j, [1],
                      float("nan"), float("inf"), float("-inf"), -1, 0.0, 1.5]:
            with self.subTest(position="attempt", value=value):
                self.assert_invalid(value, 1, 10, 0)
        for value in [True, False, None, "1", 1 + 2j, [1],
                      float("nan"), float("inf"), float("-inf"), 0, 0.0, -1]:
            with self.subTest(position="base_delay", value=value):
                self.assert_invalid(0, value, 10, 0)
            with self.subTest(position="max_delay", value=value):
                self.assert_invalid(0, 1, value, 0)

    def test_valid_boundaries_are_accepted(self):
        self.assertEqual(next_delay(0, 1, 10, 10), 1)
        self.assertEqual(next_delay(0, 0.5, 0.25, 0.25), 0.25)
        self.assertIsNone(next_delay(0, 1, 10, 0))
        self.assertIsNone(next_delay(0, 1, 10, -0.0))
        self.assertEqual(next_delay(2, 1, 5.0, 4.5), 4)
        self.assertEqual(next_delay(0, 10**400, 10**401, 10**401), 10**400)


class NumericExtremes(unittest.TestCase):
    H = 10**400
    F = sys.float_info.max
    S = float.fromhex("0x0.0000000000001p-1022")

    def test_large_ints(self):
        self.assertEqual(next_delay(0, self.H, 10 * self.H, 10 * self.H), self.H)
        self.assertEqual(next_delay(1, self.H, 10 * self.H, 10 * self.H), 2 * self.H)

    def test_max_float(self):
        self.assertEqual(next_delay(1, self.F, self.F, self.F), self.F)
        self.assertFalse(math.isinf(next_delay(1, self.F, self.F, self.F)))
        self.assertEqual(next_delay(1, self.F, 1 << 2000, 1 << 2000), int(self.F) * 2)

    def test_subnormal(self):
        self.assertEqual(next_delay(0, self.S, 1, self.S), self.S)
        self.assertEqual(next_delay(1074, self.S, 2, 1), 1)
        self.assertEqual(next_delay(2098, self.S, self.F, self.F), self.F)

    def test_delay_beyond_float_range(self):
        self.assertEqual(next_delay(1500, 1.0, 1 << 2000, 1 << 2000), 1 << 1500)

    def test_cap_boundary(self):
        below = math.nextafter(8.0, 0.0)
        above = math.nextafter(8.0, math.inf)
        self.assertEqual(next_delay(3, 1.0, below, 8), below)
        self.assertEqual(next_delay(3, 1.0, above, 8), 8)


class HugeAttemptWatchdog(unittest.TestCase):
    def test_huge_attempt_completes_within_watchdog(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script = (
            "import sys, unittest\n"
            "from retry_policy import next_delay\n"
            "F = sys.float_info.max\n"
            "s = float.fromhex('0x0.0000000000001p-1022')\n"
            "class HugeAttempt(unittest.TestCase):\n"
            "    def test_calls(self):\n"
            "        self.assertEqual(next_delay(10**9, 1, 10, 10), 10)\n"
            "        self.assertIsNone(next_delay(10**9, 1, 10, 9))\n"
            "        self.assertEqual(next_delay(10**9, s, F, F), F)\n"
            "        self.assertEqual(next_delay(10**100, 1, 10, 10), 10)\n"
            "unittest.main(verbosity=0)\n"
        )
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=root,
            timeout=5,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)


class Determinism(unittest.TestCase):
    def test_repeated_calls_are_identical(self):
        first = next_delay(3, 0.25, 10, 10)
        self.assertEqual(first, 2)
        for _ in range(5):
            next_delay(7, 1, 3, 3)
            self.assertEqual(next_delay(3, 0.25, 10, 10), first)


if __name__ == "__main__":
    unittest.main()
