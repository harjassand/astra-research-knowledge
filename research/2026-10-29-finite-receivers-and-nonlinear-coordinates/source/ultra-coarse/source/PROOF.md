# A coarse-record intervention receiver on a native catalytic model

29 October 2026. This is a changed question from N744, not an application
of its hidden microscopic-source LP. The positive construction is a
partial-observation, finite-exposure counterfactual envelope, actually
consumed on trajectories from a pinned public RuO2(110) KMC catalog.
All newly acquired trajectories are COMPUTATIONAL. No physical catalyst
record, event detector, reset, rate calibration or global design optimum
has been acquired. No new Girsanov, graph-DP or confidence principle is
claimed. `PRIOR_AND_DECISION.md` gives the matched ordinary comparison.

## 1. What was acquired, and why N744 does not apply

The complete current N744 packet, its continuation, and all 599 lines
of its governing ResearchNote were fetched at Astra revision
d6672151ce8e86d4af3e74b3b880abcdc82ae304/input9301bf5171d4110151e38e5ddebeb1212f593a1c14f7751e019e9a8264a3b8ef.
Its current notice says the separate N991 first-contact kernel does NOT
validate its reset-ejection/microscopic-source assumptions. N744 itself
is source-reported mathematical candidate evidence, not an inherited
independently accepted theorem or physical operation. No scientific
acceptance is inferred from its source hashes.

N744 assumes each actuator adds u_j(nu_j-e_aj)e_aj^T at ONE distinct
microscopic source state, with the SAME destination law under every
combination. Its acquisition also requires tagged events, source
indicators, a reproducible reset law, and further conditions for its
strength-independent cost. An instrument knob need not have this form.

The acquired nonbiological native source is
`kmcos/kmcos`, commit4442009d73032cbe39f8201370ad6d8927c7be4c,
`examples/CO_oxidation.ini`. All 36 directional processes are parsed,
including adsorption/desorption, diffusion, and CO2-producing reactions.
The physical source literature groups directions into fewer symmetry
classes; no discrepancy/error is inferred from those counts. The
upstream F90 client explicitly exposes per-process `set_rate_const`.
Our code is an independent consumer of the complete catalog, not an
execution of the upstream Fortran binary or an experimental reactor.

The actual CO-pressure mechanism adds CO at EVERY empty site. Its
generator component C_M, after removing a positive coefficient, has

    rank(C_M)=3^M-2^M.                                        (1)

Proof: fix the subset of sites occupied by O. On the remaining m sites,
CO adsorption is a pure-birth process on the 2^m empty/CO subsets.
Order by CO count. The matrix is triangular, with one zero eigenvalue
at the fully CO-occupied state and nonzero diagonal at all others.
Equivalently, it has one absorbing class and rank2^m-1. Sum over all
O subsets: sum_i binom(M,i)(2^(M-i)-1)=3^M-2^M. The same conclusion
holds with any positive site-dependent adsorption coefficients.

At the actual32-site model (1) is 1853015893884545. A sum of k rank-one
operators has rank at most k, so replacing this operation by one or two
microscopic-source columns is incorrect. Splitting every microscopic
source into a separately tied actuator gives exponentially many sources,
not the small experimental table promised by N744. `check_catalog.py`
checks the literal native adsorption conditions/actions and small exact
integer instances; the proof supplies all-M scope. This is a native
control obstruction, not a general identifiability or hardness theorem.

## 2. Replacement contract: controlled counting intensities

Consider any nonexplosive finite-horizon marked process on [0,T]. Its
full hidden history can have arbitrary background dynamics. Two marked
families have baseline predictable intensities lambda_1(t),lambda_2(t).
The intervention multiplies them by constants a,b in(0,1], leaves their
conditional destination rules unchanged, and changes no other
conditional path mechanism. The initial law is the SAME. These are
structural premises, not conclusions from isolated response fits.

For a full baseline path let N_1,N_2 be the marked counts and
A_j=integral lambda_j dt. The usual counting-process/Gillespie
likelihood ratio is

    W_ab=a^N1 b^N2 exp[(1-a)A_1+(1-b)A_2].                    (2)

One derivation multiplies every marked-jump density by a or b and
every waiting survival by exp(-integral(target total-baseline total)).
All unchanged jump/destination factors cancel. Bounded controlled
intensities on finite T justify the stochastic exponential and its
unit mean. No Markov property of the observed coarse variables is
required. The intensity scaling/destination invariance is required;
it is not inferred from a coarse Markov fit.

Suppose an acquired coarse record brackets the integrated activities:

    A_j^- <= A_j <= A_j^+.

Then for a,b<=1,

    W^- = a^N1 b^N2 exp[(1-a)A_1^-+(1-b)A_2^-],
    W^+ = a^N1 b^N2 exp[(1-a)A_1^++(1-b)A_2^+].

For any supplied nonnegative bounded path reward 0<=F<=1,

    E_0[F W^-] <= E_ab F <= E_0[F W^+].                       (3)

This is a positive partial-likelihood envelope. It is NOT a new change
of measure, an identified hidden generator, or a sharp whole-path
identification theorem. It does not self-normalize by a random mean
weight. The target is a finite-exposure law, not a stationary law or
an unreset long-time reaction rate.

Measurement uncertainty can be represented in the same contract if
it is actually acquired. For count brackets n_j^-<=N_j<=n_j^+, use
a^n1+ b^n2+ in W^- and a^n1- b^n2- in W^+. Supplied reward brackets
multiply the lower/upper weights in the corresponding direction.
This extension does not supply a detector or a bound on missed events.

## 3. A native coarse activity envelope

In the catalog the per-site CO adsorption coefficient k_CO is common,
and each undirected neighboring empty pair has the common O2 coefficient
k_pair. Let v(t) be ONLY the total vacancy count. Then

    lambda_CO(t)=k_CO v(t),
    lambda_O2(t)=k_pair E(S_t),                              (4)

where S_t is the unobserved vacancy set and E(S) its induced-edge count.
No diffusion/reaction/desorption rate is needed in (2)--(4).

Every O2 adsorption condition/action is enumerated in `PAIR_GRAPH.json`.
There are32sites,64 distinct edges, and degree4 at every vertex. The
native index2*(x+4y)+type maps to the8-by4 square torus by X=2x+type.
The complete native edge list verifies that map; it is not assumed
from the model name. Counting degrees gives

    max(0,4v-64) <= E(S) <= 2v.                             (5)

For the lower bound, all edges incident on the complement number at
most4(32-v), so E(S)>=64-4(32-v). The upper follows from the4v
incident half-edges. The lower is attained: choose subsets of one
bipartition for v<=16 and use complements for v>=16.

The strongest ordinary SAME-coarse-information pointwise envelope was
also paid. Root's separate `root_vacancy_envelope/` reads all64native
edges and acquires exact E_min(v),E_max(v) by ordinary frontier DP,
with8columns of4sites and16masks per column. Fixing the first mask,
retain last mask, total count, and minimum/maximum accumulated inside
and adjacent-column edge score; add the final periodic cut at closure.
Induction over columns covers every vacancy set exactly. All66extreme
witnesses and41449low-v native subsets were checked. I whole-read its
proof, complete code, and receipt. No repeat dynamics was needed.

E_min equals (5). E_max, for v0..32, is

    [0,0,1,2,4,5,7,9,12,13,15,17,20,21,23,25,28,
     29,31,33,36,37,39,41,44,45,47,49,52,54,57,60,64].

This is a sharp per-v geometric bound, not a sharp dynamic path
envelope. Temporal constraints could further reduce uncertainty and
are not paid. Root's geometry costs are .0767s acquisition and .1476s
verification,270592integer DP transitions. This is a credited ordinary
optimization, not a new algorithm or a microscopic measurement.

Acquire the coarse residence histogram H_v=integral1_{v(t)=v}dt. Then

    A_CO=k_CO sum_v v H_v,
    k_pair sum_v E_min(v)H_v <= A_O2
                      <= k_pair sum_v E_max(v)H_v.            (6)

Total vacancy count is not a Markov state in general: two vacancies
can be adjacent or separated, with different O2 intensities. Equations
(3),(6) retain that ambiguity rather than replacing it by a closure.
The histogram/trace is an actual additional observable. A single
time-averaged coverage scalar does not contain all H_v for free.

## 4. Finite-data confidence and access boundary

Assume n independent repetitions of the SAME initial law, with exact
coarse records. An IDEAL Gillespie host that resets the configuration
and uses fresh independent ideal variates in each episode warrants this
IID contract. The actual logger resets the configuration but consumes
one continuously seeded mt19937 stream; that numerical implementation
does NOT prove IID or exact Gillespie laws. The confidence theorem is
conditional, and no IID contract is assumed for observational physical
catalyst data. All three target pairs are fixed before the main batch.

The controlled intensities have known upper bounds Lambda_CO=M k_CO
and Lambda_O2=64 k_pair. Counts are nonnegative, so all weights in
(3) are bounded by

    B_ab=exp(T[(1-a)Lambda_CO+(1-b)Lambda_O2]).                 (7)

For samples X_i in[0,B], `bounded_confidence.py` intersects three
ordinary scalar intervals. With sample mean m, unbiased variance s²,
and t=14, the symmetric empirical-Bernstein radius is

    sqrt(2 s² t/n)+7Bt/[3(n-1)],

using Maurer--Pontil Theorem4 in both directions (failure<=4exp(-t)).
Hoeffding gives radius B sqrt(t/(2n)), failure<=2exp(-t).
The bounded-KL interval solves

    d(m/B || mu/B) <= t/n,

with binary relative entropy d. It applies to ANY bounded variable,
not just a Bernoulli observation: exp(sx)<=1+x(exp(s)-1) on[0,1]
and Chernoff optimization prove each one-sided tail. Its two-sided
failure is at most2exp(-t). Intersecting all three intervals costs
at most8exp(-t) per scalar statistic. KL inversion avoids treating a
zero empirical-Bernstein rare-output lower bound as an intrinsic
acquisition failure.

The combined comparison has57statistics:3baseline outputs, plus
3targets*3outputs*(4coarse lower/upper statistics+1full-activity
statistic+1direct statistic). The union bound is

    8*57*exp(-14) < .000380.                                 (8)

Dependence across target/observable functions on the same baseline
paths does not invalidate this finite union bound. It is not a
uniform guarantee over an unrestricted adaptively searched control
domain. For a fixed target, bound its expectation below by the lower
confidence limit for F W^- and above by the upper for F W^+.

The standalone `coarse_only.py` reads ONLY `COARSE_CONTRACT.json`,
`BASELINE_COARSE.csv`, and the acquired geometry envelope, plus the
data-free confidence helper. It sees neither `MODEL.json` background
rates nor exact pair activities nor held-out paths. It was ACTUALLY
run in a temporary directory containing only those five code/input
files. Its numerical outputs agreed recursively with the separately
labeled rich/held-out wrapper. `COARSE_ACCESS_CHECK.json` preserves
that execution; it is not a formal filesystem isolation theorem.

The supplied F values are two endpoint coverages and a SEPARATE
CO2-reaction path flag (whether any CO2-producing event occurred byT).
The latter is not generally recoverable from H_v, adsorption counts
and endpoint coverages alone. The computational logger acquires it;
physical CO2 event detection remains an extra unacquired readout.

## 5. Native acquisition and actual unseen combinations

The acquired source instance uses every catalog process on4-by4unit
cells (32sites), periodic boundaries, T=450K and baseline partial
pressures1e-5bar each. The mass/thermochemical conventions and native
rate expressions are explicit in `MODEL.json`. The upstream ASE
dependency is unpinned; the declared masses are28.010 and31.998amu.
NIST selected rows were read through the web; direct NIST byte download
returned403. Source thermochemical interpolation is preserved. No rate
was fitted to output data. This is a specified public-model instance,
not a new measurement or validation of RuO2 kinetics.

The implemented native computational actuator scales ONLY the two
adsorption process families, through an existing process-rate setting
operation. For an ideal-gas pressure model this is the intended pressure
change. The source's separately rounded CODATA constants leave a tiny
literal pressure/desorption dependence; `MODEL.json` reports it and a
coupling-error proposal. We do NOT turn that proposal into a physical
actuator calibration. Real pressure changes could also change heating,
surface structure or other rates; invariance is unacquired physically.

Here k_CO=2354.055437797229/s and k_pair=4404.958480478071/s.
The exposure T=1.1196731372603374e-5s was fixed so the maximal
baseline gas-arrival activity timesT is4. All episodes start at the
clean surface. This short finite-pulse target is NOT a stationary
turnover frequency, an unreset first-passage rate or industrial output.

The locked multiplier pairs are (.8,.9),(.9,.8),(.8,.8). One20000-path
baseline batch predicts them all. Each has an additional independent
20000-path direct batch solely for ordinary validation/comparison.
The learner's data fields exclude the exact pair activity; it is used
only by a labeled richer-information Girsanov comparator.

For (.8,.8), the exact-graph coarse receiver gives

    oxygen coverage: [.1276422,.1434800],
    probability of any CO2 event: [.0014334,.0088637].          (9)

The fresh direct numerical means are .135265625 and .0037. All three
target comparisons are in `COARSE_RESULT.json`. The ideal-law
confidence statement is (8); these binary64/seeded-mt19937 Gillespie
runs are numerical applications/diagnostics. A formal finite-bit
distribution/roundoff certificate and physical-data confidence are
NOT_ACQUIRED. Displayed endpoints are not an exact-arithmetic
probability certificate for the actual computer or a real instrument.

The three CO2 intervals overlap; no catalytic-product winner is
certified. The finite surface-oxygen objective does have a conditional
ordering: lower(.8,.9)=.14356864459 exceeds both competing uppers,
with minimum margin .00008867243. This is ONLY a finite-set surface
coverage decision under (8), not a CO2 optimum, a new optimization
method, or a physical recommendation. Choosing among the fixed
reported outputs/candidates is covered by the joint event; searching
additional controls would need additional uniform accounting.

The same acquired joint event also bounds the baseline oxygen coverage
below by.15865131017. Thus all three unseen combinations decrease that
surface-coverage output relative to baseline, by at least.00177,.01597
and.01517 respectively. This is a stronger directional finite-query
consequence of existing statistics, not a new sample or a claim that
catalytic product formation improves.

## 6. Full cycle and strongest ordinary alternatives

`ACQUISITION.json` records80000independent main episodes,964975native
events,697460960condition checks,2009950requested64-bit PRNG words,
and1.03085s of sampling+writing. The0.76999s compilation is separate.
The preliminary1000-path cost preview is retained, including its
13440events and.01283s runtime.

The first main logger retained only integrated v and degree-envelope
statistics. The stronger ordinary graph comparator needed H_v. We
therefore PAID a SAME-seed baseline replay, not a new independent
experiment:270908events, .35185s sampling+writing and1.0775s compilation.
Every one of the original11fields is bit-identical for all20000paths.
The graph DP costs in Section3, coarse packaging, all attempted source
retrieval, and receiver execution are also retained. Coarse-only
processing took about.1151s, the rich/direct wrapper about.3478s; the
standalone access check adds.1982s. Proof/development and network
acquisition are not included in a sampling speed claim.

Model exposure totals are not actual laboratory wall time. Preparing
81000independent clean surfaces (including preview), observational
bandwidth, actuator transients, reset energy and physical calibration
have not been supplied. The replay executes another20000computational
histories but is not another20000independent samples.

The entire public local-rate catalog is available to BOTH methods in
the computational experiment. Ordinary direct KMC is therefore a
genuine stronger comparator, not an imagined exponential stationary
solve; its three held-out batches took about.75845s sampling+writing.
The current small-query FULL cycle does not establish a speed win.
Root's ordinary graph DP is part of the comparison, not withheld
from the proposed receiver. Given the SAME coarse data, calibrated
arrival coefficients and structural premises, an informed ordinary
partial-likelihood/graph method reproduces our operation exactly.
The full-activity comparator gets additional microscopic pair activity
and is explicitly labeled as such. No exclusive new capability or
historical priority is inferred from this composition.

## 7. Exact surviving acquisition debt and disposition

A physical version would require: validated adsorption-only intensity
scaling and conditional destination invariance throughout the domain;
site graph/count and adsorption coefficients; tagged CO/O2 arrival
counts; temporally resolved total-vacancy residence statistics; the
chosen reward readout, including CO2-hit detection when used; and a
qualified same initial ensemble/independent repetition contract. These
were genuinely acquired only in the computational model. Published
mean turnover curves or time-averaged coverages do not discharge them.
No actual source supplies a uniform instrument/model mismatch bound.

If an ideal baseline and target could be coupled to actual laws with
TV errors eta_0 and eta_ab, the bounded estimator means would pay
B_ab*eta_0 plus eta_ab in target expectation. This makes the missing
calibration price explicit; it is not a method for acquiring those
errors. Bounds on missed count/coverage observations are likewise
premises of the robust version of Section2, not inferred here.

For fixed fractional pressure change and physical exposure, (7) grows
exponentially in total potential arrival activity, hence in surface
size. Our short-exposure choice keeps that activity equal to4. This
does not solve long-time/bulk catalytic discovery. It is a limitation
of this conservative receiver, not a lower bound on every coupled,
adaptive, or sequential experimental method. Known reweighting
literature already explains long-path overlap problems.

The positive result is an actually executed coarse-record finite-pulse
prediction/design interface with a fully identified native source,
no learned hidden generator in the receiver, an ordinary geometric
comparator, and explicit statistical/physical scope. N744's physical
microscopic-source gate is not solved or assumed. A civilisation-level
discovery multiplier, practical physical advantage and a new generic
intervention theory remain NOT_ESTABLISHED. The next meaningful
resource would be an actually qualified event-resolved experimental
record, not another synthetic hidden-network LP or more pressure-grid
fixtures. No such resource is acquired in this wave.
