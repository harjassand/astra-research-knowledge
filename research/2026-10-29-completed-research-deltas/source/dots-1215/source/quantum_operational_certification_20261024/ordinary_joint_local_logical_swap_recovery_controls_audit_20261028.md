# Independent controls and global-service review: joint local logical SWAP recovery

28 October 2026. **PASS under the stated common-algebra, calibrated-margin, reset and paid-control contracts.** Global noisy-source oracle comparison additionally requires the separate global operator-dominance promise. This review is mathematical only: zero new source calls, zero new simulations, no private pilot data, and no modification of the received one-logical sources or earlier pilots.

## 1. What the local acquisition does and does not supply

The training input for logical i is an ordinary Pauli eigenstate on i and maximally mixed states on the other q-1 logical inputs. The latter are real preparations using independent private bits; the estimator does not condition on those bits or the individual anchor labels. Its unconditioned physical state is exactly the displayed four-state bank, with common marginal

    rho=U[I_(2^q)/2^q tensor Gbar]U†.

The other logical registers can be included in the proof gauge. Grouping global Pauli errors by their action on i gives the required one-logical Pauli/gauge representation without learning or enumerating its exponentially many global components.

For local acquisition one uses only the calibrated X_i/Z_i margins and exact common local algebra. The source's all-encoder marginal oracle assumptions are not needed or inferred. The received local ERM/tournament proof establishes ell0_i<=eta while every returned D_i remains an exact CPTP map. It does **not** establish that directly applying these maps sequentially would preserve the other logical qubits. The manuscript correctly avoids that invalid composition.

The local constants independently check. With m=kappa^2 eta/256, zeta_ERM<=m, the ERM bound gives r_min<=22kappa eta/256. The balanced bracket with t=kappa eta/(4h^2) yields

    r_selected <= (44/256+1/4)kappa eta
               = (27/64)kappa eta < kappa eta/2,
    ell0_i <= (27/32)eta < eta.

The single-candidate case simply skips the bracket and is stronger. Different logical indices consume separately charged calls; they are not independent experiments obtained for free from one input. Within a color, the already received disjoint-patch marginal-bank law remains valid even when true supports of different logical qubits overlap.

## 2. Weighted sign rounding needs no hidden spectral gap

For the one-logical channel D_i E0_i, Pauli twirling is a proof identity: its diagonal transfer coefficients obey 1-t_jj<=2ell0_i. The actual pullback A_j=D_i†sigma_j is a Hermitian contraction. Since rho commutes with the true logical reflection B_j,

    Tr rho(A_j-B_j)^2<=2(1-t_jj)<=4eta.

Now let C be a known Hermitian matrix within operator norm sqrt(eta)/2 of A_j. Diagonalize rho and B jointly, with eigenvalues r_k>=0 and b_k=+/-1, and diagonalize C with eigenvalues c_l. In these bases,

    Tr rho(B-sign C)^2
      =4 sum_(b_k opposite sign(c_l)) r_k |<k|l>|^2.

Every indicated term has |b_k-c_l|>=1, including arbitrary sign choices for c_l=0. Therefore this sum is bounded by 4Tr rho(B-C)^2. This proof does not assume [rho,C]=0, a gap at zero, or a lower bound on a nonzero gauge weight.

The weighted Hilbert-Schmidt triangle inequality gives

    Tr rho(B-sign C)^2
      <=4(2sqrt(eta)+sqrt(eta)/2)^2=25eta.

The implemented reflection is the exact sign of a certified nearby known matrix, represented by an exactly unitary reference diagonalization and signed labels. Finite universal-gate approximation belongs to the linked implementation budget. The proof does not declare floating eigenvectors exact or infer exact anticommutation/cross-commutation of learned reflections.

## 3. Exact control order and why mixed ancillas are essential

Let C_Z(B) be the logical-to-ancilla CNOT formed from the two spectral projectors of a Hermitian reflection B, and C_X(B) the ancilla-to-logical controlled B. Each is unitary for every reflection. The chronological product

    C_Z(B'_Zi), C_X(B'_Xi), C_Z(B'_Zi)

is thus unitary even for learned reflections that do not anticommute or commute across indices. For the true pair it is the standard three-CNOT SWAP between encoded logical i and ancilla A_i. Actual overlapping supports are executed in a fixed sequence; no disjointness or learned compatibility is smuggled in.

A controlled B'_Z plus an ancilla Hadamard before and after realizes each C_Z. Two such gates and the middle controlled B'_X therefore cost three controlled local reflections and four ancilla Hadamards per logical index. All q distinct output ancillas must be present; one reusable ancilla cannot substitute for the q-qubit recovered block.

Preparing each ancilla in I/2 is a real paid operation: reset, one private fair bit, and at most one conditional X, then discard the preparation record. Pure reset ancillas would not give the invariant marginal used below and cannot be substituted without a different proof. Receiver-local purifications are mathematical devices, not protected references sent through the unknown source.

## 4. Full-reference hybrid proof, including overlapping patches

For global entanglement fidelity, retain the entire q-qubit Bell reference R in the mathematical proof. Purify Gbar on E and every receiver mixed ancilla on a local S_i. The reduced state of the physical register P and all ancillas is

    rho_PA=(U tensor I_A)[I_(L,A)/2^(2q) tensor Gbar](U† tensor I_A).

Every **ideal elementary** CNOT acts only on L,A and identically on the gauge, hence leaves rho_PA exactly invariant. This is stronger than invariance only after a whole SWAP and is precisely what is needed for the hybrid argument. It is not asserted for an actual approximate prefix, an arbitrary payload marginal, or a state conditioned on the discarded coins.

For each Z gate the difference operator is (B'_Z-B_Z) tensor (I-X_A)/2; for the X gate it is (B'_X-B_X) tensor |1><1|_A. On the invariant rho_PA, their squared state-vector errors are delta_Z/2, delta_X/2 and delta_Z/2. This evaluation depends only on the reduced P,A state, so all purifying references remain intact throughout.

Expand the difference between complete actual and ideal products with ideal gates before each error and actual gates after it. The actual suffix is unitary, preserving each error norm. Cauchy-Schwarz over the 3q terms gives

    ||psi_actual-psi_ideal||^2
      <=3q sum_i(delta_Zi+delta_Xi/2)
      <=(225/2)q^2 eta.

The ideal final state has the full Bell pair |Phi>_(R,A) as a tensor factor. Its orthogonal-complement probability in the actual state is no greater than the squared vector difference. Tracing P,E,S therefore proves the stated **joint** Bell-loss bound. It preserves entanglement across the logical inputs and with the full reference in this fidelity sense; it is not a product of marginal-fidelity statements. The q^2 amplification is explicitly paid rather than removed by an unjustified independence assumption.

## 5. Global oracle transfer is a separate hypothesis

For a full q-logical decoder, the global Bell-basis probabilities define a gauge POVM T_alpha. The noisy-source success is sum_alpha Tr G_alpha T_alpha. Only under the separate condition G_I>=G_alpha for every global Pauli error and encoder is the common identity logical decoder globally optimal. Then

    ell(D E_x)-ell_star(x)
      <=Tr G(x)(I-T_I)<=4Tr Gbar(I-T_I)=4ell0_joint.

The factor four comes from the fixed four-real-coordinate encoder, not from q or the number of global Pauli labels. The learner need not enumerate the 4^q proof labels.

The retained q=4 counterexample is valid: probabilities .1 for I, .3 for XXXX and .15 for each of the four single-X errors sum to one, give each local X contraction 1 and Z contraction .1, yet make correcting XXXX better than identity. Thus calibrated local positivity cannot replace global operator dominance. All-Pauli positivity is a sufficient stronger condition by Pauli Fourier inversion, but is not supplied by the local observations.

With eta=epsilon/(16384q^2), the uniform global decoder regret is at most 450epsilon/16384<epsilon/20. Without global dominance the coherent extraction bound relative to E0 survives, but the unrestricted noisy-source oracle claim does not.

## 6. The encoder test is genuinely global and ordinary

The frozen joint decoder is tested using C|0^q> for a fresh uniform known q-qubit Clifford C, followed by C† on the recovered output and one joint all-zero event. Input entanglement is confined within the q logical inputs. There is no retained source reference, inverse source, or inferred global result from q independent marginal tests.

Uniform stabilizer states are a projective two-design: Pauli signs kill distinct cross moments, Clifford transitivity equalizes nonidentity diagonal moments, and purity gives their common value 1/(d+1), d=2^q. This yields E[rho tensor rho]=(I+Swap)/(d(d+1)). Consequently for any TP channel,

    e_D(x)=[d/(d+1)]ell(D E_x).

The normalization is not exponentially small and preserves the nonnegative ten-feature quadratic in x. The source's four-real-coordinate encoder dimension has not silently grown with q. The displayed active-design tolerance/cap therefore gives the claimed Bell-risk error using actual global Bernoulli outcomes.

The symplectic-basis sampler must choose each next vector in the preceding pairs' symplectic orthogonal complement and its partner from the product-one affine hyperplane. The revised manuscript explicitly does so, samples partners directly, and caps nonzero-vector rejections into the global randomness discrepancy. Finite Clifford compilation, the inverse output circuit, q readouts, and routing are paid. Product-only logical input/readout access does not supply this test; the note correctly excludes that weaker contract from the global fast-encoder claim.

## 7. Ancilla routing, complete cost, and service boundary

A concrete finite line implementation puts all q labeled ancillas in an end block. For each logical index, route its ancilla beside its learned width-w patch, execute all three controls, then reverse the routing permutation. This restores the original physical-register positions and all earlier output positions, even when the route passed across them. At most 2(n+q) routing SWAPs per index suffice. The recovered outputs end in a contiguous block, supporting a paid local compiler for the global inverse-Clifford test. This is an explicit O(q(n+q)) cost, not free adjacent ancillas.

Each joint invocation retains n+q data qubits, uses q mixed preparations, 3q controlled local reflections and 4q Hadamards, plus finite generic synthesis and routing. The joint decoder is used for the encoder-training calls and final payload, not falsely charged as the receiver for every local-estimation shot. Each source block call carries q logical input qubits and emits n physical outputs; the note separately charges these qubit exposures and selector/control registers. Collective Bures bank workspace and cross-copy routing remain much larger possible costs and are not hidden inside the q decoder ancillas.

The complete source cap includes all q local modules, their failures, the global encoder learner, and one payload call. The statistical allocation and linked complete-operational discrepancy cover the whole process. The one-logical references and pilots remain unchanged.

Finally, joint Bell loss is not a dimension-free untwirled diamond guarantee. The displayed conservative bound min(2,2*2^q*sqrt(ell)) is valid. The optional private-key whole-logical Pauli twirl changes the averaged service: it preserves Bell loss and makes the possibly correlated Pauli channel's unhalved diamond error exactly 2ell. Its 2q-bit key, input/output Pauli gates, coordination and key discard are paid. No statement is made for each exposed or key-conditioned channel. The equally informed conventional learner receives this entire construction; no comparative advantage or generic fault-tolerant coding claim follows.

## Final status

All requested physical, sign-rounding, composition, global-validation and resource checks pass on the bound manuscript. No new simulations or source calls were used. There is no unresolved objection under the explicit structural/access contract; stronger source violations, product-only global validation and improved q scaling remain outside this receipt.
