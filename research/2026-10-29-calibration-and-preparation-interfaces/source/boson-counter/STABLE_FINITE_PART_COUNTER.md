# A stable Kramers HS identity whose continued determinant has the wrong trace

## 1. Precise statement and primary boundary

Consider a single site with two unconstrained boson modes a=(b,c). Let N=a^dagger a and S_j=a^dagger sigma_j a, j=x,y,z. At beta=1 choose

`H = S_x^2+S_y^2+S_z^2 - N^2/2`.

This is a stable Hamiltonian with a finite, unambiguous grand-canonical partition function. It admits an exact continuous Gaussian/compact-group HS identity, sector by sector, all of whose one-body histories have Kramers symmetry and a positive algebraic inverse determinant. Nevertheless integrating that continued determinant does NOT yield the physical partition function: the proposed result is less than 7/9, while the physical result is greater than one.

The controlling claim tested is the post-continuum finite-part recovery identity in Yu–Wei–Li **arXiv:2610.31541v1**, SM section IV, equations (S95)–(S103), especially (S101) and (S103). The stated input there is a stable many-body Hamiltonian with finite grand-canonical trace; the treatment expressly allows field histories with divergent bare traces. Its starting interaction class in SM (S1) is a sum of squares of Hermitian one-body operators, with either sign, and (S3)/(S4) give their real/imaginary Gaussian decouplings. No commutativity of different channels is assumed there. The present H has exactly four such channels, with coefficients +1,+1,+1,-1/2 and quadratic H0=0.

The configuration-level Kramers determinant sign statement, SM (S111)–(S113), remains true. The counter does not reject trace-convergent implementations, the valid U2=0 lattice models, canonical coefficient recurrences, or all positive representations of this Hamiltonian. This one-site physical model has an ordinary positive occupation representation.

**Limit boundary:** the exact continuous HS identity below is used directly. We do NOT claim that a particular finite Gaussian-slice determinant expectation converges to our answer. Its kernel is unbounded near a determinant zero, so weak convergence of the group products alone would not pay that extra limit or trace-norm convergence. The counter targets a general post-continuum finite-part completion, not the numerically reported finite-slice solver's unqualified limiting value.

## 2. Stability and normal ordering

The Schwinger-boson identity is

`S_x^2+S_y^2+S_z^2 = N(N+2)`.

For example S_z=n_b-n_c, S_+=b^dagger c, S_-=c^dagger b, S_x=S_++S_-, S_y=-i(S_+-S_-). Then S_x^2+S_y^2=2(S_+S_-+S_-S_+)=4n_b n_c+2N. Adding S_z^2 gives N^2+2N. All normal-order contributions have therefore been included.

Consequently

`H = N^2/2+2N = N(N-1)/2+(5/2)N`.

In the n-particle sector it has energy n^2/2+2n and multiplicity n+1. Hence

`Z_phys = sum_{n>=0} (n+1) exp[-n^2/2-2n] > 1`,

and the sum converges superexponentially. Its vacuum energy is exactly zero. There is no omitted scalar prefactor or chemical-potential shift.

## 3. Exact continuous HS construction from native one-body Gaussian increments

Let U_t be SU(2) Brownian motion starting at identity, generated in Stratonovich form by the three independent increments

`dU_t = i sqrt(2) sum_j sigma_j U_t circle dW_j(t)`.

This is the compact-group limit of the ordinary repulsive-channel Gaussian factors exp[i sqrt(2 dt) phi_j sigma_j]. It stays unitary with determinant one. In the n-boson symmetric-power representation, Ito correction gives

`d Gamma_n(U_t) = i sqrt(2) sum_j S_j Gamma_n(U_t) dW_j - sum_j S_j^2 Gamma_n(U_t) dt`.

Thus

`E Gamma_n(U_1) = exp[-n(n+2)] I_(n+1)`.

Let s be an independent real standard normal. It is exactly the scalar HS field for the attractive channel -N^2/2, and E exp(sn)=exp(n^2/2). For B=exp(s) U_1 we therefore have the exact sector identity

`E Gamma_n(B) = exp[-n^2/2-2n] I_(n+1)`.

It holds on the finite-particle core for every n, and its sectorwise average extends to the actual positive trace-class exp(-H). It is not a Bochner integral of trace-class field operators: many individual histories are not trace class. That is the missing interchange to be tested, not an assumption made here.

Every history is Kramers invariant. Theta=i sigma_y K obeys Theta^2=-I, sends every sigma_j to -sigma_j and i to -i, and so leaves each i sigma_j increment invariant. The real scalar exp(s) is invariant as well. Particle-number conservation supplies the corresponding number-conserving class of the primary theorem. The number-conserving second-quantized propagator Gamma(B) fixes the vacuum; no Nambu half-shift or extra c-number is present.

## 4. The positive finite part and its exactly integrated value

Write r=exp(s)>0. For U in SU(2) with eigenvalues exp(+-i theta),

`W_reg(r,U) = det(I-rU)^(-1) = [1-2r cos(theta)+r^2]^(-1)`.

It is strictly positive except at r=1,U=I. For r<1 it is the convergent bare Fock trace and has the character expansion

`W_reg(r,U) = sum_{n>=0} r^n chi_n(U)`.

Since |chi_n(U)|<=n+1 and r<1, averaging this expansion is justified by absolute convergence. Put

`F(r) = sum_{n>=0} (n+1) exp[-n(n+2)] r^n`.

The group average of W_reg equals F(r) for 0<r<1. For r>1 use the exact SU(2) determinant identity

`W_reg(r,U) = r^(-2) W_reg(1/r,U)`.

Thus its average is r^(-2)F(1/r), not the entire analytic function F(r). The real Gaussian s has positive probability on BOTH sides of zero, and the field formula's positive continuation has changed the integrated answer.

Define J(a)=integral_0^infinity (2pi)^(-1/2) exp(-t^2/2-a t) dt. By Tonelli applied to the nonnegative averaged series on each half-line,

`Z_det = E_s,U W_reg(exp(s),U)`

`      = sum_{n>=0} (n+1) exp[-n(n+2)] [J(n)+J(n+2)]`.

This converges. No unproved passage from finite time slices is involved in the formula. The discrepancy comes from replacing the physical sector sum/HS average by a pointwise continued trace.

## 5. Strict rational separation without numerical quadrature

J is decreasing, J(0)=1/2, and

`J(2) <= (2pi)^(-1/2) integral_0^infinity exp(-2t)dt < 1/5`,

using pi>25/8. Hence J(n)+J(n+2)<7/10 for every n>=0. Also n(n+2)>=3n for n>=1. Since e^3>20,

`sum_{n>=1} (n+1) exp[-n(n+2)] < sum_{n>=1}(n+1)/20^n = 39/361 < 1/9`.

Therefore

`0 < Z_det < (7/10)(1+39/361) = 280/361 < 7/9 < 1 < Z_phys`.

The gap is at least 81/361. It is not a small trace-pole variance effect. There can be no missing scalar normalization consistent with the original number-conserving HS identity and vacuum convention: those already fix exp(-H)'s vacuum contribution at one.

`regularization_counter.py` verifies the elementary constant bounds with exact Fractions, checks finite symmetric-power Casimirs as controls, and evaluates both convergent series at high precision for illustration. The all-n identity and strict separation are the analytic proof above, not an extrapolation from those controls.

## 6. Consequence for the chosen capability

Positive algebraic weights are not enough to acquire a physical Gibbs law on an unbounded bosonic Fock space. For divergent bare histories, removing a field-dependent growing contribution and then integrating requires a new, valid interchange theorem; finite physical Z alone does not provide it. Our construction gives an exact stable failure for that broad post-continuum claim, including its advertised Kramers symmetry.

The balanced K,K canonical operation in PROOF.md avoids this failure completely: each actual sector trace is a finite polynomial, with no finite-part continuation, and the class has a native nontrivial extensive U2=0 Hamiltonian. Its own precision/statistical costs and the strong canonical-AFQMC incumbent remain. This is a scoped mathematical and operational discrimination, not a general solution of frustrated many-body prediction or a historical-priority claim.
