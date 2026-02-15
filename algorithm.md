# Algorithm

## Script Behaviour

The script runs as a loop, prompting the user to enter either an integer or "stop":

- **Integer matching problem criteria**: print the corresponding date.
- **"stop"**: exit the script.
- **Anything else**: print an error message and re-prompt.

There is an option to run in **CHECKING mode**, which triggers extra validation checks (noted below).

## Constraints

- A valid date consists of 1 or more pairs of digits (each digit 0–9 inclusive) in sequence.
- Each pair is `(freq, i)` where `freq` is the total number of occurrences of digit `i` in the date.
- `i` is not repeated across pairs, so there can be at most 10 pairs.

## Top-Level Logic

To determine the date for a given integer `d`:

1. Create an empty list to store all dates calculated so far, in sequence.
2. Set the number of pairs `n` used to create the next set of dates to 1.
3. Prompt for the integer `d`.
4. If `d` <= number of dates calculated so far:
   - Return the `d`th date in the list.
   - Go back to 3.
5. Calculate the ordered list of all dates with `n` pairs.
6. Add this list to the list of dates calculated so far.
7. Increment `n`.
8. Go back to 4.

## Calculate Ordered List of Dates with `n` Pairs

1. Create an empty list to store all the dates.
2. Create a list of all possible combinations of `n` positive integers that sum to `2n` (these will be the frequencies for the `n` pairs), with the constraint that each integer <= 9.
3. For each combination:
   - Calculate the list of all possible dates using these frequencies.
   - Add this list to the overall list of dates.
4. Sort the overall list of dates and return it.

## Calculate List of Dates for a Given Combination of Frequencies

1. Create an empty list to store all the dates.
2. Calculate the list of all possible combinations of pairs `(freq, i)` given this combination of frequencies.
3. For each combination of pairs (i.e. a list of pairs):
   - Calculate all permutations for this list of pairs.
   - For each permutation, assemble the date:
     - E.g. given pairs `[(1, 0), (1, 2), (3, 1), (3, 3)]` the date is `10123133`.
     - If CHECKING mode is set, check the date is valid.
     - Add the date to the overall list of dates.
4. Return the overall list of dates.

## Calculate All Possible Combinations of Pairs Given Frequencies

1. Create a structure that assigns a unique digit to each frequency, initially null (no assignment yet).
2. Create a set of available digits: 0 through 9 inclusive.
3. Determine the ordered counts for each frequency — another list of pairs, in reverse order.
   - E.g. if `n = 5` and frequencies are `(1, 1, 1, 2, 5)` then the ordered counts are `[(3, 1), (1, 5), (1, 2)]`.
4. Calculate the list of all possible combinations of pairs `(freq, i)` given the assignments to date (per step 1), available digits (step 2), and remaining counts for the frequencies (step 3).
5. Return this list.

## Calculate Combinations of Pairs Given Assignments, Available Digits, and Remaining Counts

1. While there are remaining counts:
   - Pop the next `(count, freq)` pair from the front of the remaining counts list.
   - Check whether `count + 1 == freq` AND `freq != 2`:
     - If yes, return an empty list.
   - Check whether there is a slot free to assign a digit to `count + 1`.
     - If no, return an empty list.
   - Assign the digit `freq` to `count + 1`.
     - Remove digit `freq` from the set of available digits.
2. If all frequencies have been assigned:
   - Convert the assignments into a list of pairs.
   - Return this inside a list.
3. If CHECKING mode is set, check the value of all remaining frequencies to be assigned:
   - If any remaining frequency != 1, raise an error.
4. Let the number of remaining frequencies be `num_freq`.
5. Create a list of all possible combinations taking `num_freq` digits from the available digits.
6. Create a new list from this list of combinations:
   - Each item is a copy of the assignments with each digit in the combination assigned to one of the remaining frequencies.
   - E.g. if there are 3 remaining frequencies (all `freq = 1` per above) and the combination from available digits is `(5, 6, 7)`, then assignments will be `1->5`, `1->6`, `1->7`.
7. Convert each assignment in the list to a list of pairs.
8. Return the list of lists of pairs.

## Validate a Date (CHECKING Mode)

1. Convert the integer into an ordered list of digits.
2. If the length of the list is odd, return FALSE.
3. Create a set of counts represented by the list:
   - For each pair of digits `(i, j)` in the list, add `(i, j)` to the set.
4. Actually count the digits in the list and create another set from this.
5. If the two sets match, return TRUE, otherwise return FALSE.
