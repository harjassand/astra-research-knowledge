# Noisy refresh robustness: independent challenge and closest prior art

Date: 2026-10-16. Scope: finite-dimensional local channels, fixed schedules, shared persistent bath, causal all-accept effects. This is a bounded mathematical audit and primary-source check, not external validation, a novelty certification, or a physical threshold claim. No acquired code, numerical experiments, outreach, publication, or repository changes were used.

## Bottom line

The dimension-free CP-majorant step is valid. For channels N and T on the same full local-system–persistent-bath input/output, with epsilon = (1/2)||N-T||_diamond, there are CPTP channels E_plus,E_minus on those same spaces such that

    N - T = epsilon (E_plus - E_minus),
    N <=_CP T + epsilon E_plus.

Under the additional reservation-locality and causal-interface assumptions below, first-fault expansion gives the endpoint/record-event bound

    Pr(all selected parents accept)
      <= product_i min{1, f_i + sum_k epsilon_ik}.

Here f_i is the exact tester's already-proved uniform singleton bound, and k ranges over imperfect nodes of parent i. Shared bath memory does not invalidate this result. Reduced-channel calibration, unrestricted cross-parent node support, or a claimed actual good/fault Kraus decomposition would invalidate the argument. The norm/majorant machinery and stopped fault expansions have substantial prior art; the refresh-specific embedding and erasure transfer are the application-level contribution requiring proof.

Inputs read: causal_refresh_product/PROOF.md and memory_support_transfer_audit/AUDIT.md. The one-node and multi-node proposed contracts were directly challenged with the deriving worker.

## 1. The exact contract that survives the challenge

At each node (i,k), both N_ik and its specified ideal T_ik are CPTP maps on D_i tensor B, tensored with identity on every other currently active full reservation. D_i is the entire physical reservation, not just a nominal weak-error footprint. B includes all persistent bath and controller degrees of freedom that can interact again. Input entanglement with arbitrary references is allowed. The diamond estimate is uniform on arbitrary D_i B inputs; it is not evaluated only on the physical bath's marginal calibration state.

The exact-node process must already have the causal tester implementation and uniform singleton value f_i. Preserve its fixed/exogenous schedules, exact entry/retirement requirements, own-odd/other-even interface, and private inaccessible measurement environments. A node noise environment that returns later belongs in B; it cannot be traced out and silently treated as fresh private garbage. The independent testers are mathematical private resources. The persistent shared bath is a single unrestricted prover resource.

Identity on all other reservations is a clean sufficient assumption. A weaker other-parity-preserving support condition might also work, but would need its own CP-majorant support argument. A small full-joint diamond distance alone supplies no spatial or reservation locality.

## 2. Dimension-free CP majorant, including the factor 1/2

Write Delta=N-T, d=||Delta||_diamond. The Hermiticity-preserving diamond-norm dual supplies a normalized channel Choi operator R with

    -d R <= J(Delta) <= d R.

For d>0 set J(E_plus)=R+J(Delta)/d and J(E_minus)=R-J(Delta)/d. Both are positive. Because Delta is trace annihilating, both partial output traces are identity, so both maps are CPTP. Subtracting proves the displayed decomposition with epsilon=d/2. The d=0 case is immediate. Equivalently the one-sided channel-discrimination SDP minimizes ||Tr_out Z||_infinity subject to Z>=0 and Z>=J(Delta); its value is d/2. Completing its common trace slack yields the same pair of channels. There is no bath-dimension factor.

This is standard SDP machinery: [Watrous, 2013, Section 3.2](https://cs.uwaterloo.ca/~watrous/Papers/SimplerSDPforCBnorm.pdf) gives the general Choi SDP, from which the Hermitian symmetry reduction follows.

For an entire multiround object the appropriate metric is the strategy norm, not the diamond norm of a channel obtained by closing or ignoring its intermediate ports. [Gutoski, 2010/2012, Section 4, equation (2), Theorem 3](https://arxiv.org/pdf/1008.4636) gives the analogous normalized causal majorant. A difference of deterministic strategies satisfies homogeneous causal trace constraints, so the same plus/minus construction remains deterministic and yields the half-strategy-norm coefficient. Full-joint one-node diamond estimates suffice here because nodes are replaced before composition with the remaining causal circuit.

## 3. Why shared-bath correlations do not defeat the product

Use positive comparison branches, not conditional probabilities given generated fault records. Replace a noisy node by T_ik + epsilon_ik E_ik. On the T branch keep that parent's exact tester. On its first E branch, remove that parent's acceptance constraint and stop expanding its subsequent nodes. Its later ACTUAL N nodes are already normalized CPTP operations and therefore cost no additional multiplicative factors.

In a single chain this is the positive version of

    N_m ... N_1 - T_m ... T_1
      = sum_k N_m ... N_(k+1) (N_k-T_k) T_(k-1) ... T_1.

For interleaved parents, branch chronologically only at nodes belonging to parents still retained as testers. Each parent is either exact at every node, or has a specified first error location k with coefficient epsilon_ik. After dropping a parent, move all its private mathematical registers to the prover, allowing the inverse sector-coordinate embedding to reconstruct D_i coherently if necessary. This only enlarges the prover. No actual measurement, reset, or postselection is introduced.

Reservation disjointness is decisive: an arbitrary error channel on the erased D_i B and all its later physical operations remain prover operations relative to every surviving tester. They can correlate bath states, learn from the erased tester, and change future strategies, but cannot directly access surviving private parities or records. Every positive branch is a normalized causal process against the surviving exact independent testers. Its all-accept probability is at most the product of their f_i values. Sum first-error choices to obtain product_i(f_i+sum_k epsilon_ik).

The separate cap is valid by first discarding every target constraint whose factor exceeds one, then applying the proof to the remaining subset. It is not obtained by capping individual terms inside an unnormalized expansion.

The exact all-accept tensorization is established machinery: [Gutoski–Watrous, 2007, Theorem 9](https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf), printed page 13 in that PDF, identifies the maximum forcing probability with the minimum normalized positive causal majorant. Products of compatible deterministic combs are deterministic. This does not assert independent outcomes or independent prover operations.

## 4. Exact counterexamples that delimit the statement

### A. Reduced marginal diamond errors do not imply local-stochastic products

Let F be a single classical bath bit, initially 1 with probability epsilon and 0 otherwise. All k parity bits start in 0. The ideal refresh is computational-basis dephasing D_Z. At node i apply D_Z and then X_i if F=1, preserving F. For an isolated marginal experiment with that bath distribution, the channel on i is

    N_i,reduced = (1-epsilon) D_Z + epsilon Ad_X D_Z,
    (1/2)||N_i,reduced-D_Z||_diamond = epsilon.

Yet the actual shared-bath experiment has every endpoint flipped exactly when F=1:

    Pr(all k fail) = epsilon, not epsilon^k.

The full joint controlled channel is distance one in half-diamond norm from D_Z tensor id_F: choose input F=1 and parity 0. Thus this example violates the uniform full-joint contract, precisely where the product proof needs it. Even if only one bath state is physically prepared, replacing the uniform assumption by that state's reduced calibration does not recover the theorem. Conditioning on the first failure makes all later failures certain.

### B. Full-joint closeness without own-reservation locality also fails

At a single node assigned to parent 1 apply, with probability epsilon, X_1 ... X_k after ideal dephasing of all bits; otherwise apply the ideal channel. Its half full-joint diamond distance is epsilon. With zero charged actions and all other nodes exact, all k endpoints nevertheless flip with probability epsilon. Any formula assigning this error only to parent 1 and retaining zero factors for the other parents is false. The faulty operation touches their private data. A shared bath is harmless only while its interface cannot do this.

### C. A CP upper comparison is not an actual good/fault instrument

For N=Ad_U with U close to but not proportional to identity, J(N) and J(Id) are distinct rank-one rays. There is no nonzero positive Choi operator below both. Therefore diamond closeness need not give any positive ideal-identity subchannel of N. The virtual E branches above cannot be named actual physical fault events or used as an actual Kraus-history refinement.

For the memory-support transfer there is an even simpler obstruction: let L be a nontrivial logical Pauli on D_i that commutes with every measured syndrome. The channel

    N=(1-epsilon) T + epsilon Ad_L composed with T

is at half-diamond distance at most epsilon from T and can have zero endpoint syndrome mismatch while causing a logical error. An endpoint-effect bound alone consequently does not supply the old endpoint-good support certificate. One needs a genuine qualified CP refinement or a separately proved no-local-logical condition on the UNION of every weak/noisy footprint, with all reservation costs retained.

## 5. Closest primary fault-tolerance context

1. [Aliferis, Gottesman, Preskill, Quantum accuracy threshold for concatenated distance-3 codes, 2005/2006, Section 11](https://arxiv.org/pdf/quant-ph/0504218). The closest broad shared-bath antecedent: local fault paths have norm bounds for any designated faulty set, while other locations are unrestricted. The bath Hamiltonian can be arbitrary; locality is imposed on the system coupling. See the Local Noise definition/equation (59), Section 11.1, and the final discussion in Section 11.4. Their coherent fault-amplitude norm bounds and recursive threshold construction are not this refresh endpoint-effect theorem. Their Section 11.6 also discusses syndrome-induced decoherence, relevant context for why probability-level gains need a proved record interface.

2. [Terhal and Burkard, Fault-tolerant quantum computation for local non-Markovian noise, 2004/2005](https://arxiv.org/pdf/quant-ph/0402104). Earlier local non-Markovian threshold machinery. Their original bath restrictions are stronger, so it is inaccurate to cite this theorem alone for unrestricted shared baths. Nevertheless the proof of Lemma 5 already stops branching after specified faults and appends the remaining full evolution, a clear antecedent of the stopped-expansion bookkeeping used here.

3. Gutoski–Watrous and Gutoski, linked above, are the nearest primary mathematical sources for positive causal all-accept domination and normalized strategy-norm majorants. Watrous is the direct one-node diamond SDP source. Neither the existence of dimension-free majorants nor causal all-accept tensorization should be presented as new.

Bounded novelty assessment: the verified general ingredients are established. The potentially useful specific interface is the combination of the already-proved exact refresh tester embedding, local full-joint channel perturbations, erasure of a faulted parent, and the resulting parentwise additive robustness budget. No claim that the exact combined formulation is historically new follows from this targeted search.

## Final audit disposition

PASS, conditional, for the endpoint/record-event product bound under Section 1's full contract, with per-parent error budget sum_k epsilon_ik and no dimension penalty. FAIL for marginal-only calibration, for arbitrary cross-reservation noisy nodes, or for inference of an actual good CP support refinement solely from the upper comparison. Hardware qualification, calibration feasibility for all bath inputs, noisy endpoint records, scalable implementation, and a physical threshold remain separate tasks.
