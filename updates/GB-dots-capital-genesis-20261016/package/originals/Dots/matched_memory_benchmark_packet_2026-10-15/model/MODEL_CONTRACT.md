# Contract for an independently implemented 4D Pauli-trajectory benchmark

## Readout update

The global readout completeness obstruction is resolved by the independently checked tensor-product contraction in `TENSOR_READOUT_VERIFICATION.md`, with own checker/results alongside it. Replace the global GF2 fallback proposed below by that deterministic H(s), retaining the small-component local branch. Direct expansion has O(L^5) worst-case time, but a separately implemented and checked separable-axis form reduces this to O(L^4) time and memory, including all ip expansions. It agrees on every basis edge for L=2,3,4 and passes an L=16 random-boundary algebra test. Global H alone incorrectly recovers some single-face faults logically, so it is not a substitute for the local branch; L<=8 remains fallback-dominated. No Monte Carlo has been run.

## Decision and scope

An honest own implementation is possible. The first useful experiment is the exact one-sector Poisson trailing-vertex sweep from `memory_domination_review/original_theorem.md`, compared with explicitly named **Poissonized 4D Toom and DKLP variants**, using one common, deterministic, syndrome-only final recovery. This measures specified finite-time decoded error probabilities. It is not reproduction of the 2016 parallel-schedule curves, an optimal decoder benchmark, or evidence proving an exponential lifetime.

The missing original source blocks bit-for-bit reproduction, not implementation of the published local rules. The supplied theorem leaves its global fallback recovery unspecified. Its accompanying `memory_domination_review/TORUS_HOMOLOGY_BRIDGE.md`, §5, reconstructs a fixed-order axial-prism local filling and the global fallback policy. That resolves the mathematical readout design; an implementation still must freeze its axis/tie-break order and fallback before logical probabilities have a unique numerical meaning. Below is an explicit box-linear-algebra alternative, with cost and limitations. Do not silently replace it by a favorable error-history-aware recovery.

No simulator was executed or installed for this contract.

## Primary-source comparison (bounded summary)

[Breuckmann et al., 1609.00510v2](https://arxiv.org/pdf/1609.00510), §§2.1, 6.3–6.4, 7.2: Toom flips a face when its north and east checks are defective. Six plane-orientation groups are updated sequentially, with simultaneous updates within each group. DKLP flips with probability one for at least three defective boundary edges, one-half for two, otherwise zero; each orientation is split into checkerboard substeps. Noise is independent per-face Bernoulli per QEC cycle. Their final test repeatedly applies the same decoder with perfect syndrome. Residual stuck syndrome is counted as failure, separately from reaching a wrong codeword. Full minimum-surface final decoding was not performed. These statements specify local algorithms, not the exact hidden termination details of unavailable code.

Our supplied theorem instead uses independent vertex clocks, an eight-edge trailing condition, fixed pairing, and possibly two simultaneous face flips. Its final decoder fills small syndrome components in lifted boxes, with a global fallback. These are different microscopic rules and readout policies.

## 1. Common geometry and one-sector semantics

Use an even integer L >= 4 for comparison including periodic checkerboards; small odd sizes are permissible for Poisson models but must not be mixed with an invalid odd-L two-color periodic DKLP schedule. Restrict to L >= 4 to avoid degenerate coincident small-torus incidences. Empirical sizes need not meet the theorem's unknown sufficiently-large L=bM regime, and results must say so.

Coordinates x in (Z/LZ)^4, axes 0,1,2,3; lexicographic orientation order (01,02,03,12,13,23). Store 6L^4 face bits E[x,ij]. Work on the **dual lattice** so E represents physical X errors and their four dual boundary edges represent violated primal Z checks. This is simply relabeling the self-dual cell complex; no second sector or Y noise is simulated. State initially E=0, syndrome s=0, i.e. any encoded state, possibly reference-entangled. No arbitrary logical-state sampling is necessary for Pauli trajectories.

All arithmetic below is F2. Let e[x,i] denote the edge from x to x+u_i. Face f[x,ij] has boundary

    d2 f[x,ij] = e[x,i] + e[x+u_j,i] + e[x,j] + e[x+u_i,j].

An independent gather-form syndrome oracle is s_i(x)=XOR_(j != i)[E_min(i,j),max(i,j)(x) XOR E_min(i,j),max(i,j)(x-u_j)].

Store s=d2 E and update it by toggling those four entries for each toggled face. A correction chain with two faces is one event: calculate both faces from OLD s, then XOR both boundaries; no intermediate eligibility checks. Never erase accumulated E when syndrome vanishes.

## 2. Exact target dynamics, without time discretization

Set dimensionless time tau=kappa*t and alpha=lambda_X/kappa. In this one-sector test lambda_Y=lambda_Z=0. Each face suffers independent X-toggle events at rate lambda_X. Each vertex has independent correction-attempt rate kappa, including attempts that do nothing.

At vertex v, incoming edges are e[v-u_i,i], outgoing edges e[v,i]. If any incoming bit is one, do nothing. Otherwise form sorted O={i:s[v,i]=1}. If |O|=2 or 4, pair consecutive directions and toggle corresponding f[v,ij]; otherwise do nothing. Valid exact syndromes force |O| even in this case. Encountering odd |O| is a failed invariant, not an extra noise mode. There are six two-direction patterns plus the all-four pattern. Every such pattern uses the SAME rate-kappa vertex clock: seven independent unconditional vertex clocks would be the wrong process.

An exact, simple sampler has constant total proposal rate R=L^4*kappa+6L^4*lambda_X. Draw exponential waiting time with rate R, then choose correction with probability L^4*kappa/R or noise otherwise, and choose a uniform corresponding site. Include null proposals. Stop before applying an event with time >T. Rates kappa=0 or lambda_X=0 require straightforward limiting branches. Independent seeded streams for clock/noise/location/correction coins should be recorded. Event-driven sampling is exact for the ideal instantaneous-jump theorem; it models no finite gate durations.

## 3. Comparator kernels and schedules

**Poisson-Toom (own schedule variant).** At each face f[x,ij], independent rate-r attempts check north e[x+u_j,i] and east e[x+u_i,j]. Toggle f iff both are one. No other edges are required to vanish. This is not the target trailing-vertex rule.

**Poisson-DKLP (own schedule variant).** At a rate-r face attempt count its four boundary syndrome bits. Toggle if count >=3; use an independent fair coin if count=2; otherwise do nothing. Sequential Poisson events eliminate simultaneous-neighbor conflicts and need no checkerboard. The count-three update lowers syndrome weight by two, count-four by four, and count-two preserves it. This diagnostic must hold at every accepted event.

**2016-style parallel modes (optional separate experiment).** One noise layer precedes a full correction cycle. For Toom, process the six orientations in fixed lexicographic order, calculate all decisions within an orientation from its old syndrome, XOR their combined boundaries, then proceed. For DKLP use the same orientation order and colors (x_i+x_j) mod 2 = 0 then 1, with fresh coins; recompute between colors. Explicit ordering is our reproducibility convention because the text gives example orientation sequencing rather than a full implementation manifest. Updates read global syndrome, not parity of only two coplanar faces. With q=0, current exact syndrome is used after updates. These modes have batched noise and scheduled correction, so should not be labeled the same physical process as Poisson dynamics.

## 4. Resource normalization: report more than one axis

There is no unique hardware-equivalent rate conversion between a vertex operation and a face operation. Primary convention: **equal attempted local updates per unit physical time**, including null attempts. Target budget B=kappa*L^4; set r=kappa/6 for either Poisson face comparator. Report alpha=lambda_X/kappa AND lambda_X/r=6*alpha. Do not match the number of successful flips, which is trajectory- and decoder-dependent. A target attempt can toggle two faces; a face attempt at most one.

Also report actual syndrome-bit inspections, RNG draws, successful one/two-face operations, and wall time. The target reads eight checks per attempt; Toom two; DKLP four. A secondary equal-check-read convention would use r=2*kappa/3 for Toom and r=kappa/3 for DKLP. These are different budgets, not interchangeable x-axis labels. They are algorithmic proxies, not reservoir/control/energy costs.

For parallel mode one full cycle makes 6L^4 face decisions regardless of six/twelve substeps. Equal attempted updates gives cycle duration Delta=6/kappa, or Delta=6m/kappa for m repetitions. If a no-correction interval of length Delta is replaced by one parity-noise layer, its exact face flip probability is p=(1-exp(-2*lambda_X*Delta))/2. This is a valid noise-marginal conversion only: batching all noise before correction does not equal interleaved continuous noise. At small rate p approximately lambda_X*Delta; use the exponential formula, not p=alpha. The number and duration of parallel layers are separate latency resources.

## 5. Fixed final recovery: specify before evaluating

Use identical D(s) for all memory kernels. D must depend only on final syndrome, lattice, and frozen deterministic tie-breaks. It cannot inspect E, the fault record, or the known initial logical value. The simulator uses E only AFTER D has been chosen, to score the residual C=E+D(s).

Proposed theorem-compatible family:

1. Find connected syndrome-edge components by shared vertices. Lift each component to integer coordinates by traversing its edges with signed unit steps. Inconsistent winding constraints mean the component cannot use the local branch. Anchor and traversal order are lexicographic.
2. Test the theorem’s actual criterion: ambient torus infinity diameter strictly less than L/8 (all pairwise wrapped coordinate distances). If this holds, its consistent short lift fits a contractible coordinate box. Solve d2 D_component=s_component using ONLY faces inside that box. Use deterministic F2 elimination with prescribed edge/face order and all free variables zero. A rectangular full cubical box is contractible, so a closed 1-chain in it has a filling. Failure of consistency is an implementation error. Translation of the integer lift must not affect the mapped-back result.
The cheaper source-style alternative to local elimination is explicit axial prism contraction. Let a be the lower corner of the lifted box. For each axis d in order 0,1,2,3, every current occupied i-edge at x with i != d contributes faces in the (i,d) plane based at x with coordinate x_d replaced by t, for t=a_d,...,x_d-1. XOR these into D; project surviving transverse edges to x_d=a_d and delete d-directed edges. On a cycle, the prism boundary is the old cycle XOR its projection. The four stages telescope to a filling. This avoids a dense local solve, but must be independently compared with incidence-matrix boundary checks before use.

3. If every component qualifies, XOR these fillings. If any component fails the size/lift criterion, use one fixed global F2 solution d2 D=s for the WHOLE syndrome, again lexicographic elimination and zero free variables. Global solvability follows from s=d2 E. Do not try to fill a single winding component globally: two nontrivial loops can bound jointly while neither bounds individually.

The stated diameter criterion matches the supplied bridge; deterministic box elimination supplies the same locality and filling properties as its axial-prism construction, but is a different explicit decoder choice. Do not claim it reproduces a unique original numerical channel. The two fillings inside one contractible box have identical logical action; choices on large-component fallback cases can differ logically. Record a local-branch/fallback flag and decoder cost on every readout. Global algebraic filling is not minimum-weight or maximum-likelihood and can make poor choices; an apparent crossover may be readout-limited. It is nevertheless a bona fide complete noiseless syndrome recovery, so decoded logical error is well-defined.

Important small-size caveat: for L <= 8, a single-plaquette syndrome has diameter 1 and fails the strict L/8 test. Such sizes invoke fallback even for the simplest nonempty syndrome. Their numerical behavior is especially fallback-dependent. Increasing the local cutoff merely to improve these curves would define a different decoder and must be labeled.

Dense global elimination is not automatically practical. Store/reuse a fixed factorization for a given L if possible; profile separately. The matrix has 4L^4 rows and 6L^4 columns, before rank reduction. Dense binary storage alone is approximately 3L^8 bytes, and elimination can dominate. A constructive chain contraction could replace it after independent validation, with an explicit new decoder version. An exact minimum-weight fallback could instead use binary face variables z_f and integer auxiliaries k_e with sum_(f incident e) z_f - 2 k_e = s_e, minimizing sum_f z_f. It has 6L^4 binary variables and 4L^4 parity constraints; no runtime guarantee or available suitable solver has been established here. A returned feasible incumbent is a valid recovery but not certified minimum weight without an optimality certificate. Tie-breaking must remain syndrome-only. Even certified minimum-weight recovery is not automatically maximum-likelihood recovery for correlated stationary errors from these dynamics. Therefore MILP is not the initial execution route. For initial smoke work, stopping and marking unresolved fallback cases is acceptable, but then report lower/upper error bounds, not a completed logical-failure estimate.

## 6. Scoring, finite T, and stopping

After D, assert d2 C=0. For each i<j define

    h_ij(C)= XOR of C[x,ij] over all x with x_i=0 and x_j=0

(the remaining two coordinates range freely). This intersects C with a complementary dual two-torus. Any nonzero one of these six bits is a decoded logical X-sector failure. Never apply this criterion directly to an open chain E. A closed coordinate ij sheet with other two coordinates fixed must give h_ij=1 and all other bits zero, for odd AND even L.

At a predeclared T report trials, failures, six-bit error distribution, binomial confidence intervals, syndrome weight, correction/noise counts, local/fallback readout frequency and costs. For N independent trajectories with zero failures, a one-sided 95% upper bound is 1-0.05^(1/N), approximately 3/N, not zero. Do not terminate trajectories merely because a noisy syndrome is nonempty.

If global readout is not implemented, return three categories: proven decoded success, proven decoded failure, unresolved. Failure frequency lies between n_failure/N and (n_failure+n_unresolved)/N, with sampling uncertainty in addition. An unresolved case is not an established logical failure.

Publication-style cleanup is a SECOND observable on a copy: run chosen local rule without new noise. Distinguish (a) cleared syndrome and zero homology, (b) cleared syndrome and nonzero homology, (c) certified fixed point/cycle with residual syndrome, and (d) readout timeout. Deterministic Toom can detect repeated complete cycle-boundary states. For stochastic DKLP or Poisson sweep, one unchanged attempt or even a quiet finite sweep does not prove trapping. A nonzero state with no possible nontrivial transition is a certified absorbing obstruction; other timeouts remain censored/unresolved. Do not label all (c,d) logical information loss.

Snapshot error at T and first decoded failure before T are different. For a sampled lifetime, run D on copies at predetermined observation times and report first observed failure, censoring, and spacing. This misses between-sample changes. Exact first-change estimates require checking every event and may be prohibitively costly. Restrict initial study to finite-T endpoints. Fix (L, alpha, T, N, seeds, readout cap) in advance and finish that bounded grid; no threshold or lifetime-law fit is a completion requirement.

## 7. Independent validation required before Monte Carlo claims

- Independent incidence-matrix implementation verifies d1*d2=0 and d2*d3=0 over F2; do not merely reuse the optimized boundary routine as its own oracle.
- Recompute d2 E from scratch after scripted and random event sequences and compare incremental syndrome bit-for-bit. Test periodic seam faces and the four-outgoing/two-face event explicitly.
- Each cube boundary has zero syndrome and six zero homology bits. A cube in directions i,j,k has ij faces at x,x+u_k, ik faces at x,x+u_j, and jk faces at x,x+u_i. Six coordinate logical sheets have identity homology matrix. Translation/seam moves leave closed-chain homology unchanged. Check both parities of L; XOR of every ij face is NOT a correct generic homology formula.
- Small-L full binary ranks satisfy rank(d2)=rank(d3)=3L^4-3 and dim ker(d2)-rank(d3)=6. This is an independent homology oracle, subject to resource limits.
- Every final recovery satisfies d2 D=s. Syndrome-identical inputs must get identical D, even when they differ by a logical sheet; recovered outputs must retain that logical difference.
- Local-box recovery: single face, multi-face disks, seam-crossing disks and translated copies; global fallback: pair of winding syndrome loops, including a thin wrapped strip. Never use hidden E to choose the favorable filling.
- Exact target: incoming-edge veto, all six pairs, all-four fixed pairing, no illegal odd pattern, no cascade within a jump. Toom counterexamples with incoming syndrome establish kernels are intentionally distinct. DKLP energy change invariant as above.
- Scheduler without correction: empirical per-face parity matches (1-exp(-2 lambda T))/2; attempt counts and waiting-time law match specified rates. This stochastic validation is future authorized execution, not performed here.

## Minimum useful own implementation and release gate

Implement geometry + exact target + Poisson-Toom + fixed common readout first; DKLP is a small additional comparator. Keep parallel publication-style modes separate. A first fixed-T comparison is useful only after algebra checks pass and either global readout is complete or unresolved bounds are explicitly shown. Save raw endpoint categories and seeds, not merely averages. No 3D sweep curve substitutes for a 4D incumbent. No small-L Monte Carlo result proves the theorem, its asymptotic exponent, or a useful threshold.
