# Governing implementation result: the untouched source has K≤15

2026-11-02. This is the strongest same-resource baseline established by the completed finite-star audit. It supersedes comparing the optional K13 re-encoding only to the older conservative K180 certificate.

## 1. Actual unchanged Hamiltonian and incidence

The declared intrinsic-page, skeleton-first atlas has Q_v=Σ_(e∋v) dim F_e≤13 at every actual abstract vertex, counting distinct coincident germs separately. Exterior vertices have Q_v≤12; all 252 exceptional-star cases are compiled. Twice-covered face restrictions give dim F_v≤6. Consequently every **existing** X generator, in its existing vertex and edge bases, has weight≤13 and each data qubit belongs to at most12 X checks.

The original physical edge bases have dimension at most3, and every actual face has at most5 boundary edges. Hence the existing Z generators have weight≤15, in ANY such edge basis. Each edge has at most4 incident faces, so q_Z≤4. Thus the **original Hamiltonian without any change of basis or generator** has

    K_a=max(3,w_a)≤15,    q_X+q_Z≤16.

The common check-overlap bound is D≤196, not merely226. An X check has at most13 support qubits and hence at most13(16−1) other neighbors. A Z face check can meet X checks only at its at most5 vertices (≤6 each, thus30), and other Z checks only at its at most5 edges (≤3 others per edge, thus15); including itself its overlap is at most46.

Equivalently, use edge-block overlap: each physical edge block supports at most12 vertex checks and4 face checks; each X check uses at most13 edge blocks, and each Z check uses at most5. Therefore the edge-block overlap graph has D_block≤196. This enlarged graph is invariant under any invertible basis change separately inside the edge blocks.

No source Gibbs transfer theorem is needed for K15: the complete source Hamiltonian, all syndrome labels, Gibbs law at every beta, actual checks, physical data bases, decoder, full charged traces, distance and filling are literally unchanged. The new implementation recompiles these actual checks with smaller native clocks; its finite-temperature theorem must still be applied to that actual new native Hamiltonian, not inferred by a ground-space argument.

## 2. Same physical resources, honest comparator

There is one clock site per actual check, just as before. Largest clock dimension is15, with no new data qubits or spatial dimension. The two-body native compiler is applied directly to the unchanged single-qubit Pauli factors; no multi-data-qubit native interaction is introduced.

At fixed effective source coefficient J in −J S (violation energy2J) and fixed eta,

    t_peak=J M³/(2 eta²),       M=max K_a.

Against the older sufficient M=180 padding, M=15 reduces this coefficient certificate by (15/180)³=1/1728. This is a correction of an unnecessarily costly certified design, NOT a lower bound on what an optimized old device needed. The strongest newly available baseline is15.

The optional globally shared parity-path edge basis has M≤13 and gives exact termwise local-Clifford source Gibbs conjugacy, but its additional peak-coefficient improvement against15 is only (13/15)³≈0.650963. Its data faults acquire at most three old-frame qubits per new physical qubit. It is therefore an optional dimension/noise tradeoff, not an automatically superior generic-noise design.

## 3. Exact prefix dictionary: no repeated light-cone explosion

Consider one microscopic unwanted term V of norm v, supported on d data qubits, c clock sites and b bath sites, with bath local dimension≤d_B. Use M as a uniform clock-dimension bound and the edge-block overlap graph above. Expand V first into data Paulis and clock/bath matrix units. There are at most

    4^d M^(2c) d_B^(2b)

coefficients, each of absolute value at most v. This is an intentionally simple operator-norm-to-dictionary bound, not an optimized basis norm.

The exact native gauge is U=Σ_q |q><q|⊗W(q), where W(q) is the ordered product of the check prefixes F_a(q_a). For a clock matrix unit changing only clocks C, |C|≤c, its dressed data factor is

    W(q')† E W(q).

Cancel the unchanged prefixes by Pauli commutation. Up to a modulus-one scalar, the remaining data word is E times F_a(q'_a)F_a(q_a) for a∈C. Each such difference is an interval of the single-check Pauli factors, supported on at most M qubits. Thus the K15 route has

    b_D ≤ d+15c.

Dependence on unchanged clock labels is only a diagonal phase on checks touching E or neighboring a changed clock. There is **no iterative propagation** from those diagonal controls: diagonal clock functions commute with every prefix gauge. The number of additional clock coordinates is at most16d+195c. Expanding those diagonal phases into diagonal matrix units multiplies coefficient l1 norm by at most M^(16d+195c). Therefore a fully explicit safe dictionary bound for the unchanged K15 route is

    v_dict ≤ C_dict v,
    C_dict = 4^d 15^(16d+197c) d_B^(2b).

All data-touch checks, explicitly acted-on clocks, and changed-check neighbors are already in the same enlarged set. Hence owned-column and one-neighborhood contact bounds are

    b_c ≤16d+196c,       d_c ≤196 b_c.

Actual data/bath supports are still marked when defining used-label components. These bounds retain every noncommuting insertion and all thermal clock sectors; they do not project clocks to their ground band.

For the optional K13 route, the same edge-block graph and b_c,d_c bounds hold. Conjugating its data word into the old decoder frame changes no Pauli coefficient and gives b_D≤3d+39c. Its analogous crude C_dict replaces15 by13. A common conservative source envelope can use b_D=3d+39c for both designs; this permits a fair common-envelope bound, but does not prove that an independently optimized K13 tolerance beats an independently optimized K15 tolerance. Physical local-term overlap, bath range, density and the rooted label-count entropy must still be supplied as in the existing admission theorem.

## 4. Full finite-temperature clock admission

The companion DIRECT_K13_NATIVE_RESOURCE_LEDGER.md proves a uniform M≥3 tail/wrap check for the heterogeneous resonant choice

    t_a=J M² K_a/(2eta²),   g_a=eta t_a/M,
    Dbar eta²≤1/64, beta J≥1.

That derivation applies unchanged at M=15 and M=13; no false assumption that wrap margins are monotone when reducing M is used. The ordinary tail obeys beta delta_bar≤4exp(−3/(2eta²)), while the common multi-rod activity retains its beta J Dbar eta² dependence. All finite-temperature sectors are included.

The actual generic-perturbation criterion remains

    q_native≤M^(b_c) d_B^(b_B) exp(beta delta_bar b_c)
              [exp(beta v_dict)−1] ≤q_*,

with cold, event, charged-trace, filling and rooted-source entropy margins from the admitted theorem. The explicit support/dictionary formulas above close the finite locality gate; they do not calculate a useful absolute laboratory tolerance. No new Gibbs-preparation, noisy WRITE, autonomous equilibration or physical readout service is obtained.

## Status

Finite source geometry, original-basis K15/D196, and optional exact-Gibbs K13 passed independent internal audit. The native compiler is an already admitted all-fixed-K theorem; the uniform new-M thermal estimates and explicit dictionary ledger bind its input resources. No claim of north-star physical-memory completion or same-resource active-QEC advantage is made.
