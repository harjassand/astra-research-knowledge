# Independent whole review: unit-mobility-capable well-current MFPT

## Verdict boundary

DRAFT: executable/numerical/receiving checks PASS; final whole acceptance is
withheld pending the independent new-current theorem receipt.

Candidate manifest `well_redistribution_mfpt_20261031/FROZEN_SHA256.json`:
`c8b611cb33803a972c10efc1abe35a883c7d92ce240871e3e4f292cf241bc3fb`.
All 16 explicit files and seven dependency pins were verified and copied; all
original bytes remain unchanged. Principal source bindings:

- New current theorem: `207d9ee314c2c3f4638d0a3c45eaa7e23fd85246010ef799fd538201a0278ab7`.
- New receiver: `4a4603007fd4e339011d0f8fc8eed6a5ff90f298762b74fd8ef8634e8b1adfa0`.
- Author suite: `5e4e407df72551a132f4dc718d0acdfbe91d97f92dd30aae28c3978257c115a9`.
- Inherited accepted constant-SPD code: `7c3a732589bec0aa4240c3970c84be2079421343f791ce68b2e4e92bd65b81ca`.
- Inherited corrected-v2 manifest: `61ace87427769d160cc0c6121377298f02b914059f5018eafe8bc0e30614c298`.

This operation encloses the actual mean first arrival at Y>=1/2 from EXACT FULL
Gibbs conditioned on Y<=-1/2 for the original ordinary constant-mobility
Langevin process. The new current is a mathematical variational witness, not a
new drift, mobility tensor, control law, physical redistribution or sampler.
Dense SPD is within the mathematical theorem with an earned floor, but the
executable grammar accepts only positive isotropic or diagonal constant
transverse mobility, unit longitudinal mobility and zero cross-mobility.

## Actual executed evidence and result

In a clean source-relative copied tree, the author suite passed **5,520 checks**,
actually replaying all four saved cases. Its output report is byte-identical to
the frozen report; diagnostic time was 16.476 s. The new independent suite passed
**1,305 checks**, including **139 UNKNOWN refusals** and all four further actual
recaptures from literal original tasks; diagnostic time was 17.595 s. No candidate
code correction was needed. Floating mpmath checks in the author suite remain
diagnostics; the independent R and Rplus checks below are rational proofs.

| Fiber m | Actual mobility floor | Actual mean interval, diagnostic decimals | Total ratio |
|---:|---:|---|---:|
|128|1|[214677829.3305657,221028415.84478948]|1.0295819392902703|
|256|1|[4.567286514280587e17,4.625077470883771e17]|1.0126532365382572|
|512|1|[4.19289284446448e36,4.2211100912492584e36]|1.0067297800901427|

The fourth case has m=512, coupling 10^100 and diagonal mobility 1,...,512;
its exact outer interval equals that for coupling 20 and I. This does not assert
equality of actual means or distributions.

The new and previously accepted old unit-mobility m=512 records have IDENTICAL
acquisition, full generator, full initialization, basin-mass interval and ordinary
slab-resistance interval. Their complete raw hash is
`e693d5c1ccf5fe43336f3e845d78fdad3a308d0fe88094cc8c4688a5caca76ff`.
Thus tightening the old ratio 1.2569757838742874 to 1.0067297800901427 demonstrably
changes the proof/current, not the received actual dynamics or time convention.
The old production output was already independently replayed in its own receipt;
this comparison reads those immutable source-bound records rather than rerunning
an unrelated old solver for an invented benchmark.

The m=256 model passes its original 1.03 ratio request and honestly refuses a
1.01 request. Very small actual mobility also retains a growing current penalty
and may refuse. Refinement tolerance is not substituted for total structural
width; UNKNOWN is not a lower bound on what every method could achieve.

## 1. New full-state current and the source split

The inherited ordinary constant-SPD theorem supplies global nonexplosion,
reversibility, finite invariant reference measure and the actual killed
zero-resolvent-to-mean identity. Its raw grammar gives positive homogeneous
quartic U, alpha=m/4 integer>=4, d_min, U>=d_min||z||^4/m, and the actual least
mobility mu. The unknown fiber normalizer cancels analytically; no empirical
parameter or angular sampler is acquired.

For normalized pi_s proportional to exp(-beta*s*U),
partial_s pi_s=div_z[z pi_s/(4s)]. In the part of A with v<vstar, the new
j_y=J_A*pi_vstar and j_z=q*(-z/4)*integral_v^vstar pi_s/s ds have divergence
q*pi_v. In the left tail v>=vstar the old conditional current is used. On S,
j_y=M*pi_vstar and j_z=0. Normal longitudinal flux matches at v=vstar and y=-1/2;
tangential jumps in j_z do not generate a delta source across constant-y
interfaces. Full-energy/core justification is part of the new theorem gate,
not inferred from a few symbolic test values.

The density identity pi_s^2/pi_v=[s^2/(v(2s-v))]^alpha*pi_(2s-v) supplies the
parallel slab profile. Coercivity/virial/Jensen bounds the inverse-mobility moment,
not angular mixing. Cauchy in the homotopy parameter bounds the entire transverse
well redistribution without evaluating that homotopy integral or a fiber PDE.
The near-well, middle-well and infinite-tail longitudinal terms are separately
retained. The cutoff sqrt(2) belongs to the proof; conservative rational
extensions produce the finite constants 128 and 16, so no unreceived numerical
irrational cutoff is used.

Crucially, the improved A-current does NOT automatically imply
Q_S<=eta^2 B_new. The new receiver retains an independent conditional S-current,
whose support is the slab and whose energy is bounded by

    B_S=beta*M_S^2*R*(1+C_s).

The old O(1/mu) slab factor is therefore deliberately removed only from the
A-current gate; it remains as an S-source factor. At unit parameters this factor
is 1.256, larger than a 1.01 target, but does not prevent the valid new A-current
certificate. Removing it from S as well would be wrong; the code does not do so.

## 2. Complete finite formulas and directions

Write d=1/alpha, a=1+9*kappa/16, vstar=1+kappa,
G_b=vstar^2/(2*vstar-a), G_1=vstar^2/(2*vstar-1),
K=alpha/[8*mu*sqrt(beta*d_min)],
D=4*alpha*max(kappa,1)/[mu*sqrt(beta*d_min)].
The code uses upward K,D,C_s and upward powers G_b^alpha,G_1^alpha,a^-alpha.
With received scalar intervals M,R,P=Rplus and r>=M_S/M, its U_A is the sum

    beta*M_hi*P_hi,
    beta*M_hi*(1+d-1/2)*G_b_power_hi,
    beta*vstar^2*G_1_power_hi/[128*kappa^2*(alpha-1)^2*d^2*M_lo],
    beta*K_hi*kappa^2*G_1_power_hi/M_lo,
    beta*(1+D_hi)/[16*kappa^2*(alpha-1)^2*M_lo].

Each is in the safe outward direction for B_new/M. It separately returns
U_S=r^2*beta*M_hi*R_hi*(1+C_s_hi). Positivity of the actual resolvent and
source Cauchy yield the mean bound; the rational AM–GM join implemented is

    cross=r*(U_A+beta*M_hi*R_hi*(1+C_s_hi))/2,
    T_hi=U_A+cross,        T_lo=beta*M_lo*R_lo.

The independent suite reconstructed all five A terms, both source bounds and
this cross term, and checked cross^2>=U_A*U_S. It tested non-square beta,kappa,
d_min and mobility factors with exact squared outward-root inequalities. The
minimum coefficient and minimum mobility were deliberately placed on the last
coordinate, verifying complete acquisition rather than first-axis assumptions.

The T_lo expression is earned by the scalar Poisson A-source trial. It is not
an assertion of mean equality with inverse capacity. Finite A/S current energies
and the positive discounted resolvent earn finiteness before taking its zero
limit. Initialization remains the exact FULL Gibbs|A distribution; a fixed ray,
matching energy marginal or small TV preparation is not a received replacement.

## 3. Rplus arithmetic and independent exact integral reference

The one new scalar profile is

    P(y)=[vstar^2/(2*vstar-v(y))]^alpha,  0<=y<=1/2.

Its denominator is positive, v decreases on the half slab, and P decreases there.
It also dominates v^alpha pointwise because the difference of their bases is
(vstar-v)^2/(2*vstar-v). The code performs directed integer powers and monotone
Darboux sums, doubles by evenness, and charges all profile points and products
to the SAME cache, point limit and product budget as M and R.

The loop accepts numerical refinement only when both the M/R product ratio and
P_hi/P_lo meet quad_relative; it then independently checks the actual total
mean ratio. Every explicit well correction remains in that final ratio.
The inherited mass seed, full-infinity tail, cutoff and grid budgets are retained.
The loop is not an unbounded attempt to force structural error below any request.

For every actual kappa=1 case, I independently enclosed the ENTIRE Rplus integral
without using the producer's powers or quadrature. Put x(y)=y^2-y^4/2>=0. Then

    Rplus=2^alpha integral_-1/2^1/2 (1+x(y))^-alpha dy.

All derivatives of (1+x)^-alpha alternate in sign on x>=0. Taylor's remainder
therefore makes degree 160 an upper polynomial and degree 161 a lower polynomial.
Each integrated monomial is exactly

    I_n=4^-n sum_(j=0)^n binom(n,j)*(-1/8)^j/(2*n+2*j+1).

Exact Fraction arithmetic evaluates these finite sums and the signed Taylor
coefficients. Both resulting integral bounds lie INSIDE each production Rplus
interval. Their relative separation is approximately 3.88e-24 at alpha=128,
3.22e-52 at alpha=64 and 3.44e-73 at alpha=32. These are rigorous enclosures,
not sampled comparisons or arbitrary-precision floating estimates.

R was also integrated independently as an exact polynomial. Additional tests
compare 400 Rplus point enclosures to exact rational powers and 12 coarse
Darboux intervals to finer exact rational sums across nonunit kappa and alpha.
Outside-slab and malformed-integration requests are refused.

## 4. Full receiving, budgets and cost scope

The hash-pinned inherited parser scans every energy exponent/coefficient and
every actual diagonal mobility entry. Strict native int and Fraction task types
exclude bool and approximate numerical aliases. Malformed final terms, missing
pure terms, duplicates, odd/nonhomogeneous powers, oversized coefficients,
unsupported dense/radial mobility and incomplete models are refused.
The exact generator is not inferred from local probes or physical measurements.

Verification recomputes from ORIGINAL raw input and externally supplied controls,
then binds every declared proof-bearing field and all eight interval endpoints.
Changing source-A, source-S, cross, Rplus, constants, initialization, model hash,
actual mobility, numerical controls or exact endpoints cannot reuse a certificate.
The core verifier intentionally ignores diagnostic work/seconds/display fields
and unrelated extra annotations; those extras are not authenticated claims.
The subsequent survival wrapper is stricter about extra fields and has its own
separate acceptance. Diagnostic counters cannot change producer budgets because
verification recomputes the operation.

Exact grid, total point, precision, guarded-product and integer-bit boundaries
passed; one-below variants refused. Exact total-width equality passed and a
slightly smaller request refused. Changing beta to nine and actual mobility to
one third multiplied both mean endpoints by nine, preserving absolute-time
factors. A tampered isolated code dependency was rejected before import; no
frozen or clean runtime source was changed for this test.

For either actual m=512 case, the code reads 1,023 terms and 523,776 exponent
entries, plus one isotropic value or 512 diagonal values. At N=32768,T=2,P=512,
it acquires 131,075 scalar points, 131,079 powers and 2,228,343 guarded fixed
products, with three root calls. The largest tracked product bound is 1,154
bits; these unit-parameter roots are exact rationals with small operand sizes.
The independent cache ledger uses points=(J+3)*N+3, powers=points+J+3 for
J=log2(T), and products=powers*[1+2*(popcount(alpha)+bitlength(alpha)-1)],
which agrees with all four actual recaptures.

These counters are not all Fraction operations, isqrt cost, gcd/division,
parsing, hashing, fixture generation, serialization, input storage or peak memory.
The root CALL count is fixed; operand sizes and bit work depend on data,
dimension and precision. There is no dimension-free total input/bit-cost claim.
Raw sizes, complete input scanning and verification repetition remain real costs.
Timings are diagnostics, not an optimized-solver comparison benchmark.

## 5. Ordinary comparison, scope and preserved history

The Rplus scalar building block existed in the earlier finite-Jensen conductance
work. What is newly earned here is the explicit finite-cost full source current,
all well/infinity contributions and correct separate S join needed for the actual
FULL Gibbs|A mean. Giving an ordinary Poisson-current/variational implementation
this same derived witness gives the same result. Verified PDE, averaging and
simulation alternatives receive the same entire model and certificates; rare
crossings alone do not prove those methods expensive. Historical priority and a
generic computational separation are not established.

This receiver does not supply survival/CDF queries, relative tails, exponential
moments, all-start kinetics, model calibration, angular equilibrium sampling or
finite-bit physical initialization. The separate survival consumer requires its
own full source-specific join and receipt. The later universality theorem is not
a dependency in this executable freeze and is not automatically accepted here.

The author's preserved earlier proof wording and test failures remain bound as
history. No frozen source, previous receipt or accepted archive was overwritten.
One audit-side read command used an incorrect relative path for a log and found
no file; it did not alter a file or affect the correctly located survival replay.
There was no denied write, uncertain external operation, helper use or candidate
patch. `dependency_tamper` is an intentionally invalid isolated test copy, not a
runtime distribution. All final source/readback hashes are recorded separately.
