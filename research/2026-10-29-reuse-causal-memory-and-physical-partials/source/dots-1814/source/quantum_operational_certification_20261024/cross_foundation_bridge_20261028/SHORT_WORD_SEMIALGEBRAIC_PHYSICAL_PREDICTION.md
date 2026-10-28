# Short-experiment physical prediction without a rank or core promise

28 October 2026. **New theorem candidate; not independently received; excluded from the 16:16 freeze.** No source samples or real-algebraic solver have been run. This is an intentionally expensive finite construction, not a practical learner or novelty claim. Its proposed increment over exhaustive horizon-H word acquisition is **experiment length bounded by the supplied physical memory dimension, independently of H**, together with an explicitly computable short-observable-to-prediction modulus. Total samples and classical work may be far worse.

## 1. Supplied finite physical model class

Fix a stationary finite native action/outcome library with `s` branches, at most `b` outcomes per action, and a supplied quantum memory dimension bound `d`. Let `D=d²`. Independent whole-process episode starts and the same complete native action interface at acquisition/deployment are supplied. Neither a tight observable-rank bound, a well-conditioned core, nor a Choi-interior margin is supplied. Arbitrary larger/infinite memory, nonstationarity and new coherent interventions are outside this class.

Let `K_d` consist of every physical dimension-d HQMM described by an initial density `rho` and unnormalized Choi matrices `J_z`:

    rho>=0, Tr rho=1,   J_z>=0,
    sum_o Tr_output J_(a,o)=I_d for every a.              (1)

Use real and imaginary Hermitian matrix entries as coordinates, with their Frobenius weights included in the squared Euclidean metric. This is a rational, closed, bounded semialgebraic set: `Tr J_z<=d`. A smaller physical source can be embedded in dimension d with a separate TP completion on the unused block, without changing its reachable law. No latent source coordinates are supplied to the learner; they are quantified variables.

An optional finite library of truly final POVMs is represented by additional matrices `F_ab>=0`, `sum_b F_ab=I_d`, with at most `t` outcomes per terminal test. Include them in the model coordinates. They add a compact semialgebraic factor; their physical implementation and acquisition costs remain paid. They are not a replacement for post-measurement instruments if memory is retained afterward.

For a native branch word w let `p_theta(w)=Tr Phi_w(rho)`. These are polynomial functions of the model entries, of degree at most `|w|+1`. Optional final-seed probabilities `p_theta(w;a,b)=Tr[F_ab Phi_w(rho)]` have degree at most `|w|+2`.

## 2. Fixed-length words determine the entire classical law

Put

    L=2d²-1.                                             (2)

Let the finite short probability vector `S(theta)` contain all native word probabilities of lengths at most L, and, if present, each such word followed by each declared final-effect seed. Empty native trace is the known constant one. This is a fixed finite experiment pool depending on d and the declared library, not on H or the desired prediction accuracy.

**Short-word equivalence lemma.** If `S(theta)=S(theta')`, the two models have the same probabilities for all native words and all word-plus-final-test events. Consequently their full classical transcript laws agree for every classical feedback controller from their respective specified starts.

**Proof.** On the direct sum of their two real Hermitian Liouville spaces, use block-diagonal transition maps and initial vector `(rho,rho')`. Its reachable span has dimension at most `2D`. The spaces spanned by words of length at most n start in dimension one; once a stage does not grow it is invariant under every native branch. Thus they stabilize by `2D-1`. The row `(Tr,-Tr)` annihilates the entire reachable span if it annihilates those short words. For each final effect, the corresponding row `(F_ab,-F'_ab)` obeys the same argument. Every longer difference is zero. A feedback tree is composed of these word probabilities; private randomization is a convex average. Infinite clocked laws follow by their finite cylinders and almost-sure stopping. QED.

This is conventional finite-dimensional weighted-automaton equivalence, applied to real Liouville representations. [Kiefer et al., CAV 2011, Proposition 2](https://www.cs.ox.ac.uk/andrzej.murawski/papers/cav11.pdf) gives the familiar sum-of-state-dimensions short-witness principle; the direct span proof above supplies the precise `2D-1` bound used here. The quantum counterpart is also established prior art: [Li–Qiu, Theorem 5](https://arxiv.org/pdf/quant-ph/0604085), explicitly gives the `n_1²+n_2²-1` equivalence length for quantum sequential machines by bilinearization. The short-length lemma is not claimed as a new quantum-automata result. Exact equivalence does not by itself provide a stable noisy-data inverse.

## 3. Distance to the equivalence RELATION, not to a physical source model

For a model pair `y=(theta,theta')` in the compact set `A=K_d×K_d`, define

    F(y)=||S(theta)-S(theta')||_2²,
    Z={y in A:F(y)=0},
    g(y)=dist(y,Z)².                                      (3)

Z is nonempty (it contains the diagonal), compact and semialgebraic. Distance to Z is continuous and semialgebraic. Crucially, this is distance of a **pair to the relation of observational equivalence**. It is not distance between theta and theta', nor identification of a physical memory gauge. Distinct, physically far-apart but observationally identical models already lie in Z.

The compact semialgebraic Łojasiewicz inequality implies integers `n>=1` and `C>=1` such that

    g(y)^n <= C F(y),   every y in A.                      (4)

The only external theorem needed here is the standard compact version for two continuous semialgebraic functions with the requisite common-zero relation; see [Basu–Mohammad-Nezhad, Forum of Mathematics, Sigma 2024, Theorem 1.1](https://doi.org/10.1017/fms.2024.66). Apply it to `g=dist²` and F, whose zero sets agree, and enlarge its finite constant to an integer. The article also studies effective bounds, but no uncomputed convenient exponent is imported into the resource ledger.

### Explicit terminating exact procedure for n and C

Do not leave (4)'s constants free. Enumerate positive integer pairs `(n,C)` in a finite-diagonal order. For each, use exact real quantifier elimination to decide the following rational-polynomial sentence:

    for every y in A, there exists z in A such that
        F(z)=0  and  [dist_Euclidean(y,z)²]^n <= C F(y).   (5)

Here `dist_Euclidean(y,z)²` is simply the explicit quadratic sum of squared matrix-entry differences, not a quantified distance function. The constraints defining A are (1) and the optional POVM constraints, using principal minors if desired. Every individual decision is finite. Compactness of Z makes its distance minimum attained, so (5) is equivalent to (4). The standard inequality guarantees that this integer enumeration eventually returns a valid pair. The algorithm may be fantastically expensive; all tested integer pairs, quantified-variable counts, polynomial degrees, exact signs and coefficient bit lengths are charged. It is a finite computable modulus procedure, not an executed computation in this note.

Once certified, n and C depend only on d and the full fixed native/terminal interface. They are independent of the unknown source, its observable rank, H, count outcomes and core conditioning. Rank singularities are paid through this possibly atrocious global modulus, not assumed absent. Standard exact real-algebraic decision/sampling machinery is described in [Basu's survey, Sections 2.1–2.5](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).

## 4. CP stability converts relation-distance into long-horizon prediction

Take `z=(bar_theta,bar_theta') in Z` attaining the distance to y, and let

    a=||y-z|| <= (C F(y))^(1/(2n)).                       (6)

The two barred physical models have exactly the same classical laws by Section 2. Compare each original model to its respective barred model using ordinary CP hybrid bounds. For one individual parameter displacement u,

    half trace distance(initial states) <= (sqrt(d)/2) u,
    half diamond distance(joint action instruments)
                       <= (d sqrt(b)/2) u.              (7)

To see the native bound, `||Delta Phi_z||_diamond<=d||Delta J_z||_F`; sum branches and apply Cauchy–Schwarz. The Choi inequality follows, for example, by the CP order majorants with Choi matrices `kappa I +/- Delta J` for `kappa>=||Delta J||_op`. The two individual displacements have sum at most `sqrt(2)a`; the intentionally loose rational constants below absorb this.

For optional final tests, direct same-state effect comparison gives an additional term at most `t a` for the two sides together. There is no intermediate source-to-fit memory identification. The middle equivalence comparison is **only classical**.

**Long-horizon theorem.** For every H-step classical feedback policy over the declared interface, including a policy selected after the data,

    TV(P_theta,P_theta')
      <= min(1, M_H [C F(y)]^(1/(2n))),
    M_H=d(1+bH)+t.                                      (8)

Set `t=0` when there is no final POVM library. Stopping early can only shorten the physical hybrids; full histories and terminal labels are retained. No enumeration of H-depth feedback trees is needed to establish this bound.

For a calibrated independent abort coin of probability delta before each native attempt, `gamma=1-delta`, both physical endpoints and both barred models terminate almost surely. The same complete-record CP hybrid uses expected native count at most `gamma/delta`, giving

    TV(full clocked transcript)
      <= min(1, M_clock [C F(y)]^(1/(2n))),
    M_clock=d(1+b gamma/delta)+t.                        (9)

Several concatenated memory-retaining invocations from the same start replace the expected native-call cap by its paid sum; the initial-state term remains once. The optional terminal-effect term is once for a genuinely final readout. Memory-retaining macros need their complete native instruments. Arbitrary unclocked infinite-time controllers need another termination/error argument.

Equations (8)-(9) are classical full-law guarantees. Although the outer comparisons use complete physical norms as proof tools, the barred equivalence step gives no external coherent-reference or arbitrary new-input/control guarantee. That gap cannot be closed by terminology. The separately received terminal-test/payload lemma can still be invoked at its stated initially independent datum and identical terminal-circuit interface.

## 5. An explicit count-only finite learner

Fix positive rational accuracy/confidence budgets `epsilon,alpha` (or certified rational budgets no larger than the requested ones), and either H or a positive rational clock delta. First compute/certify n,C by (5), and let M be the corresponding rational upper bound in (8) or (9). Let K be the number of uncertain probabilities in the finite short vector. Choose a positive rational width w satisfying

    4 C K w² M^(2n) <= epsilon^(2n).                     (10)

This can be tested by exact rational arithmetic. For example, choose a sufficiently small dyadic w; no fractional-root oracle is required. Allocate independent complete reset episodes to every short event with

    N_event >= log(2K/alpha)/(2w²),                       (11)

using an outward certified integer upper bound. Record actual complete native outcomes. Each event count is binomial even if different event statistics are pooled from a shared multinomial setting; simultaneous confidence needs only the union bound. Every failed early branch is a charged episode with event indicator zero. No conditional state normalization, restart-until-success oracle or retained coherent calibration reference is supplied.

From empirical probabilities, impose the confidence-valid rational closed intervals of half-width w (or rigorously justified narrower confidence intervals) on a full physical candidate in K_d. Arbitrarily shrinking a confidence interval is not permitted. Exact real-algebraic feasibility/sampling returns a real-algebraic candidate, or a resource-capped implementation returns UNKNOWN. On the confidence event the source is a real feasible point, so an unrestricted exact procedure succeeds even on CP/rank boundaries. There is **no candidate rank constraint** and no data-selected core inversion. Nonempty rational semialgebraic feasibility sets have algebraic sample points; rational approximation is not substituted for exact boundary feasibility.

Both source and candidate lie in the same intervals, so `F<=4K w²`. Equations (8)-(10) certify the target uniformly over all declared classical feedback policies. If a solver only proves wider fit residuals, use their explicit squared difference bound instead; do not retain the original epsilon without charging them.

For the trace-only library, a simple pool bound is

    K <= sum_(l=1)^L s^l,       L=2d²-1.                 (12)

Optional terminal effects multiply/add the appropriate seed count, including zero-native-call tests. Each native-only episode uses at most L native calls. A terminal seed adds its separately declared physical cost. Thus a simple total bill is K times the per-event reset/shot budget and at most L times that many native calls, plus terminal costs. For fixed d/library, an indicative width choice gives sample growth proportional to `(M/epsilon)^(2n)` with the computed C,K factors. This can be vastly worse than both inverse-core local bounds and direct horizon-H acquisition.

All physical candidate evaluation, algebraic-number precision, classical planning, gate compilation, storage, random-sampler and complete-instrument implementation errors are additional paid resources. A mathematical algebraic physical model is not automatically a synthesized laboratory instrument. The theorem asserts finite acquisition under explicit supplied resources, not that its generic construction has been implemented.

## 6. Comparator, attack checks and remaining limits

* **Trivial exhaustive-H baseline.** Measuring every raw word through H already gives finite all-policy classical prediction without a physical model, rank or core. The new proposed capability is only that the maximum native experiment length in (12) depends on d, not H, while (8)-(9) propagate accuracy via CP stability. There is no established total-resource advantage: the modulus and precision can dominate the exponential-H baseline.
* **Long words without a dimension bound.** A larger hidden timer can agree on every acquired short word and diverge later. Finite d is indispensable; the claim does not learn it from counts.
* **Exact equivalence is insufficient by itself.** Linear independence can become arbitrarily ill-conditioned near rank drops. Equation (5), not an assumed well-conditioned spectral reconstruction, pays this global singularity cost. An uncomputed or informal constant cannot support a numerical acquisition claim.
* **Distance between physical models is the wrong target.** Unobservable memory sectors and gauge changes can make identical word laws physically far apart. The set Z is an equivalence relation on pairs, not the diagonal. Replacing it with the diagonal would make (4) false.
* **Comparison with the received residual provider.** A successful residual certificate needs a supplied observable-rank bound and a fitted physical candidate, but need not identify a finite source-memory Hilbert dimension. This global alternative removes rank/core conditioning only by using the supplied physical dimension bound on the actual source. It is a different resource trade, not unconditional domination.
* **Boundary and source physicality.** Non-strict PSD/TP and compactness include unitary channels, projectors, known zeros and lower-rank limits. The source must nevertheless have a finite stationary realization in the supplied d-bound. The construction does not lift arbitrary abstract positive predictive quotients.
* **General controller time.** The clock denominator in (9) is paid. No finite short-word error gives a small uniform error over unrestricted arbitrary horizons; even distinct i.i.d. Bernoulli laws eventually become distinguishable.
* **Prior art.** Finite word equivalence is classical weighted-automata linear algebra; compact semialgebraic error bounds and quantifier elimination are standard; HQMM physical model fitting and the CP realization problem are longstanding, including [Monras–Winter, TQC 2014](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2014.99) and [Srinivasan et al., AISTATS 2018](https://proceedings.mlr.press/v84/srinivasan18a.html). This note proposes their explicit confidence/complete-classical-law composition at the supplied interface, with no novelty certification or quantum learning advantage.

## 7. Exact small-class diagnostics, not generic modulus execution

`short_word_modulus_exact_check.py/.json` checks two analytically certified subclasses:

1. For the **entire d=1, one-action binary instrument class**, `rho=1`, Choi scalars `(p,1-p)`, `L=1`. The midpoint equivalent pair gives exact squared relation-distance `(p-q)^2`, while `F=2(p-q)^2`; hence `n=C=1` is a complete global certificate for this small class. The script additionally checks 3,087 exact finite-horizon Bernoulli laws against both ordinary coupling and the stated conservative CP bound.
2. A **restricted d=3 one-shot family** has `rho(a)=diag(a,1-a,0)` and measure/reprepare branches `Phi_1(X)=b Tr(P_A X)|sink><sink|`, `Phi_0(X)=Tr[(I-bP_A)X]|sink><sink|`. Every native Choi lies on the boundary, and observable rank drops from two to one at `ab=0`. Its entire law depends on `ab`; for `L=17`, `F=2L(ab-a'b')^2`. Reducing one coordinate of the larger product constructs an equivalent physical pair with squared parameter distance at most `2|ab-a'b'|`, proving `n=2,C=2` on this restricted family. There are 625 exact repair and clock checks.

On the restricted singular ray `(a,b,a',b')=(e,e,0,0)`, the squared relation-distance is exactly `2e²`. A sum-of-squares identity on `ab=a'b'` proves the lower bound. Thus a linear distance modulus fails **for this constrained family**. This is not claimed to prove that exponent one fails for the entire d=3 physical HQMM relation: allowing additional physical model directions may supply closer equivalent repairs.

The same family explicitly shows why distance to the relation is essential: `(a,b)=(1,0)` and `(a',b')=(0,1)` have identical all-zero word laws but squared physical parameter separation four. Their pair belongs to Z and has relation-distance zero. A diagonal-identification replacement would fail.

**Current status:** owned derivation and exact small-class evidence only; independent theorem review is pending. No generic n,C quantifier-elimination computation, candidate feasibility solve, acquisition, or physical synthesis has been performed. All diagnostics have zero source calls, episode starts and RNG calls. The received normalized/raw-core residual results remain separate and are not weakened or overwritten by this global alternative.
