# Actual native LOCC interface to the compressed-circuit canonical basin
2026-10-30. Structural verification for the root's new noncommuting-basin construction. This supplies actual locality/radius/common-Bell-module premises; it does not independently prove that abstract construction's boundary telescopes or the remaining useful-service candidates.

## 1. Define the OUTER projector using the actual relative syndrome

Let sigma_A,sigma_B be complete RAW stabilizer eigenvalues, and delta=sigma_A+sigma_B their relative CSS syndrome. In each CSS sector choose one fixed minimum-physical-weight representative R_delta of that syndrome, with deterministic tie breaking. Let r(delta) be the SUM of the two sector weights. This is a function of the raw relative syndrome, not of an unobserved Pauli trajectory or the absolute Alice syndrome.

Choose a fixed r0>0 strictly below the minimum of all admitted Tanner confinement/active-density radii, with an additional strict distance margin `2 r0 N+ell_max<d_N` for sufficiently large N. Define

    P0=1_(r(delta)<r0 N) tensor I_apparatus.

This projector does not itself distinguish correct versus incorrect logical Bell classes. Preservation of the initial correct common module is a separate edge statement below. In particular, no energy-only cutoff is substituted for this radius projector.

## 2. Commutation with the actual raw potential and discounts

U is a function of raw relative stabilizers. Every mechanical B is DATA-independent in the exact forest frame. Every false token compares a computational payload with current RAW Alice stabilizers, with the actual program-validity projector. Thus E and V commute P0.

Each A/C coefficient has only controller/tag/monitor off-diagonal entries. Its DATA dependence comes from diagonal raw-syndrome/program truth guards; the normalized decrement a_h is likewise a raw-stabilizer function. Consequently every actual discount C_h=I-t A_h^c a_h commutes P0. Hence V_c=V product C_h and its square roots/inverses commute P0 exactly. This is compatible with arbitrary absolute syndrome-gauge superposition, not a fixed measured Alice baseline.

## 3. Fixed local supports and actual energy bandwidth

All physical nominal terms and noise system legs are first put in the accepted exact forest frame. Its bounded-depth commuting ownership factors enlarge a local support by only a fixed amount. The raw V similarity sees only incident commuting energy terms. The credited C_h similarities likewise cancel all disjoint commuting factors. The debt and activity witnesses are finite local telescoping polynomials for the fixed raw conservative zero-Bob-LOAD generator; their support degree is chosen BEFORE lambda,t. The exposure witness is the FULL finite-cone physical polynomial and its finite pinching/DATA expectation extension, not the withdrawn private-pipe decoupling shortcut.

Thus every proof generator Xi and every actual dressed physical system leg has a fixed finite DATA/controller support independent of N,lambda,t at the chosen physical instance. Its arbitrary system operator can be expanded in a finite Pauli basis on DATA and matrix units on auxiliaries. Let ell_max bound the SUM of X- and Z-sector weights of the RELATIVE Pauli edge induced by any such term. Paired Alice/Bob supports are counted by their union, with at most a factor two for the CSS sum. Increase ell_max for the finite local cones used by the boundary proof if needed; it remains fixed. This is an algebraic expansion, not a stochastic Pauli law.

Because E is a bounded-incidence sum of commuting bounded local terms, each local Xi also has a fixed energy bandwidth K_X. This includes false-token comparisons and history weights, not just raw check count. Compressing Xi by P0 does not enlarge its energy-conjugated norm, since [P0,E]=0. Uniform local C_h inverse bounds for t<t0<1/2 give the corresponding fixed-theta V_c-weighted norm premise. No global condition number is used for a local leg.

## 4. BOTH sides of an actual radius crossing have high raw energy

For a relative Pauli f of CSS weight <=ell_max,

    |r(delta+sigma(f))-r(delta)|<=ell_max.             (1)

Indeed R_delta+f is a candidate for the new minimum, and the reverse inequality uses f again. This is true for minimum-syndrome representatives without requiring a stochastic history or a logical-class assumption.

Therefore every matrix element of a bounded-support operator crossing P0 has BOTH endpoint radii in

    [r0 N-ell_max, r0 N+ell_max].                     (2)

Choose N sufficiently large that the upper endpoint lies below the COMMON admitted confinement radius. Each canonical representative is in particular reduced modulo stabilizers, so the reviewed confinement theorem applies on both sides. With its common h>0,

    E>=U>=h(r0 N-ell_max)                            (3)

on the whole crossing strip. This supplies b=h r0 and a fixed O(1) loss. It is not an inference from small syndrome globally. One strip works for the union of the finitely many bounded support sizes; no extra N-dependent radius margin or noise-partner graph is introduced.

## 5. The actual common Bell module, not arbitrary joint logical identity

For each allowed raw relative syndrome delta and absolute syndrome s, consider

    (I tensor R_delta) Omega_s,

tensored with arbitrary controller/bath/reference vectors. Let M0 be their coherent span for r(delta)<r0 N. The accepted signed-Bell algebra and the final relative decoder map this entire span to the SAME pure encoded Bell target times an auxiliary state. This is the accepted target/gauge module, not an arbitrary-logical-input identity theorem on the enlarged joint two-party space.

For a bounded local Pauli P_A tensor P_B, the signed Bell relation moves Alice's Pauli to Bob, up to transpose phases and a shift of the absolute gauge syndrome. Its relative edge has mask f=P_A^T P_B (CSS-vector notation; phases are auxiliary). If both source and target radii lie in P0, then

    sigma(R_delta+f+R_delta')=0,
    |R_delta|+|f|+|R_delta'|<d_N.                      (4)

The difference is therefore a stabilizer, with any syndrome-dependent sign absorbed in the gauge/bath coefficient. Thus the compressed local leg P0 O P0 maps M0 INTO M0 for every local O, by its finite linear Pauli/matrix-unit expansion. No coefficient count multiplies an error probability; this is an exact common-span statement.

For self-adjoint proof Xi, the compressed P0 Xi P0 leaves M0 reducing inside P0. Its exponential, products, adjoints and functional calculus therefore preserve the same module. Raw E, discounts and V_c already preserve it by their syndrome/controller form. Hence the compressed proof circuit, its positive witness W0 and the INNER spectral projector P1 of W0 preserve the protected Bell-target/gauge module. Actual compressed Hamiltonian/reset/noise system legs preserve that module as well, with arbitrary retained bath coefficients.

This is the exact structural fact needed for the root's spectral kill. It should NOT be described as identity action on every arbitrary joint logical input: changing the absolute syndrome can produce matched signed-decoder logical actions that preserve the fixed Bell target without being identity on a general two-party logical state. The scope remains the common Bell-target channel, uniformly over allowed gauge/reference inputs.

## 6. Initialization and limits

Clean native engines I/W/P0, no own tags, empty channels, Alice workers IDLE and Bob masters FLUSH_SEND(0) give zero mechanical/semantic/activity debt. For the ideal Bell-target module with relative delta=0, U=0 and every current decrement a_h=0; all proof witnesses vanish on the initialized range and the initial dressed moment is exactly one. A source-error input needs its explicit small support/moment envelope in the same common module. Arbitrary initial classical contents from the older stochastic theorem are NOT imported into this small-moment premise.

The independently accepted native hardware/source restrictions remain: grouped finite-dimensional two-site H and onsite resolved resets, measured classical interparty transport, fixed finite capacities and clocks, declared raw Bell resource, ideal forest/relative encoded output. The root's new boundary/exit theorem and the repaired full-service composition require their own review before any continuous-noise lifetime promotion.
