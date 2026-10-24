# A paid encoded-quantum preparation operation for the weak-bridge family

24 October 2026. Owned constructive extension after the canonical-coherence
proof and its independent whole reviews. This is a compiled quantum algorithm
in an explicit universal-gate model. It is not an acquired material control
scheme, a natural Hamiltonian ground-state result, a fault-tolerant device, or
a demonstrated speedup over an equally informed tensor-network method.

The operation closes a different interface from classical contraction: prepare
the specified hard-projected canonical state, then optionally measure a
configuration. It does not assume a completed corrector, a continuous bath
output, a normalizer oracle, an exact mean oracle, or a free global projector.
The parent-gap and elementary adiabatic machinery have strong established
ancestors. The native nonnormal-filter representation, its explicit gap
certificate, and the paid particle-number/precision interface are given here.

## 1. Input, output, and declared quantum primitives

Use an explicitly supplied symmetric zero-diagonal `F in Q(i)^(n by n)` and
an acquired or verified partition into bounded-size even-parity reference
blocks. Cross physical degree is at most fixed `Delta`; the simple block graph
has degree at most fixed `D`. Block size is at most fixed `b`. All norms below
are on the no-double-occupancy Hilbert space, with local basis `0,up,down`.
The exact graded edge representation is the one already proved in
`BLOCK_CANONICAL_OBSERVABLES.md`; it is not an assumed PEPS oracle.

The abstract quantum computer supplies a fixed finite universal gate set with
inverses, computational measurements, initialized qubits, resets, and classical
feedforward. Gate approximation is charged below. A physical realization must
meet the stated accuracy budget; its availability is not established by this
theorem. No error-free hardware or cost-free fault tolerance is inferred.

The general parent lemma below applies to any explicitly computed normalized
even block reference. For the complete tilt/preparation protocol specialize to
the actual four-site family of `CANONICAL_COHERENCE.md`: on every block
`F_01=F_23=F_02=F_13=1`, and all other internal entries vanish. There are `M`
blocks, `n=4M`, maximal pair number `m=2M`, and target `k=M`. Its finite native
reference polynomial is `B(r)=1+8r+4r²`.
For this specialization the input check verifies the complete internal pattern,
not merely the size of a component found by thresholding its entries. When
`lambda<1/2`, thresholding at `1/2` first recovers the candidate blocks; direct
entry and degree checks then accept or reject this promised family.

The required output is a success flag and, when accepted, an encoded state
within requested half-trace distance `epsilon` of

```
|Psi_k(F)> proportional to P_(N=2k) P_G
       exp(sum_ij F_ij c†_(i,up)c†_(j,down)) |vac>.
```

An abort budget `xi` is also supplied; take `0<epsilon,xi<=1/2`. Reading the
accepted state in the occupation basis supplies a QUANTUM-generated sample
within the same total-variation error. It does not give a classical sampler.
The input matrix and partition are classical data, not experimentally acquired
wavefunction parameters. A general diagonal congruence remains a physical
occupation filter at finite holes and is not used as a free gauge.

## 2. Exact local parent path without a global condition-number assumption

Fix a positive fugacity `r`. Let `|omega_B(r)>` be the normalized exactly
computed hard reference state on block `B`, and put

```
|Omega_r>=tensor_B |omega_B(r)>,
P_B=I-|omega_B(r)><omega_B(r)|.
```

For each cross edge define the hard projected singlet creator `C_e†` as before.
It has norm at most two and squares to zero. Disjoint creators commute as even
operators. Creators sharing a site have zero product in EITHER order, because
they would create double occupancy. Thus all these creators commute exactly.
For `0<=s<=1`, set

```
g_e(s)=I+s sqrt(r) E_e C_e†,
g_e(s)^(-1)=I-s sqrt(r) E_e C_e†,
G_s=product_e g_e(s).
```

Their factors are invertible, commuting and generally NONNORMAL. Applying them
as postselected gates is not the claimed algorithm; that route can have a poor
global success probability.

Let `G_B(s)` contain exactly the edges incident to block `B`, and define

```
A_B(s)=G_B(s) P_B G_B(s)^(-1),
h_B(s)=A_B(s)† A_B(s),
H(s)=sum_B h_B(s).                                              (1)
```

`h_B` is supported in the closed block neighborhood `N[B]`, at most
`b(1+D)` physical sites. Every omitted factor in `G_s/G_B` avoids `B` and
commutes with `P_B`, while all edge factors commute with each other. Hence

```
A_B(s) G_s=G_s P_B.                                            (2)
```

It follows that the common kernel of the `h_B` is precisely the one-dimensional
space spanned by `G_s|Omega_r>`. Thus (1) is a local frustration-free parent
path with the desired grand state as its unique ground vector.

The SAME argument must hold for every PAIR of constraints. Let `G_BC` contain
the union of all edges incident to `B` or `C`. A factor in `G_BC/G_B` avoids
`B`, so

```
A_B G_BC=G_BC P_B,      A_C G_BC=G_BC P_C.                      (3)
```

Consequently `ker(h_B+h_C)=G_BC ker(P_B+P_C)` on the finite union support.
The nullity is exactly the original nullity, not just approximately continuous.
The global norm or condition number of `G_s` can grow exponentially with `M`;
it is NOT used to estimate the gap.

## 3. A native uniform gap test and its full proof

Take `r in [r_lo,r_hi]`. Acquire a rational

```
e >= 2 sqrt(r_hi) lambda,
ell=b Delta,
L=(1+e)^ell,
delta=L^4-1.
```

Square-root upper intervals or squared rational comparisons pay the first
bound. There are at most `ell` edges incident to a block. Each `g_e` and its
inverse has norm at most `1+e`, and each differs from identity by at most `e`.
Thus, uniformly in `s,r`,

```
||G_B||,||G_B^(-1)||<=L,
||G_B-I||,||G_B^(-1)-I||<=L-1,
||A_B-P_B||<=L²-1,
||h_B-P_B||<=delta.                                           (4)
```

The last line follows from `||A†A-P||<=(||A-P||)(2+||A-P||)`.
Assume the explicit rational test

```
delta(1+3D²)<=1/2.                                            (G)
```

For a single term, (2) preserves the rank of `P_B`. Weyl's eigenvalue bound
and (4) therefore put every NONZERO eigenvalue of `h_B` in
`[1-delta,1+delta]`. In particular

```
(1-delta)h_B <= h_B² <= (1+delta)h_B.
```

For a pair, (3) preserves the nullity of `P_B+P_C`, whose nonzero eigenvalues
are one and two. Since the pair perturbation has norm at most `2delta`,

```
(h_B+h_C)² >= (1-2delta)(h_B+h_C).
```

Subtracting the upper single-term squares gives

```
{h_B,h_C} >= -3delta(h_B+h_C).                                 (5)
```

If the two closed neighborhoods are disjoint, the even terms instead commute
and their anticommutator is positive. A closed neighborhood overlaps the closed
neighborhoods of at most `D+D(D-1)=D²` other centers. Summing (5) only over
those unordered pairs yields

```
H(s)² >= [1-delta(1+3D²)] H(s) >= H(s)/2.                      (6)
```

The path gap is at least one half for EVERY `s in [0,1]` and every fugacity in
the bracket. This proof uses actual local similarities and fixed pair-kernel
dimensions; closeness of extensive Hamiltonians in operator norm would not
give it. It is an analytic finite-overlap certificate of the conventional
`H²>=gap H` kind.

## 4. A genuine larger sufficient family, without a classical norm oracle

For the four-site example take `[r_lo,r_hi]=[1/4,1]`, `ell=4Delta` and
`e>=2lambda`. In addition to (G), require

```
ell e<=1/128.                                                 (T)
```

This is a size-independent nonempty bridge regime. For instance a degree-three
block graph can allocate one of three different physical ports of each block
to each neighbor. Then `Delta=1`, `D=3`, and `lambda=1/2000`, `e=1/1000`
give

```
delta=(1001/1000)^16-1,
1-28delta > 1/2,
ell e=1/250<1/128.
```

The displayed inequalities can be checked with exact integer arithmetic. Such
graphs may have growing width and need not be bipartite. This scale is far
outside the earlier deliberately crude KP certificate, but does NOT show
classical hardness, practical affordability, or an advantage over stronger
classical algorithms on these matrices. It only separates the two proved
sufficient tests. An equally informed compiler can use the same gap argument.

We now acquire the fugacity using quantum data from a fully specified circuit,
not hypothetical native data. First prove the bracket independently. There are
at most `M ell/2` cross edges, and the exact representation gives on the positive
ray

```
|log Z(r)-M log B(r)| <= M ell log(1+e) <= M ell e.              (7)
```

This follows by bounding the norm and inverse norm of the full `G` and then
taking logarithms. The bound is used ONLY for this extensive log comparison;
it is not an efficient preparation or a global gap estimate.

Write `Lambda(t)=log Z(exp t)`, whose derivative is the mean pair count. It is
convex because the coefficients of `Z` are nonnegative. The exact reference
secants satisfy

```
log[B(1/2)/B(1/4)]/log2 = log(24/13)/log2 < 15/16,
log[B(1)/B(1/2)]/log2 = log(13/6)/log2 > 17/16.
```

The first is the integer comparison `24^16<13^16 2^15`; the second follows
from `13/6=4/(24/13)`. Equation (7), `log2>1/2` and (T) imply

```
mu(1/4)<31M/32 < M < 33M/32<mu(1).                            (8)
```

No actual finite sample is asserted in (8). It is a proved prior bracket for
the number-measurement calibration protocol below.

## 5. Compile and pay one approximate grand-state preparation

All local block states and every finite matrix in (1) are computed directly
from the supplied entries and `r`. The local dimension is
`3^(b(1+D))`, a fixed cost here. Rational-complex arithmetic, square-root
intervals and normalization bits are charged; exponentially large internal
block amplitudes require their input bits, not exact-real oracle access.

Useful derivative bounds, with derivatives in `s`, are

```
J0=L^4,
||h_B||<=J0,
||h_B'||<=J1=4ell e L^4,
||h_B''||<=J2=16ell²e² L^4.                                   (9)
```

Differentiate the at-most-`ell` linear factors of `G_B` and of its exact inverse:
their first derivatives are at most `ell e L` and their second derivatives at
most `ell²e²L`. The product rule then gives (9). Consequently
`||H'||<=M J1`, `||H''||<=M J2` uniformly. The path starts in the known product
`|Omega_r>` and has rank-one ground projection and gap at least one half.

The explicit finite-dimensional bound of Jansen--Ruskai--Seiler, Theorem 3,
therefore gives final leakage amplitude at most `C_M/T`, where it is safe to use

```
C_M=8M J1+4M J2+56M²J1².                                     (10)
```

Its rank-one leakage bound is also the half-trace distance to the desired pure
ground state. Choose a physical simulation time `T=max(1,8C_M/eta)` for a
requested FULL trace-norm error budget `eta` per completed grand-preparation
and number-measurement instrument. The energy unit in (1) is a compiled
algorithmic choice; this time is not a measured device duration.

A simple paid digital implementation suffices. Divide `[0,T]` into `J` equal
steps, hold each `h_B` at its midpoint, and use a first-order product of the
local exponentials at each step. Only at most `D²` terms overlap any term.
Unitary Duhamel and Lie-product estimates bound the total operator error by

```
[M J1 T+M D² J0² T²]/J.
```

Thus `J>=8[M J1 T+M D²J0²T²]/eta`, rounded up to at least one, pays a small
constant fraction of the state-error budget. Initial block-state synthesis,
local exponential synthesis, the number counter/readout and any actual gate
noise share the remaining budget; each of a counted `L_gate` elementary
operations may be allocated `O(eta/L_gate)` diamond error. Telescoping is the
bound, with no iid noise assumption. Standard finite universal synthesis adds
polylogarithmic precision overhead for the bounded-size unitaries. The constant
can be exponential in `b(1+D)`, which is fixed, not hidden polynomial in a
growing degree or block size.

There are `O(MJ)` local exponentials. Even on a line of encoded qubits, their
supports can be routed into a contiguous window and back using `O(n)`
fermionic site-swap gates per term, at fixed local support size. A site swap
exchanges its two spin modes WITH the phase from crossing occupied modes.
It is a bounded-size unitary, not an ungraded permutation. This charges
`O(nMJ)` routed local operations before synthesis. The earlier interleaved-block
shuffle bug in a finite classical helper is not repeated here. Initial block
preparation likewise routes an arbitrary interleaved partition with these graded
swaps; its polynomial routing cost is included before the adiabatic steps.

Use two qubits per physical site, reserving the three basis states for
`0,up,down`; the fourth is invalid. Ideal compiled local unitaries extend
block-diagonally to the invalid subspace and preserve the valid hard code.
Routing entire sites preserves that encoding. The ideal adiabatic theorem
applies in this invariant hard subspace; a penalty on invalid states could
also be compiled. Approximation/leakage errors are included in `eta`.
The register has `O(n)` data qubits and `O(log n)` counter/work bits at fixed
local dimension, with bounded extra synthesis workspace.

The resulting per-call cost is polynomial in `M,1/eta` and the input bit length.
For fixed structural constants, a deliberately unoptimized routed bound is
`O(M^7 eta^(-3) polylog(M/eta))` elementary operations, plus polynomial-bit
classical matrix and compilation work. Nothing here claims this large bound is
competitive. An optimized known local adiabatic algorithm is allowed as the
conventional comparator.

This parent generally BREAKS number conservation: the reference block and
`P_B` mix pair numbers. Universal ENCODED qubit control can implement it, since
the occupations are logical labels. A material realization with exact native
`U(1)` control would additionally require a pair reservoir/phase reference or
a different number-conserving construction. Those are not supplied here.
Global fermion parity is even throughout the ideal path.

## 6. Actually acquire the mean and choose the tilt

The internally reconstructed scalar-charge theorem applies to the FULL norm
polynomial even outside the KP certificate. Its positive-real tilted charge
law is Poisson-binomial. In particular

```
d mu/d log r=Var_r(K),       0<=Var_r(K)<=m/4.
```

These structural facts do not provide the factors to the algorithm. To evaluate
a mean, prepare the approximate grand state by section 5 and reversibly count
total occupation in `O(n log n)` gates and `O(log n)` workspace. Measure the
counter. Divide the result by two and clip it to `[0,m]` if needed. Odd/invalid
outcomes under faulty execution count toward the instrument-error budget; the
ideal state has only even total number. The counter is not a measurement of
individual site occupation, which would destroy the desired coherence.

Allocate full trace error at most `eta_mean=1/(128m)` per such complete trial.
This guarantee is conditional on every causal past, including all preceding
measurement outcomes. A trial begins with reset/reinitialization of its data
and counter, and includes the number measurement and readout. Reset error
cannot be left outside this completed-instrument budget.
The resulting mean bias is at most `1/128`. Use

```
B_calls=ceil(log2(64m))+4,
delta_conf=min(epsilon,xi)/16,
L_samples=ceil[8192m² log(2B_calls/delta_conf)]                  (11)
```

fresh preparations per queried fugacity. The empirical mean is within `1/32`
of the true mean simultaneously for the at most `B_calls` queried fugacities,
except with probability `delta_conf`. Hoeffding at tolerance `1/128` and a
union bound suffice, with spare constants. In the noisy version one may use
the conditional Hoeffding martingale bound if each complete trial obeys the
uniform error guarantee after every past history; arbitrary persistent drift
without that guarantee is not covered.

Starting with the proved bracket `[1/4,1]`, use rational bisection. If an
empirical midpoint mean is within `1/8` of `k=M`, stop. Otherwise its estimated
sign is correct on the confidence event and the corresponding half-bracket
is retained. If the width reaches `r_lo/(16m)`, use its midpoint. Since
`d mu/dr<=m/(4r_lo)`, this last width also guarantees a true mean within `1/4`
of `k`. Thus the returned rational tilt has

```
|mu(r)-k|<=1/4                                                (12)
```

on the confidence event, using only the paid quantum circuit and bounded
classical arithmetic. Adaptivity requires bounds conditional on the acquired
past; it does not require a confidence union over unvisited fugacities.

This step can be replaced by the deterministic KP tilt evaluator when its
stronger certificate happens to pass. It is not assumed to pass in this note.

## 7. Number projection, accepted-state accuracy, retries and reset

At a tilt obeying (12), the all-size unimodal mass bound already reconstructed
in the canonical proof gives

```
p_k=Pr_r(K=k)>=a_m=3/[4(m+1)²].                               (13)
```

There is also a sharper supplied-family bound independent of KP. Bernoulli
variances change by at most a factor four over `[1/4,1]`. Equation (8) implies

```
M/16 <= mu(1)-mu(1/4)
       = integral_(log(1/4))^0 Var(K) d log r
       <=4log4 Var_r(K)<8Var_r(K).
```

Hence `M/128<=Var_r(K)<=M/2` throughout this bracket. For
`M>=128*160²`, the explicit finite local CLT in `CANONICAL_COHERENCE.md` gives

```
p_k>=1/(8sigma)>=1/[8ceil(sqrt(M/2))].                         (14)
```

Use the stronger applicable rational lower bound `a` from (13),(14). No variance
oracle or Bernoulli factor computation is needed. Small sizes are covered by
(13), rather than an unproved central limit approximation.

For an ideal grand state, measuring ONLY total number and accepting `N=2k`
produces exactly `|Psi_k(F)>`: every component in this sector has the same
fugacity scalar `r^(k/2)`. Therefore different adaptive choices of positive `r`
do not change the ideal accepted target. The counter measurement retains
within-sector coherence. The number projector is a concrete circuit, not a
given completed operation.

For robustness, if the full classical-quantum trial instrument differs from
the ideal one by at most `eta` in trace norm, its accepted subnormalized block
differs by at most `eta`. Success probability is at least `p_k-eta`, and the
conditional accepted HALF-trace distance is at most

```
eta/(p_k-eta).                                                (15)
```

This follows by adding the normalization difference to the subnormalized block
error. False acceptance/readout, not just a unitary state error, is included.
Use `eta_final=epsilon a/32`. Then each successful trial on the confidence
event has distance less than `epsilon/8` from the target and conditional success
probability at least `a/2` after every prior failed trial.
Here too the full instrument guarantee is uniform conditional on each past
failed branch and includes the reset/reinitialization that starts the next
attempt. An uncontrolled persistent error across attempts is not covered.

Cap final attempts at

```
R=ceil[(2/a)log(8/xi)].                                       (16)
```

On the confidence event the abort probability is at most `xi/8`; the bad
calibration event has probability at most `delta_conf`. Thus total abort
probability is below `xi`. Its weight among accepted outputs is at most
`2delta_conf<=epsilon/8`, so the averaged ACCEPTED state is within the requested
`epsilon` (in fact a smaller spare bound) of the target. This explicitly avoids
forgetting that later acceptance can condition on a failed calibration branch.

The number of complete grand preparations is at most
`B_calls L_samples+R`, all polynomial at fixed structural parameters. Expected
final attempts are at most `2/a+delta_conf R`; the cap controls even a mistaken
calibration branch. In the large-variance range (14), the final projection alone
needs `O(sqrt(M))` expected attempts, but mean acquisition still costs the
polynomial sample budget (11). No lower total scaling is inferred from that
projection-only fact.

After each failed number measurement, reinitialize all data and counter qubits;
charge `O(n)` resets and their error. The procedure discards failed coherent
states and produces classical number records. It is not a thermodynamically
reversible preparation claim. Control memory, gate time, resets, routing and
approximation precision have been stated; monetary/device costs remain
unacquired. No amplitude amplification shortcut is used. Adding one would
require the complete inverse preparation and accurate charge/reference
reflections, with their own error budget.

## 8. Strong conventional comparison and scientific claim boundary

I read Ge--Molnar--Cirac,
[Rapid adiabatic preparation of injective PEPS and Gibbs states](https://arxiv.org/html/1508.00570),
main equations (3),(5),(6), Appendix C and the high-temperature gap argument
in Appendix D. Their general displayed filters are strictly positive Hermitian
and commuting; the present nilpotent nonnormal factors are not automatically
that representation. Their parent-state and local adiabatic preparation
machinery is strong ancestry. Their faster implementation theorem is not
imported without a separate representation and path mapping. The actual
algorithm here uses (1), its proved gap, Jansen--Ruskai--Seiler and the explicit
product-formula compilation above. No new general adiabatic principle or
superior gate complexity is claimed.

I also read Cruz et al.,
[Preparation and verification of tensor network states](https://arxiv.org/html/2105.06866),
sections II--III. Their local pair SDP explicitly certifies `H²>=gap H` and
is a direct equally informed competitor. Our fixed-kernel/Weyl argument is an
explicit analytic feasible bound for this actual parent family. The input state
class is outside their displayed positive-commuting-filter parametrization
unless a further representation is shown, but the gap-test concept is not new.
An implementation may replace the conservative analytic bound by their local
SDP when it certifies the whole path.

The adiabatic bound used above is the primary
[Jansen--Ruskai--Seiler Theorem 3](https://arxiv.org/html/quant-ph/0603175).
Bounded-size universal compilation uses the standard
[Dawson--Nielsen Solovay--Kitaev construction](https://arxiv.org/html/quant-ph/0505030),
whose theorem, instruction-set assumptions and error telescoping were read.
These are supplied established primitives with their assumptions, not our
scientific discoveries.

For general projected-BCS preparation, the strong current comparator is
[Kang et al. AAGP](https://arxiv.org/html/2606.06919), equations (109),(133):
amplitude amplification improves a global Gutzwiller postselection of weight
`W` from `1/W` to `O(log(1/delta)/sqrt(W))` BCS queries. That paper is an arXiv
v1 preprint; its numerical weight fit is exponential in its tested lattice size,
and those data are not our matrices. Its displayed BCS/RVB ansatz has particle-
number fluctuations: this is a Gutzwiller-only comparator, not an acquired
fixed-`N` projection cost. At our zero-bridge reference, global Gaussian
preparation followed by `P_G` has weight `(2/3)^M` at `r=1/2`, since the Gaussian norm per block is
`(1+4r)²=9` and the hard norm is six. But an equally informed blocked compiler
already prepares EACH finite hard block directly in polynomial total cost.
It would be misleading to claim an advantage over that compiler by comparing
only to its unnecessary global projector. The meaningful added question is
nonzero weak bridges; the explicit local path and paid charge calibration close
one such controlled operation. No quantum/classical separation follows.

On the smaller KP-certified subset, the preceding theorem additionally proves
pair ODLRO. The wider preparation certificate (G),(T) by itself proves neither
that property nor a ground state/stiffness claim. This entire result is an
encoded state-preparation/sampling algorithm for a supplied ansatz family,
not an acquired native superconducting or chemical capability. Priority remains
unresolved. Root and the four existing exposed Luna supports independently
challenged the kernel, gap, source and resource steps; the owner retains the
whole proof and does not elevate their agreement into physical validation.

The same information also permits a conventional inverse-dressing parent
`h'_B=(G_B^(-1))† P_B G_B^(-1)`. It has the same local/global kernel identities
and the tighter estimate `||h'_B-P_B||<=L²-1`; the same finite-overlap proof
therefore improves constants. The valid but conservative construction (1) is
retained above. Its certificate or gate count is not claimed optimal even
within this state family.

## 9. Finite diagnostic and exact review scope

`check_preparation_gap.py` and `PREPARATION_GAP_CHECK.json` preserve one executed
27-dimensional hard-qutrit diagnostic. Three vacuum-reference sites on a
triangle use coefficients `(lambda,i lambda,-lambda)`, with `lambda=1/1000`.
It checks creator nilpotence/commutation, the exact local similarity identities,
pair nullities, pair anticommutator inequalities and the global gap inequality
at `s=0.37,1` in floating arithmetic. The analytic lower gap bound is about
`0.790538`, while the two measured matrix gaps are about `0.99999986` and
`0.99999900`. These are eigenvalues of explicitly constructed finite matrices,
not measured device gaps. Exact integer checks separately verify the four-site
family's displayed gap and reference-secant inequalities. This fixture tests
the general parent lemma; it does not execute the four-site-block protocol,
the adaptive sampler, or a large-size adiabatic preparation.

All four existing Luna supports independently checked bounded parts of the
saved precursor of this note: the local algebra and constants, adaptive
calibration and postselection, compiled interface/cost, and primary-source
comparators. Their findings were rederived by the owner. The present clarity
changes include their reset-history and comparator-scope qualifications.
Parent supplied independent derivations of the kernel and gap route. The
separate canonical-coherence theorem already has parent and another Sol whole
reviews; no separate whole-Sol review of this NEW preparation theorem has yet
been received. Agreement and finite replay do not settle priority.

After this preparation construction had been saved, a team-status inventory
exposed brief final summaries of other completed owners. No result from those
summaries enters this construction. Earlier parent scientific input and the
four supports are actual development exposure, rather than blind replication.

The closed claim is thus a polynomial-cost, precision-controlled ENCODED
quantum preparation and heralded sampling operation for the supplied native
weak-bridge family satisfying (G),(T), including paid mean acquisition and
failed-branch reset. It does not depend on passing the older classical KP test.
Whether a substantially stronger classical contraction certificate covers
this wider family, or this path gives any practical or asymptotic comparative
advantage, remains open here. The small-bridge ODLRO theorem retains its own
stronger hypotheses. None of these statements acquires an experimental
superconductor, a material ground state, a device noise guarantee, or a
civilisation-changing discovery.
