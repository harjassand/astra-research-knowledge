# Independent hostile audit: depolarization-assisted exact Poissonization

2026-10-29 UTC. Exact inputs are pinned in `SOURCE_SHA256.txt`; lead text, original checker and original JSON are copied here unchanged. The original checker was rerun separately. No original source was edited.

## Verdict

**The finite-dimensional exact lemma is correct.** Its use for an unconditional autonomous decoded-memory channel is valid conditional on the accepted arbitrary-local-CPTP-kick memory/physical-compiler contracts, provided the deliberate full-patch depolarization is actually supplied, the strength/support bounds are calibrated, and the final decoder does not depend on the original detector record.

This is a modified physical architecture, not a theorem about the unmodified generator. It does not cover arbitrary common retained baths or turn independent onsite depolarization into a joint-patch cushion. For deformed reset operators, the restored clean reset records belong to an alternative genuine CP unraveling of the same modified system generator, not necessarily to the original laboratory detector instrument.

## 1. Norm convention and exact Choi lemma

Use the normalized maximally entangled vector |Omega_d>=sum_i|i,i>/sqrt(d) and J(N)=(id⊗N)(|Omega><Omega|). Its input has trace norm one, so ||J(N)||_1≤||N||_diamond, with no extra d factor. HP implies J(N) is Hermitian. The normalized Choi matrix of full depolarization Delta(X)=Tr(X)I/d is I_(d²)/d². Thus

J(Delta+N/delta) ≥ [1/d²-epsilon/delta] I ≥0

when delta≥d² epsilon. Trace annihilation of N gives trace preservation of Phi. The displayed generator identity is then exact by expansion. Neither N alone nor its summands need be GKSL. This is not a small-time Euler map id+dt N: the interior channel Delta supplies the full-rank CP cushion.

Endpoint convention: if epsilon=delta=0, the formula N/delta should be replaced by the trivial N=0/no-added-kick case, or choose any positive delta. No substantive claim fails at that endpoint.

The stated estimate 2||h||+2sum||K||² is a valid diamond-norm bound for a Hamiltonian commutator plus Lindblad dissipators. It is conservative, not an exact diamond-norm calculation.

## 2. Unknown deterministic time dependence and calibration

A fixed delta_Z chosen from a uniform worst-case epsilon_Z makes every Phi_Z(t) CPTP. A rate-delta_Z independent Poisson clock with the deterministic-time-dependent channel Phi_Z(t) at its event time has the exact time-dependent generator in the text. No Trotter approximation is needed even when supports overlap. Finite bounded incidence controls the summed primitive-rate budget, not merely the maximum rate of one of arbitrarily many supports.

The channel need not be characterized online, but the support architecture, finite patch dimensions, and a reliable uniform strength upper bound do need to be known. Noise may vary adversarially in deterministic time within that bound. Unbounded unknown support, uncontrolled non-Markovian bath coupling, or arbitrary dependence on unmodeled detector history is not thereby covered.

The depolarization resource itself must have a certified implementation or its deviation must be included in N. There is a possible self-consistency budget, not a free perfect-noise assumption: if an implementation deviation has norm at most eta*delta in addition to external epsilon_ext, this proof requires delta≥d²(epsilon_ext+eta*delta). A sufficient feasible choice exists when d² eta<1, with delta≥d² epsilon_ext/(1-d² eta), and this rate must still lie below the kick theorem's threshold. The manuscript's instruction to charge implementation errors is necessary.

## 3. Signed reset-deformation differences

For a local actual-vs-clean generator difference N=L_actual-L_clean, HP and trace annihilation hold even when N is not itself a Lindbladian. The Choi lemma applies directly. For matched local jump operators A,B one useful small-deformation estimate is

||D[A]-D[B]||_diamond ≤2(||A||+||B||)||A-B||,

plus 2||Delta h|| for a Hamiltonian change. This permits a small signed deviation budget; merely bounding both generators separately can produce a useless large bound. Completely removing a strong clean reset generally costs a strong deviation and is not made threshold-small by algebraic relabeling.

After adding the actual cushion, L_actual+delta(Delta-id)=L_clean+delta(Phi-id) is a bona fide GKSL decomposition. In contrast to an arbitrary nominal subtraction without a cushion, deleting a clean-reset gain from THIS explicitly positive decomposition does define a CP killed instrument.

## 4. Alternative CP records versus original detector records

An identical time-local system generator gives the identical system propagator for the specified initialization. The RHS decomposition admits an honest positive trajectory instrument with clean reset/monitor channels and independent CPTP-kick clocks. It may be viewed as an alternative Markov dilation/unraveling; its classical records are valid CP analysis records.

If the memory theorem is about the unconditional system output followed by a fixed decoder depending only on final system registers, all its mark, killed-map, and common-correctable-span estimates can be proved in that alternative instrument and then the records summed out. Generator equality transfers the resulting decoded channel bound to the actual modified device. The forest-frame decoder described in the cited compiler interface depends on final controller state, not an externally supplied jump log, so this route is compatible with that interface.

It does NOT identify alternative clean-reset labels with the detector clicks from deformed physical reset operators. It does not establish their measured waiting-time law, marked-emission probabilities, heralded/postselected logical channel, or detector-conditioned recovery. If original detector outcomes drive external future feedback, are retained as a required output, or reveal a non-Markovian bath that later reinteracts, equality of reduced system generators alone is insufficient. Such records/feedback must be explicitly included in the modeled system, and the enlarged support/dimension assumptions rechecked.

Thus the earlier prohibition on fictional nominal records is not contradicted: before Poissonization nominal subtraction could be non-CP; here a new actual full-rank dissipative primitive supplies an exact CP decomposition. The valid claim is an alternative CP analysis instrument for unconditional autonomous output, not preservation of original detector statistics.

## 5. Onsite native-architecture corollary

For each finite-dimensional physical qudit, full depolarization has onsite Lindblad jumps sqrt(delta/d)|a><b| for all a,b. Their gains sum to delta Delta and their complete loss is delta I. This requires d² fixed onsite channels, which is a fixed cost when each site dimension is fixed independently of system size.

Therefore arbitrary bounded onsite HP trace-annihilating deviations on full physical data/controller/workspace/monitor sites can be cushioned with actual onsite full depolarization. The equivalent noise kicks are onsite CPTP maps and are included in an accepted compiler theorem covering arbitrary local site faults. The clean two-site Hamiltonian/onsite dissipative form is preserved. No new all-resource or multi-site dissipative primitive is needed for this ONSITE-noise corollary. Controller faults must still be charged through the compiler's mark/service and support-incidence contracts, not treated as harmless data noise.

This statement does not cover arbitrary errors in two-site Hamiltonian couplings using only independent onsite cushions. A support-Z perturbation needs full JOINT depolarization on Z (or a proved alternative full-rank cushion), potentially adding multi-site dissipation outside the original native architecture.

## 6. Explicit onsite-versus-joint counterexample

For two qubits let N=-i[X⊗X,.] and add the sum of the two onsite depolarizing generators. In the normalized Choi matrix of id+[N+delta(D_1+D_2-2id)]/Lambda, the vector |XX>> has zero diagonal cushion but a nonzero offdiagonal entry to |I>> from the Hamiltonian commutator. A positive matrix with zero diagonal on a vector must have zero cross entries there, so the candidate is non-CP for every finite Lambda>0, regardless of how large the onsite depolarization rate is. This directly disproves an unrestricted replacement of joint patch depolarization by independent onsite generators.

The independent numerical checker records negative Choi eigenvalues -0.0116062 at delta=1,Lambda=10 and -0.000101512 at Lambda=100. This is a preserved boundary counterexample, not a failure of the correctly stated full-patch lemma.

## 7. Retained bath boundary

Data-only depolarization tensor identity on a bath is not full joint depolarization: its Choi matrix is rank-deficient in bath directions. Arbitrary joint Hamiltonian/dissipative terms can couple into those uncushioned directions, defeating the minimum-eigenvalue proof. An accessible finite local ancillary factor can be included and depolarized at the larger fixed d. A generic shared retained bath cannot. The claim excludes it correctly; the broader retained-bath strength of the older kick theorem does not broaden this reduction automatically.

## 8. Composition and remaining obligations

The atomic conclusion follows directly from the accepted ideal atomic CPTP-kick theorem with delta_Z as primitive rates, conditional on its D0/D1 contracts. The physical transactional conclusion similarly follows only from the accepted full compiler interface: correct initialized state, coefficientwise current-syndrome SSF semantics, bounded enlarged dressed support/incidence, physical-window mass and service moments, and the declared final mathematical decoder. Poissonization supplies the missing continuous-Markovian-to-positive-kick interface; it does not reprove those contracts or provide efficient/noisy physical readout.

The nonzero admissible epsilon threshold can be extremely small due to d_Z² and compiler constants. No practical rate, advantageous hardware overhead, passive thermal implementation, generic non-Markovian threshold, or unchanged detector-record guarantee is established.

## Fresh evidence

* Original `check_poissonization.py` rerun, with output saved separately; PASS.
* Independent 30 signed HP trace-annihilating trials in dimensions 2,3,4: all Phi Choi matrices positive; maximum generator identity residual 4.58e-16 and TP residual 1.12e-16.
* Explicit non-GKSL negative dissipator difference -D[lower] successfully cushioned.
* Onsite-vs-joint negative examples preserved in `independent_signed_checks.json`.

These finite matrix tests supplement the analytic argument, not replace it. No permission/tool blocker occurred.
