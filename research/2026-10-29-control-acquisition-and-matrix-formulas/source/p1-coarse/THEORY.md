# Reciprocal experiment words and acquired error certificates

28 October 2026. Successor P1 construction. Ordinary proofs conditional on
the experimental interface below. Historical priority and a
civilisation-changing capability have not been established.

## 1. Change of scientific question

The predecessor's static scalar acquisition and concave control results
remain at their stated ranks, precision and execution scopes. The new
question is whether scalar experiments can acquire a finite description of
*compositions* of operations, while bounding its missing state instead of
assuming that state absent.

The exact pair in `branches/dynamics/CLIFFORD.md` agrees on every frozen
mixture, its scalar powers, resolvents and semigroups, and embeds in P1's
finite-rank variational source family. A five-operation word nevertheless
has responses 781/32768 and 1267/32768. More accurate static measurements
cannot resolve this ambiguity. Mixed words acquire different information.

Gram/GNS/Hankel realization, residual Koopman diagnostics and corrected
primal-dual output estimates are established mathematics. The proposed
addition is acquisition of their actual source inner products and residual
forms through scalar experiments, with finite-error certificates and no
hidden-rank assumption. No new generic projection principle is claimed.

## 2. Native experimental contract

In a real Hilbert space H of unspecified dimension, let b be a fixed
reset/read vector and A_i=A_i* with ||A_i||<=1. Positive contractions are
an important subclass. A chronological word w=(i_1,...,i_h) executes
A_w=A_(i_h)...A_(i_1); the empty word is I. An experiment prepares b,
executes w and supplies an interval for f(w)=<b,A_w b>.

Every interval used together must hold simultaneously during a stable,
calibrated epoch. Errors may be correlated or adversarial. Reproducible
reset, matched preparation/readout, required word lengths and reversed mode
order are supplied capabilities. Individual reversibility in different
metrics is insufficient: the Hilbert metric must be common.

For C xdot=-L_i x with one fixed C>0 and symmetric L_i>=0, propagation
exp(-tau_i C^-1 L_i) satisfies this contract in the C inner product. A port
profile v prepares C^-1v and reads v^Tx. Reversing the sequence order gives
the adjoint product without reversing diffusion. These are physical model
premises, not consequences of a finite fit. The separate physical note
also constructs a nonselective Lüders-channel interface and an exact
failure when the common-metric premise is removed.

## 3. Acquired source geometry

Choose native dictionary words w_1,...,w_r with w_1 empty, and write
V=[A_(w_1)b,...,A_(w_r)b], c=(1,0,...,0), so b=Vc. Columns may be dependent.
Acquire G=V*V, M_i=V*A_i V and N_i=V*A_i^2 V. Every entry is a scalar word:

    <A_v b,A_u b> = f(u followed by reverse(v)).

Insert i or ii between these two parts for M_i or N_i. Before duplicate
caching, at most (1+2q)r(r+1)/2 scalar readings suffice. If dictionary
lengths are <=L, acquired words have length <=2L+2. Standards are additional;
the sum of actual word lengths charges native operations. Reset, waiting,
energy, command fidelity and precision are not supplied by this count.

Any method may propose rational coefficient maps T_i. Define actual defects

    D_i = A_i V - V T_i,
    F_i = V* D_i = M_i - G T_i,
    E_i = D_i* D_i
        = N_i - M_i T_i - T_i* M_i + T_i* G T_i.       (1)

True E_i are PSD. No inverse of G or hidden dimension is needed. Exact
Galerkin T_i=G^-1 M_i, when meaningful, is the familiar F_i=0 special case.

## 4. Signed correction and exact identity

For a future word define alpha_0=c, alpha_t=T_(i_t)alpha_(t-1), beta_h=c,
and beta_(t-1)=T_(i_t)beta_t while traversing backward. Put

    ftilde = c*G alpha_h + sum_t beta_t*F_(i_t)alpha_(t-1).              (2)

**Theorem 1.** For arbitrary finite dictionary and arbitrary T_i,

    f(w)-ftilde = sum_(s<t)
      <D_(i_t) beta_t,
       A_(i_(t-1))...A_(i_(s+1)) D_(i_s)alpha_(s-1)>.                (3)

Consequently the absolute error is at most

    sum_(s<t) sqrt(alpha_(s-1)*E_(i_s)alpha_(s-1))
               sqrt(beta_t*E_(i_t)beta_t).                          (4)

**Proof.** The true forward state minus V alpha_t obeys an inhomogeneous
recurrence with forcing D_(i_t)alpha_(t-1). Telescope and pair with b. Each
forward defect is paired with the exact backward suffix
z_t=A_(i_(t+1))...A_(i_h)b. Its approximation V beta_t has error

    z_s-V beta_s = sum_(t>s)
      A_(i_(s+1))...A_(i_(t-1)) D_(i_t)beta_t.

The pairing with V beta_s gives exactly the signed correction in (2).
Pair the remaining two defects and reverse the interior product using
selfadjointness to get (3). The interior is a contraction; Cauchy-Schwarz
proves (4). No projection, rank, gap or inverse was used. QED.

For h=1 the corrected prediction reduces to its acquired M_i entry. A
poor proposal need not improve its point estimate after correction; the
identity and bound are the claims.

## 5. Exact finite-error implementation

Once T_i and the coefficient trajectories are fixed, (2) and every squared
residual in (4) are linear combinations of acquired scalar records. Combine
identical words before applying signed interval arithmetic. This respects
reuse of the same data and requires no independence. A numerical fitted
moment matrix is never silently treated as the source.

Take each squared-residual upper endpoint U and an outward rational bound
on sqrt(U). The code uses integer square root, then checks its square
exactly. A negative upper endpoint signals inconsistency with at least one
declared premise and stops the computation; it is not clipped to zero.

The double sum needs O(h) arithmetic after the forward/backward residuals
are available. Coefficient propagation and interval-expression assembly
use O(hr^2) arithmetic for fixed alphabet. Rational bit growth and storage
must also be charged; the execution records maximum coefficient bit length.
Singular G does not invalidate this procedure. It can make a proposal or
its noise amplification bad, producing a weak but sound certificate.

## 6. Uniform reuse without a hidden contraction gap

**Theorem 2.** Suppose a computational metric W>0 and 0<=rho<1 satisfy

    T_i* W T_i <= rho^2 W,       E_i <= epsilon^2 W                 (5)

for every primitive. Then every length-h word, h>=2, satisfies

    |f(w)-ftilde(w)|
      <= ||c||_W^2 epsilon^2 sum_(j=0)^(h-2) (j+1)rho^j
      <= ||c||_W^2 epsilon^2/(1-rho)^2.                            (6)

**Proof.** The forward residual at s is <=epsilon rho^(s-1)||c||_W,
and the backward residual at t is <=epsilon rho^(h-t)||c||_W.
Insert these in (4). With j=h-t+s-1, exactly j+1 pairs contribute.
The infinite series is (1-rho)^-2. QED.

The true operators and their unobserved complement need no contraction
gap. What is checked is a gap of the finite coefficient maps, *and* their
small measured actual source defects. Artificially shrinking a proposal
generally increases E_i; it does not establish (6) for free.

Let Ghat,Mhat be midpoint matrices. If their W-metric operator errors are
bounded by gamma_G and gamma_M, the point-prediction error from using these
midpoints in (2) is at most

    ||c||_W^2 [gamma_G rho^h
      +(gamma_M+rho gamma_G) h rho^(h-1)]
    <= ||c||_W^2 [gamma_G+(gamma_M+rho gamma_G)/(1-rho)].             (7)

There are h signed corrections and each coefficient norm product is
<=rho^(h-1)||c||_W^2. Also h rho^(h-1)<=1/(1-rho); the h=0 case is just the
Gram error. This proves (7).

`uniform_certificate.py` computes a sound upper matrix for E_i by adding
to its interval midpoint the diagonal of row sums of interval radii.
Validity follows from 2|x_j x_k|<=x_j^2+x_k^2. Domination constants are
proposed by a numerical generalized eigenproblem, then accepted only after
exact rational PSD checks. Computational W positivity and (5) are checked
the same way. Solver failure does not prove that no source certificate is
possible. A separate reviewer reconstructed all reported bounds without
importing this checker, using all principal minors instead.

## 7. Decisions and limits

For any finite menu of response intervals [L_w,U_w], select a word with
largest L_w. Its regret is <=max_w U_w-L_selected. Known linear costs can
be subtracted. The words may be selected after acquisition: the source
certificate is uniform. This does not solve the possibly exponential
optimization over all length-h programs, nor certify the complete
distribution of an adaptive measurement transcript.

In particular, this construction does not obtain a nonlinear source model,
an uncontrolled-environment reset, a conditional postselected quantum law,
or an adjoint operation for an arbitrary nonreciprocal device. There is no
guarantee that a small dictionary or useful computational gap exists. A
large residual, poor instrument precision or rho near one can make the
all-word bound vacuous.

## 8. Short echoes can lose a long task at finite precision

Compare, for b=e_1 and 0<e<=1/2, the positive contractions

    A_e = [[1-e,e],[e,1-e]],       B_e = (1-e) I.

Their length-h responses are (1+(1-2e)^h)/2 and (1-e)^h. Up to length four
the difference is at most 6e^2, so identical readings with radius 3e^2 can
be valid for both. At h=5/e the response difference tends to
(1+exp(-10))/2-exp(-5)>0.49. Thus a fixed short-echo design can need
precision O(h^-2) for a constant-error long task. This remains true in the
positive-contraction subclass; it is not merely a reflection example.

`SHORT_ECHO_OBSTRUCTION.json` checks h=20,100,500,2000 exactly. At h=2000,
all echoes of length <=4 admit common records of radius 0.00001865638671875,
while the long response gap is about 0.49332624. One length-h echo at error
0.01 separates this *known pair*, paying h native operations. No general
information lower bound or efficient search for such a word is inferred.

The first serialization of the long rational exceeded Python's decimal
digit limit. Its numerator and denominator are now retained as exact
hexadecimal integers; the mathematical computation and comparisons were
exact throughout.

The next construction uses informative blocks and their reversed adjoints,
paying block length explicitly. Known conserved components can be centered
out only under an actual source warrant or exact certificate. A small noisy
residual does not prove exact conservation.
