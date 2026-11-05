# Final question-level audit: terminal readout and finite-device scope

2026-11-05. This is a correction of the operational target, not a new external proposal.

## Verdict

Do not demand arbitrarily small total error at a fixed noisy physical output cell. Under the same reset-burst model, that demand is impossible for a reason independent of storage quality. Separate storage error from a declared finite-query measurement interface, and keep the interface's accuracy and physical cost visible.

Also distinguish two consequential questions:

1. One finite commissioned input seed remains recoverable for arbitrarily late queries under one continuing local protocol. Here the d+1 moment obstruction is appropriate.
2. A family of finite commissioned devices serves longer finite missions with a sharp resource/lifetime law. This does not require self-organizing expansion from a fixed finite seed, and it has a different general tail boundary.

The second is sufficient for many practical capabilities. It cannot silently inherit the first question's necessary-and-sufficient moment claim.

## 1. Fixed-output noise creates an irreducible floor

Let the terminal readout at deterministic time T observe only a cube of fixed halfwidth r_out. Assume the reader and its records are within the same finite-speed fault model. A reset at time T-u that covers the entire backward causal cone of that observation makes the terminal state input-independent.

For a storage age at least h, even just the last h units of time give

\[
\Lambda_{\rm out}(h)=
\lambda2^d\int_0^h
\mathbb E(R-r_{\rm out}-vu)_+^d\,du.
\]

For uniform binary input,

\[
P_{e,\rm out}\ge
\frac{1-e^{-\Lambda_{\rm out}(h)}}2.
\tag{A1}
\]

This floor is positive whenever a sufficiently large burst has positive probability. Increasing the memory size does not remove it.

The bound concerns an output observed at one endpoint. A transcript already delivered to an external observer is an additional input-bearing record and changes the endpoint's causal support. Ignoring that transcript would incorrectly apply the lower bound; allowing it without accounting for the receiver would incorrectly promise a physical decoder.

A fixed noisy port therefore cannot provide arbitrary total accuracy, even if the internal stored codeword is perfect. Heralding does not solve this under arbitrary unflagged corruption: a burst can overwrite both the answer and its success flag.

## 2. Recommended commissioning contract

At a specified commissioning start, an unknown bit is presented at a finite input source. A finite writer may retain that bit only during an explicitly charged preparation interval. Preparation has declared hardware, speed, energy, material and computation requirements and an error bound epsilon_init.

At commissioning completion:

- the device contains a finite encoded seed;
- the writer and every external input-dependent backup are disconnected and unavailable to the mission;
- all subsequently usable input-dependent degrees of freedom are counted as part of the device;
- the initial encoding is generated without a fault-free distributed input copy being granted at no cost.

A theorem conditional on a finite encoded seed is acceptable as a foundational theorem, but it must label preparation as an unearned premise until the preparation operation is constructed.

During storage no reader, evaluator, diagnostic transcript or service controller may retain a usable copy of the unknown input outside the counted fault support.

## 3. Two honest readout contracts

### Recommended minimal foundational contract

Use a specified terminal instrument with fixed accuracy epsilon_term < 1/2, independent of mission age. The instrument is initialized independently of the input and is connected only when a query is requested. Its sensing region, finite processing protocol, duration, hardware and energy are charged. Its fault model and accuracy bound are explicit.

Require the memory plus its local query protocol to add at most delta error, where delta can be reduced by increasing the paid memory/readout resources. The total guarantee is

\[
P_e\le
\epsilon_{\rm init}+\delta+\epsilon_{\rm term}.
\tag{A2}
\]

Do not call delta the total physical error. This retains arbitrary reduction of storage and transfer error above a stated measurement floor, while requiring useful output with accuracy bounded away from 1/2 at arbitrarily late queries.

This is already enough for a major recoverability theorem: the infinite-moment lower result forces every fixed nontrivial output advantage to vanish. It is not necessary to demand arbitrarily small total terminal error to establish that phase boundary.

The instrument can perform finite local computation, but an ideal global majority is not its implementation. If the proof uses a global codeword decoder, a separate finite local query protocol must earn (A2).

### Stronger total-accuracy contract

If arbitrary total accuracy epsilon is desired, allow a family of finite fresh terminal instruments indexed by epsilon. Their sensing extent, time, hardware and energy must grow as required by their own physical error bound. Require explicit finite local collection and processing and

\[
\epsilon_{\rm init}
+\epsilon_{\rm store}
+\epsilon_{\rm transfer}
+\epsilon_{\rm term}
\le\epsilon.
\tag{A3}
\]

The terminal instrument may not be a fixed noisy cell. It must either have growing terminal observation support or a separately justified protected receiver/measurement contract. Its proof or calibration is part of the capability. A protected final consumer is a substantive boundary condition, not an illicit long-term memory source, provided it is input-independent and unavailable until the query. Its finite query-time reliability is not the same task as retaining the bit throughout the preceding mission.

If every part of the terminal instrument remains under the same reset law and the result is ultimately read at one fixed bounded noisy support, (A1) still applies. No renaming of a detector as a decoder removes that obstruction.

One should not assume a parameterized receiver merely because it is convenient. The full construction either earns its finite-query performance or presents the fixed-floor version (A2).

## 4. Is finite-seed arbitrary-corruption expansion necessary?

It is not necessary for a consequential finite-device capability. A commissioned device of diameter L with a sharp useful lifetime bound is already a complete physical operation if preparation, storage, readout and reuse are included. This avoids an unnecessary separate problem of authentic colony growth among forged seeds.

For Pareto bursts, an attaining finite-device theorem would target useful lifetime of order L^(alpha-d), at bounded local update rate and power density, and compare this lifetime with preparation and readout times at least of order L/v for an encoding spread across that diameter. For alpha>d+1, the potential ratio of operating lifetime to one-time propagation/preparation time grows as

\[
L^{\alpha-d-1}.
\]

This is a concrete amortization consequence. One need not solve autonomous indefinite expansion to obtain it.

However, if the selected theorem's headline is the exact E R^(d+1) boundary for a single finite seed, switching to an L-dependent family changes the theorem. The preparation extent is allowed to grow with the mission horizon; the finite-seed impossibility no longer rules out that family.

## 5. A decisive critical-tail example separating the two targets

Take a tail, for all sufficiently large r,

\[
\Pr(R>r)=
\frac{c}{r^{d+1}\log r}.
\tag{A4}
\]

Then E R^d is finite but E R^(d+1) is infinite. Therefore every one-time finite seed is eventually forgotten under the cone theorem.

Nevertheless,

\[
\mathbb E(R-a)_+^d
\sim\frac{c}{a\log a}.
\tag{A5}
\]

To verify (A5), use

\[
d\int_0^\infty
\frac{c\,u^{d-1}}
{(a+u)^{d+1}\log(a+u)}\,du,
\]

set u=ay and multiply by a log a. Dominated convergence applies, and the remaining integral

\[
d\int_0^\infty
\frac{y^{d-1}}{(1+y)^{d+1}}\,dy
\]

equals 1.

Thus the complete-reset rate of a cube of side L obeys

\[
\kappa_L
=\lambda2^d\mathbb E(R-L/2)_+^d
\sim
\frac{\lambda2^{d+1}c}{L\log L}.
\]

Its complete-reset ceiling is therefore of order L log L, which is superlinear in the O(L) propagation/preparation scale. This does not establish an attaining memory construction; it proves that the universal complete-reset obstruction leaves room for a useful finite-device family even though the fixed-seed d+1 moment criterion fails.

Consequently, superlinear finite-device mission length or favorable commissioning amortization is not equivalent to finite E R^(d+1) for general tails. The exact fixed-device obstruction is the integrated tail quantity

\[
\mathbb E(2R-L)_+^d,
\]

not merely a named moment or a Pareto exponent.

## Final recommendation

Retain the finite-seed moment theorem as a clean foundational impossibility result. For the positive operation, state explicitly whether the chosen objective is:

- one fixed finite seed with recoverability at every horizon, which requires expansion or another sustained growth mechanism; or
- a charged family of finite commissioned memories with sharp lifetime-versus-resource scaling and useful query access.

The latter is less demanding and already consequential. It is the stronger practical selection unless indefinite finite-origin autonomy is itself the promised consequence. The two should not be conflated. In either case, use the fixed-floor terminal contract by default and promote to arbitrary total accuracy only after constructing the scalable finite-query receiver.
