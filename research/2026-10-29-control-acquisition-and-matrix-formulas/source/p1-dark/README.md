# Astra P1: acquiring a reusable law despite dark controls

**Completed continuation, 28 October 2026.** The construction now acquires a
uniformly certified intervention law from finitely many noisy scalar readings
without resolving each coupling, identifying hidden rank, or discarding dark
controls. It then certifies continuous conductance and compliance decisions
from the same record. A second result gives a positive rational representation
with a sharp factorial truncation bound. Economical acquisition of that second
representation remains open.

This is a mathematical and executable synthetic result for a specified source
class. It is not a device demonstration, a universal speed or photon advantage,
or an independently audited foundational breakthrough. The useful capability
is reuse: experiments can support later intervention questions that were not
specified at acquisition time, while uncertainty remains visible in the answer.

## 1. The obstruction selected

The preceding continuation established the unnormalized response representation
and retained dark controls in an uncertainty family. Its inexpensive normalized
compiler still needed resolved couplings. Moving to a positive reference can
illuminate a dark control algebraically, but generic nonzero coupling does not
give a finite-noise conditioning guarantee. Identifying every relevant control
at a fixed bounded error is impossible without a relevance margin.

Three openings were developed before committing the main continuation:

| Opening | What it can remove | Decisive remaining condition |
|---|---|---|
| Acquired positive reference and de-embedding | Baseline darkness for a sufficiently resolved source | Must pay for discovery and verify conditioning; genericity is insufficient |
| Entire scalar Stieltjes curves along selected rays | Weak-pole identification along a ray | Too few rays leave angular response unresolved; even the linear subclass needs at least n informative scalar directions for a sufficiently accurate uniform law |
| Direct approximation of the whole intervention law | Any need to resolve individual couplings before prediction or control | Must pay for finite multidimensional acquisition and certify approximation plus measurement error |

The third opening was selected and executed. The shifted route's positive
results, finite excitation procedure and failures are preserved in
`shifted_theorem.md`, `shifted_excitation.md` and their exact runs. The ray
obstruction is proved in `selection/inference_ray_obstruction.md`. None of these
results deletes the earlier reciprocal receiver construction or changes its
information model.

## 2. Source and acquisition contract

The governing response is

\[
J(u)=c_0+g^TP(I+PBP)^{-1}Pg,\qquad
P=\operatorname{diag}(\sqrt{u}),\qquad B\succeq0,
\]

on \(u\ge0,\ \sum_i u_i\le\delta\), with warranted bounds
\(c_0>0,\ |g_i|\le G,\ B_{ii}\le\kappa\). There is no positive lower bound on
\(|g_i|\) and no low-rank assumption. This follows from the retained affine
positive quadratic-form source. Its fixed rank-one actuators and scalar boundary
response are part of the contract. A canonical positive quadratic realization
does not establish realization by every local resistor graph, mechanical
apparatus or electromagnetic target.

The fresh emulator has \(\delta=1/5\) and reports \(R=3/2+J\). Its receiver has
unknown shared gain and offset. Two acquired known standards enclose both. Raw
errors are deterministically bounded and correlated; they are not assumed to
average away. The runs use 20-bit inward-rounded actuation and 24-bit readout.
The source offset \(3/2\), source class, bounds \(G,\kappa\), known standards,
stable receiver, settling and reset are declared emulator specifications. A
physical implementation must establish them. Receiver calibration alone does
not identify an unknown constitutive offset for the transformation \(Z=1/J\).

The learner uses command/response intervals and these declared bounds. Hidden
vectors and determinant/cofactor responses enter only the post-decision
checkers. No equipment was operated.

## 3. Completed finite whole-law acquisition

At degree \(k\), acquire every simplex lattice node

\[
u_\alpha=(\delta/k)(\alpha_1,\ldots,\alpha_n),\qquad
\sum_{i=0}^{n}\alpha_i=k.
\]

There are \(M=\binom{n+k}{k}\) scalar source readings, including zero once.
Each acquisition uses at most \(k\) active controls. Every reported interval
includes calibration, raw error, quantization and the discrepancy between the
requested lattice node and its actual DAC command.

The same finite record gives two complementary representations.

**Interpolating representation.** With barycentric coordinates
\(\lambda_0=1-\sum u_i/\delta,\lambda_i=u_i/\delta\), the cardinal basis is
\(L_\alpha=\prod_i\binom{k\lambda_i}{\alpha_i}\). Its dimension-uniform
Lebesgue bound is

\[
\sum_\alpha|L_\alpha(u)|\le C_k=\binom{2k-1}{k}.
\]

This constant is sharp over dimensions for this lattice. If the largest
acquired node radius is \(\epsilon\), \(q=\delta\kappa\), and \(p_k\) is the
acquired interpolant, the proved all-command enclosure is

\[
\|J-p_k\|_\infty\le C_k\epsilon+
\min\left\{
\frac{C_k+1}{2}\frac{\delta G^2q^k}{1+q},\quad
(C_k+1)\frac{\delta G^2}{T_k((2+q)/q)}
\right\}=:E.
\]

The Chebyshev polynomial is a proof comparator, not an unmeasured input to the
learner. For \(q=0\), the model bias is zero. Shared additive calibration error
can be retained without multiplying it by \(C_k\); the executed independent
interval enclosure is conservative about that correlation.

**Positive Bernstein representation.** Multinomial weights are nonnegative
and sum to one. For the exact source,

\[
0\le J(u)-B_kJ(u)\le C:=\delta^2\kappa G^2/k.
\]

Therefore the same noisy record gives an interval of width at most
\(2\epsilon+C\), with noise amplification one. The proof uses the source's
energy minimization and multinomial variance. It does not assume that a
multivariate Bernstein approximation preserves concavity, or that every
individual residual is bounded by \(G\).

The positive representation works for every finite \(q\). Both methods pay
the combinatorial acquisition cost; neither makes arbitrarily small error
possible at fixed nonzero sensor and actuation error. Increasing degree can
make interpolation worse. The two valid query intervals are intersected.
The complete proof and exact transform are in
`theory/SIMPLEX_LAW_ACQUISITION.md` and `code/simplex_law.py`.

## 4. Continuous decisions without new source measurements

For a later known price vector \(c\), the task can maximize either
\(J(u)-c^Tu\) or \(-1/J(u)-c^Tu\). The latter is compliance reduction minus
price up to a shared baseline, which cancels from regret.

The first control construction takes convex combinations of acquired lower
response points. Concavity of the true source makes these feasible lower
values. Separate outer hypographs come from the positive approximation and
the interpolant's Bernstein coefficients plus its error. After mapping each
point to response and price, optimizing the scalar increasing concave utility
reduces to a two-dimensional lower-cost convex hull. Two nodes suffice for a
proposed deterministic mixture. The command is rounded inward and all lost
response allowance and actual-command costs are retained.

This closes a continuous-domain certificate, but the outer hull can be loose.
The next construction repairs that limitation using **the acquired
polynomial's curvature**, without recovering source gradients.

For degree \(k\), its Bernstein Hessian has
\(\binom{n+k-2}{k-2}\) rational coefficient matrices. A numerical eigensolver
only proposes \(\mu\ge0\); exact rational LDL checks prove that each matrix
is at most \(\mu I\). A rational Gershgorin fallback guarantees a checkable
bound. Consequently \(\nabla^2p\preceq\mu I\) throughout the simplex.

For any finite feasible candidate \(x\), Taylor's inequality and convex
vertex maximization give

\[
\max_u[J(u)-c^Tu]\le p(x)-c^Tx+E+
\max_{v\in\{0,\delta e_1,\ldots,\delta e_n\}}
\left[(\nabla p(x)-c)^T(v-x)+\tfrac\mu2\|v-x\|^2\right].
\]

For compliance, the globally valid tangent
\(-1/J\le-2/j_0+J/j_0^2\), with any \(j_0>0\), supplies the corresponding
bound. The code uses \(j_0=p(x)\) when positive, and a warranted positive
baseline otherwise. Positive acquired lower values give candidate rewards.
The minimum of valid global upper bounds and maximum of valid candidate
lower bounds give a regret certificate. SLSQP proposes commands; its success
flag is never a certificate. Numerical proposal failures retain the preceding
command. Polynomial gradients need not approximate true source gradients.

For cubics, the Hessian coefficient matrices are the actual Hessians at the
simplex vertices. Thus this curvature representation adds no coefficient
relaxation at that step. Full proofs and implementation are in
`theory/HYPOGRAPH_CONTROL.md`, `theory/POLYNOMIAL_CURVATURE_CONTROL.md`,
`code/hypograph_control.py` and `code/polynomial_curvature.py`.

## 5. Executed results and full cost scope

Five fresh exact rational synthetic sources were acquired. Every case ran
three later conductance tasks and three compliance tasks, with no additional
source readings for their decisions or certificates. All intervals and
certificate comparisons passed their exact post-decision checks.

| Source | Degree | Dark controls | Raw error bound | Source + calibration readings | Nonzero writes; individually cleared reset writes | Uniform interpolant error in J |
|---|---:|---:|---:|---:|---:|---:|
| Exact pair | 4 | 1 of 2 | 1e-6 | 15 + 2 | 20; 20 | 0.000409602 |
| Mixed six | 3 | 4 of 6 | 1e-6 | 84 + 2 | 168; 168 | 0.000488380 |
| Mixed six | 4 | 4 of 6 | 1e-6 | 210 + 2 | 504; 504 | 0.000522403 |
| Mostly dark twelve | 3 | 11 of 12 | 1e-6 | 455 + 2 | 1092; 1092 | 0.000488380 |
| Noisier mixed six | 4 | 4 of 6 | 1e-3 | 210 + 2 | 504; 504 | 0.233152332 |

The last row's positive representation has centered uniform error
0.011659725 or less and still yields compliance regret certificates between
0.01698 and 0.01884. This is a representation fallback using the identical
observations, not a new high-precision measurement.

On the difficult price task for the twelve-control source, the conductance
regret bound improved from **0.00422252 to 0.00120005** and the compliance
bound from **0.00325782 to 0.00161983**. The selected commands activate the
bright control and one exactly dark control. Curvature certification used
13 matrices of order 12 and zero new source readings. Exact pair conductance
regret was bounded by 0.000692641; its independently known optimum showed
actual regret below 6.48e-9 on that one example. The latter is a checker result,
not a replacement for the acquired certificate.

For general \(n,k\), the nonzero setting-write count is
\(n\binom{n+k-1}{k-1}\). The recorded protocol pays one source preparation,
settling/integration and reset cycle per lattice reading, plus the two known
standard acquisitions and their preparation/restoration. Ideal total source
dose is \(M\delta n/(n+1)\); actual rounded doses are saved. For the twelve
case it is just below 84, across 455 separate resets, with maximum dose below
0.2. This is not 455 simultaneous readings or a free reset protocol.

Each later physical application still pays its active writes, settling and
eventual reset. The executed selected commands used one or two active controls.
The hypograph construction permits up to \(\min(n,2k)\); a general curvature
proposal can be dense. Any requested later measurement or calibration refresh
must be added. No physical durations or energies were acquired.

Storage uses \(M\) nodal values and coefficients per representation. The exact
face transform has maximum block order \(\binom{k-1}{s-1}\) on a support of
size \(s\), instead of one dense \(M\)-order solve. Hypograph sorting costs
\(O(M\log M)\) per price. Curvature assembly and exact LDL use respectively
\(O(n^2)\) and \(O(n^3)\) rational operations per Hessian coefficient matrix;
bit complexity depends on the acquired precision. Offline matrix setup in
the saved twelve-control run took approximately 0.085 seconds in this
environment; this is a software diagnostic, not physical acquisition time.
All exact costs, raw records, bounds and candidates are in `results/`.

## 6. Stronger positive rational foundation

The selected route also exposed a more powerful representation. Put \(F=J-c_0\),
\(U=\operatorname{diag}(u)\), and

\[
D=\det(I+BU),\qquad N=\det(I+(B+gg^T)U)-D.
\]

Then \(F=N/D\). Both polynomials are multiaffine with nonnegative
coefficients. Retain total degrees through \(r\), obtaining \(F_r=N_r/D_r\).
The new ordinary theorem proves, uniformly over the entire simplex,

\[
0\le F-F_r\le F H_r(q)\le\delta G^2H_r(q),\qquad
H_r(q)=\frac{q^r/r!}{\sum_{j=0}^r q^j/j!}.
\]

For \(r\ge1\), \(F_r\le F\le F_r/(1-H_r(q))\). The bound decays factorially
at fixed finite \(q\), including \(q\ge1\), where the earlier geometric
truncation bound does not decay. A projector family attains the limiting
constant as dimension grows, establishing sharpness **for this truncation**.
It does not establish an optimality lower bound for all representations.

Two sources agreeing on every command with at most \(k\) active controls
satisfy the stronger ideal-information bound

\[
\sup_u|J(u)-J'(u)|\le\delta G^2\Pr\{\operatorname{Poisson}(2q)\ge k\}.
\]

Here Poisson variables are an algebraic counting device. The coupling uses
\(\log(1+\lambda)\), not the Bernoulli mean. This is no photon, statistical
or finite-noisy-transcript lower bound. Exact face equality is stronger than
agreement at finitely many acquired nodes.

Acquired intervals impose linear inequalities on the unknown truncated
positive coefficients; later ratio bounds can be posed as verified
linear-fractional programs. That outer family is valid, but its economical
uniform acquisition has **not** been executed or proved. Its coefficient
count is \(\sum_{j=0}^r\binom nj\) per polynomial, and relaxed coefficients
need not describe a physical source. The complete theorem, sharpness examples,
exact checks and corrected tail display are retained under `selection/`.

## 7. Conventional comparison, evidence and next obstruction

An equally informed conventional method can use the identical acquired
lattice, Bernstein bounds, hypographs and curvature certificate. It therefore
matches all claimed measurement counts. Classical simplex-grid approximation,
positive determinant generating functions, verified matrix bounds and SLSQP
are established tools; references and inspected implementations are in
`PRIMARY_SOURCES.md`. No historical novelty or universal superiority is claimed.

The direct acquired negative-compliance polynomial was also executed on the
same data, including its enlarged source bounds from the acquired baseline.
The response-utility representation often gives a tighter certificate in these
examples. A strong comparator is entitled to choose it too. A one-task online
method may cost less than acquiring a reusable whole law. Methods exploiting
additional resolved low rank or a better physical sensor may also be cheaper,
but those are different warranted information conditions.

The main advance relative to this mission's previous state is closure of an
actual finite noisy acquisition-and-control path for arbitrary darkness under
the bounded source contract. It turns failure to identify a component into
an approximation question about the complete response, then into a certified
decision. That is a useful foundation for reusable experimental inference;
practical importance depends on a source where the operations and bounds can
be established at an acceptable total cost.

The strongest remaining attack is economical, stable acquisition of the
positive rational representation. Its factorial theorem now separates the
representation error from the unresolved cost of learning its coefficients.
The present lattice method remains a complete fallback. The relevant next
test is a verified interval-family learner with an explicit acquisition rule
and uniformly narrow later answers, compared with a conventional method given
the same raw record; simply fitting one rational model would not close it.

## 8. Preservation and review scope

Current Astra cards and governing sources were read at commit
`ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2`. The governing N1082 and N1089
files match their retained source hashes. The named N1089 producer and raw
historical run remain unacquired; the present runs are fresh implementations.

The unchanged prior archive is included, retaining the reciprocal three-load
receiver, shared calibration bounds, all-input Gram theorem, exact rational
tests, blind cases, measured-backplane offline emulation, unchanged OpenWFS
comparison and useful failures. Its information/calibration distinctions,
finite setting and reset costs, two-root normalization issue, scoped 407 versus
539 example, and lack of an on-device load-protocol demonstration remain intact.
No photon or statistical lower bound is inferred from bounded-error arguments.

Internal scoped reviews checked the positive approximation, determinant
argument, hypograph implementation and curvature construction. A false
intermediate Poisson-tail inequality was corrected with its exact counterexample
preserved. Two optional-refinement availability bugs were reproduced and
repaired; their original code and probes are retained. Finite checks support
their actual scope; no independent whole-proof audit is asserted.
`RESEARCH_LOG.md`, `reviews/`, `REPRODUCE.md` and the saved receipt identify
the preserved failures, reviewed versions and executed work.
