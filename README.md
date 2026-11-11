# Harness v3 synthetic pilot

Only synthetic retry-policy code. No production data or credentials.

## `next_delay(attempt, base_delay, max_delay, remaining)`

Pure function that computes a capped exponential retry delay. It only calculates
the value: it never waits, reads a clock, uses randomness or performs I/O.

Arguments:

- `attempt` — `int >= 0`; `bool` is rejected.
- `base_delay` — finite `int` or `float` greater than zero; `bool` is rejected.
- `max_delay` — finite `int` or `float` greater than zero; `bool` is rejected.
- `remaining` — finite `int` or `float` greater than or equal to zero; `bool` is
  rejected.

Any other value raises `ValueError`, and all four arguments are validated before
the budget check. `NaN`, infinities, negative values, zero bases/caps and
non-numeric types are invalid.

The result is `min(max_delay, base_delay * 2**attempt)` when that delay is less
than or equal to `remaining`. An exact match with the budget is accepted. If the
delay exceeds `remaining`, or `remaining` is zero, the result is `None`; an
exhausted budget is a normal outcome, not an error.

The calculation is exact and bounded: it compares integer ratios instead of
building `2**attempt`, so a huge `attempt` such as `10**9` returns the cap
quickly without overflow or a loop over the attempt count. The returned number
may be an `int` or a `float`; numerically equal values are equivalent, and an
integer delay beyond the float range stays an `int`. Only the standard library
`math` module is used: no new dependencies, no side effects.

Examples:

    next_delay(3, 1, 10, 8) == 8
    next_delay(4, 1, 10, 9) is None
    next_delay(10**9, 1, 10, 10) == 10

Run the targeted unit tests with:

    python3 -m unittest discover -s tests -p test_retry_policy.py -v
