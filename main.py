#!/usr/bin/env python3
"""Allusional Almanac - BIO 2019 problem solution."""

import sys
import time
from collections import Counter
from itertools import combinations, permutations

# Module-level flag for extra validation checks.
CHECKING = False


def main():
    """Main loop: prompt for integers, print corresponding dates."""
    global CHECKING
    CHECKING = "--check" in sys.argv

    # Cache of all dates calculated so far, in order.
    all_dates = []
    # Current number of pairs being generated.
    n = 1

    while True:
        user_input = input("Enter date number (or 'stop'): ").strip()

        if user_input.lower() == "stop":
            break

        try:
            d = int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer or 'stop'.")
            continue

        if d < 1:
            print("Please enter a positive integer.")
            continue

        # Expand cache until we have enough dates.
        start = time.perf_counter()
        while len(all_dates) < d:
            new_dates = calculate_dates_with_n_pairs(n)
            all_dates.extend(new_dates)
            n += 1
        elapsed = time.perf_counter() - start

        print(f"{all_dates[d - 1]}  ({elapsed:.3f}s, {len(all_dates)} cached)")


def calculate_dates_with_n_pairs(n):
    """Return the sorted list of all valid dates formed from exactly n pairs."""
    all_dates = []
    for freq_combo in get_frequency_combinations(n):
        all_dates.extend(calculate_dates_for_frequencies(freq_combo))
    all_dates.sort()
    return all_dates


def get_frequency_combinations(n):
    """Generate all partitions of 2n into n positive integers, each <= 9.

    Yields tuples in non-decreasing order.
    """
    yield from _partition(2 * n, n, 1)


def _partition(total, parts, minimum):
    """Recursively partition `total` into `parts` positive integers >= minimum, each <= 9."""
    if parts == 1:
        if minimum <= total <= 9:
            yield (total,)
        return
    # The current part ranges from `minimum` to at most total // parts
    # (to keep non-decreasing order) and at most 9.
    max_val = min(total // parts, 9)
    for val in range(minimum, max_val + 1):
        for rest in _partition(total - val, parts - 1, val):
            yield (val,) + rest


def calculate_dates_for_frequencies(freq_combo):
    """Return all dates that can be formed from the given frequency combination.

    For each valid digit assignment, generate all permutations of the pairs
    and assemble each into a date integer.
    """
    all_dates = []
    pair_combinations = calculate_pair_combinations(freq_combo)
    for pairs in pair_combinations:
        for perm in permutations(pairs):
            date = assemble_date(perm)
            if CHECKING:
                if not validate_date(date):
                    raise ValueError(f"Invalid date generated: {date}")
            all_dates.append(date)
    return all_dates


def calculate_pair_combinations(freq_combo):
    """Return all valid assignments of digits to the given frequencies.

    Each assignment is a list of (freq, digit) pairs.
    """
    # Count how many times each frequency value appears.
    freq_counter = Counter(freq_combo)

    # Build ordered counts: (count, freq) pairs sorted descending by count,
    # then descending by freq for tie-breaking.
    ordered_counts = sorted(freq_counter.items(), key=lambda x: (-x[1], -x[0]))
    # Convert from (freq_value, count) to (count, freq_value).
    ordered_counts = [(count, freq) for freq, count in ordered_counts]

    # Assignments: maps frequency value -> list of digits assigned to it.
    assignments = {freq: [] for freq in freq_counter}
    available = set(range(10))

    return _assign_digits(assignments, available, ordered_counts, freq_counter)


def _assign_digits(assignments, available, remaining_counts, freq_counter):
    """Recursively assign digits to frequency slots.

    Processes forced assignments (where a frequency's count+1 matches another
    frequency value) first, then fills remaining freq-1 slots by combination.
    """
    # Work through forced assignments.
    while remaining_counts:
        count, freq = remaining_counts[0]
        remaining_counts = remaining_counts[1:]

        # Check whether there is a free slot at frequency count+1.
        target_freq = count + 1
        if target_freq not in assignments or len(assignments[target_freq]) >= freq_counter[target_freq]:
            return []

        # Assign digit `freq` to the slot at frequency `target_freq`.
        if freq not in available:
            return []
        assignments = {k: list(v) for k, v in assignments.items()}  # deep copy
        assignments[target_freq].append(freq)
        available = available.copy()
        available.discard(freq)

    # Check if all frequencies have been fully assigned.
    all_assigned = all(len(assignments[f]) == freq_counter[f] for f in assignments)

    if all_assigned:
        # Convert assignments to a list of (freq, digit) pairs.
        pairs = []
        for freq, digits in assignments.items():
            for digit in digits:
                pairs.append((freq, digit))
        return [pairs]

    # Find remaining slots (frequencies that still need digits assigned).
    remaining_freqs = []
    for freq in sorted(assignments.keys()):
        needed = freq_counter[freq] - len(assignments[freq])
        for _ in range(needed):
            remaining_freqs.append(freq)

    if CHECKING:
        # All remaining frequencies should be 1.
        for f in remaining_freqs:
            if f != 1:
                raise ValueError(f"Remaining frequency {f} is not 1")

    num_remaining = len(remaining_freqs)
    results = []

    for combo in combinations(sorted(available), num_remaining):
        # Assign each digit in the combination to a remaining frequency slot.
        new_assignments = {k: list(v) for k, v in assignments.items()}
        for digit, freq in zip(combo, remaining_freqs):
            new_assignments[freq].append(digit)

        # Convert to pairs.
        pairs = []
        for freq, digits in new_assignments.items():
            for digit in digits:
                pairs.append((freq, digit))
        results.append(pairs)

    return results


def assemble_date(pairs):
    """Convert an ordered sequence of (freq, digit) pairs into a date integer.

    E.g. [(1, 0), (1, 2), (3, 1), (3, 3)] -> 10123133
    """
    result = 0
    for freq, digit in pairs:
        result = result * 100 + freq * 10 + digit
    return result


def validate_date(date):
    """Validate that a date integer is self-consistent.

    Each pair (freq, digit) in the date claims that `digit` appears exactly
    `freq` times in the entire date string. Returns True if all claims hold.
    """
    digits = []
    n = date
    while n > 0:
        digits.append(n % 10)
        n //= 10
    digits.reverse()

    # Must have even length.
    if len(digits) % 2 != 0:
        return False

    # Build claimed counts from pairs.
    claimed = set()
    for i in range(0, len(digits), 2):
        freq, digit = digits[i], digits[i + 1]
        claimed.add((freq, digit))

    # Build actual counts.
    actual_counts = Counter(digits)
    actual = set()
    for digit, count in actual_counts.items():
        actual.add((count, digit))

    return claimed == actual


if __name__ == "__main__":
    main()
