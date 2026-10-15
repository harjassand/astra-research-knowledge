# Astra scientific capital: sharp quasiconvexity and obtainable information

15 October 2026. Initial inspection: `33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d`.
Reconciled integration base: `8a1e001ac128468ae8d151c9a859b89ef3b9a664`.
Archived prompts were treated as data. All conclusions below retain internal,
externally unreviewed status; historical originality is not asserted.

## Principal mathematical advance

Let A=[[a,b],[c,d]], u=a²+c², v=b²+d², j=ad−bc, and
H=(u+v−2j)²=|(a−d,b+c)|⁴. Consider the four-dimensional space

    F = alpha H + beta u² + gamma j² + delta uj.

It is exactly the linear span of the exposed acoustic-contact face
D²F(I)[e12,e12]=0 in the nine-dimensional left-SO(2)-invariant homogeneous
quartic rank-one-convex cone. An exact classification now gives

    F is rank-one convex iff both matrices are positive semidefinite:
    [[6 beta+delta, delta], [delta, gamma]],
    [[8 alpha, delta], [delta, 2 beta+delta]].

Necessity follows from two explicitly parametrized acoustic tests, including
their limiting coefficients. Sufficiency has a universal four-square acoustic
identity and an exact positive decomposition. Singular cases, including
delta=0, are covered; no numerical sampling substitutes for these statements.

The sharp generators are

    J_r = [3r/(8(r+2))]H + [r(r−1)/6]u² + j² + r uj,
    r<−2 or r>0.

The remaining extreme rays of this invariant contact cone are H,u²,j².
Every delta≠0 member satisfying the two LMIs decomposes exactly as

    lambda J_r + (gamma−lambda)j² + (alpha−alpha0)H,
    r=(6 beta+delta)/delta,
    lambda=delta²/(6 beta+delta), alpha0=delta²/[8(2 beta+delta)].

The central new analytic construction certifies J_r quasiconvex for every
finite r<−2. It follows that, **throughout the entire delta≤0 sector of this
four-dimensional face, quasiconvexity is equivalent to rank-one convexity
and to the two displayed LMIs**. For delta=0 this is the immediate
convex/polyconvex limiting case. The positive-delta branch is not settled.

The positive sharp branch does have a decisive method obstruction. An exact
48-term equality dual excludes every positive input-diffusion/local closed-
form certificate for all r>0, including non-SOS corrected densities. An
independent flat-contact Hessian argument eliminates the only skew-output
coefficient left by exhaustive rotation/reflection averaging. Together they
exclude every fixed real constant strongly parabolic output-matrix generator
with a quadratic closed-form correction, and the Peano tangent theorem
excludes the corresponding smooth adaptive local class. No negative compatible
Jensen field was obtained, so QC remains UNKNOWN. Finite positive generation
from invariant heat pieces and quartic PC addends cannot reach these non-PC
extreme rays. Singular/angular, nonlocal, degenerate or higher-jet operations
require a genuinely different argument. The exact dual and output-skew proofs
are distinct from the negative-branch positivity certificate.

The incoming source only certified a smaller parameter interval at coefficient
alpha near3. Independent acoustic reconstruction found the sharp floor
alpha*=3r/[8(r+2)], ranging from63/40 to15/8 on that interval. A second acoustic
contact forced twelve, rather than six, Gram null directions. Solving on that
moving support produced an exact interval certificate with72 rational positive
Bernstein pivots. A further elliptic quarter-turn symmetry identified the
natural diffusion

    d1=(2r+1)/(r−1), d2=−3/(r−1), d1+d2=2.

For r<−2 both are positive. The resulting rational Gram matrix splits by an
explicit invertible congruence into blocks4+4+2+2. Twelve rational LDL pivot
functions are positive on the whole branch, proved algebraically by putting
r=−2−s,s>0. Exact coefficient identity, closedness, primitive, and all-branch
positivity supply the proof; discovery optimizers and finite parameter grids
are not premises. The standard anisotropic heat relative-energy argument then
establishes every affine Jensen inequality and strong W1,4 approximation.

All sharp J_r are non-polyconvex, including r>0 where QC remains unknown.
At I a convex lifted support must use determinant multiplier r+2. Its gap
along I+t diag(1,−r−1) has nonzero cubic coefficient −r(r+2)/3, contradicting
local nonnegativity. This avoids misidentifying a non-gradient lifted law as
a quasiconvexity counterexample. A simple integer negative-branch example is

    E=45H+35u²+24j²−60uj=24J_(−5/2), E(I)=−1.

The sharp rays are extreme in the full **left-invariant** cone, and hence in
its QC subcone when QC is established. They are not exposed in that full cone:
all their zero acoustic evaluations also vanish on j². Their minimal exposed
face is cone{J_r,j²}. They are exposed inside the four-dimensional contact
face. No extremality claim is made in the unrestricted noninvariant cone.

Bruno–Pasqualotto's heat/exact-form method is essential prior art. Their
AppendixA already has a two-LMI criterion and boundary-plus-determinant-square
decomposition for the doubly rotational invariant cone. That structure and
method are not claimed as new. Their both-left-and-right-SO(2) theorem does
not directly supply this anisotropic face; the full GL-orbit comparison is
recorded separately. Priority remains
UNKNOWN. This is a substantial internally proved expansion of Astra's
quasiconvex cone, not a solution of the full planar Morrey problem.

Evidence: workers/moving_kernel_genesis; sharp_floor_independent;
sharp_boundary_qc; sharp_certificate_audit; contact_face_priority_audit;
nonlinear_flow_audit. The interval certificate hash is
2adcc075976981aab4533fbaf16830e2fd6a99b86e0aa16b7d0fd65226674863;
the universal negative certificate hash is
f45149312e694f6080a179b77d322aceabf0d7c2a55ed60c5e102037e55f6ee7.

## What the new mathematics does not automatically supply

The sharp generator cannot lose any positive multiple of H while remaining
rank-one convex: its second contact gives an explicit negative acoustic value.
Thus the incoming elliptic-subtraction proof of a uniform fourth-order Jensen
margin does not transfer to the boundary. This does not refute such a margin
by every other argument. Under the negative-delta two-LMI hypotheses, for
alpha>alpha0 the displayed positive H addend supplies the established
Beurling-based coercivity mechanism, with its coefficient paid explicitly:
the Jensen constant is4(alpha−alpha0)/1875. For the earlier G this is3/1250,
exactly6000times its previous1/2500000. The same new constant holds uniformly
for the incoming alpha3 family on[-21/8,-5/2]. No optimal constant is claimed.

Concurrent PR98/N866 proves an effective storage construction for the earlier
Heat18 G under its own coercivity and fixed-diffusion contracts. Its sufficient
example uses roughly8×10^88 real parameters; it computed no storage value.
The new boundary QC theorem alone does not discharge that gradient-budget
hypothesis or establish a practical storage solver. For the same earlier G,
however, the stronger constant legitimately improves N866's supplied example:
R<21 and a sufficient horizon N=10^17 pass the same exact0.001horizon test,
instead of the published R<184,N=10^22. The full spatial grid was not
reoptimized or enumerated. Transfers to other family members still require
parameter-dependent heat, growth and receiving constants explicitly.

For the older, different N863 exposed ROC ray, smooth adaptive local flows do
not remove the known obstruction. The root tangent theorem proves that any
continuous-at-zero, strongly parabolic quasilinear generator, with a local
quadratic-Hessian null correction admitting a second-order Peano coefficient
jet, reduces to a constant-generator quadratic certificate. It uses the true
canonical dissipation P_C, not an invalid variable-C heat substitution.
An explicit exact two-form converts constant P_C to E_C. This excludes that
smooth adaptive certificate class; degenerate, singular/angular, integrated,
nonlocal and higher-jet operations remain outside the theorem.

The old ray also admits no global determinant-support selection with a second
Peano jet, hence no convex polynomial lift. Two exact integer test pairs give
incompatible multiplier bounds. Ordinary polyconvexity remains UNKNOWN:
polyconvexity does not automatically provide the excluded smooth selection.
Primary Ball–Currie–Olver and Olver–Sivaloganathan machinery limits novelty
claims for the null-form and regularity lemmas.

## Decision-relevant computational results

The battery construction now has two exact positive RC models fitting every
component of the actual retained58-point EIS row inside0.1mOhm. They share
positive inductance and a common positive19-mode baseline. Their Q1000 values
are187.72905369456889... and266.16089938984994...mOhm, crossing200mOhm.

Their step difference is d(t)=125(1−exp(−pi t/2000))²mOhm, with nonnegative
impulse difference. Every current bounded by Imax over10s therefore separates
their entire voltage paths by at most Imax×0.0303624501728855mOhm. At1A,
bounded voltage corruption of15.1813microvolts can hide the pair. The midpoint
argument covers deterministic adaptive protocols; randomized protocols require
a causal current-reactive corruption contract. No oblivious-noise randomized
lower bound is asserted. A maximum-slew ramp followed by a plateau is exactly
optimal for this pair; the known-segment minimax error is proved explicitly.

This changes the source's sparse-frequency failure into a quantified
all-waveform short-experiment limitation, with exact feasible models. It is
conditional on stationarity, known incremental initial state, RC positivity,
bounded current and an additional bounded voltage-error interface. It does
not establish that actual batteries meet those premises. Brown–Grabovsky
extrapolation and established set-membership experiment design are close prior
art; historical originality and global minimax optimality are unestablished.

Original Zenodo EIS/POCV/pulse MAT files were acquired with matching published
MD5 checksums. The supplied first-cell EIS row matches the original MAT. No
measured-current trace or absolute per-cell pulse amplitude was found. Under
equal rectangular pulses and zero initial relaxation, a continuum positive-RC
paired-rise/fall inequality is violated by all92cells, demanding at least
1.077–2.028mV endpoint discrepancy. This is a conditional model/interface
falsifier, not current-calibrated validation. An actual pinned hybrid-drt
joint-domain baseline was executed; its held-out discharge errors remain near
4mV under the declared inferred-amplitude assumptions. No superiority follows.

A separate root operation samples complete interacting failure paths using
only local rate queries. With supplied a_i(x)=b_s(1+eta_i(x))/(n−s),
0<=eta<=beta/n, and an exact count-reference event bridge, marked Poisson
killing and jump rejection give the exact target conditional law with at most
exp(beta) expected proposals. Expected local queries are bounded by
exp(beta)(k+beta BT/n). A retained-reference cutoff or reference total-variation
error delta, followed by the same exact acceptance kernel, propagates to at
most Mdelta; other rounding, rate and finite-bit errors need their own bounds.
uniformization stiffness BT, finite-bit primitives and local-query arithmetic
are charged. This is an existence/query result, not a free exact finite-bit
implementation or unknown-rate acquisition.

A fixed full-failure n=k=400 rational fixture produced a conditional95% band
[8.9983807699,9.0677630742]×10^−143 using5000direct-weight trials. The fixture
has a supplied count-lumpable collective multiplier and vanishing heterogeneous
residuals; it does not solve the earlier fixed-heterogeneity or avalanche
targets. An avalanche boundary-conditioned proposal was rejected as an efficient
mechanism after zero true failures in10000conditional draws. Permutation CMC
can reduce variance, while marked rejection may save aggregate queries. No
measured advantage over that strongest equally informed comparator was proved.

## Physical operations and acquisition

No new physical operation was acquired. The dislocation screw arm's net
neutrality does not mean optical inactivity: its charged partials share a
Zn30 constituent with the mixed arm. Published reversible electric motion of
charged partials is a stronger comparator but does not move both complete
arms. Selective Zn90 absorption is a concrete unmeasured lead; substrate
carrier production at350°C may defeat it. The required same-loop reversible
endpoint response remains absent. Directional hysteresis also invalidates an
unqualified phase-reversal test, and fixed-light stress cycles can pump when
response ratios depend on force. Exact glide-energy and four-branch controls
are preserved for the next experiment.

On the binary-control hard family, independently exciting control ports with
one signed detector gives a polynomial probe construction, verified on exact
and synthetic cases. Passive-load access does not supply those source ports,
and intensity-only probing loses the sign. Existing Virtual VNA experiments
are a strong instrument comparator. The fixed-source noisy lower bound is
not contradicted; the experiment's information interface has changed.

## Research process, provenance and continuation decisions

Seventeen GPT-6.1 Sol Max and two GPT-6 Luna Max agents were invoked this round.
Luna handled bounded source identity and selective external-capital retrieval;
Sol handled independent invention, analytic reconstruction, exact adversarial
checks, physical acquisition/comparators and reviewable integration drafting.
Workers were redirected after genuine leverage appeared, rather than assigned
mechanically to the three reports. Requested configurations are known from
tool calls; inference tokens, per-worker thinking time, financial/energy cost
and peak parallel occupancy are UNKNOWN. Code timings are not inference time.

This round provides descriptive evidence of compounding mathematical capital:
fixed support failure led to moving support, a sharper acoustic boundary,
additional contact geometry, a new symmetry and an all-branch certificate.
It does not demonstrate a causal benefit of a model, prompt or worker count.
Physical efforts again reveal missing coupled same-specimen responses. More
reasoning cannot be treated as acquisition of those responses. These mixed
observations support a limited epistemic-closure hypothesis for supplied exact
mathematical interfaces and oppose its unrestricted physical version; neither
is a controlled evaluation.

All13supplied groups were inventoried:58original files and319extracted ZIP
members. No exact source hashes matched1495selectively compared capital files,
but semantic duplication and classical antecedents were examined separately.
One avalanche embedded hash contradicts its archived member; both original
bytes and discrepancy were preserved. New acquisitions and old source-reported
claims are separately attributed. OpenAI/math was pinned at1581d4cb... and two
actual proofs inspected; neither supplied a valid transfer to the chosen tasks.

Highest-value next work is independent external review of the universal
certificate and full-face theorem, followed by the positive-delta sharp
generators (QC still UNKNOWN), coercivity at the sharp boundary, and a usable
storage computation with explicit receiving hypotheses. Continue the rare-path
operation only on declared rates and matched conditional-path/CMC costs. For
batteries acquire measured current, initial state and model-error bounds before
promoting an experimental prediction. For dislocations prioritize the coupled
same-loop response assay; park device-level claims until it passes. Preserve
the old N863 ray's angular/nonlocal escape problem rather than repeating smooth
local ansatzes already excluded.
