# Allusional Almanac

BIO 2019 Problem — [Source](https://www.olympiad.org.uk/papers/2019/bio/bio19-exam.pdf)

## Problem Statement

In "The Masked Lady and the Allusional Almanac" after a jaunty journey
through jeopardous jungle, our heroine found the remains of an ancient
civilisation. After decoding divers dubious dates she determined that the
civilisation had marked the days by using numbers that described themselves. The
novel's concluding remarks, that the civilisation's collapse was caused by
complexity, being seen as thinly veiled allusion against industrialisation.

Each date was represented by a number that described itself by being read as a
count of each digit 0, …, 9 occurring in the number. The dth day since the
foundation of the civilisation was represented by the dth such number. A date
only consisted of digits and their counts, counts always appeared immediately
before the corresponding digit, and no digit and its count were repeated or
overlapped.

For example:

- the first recorded day was 22 (two 2s);
- the second was 10123133 (one 0, one 2, three 1s and three 3s);
- the 500th day was 31143312.

The input will consist of a single integer, d (1 ≤ d ≤ 2²⁴), indicating a date. Test
input will always be for a date that can be represented.

You should output a single integer, the civilisation's representation for day d.
