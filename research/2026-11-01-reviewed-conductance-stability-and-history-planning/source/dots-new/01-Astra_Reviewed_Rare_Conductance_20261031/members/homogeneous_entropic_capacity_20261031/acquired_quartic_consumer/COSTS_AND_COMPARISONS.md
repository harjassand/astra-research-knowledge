# Costs, retaining alternatives and scope

## Paid access and computation

The task starts from every rational coefficient of a complete expanded degree8
polynomial, encoded as an n-long exponent vector per monomial. The current
parser scans all coefficients and vectors, acquires the unique aligned absent
axis from F4, kappa, d_min, all graph weights, the coercivity certificate and the
entire identity F=vU. For L nonzero terms this takes O(nL) exponent/coordinate
work and polynomial rational arithmetic in input bit size. Storing a graph as
an expanded polynomial is not magically O(n): a dense graph has L=Theta(m^2),
and these dense exponent vectors occupy Theta(m^3) entries. No hidden basis or
positive-form recognition oracle is granted. Generic rotations can be UNKNOWN.

No external code dependency is needed: compile.py uses Python's standard library.
The producer and receiver both pay acquisition, adaptive grids, exact powers,
integer roots, tail bounds and serialization. The receiver deliberately reruns
the computation rather than trusting the producer's scalar output. Code loading,
input decoding and JSON output are ordinary additional costs; reported timers
start on an already in-memory raw dictionary and do not include fixture creation,
module import, JSON file parsing or serialization. These are not benchmark
claims against optimized implementations.

Finite budgets cover dimension, term count, input/task coefficient bits, maximum
per-piece N, total distinct points across refinements, tail cutoff, fixed root
precision, and power/root-shift intermediate bits. All receiving arguments are
strict typed values (positive Fraction for beta/delta, positive int for budgets).
Unsupported or insufficient cases return UNKNOWN. The power-bit guard applies
to rational numerator/denominator exponentiation and following root shifts,
NOT every Fraction addition, product, accumulated integral or serialized output.
max_power_integer_bits is the largest exact point/tail power numerator or
denominator observed, not a total peak-memory or whole-program arithmetic bound.

## Why rare conductance does not force inverse-rate work here

Each point computes v^m by integer exponentiation and one or two integer fourth
roots. If an endpoint rational v has B bits, its powers have O(mB) bits; the
root shifts add 4P bits. The number of repeated-squaring multiplication steps is
O(log m); their bit costs are paid rather than a unit-cost real oracle. For a
rational geometric grid through T, B=O(input bits+log N+log T). There are
O(N log T) final points plus a constant-factor refinement overhead and the seed.

For unit kappa the logarithmic derivatives are controlled by O(m) on the compact
slab and by O(m/y) on each geometric tail segment. Therefore an adequate
N=O(m/delta) makes the exact endpoint Darboux ratio1+O(delta). Adequate dyadic
precision P=O(m log T+input bits+log(N/delta)) resolves those endpoints. Equation(4)
gives a finite cutoff with log T polynomial in those data for m>=2. This is an
explicit sufficient arithmetic regime, not a statement that the fixed prototype
precision policy succeeds for every adversarial parameter or requested delta.
The prototype may soundly return UNKNOWN; it never assumes missing precision.

For kappa=1, near y=1 the basin mass has a lower bound c/sqrt(m), while near y=0
R0 has a lower bound c'2^(m/4)/sqrt(m). These follow by taking intervals of width
1/(2sqrt(m)), bounding v(1+t)<=1+25/(16m) and
v(y)>=2(1-1/(4m)), and applying (1+x/m)^m bounds. Hence k_free<=C m 2^(-m/4):
this is genuinely exponentially rare in dimension. The algorithm still uses
polynomial-bit powers and scalar quadrature, not O(1/k_free) transition samples.
No general sampling lower bound or #P-hardness claim is needed or established.

## Actual scientific consequence, not only a timing example

All nonnegative static quartic interaction graphs with d_i>=1 and unit beta,
kappa have the same k_free, and their full equilibrium conductances differ by
at most 157/125. Unknown angular partition constants cancel; angular mixing is
not required for the conditional transport proof. It is not correct to infer
identical full rates or equal arbitrary-start kinetics. New model coefficients
must still be read and checked. Reusing just an old scalar rate without checking
the new polynomial is not admitted by the receiver.

## Strong retaining alternatives

1. **Exact homogeneous scaling + one-dimensional free energy.** An equally
   informed ordinary method can obtain q=v^(-m/4) immediately after the SAME
   raw acquisition. This already avoids Z_U and gives the exact restricted
   Dirichlet upper bound. Our capability is NOT a claimed speed advantage over
   this comparator for q or k_free. Its remaining obstacle is a certified LOWER
   bound for the full isotropic diffusion, because projected y is not Markov.

2. **Conventional Dirichlet/Thomson and conditional transport.** These are the
   genuine ordinary primitives used to construct our lower bound. An ordinary
   implementation augmented with the radial current and moment/resistance proof
   in PROOF.md obtains the same result. That is not an independent pre-existing
   win and not an algorithmic separation from ordinary mathematics. Historical
   priority of the assembled theorem remains unresolved.

3. **Homogeneity/virial identities.** The partition scaling, Euler identity and
   Gibbs virial identity are standard. Röver et al.(2023), Section 3 Eq 14, explicitly
   derive the canonical virial trace by integration by parts for general
   potentials. Their sampling-convergence application is not the conductance
   certificate here. We use the exact ensemble identity, not a claim that a
   slowly mixing trajectory has equilibrated. The elementary coercivity bound
   and Jensen inequality are likewise conventional.

4. **Variational committor/profile methods.** Petersen–Lichtinger–Covino(2026)
   already give reaction-rate estimators using equilibrium or reweighted data,
   without requiring observed rare crossing trajectories. Their exact
   flux-fidelity normalization supports a variational upper bound. The paper's
   substitution of basin-average fidelity for flux-weighted boundary fidelity
   is explicitly approximate and can lose that bound direction. It is not a
   located certified counterpart of our analytic full-rate lower bound. We
   retain their stronger sample-access comparator rather than only blind
   crossing counts; no experimental head-to-head was run.

5. **Full elliptic PDE / rare-event sampling / symbolic fiber integration.**
   These remain valid potentially stronger methods outside our grammar and can
   estimate the exact capacity more accurately. No lower bound against them is
   proved. For coupled quartics, separately integrating Z_U is unnecessary for
   this target, even if that integration happens to be easy on a given graph.
   The new consequence is cancellation plus a received kinetic sandwich, not a
   claim that every fiber partition is hard.

## Evidence boundaries

No application was selected from a convenient representation and then passed off
as general science: the broader unmet task is certified rare finite-rate
conductance in high-dimensional stochastic models; this exact sufficient family
is a demonstrated structural boundary. Physical utility for a particular
system, arbitrary bases, coefficient noise, global positivity recognition,
arbitrary basins, angular kinetics and general nonhomogeneous potentials remain
unearned. No chemistry/biology operation, external publication or source-code
upload was performed. The held workstreams and accepted earlier packages are
unchanged.
