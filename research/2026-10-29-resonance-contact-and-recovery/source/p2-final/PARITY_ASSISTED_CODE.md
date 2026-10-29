# A bath parity bit completes a diagonal-error syndrome

Author: `producer-workspace/code_alternative`, 29 October 2026 Australia/Brisbane. **Authored derivation; independent review is separate.** Frozen `p2_mediator` files are unchanged. This is a conditional storage/recovery construction, not a new parity-erasure claim or an acquired device.

## 1. Result and significance

For an odd-length X-repetition code, a data syndrome identifies a diagonal Pauli error up to its all-qubit complement. A known initial bath parity and an observed final bath parity distinguish those two possibilities. The corrected instrument then acts as the identity on the logical qubit tensored with a bath instrument, even for arbitrary logical/bath/reference correlations supported in the known initial parity sector.

The noise need not be weak, Markovian, Gaussian, linear in bosonic coordinates or approximately solved. The decisive property is a **complete conserved symmetry**, together with diagonal source evolution. Time-dependent noncommuting bounded-sine contacts fit this algebra when their bath operators are parity odd. One must acquire the full parity boundary; inaccessible photons and an unmeasured retained oscillator are not automatically included.

Photon-parity recovery of pure dephasing is established prior art: Zhao–Hedemann–Yu (2013), especially Section IV A, explicitly gives the one-qubit parity mechanism. The useful bridge here is its operator-valued syndrome completion and complete-boundary extension. Historical priority of that extension is unestablished. In particular n=1 already works, so the larger repetition code is not an automatic storage improvement.

## 2. Exact operator assumptions

Let B be an arbitrary Hilbert space with a self-adjoint unitary parity Pi. Write Q_p=(I+p Pi)/2 for p=+1 or -1. The n-qubit source undergoes

    U = sum_z |z><z| tensor U_z,
    Pi U_z Pi = U_(-z),                       (1)

where z ranges over {+1,-1}^n. Each U_z is a unitary on the **whole** bath boundary. Source diagonal phases included in this U are not exempt from the identity recovery target. Section 6 separately allows a prescribed code-preserving target factor G and proves its preservation.

The initial joint normal state may correlate the logical qubit, B and an untouched reference R, but has support in C tensor Q_p B tensor R, where

    C = span{|+>^n, |->^n}

and the initial parity p is known. A parity-invariant density operator is weaker than support in one known sector and is not sufficient by itself.

The supplied recovery measures the commuting source stabilizers X_j X_(j+1), j=1,...,n-1, measures final bath parity, and applies a source Z-string selected from those outcomes. The source syndrome measurement must be nondestructive on the logical code. Measuring each physical X and merely coarsening its outcomes destroys the logical state and does not implement this recovery.

## 3. Walsh decomposition and charge

For e in F_2^n, define z^e=product_i z_i^(e_i) and

    A_e = 2^(-n) sum_z z^e U_z.

Fourier inversion on the sign cube gives the exact finite operator identity

    U = sum_e Z^e tensor A_e.                (2)

No field truncation or expansion in interaction strength has been used. Applying (1), changing z to -z, and noting (-z)^e=(-1)^|e| z^e gives

    Pi A_e Pi = (-1)^|e| A_e,
    Q_q A_e Q_p = 0 unless q = p (-1)^|e|.   (3)

Let H be the (n-1)-by-n binary matrix whose jth row has ones in positions j,j+1. Error Z^e maps the code into syndrome H e. Its kernel is {0,1^n}. For odd n, e and e+1^n have opposite weight parity. Consequently the pair

    (s,t)=(H e, |e| mod 2)

determines e uniquely. The decoder is an explicit binary linear inverse of the square matrix with rows H followed by 1^n.

Let P_s be the source syndrome projector, J the code isometry and e=e(s,t). For q=p(-1)^t,

    (Z^e P_s tensor Q_q) U (J tensor Q_p)
       = J tensor A_e Q_p.                  (4)

Indeed P_s Z^f J vanishes unless Hf=s; (3) eliminates the remaining complementary error, and Z^e Z^e=I. Equation (4) is an operator identity on the entire logical/bath input sector, hence proves the instrument statement for every correlated normal input and every reference. Summing outcomes is trace preserving because it is a unitary followed by complete measurements and unitary feedback.

For a field measurement with Kraus operators M_(q,a)=M_(q,a) Q_q, where a is any finer record and all q,a branches form a complete instrument, the same identity is

    (Z^e P_s tensor M_(q,a)) U (J tensor Q_p)
       = J tensor M_(q,a) A_e Q_p.           (5)

Thus **all actual fine outcomes** can be retained, provided the measurement genuinely refines the final parity sectors. The comparison is id_L tensor a bath instrument. Existing logical/bath correlations can induce logical/record correlations through that common instrument; independent record probabilities are asserted only for independent logical and bath inputs.

This fine-record result is derived branchwise. It is not imported from Astra's coarse-teleportation identities, whose fine-record counterexamples remain valid.

## 4. A direct Hamiltonian interface beyond Weyl displacements

For bounded measurable self-adjoint controls, take

    H(t)=I tensor H_even(t) + sum_i Z_i tensor B_i(t)
         + sum_(even |v|) Z^v tensor C_v(t),

where Pi H_even Pi=H_even, Pi B_i Pi=-B_i, and Pi C_v Pi=C_v. All source factors commute with every Z_i. The bath operators may be mutually noncommuting and time dependent. Then H_z(t) satisfies Pi H_z(t) Pi=H_(-z)(t), and uniqueness of the propagator proves (1) with its full time ordering.

More generally, a term Z^v tensor C_v is allowed precisely when Pi C_v Pi=(-1)^|v| C_v. For an unbounded bath Hamiltonian, existence/domain covariance of the propagator must be qualified; it is not supplied by the bounded proof. A parity-even bath reference can instead be factored into an interaction picture when the bounded interaction and its parity covariance are established.

Bosonic total number parity reverses every linear quadrature. Therefore sin(Phi(f)) is parity odd, and bounded contacts Z_i sin(Phi(f)) satisfy the hypothesis. Number-conserving passive bath propagation is parity even. The previously certified noncommuting sine contact is thus relevant algebraic machinery without having to pretend its full dilation is a controlled-Weyl displacement. Its earlier numerical certificate does not certify a new parity detector or this recovery circuit.

## 5. Why an extra code is not automatically useful

For n=1, the syndrome is empty and the same proof gives

    U=I tensor A_even + Z tensor A_odd.

Known initial bath parity and final parity measurement already correct an arbitrary parity-covariant pure-dephasing coupling. This is the closest existing mechanism. For n>1 the construction allows many physical source couplings, arbitrary bath correlations and extra coherent error paths to be corrected with one bath bit plus n-1 stabilizer checks; it does not improve the number of stored logical qubits per protected physical qubit in the pure-dephasing-only task.

Here is a finite-algebra sufficient corollary. Suppose there are r commuting bath involutions Pi_a with a known initial joint sector and operator grades

    Pi_a A_e Pi_a = (-1)^((L e)_a) A_e.

Let H be an X-stabilizer check matrix. The joint data syndrome and observed charge change select a fiber of e -> (H e,L e). If ker H intersect ker L={0}, that fiber has one member and the proof of (4) applies directly. For a CSS code with Z-stabilizer space D, it suffices that ker H_X intersect ker L is contained in D. Every two errors in the selected fiber then differ by a Z stabilizer, so their action on the code agrees; after a representative Z correction their bath coefficients sum into one bath operator. This proves id_L tensor the corresponding bath instrument on every joint sector. Stabilizer eigenvalue signs, if chosen negative, enter this sum as their known scalar phases.

For a pure-X code rank H=n-k, the injectivity condition requires k<=rank L<=r. For a CSS code, write dim D=r_Z and rank H_X=n-k-r_Z. The quotient condition implies rank[H_X;L]>=n-r_Z, hence again rank L>=k. This is a requirement for resolving the **whole diagonal-error family under the supplied charge signatures**, not an unconditional capacity bound on arbitrary environment-assisted codes.

When the criterion fails, an undetected diagonal logical operator in the common kernel carries neither syndrome nor charge signature. Symmetry alone cannot give a universal decoder for that error set. A particular calibrated model may still be more restricted, so this is not a universal physical no-go.

## 6. The system-only algebra obstruction and a preserved target factor

First consider **system-only recovery with the environment unobserved**. Let A be a unital star algebra of source errors exactly corrected by a code P. The Knill–Laflamme relations applied to I and a in A imply P a P=c_a P. Hence any U in A which preserves the code acts only as a scalar phase on that code. This elementary obstruction concerns that system-only error model. It does not apply to the unconditioned source algebra of an environment-assisted recovery: distinct bath outcomes can label different actions of the same source operator.

A simple receiver example is dual rail: restricting two source qubits to span{|01>,|10>} leaves one effective displacement feature f_1-f_2, so ordinary homodyne needs no retained quantum receiver mode. But Z_1 Z_2=-I on this code. The native pair phase exp(i theta Z_1 Z_2) is global and provides no encoded entangler.

If even-weight diagonal source phases are included inside U_sym in the odd repetition theorem, the recovery treats them as part of the error and removes them. A bath-free odd logical Z string violates the covariance of that error factor, so an **unmodelled unwanted** rotation generated by it remains uncorrected. Neither statement prevents preserving a specified desired gate.

**Target-factorization corollary.** Suppose the actual completed operation has an acquired factorization

    U_total=(G tensor I_B) U_sym,
    G J=J G_L,

where G is a prescribed diagonal source unitary preserving the code and U_sym obeys the preceding charge/covariance hypotheses. Use the same data syndrome, bath charge measurement and Z-string correction. Because G commutes with every Z^f,

    G Z^f J=Z^f J G_L.

Substituting this identity into the branchwise proof gives

    (Z^e P_s tensor M_(q,a)) U_total (J tensor Q_p)
       = J G_L tensor M_(q,a) A_e Q_p.       (6)

Thus the same complete instrument preserves the **nontrivial logical target G_L exactly**, for the same correlated inputs and fine records. For the odd repetition code, G also commutes with all syndrome projectors. The displayed derivation needs only code preservation and commutation with the diagonal errors; in more general codes it can be applied on the error-reachable code sectors without asserting an unnecessary global projector commutation identity.

For example,

    G=exp(i theta Z^(1^n))

preserves the odd repetition code and acts as exp(i theta X_L) in the basis {|+>^n,|->^n}. This is a continuous nontrivial logical gate. It breaks covariance of U_total, but not that of the separately identified error factor U_sym, which is all the corollary requires. The desired bath-free action and a charge-labelled error can therefore use the same source Pauli operator. A diagonal source Hamiltonian for G commutes with the specified diagonal-source bath contacts, so an actually supplied implementation can factor throughout an epoch.

The many-body control implementing that G for n>1 is not acquired. More generally, establishing U_total=G U_sym and the physical gate/recovery interface remains essential. An arbitrary unknown logical source term cannot be declared a desired G after the fact. The actual obstruction is missing distinguishability or a missing target/control interface, not a universal demand that the signal lie outside the source algebra appearing in monitored noise.

## 7. Interface, loss and reuse

The known-sector supply can be vacuum, a known parity state, or a trusted parity preparation/measurement. Thermal parity invariance alone is insufficient. A nondestructive initial parity measurement can prepare a known sector but has its own acquisition, back-action, bandwidth and resource cost.

For a no-return outgoing field, one can destructively count each packet and keep only the running parity bit for the decoder. The complete fine count record may also remain. This requires collection and parity discrimination of **every relevant** outgoing quantum mode, and measurement of any source-dependent retained memory or a proof that it is irrelevant. Destructive photon detection and nondestructive measurement of a retained oscillator are different operations.

Any missed parity-changing event can select the complementary logical error. If a bath is reused after a nondestructive final parity readout, its new sector q is known and the full-boundary identity composes with the next qualified epoch without a bath reset. Destructively read outgoing modes cannot later be reused as coherent resources. All subsequent Hamiltonians, source frames and syndrome controls must meet their actual toggled contracts; N1064's correction remains in force.

Ordinary unmonitored physical Z errors, parity-breaking drives, relaxation/leakage and faulty stabilizer extraction are additional channels. In particular a single untagged Z error can make a hard parity decoder choose the wrong logical complement. A practical decoder should treat an imperfect charge bit as evidence rather than an infallible constraint, using a qualified noise model. The ideal theorem alone gives no threshold or advantage over conventional QEC.

## 8. A streaming parity boundary with a reusable core

The required global charge measurement can have a local implementation when the actual bath has a retained core C and no-return outgoing packets. Suppose all bath-only propagation preserves the product of core and packet parities, and every declared source-odd contact reverses that same product parity. Let p_C be the known initial core parity, p_j the known incoming packet parities, q_j their measured outgoing parities, and q_C the final nondestructively measured core parity. The required charge-change bit is exactly the sign

    (-1)^t = q_C product_j q_j / (p_C product_j p_j).      (7)

All measured local parities commute. Outgoing packets may be destructively counted as soon as the no-return condition holds; keeping their full count records is a permitted refinement in (5). Only the running product is needed for decoding. Source-dependent core displacement need not close, because its parity is measured rather than omitted. The retained core remains a physical quantum memory, with its actual energy, lifetime and coupling costs.

For a storage epoch, the logical correction and core parity readout give id_L tensor a core-and-record instrument. A subsequent qualified epoch starts with the measured core sector q_C, so the bath can be reused without cooling or resetting its state. Known parity is the invariant supply condition. Thermal bath states can be made sector known by a trusted initial parity measurement, but the preparation cost and any conditioning of their energy distribution remain real; earlier thermal-start numerical/representation certificates cannot be silently transferred. Every entering packet must also have a known charge or a measured input charge record.

This is a concrete interface to finite causal-core machinery: acquire parity covariance of the actual interactions, initial charge knowledge, no-return packet access, a complete outgoing counter and a core parity instrument. It does not require acquiring every continuous output feature or representing the core state. For n=1 it is a non-Gaussian environment-assisted storage instrument; the code merely generalizes the error-label resolution. The symmetry and measurement interfaces remain stronger physical assumptions than small retained dimension.

## 9. Comparison and recommendation

This route supplies a clear mechanism outside the passive homodyne receiver class. It can replace detailed continuous bath-feature calibration with a conserved binary symmetry, at the price of known-sector startup and a complete non-Gaussian charge measurement. It is valuable as an extension/checkpoint and as a test of how strongly the passive receiver class mattered.

The equally informed conventional alternatives already include the n=1 parity eraser, model-specific random-unitary bath measurements, ordinary detected-error QEC, tailored codes for common dephasing, and passive no-knowledge homodyne when its feature interface is available. Their advantages cannot be excluded by this theorem. A broad computing advantage needs either several independently accessible charge signatures with useful logical rate, or an acquired encoded operation whose target factor is preserved while its unwanted coupling remains charge labelled. The target-factorization corollary supplies a mathematical compatibility principle; its many-body physical interaction/control bridge is still unconstructed.

Source details and exact executable checks are separate files in this directory. No external validation or historical novelty is claimed.
