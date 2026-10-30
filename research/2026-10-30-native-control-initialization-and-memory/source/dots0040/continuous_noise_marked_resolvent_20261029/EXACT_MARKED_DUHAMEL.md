# Exact marked Duhamel resolution and a uniform first-reinsertion bound

2026-10-29. New, not independently reviewed. This is an actual algebraic construction for the reset-first forest-gauge generator, not a continuous-noise memory theorem.

## Result first

One can resum **every exterior perturbation** as genuine CPTP evolution, track only the still-unregenerated controller neighborhoods touched by one specified local insertion, and obtain a first-reinsertion remainder bounded by

    ||remainder||_diamond <= delta eta m C/r_bar,

uniformly in system size and observation horizon. Here delta is the diamond norm of the specified insertion, m its bounded number of initially marked owners, eta the incident perturbation norm budget per marked owner, and C/r_bar the uniform actual-reset residence bound. The insertion may be non-CP. No positive Poisson noise record, Pauli twirl, independent clock law, or external stop is used.

This gives a concrete inclusive single-seed fault-burst resolution. It does NOT yet bound the all-orders growing cluster needed for the memory threshold. The precise outstanding step is identified below.

## 1. Assumptions already available, and permitted continuous noise

Work in the exact full-Hilbert forest frame. The nominal generator L0 has actual separately recorded terminal/abort gains J_h. Its controller-only evolution and complete reset output identities hold on the full Hilbert space. Add local generators K_e(t), each either a Hamiltonian commutator or an added positive Lindblad generator. Every subset of these terms therefore remains a legitimate CPTP generator. The nominal reset channels remain actual channels; arbitrary changes to those reset operators are NOT covered.

Write H_e for the owners whose history-neighborhood support intersects the transformed support of K_e. Assume |H_e| <= b and

    sum_(e: h in H_e) ||K_e(t)||_diamond <= eta.

All supports and b are fixed graph-local constants. The commuting forest frame gives bounded support enlargement without iterative spread.

Use the existing local killed-generator Lyapunov witnesses Z_h, alpha I <= Z_h <= I. Their local perturbation estimate applies to Hamiltonian and positive Lindblad additions, not just kicks: it uses their adjoints annihilating I, local norm bounds, and the actual killed-map CP property. At sufficiently small incident noise on the larger Z supports it yields a common r_bar > 0 for EVERY subset of the added terms. Thus C=alpha^(-1) gives a uniform no-designated-reset bound C exp(-r_bar t), also for time-dependent subset choices and classical-record-adapted choices. For the latter, apply the same operator drift in each direct-sum record sector; record transfers that do not clear h preserve its witness.

## 2. Protected instrument

Start a classical analysis label M=M0. It is not measured on the quantum system. In label M use the generator

    L_M(t) = L0 + sum_(e: H_e intersect M is empty) K_e(t).

Every L_M is CPTP. Route each ACTUAL J_h gain to label M minus {h}; all its physical outputs remain unchanged. Other physical records keep M. The label is thus determined by initial M0 and actual reset records. Once M is empty, the process is the full noisy generator forever. This construction is an analysis instrument with record-dependent coefficients, not an autonomous hardware modification or an available external disable operation.

For each h initially marked, its survival label means exactly that no actual designated h reset has occurred. The Lyapunov estimate gives, as a CP instrument effect inequality,

    effect(h still marked at t) <= C exp(-r_bar t) I.

Summing owners therefore bounds the positive active-occupation instrument by

    effect(weight |M(t)|) <= m C exp(-r_bar t) I.

This estimate includes arbitrary exterior noisy evolution, arbitrary entangled initial states, and all actual quantum reset/monitor records. The initial local insertion need not produce a state: the resulting CP-instrument norm bound can be composed with any superoperator E of diamond norm delta.

## 3. Exact routed Duhamel lift

For a deleted term e with H_e intersect M nonempty, insert K_e and route its output to M union H_e. On the direct sum of mark sectors this is a generally signed, non-CP off-diagonal transfer. Keep the protected generator and actual reset routing of Section 2.

Summing over labels gives EXACTLY the physical generator L0+sum_e K_e: each deleted K_e is restored once, and each nominal reset gain is neither deleted nor duplicated. This identity holds for actual physical record instruments as well as their sum. It is an ordinary finite-volume Dyson/Duhamel identity on an enlarged linear space. It is NOT a probability distribution over marks or perturbation insertions.

Equivalently stop at the FIRST routed perturbation. Before it use the protected instrument; after it use the complete full noisy CPTP instrument and discard analysis marks. This first-insertion Duhamel identity is exact for every finite horizon T. The empty-label sector has no remainder, so the time integral automatically stops at regeneration of all initial marks.

## 4. Uniform first-reinsertion remainder

In label M the sum of deleted generator norms is at most eta |M|. Future full noisy evolution, including retained actual records, is CPTP and has diamond norm one. The direct-sum norm bound and Section 2 therefore give

    ||R_T E||_diamond
      <= delta integral_0^T eta m C exp(-r_bar t) dt
      <= delta eta m C/r_bar.

This is uniform in N and T. It is stronger than a fixed-duration epsilon T estimate for one dirty seed: its exposure is the actual finite-rate regeneration residence time, not the final observation horizon. It avoids exp(N epsilon T) because no exterior perturbation was ever expanded.

On the protected term each initially marked owner has at most one possibly malformed terminal/abort DATA emission, then complete reset. Its no-further-touch protected history is good thereafter until a later exterior/background perturbation hits it. The latter is already part of the resummed background, not silently declared absent. Pending emissions at T remain explicit marked controller state; dressed output keeps the exact finite-horizon equality. They must NOT be discarded or counted as an already completed channel.

## 5. What this does not prove, precisely

The bound is an inclusive influence/episode statement against an otherwise fully noisy background. That background can contain other dirty hubs. Accordingly it is not a declaration that all unmarked events are intended SSF operations. Applying the coefficientwise clean-history lemma globally still requires expanding or controlling every perturbation that creates the witness cluster.

Repeated use of the routed identity grows M by up to b owners at each reinsertion. A naive scalar iteration of the bound in Section 4 produces factors proportional to

    m (m+b) (m+2b) ...,

and is NOT a convergent geometric series. Chronological simplex factors cannot simply be asserted to cancel these factors after random reset stopping times. Nor may signed routed histories be treated as a classical contact process without proving an appropriate CP majorant and cluster estimate.

The missing theorem is a connected, growing-mark inclusive norm estimate that exploits LOCAL births and ACTUAL reset deaths, resums every exterior term, and controls arbitrarily long-lived or merging clusters. The existing joint killed-reset bounds are promising inputs but do not alone constitute that theorem. A proof must also couple the resulting cluster envelope to the backward SSF witness rather than replace its state-dependent schedule by an independent one.

Thus this construction closes the single-seed residence-time obstruction, but not the all-seed/combinatorial obstruction. It supplies a concrete exact resolvent on which a genuine continuous-noise proof can operate; it is not a new conditional memory claim.

## Sources within the construction

- producer-workspace/FULL_HILBERT_FOREST_GAUGE.md
- producer-workspace/COEFFICIENTWISE_COMPILER_INTERFACE.md
- producer-workspace/JOINT_LOCAL_LYAPUNOV_TAIL.md

No previous reviewed file was edited.
