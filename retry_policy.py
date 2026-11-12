"""Pure retry timing for a synthetic demonstration."""
import math


def constant_delay():
    return 1


def _require_finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + " must be a finite int or float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(name + " must be finite")


def _positive_ratio(value, name):
    _require_finite_number(value, name)
    if value <= 0:
        raise ValueError(name + " must be greater than zero")
    if isinstance(value, int):
        return value, 1
    return value.as_integer_ratio()


def next_delay(attempt, base_delay, max_delay, remaining):
    """Return the capped exponential delay when it fits the remaining budget."""
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 0:
        raise ValueError("attempt must be a non-negative int")
    base_num, base_den = _positive_ratio(base_delay, "base_delay")
    cap_num, cap_den = _positive_ratio(max_delay, "max_delay")
    _require_finite_number(remaining, "remaining")
    if remaining < 0:
        raise ValueError("remaining must be non-negative")

    scaled_num = base_num * cap_den
    scaled_cap = cap_num * base_den
    scaled_bits = scaled_num.bit_length() + attempt
    cap_bits = scaled_cap.bit_length()
    if scaled_bits > cap_bits:
        capped = True
    elif scaled_bits < cap_bits:
        capped = False
    else:
        capped = (scaled_num << attempt) >= scaled_cap

    if capped:
        delay = max_delay
    else:
        exponent = base_den.bit_length() - 1
        if attempt >= exponent:
            delay = base_num << (attempt - exponent)
        else:
            delay = base_num / (base_den >> attempt)
    return delay if delay <= remaining else None
