# Exact absorption law for an almost-dark label

2026-10-29. Root calculation, receiving review pending. This is a diagnostic for the specific IID label model, not a theorem about arbitrary contaminated source channels.

Let sigma=x|c><c|+a P_W, a=(1-x)/8, W=c-perp in C9, 0<x<1/9. Apply repeated exact antisymmetric growth (fresh record; exact P_(k+1)/I-P_(k+1) measurement; discard only new record on failure) until obtaining wedge8, and then Hodge decode. The generic growth mechanism is prior work, specifically Bene Watts et al., arXiv2610.06737, Algorithm2/Theorem5; root independently developed this noise diagnostic, not the generic algorithm.

By U(8) symmetry the current diagonal exterior mixture has only two weights: v0 for k-subsets without c, and v1 for those containing c. Put v=(1-x,x) at k=1. A successful growth has matrix
 S=[[ (8-k)a/(k+1), 0 ], [ x/(k+1), (9-k)a/(k+1) ]].
The failure transitions between classes are f01=kx/(k+1)^2 and f10=(9-k)a/(k+1)^2. Thus
 F=[[1-sum(S_column0)-f01, f10],[f01,1-sum(S_column1)-f10]].
The failed-repeat sum is (I-F)^-1; update v <- S(I-F)^-1 v. Expected new minus records used at this stage is 1^T(I-F)^-1v. Exact rational symbolic arithmetic implements k=1,...,7.

At k=8 the desired Hodge program corresponds precisely to the subset omitting c, so final infidelity is v1. It obeys
 1-F_program = (9218/315)x + O(x^2).
For x=.001 it is .0287098810; for x=.01 it is .2442051741. At x=1/9 all labels are isotropic and the output infidelity is8/9, correctly containing no information about c. The final output is (1-v1)|conj(c)><conj(c)|+(v1/8)P_conj(W).

For comparison, disjoint one-shot wedge8 projection gives hole weights proportional inverse eigenvalues: infidelity=8x/(a+8x)=64x/(1+63x). The repeated growth procedure has a better leading noise coefficient and much better acquisition yield, but it does not erase dark-direction contamination. No meaningful robustness should be inferred from eventual exact heralds under the ideal support assumption.

The supplied script calculates the exact rational expression, expected number of NORMALIZED MINUS RECORDS (not ordinary source calls), and several evaluations. It does not impose a fixed call cap. A cap changes the conditional output distribution and requires a separate finite-time calculation. No Monte Carlo data or native hardware execution is used here. An independent full-subset CP-map check and cap calculation are pending.

A label-level model must be derived from an actual acquisition instrument before it can be used for physical source error claims. Protected-record storage/control errors and subsequent transducer/gate errors are not included.
