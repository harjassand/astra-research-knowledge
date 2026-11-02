# Ocko–Yoshida shielding: primary-source audit and new thermal deductions

2026-11-01. Follow-up to independent clock construction. No claim of novelty for clocks, controlled-prefix unitaries, or shielding.

## Primary-source facts (concise)

[Ocko–Yoshida, arXiv:1107.2697v3](https://arxiv.org/html/1107.2697) uses replicated toric-code data grouped into bounded-dimensional plaquette particles. Z plaquettes become onsite, equality constraints stay two-body, and only X stars require clocks. Two-clock diagonal shielding cancels equality-induced interactions **inside the ground-compatible invariant sector** M(0). Other invariant sectors retain interactions on violated equality links. The authors establish ground-space local-unitary equivalence, localized excitations, and a size-independent spectral gap; the paper does not prove the present finite-temperature memory-transfer theorem. Appendix A constructs shielding; Appendix B bounds the other sectors by one-clock Hamiltonians. The main text and Appendix A also display differing down-direction indicator formulas. Appendix B prints a local bound of 0.25U but subsequently uses a total bound of 0.075U. These numerical details require rechecking rather than uncritical reuse.

## 1. Why this comparator is stronger than generic SW

The full Hilbert space is resolved into invariant sectors; the ground-compatible sector is solved without perturbative truncation. Crucially, the other sectors are not thrown away. They have an explicit residual interaction structure suitable for a finite-temperature contour argument. This is an actual potential route to thermal implementation, not merely a better low-energy approximation.

However, 'exactly solvable' must not be promoted into 'all thermal sectors are independent clocks'. Equality defects undo the cancellation. At fixed positive temperature, their number is generally extensive. Keeping only M(0) is exactly the forbidden global-vacuum maneuver.

## 2. A full-temperature consequence of the residual structure

The following is our deduction, not a theorem claimed in the source.

Write the lifted ancillary Hamiltonian associated with an equality-defect set E as

    H(E)=sum_v h_v + 2J sum_{e in E} T_{e,v} T_{e,w},

up to fixed diagonal-code sector energies. There are no residual contacts on edges outside E. Therefore, on the lifted tensor-product clock space, H(E) factorizes into connected components C of the defect graph plus isolated clocks.

Suppose one has a local operator certificate on every component,

    H_C >= sum_{v in V(C)} h'_v,
    lambda_min(h'_v) >= E0 + delta,
    E0=lambda_min(h).

The one-site h'_v may depend on the incident occupied edges. Because trace exponential is monotone under Hermitian operator order (via eigenvalue monotonicity),

    Tr exp(-beta H_C)
      <= product_v Tr exp(-beta h'_v)
      <= d_clock^|V(C)| exp[-beta(E0+delta)|V(C)|].

Meanwhile z0=Tr exp(-beta h)>=exp(-beta E0), so the EXACT component activity obeys

    w(C)=Tr exp(-beta H_C)/z0^|V(C)|
        <= [d_clock exp(-beta delta)]^|V(C)|.

This bound includes every ancillary eigenstate. All unoccupied clock partition factors cancel exactly. No error proportional to total volume appears. Bounded-degree connected-component counting then gives the usual small-polymer criterion when beta*delta exceeds the entropy constant.

Caveats that must not disappear:

- The toric-code lifted lambda representation has a global redundancy/parity constraint; unrestricted tensor-product traces are not literally the physical sector trace. Those constraints must be restored, e.g. by projected traces, with a controlled comparison.
- Equality-defect patterns and original stabilizer syndromes can obey compatibility relations. A witness-erasure map must preserve or explicitly repair them.
- A global ratio Z(E)/Z(empty) alone is insufficient for event probabilities: summing unconstrained defects elsewhere loses an extensive entropy factor. The component representation is what permits cancellation against arbitrary distant defects.
- A Gibbs polymer bound is not a bath-lifetime theorem. Locality of encoded errors and the existing quantum dynamical crossing argument remain required.

This makes OY a particularly serious comparator when its architectural conditions hold: nonperturbative local positivity may replace the small-hopping expansion.

## 3. Precise route from a general bounded-weight CSS code

Here is a concrete attempted extension.

1. For every original data qubit q, create one copy for each incident Z check, with a bounded local tree of ZZ equality stabilizers identifying the copies. Retain a copy for a qubit with no Z incidence.
2. Group all designated copies belonging to a Z check into a single bounded-dimensional physical spin. Every original Z check is now onsite. Equality tree edges are native two-spin terms.
3. Replace each original X check by the product of X over ALL copies of each original qubit it touched. For each composite spin, its restriction is an onsite operator. A bounded clock walks through these restrictions.
4. All such clock-hop data operators are X type, so they commute. Furthermore, an X-check restriction inside a Z block commutes with its onsite Z check because the original CSS intersection is even.

This reproduces the important OY asymmetry: there is no X-versus-Z clock-hopping frustration. It has constant overhead, bounded-dimensional spins, and geometric locality under the stipulated bounded-incidence/local geometry. The repetition encoding is locally Clifford-equivalent to the original data plus gauge qubits, but its full thermal properties still must be compared rather than inferred from ground equivalence.

### The exact shielding bottleneck

For an equality link e joining two copies of q, controlled-prefix dressing gives

    U^dagger C_e U = C_e * product_{g: X_g contains q} f_{e,g}(m_g),

where f_{e,g}=+/-1 tracks whether the prefix has flipped precisely one endpoint. Each factor is a genuine nonconstant function unless the two endpoints can be acted on in the same onsite hop.

In the equality-good sector, canceling -J C_e therefore requires

    H_shield,e = +J product_{g:X_g contains q} f_{e,g}(m_g).

Its arity is the X-check incidence d_X(q), not the weight of the original Z check. Thus d_X(q)<=2 is a clean sufficient condition for native two-body shielding in this specific construction. Merely saying d_X is bounded does NOT suffice: a bounded three-body interaction is still not a native two-body interaction.

The actual deterministic incidence data now falsify this simple sufficient condition already at the two-level instance, rather than merely leaving it unverified. I read `root_actual_incidence.json`, reproduced by the parent's `root_actual_incidence.py`:

| Instance | X incidence counts | Z incidence counts |
|---|---|---|
| seed, n=5 | 1:4, 2:1 | 1:4, 2:1 |
| RX, n=60 | 1:16, 2:44 | 1:20, 2:8, 3:28, 4:4 |
| RX then RZ, n=1336 | 1:128, 2:400, 3:688, 4:120 | 1:104, 2:1056, 3:152, 4:24 |

The seed meets the incidence condition in either orientation; the 60-qubit instance meets it only when X checks are gadgeted. The 1336-qubit instance has maximum incidence four in BOTH orientations, so simply exchanging X and Z does not repair the issue. These facts rule out direct application of the particular two-clock shielding formula to this copying architecture. They do not rule out a different code splitting, grouping, or more general OY-inspired extension. Such a change would need its own native-resource and full-temperature proof.

### Why 'just enlarge the ancilla' is not yet a repair

Grouping all clocks entering one shielding term into a composite spin makes that term onsite. But neighboring shielding terms overlap. Taking the transitive closure can group a macroscopic connected component, violating bounded spin dimension. A uniformly bounded-component incidence graph would suffice; bounded degree alone does not.

Replicating clock labels introduces equality constraints. Since clocks hop coherently, exact equality-preserving hopping then acts on multiple copies, reintroducing many-body interactions. Finite penalties only recreate a thermal gadget problem. This is not a proof that every fixed-dimensional extension fails, but it closes the immediate regrouping/copying shortcut.

## 4. Why direct X/Z clock signs are not OY shielding potentials

For direct clocks on original data, consider two elementary hops with labels P and Q on shared data and PQ=-QP. Following the elementary square in the clock configuration graph gives

    P Q P^dagger Q^dagger = -I.

This is nontrivial discrete gauge curvature. Clock-diagonal changes of basis conjugate loop holonomies but cannot change a scalar -I into +I. Adding diagonal ancilla–ancilla contacts changes onsite potentials on that configuration graph, not its hopping holonomy. Hence OY's diagonal shielding does not cancel these signs.

Adding degrees of freedom independently to each clock, with a hop still acting only on that clock and its data qubit, does not fix the algebra: operators on distinct clocks commute, so the shared-data anticommutation remains. A compensating hop controlled by another clock generally acts on data plus two clocks (three physical spins). An ancilla-only offdiagonal contact changes a different transition matrix element; it is not termwise cancellation of the data-labeled hop. A more elaborate extension might work, but it needs a new construction and full-spectrum proof.

OY avoids this curvature obstruction rather than canceling it: all gadgeted data hops are commuting X type, and remaining interactions are diagonal equality potentials.

## 5. Local numerical audit

`check_oy_local.py` reconstructs the eight-dimensional h and all 15 nonempty incident-edge local certificates using the Appendix A direction functions and the Appendix B stated parameters U=1,t=.375,J=.09, redistribution .25 in the horizontal direction.

It gives:

    E0 = -1.2686388644527846
    min_a [lambda_min(h'_a)-E0] = 0.0249204642775418.

Thus the printed 0.25U local claim is not reproduced; even a literal 0.025U threshold is slightly above this minimum at the rounded stated parameters. A conservative smaller positive constant appears viable. This calculation is a finite-matrix check, not a rigorous interval certificate and not a thermodynamic theorem. It is preserved to prevent accidental propagation of the printed number. The qualitative local-certificate mechanism survives.

## 6. Reconciled decision

For CSS families with the required one-sided grouping/incidence, OY plus a full-temperature defect-component argument may be stronger than a perturbative flux expansion and should be preferred if its physical resource constraints are met.

For the present general bounded-degree CSS family, the direct clock-loop mechanism remains more general: native two-body terms are immediate, with exact full-space dressing, but it retains genuine ancillary hopping frustration. OY cannot presently remove that frustration at the same resources. The open thermal step remains a local free-energy expansion or other uniform witness-ratio theorem for those signed ancillary models.

## Appendix: targeted additional primary priors

### Hutter–Pedrocchi–Wootton–Loss (2014)

[Effective quantum memory Hamiltonian from local two-body interactions, PRA 90, 012321; arXiv:1209.5289v3](https://arxiv.org/html/1209.5289), Sections IV–VI and Appendix B:

- Already earned: a bounded-spin, local two-body microscopic proposal combining five-spin perturbative gadgets with a three-dimensional Heisenberg ferromagnet; an effective magnon-mediated memory mechanism. This is stronger implementation prior than merely noting generic gadget universality.
- Their displayed scaling uses h_z proportional to L^(-4) and ferromagnet side Lambda proportional to L^3. Thus one coupling is size-tuned and the mediating spin count scales as L^9.
- Their noise discussion assumes ground-state mediators and adiabatic errors, gamma(-A)<<A. It does not establish the requested full-spectrum microscopic Davies lifetime bound.
- Local ferromagnet backaction motivates periodic refresh on timescale JS/A^2. They also discuss a no-refresh longitudinal alternative with expected polynomial memory scaling; the size-tuned field remains.
- Appendix B explicitly leaves rigorous convergence outside its scope. Exactness within the harmonic approximation is not exactness of the bounded-spin microscopic model.

### Landon-Cardinal–Yoshida–Poulin–Preskill (2015)

[Perturbative instability of quantum memory based on effective long-range interactions, PRA 91, 032303](https://preskill.caltech.edu/pubs/preskill-2015-instability.pdf), Sections V–VII:

The paper analyzes the vulnerability of infrared-divergent anyon chemical potentials to small perturbations that gap the mediator. It also discusses why symmetry-protected Goldstone modes constrain the allowed coupling, and why a localized excitation in a bounded-range, bounded-norm spin Hamiltonian has bounded creation cost. It does not prove a general impossibility theorem for three-dimensional self-correction or for all two-body implementations. Its critique specifically distinguishes stable microscopic physics from an attractive low-energy long-range effective description.

### Same-resource conclusion and vulnerability check (our assessment)

Verdict: substantial prior implementation capability, but not the requested fixed-ratio, full-spectrum passive guarantee. Neither the large overhead nor the optional refresh should be misrepresented as a universal no-go.

Small bath rates alone cannot substitute for a full thermal-spectrum proof: reducing a Davies coupling rescales waiting times without eliminating the corresponding excited-sector Gibbs weights. An adiabatically adjusted effective excitation and a microscopic local jump must not be silently identified.

The clock route is not based on an infrared-divergent cost for one local excitation; it seeks a collective logical barrier already present in the target code. Therefore the specific mass-generation critique does not directly refute it. Its analogous vulnerability is nevertheless real: generic microscopic perturbations break the exact dressed stabilizer algebra. Transferring the earned weakly noncommuting thermal-memory region through real ancillary excitations still requires proof. The exact algebra receipt proves neither robustness nor passive finite-temperature lifetime.
