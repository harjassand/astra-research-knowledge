# Independent review: uniform all-prior replacement comparator

**Decision: ACCEPT the nonreference theorem in finite dimension and the stated
qubit/product-mean complete extension.** No correction to the frozen governing
statement is required. This review spells out support completions and excluded
extensions so that neither is left implicit.

Reviewed 2026-10-29 by `producer-workspace/review_history_program_bounds`.
Source: `uniform_coherent_prior_20261029/GOVERNING.md`, SHA-256
`9382f4581fbb6c82732dbec1f64a0a878626893897a0b7a3fb670d01797e579d`.
Only the files in the original SHA256SUMS manifest are received. Unmanifested
exploratory boundary/norm sweeps are not dependencies. Originals remain unchanged.

## 1. Received claims and metrics

Assume a finite-dimensional CPTP channel Phi has a specified state trace-distance
contraction upper bound c<1. For every finite ensemble with its **actual** mean
sigma, define the Holevo loss delta under Phi. The replacement channel
`E_sigma(A)=Tr(A) sigma` is EB, fixes sigma, and obeys

`sum_x p_x T(rho_x,sigma) <= min(1,sqrt(delta)/(1-c))`.

The prior need not be stationary, diagonal, faithful, or approximately known; the
mathematical conclusion is uniform over priors. Implementing the comparator does
presume sigma is specified. There is no prior-learning cost claim.

When A is a **qubit** and the actual ensemble mean on AR is sigma tensor omega,
the received complete version is

`sum_x p_x T(rho_AR,x, sigma tensor rho_R,x)
 <= min(1,3 sqrt(delta)/(1-c))`,

with delta now the Holevo loss under `Phi tensor id_R`. Letters may be entangled;
the reference is arbitrary finite-dimensional, and its marginal can depend on x.
The complete coefficient has no reference-dimension factor. E_sigma is EB on A,
not globally EB on an untouched AR reference.

All formulas above use nats; the displayed constants are also safe for bits.
For `Phi_gamma=Ad_X o AD_gamma`, its Bloch difference matrix is
`diag(sqrt(1-gamma),-sqrt(1-gamma),-(1-gamma))`. Therefore its exact coefficient is
`sqrt(1-gamma)` (attained on opposite equatorial pure states). For gamma>=1/2,
`1/(1-c)<=2+sqrt(2)`, yielding the advertised uniform unreferenced and complete
constants `2+sqrt(2)` and `3(2+sqrt(2))`. The c=0 endpoint is valid by the general
lemma, including a singular constant output.

## 2. Independent proof check

The pinned primary
[Junge–Renner–Sutter–Wilde–Winter, arXiv:1509.07127v3](https://arxiv.org/pdf/1509.07127v3)
was consulted at Theorem 2.1, Remark 2.2 / equations (18)–(21), and the stabilization
statement in Remark 2.4(4). Its universal averaged rotated-Petz channel gives,
on the appropriate support, one recovery R fixing sigma and
`T(rho,R Phi rho)<=sqrt(ell_sigma,Phi(rho))` for all supported rho. The trace bound
follows from its root-fidelity statement via
`T^2<=1-F^2<=1-exp(-ell)<=ell`.
The same recovery applies to every ensemble member.

CPTP contraction and the stipulated contraction coefficient then give

`T(R Phi rho,sigma)=T(R Phi rho,R Phi sigma)
 <= T(Phi rho,Phi sigma)<=c T(rho,sigma)`.

Triangle inequality moves the final term to the left. Averaging and Jensen prove
the first theorem because the ensemble mean is sigma and hence
`sum p_x ell_sigma,Phi(rho_x)=chi(ensemble)-chi(Phi ensemble)` exactly. This argument
does not assume decay of successive entropy losses, CP-mixture minorization,
self-compatibility, or a fidelity remainder for the unrotated Petz map.

The basic strictly contractive-channel framework is established prior machinery;
[Raginsky, arXiv:quant-ph/0105141v3](https://arxiv.org/pdf/quant-ph/0105141v3),
17 October 2001, was directly checked for the state-distance definition. No
historical novelty or priority conclusion is received here.

## 3. Support and regularization: no gap

Let P=supp sigma and Q=supp Phi(sigma). Every positive-weight ensemble state is
supported on P. Because sigma is strictly positive on P, each such state is
bounded above by a finite multiple of sigma; positivity of Phi puts its output in
Q. In fact the restriction `Phi: B(P)->B(Q)` is a CPTP channel on those spaces and
inherits the same contraction upper bound.

Apply the faithful-support recovery theorem there. If a channel on the original
ambient output is needed, the explicit completion is

`R_ext(Y) = R_Q(P_Q Y P_Q) + Tr[(I-P_Q)Y] sigma`,

with R_Q's output embedded back into the input space. This map is CP and TP,
agrees with the recovery on every relevant output, and fixes sigma after Phi.
Thus singular outputs do not require assuming the existence of a faithful
ambient output. This direct construction also makes the contraction argument
legitimate on the original spaces.

For the complete qubit theorem, if sigma has rank two, restriction to Q includes
Phi's outputs for **every** qubit state, so Psi=R_ext Phi is a full qubit CPTP
channel. A singular reference omega is handled by restricting its support;
positivity of the product ensemble mean places every letter there. At each
rotation time the omega modular factors cancel, leaving `R tensor id_R` on the
relevant support. Averaging preserves that identity.

If the qubit sigma has rank one, every AR letter is supported on
`span{|psi>} tensor R` and consequently equals `sigma tensor rho_R,x`. The
complete disturbance is exactly zero. This closes the pure-mean boundary
without any inverse, logarithm of zero, or continuity assertion about the
recovery map. Common faithful-state regularization is another valid route for
the unreferenced conclusion, but is not needed in this review.

## 4. Complete norm step: received, not naive tensor contraction

Write the full qubit channel Psi=R Phi in Bloch affine form `(r -> B r+b)`.
Since state trace distance for qubits is half the Euclidean Bloch distance,
composition with the CPTP R implies `||B||_2<=c`. Opposite Bloch states test every
real direction, so the bound covers the entire real 3x3 linear part. It does not
require B to be symmetric, normal, or diagonalizable.

The Neumann series gives `M=I-B` invertible and
`||M^-1||_2<=1/(1-c)`. Define L(I)=0 and L's Pauli transfer to be M^-1. On traceless
operators, the deficit `id-E_sigma` is the identity, so
`id-E_sigma=L(id-Psi)`. Both deficits vanish on sigma, and every operator A can
be written as `Tr(A) sigma + A_0`, Tr(A_0)=0. Hence the identity holds on all
operators, including traceful and non-Hermitian ones, and after arbitrary
reference stabilization.

For column v_j of M^-1 the rank-one operator map
`A -> (v_j.Pauli) Tr(Pauli_j A)/2` has diamond norm exactly ||v_j||_2: its output
trace norm is 2||v_j||_2, and the input functional has operator norm 1/2. Summing
three columns yields
`||L||_diamond<=sum_j||v_j||_2<=3||M^-1||_2<=3/(1-c)`.
Combined with the stabilized recovery theorem at the product prior and the exact
actual-mean Holevo identity, this proves the complete claim.

In particular, the proof never claims that `Phi tensor id_R` is strictly
contracting on all joint states. Such a claim would be false: states differing
only on an untouched reference keep their distance unchanged.

## 5. Independent tests

The author's 600-ensemble script replayed from a copied directory, producing a
byte-identical UNIFORM_CHECKS.json. It was inspected; the unused retrodicted-E
matrix returned by lib.py is not an assumption in its replacement-channel tests.

The independent script imports **no author code** and constructs averaged
rotated recovery by a general-dimensional spectral superoperator. It includes
an explicit CPTP completion outside the output support. Results:

- 75 qubit actual-mean HJW ensembles: complex coherent directions, radii through
  pure means, and gamma=.01,.25,.5,.9,1. Values below .5 test the general c-dependent
  theorem, not the uniform gamma>=.5 constant.
- 150 product-mean quantum-reference ensembles, including entangled letters,
  coherent/nonmaximal reference means and singular reference supports.
- 18 general-dimensional ensembles in dimensions 3 and 4, with input ranks 1,2,
  or full; rectangular padded outputs; and c=0,.3,.8. Known c is certified by
  constructing Phi as `c Lambda+(1-c) replace_tau`, rather than estimating it
  from samples. Recovery TP on the ambient output was checked.
- 100 exact Fraction 3x3 inverse cases with nonnormal matrices and a certified
  Frobenius contraction upper bound. These check algebra/transposes; the global
  Neumann and diamond estimates are analytic, not inferred from these samples.

Maximum fixed-prior residual was 2.23e-15; maximum full-operator deficit identity
residual 5.84e-14. All bounds passed, including boundary cases with zero error
(up to diagnostic roundoff). Numerical tests are explicitly not certificates of
universality; the analytic proof is the certification.

## 6. Essential limitations, with exact witnesses

1. **c<1 is essential for this theorem.** Computational dephasing preserves the
   equiprobable orthogonal Z-state ensemble, giving Holevo loss 0 but replacement
   disturbance 1/2.
2. **Product mean is substantive.** A singleton maximally entangled Bell ensemble
   has Holevo loss 0 for every channel, while replacement of A by its marginal
   sends the state to I/4 at trace distance 3/4. It is not a product-mean ensemble.
3. Strict contraction on A does not survive stabilization as a strict contraction
   on all AR states: orthogonal unchanged R states give input/output distance 1.
   The Pauli-deficit proof is what avoids this mistake.
4. No dimension-free complete theorem for arbitrary input dimension, no tensor
   powers of many noisy qubits, no uniform extension to c=1 or c approaching 1,
   and no unrestricted N371 closure are received.
5. The earlier one-prior complete coefficient 5 and diagonal-preserving comparator
   can remain sharper or preserve more information. This theorem instead
   demonstrates concentration around the actual mean in the strictly contracting
   regime. It does not claim preservation of nontrivial classical information.
6. No self-compatibility audit, finite-data prior learning, hardware performance,
   implementation advantage, or novelty conclusion is part of this receipt.
