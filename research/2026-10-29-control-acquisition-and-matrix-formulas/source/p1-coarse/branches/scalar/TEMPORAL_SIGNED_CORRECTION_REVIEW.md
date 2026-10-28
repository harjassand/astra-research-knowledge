# Independent review: temporal signed correction and precision

28 October 2026. This is a scoped independent argument and exact finite check
of Root's new temporal construction, not a whole-pipeline or physical audit.
Root independently derived the signed correction and owns the central
compiler. No accepted Astra foundation is reopened here.

## Contract and scalar acquisition

Let b be a repeatable preparation in a real Hilbert space, and let the A_i be
bounded selfadjoint contractions in one common inner product. A chronological
word w=(i_1,...,i_h) means A_w=A_(i_h)...A_(i_1). The receiver supplies sound
intervals for f(w)=<b,A_w b>. This amplitude interface, common metric,
reciprocity, contraction and reset/stability are genuine source premises.
Intensity-only readings do not automatically provide it.

Choose q preparation words w_j, including the empty word. Their unobserved
column operator is V=[A_(w_1)b ... A_(w_q)b]. No linear independence, known
hidden dimension or finite hidden rank is required. Echoes acquire

    G=V^T V,   M_i=V^T A_i V,   N_i=V^T A_i² V.                (1)

Entry j,k is the scalar chronological word w_k, zero/one/two inserted i
operations, then reversed w_j. Reversal uses the same actual selfadjoint
operations, not an opaque adjoint oracle. The matrices are symmetric. Before
word reuse, at most (2a+1)q(q+1)/2 scalar moment values suffice for a operation
types. If preparation words have length at most ell, acquisition words have
length at most 2ell+2. Counts do not acquire preparation, operation time,
resetting, calibration, integration time or absolute precision.

## Exact signed-correction identity

Choose arbitrary q-by-q real coefficient maps L_i. They need not be
contractive, metric selfadjoint, or obtained from a Gram inverse. Let c0
select the empty-word column, so Vc0=b exactly. Define

    E_i=A_i V-V L_i,
    D_i=M_i-G L_i=V^T E_i,
    R_i=N_i-M_i L_i-L_i^T M_i+L_i^T G L_i=E_i^T E_i.           (2)

Thus R_i is PSD even when G is singular. For target word i_1,...,i_H, put

    alpha_t=L_(i_(t-1))...L_(i_1)c0,      alpha_1=c0,
    beta_t=L_(i_(t+1))...L_(i_H)c0,       beta_H=c0,
    alpha_(H+1)=L_(i_H)...L_(i_1)c0.

Root's signed-corrected predictor is

    ftilde=c0^T G alpha_(H+1)+sum_t beta_t^T D_(i_t) alpha_t.   (3)

The exact remainder identity is

    f(w)-ftilde
      =sum_(1<=t<s<=H) (E_(i_s) beta_s)^T
        A_(i_(s-1))...A_(i_(t+1)) (E_(i_t) alpha_t).           (4)

An empty middle product is identity.

**Proof.** Forward telescoping gives

    A_(i_H)...A_(i_1)b-V alpha_(H+1)
      =sum_t A_(i_H)...A_(i_(t+1)) E_(i_t) alpha_t.

Taking inner products with b and reversing each left suffix by selfadjointness
introduces z_t=A_(i_(t+1))...A_(i_H)b. Telescoping this reversed suffix gives

    z_t=V beta_t
      +sum_(s>t) A_(i_(t+1))...A_(i_(s-1)) E_(i_s) beta_s.

The first terms yield (3). Transposing the remaining middle products gives
(4). The calculation uses no Gram inverse, rank decision, orthogonal
projection or finite-dimensional hidden realization. Finite words and bounded
operators make the argument equally valid in an infinite-dimensional Hilbert
space. True contractions and Cauchy-Schwarz yield

    |f(w)-ftilde| <= sum_(t<s)
       sqrt(beta_s^T R_(i_s) beta_s)
       sqrt(alpha_t^T R_(i_t) alpha_t).                       (5)

The correction need not improve the point estimate for arbitrary poor L. The
claim is the exact identity and second-order residual remainder. Exact
Galerkin data D_i=0 specialize to the ordinary two-crossing projection bound.

## Finite precision without a Gram floor

For fixed L and a target word, (3) is linear in raw moments. Each residual
square is also linear in raw moments:

    z^T R_i z=z^T N_i z-2(L_i z)^T M_i z+(L_i z)^T G(L_i z).   (6)

A simultaneous bounded-error transcript therefore gives an interval for
ftilde and upper bounds for every residual square in (5), without any lower
bound on the smallest Gram eigenvalue. G may be singular. Joint PSD and
word-consistency constraints can tighten this; simple raw intervals already
suffice for soundness.

Aggregate coefficients of identical raw words before applying the error
allowance. For uniform error eta and aggregated coefficients a_w, the
allowance is eta*sum|a_w|. Bounding G, the raw predictor and each correction
independently loses cancellations. For H=1, (3) collapses exactly to a single
acquired moment regardless of the arbitrary proposal L. Known transitions
between dictionary word columns similarly give residual polynomials that
are identically zero; duplicated noisy uses must not invent an error there.

Adaptive choices of L and future words are valid on the simultaneous raw-data
event because these bounds are deterministic on that event. They do not
improve its probability. A probabilistic receiver must pay its confidence
construction for the actual acquisition. Large coefficients, residuals and
horizons can still make certificates wide. The absence of a Gram floor is
not free precision or a universally efficient state-learning theorem.

## Fixed short-record precision witness

Let b=e1 in R², c²+s²=1, s>0, and

    A=[[c,s],[s,-c]],  Bplus=I,  Bminus=diag(1,-1).             (7)

These are selfadjoint contractions. The witness uses negative eigenvalues;
it would require reconsideration under an additional PSD-operation premise.
With dictionary V=[b,Ab], both sources have

    G=[[1,c],[c,1]],  M_A=[[c,1],[1,c]],  N_A=N_B=G.

Their B moments differ only at entry (2,2):

    M_Bplus=G,
    M_Bminus=[[1,c],[c,c²-s²]].                               (8)

The gap is 2s². All queries have length at most four. A common record with
the differing value at its midpoint fits both sources with per-reading
adversarial error eta>=s². Repetition does not remove that ambiguity. Both
exact dictionaries span the entire hidden space, so exact projection leakage
is zero; the obstacle is uncertainty in the acquired representation.

Write c=cos(theta),s=sin(theta). A Bminus is a rotation by theta whereas
A Bplus=A. For even k near pi/(2theta), the chronological word B,A repeated
k times has amplitudes

    fplus=1,  fminus=cos(k theta),  H=2k.                     (9)

The gap is order one while s² is order H^-2. Thus this fixed short-moment
acquisition needs resolution on the H^-2 scale to exclude a constant target
prediction error. This is not a lower bound against all experiments: a direct
query of the long word distinguishes them, with its operation/preparation
costs charged.

Exact rational instances use t=1/N, c=(1-t²)/(1+t²), s=2t/(1+t²).
At N=512,k=402,H=804,

    eta=1048576/68720001025 ~ 1.52587e-5,
    lambda_min(G)=2/262145,

while the target amplitude gap is approximately 0.999514. The exact rational
gap is proved greater than 9/10 in the executable check.

With the perfectly conditioned one-column dictionary V=[b], the same family
has leakage epsilon_A=s, epsilon_B=0. Coherent repeated excursions produce
constant scalar error when Hs is order one. Quadratic two-crossing accumulation
is therefore a real possibility, independent of an ill-conditioned Gram.

## Established machinery and the potential acquisition contribution

The signed primal-dual output correction is established reduced-model
machinery. Haasdonk and Ohlberger, *Efficient Reduced Models and A-Posteriori
Error Estimation for Parametrized Dynamical Systems by Offline/Online
Decomposition* (journal 2011; preprint November 2009), Section 5, improves
scalar outputs with a dual correction. The source formulates reduced models
using state/operator projection and an offline/online decomposition:

https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/publications/HO11_pre.pdf

A stronger data-driven comparator is Uy and Peherstorfer, *Probabilistic error
estimation for non-intrusive reduced models learned from data of systems
governed by linear parabolic partial differential equations*, ESAIM M2AN 55
(2021), 735–761:

https://www.numdam.org/item/10.1051/m2an/2021010.pdf

The actual first two pages explicitly require a queryable source returning
high-dimensional solution trajectories for chosen initial conditions and
control inputs. Residual-norm operators are acquired by least squares.
Associated research code was located at
https://github.com/wayneisaacuy/OpInfErrEst ; it was not executed or audited
in this branch.

The candidate contribution is acquisition of the residual quadratic forms
and signed correction through scalar reset-and-echo words, with certification
in potentially singular data coordinates. It is not a new general DWR
principle. An equally informed existing model-reduction implementation may
adopt the acquisition operation without erasing that addition. Historical
novelty, practical physical coverage, acquisition/precision economics and
advantage over direct long-word queries remain distinct obligations.

## Completed review scope

`temporal_residual_review.py` does not import Root's compiler. It constructs
rational native matrices, word columns and arbitrary coefficient maps, then
checks (2) and exact identity (4) at horizons 1,2,5,6. Four dictionary columns
live in R3, so G is necessarily singular. The coefficient maps are deliberately
non-selfadjoint and are not Galerkin solutions. Every pair term satisfies its
exact Cauchy inequality. The script also checks compatible-record precision
witnesses at horizons 12,52,200,804. Its result is
`TEMPORAL_RESIDUAL_REVIEW_CHECKS.json`.

Covered: the displayed algebra, contraction bound, and finite exact witnesses.
Not covered: Root's raw-word aggregation code, finite-instrument decoding,
physical realizations, universally efficient basis discovery, or complete
system comparison. Those are separate new load-bearing uses.

## Additional precision strengthening: a well-conditioned Gram and a paid binary receiver

The H^-2 raw-signal separation is not inherently a Gram singularity. Add a
third hidden coordinate killed by both operations, and take

    b=(3/5,0,4/5), a=9/25,
    A=diag(A_(2x2),0),
    Bplus=diag(1,1,0), Bminus=diag(1,-1,0).

All remain selfadjoint contractions and ||b||=1. Use V=[b,Ab]. Both sources
now have

    G=[[1,a c],[a c,a]],
    M_A=[[a c,a],[a,a c]],
    N_A=N_B=[[a,a c],[a c,a]],
    M_Bplus=N_B,
    M_Bminus=[[a,a c],[a c,a(c²-s²)]].                         (10)

Only the last B moment differs, by 2a s². The Gram is uniformly well
conditioned: determinant >=a(1-a)=144/625 and trace=34/25, so its smaller
eigenvalue is at least determinant/trace >=72/425. Yet the same long word
has amplitudes a and a cos(k theta), with constant separation.

This also exposes a complete-cost trap under an explicitly declared receiver.
Suppose each independent reset-and-word experiment returns Y in {-1,+1}
with mean f(w), with no added information. This is one allowed statistical
scalar receiver model, not a claim about every physical instrument. For the
only differing short moment, the Bernoulli success probabilities differ by
a s² and stay bounded away from 0 and 1. Their one-read KL divergence is
O(s^4). All other acquired moment words have identical output laws.

The chain rule for KL therefore bounds an adaptive T-reading transcript's
KL by O(T s^4). Pinsker's inequality implies that constant-confidence
separation of the two target predictions needs T=Omega(s^-4)=Omega(H^4)
short-moment readings. A direct query of the target word has a constant
amplitude gap and needs only a constant number of this receiver's readings
for constant error/failure probability, each paying H operations. This is
an Omega(H^4) versus O(H) operation-cost contrast for this *one task and
this acquisition dictionary*, up to constants, since moment words have
bounded length. Reuse over enough future tasks, a different dictionary,
longer acquisition words, stronger receiver information or actual structure
can change that comparison.

Consequently the temporal compiler's structural theorem is meaningful, but
scalar read counts alone do not establish an operational speedup. Required
precision and the actual receiver law must be charged. The deterministic
bounded-error witness and the binary statistical lower bound have different
premises and should not be merged into a universal sample/photon theorem.
