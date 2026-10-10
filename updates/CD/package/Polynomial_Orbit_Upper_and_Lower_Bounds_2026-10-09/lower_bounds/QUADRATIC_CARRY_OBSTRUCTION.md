# Quadratic, linear-output exponential delay

9 October 2026. An illustrative explicit lower obstruction, independently reconstructed. No novelty or new complexity classification is claimed. Boolean/circuit simulation already underlies known PSPACE lower bounds for polynomial-recursive zeroness; the point here is an exact, small-coefficient, fixed-degree family that sharpens the parameters of the saved example.

## Statement

For every m >= 1 there is a polynomial map F_m: Q^(2m) -> Q^(2m), of coordinate degree at most 2 and with coefficients in {-2,-1,0,1,2}, and a coordinate output h of degree 1, such that the all-zero initial state has first nonzero output exactly at

L_m = 2^(m+1) - 2.

Thus no polynomial or subexponential-in-dimension coefficient-uniform zero-prefix bound is possible even for quadratic updates and linear outputs. This does not imply that an elementary upper bound is impossible, and supplies no tower lower bound.

## Polynomial map

Coordinates are bits b_0,...,b_(m-1), carry-token coordinates c_1,...,c_(m-1), and an output coordinate z. Define the polynomial abbreviation

c_0 = 1 - sum_(i=1)^(m-1) c_i.

Use simultaneous updates

b_i' = b_i + c_i - 2 b_i c_i,                  0 <= i < m,
c_i' = b_(i-1) c_(i-1),                       1 <= i < m,
z'   = b_(m-1) c_(m-1).

The initial values of all actual coordinates are zero, so the implicit token c_0 is initially 1. Output h=z. Empty sums are zero; for m=1 the map is simply b_0'=1-b_0, z'=b_0.

Every formula is globally polynomial, rather than a conditional or partially defined update. After expanding the abbreviation, every coordinate has degree at most 2 and the stated coefficient set. There are O(m) nonzero monomials in the whole system, counting the two occurrences of the sum defining c_0.

## Invariant and counter interpretation

Along this initial orbit, every b_i is Boolean and exactly one of c_0,...,c_(m-1) is 1. If the token is at i, only b_i flips.

- If b_i was 0, that bit becomes 1 and the token resets to 0.
- If b_i was 1 and i < m-1, that bit becomes 0 and the token advances to i+1.
- If b_i was 1 and i=m-1, that bit becomes 0 and the token resets to 0; exactly this step sets z'=1.

To verify the token claim, c_j'=b_(j-1)c_(j-1) for j>=1 can be nonzero only at j=i+1, and only if the old bit b_i was 1. The implicit next c_0 is 1 minus the sum of those new tokens. The three cases follow. Bit updates preserve {0,1} because they perform exclusive-or with the active token.

This is a serial binary incrementer. At every completed increment the token is back at 0 and the bits represent the completed-increment count modulo 2^m. Before the first wrap, a token reaches the top bit with that bit already 1 only during the final increment, from 2^m-1 to 0. Therefore z remains zero until that final microstep.

## Exact delay count

During one complete traversal of all 2^m increments, bit i flips exactly 2^(m-i) times. Each microstep flips one bit. The number of microsteps before the first overflow pulse is consequently

sum_(i=0)^(m-1) 2^(m-i) = 2^(m+1)-2.

The output coordinate is set on the overflow transition, so its first nonzero state has index L_m, not L_m+1. The initial output at index 0 is zero.

## Primary comparison boundary

Clemente, Donten-Bury, Mazowiecki, Pilipczuk, *On Rational Recursive Sequences*, STACS 2023, proves PSPACE hardness of zeroness/equivalence for polynomial-recursive sequences. This explicit family is not presented as a new lower-complexity theorem.

https://drops.dagstuhl.de/storage/00lipics/lipics-vol254-stacs2023/LIPIcs.STACS.2023.24/LIPIcs.STACS.2023.24.pdf

A search for fixed quadratic-degree formulations did not establish priority for this exact normalization; absence of a matching phrase is not evidence of novelty.
