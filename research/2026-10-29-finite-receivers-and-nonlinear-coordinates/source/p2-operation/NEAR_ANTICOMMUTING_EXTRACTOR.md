# A finite causal extractor stable under near anticommutation

Author `producer-workspace/causal_algebra`, 29 October 2026 Australia/Brisbane. New construction; independent review pending at creation. The exact algebra theorem and its actual reviews remain unchanged. This proof independently derives the robustness extension of the explicit finite-query extractor in `../extractor_circuit/FINITE_QUBIT_EXTRACTOR.md`.

## 1. Consequence and interface

Exact rational Weyl commutation is unnecessary for a finite-error causal receiver. One can use controlled queries to the **actual** source-relative unitaries U,V, provided

    ||UV+VU|| <= eta.                                      (R1)

The construction never substitutes nearby rational Weyl operators for U,V. They may act on any separable Hilbert space, and all bounds are operator bounds valid for arbitrary input/reference states, without a field-energy restriction.

The receiver requires supplied controlled-U and controlled-V operations, fresh finite-dimensional registers, specified finite state preparation and Fourier gates, measurements, and record-controlled qubit rotations. Controlled access is an additional physical interface; ordinary unknown black-box access to U,V is not asserted to supply it. Errors in implementing these queried operations must be charged separately. During extraction the captured field is still available; only afterward is it retired.

After two such arrivals, one extracted qubit from the first is retained and paired with the second in a standard Bell measurement. All phase-estimation and Bell outcomes are retained. The source receives only record-dependent diagonal feedback, deferred until permitted by the actual interaction schedule. No new source-to-field coupling is used.

### Theorem

Let M>=2, K=M-2, and

    r=2 sin(pi/(2M)).

There is a source-independent isometry R from the arriving field to two M-valued phase registers, one extracted qubit and a residual field, with record-dependent phases alpha,beta, such that

    ||R U - exp(i alpha) X R|| <= delta_U,
    ||R V - exp(i beta) Z R|| <= delta_V,

where

    delta_U = r + (6K+1+1/sqrt(2)) eta,
    delta_V = r/sqrt(2) + 2K eta.                         (R2)

The Paulis act on the extracted qubit; the phases are diagonal on the actual phase records. Therefore every binary ordered source word U^x V^y satisfies

    ||R U^x V^y-exp[i(x alpha+y beta)] X^x Z^y R||
      <= delta_U+delta_V
       = r(1+1/sqrt(2))+(8K+1+1/sqrt(2))eta.             (R3)

For two arrivals with respective defects eta_1,eta_2 and the same M, the complete corrected source/reference/**all actual records** half-trace error relative to the same receiver on the common input is at most

    min(1, 2r(1+1/sqrt(2))
              +(8K+1+1/sqrt(2))(eta_1+eta_2)).           (R4)

The original arrivals can be correlated with one another, with the source and with its reference. The desired diagonal source target G_S and any source cocycle must be retained in the acquired dilation. The result is a sufficient operation bound, not an optimum.

For a common defect allowance eta, the two-arrival sufficient bound has scaling O(1/M+M eta). Selecting M of order eta^(-1/2) gives an O(sqrt(eta)) sufficient error. Increasing the phase register indefinitely at fixed nonzero defect does not improve this certificate: repeated queries also accumulate noncentrality. This is a limitation of the stated construction and bound, not a necessary physical error floor.

## 2. Finite sine-window phase estimation

Prepare an M-dimensional phase register in

    sum_(k=0)^(M-2) a_k |k>,
    a_k=sqrt(2/M) sin(pi(k+1)/M), a_(M-1)=0.

For a unitary C, query sum_k |k><k| tensor C^k and apply the inverse M-point Fourier transform. The resulting isometry is

    F_C=sum_(j=0)^(M-1) |j> tensor K_j(C),
    K_j(C)=M^(-1/2) sum_(k=0)^(M-2) a_k exp(-2pi i jk/M) C^k.

The register output phase is phi_j=2pi j/M. Normalization follows from Fourier orthogonality and sum a_k^2=1. The adjacent-window identity is

    sum_(k=0)^(M-3) a_k a_(k+1)=cos(pi/M).

The last zero amplitude prevents a Fourier wrap contribution. Direct summation gives the **operator identity**

    sum_j K_j(C)* (C-exp(i phi_j)I)*
             (C-exp(i phi_j)I) K_j(C) = r^2 I.          (R5)

Thus phase estimation does not need a favorable input spectral distribution. It estimates only C's phase for this bounded residual objective; it does not produce a uniform small error in a sharp continuous phase POVM.

For any unitary A, telescoping powers gives

    ||[C^k,A]|| <= k ||[C,A]||.

Working before the register Fourier transform, the k components are orthogonal, so

    ||F_C A-(I tensor A)F_C||
       <= K ||[C,A]||.                                  (R6)

The root-mean-square k can replace K, but the stated result uses the simpler maximum; no improvement is needed for the separation below.

## 3. The actual sequential phase-estimation order

Set

    F = F_(V^2) F_(U^2),
    F=sum_(j,k) |j,k> tensor K_k(V^2)K_j(U^2).

The order must not be exchanged. Define alpha_j=phi_j/2, beta_k=phi_k/2, and, on the output record fibers,

    A=exp(-i alpha_j)U, B=exp(-i beta_k)V.

Let E=UV+VU. The exact identities

    [U^2,V]=U E-E U,
    [V^2,U]=V E-E V

imply norms at most 2eta. Also ||[U^2,V^2]||<=4eta. Equation (R6) therefore gives

    ||F U-U F|| <= 2K eta,
    ||F V-V F|| <= 2K eta.                               (R7)

Here and below U,V on an output space mean their identity extensions. The U phase register commutes with the later V^2 phase-estimation stage. Move U^2 through that later stage using (R6) and ||[U^2,V^2]||<=4eta, then use (R5) for the earlier stage. This yields

    ||(A^2-I)F|| <= r+4K eta.                            (R8)

The V^2 phase estimate occurs last, so its uniform isometric residual applies directly to the earlier output:

    ||(B^2-I)F|| <= r.                                  (R9)

Neither statement is a pointwise bound after conditioning on a rare phase outcome. They are operator bounds for the full isometry, which is the right object for an unconditioned complete-instrument guarantee.

## 4. Explicit qubit extraction and near-Pauli intertwining

For each actual phase record put P_+=(I+B)/2 and P_-=(I-B)/2, and define

    W = |0> tensor P_+ + |1> tensor A P_-.

Because A,B are unitary,

    W*W=P_+*P_+ + P_-*P_-=I.

The P_+ and P_- need not be projections. The physical circuit prepares |0>, applies H, controlled-B, H, and controlled-A with control |1>. The known record phases in controlled-A and controlled-B are qubit phases. Thus W is always an exact isometry under the supplied queried gates; no nonexistent exact involution is assumed.

For E_hat=AB+BA, ||E_hat||<=eta, direct block multiplication gives

    W A-XW = [ E_hat/2 ; -A E_hat/2 ]
                   + [ 0 ; (A^2-I)P_+ ],               (R10)
    W B-ZW = [ (B^2-I)/2 ; -A(B^2-I)/2 ].              (R11)

The first vector in (R10) has norm at most eta/sqrt(2). Since

    ||[A^2,P_+]|| = ||[A^2,B]/2|| <= eta,

equation (R8) gives

    ||(A^2-I)P_+F|| <= r+4K eta+eta.

Equation (R11) and (R9) give r/sqrt(2). Finally set R=WF and move the actual input U or V through F using (R7). This proves exactly the two bounds (R2).

For the ordered word UV, use

    RUV-U_tilde V_tilde R
       =(RU-U_tilde R)V+U_tilde(RV-V_tilde R),

with U_tilde=exp(i alpha)X and V_tilde=exp(i beta)Z. These are unitary on the output register/qubit space, proving (R3). Input U,V and output X,Z are not interchanged without this error accounting.

## 5. Complete two-arrival correction

Take the acquired branch family

    (U_1^x V_1^y) tensor (U_2^x V_2^y), x,y in {0,1},

with any known source-only cocycle included in G_S. Apply the two extraction isometries. Their comparison branch acts as X_1^x Z_1^y tensor X_2^x Z_2^y, multiplied by the two phase-register factors. The two global Pauli generators commute. A standard Bell measurement returns their two binary eigenphases; local source phase feedback cancels these and the phase-estimation records.

The ideal comparison branch is therefore exactly erased by the **same actual receiver and record interface**. The tensor-product isometry comparison has norm error at most the sum of the two bounds (R3), uniformly on arbitrary joint inputs, including initially entangled arrivals. The controlled source is a direct sum over branches, so the largest branch bound also bounds the controlled isometry difference. Pure-state half trace distance is at most this norm difference; purification and a common output channel give (R4).

The phase registers may be measured before the record-dependent W gates. Keeping them coherently in the proof is a common Stinespring dilation of that actual measured-and-fed-forward circuit. Dephasing them at the end is the same common channel at both comparison endpoints. No additional unrecorded fine measurement is presumed.

At the inter-arrival cut the original field and all phase-estimation quantum registers have been retired; only the extracted qubit remains coherent. The receiver retains its actual two M-valued outcomes classically. All transient quantum paths used during extraction still count toward live workspace and processing time.

## 6. A strict separation with nonzero algebra defect

The earlier actual-operation lower bound applies to every purely classical receiver across the cut:

    epsilon_classical >= ||[U,V]||/16.

Assumption (R1) gives ||[U,V]||>=2-eta by the triangle inequality, so

    epsilon_classical >= (2-eta)/16.                    (R12)

This comparison allows arbitrary non-Gaussian receiver processing and classical adaptation, but the same phase-feedback, no-extra-source-coupling and arbitrary correlated-input contract. It is not a bound for a promise of one known vacuum state.

Choose M=128, K=126, eta_1,eta_2<=1/100000. Using sin x<=x, pi<22/7 and 1/sqrt(2)<5/7, (R4) gives the strict rational upper allowance

    epsilon_quantum < 2*(12/7)*(22/(7*128))
                         +2*(8*126+12/7)/100000
                    = 33/392 + 1767/87500
                    < 0.10438.

Meanwhile every purely classical receiver has

    epsilon_classical >= (2-1/100000)/16 > 0.124999.

This is a nonzero-defect separation of actual instrument performance under the declared interfaces. It does not require an exact rational commutation phase.

An explicit finite rational witness is U=cZ+i sI and V=X, with t=1/400000, c=(1-t^2)/(1+t^2) and s=2t/(1+t^2). Both are exactly unitary, UV+VU=2i sX has norm 2s<1/100000, and U^2 does not commute with V. The executable checks these statements in exact rational complex arithmetic. The witness tests a genuinely noncentral square, although the theorem also permits both squares to be noncentral and permits infinite-dimensional inputs.

For an actual Weyl pair UV=exp(i chi)VU,

    eta=|exp(i chi)+1|=2|sin((chi-pi)/2)|.

An irrational chi/(2pi) can therefore satisfy the same finite-error construction. Exact finite-dimensional classicalization remains impossible there; the finite-error statement is compatible with that earlier exact obstruction. This works because the commutator phase is close, even though the Weyl operators themselves need not be close in unrestricted operator norm.

## 7. Query, energy, timing and reuse accounting

For M=2^m, each phase register has m qubits and yields m actual classical bits. The two arrivals plus Bell result yield 4m+2 bits, equal to 30 at M=128. These are all the actual measurement outcomes in the declared circuit.

The controlled-power preparation can be implemented with K calls to controlled-U^2 and K to controlled-V^2: on step r=1,...,K, apply the square controlled by the reversible register predicate k>=r. Resolving each square into two primitive controlled calls costs 4K queries per arrival. W adds one controlled-U and one controlled-V. Thus this predicate implementation costs 4K+2 primitive calls per arrival, 8K+4=1012 for the two-arrival example. Predicate computation and uncomputation require additional finite gates and, in a chosen implementation, temporary workspace. This differs from the ordinary binary-power schedule in the exact-extractor package, whose actual query count is 8M-4=1020; that schedule also implements the present theorem and avoids a predicate-cost claim. The two counts refer to different schedules, not to different error bounds. Efficient controlled-power hardware may change wall time; it must not erase the cost of synthesizing those powers.

This construction replaces an unspecified exact subsystem extraction by a finite circuit of specified queries. It still needs coherent controlled access to the acquired relative unitaries, their phase reference, field capture during the queries, fresh sine-window registers, readout, a retained qubit with sufficient lifetime, and source coherence until feedback. The exact-extractor package gives a deterministic finite sine-state preparation and a complete binary-schedule finite-gate ledger; both are valid here without an exact algebra promise. Ancilla-state and finite qubit-gate errors are separate complete-channel allowances; they add by ordinary contraction/telescoping. If the actual implemented receiver differs from the specified ideal circuit by an allowance eta_R on every admitted comparison input, comparison to the SAME implemented receiver's common-input baseline generally costs 2 eta_R, one endpoint per replacement. A single eta_R is justified only if the baseline remains the specified ideal receiver. Errors in actual field displacements can require energy bounds even though the ideal query analysis does not.

Repeated U/V powers can move field energy. The finite dimension of the retained qubit is not a bound on intermediate energy, pump work, query duration, mode loss or memory decay. For Weyl displacements, those costs must be computed from the actual strengths and query schedule before making a hardware claim. The fully informed classical comparator is allowed the same query primitives and temporary processing resources; it may not retain an uncounted coherent system across the designated cut.

No exact algebra acquisition, low-loss controlled displacement, or scalable workload has been demonstrated by the operator theorem. The established advance is a concrete finite-query, finite-record receiver whose operation guarantee survives a nonzero commutation defect and crosses a rigorous classical-memory error floor at its supplied interface.

## 8. Evidence and ancestry

`robust_extractor_checks.py/json` supplies eight exact rational-complex cases of the extraction and commutator identities, the exact rational noncentral witness and separation arithmetic, finite floating diagnostics for the actual ordered phase instrument through M=128, and a direct 1024-branch two-arrival Bell/feedback audit at M=4. The floating diagnostics are not outward-rounded error enclosures. The unrestricted-input guarantee follows from the displayed operator proof, not a finite matrix truncation.

The proof uses the exact-extractor package's finite sine instrument and controlled-copy/flip circuit, which in turn records the primary sine-state and SWAP-isometry ancestry. The actual-operation lower bound is the separately reviewed `../causal_algebra/ACTUAL_OPERATION_MEMORY_SEPARATION.md`. Its reviewed assumptions are retained here. The new step is to control the actual noncentral measurement order and extraction defects directly, avoiding a false approximation of irrational Weyl operators by norm-close rational operators. No additional external theorem or hardware result is imported by this robustness extension.
