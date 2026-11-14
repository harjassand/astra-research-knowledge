# Independent check of non-target mass and finite certificates

## Non-target lower bound
The n translated solid4R-square configurations are distinct at L=8R. Each contains16R² plus spins versus n/2=32R², so every one lies strictly outside B. Each belongs to the four-corner family (all corner partitions empty), satisfies positive interior, the minus collar and empty exterior companion gas. The interface/field exponent relative to all-minus is exactly -2theta(16R)+2(theta/R)(16R²)=0. Therefore the lower bound applies directly to **Z_(G minus B)**, not merely Z_G:
Z_(G minus B)>=n w_minus.

For the inherited core box-size convention, each plus component is contained in a box of side at most r+2. Its volume is at most(r+2)/4 times its physical perimeter. Summing over components gives Nplus<=(r+2)Ptotal/4; holes do not invalidate this upper bound, and nested filled domains are not being counted as occupied plus spins. Hence w/w_minus<=exp[-k0 Ptotal], k0=2theta-phi(r+2)/2.

The fixed resolved contour representation encodes the full physical domain-wall set, including inner boundaries, with total perimeter Ptotal. The physical-contour count6n4^P overcounts possible contours. Given a compatible wall collection, at most two global spin assignments occur; only assignments lying in the core need the preceding field bound. Dropping compatibility and using1+x<=exp(x) gives
Z_A/w_minus<=2exp[6n q0^4/(1-q0)], q0=4exp(-k0).
No hypothetical all-plus core member is used, and no independent-contour Gibbs model is asserted. This remains conditional on the inherited core-box and planar wall encoding; I found no new geometric assumption beyond them.

## Independent exact arithmetic
`independent_scalar.py/json` is a fresh calculation: it does not import prior scripts or their numerical receipts. It uses rational Taylor LOWER bounds for exp, and rational atanh-series UPPER bounds for log after power-of-two range reduction. All pass/fail comparisons use Fraction arithmetic; floating outputs are display only.

The code independently verifies q0<1/500, the core pressure bound, u4/u1/alpha<1/2, the target-cut contribution versus the structural barrier, and a complete conservative capacity upper
C/ZA<=48n(6nR)^8 exp[-(24/5-7/5-1/R)((32/5)R-4)].
This pays the three numerator terms and the denominator factor2; it uses the already known kappa<=1 only as an upper bound on the positive source-target term. It does not change the clock.

It combines that with the independently calculated energy bound
log K <=log(8n³)+16+(22/7)² R/3,
using pi<22/7 and denominator product<4.

For R80/200/1000/10000 the exact rational computations imply occupation bounds stronger than exp(-612),exp(-1703),exp(-9047),exp(-91930), respectively. Displayed independent log upper values are approximately-615.52,-1708.89,-9070.12,-92136.95. No simulation or floating error estimate is involved in these certificates.

The same exact calculation gives Z_(G minus B)/ZA>=n/3 for the first three instances and>=n/6 for the last. It uses exp(-S)>=1-S directly; at R10000 the rational pressure upper is1536/2495≈.61563, still sufficient.

## Verdict
The claimed high non-target Gibbs mass is genuine for these finite instances under the inherited core convention, and not just failure of an equilibrium upper bound. Thus the exponentially small voltage occupation is not obtainable from v<=1 with this family's Gibbs mass. This strengthens the fair-baseline comparison.

It does not establish coverage of all large domains, current-weighted prevalence, a full mean hitting time, or a new general physical capability. The separate native-flow and capacity geometric proofs remain dependencies even though their scalar arithmetic was independently checked.
