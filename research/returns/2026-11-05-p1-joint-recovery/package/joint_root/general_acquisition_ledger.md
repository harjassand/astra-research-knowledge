# A positive acquisition ledger for every causal receiver

5 November 2026. New continuation framework for the same homogeneous tracial
partial-SWAP stream. The collision identity is the accepted Astra acquisition
identity, now applied in the changing relative Hilbert space of an arbitrary
physical receiver. Contractivity of the sandwiched order-two relative norm,
Petz recovery and Renes's fidelity comparison are existing machinery. This
framework does not, by itself, evaluate the optimum memory-dependent loss.

## Scope and normalization

Let the input qubit be L and the source be S. After receiver step j, let
N_j:L -> S M_j be the full channel, where M_j includes all retained quantum
systems and all classical history as a direct sum. The reference is arbitrary.
Receiver maps may depend on the complete classical record and use independently
initialized pure or mixed workspace. No source access is supplied.

For logical input tau=I/2, the actual source and receiver average state factors
EXACTLY: N_j(tau)=tau_S tensor sigma_j. This follows because the original source
and all unprocessed carriers are jointly tracial on this input, and receiver
actions on emitted carriers cannot correlate them with the source. Conditional
average states in each classical-history block also have this product form.
This does not say that source and memory are independent for other logical
inputs or for the Bell input.

For mu=1,2,3 define rho_(mu,j)=N_j(sigma_mu/2) and the balanced operators

  X_(mu,j)=(tau_S tensor sigma_j)^(-1/4) rho_(mu,j)
                                      (tau_S tensor sigma_j)^(-1/4).

All inverses are on support. Channel positivity ensures that the logical images
have the required support. Use ordinary Hilbert-Schmidt norms, summing over
classical blocks. Let P be the orthogonal projection onto the source-identity
sector, and Q=I-P. Thus P(X)=I_S tensor Tr_S(X)/2. Put

  a_j=(1/3) sum_mu ||P X_(mu,j)||_2^2,
  q_j=(1/3) sum_mu ||Q X_(mu,j)||_2^2.

Initially a_0=0 and q_0=1 for ANY independent receiver initialization.

## Receiver contraction

For a CPTP receiver map Lambda_j from M_(j-1) E_j to M_j, including a classical
history register, its average input is omega_j=sigma_(j-1) tensor tau_E and its
average output is sigma_j. Define the relative Hilbert-space map

  V_j(X)=sigma_j^(-1/4) Lambda_j(omega_j^(1/4) X omega_j^(1/4))
                                                   sigma_j^(-1/4).

It is a contraction in Hilbert-Schmidt norm on the support. One justification is
data processing of the sandwiched order-two relative divergence, applied to
omega+t A and omega and expanded to second order for arbitrary supported
Hermitian A. If Tr A is nonzero, normalize the perturbed state by its trace;
the same scalar normalization occurs before and after Lambda and cancels.
The constant and linear terms cancel because Lambda is trace preserving.
Splitting a general matrix into Hermitian and anti-Hermitian parts
gives the full contraction. Equivalently this is the monotone chi-square metric
associated with the operator-monotone function f(t)=sqrt(t).

The map on S M E is id_S tensor V_j. Therefore it preserves the P and Q sectors
and is contractive separately on each. Direct sums include classical outcomes
and feedback; direct integrals give the same argument for continuous outcomes.
No bound on their number is used in this argument.

## Exact collision and nonnegative losses

Appending tau_E appends I_E/sqrt(2) in balanced coordinates. Because the source
and new carrier are tracial, the partial-SWAP unitary commutes with the reference
state and acts unitarily on balanced coordinates. The accepted source-identity /
source-traceless orthogonal splitting consequently applies without modification:
with b=sin(theta)^4 and r=1-b, immediately after the collision and before receiver
processing,

  a_j^- = a_(j-1) + b q_(j-1),
  q_j^- = r q_(j-1).

The new P contribution is orthogonal to the old P contribution because its new
carrier factor is traceless. The collision scales the entire Q norm by r, with
all old receiver coefficients included; no product approximation is made.

Define actual receiver losses

  ell_j^P = a_j^- - a_j >= 0,
  ell_j^Q = q_j^- - q_j >= 0.

Then EVERY permitted physical receiver obeys the exact equalities

  a_j = a_(j-1) + b q_(j-1) - ell_j^P,
  q_j = r q_(j-1) - ell_j^Q.

In particular,

  a_j+q_j=1-sum_(k<=j)(ell_k^P+ell_k^Q),
  q_j=r^j-sum_(k<=j)r^(j-k)ell_k^Q,

and the final accessible visibility is EXACTLY

  a_N = 1-r^N - L_N,
  L_N = sum_(j=1)^N [ell_j^P+(1-r^(N-j))ell_j^Q] >= 0.       (LEDGER)

Loss in already acquired information has weight one. Loss in the remaining
source-traceless component has the exact remaining-acquisition weight
1-r^(N-j). This distinguishes coherent receiver processing from pre-access
carrier deletion without changing the underlying physical source.

## Operational interpretation and attained fidelity comparison

Let E_N=Tr_S N_N be the actual channel into retained memory and classical history.
Its Petz channel relative to tau has entanglement fidelity

  F_P(E_N) = [1+3 a_N]/4.                                  (EXACT)

To verify this, for any qubit-input channel E with average sigma=E(tau), expand
the normalized Choi state in the Pauli basis. Its Petz entanglement fidelity is
one quarter of the sum of the four balanced Hilbert-Schmidt squared norms.
The identity contribution is one. Taking Tr_S selects exactly the P-sector
coefficients above: if P X=I_S/sqrt(2) tensor A, then the balanced reduced
memory image is A. This proves the displayed equality.

Consequently the optimum final decoder on the attained memory has

  epsilon_opt >= (3/4)(1-sqrt(a_N)).

There is also a direct proof of this comparison in the present normalization.
For a final decoder D define y_mu=sigma^(-1/4) E_N(sigma_mu/2)
sigma^(-1/4) and z_mu=sigma^(1/4) D^*(sigma_mu) sigma^(1/4). Then
F_e(D E_N)=1/4+(1/4)sum_mu <z_mu,y_mu>. For Hermitian B,
Tr(sqrt(sigma) B sqrt(sigma) B)<=Tr(sigma B^2); this is the nonnegativity
of the squared commutator [sqrt(sigma),B]. Kadison's inequality for the
unital CP map D^* gives D^*(sigma_mu)^2<=I, hence ||z_mu||_2<=1.
Cauchy-Schwarz and sum_mu||y_mu||_2^2=3a_N yield
F_e(D E_N)<=(1+3sqrt(a_N))/4, and half-diamond error is at least 1-F_e.
The sharper general recovery comparison and its prior attribution to Renes
are retained; this elementary proof checks the exact source-specific factors.

Conversely, run a finite Clifford twirl of the whole receiver (apply the same
random Clifford to every arriving carrier, retain its classical label, and undo
it on the final output) and finish with the corresponding physical Petz decoder.
Source covariance guarantees that this operation has a depolarizing logical
channel with visibility a_N. It therefore attains

  epsilon_Petz-twirl = (3/4)(1-a_N)
                    = (3/4)(r^N+L_N).

The error ratio is at most two. The Petz decoder is a definite finite CPTP map
on the actual retained register; it may require expensive synthesis and service
time. The statement does not assume it is cheap, or that a low-loss receiver has
already been constructed. Independently initialized ancillas and the transient
environment must be counted in a physical implementation.

For target 0<=epsilon<=3/4, every successful receiver necessarily satisfies

  L_N <= 1-r^N-(1-4epsilon/3)^2.

The sufficient condition supplied by the physical Petz-twirl finish is

  r^N+L_N <= 4epsilon/3.

For small epsilon these necessary/sufficient budgets differ only by a factor two
in total residual-plus-loss. They hold jointly for every theta,N,epsilon.

The source-granted Petz fidelity at prefix n is likewise

  F_P(N_n)=[1+3(a_n+q_n)]/4.

For a completely Kraus-refined receiver, the accepted positive-instrument witness
has the direct ledger meaning
Tr(H_n Z_n)=(3/4) sum_(j<=n)(ell_j^P+ell_j^Q).
For an unrefined physical receiver, reveal the additional Kraus labels only in
the converse relaxation. Relative-norm contraction when these labels are
forgotten implies Tr(H_n Z_refined) <= (3/4) sum_(j<=n)(ell_j^P+ell_j^Q).
Thus the same dimension-based lower bound applies to the actual ledger, but
equality with a refined witness is not asserted for a coarse instrument.
This joins the old all-instrument spectral converse to a time-resolved positive
loss identity; it does not replace its needed spectral or causal estimate.

## A finite-count strengthening of the preserved crossing converse

Let D=2^n and suppose every branch at cut n has memory dimension <=m. Let g_n
be the preserved all-prefix crossing bound (or any stronger valid gap). The old
witness gives

  (3/4) sum_(j<=n)(ell_j^P+ell_j^Q) >= g_n (1-m/D).

All losses in this prefix have final weight at least 1-r^(N-n). Hence, for n<N,

  a_N <= 1-r^N -(4/3)(1-r^(N-n)) g_n (1-m/D).

Combining with a_N >=(1-4epsilon/3)^2 yields the necessary joint finite-parameter
condition

  m/2^n >= 1 -
    3[1-r^N-(1-4epsilon/3)^2]/[4(1-r^(N-n))g_n].

Negative numerator means that even the unrestricted all-output acquisition
necessary condition fails. A negative right-hand side is simply vacuous. This
bound retains all angle, error and collision-count quantifiers. It still does
not yield the requested matching weak-angle memory scaling with the presently
proved g_n.

## Relation to the local preprocessing extension

For a product local preprocessor with Petz visibility lambda_j, the exact losses
are ell_j^P=(1-lambda_j)s^4 q_(j-1) and
ell_j^Q=2(1-lambda_j)c^2s^2 q_(j-1). Substitution gives the previously derived
recurrence a_j=a_(j-1)+lambda_j s^4q_(j-1),
q_j=(c^4+2lambda_j c^2s^2)q_(j-1). A shared coherent receiver has general losses
depending on its full state and cannot be assigned those product formulas.

## Remaining central operation

The original problem is equivalently an attainable low-loss control problem:
construct finite-width causal instruments whose actual L_N is O(epsilon) at
N=Theta(theta^-4 log(1/epsilon)), with paid service and control, or prove the
minimum possible L_N at a given coherent width and processing budget and match
it by an operation. The ledger is exact for this task. Its equality alone is
not that minimization, and no optimal memory scaling is claimed here.

## Primary attribution and validation

The relative-norm contraction is the monotone quantum chi-square metric of
Petz, with the channel monotonicity proof reproduced as Theorem 4 of Temme,
Kastoryano, Ruskai, Wolf and Verstraete, J. Math. Phys. 51, 122201 (2010),
arXiv:1005.2358. It also follows from sandwiched Renyi-2 data processing:
Beigi, J. Math. Phys. 54, 122202 (2013), arXiv:1306.5920; Frank and Lieb,
J. Math. Phys. 54, 122201 (2013), arXiv:1306.5358. The source collision
orthogonality, all-output decoder and sharp finite-prefix witness are the
accepted Astra results preserved in the earlier report and package.

The changing-reference split and weighted ledger are this continuation's
deductions. Independent channel and algebraic audits checked the contraction,
normalizations and coarse/refined witness distinction. The script
check_general_ledger.py tested 48 combinations of nontracial initialized
memory, random CPTP maps, recorded versus discarded Kraus outcomes and
history dependence at several angles and dimensions. It reconstructed
physical Petz Kraus operators as an independent fidelity check. Maximum
ledger residual was 2.7e-15 and maximum fidelity residual 2.5e-15. These
finite tests validate implementation, not the general proof or an optimum law.
