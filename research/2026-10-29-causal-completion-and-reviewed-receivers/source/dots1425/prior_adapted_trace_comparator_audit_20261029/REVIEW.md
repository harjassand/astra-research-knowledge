# Independent receiving review: coherent-prior EB trace comparator

**Decision: ACCEPT, at the explicitly stated one-prior / product-barycenter scope.**

Reviewed 2026-10-29 by `producer-workspace/review_history_program_bounds`. The frozen source is
`prior_adapted_trace_comparator_20261029/GOVERNING.md`, SHA-256
`593e0f324def42d2576b5b7d8478411a91c22f9f18000cf54b5afeec8c2bd53d`.
No source file was edited. The receipt binds copies, original manifests, independent
programs and results. This review is separate from all decoder/compression receipts.

## 1. Precisely received statement

Let `Phi = Ad_X o AD_(1/2)` and
`sigma = [[1/2,1/4],[1/4,1/2]]`. Let `E` measure computational Z and, after outcome j,
prepare the normalized pure state proportional to `sqrt(sigma)|j>`.
For any finite ensemble with **actual mean sigma**, writing

- `delta = chi(ensemble) - chi(Phi ensemble)`,
- `e_avg = sum_x p_x ||rho_x-E(rho_x)||_1/2`,

one has `e_avg <= min(1,5 sqrt(delta))`, with entropy measured in nats. The same
numerical inequality is also safe if entropy is in bits. More generally the
certificate gives the smaller constant `C = sum_ij |T_ij|`, rigorously enclosed near
4.3686449267162265.

The received reference extension replaces states by arbitrary, possibly entangled
`rho_AR,x`, Phi by `Phi tensor id_R`, and E by `E tensor id_R`, **provided the actual
ensemble mean is sigma tensor omega_R**. There is no reference-dimension penalty.
The map E is EB on A; this does not assert that `E tensor id_R` is an EB channel on
the entire AR input. A singular omega is handled by restricting to its support;
positivity and the assumed ensemble mean put every nonzero-weight letter there.

The general sufficient mechanism for a faithful qubit prior, faithful output,
invertible deficit matrix M and an explicit EB map fixing that prior is accepted.
Existence of such an invertible M, of a suitable EB map, or of any uniform C is not
asserted in general.

## 2. Full-operator and complete-norm arguments

Both Psi = averaged-rotated-Petz o Phi and E are trace-preserving and fix sigma.
Thus their deficits preserve the traceless subspace. On the Pauli basis their
matrices are M and N, and `T = N M^-1` makes `id-E = L o (id-Psi)` on that subspace,
where `L(I)=0` and L has Pauli transfer T. For an arbitrary operator A, write
`A = Tr(A) sigma + A_0` with Tr(A_0)=0. Both deficits kill the first summand, proving
the claimed identity on **all** operators, not just density matrices or Hermitian
traceless inputs. Equivalently, if sigma=(I+s.Pauli)/2 then the traceful deficit
column is -M s or -N s, and `T(-M s)=-N s`.

For `F_ij(A)=Pauli_i Tr(Pauli_j A)/2`, the stabilized map is a rank-one output map
composed with a functional. Its diamond norm is exactly
`||Pauli_i/2||_1 ||Pauli_j||_infinity = 1`. The upper bound holds for arbitrary
operators and references; an eigenstate of Pauli_j attains equality. Consequently
`||L||_diamond <= sum |T_ij|`. L need not be positive or TP, and nothing in this
argument presumes it is physical. The full-operator identity tensored with an
identity map therefore gives the required trace-distance comparison.

The universal recovery input was verified directly in the pinned primary:
[Junge–Renner–Sutter–Wilde–Winter, arXiv:1509.07127v3](https://arxiv.org/pdf/1509.07127v3),
Theorem 2.1, Remark 2.2 / equations (18)–(21), and Remark 2.4(4). That primary gives
the beta-weighted rotated Petz map, the fidelity lower bound, exact recovery of the
prior, and stabilization under a faithful product reference. The resulting
`T(rho,Psi rho) <= sqrt(ell(rho))` uses
`T^2 <= 1-F^2 <= 1-exp(-ell) <= ell` (root fidelity convention).
Averaging the relative-entropy losses over the **actual** mean sigma gives exactly
delta, and Jensen yields the advertised average bound. For a product reference,
the modular factors from omega cancel at every rotation time, before averaging;
no claim of general tensorization of the rotated-Petz average is used.

## 3. Concrete map and Fourier formula

The Kraus matrices in the source are exactly those of X after amplitude damping
at 1/2. The prior eigenvalues are 1/4, 3/4. Its output is
`nu = [[1/4,sqrt(2)/8],[sqrt(2)/8,3/4]]`, with eigenvalues
`1/2 +/- sqrt(6)/8`; both priors are faithful.

For an independently transparent check on E, its two prepared states have Bloch
vectors `(1/2,0,+sqrt(3)/2)` and `(1/2,0,-sqrt(3)/2)`.
Thus E fixes sigma exactly, is a physical two-outcome measure-and-prepare channel,
and its traceless deficit matrix is
`N = diag(1,1,1-sqrt(3)/2)`.

At integration time t the primary's `R^(t/2)` contributes the phase with frequency
`-(log s_i-log s_j-log v_a+log v_b)/2`. The sign is immaterial because beta_0 is even;
the factor 1/2 is essential and the source includes it correctly. Substitution
`y=exp(pi t)` transforms `beta_0(t)dt` into `dy/(1+y)^2`. The beta integral then gives
`integral beta_0(t) exp(i x t) dt = x/sinh(x)`, with its continuous value 1 at zero.
Hence the finite spectral-projector formula evaluates the actual universal
averaged recovery, not the unrotated Petz map or an approximate time quadrature.

## 4. Interval implementation: independently received

The author's 45-decimal mpmath interval script was inspected and replayed from a
copy. The certificate JSON is byte-identical. Inputs .5 and .25 are exact binary
rationals. Every syntactic zero frequency `(i=j,a=b)` is exactly zero. All other
frequencies in this particular spectrum are bounded away from zero. Real-part
extraction is justified by exact Hermiticity preservation. The cofactor transpose
and determinant division implement the inverse correctly. Neither an inverted
interval crossing zero nor an uncertified floating inverse is used.

More importantly, `rational_interval_check.py` independently proves the same
constant **without mpmath or any floating-point transcendental operation**:

1. All endpoints are exact Python Fractions; each arithmetic operation rounds
   outward to a 180-bit dyadic grid.
2. Square-root endpoints use integer `isqrt` and exact comparisons.
3. For positive rational x, range reduction writes x=2^k z, 1<=z<=2. With
   t=(z-1)/(z+1), the log is bounded by 80 terms of
   `2 sum_(n=0)^79 t^(2n+1)/(2n+1)` and a positive remainder at most
   `2 (1/3)^161 / [161(1-1/9)]`. The same construction bounds log 2.
4. Rather than exponentials, the kernel is evaluated as
   `log(r)/(sqrt(r)-1/sqrt(r))`, where `r=s_i v_b/(s_j v_a)`.
5. Real symmetric and real antisymmetric sectors reduce the transfer inverse to
   a 2x2 inverse and one scalar inverse, independent of the author's 3x3 adjugate.
   The real basis `(X,J=iY,Z)` has identical nonzero Pauli transfer entries because
   these maps have real Kraus/projector data and preserve Hermiticity.

The rational certificate proves det M>0 and C<5; every independent interval is
contained in the corresponding original 45-digit enclosure. The C interval width
is below 1.39e-50. It also verifies interval inclusion of zero for the full deficit
identity on all four matrix units and for both fixed-prior residuals. These
residual tests supplement, rather than replace, the exact algebra in section 2.
Runtime/Python integer correctness remains trusted; this is not a proof-assistant
formalization.

## 5. Reproducible tests and boundaries

`independent_checks.py` performs supplementary, explicitly non-certifying checks:

- 10 signed/zero Fourier frequencies against direct integration;
- the entire recovery map on four matrix units against direct time integration of
  spectral matrix powers (maximum discrepancy 2.24e-16);
- complete reference factorization on 80 matrix-unit/time cases, with a coherent
  nonmaximally mixed reference (maximum discrepancy 2.67e-15);
- the full deficit identity on 80 arbitrary non-Hermitian joint operators in
  reference dimensions 1,2,3,5 (maximum discrepancy 2.71e-15);
- positivity/TP diagnostics for the three channels;
- 54 HJW pure-state ensembles with exact intended product barycenters, including
  entangled letters and reference dimensions 1,2,3; direct Holevo loss agrees with
  the average relative-entropy loss to 1.06e-15. All inequalities pass.

The author's optional 300-ensemble diagnostics and 378-point floating exploration
also replay byte-identically. They are diagnostics, not universal certificates.

**Not received:** arbitrary correlated AR means; arbitrary coherent priors;
uniform constants over a family; recovery on many independently noisy qubits;
unrestricted N371; first-Petz/first-recovery priority; acquisition, learning, or
implementation advantages. This is an explicitly known-prior EB comparator whose
recovery map is an analytical witness. The interval constant is an upper bound
on a diamond norm, not an exact diamond-norm computation. No SDP was used.
