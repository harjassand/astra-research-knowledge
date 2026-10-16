# Reverse-radius genesis: support closure and a quantitative payoff boundary

Worker: gb_reverse_genesis. Date: 16 October 2026. Repository pin: `61389569d6c53b439764f0d148b35b7fa6083eec`. Scope: independent proof reconstruction, two focused consequences, exact finite checks and bounded primary-literature comparison. No other worker's reports were read; no new agents or outbound account messages were used; the pinned repository was not edited.

The strongest result is a quantitative separation between a maximal complete-order threshold and usable decision value. Two arbitrarily close distinct pure qubit outputs have complete erasure threshold one, yet their largest binary-MMSE advantage is only proportional to their squared separation. An explicit optimal physical simulator from erasure gives the all-reference upper bound, while an analytic Bell encoding gives a matching-order lower bound. Ruling out the source-simulable alternative has a corresponding information cost.

The supporting singular-output theorem is proved directly, but is a reconstruction rather than a newness claim: older Astra N402 already contains its density-radius form inside a broader internally claimed Choi theorem. The supplied new CQ packet had explicitly excluded singular outputs. This report closes that narrow missing endpoint without depending on N402's broader claims.

## 1. Support-exact CQ endpoint

For prepared states sigma_i>=0 define S=intersection_i supp(sigma_i), G_i=(P_S sigma_i^+ P_S)|_S and

    C = 1-min_{p in Delta_m} Tr_S (sum_i p_i G_i)^-1,

with trace zero when S is zero. S is fixed by ALL channel inputs even when some p_i vanish. The same C is the unrestricted complete conditional RLD coefficient and the ordinary unsmoothed complete SLD/binary-MMSE erasure reveal threshold.

The authored proof is [proofs/SINGULAR_CQ.md](proofs/SINGULAR_CQ.md). The decisive lower construction calculates the singular Schur complement by constrained quadratic minimization. It proves W lies in the range of the compressed output baseline before regularization, supplies the explicit kernel-vector minimizer, and then proves convergence only for the supported inverse quadratic costs. Physical Hermitian tangents are realized in the frame dimension m-1; one coherent flag supplies a strict faithful SLD/MMSE witness in dimension at most m. No swap of a supremum and an uncontrolled output limit is used.

The support distinction has exact counterexamples. For two distinct pure states S=0 and C=1, however close they are. At identical pure states C=0. Naively substituting pseudoinverses without the range condition yields the impossible value -7 on |0> and |+>. For an exact noncommuting rank-two qutrit pair, the correct common-support coefficient is 5/8; compressing the states before inversion incorrectly gives 1/2. These are finite illustrations of the proof obligations, not a replacement for the general proof.

Novelty status: the support geometry is standard parallel-sum theory, and the CQ density radius is latent in older internal N402 Eqs.(3.3)-(3.4). This is a smaller direct reconstruction and an endpoint closure for the supplied packet. Historical scientific novelty is UNKNOWN.

## 2. Exact pure-qubit simulator and matching-order payoff

Let sigma_±=(I+bZ±aX)/2, 0<a<1, b=sqrt(1-a^2), c=a^2, and c<=q<1. The reference-free SLD/MMSE reveal threshold is c, while the complete threshold is one. Define

    delta_* = sqrt(q^2+2(1-q)(1-b))-q.

Then delta_* is exactly the minimum diamond distance, without a factor 1/2, from this preparation channel to any physical postprocessing of E_q. The optimal simulator prepares |0> on erase and the pure Bloch states (±a,0,b-1+q)/L on reveal, where L=q+delta_*. Its optimality follows from symmetry and the geometry of the qubit Bloch ball.

For Gamma equal to the supremum binary-MMSE advantage over every finite reference and every encoding,

    c/(1-c)(1-sqrt(q))^2
       <= Gamma
       <= min{1,2 delta_*}.

Both bounds are proportional to c as c tends to zero at fixed q. The upper bound is global and uses an actual physical simulation. The lower bound is an achieved supremum in the explicit qubit-reference Bell family; it is not a global-optimality claim.

The full Bell-family supremum has a necessary piecewise qualification: it is c-q when 0<=q<=c^2=a^4, and c/(1-c)(1-sqrt(q))^2 when c^2<=q<1. The main comparison uses c<=q and therefore always lies in the second branch. The proof explicitly excludes the erroneous extension of that branch down to q=0.

At the exact finite faithful fixture a=3/5, b=4/5, q=625/1681, delta=1/9 and t=3/10, source optimal MMSE is 5995/6724 and target Bell-optimal MMSE is 3371/4100. Their difference is

    2916/42025 = 0.06938726948245093...

This is a new ideal fixture relative to the supplied mixed-state Bell construction, with one qubit reference and a fixed four-outcome Bell basis. It is not an implemented experiment or a globally optimal encoding. The proof and all parameter scopes are in [proofs/PURE_QUBIT_PAYOFF.md](proofs/PURE_QUBIT_PAYOFF.md).

## 3. Practical information costs and the matched incumbent

The source comparator receives the same input label ensemble and reference. Its physical approximate simulator is state-independent and requires only preparation conditioned on the erasure/reveal symbol. Thus its approximation guarantee persists for arbitrary reference dimension and joint receivers. A threshold-only argument cannot dismiss this matched comparator.

Without a free promise of exact purity, an audit that must distinguish the actual target from this particular physically source-simulable alternative has final-state trace distance at most n delta_* after n adaptive calls. Equal-prior discrimination success at least 3/4 therefore requires n>=1/delta_*=Omega(a^-2) at fixed q. This is a scoped worst-case channel-discrimination lower bound, not a blanket claim about every inference task with extra prior promises.

An ideal IID Bell evaluation can have sufficient sample count O(a^-2), using its loss variance of order a^2, rather than the cruder bounded-loss count O(a^-4). This does not include calibration, receiver fitting, drift, losses or reset. At the useful family optimum, the small reference population and its eigenvalue floor are themselves of order a^2; a rare Bell sector carries order-one scores with probability of that order. That preparation/precision burden is part of the task, not granted by the exact theorem.

No laboratory state data, acquisition/calibration counts, receiver synthesis, detector efficiencies, reset/energy costs or measured matched advantage were supplied or acquired in this worker. Physical implementation, practical efficiency and overall technology advantage remain UNKNOWN.

## 4. Verification and predecessor ledger

Run `python3 checks/verify_exact.py` from this directory. It passed in the current environment, producing [checks/results.json](checks/results.json). It verifies five groups: the symbolic noncommuting qutrit Schur formula and boundary value; range containment in a rank-three four-dimensional frame baseline and its faithful-input continuation; the unsupported-pseudoinverse counterexample; the exact faithful two-input Bell fixture with source optimum and target Sylvester solution; and the piecewise-family derivative/formula identities. These checks do not formally verify the general theorems.

Primary theory predecessors were read at their exact sections: Fillmore-Williams / Anderson-Duffin for range intersections and parallel sums, Mosonyi-Bunth-Vrana for left radii and support restrictions, Zhu-Wang for signed complete variance lifts, Hirche for binary-MMSE/SLD and smoothing boundaries, and Jenčová for CQ diamond norm and channel deficiency. The particular erasure-deficiency geometry and asymptotic payoff bounds are the candidate addition, using standard machinery. The bounded search establishes neither absence of predecessors nor priority. See [SOURCES.md](SOURCES.md) and [sources/SOURCE_MANIFEST.json](sources/SOURCE_MANIFEST.json) for exact source copies, versions, sections and hashes.

The final artifact status is INTERNAL_PROOF_AND_EXACT_EXAMPLES. External review, formal certification, historical novelty and physical/practical capability are UNKNOWN. FROZEN.json records the final authored/source/check files and their hashes; freezing records integrity only.
