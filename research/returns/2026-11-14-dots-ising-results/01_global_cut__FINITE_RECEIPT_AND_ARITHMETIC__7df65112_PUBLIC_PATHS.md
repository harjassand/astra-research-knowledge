# Complete R200 upper: finite receipt and explicit arithmetic contract

## Result under the stated proof interfaces

For theta4,R200,L1600,n=2560000, original r5 core, original soft source and rate-one heatbath clocks, choose s=79/40. The global trial is the original indicator of M_(s²)\B, not a restricted contour-family potential.

- Filled-area cutoff Vmax=156025.
- Structural old-perimeter threshold S0=1576.
- Physical-perimeter DP cutoff Mper=1900.
- Rational physical-walk activities r=201/200,101/100,51/50.
- Effective tilts are t=2log r<=2phi, not falsely equal to their linear approximations.
- Each contour uses the sharper inherited isoperimetric cap Vp=min(Vmax,floor(P²/16)).

The directed computation gives

 log(T_short) <= -6216.7606208798868...,
 log(T_tail) <= -6818.1574722765074...,
 log(C_kappa/ZA) <= -6202.0050095481845... .

Thus the resulting finite upper certificate is C_kappa/ZA<=exp(-6202), subject to the documented contour-injection/filled-domain and arithmetic contracts. The current previous acquired complete upper was exp(-4136). This is not a comparison with a newly computed exact capacity, an actual energy-edge sampler, or polynomial W/C.

The three directed magnetic runs took approximately107.958,108.613,116.720 CPU seconds in the corrected rerun on this execution environment, and reported no underflow/overflow flags. No R1000 or R10000 magnetic run was executed. All larger-runtime claims remain asymptotic operation counts, not executed results.

## Tail strengthened using the fixed area cap

The physical trace has four choices for its first direction and at most three for each subsequent physical edge. Therefore a rooted actual contour count is at most4n3^(P-1). For P>Mper,

 A_tail <=(4n/3) exp(2phi Vmax)
              (3exp(-2theta))^(Mper+1)/(1-3exp(-2theta)).

This is a bound on actual contours; it need not equal the number of all overcount words used in the truncated DP. The inherited Aall=6n q_s^4/(1-q_s),q_s=4exp(-theta(2-s/2)), still bounds total activity. As before,

 T_tail<=36 A_tail max(1,Aall)^7.

This sharper tail uses only the area cap and the already justified physical nonbacktracking encoding. It is why the finite run can stop at1900 rather than using the older longer crude tail.

## Arithmetic, not an unexplained float claim

CORRECTED EDITION: magnetic_upper.cpp never changes away from FE_UPWARD. It divides volatile rational numerator/denominator operands to obtain separate upper bounds for r and 1/r, then builds both positive power tables by upward multiplication. The earlier mixed-rounding quotient scheme was defective; see the incident report. Every DP addition and multiplication is performed under FE_UPWARD. It uses exact powers-of-two scaling, records the integer scale, and prints coefficients in exact hexadecimal long-double notation. The executed platform reports64 mantissa bits, which the corrected program requires, and passes a rounding-mode test. Endpoint pruning to distance<=min(p,Mper-p) cannot remove any word returning by the cutoff.

The program is compiled with

 g++ -O3 -std=c++17 -frounding-math -ffp-contract=off -fno-fast-math

and its enclosure relies on the documented binary floating-point/compiler semantics and correct directed conversion. No incorrectly rounded libm exponential/logarithm is used inside the magnetic recurrence. Underflow rounded upward would itself be conservative, but none occurred in the recorded large runs.

certify_global_upper.py parses the hexadecimal outputs as exact Fractions. Decimal110 arithmetic, outward neighboring values of correctly rounded ln/exp, and directed operations bound the rational-tilt prefactors. It applies the per-P cap Vp before selecting the smallest valid upper among tilts. A uniform Vmax cap is valid but very loose for small contours when t<2phi; it must not be confused with a physical increase in small-contour mass.

convolution_upper.cpp performs all eight positive convolutions under FE_UPWARD. A perimeter tilt exp(4P) and a common scalar normalization keep the arrays in range. Its final geometric-weight evaluation uses an UPPER for exp(-4) derived from a finite rational lower Taylor sum for exp(4), not an uncharged libm call. Hexadecimal outputs are again parsed exactly. The final scalar script restores every normalization and adds the complete long tail, native n factor, many-small-droplet target crossing, source-target overlap (using known kappa<=1 only for an upper), and1/(1-u4).

## Independent exact checks executed

- All511 nonempty3x3 spin patterns: uniform-resolution dual geometry and280 one-loop area identities.
- Both dual root types, two rational activities, P<=8: area-enumerated moments equal endpoint-only recurrence exactly.
- Physical square trace equals dual moment exactly on the same small cases.
- Compiled directed magnetic outputs at three rational activities,P<=16 dominate independently computed exact Fraction values; maximal relative excess about1.6e-18.
- All eight compiled convolutions/weighted-tail sums in a separate rational toy case dominate exact Fraction answers; excess below6e-19.

These tests support implementation and arithmetic; the general proof still uses the explicit physical-trace injection and inherited cut/core lemmas. Independent geometry/proposal reviews are included; the repair has separate arithmetic review. Numerical tests alone are not a proof of the compiler contract.

## What this does not solve

The overcount law is not an actual energy-edge proposal. Rejecting a walk until it is a compatible simple contour tuple with physical thermal source spins may still be rare. The lower/upper interval remains broad, and original mean acquisition requires its separate normalizer, proposal, decision-time and subtraction-conditioning obligations. The R80 structural diagnostic is additionally dominated by the original trivial C/ZA<=kappa bound; do not promote that tuple as an improved best full-capacity upper.
