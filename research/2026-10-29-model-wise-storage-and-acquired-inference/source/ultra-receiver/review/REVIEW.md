# Independent whole-chain quantum-memory receiver review

29 October 2026. Retained peer C, independent mathematical reconstruction.

**ACCEPTED at the stated conditional scope.** This is a whole scientific review
of root's `root_quantum_receiver/PROOF.md` and `CKG_ADMISSION.md`, not a finite
example, a physical-bath admission, or an acceptance of the separate static
noncommuting Peierls claim. The latter has a different proof obligation.

Reviewed source digests:

* `PROOF.md`: `d94d08dc948bb6ea777629aac3fa5ff44c809ce163660e10c34f76b71d037a10`.
* `CKG_ADMISSION.md`: `0968140c280464647655ebdbc7209ab0ce01d0b72c033c2e0a341e4e372f0eb5`.

## 1. Exact logical algebra really gives a positive encoder

Let X,Z be anticommuting Hermitian involutions. Choose an orthonormal basis
of the +1 eigenspace of Z and use its X-images for the -1 eigenspace. This
constructs a unitary U identifying the full space with C² tensor K, with X,Z
acting as the logical Pauli matrices. In particular the dimension is even;
this is an exact representation, not a claim about an arbitrary decoder's
adjoint. Set Y=iXZ.

For any faithful state rho, the Pauli average is

    sigma = (rho+XrhoX+YrhoY+ZrhoZ)/4
          = U†[(I/2) tensor tau]U,
    tau = Tr_L(UrhoU†).

Consequently Enc(omega)=U†(omega tensor tau)U and Dec=Tr_K composed with U
are CPTP, and Dec Enc=id. The state rho itself need not factor or commute
with the logical Paulis. A stabilizer implementation must supply one common
syndrome recovery inducing this exact algebra. Efficient preparation of tau,
physical encoding, and implementation of U do not follow.

## 2. The fidelity constant and its precise all-input conversion

Let T_t be a CPTP semigroup fixing rho. Unital Schwarz and stationarity give

    ||T_t*(A)||_rho² <= Tr rho T_t*(A†A) = ||A||_rho²,

where ||A||_rho²=Tr rho A†A. Integrating the generator therefore gives
||T_t*(O)-O||_rho <= t||L*(O)||_rho. No detailed balance is needed.

For Lambda=Dec T_t Enc, the exact maximally-mixed entanglement fidelity is

    Fe(I/2,Lambda) = [1+sum_O Tr sigma O T_t*(O)]/4,

where O ranges over X,Y,Z. This follows directly from the Pauli expansion of
a maximally entangled state and the adjoints of Enc and Dec. Since sigma
commutes with O, the displayed correlations are real. Also
||O T_t*(O)|| <= 1, so replacing sigma by rho costs at most
epsilon=||sigma-rho||_1 per term. Cauchy--Schwarz then proves

    Fe(I/2,Lambda) >= 1-e,
    e = [3epsilon+t sum_O ||L*(O)||_rho]/4.                    (R1)

The following conversion was independently derived here and supplied to root.
For any d-dimensional CPTP map with Kraus operators A_j,

    1-Fe(omega,Lambda) = sum_j Var_omega(A_j).

Center B_j=A_j-Tr(A_j)I/d; variance is unchanged by scalar shifts. Thus

    1-Fe(omega,Lambda)
      <= Tr omega sum_j B_j†B_j
      <= sum_j Tr B_j†B_j
       = d[1-Fe(I/d,Lambda)].                                (R2)

Every purified logical-qubit input has overlap fidelity at least 1-2e, and
the pure-state trace-distance inequality implies
||Lambda-id||_diamond <= min(2,2 sqrt(2e)). These are conditional error bounds;
negative fidelity lower bounds are simply vacuous. The single-use number in
(R1) alone must not be described as every-input entanglement fidelity.

## 3. The Gibbs comparison is valid without a condition number

For rho=e^(-beta H)/Z and Hermitian involution O, set K=[O,H]. Duhamel gives

    [O,sqrt(rho)] = -(beta/2) integral_0^1
                    rho^(s/2) K rho^((1-s)/2) ds.

The overall sign is immaterial. Since K is anti-Hermitian,
|K_ij|²=|K_ji|² in a rho eigenbasis. Weighted AM--GM and this symmetry give

    sum_ij rho_i^s rho_j^(1-s)|K_ij|²
      <= sum_ij rho_j |K_ij|² = ||[H,O]||_rho².

Factoring the difference of two squares in trace norm then proves

    ||rho-O rho O||_1 <= 2||sqrt(rho)-O sqrt(rho)O||_2
                      <= beta ||[H,O]||_rho,
    ||sigma-rho||_1 <= (beta/4) sum_O ||[H,O]||_rho.           (R3)

No lower bound on the least Gibbs eigenvalue was used. Faithfulness holds
for every finite-dimensional finite-beta Gibbs state.

## 4. Whole-support stability handles coherent jumps

For a support X, assume one common orthogonal P_good satisfies
[O,A_X]P_good=0 for **every** operator on X. It follows that
[O,A_X]=[O,A_X]P_bad and

    ||[O,A_X]||_rho <= 2||A_X|| sqrt(Tr rho P_bad).            (R4)

There is no need for rho or O to commute with P_good in this argument. A
common good projector for a spanning Pauli algebra is enough by linearity;
separate projectors for different Paulis are not enough without intersection.

The exact Heisenberg identity is

    D_L*(O) = L†[O,L] + (1/2)[L†L,O].

Left multiplication is bounded in the rho norm. Both L and L†L have the
same support. Applying (R4) proves

    ||D_L*(O)||_rho <= 3||L||² sqrt(p_bad).                  (R5)

This derivation neither moves an uncontrolled operator through rho nor
replaces a coherent jump by independent Pauli jumps. Every Hamiltonian term,
including a coherent Gibbs-sampler correction, must also be included in L*.
Exact stationarity is an independent assumption.

For E=L-L_R, ||E||<=r, direct expansion of the full dissipators yields

    ||D_L*(O)-D_LR*(O)|| <= 4||L||r+2r²,  ||O||<=1.         (R6)

The cross terms are retained. A Hamiltonian tail of norm r costs at most 2r.
These estimates permit proof truncation of an exact quasilocal generator;
they do not make its finite-radius physical truncation stationary.

## 5. Strong ordinary antecedents and the actual extension

[Alicki--Horodecki--Horodecki--Horodecki, arXiv:0811.0033](https://arxiv.org/html/0811.0033),
Section II.1, already uses a virtual qubit, a thermal ancilla, and logical
autocorrelations to lower-bound average fidelity. Its Dirichlet exponential
bound uses the stated reversible/normal-generator structure.

[Bravyi--Terhal, arXiv:0907.2807v2](https://arxiv.org/html/0907.2807),
Section 6, Definition 1 and Theorem 1, already treats protected Pauli-like
observables and arbitrary stationary Lindblad noise without detailed balance.
It assumes the protected observables and protected projector commute with H,
and obtains a bound linear in the bad Gibbs weight. It explicitly credits
the earlier subsystem encoding construction. This is the controlling ordinary
comparator, rather than a claim that arbitrary Lindblad memory criteria are new.

The reviewed receiver relaxes exact Gibbs/logical commutation by paying (R3),
uses the full-generator GNS defect, and loses a square root in (R5). It does
not dominate the commuting theorem. No world-priority assertion is made for
this elementary composition or the centered-Kraus conversion.

## 6. Admission verdict

The root's CKG class is mathematically nonempty at constant per-site update
rate, with all frequency and coherent-tail costs paid; see
`CKG_INDEPENDENT.md` for an independent normalization/tail reconstruction.
It is an algorithmic exactly stationary class, not a microscopic Davies bath.
None of this accepts an unproved Peierls probability, native Gibbs
initialization, physical controlled spectral filtering, or robustness to a
constant error in the implemented generator. Those remain distinct inputs.
