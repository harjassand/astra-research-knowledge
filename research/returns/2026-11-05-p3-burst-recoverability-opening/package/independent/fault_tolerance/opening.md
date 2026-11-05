# Selection opening: finite-speed recoverability under spatial burst faults

Status: independently constructed opening for the question-selection round, 2026-11-05. The lower theorem below is proved within its declared model. The sufficiency theorem, the proposed recursion, a physical implementation, and historical novelty are not claimed. Earlier productive-control, repair-companion, direct-prevention, and first-event packages are untouched and retain their separate contracts.

## 1. The full question worth selecting

For a locally operated information-bearing system exposed to independent marked Poisson bursts of unbounded spatial radius, what is the sharp condition on the burst law for an unknown, initially localized input to remain recoverable indefinitely, and can an explicit local architecture attain that condition with finite commissioning, bounded hardware density and power density, and a charged finite readout?

A natural candidate boundary is the (d+1)st radius moment. This is already a necessary condition in the exact finite-speed model proved below. Sufficiency is the central open operation. An especially consequential resolution would supply both the criterion and a local repair construction against unflagged arbitrary state corruption, with a matching finite-size lifetime law. Flagged erasures are a strictly easier contract.

The question concerns whether any useful information can survive; it is not an extension of an evidence assay. The lower result applies to all local repair, computation, replication, encoding and decision methods with the same information and physical access, because destruction of every input-dependent record defeats all of them simultaneously. It does not posit a separation between a direct decision method and an equally informed capacity method.

## 2. Exact finite-speed model

Fix d >= 1. Space is R^d with the infinity norm. A lattice implementation can occupy sites within this space, but fault centers are allowed in the continuum. At time 0 all state whose law can depend on a binary input M is contained in

\[
C_0=[-r_0,r_0]^d.
\]

Everything outside C_0, including any auxiliary controllers, private randomness, clocks and initially unused hardware, has a joint law independent of M. There is no surviving external input copy. Local evolution, including input-dependent control signals, has strict maximal propagation speed v > 0. Thus any difference between two coupled input worlds is confined at time t to

\[
C_t=[-(r_0+vt),r_0+vt]^d.
\]

This v is a bound on ALL usable input-information propagation, not merely the local damage-healing speed. Fast wires, mobile records, radiative channels, and external controllers must be counted if the operation can access them.

Burst centers form a Poisson process of intensity lambda dx dt, with iid nonnegative marks R. A burst at (x,t,R) has footprint B_infinity(x,R). Assume E R^d < infinity so any fixed location has finite burst-hit intensity. The reset operation considered for the lower bound replaces every accessible mutable state in its footprint by an input-independent state. It does not leave an input-dependent diagnostic outside the footprint. The local control law, immutable wiring, and independent resources may persist, but none may hide M.

This is one admissible fault mechanism inside a broader arbitrary-corruption model. An upper construction for arbitrary corruptions must work for it. A simultaneous known reversible bit flip is not such a reset, and the theorem cannot be applied to one without an additional erasure argument.

Strict causal support is exact for finite-range bounded-depth local circuit layers. Independent Poisson update clocks alone do not give a deterministic speed limit: arbitrarily rapid update chains are possible. Applying the theorem to that model requires a probabilistic causal-cone estimate. A Lieb-Robinson bound has tails and also requires an approximate version of the theorem. Neither bridge is supplied here.

## 3. Proved complete-cone erasure theorem

Define A_T to be the event that no burst in [0,T] contains the entire possible influence cube C_t at its arrival time. A radius R burst covers C_t precisely when its center lies in a cube with halfwidth

\[
(R-r_0-vt)_+.
\]

Consequently the number of such covering bursts is Poisson with mean

\[
\Lambda(T)
=\lambda 2^d\int_0^T
\mathbb E (R-r_0-vt)_+^d\,dt
\]

\[
=\frac{\lambda 2^d}{v(d+1)}
\mathbb E\!\left[
(R-r_0)_+^{d+1}
-(R-r_0-vT)_+^{d+1}
\right].
\tag{1}
\]

The last line is the expectation of a nonnegative difference. It must not be rewritten as the difference of two infinite expectations. For finite T it is finite under E R^d < infinity.

Let P_m^T be the law of ALL accessible state at time T, for M=m. Then

\[
\operatorname{TV}(P_0^T,P_1^T)\le e^{-\Lambda(T)}.
\tag{2}
\]

Thus even an ideal global decoder has uniform-prior binary error

\[
P_e(T)\ge \frac{1-e^{-\Lambda(T)}}{2}.
\tag{3}
\]

Every restricted or physical decoder obeys the same lower bound. Worst-case error is at least the displayed average error. For a uniform binary input,

\[
I(M;X_T)\le e^{-\Lambda(T)}\log 2.
\tag{4}
\]

### Proof

Couple the two input worlds using the same outside initial state, all independent random resources, fault centers and marks, and random choices by the local controller. By the causal-speed assumption their state differences at time t are confined to C_t. The first burst covering C_t resets every possible difference. Outside C_t the worlds were already equal. Hence their entire accessible states become equal and remain equal under the coupled future evolution. The coupling inequality gives (2), since P(A_T)=exp(-Lambda(T)). The binary testing identity gives (3).

For (4), reveal whether a complete-cone reset has occurred. This event is independent of M. Conditional on its occurrence, the final state is input-independent by the same coupling. Conditional on no such reset, at most log 2 information remains. Revealing this independent event can only increase mutual information, proving (4).

The argument permits arbitrary adaptive repair, coding, local computational complexity and initially blank hardware. It also permits an unrealistically powerful final global decoder, which only makes the impossibility stronger. It does not provide an implementable decoder for the positive direction.

By monotone convergence,

\[
\Lambda(\infty)=
\frac{\lambda 2^d}{v(d+1)}
\mathbb E(R-r_0)_+^{d+1}.
\tag{5}
\]

For every finite r_0, if E R^(d+1) is infinite then the first complete-cone reset is almost surely finite, the total-variation bound tends to zero, and every finite-speed controller eventually loses the unknown input in the testing sense.

Finite E R^(d+1) only removes this particular universal obstruction. It does not establish recovery, positive information capacity, a functioning local clock, a finite-seed expanding code, or a physical implementation.

## 4. A concrete physical distinction forced by the lower theorem

The hit intensity of an individual point is

\[
\lambda 2^d\mathbb E R^d.
\]

Therefore the fault environment can have finite local hit rate and, if deposited burst energy is proportional to damaged volume, finite average local input power, while preserving any initially finite information is impossible. Take a radius distribution with

\[
\mathbb E R^d<\infty,\qquad
\mathbb E R^{d+1}=\infty.
\]

The additional moment is the price of having to move or reconstruct information through physical space over time. A per-component error rate or finite mean damage power does not by itself establish scalable useful operation. This does not assert that any particular hardware platform has the postulated radius tail.

No memory architecture avoids this lower bound by doing more useful computation. A computation that must later distinguish two initial inputs cannot recover their distinction after all accessible physical records have coalesced. This supplies a foundational consequence even before any positive construction is completed.

## 5. Explicit Pareto laws and resource ceilings

Suppose

\[
\Pr(R>r)=(r_*/r)^\alpha,\quad r\ge r_*,
\qquad \alpha>d,\quad r_0\ge r_*.
\]

Writing beta=alpha-d and

\[
C_{d,\alpha}=
2^d\frac{\Gamma(d+1)\Gamma(\alpha-d)}
{\Gamma(\alpha)}r_*^\alpha,
\]

the instantaneous complete-cone erasure rate is

\[
\kappa(t)=\lambda C_{d,\alpha}
(r_0+vt)^{-\beta}.
\]

This follows from the exact identity

\[
\mathbb E(R-a)_+^d
=\frac{\Gamma(d+1)\Gamma(\alpha-d)}
{\Gamma(\alpha)}r_*^\alpha a^{d-\alpha}.
\]

For beta != 1,

\[
\Lambda(T)=
\frac{\lambda C_{d,\alpha}}{v(1-\beta)}
\left[
(r_0+vT)^{1-\beta}-r_0^{1-\beta}
\right].
\tag{6}
\]

For beta=1,

\[
\Lambda(T)=\frac{\lambda C_{d,\alpha}}v
\log(1+vT/r_0).
\tag{7}
\]

Thus:

- d < alpha < d+1: distinguishability is bounded above by a stretched exponential in T^(d+1-alpha).
- alpha=d+1: distinguishability is bounded above by a power of T.
- alpha>d+1: the complete-cone hazard is integrable; this mechanism alone leaves a positive chance of avoiding complete-cone erasure.

For d=2 the constant is

\[
C_{2,\alpha}=
\frac{8r_*^\alpha}{(\alpha-1)(\alpha-2)}.
\]

At the critical exponent alpha=d+1, the first complete-cone reset has exact survival function

\[
\Pr(\tau_{\rm cone}>T)
=(1+vT/r_0)^{-q},
\qquad q=\lambda C_{d,d+1}/v.
\]

It occurs almost surely, yet its mean is infinite for q<=1; for q>1 its mean is r_0/[v(q-1)]. This is a precise reason that an infinite mean lifetime of an unavoidable catastrophic trigger does not establish indefinite information retention. Actual logical failure can happen sooner, so the formula is not a claim that every controller's logical lifetime has infinite mean.

### Seed-extent cost for high reliability

For alpha>d+1,

\[
\Lambda(\infty)=
\frac{\lambda C_{d,\alpha}}
{v(\alpha-d-1)}
r_0^{-(\alpha-d-1)}.
\]

To have uniform-prior decoding error <= delta < 1/2 at every horizon, a necessary condition is

\[
r_0\ge
\left[
\frac{\lambda C_{d,\alpha}}
{v(\alpha-d-1)\{-\log(1-2\delta)\}}
\right]^{1/(\alpha-d-1)}.
\tag{8}
\]

This is a lower bound on initial input-dependent spatial extent. It is not automatically a lower bound of order r_0^d on hardware count: sparse records can be far apart. A filled-cube architecture would pay that volume, while a sparse architecture must separately pay communication, propagation and readout costs.

If the input initially resides in one fixed unprotected cell, subsequent expansion cannot promise arbitrarily small error. Its early complete-erasure hazard creates a nonzero floor. A claim with arbitrary target delta must declare a paid commissioning process that keeps the input available while preparing a sufficiently robust finite seed, or must remain conditional on a supplied finite encoded seed.

### Fixed cube and fixed-volume convention

For an autonomous closed device occupying a cube of side L, every complete-device reset irreversibly destroys its input information. Its exact rate is

\[
\kappa_L=\lambda\mathbb E(2R-L)_+^d.
\tag{9}
\]

For L>=2r_* this becomes

\[
\kappa_L=
\lambda K_{d,\alpha} L^{d-\alpha},
\quad
K_{d,\alpha}=
2^\alpha
\frac{\Gamma(d+1)\Gamma(\alpha-d)}
{\Gamma(\alpha)}r_*^\alpha.
\tag{10}
\]

For d=2,

\[
K_{2,\alpha}=
\frac{2^{\alpha+1}r_*^\alpha}
{(\alpha-1)(\alpha-2)}.
\]

Hence

\[
P_e(T)\ge\frac{1-e^{-\kappa_LT}}2,
\qquad
T_\delta\le
\frac{-\log(1-2\delta)}
{\lambda K_{d,\alpha}}L^{\alpha-d}.
\tag{11}
\]

The mean time of first complete input erasure is 1/kappa_L. This is an information-loss ceiling, not a universal upper bound on the first time an arbitrarily chosen output happens to be wrong for a known message.

Under the filled-cube volume convention V=L^d, the ceiling scales as V^(alpha/d-1)/lambda. Volume alone is not a universal geometric constraint: a long sparse device with the same volume can have much greater diameter. A claim stated only in terms of V must include shape, density or maximum diameter, and communication/readout resources.

## 6. The serious local operation already available

For the two-dimensional north-east-center Toom rule,

\[
x_{t+1}(z)=
\operatorname{maj}
\{x_t(z),x_t(z+e_1),x_t(z+e_2)\},
\]

any finite erroneous set inside an a by b rectangle on an otherwise correct uniform background disappears within a+b-1 synchronous rounds without leaving that rectangle.

Proof: by monotonicity it suffices to begin with the entire rectangle erroneous. At step t its surviving sites satisfy

\[
(a-1-x)+(b-1-y)\ge t
\]

within the rectangle. Induction under the majority rule proves this formula. At t=a+b-1 it is empty. Complement symmetry supplies the corresponding result around the other uniform stored bit.

Thus an isolated radius-R corruption has a local repair time of order R. This is a genuine constructive ingredient, with constant-size local state and local updates. It is not a complete finite-seed memory: a finite island of the desired bit in the opposite blank background is itself eroded. Infinite initial uniform encoding is not free finite preparation.

### Why independent recovery cones fail

Start with errors at (1,0) and (0,1). Either error by itself disappears in one step. Together they create an error at (0,0) after one step and survive an extra round. More generally, errors on

\[
\{(x,y):x,y\ge0,\ x+y=m\}
\]

successively generate the diagonals x+y=m-t and disappear only at step m+1. Each original singleton alone has a one-step lifetime. Consequently the union of independent, fixed-height single-fault recovery cones does not contain the collective evolution.

Any reduction to Poisson Boolean coverage or an independent-grain model must prove a recursive interaction/merger rule that covers this phenomenon. The d+1 moment suggested by isolated cone volume is not a proof of sufficiency.

## 7. A plausible sharp constructive route, explicitly unproved

At geometric scales L_(k+1)=B L_k, use spacetime blocks with temporal depth proportional to L_k. If one can build a local operation such that a bad large block requires either two separated bad smaller blocks or a sufficiently large physical burst, a candidate recursion for a Pareto tail is

\[
p_{k+1}\le C_B p_k^2+
C'_B\lambda L_{k+1}^{d+1-\alpha}.
\tag{12}
\]

For beta=alpha-d-1>0, the algebra can close at

\[
p_k\le A\lambda L_k^{-\beta}
\]

for small enough lambda and a suitable initial scale. The number T/L of macroscopic time blocks would then give an error term of order

\[
\lambda T L^{d-\alpha},
\]

matching the whole-device reset ceiling. Small local faults could add a term of form T exp(-cL).

The two-separated-subblocks implication is exactly what remains to be proved. It is not supplied by the displayed algebra. It must survive interacting droplets, faults in state used for control, expansion of an initially finite encoding, and the actual readout.

Naive bounded-radius truncation does not solve this problem. Coloring into K=O(R^d) dependence classes leads to a local-stochastic effective rate roughly

\[
p_{\rm eff}\approx(\lambda R^d)^{1/K},
\]

so this black-box route would demand exponentially small lambda as the cutoff R grows. That is inadequate for an unbounded heavy-tail law at fixed positive intensity.

A possible complete finite-device target for alpha>d+1 would be a bound such as

\[
\Pr(\text{logical failure by }T)
\le C\lambda(T+L)L^{d-\alpha}
+T e^{-cL}
+\epsilon_{\rm commission}
+\epsilon_{\rm readout},
\]

with O(L^d) hardware at bounded local power and explicit finite commissioning/readout. This formula is a target only. It is not an established estimate for Toom's rule or any architecture in these notes.

## 8. What existing primary methods already buy

### Toom stability and contour methods

Toom's stability theorem already preserves homogeneous phases under sufficiently weak local-stochastic faults. Its fault class permits some correlation; the relevant property is an exponentially small upper bound on the probability of errors at every site of a specified finite spacetime set. A single large burst can corrupt a whole area with polynomial probability and violates that quantitative requirement. Therefore saying that ordinary Toom stability automatically applies to arbitrary polynomial burst tails would be wrong.

The 2026 Swart-Szabo-Toninelli paper revisits Toom contours and proves further stability results for intrinsic random local rule selection. It is strong relevant machinery, not a theorem already giving the present heavy-tail finite-seed operation.

### Gacs reliable computation and self-organization

Reliable computation from noisy cellular automata, including asynchronous one-dimensional self-organizing hierarchies, is established primary work. A claim to invent self-maintaining computation, faulty local clocks, or finite-state reliable organization in general would fail this comparison. The new target is the non-local-stochastic unbounded burst law, its sharp geometric lower boundary, and an attaining operation with the same input/access and full preparation/readout contract.

The 2024 corrected version of Gacs's self-organization paper should be consulted, not only the 2001 original.

### Poisson hail: the closest and most dangerous comparator

Poisson hail models spatially overlapping jobs whose footprints and service times are random. Stability means that local workload remains tight over time. Foss, Konstantopoulos and Mountford establish small-intensity stability under finite (d+1+epsilon) moments of spatial diameter and service time. For service time proportional to radius and Pareto exponent alpha>d+1, their result already supplies the expected workload boundary away from its critical endpoint.

Mountford and Wang subsequently characterize many more moment regions up to boundaries, including cases with infinite propagation speed. Their exponents are

\[
a=\sup\{s:\mathbb E R^{d+s}<\infty\},\quad
b=\sup\{s:\mathbb E \tau^{1+s}<\infty\}.
\]

With tau proportional to R, the strict Pareto regime alpha>d+1 is in an already stable region. The exact finite (d+1) moment boundary, including logarithmic corrections, is not automatically settled by those strict-moment results.

Therefore a generic observation that repair jobs have a d+1 moment threshold is not itself a new capability. The prospective work must establish a valid domination or other bridge from corrupted local information dynamics to a tractable hail process and then earn finite-seed initialization, unflagged data recovery and readout. Hail workload stability by itself does none of those.

### Boolean percolation and disaster contact processes

For the Poisson Boolean model in D dimensions, finite Dth radius moment characterizes a nontrivial subcritical phase. Setting D=d+1 is suggestive, but individual recovery regions are not independent physical grains once faults interact, as the exact diagonal counterexample demonstrates.

Lanchier's contact process with destruction of cubes and hyperplanes already proves that catastrophic-event geometry matters beyond a per-site death-rate statistic. The claim that spatial correlation or common-cause geometry matters is old. Flagged-erasure copying can reduce to a survival/contact-process question; unflagged corruption of data and controls is stronger and requires an actual new bridge.

## 9. Architecture choices that must be explicit

The first foundational positive theorem need not impose translation invariance, autonomous synchronization and spontaneous self-assembly if they are not essential to the consequence. One clean contract permits fixed finite-range circuit geometry and an input-independent bounded-rate schedule while every mutable data/control register is corruptible. A physical claim must then declare what provides that schedule and its cost.

Demanding a homogeneous autonomous finite-state organism grown from a finite seed is stronger. Noise can forge colonization states and fake seeds. Toom's uniform phases do not select an authentic finite ancestor, and standard reliable hierarchy machinery must be checked for this exact initial-information contract. That separate identity/colonization issue must not be hidden inside an assumed perfect blank substrate.

Similarly, perfect erasure flags are an extra fault-diagnostic resource. A flag that reliably distinguishes erased cells from valid but wrong data may turn the task into monotone spreading. If a positive result needs flags, it should be named as a flagged-erasure result and not promoted to arbitrary-corruption fault tolerance.

## 10. Commissioning, operation, readout, acquisition and costs

1. Commissioning. Specify how the finite encoded seed is produced, which external writer retains the input during preparation, how long it remains available, the preparation failure bound, and when it is withdrawn. A theorem conditional on an encoded seed is legitimate; it is not a delivered physical acquisition/preparation capability.

2. Input-independent substrate. Blank space, gate connectivity and schedule may supply work and order but cannot supply the unknown answer. Every input-dependent degree of freedom must be included in the influence-support accounting.

3. Useful operation. At minimum the device must retain an initially unknown bit and answer a finite physical query. With repeated queries, the error criterion must distinguish per-query error from the probability of any wrong answer over an infinite stream.

4. Readout. Global majority is a mathematical decoder, not a physically costless device. Charge local signal collection, its delay, faults during collection, any protected output register, and repeated use.

5. Expansion. Infinite-time operation may use unbounded total hardware and energy. It is meaningful to require bounded density and power density, but it is incorrect to advertise that as finite total resources. For a filled expanding cube, active volume is O((r_0+vt)^d), and constant per-site update power gives total supplied energy through T of order

\[
\frac{(r_0+vT)^{d+1}-r_0^{d+1}}{v}.
\]

The proportionality factor is the declared local operating power. This is a cost for that architecture, not a universal thermodynamic lower bound.

6. Control mechanics. Bursts that corrupt a register while leaving the local update law intact differ from physically destroying all repair hardware in the footprint. If hardware replacement is required, its transport, material, energy and controller must be modeled.

7. Acquisition. Finiteness of a high tail moment cannot be established uniformly from a finite local trace over unrestricted radius distributions. Rare indistinguishable tail additions can change it. A positive capability needs a justified physical tail envelope, a finite operating horizon with explicit residual uncertainty, or a restricted estimable family.

8. Reuse. Persistent operation is itself reuse, and no free restoration of the initially encoded bit is permitted after commissioning. A protected external backup changes the task and belongs in the shared-support accounting.

## 11. Exact scope of the preserved machinery

The previous skip-free observed-damage feedback certificate, finite-source repair companion, interacting Gibbs/direct-capacity constructions, and first-event comparisons remain valid under their own premises. No reduction from those classes to spatial Poisson bursts is assumed. Their role here is methodological: compare the actual useful decision or operation under identical access, include common support, and preserve all costs. This selection does not relabel their certificates as physical evidence that the present tail law or architecture holds.

## 12. Selection verdict

The decisive established opening is the architecture-independent causal erasure bound, including the finite local power versus impossible information retention distinction and explicit radius/lifetime resource laws. The decisive constructive opening is linear isolated Toom erosion together with the multiscale target and an exact example showing why independent recovery cones do not prove it.

The full resolution is worth pursuing only if it closes the actual bridge: an explicit local information-preserving operation against the declared burst faults, with finite seeding and usable readout, at the sharp boundary or a sharp replacement. A workload theorem, a uniform infinite initial phase, or a numerical simulation alone would not complete this programme.
