# A response-derived maximum preparation kernel

## Status and selection consequence

This independent construction gives an exact, physically attained uncertainty
geometry and a finite-error implementation from position-response data. It
does not establish historical priority, a new general theory of optimal
recovery, or an advantage over an equally informed method using conservative
realization and optimal recovery. Those comparisons are strong enough that
this is a structural companion, not the selected major programme.

The initial derivation was recorded in FIRST_PRINCIPLES_DERIVATION.md before
nearest-literature comparison. Earlier accepted results are not modified.

## 1. Physical class

Fix known M, Gamma, mu > 0. An admissible realization consists of a real
Hilbert space H, a contraction-semigroup generator A, and bounded b in H:

    x' = v,
    M v' = -mu x - Gamma v - <b,z> + f,
    z' = A z + b v.                                             (1)

The whole state has storage

    E(q) = (mu x^2 + M v^2 + ||z||^2)/2,                         (2)

and E' <= f v - Gamma v^2. Bounded coupling makes (1) a bounded perturbation
of a well-posed semigroup. No bound on dim(H) is assumed. An optional known
upper bound on ||b|| is preserved by the construction below.

The known visible law, collocation and energy norm are physical premises. A
response fit alone does not establish them. This is narrower than the class
of all passive ports. Let S(t) be the zero-state displacement step response.
Let C_S contain all realizations of (1) with that same S, each allowing every
initial state of energy <= E. Initial energy includes visible x and v; if
either is known, that information must be conditioned on, not silently reset.

## 2. Maximum-kernel theorem

**Theorem 1.** If C_S is nonempty, the kernel

    Cmax(t,s) = 1/mu - S(|t-s|)
      -2 Gamma int_0^min(t,s) S'(t-u)S'(s-u)du                  (3)

is positive semidefinite. The union, over C_S and initial energy <= E, of
free visible paths is exactly the radius-sqrt(2E) reproducing-kernel Hilbert
space ball for Cmax. A single admissible conservative-bath completion attains
that entire set, retaining the original local Gamma damper. Consequently all
bounded output functionals have exactly the uncertainty geometry of this one
energy ball, without identifying the actual hidden realization.

### Proof

Classical unitary dilation gives an isometry J and a unitary group U(t) with
J*U(t)J=exp(tA), t>=0. Replace the bath by the skew-adjoint generator of U,
and b by Jb. Both its memory kernel and its initial-state force agree:

    <Jb,U(t)Jb>=<b,exp(tA)b>,
    <Jb,U(t)Jz>=<b,exp(tA)z>.                                 (4)

Variation of constants gives the same visible path under every additive f.
The embedding preserves energy and ||b||. The completion itself belongs to
C_S; only the bath is dilated, not the supplied local damper.

Normalize q=(sqrt(mu)x,sqrt(M)v,z). In this completion let L be the full
generator, B=(0,1/sqrt(M),0), Cq=x. Then

    L+L*=-2 Gamma BB*,  LC*=-B,  CC*=1/mu.                    (5)

The first identity is an energy-form identity. The second is well defined
even for unbounded bath generators because C* has zero bath component.
Writing h(t)=C exp(tL)B=S'(t), integration of LC*=-B yields

    C exp(tL)C*=1/mu-S(t).                                    (6)

For t>=s, the dissipative semigroup identity is

    exp(tL)exp(sL*)=exp((t-s)L)
       -2 Gamma int_0^s exp((t-u)L)BB*exp((s-u)L*)du.          (7)

Integrate the weak derivative of exp((t-u)L)exp((s-u)L*); alternatively use
bounded-generator approximation, since the dissipation operator is bounded.
Multiplication by C,C* gives (3) and the Gram representation

    Cmax(t,s)=<exp(tL*)C*,exp(sL*)C*>.                         (8)

Every original realization embeds into its completion. All completions have
the same Gram kernel (3). Sending time-t representers in one completion to
those in another is an isometry on their span and its closure. Projecting
away unobservable directions cannot increase norm. Thus all completions have
the same visible energy-ball image. Any one completion attains the full union.
The standard quotient definition of the reproducing-kernel norm gives the
claimed ball equality. QED.

The result specifies maximum uncertainty over a declared class. It neither
identifies the actual state nor proves readiness of one unknown realization.
A smaller dissipative realization can have less uncertainty with the same S.
No Gaussian initial-state prior is assumed: an identity-covariance Gaussian
on an infinite Hilbert space generally is not a finite-energy measure.

## 3. Exact finite-record minimax uncertainty

For bounded output functionals ell_i, subtract the known forced response,
leaving y_i=<r_i,q0>. For target y*=<r*,q0>, set

    G_ij=<r_i,r_j>, c_i=<r_i,r*>, d=||r*||^2.                  (9)

**Theorem 2.** Exact data are feasible iff y belongs to range(G) and
y^T G^dagger y <= 2E. Their exact scalar minimax center and radius are

    center = c^T G^dagger y,
    radius = sqrt[(2E-y^T G^dagger y)(d-c^T G^dagger c)].      (10)

Both interval endpoints are attained by finite-energy physical states in
the conservative completion.

**Proof.** The minimum-norm explaining state is
q_par=sum_i (G^dagger y)_i r_i, with squared norm y^T G^dagger y. Every feasible
state is q_par+q_perp, with q_perp perpendicular to all record representers
and norm squared <=2E-y^T G^dagger y. The squared norm of the target's
perpendicular representer is d-c^T G^dagger c. Cauchy-Schwarz gives (10), and
the positive/negative residual directions attain it. Theorem 1 gives physical
attainment. Zero residual factors give radius zero. QED.

The same projection state supplies a center for a future path. Its exact
supremum-norm radius is the supremum of the pointwise radii, attained or
approached at a maximizing time. This does not assert that one state attains
all pointwise extrema simultaneously. With bounded errors in exact-model
records, the feasible set is a ball intersected with slabs. Projection onto
span{r_i,r*} reduces each scalar endpoint to finite convex optimization. The
exact pseudoinverse is not claimed robust to noisy acquisition of singular G.

### Additive actuation

At fixed observation functionals, additive controls change only a known forced
component. Subtracting it leaves the same hidden-state information. This holds
also for controls chosen from earlier reports: recursively the residual
reports carry the same information. Under an additive control-independent
meter model, the error sets also match. Changing stiffness/coupling, changing
noise, resetting the plant or allowing unknown backaction changes the premise.
This is ordinary linear superposition/observability separation, not a claim
against every physical intervention.

## 4. Forced-response order does not determine preparation rank

A finite conservative bath gives finite-rank Cmax, equal to the observable
full-state dimension. In contrast, a one-dimensional dissipative bath

    A=-a, b=sqrt(B), a,B>0, K(t)=B exp(-at)                    (11)

has a third-order rational displacement response, yet its conservative bath
kernel is B exp(-a|t|). Its spectral measure has strictly positive Lorentzian
density B a/[pi(a^2+omega^2)] on the entire line, hence infinite cyclic rank.

Cmax has infinite rank even on every interval [0,L] with L>0. The
bath-force kernel B exp(-a|t-s|) is strictly positive definite on arbitrarily
large finite sets: its positive spectral density makes every nonzero finite
sum of exponentials have positive squared norm. Its trajectory range is
therefore infinite dimensional. Fix initial x=v=0. The causal map from free
bath force to x is injective on this interval, because x identically zero
implies v=0 and then (1) gives zero free bath force. This injective map preserves
infinite dimensionality of the bath-force trajectory space. Its images lie in
the full preparation space, proving infinite rank.

This is an exact-rank statement, not an infinite finite-accuracy cost claim.
It is also a familiar conservative-dilation mechanism rather than established
historical novelty. Known small forced-response order does not alone license
a small exact sufficient state for arbitrary hidden preparation.

## 5. Finite position boxes and acquired response error

For observation/target boxes phi_i=1_[a_i,a_i+w_i]/w_i inside [0,L], extend
S(t)=0 for negative t and define

    H_i(u)=[S(a_i+w_i-u)-S(a_i-u)]/w_i.                        (12)

Integrating (3) gives

    G_ij=1/mu-int int phi_i(t)phi_j(s)S(|t-s|)dt ds
                 -2 Gamma int_0^L H_i(u)H_j(u)du.             (13)

Only position-response values and finite differences occur. No velocity
meter, differentiable response fit or derivative oracle is supplied.

Suppose an acquired certificate supplies

    sup_[0,L]|S-S_hat|<=epsilon_S.                            (14)

Completing the square in the source spring energy under unit step force gives
int_0^infinity (S')^2<=1/(2 Gamma mu). Put

    Q=1/sqrt(2 Gamma mu), e_i=2 epsilon_S sqrt(L)/w_i.          (15)

Young's convolution inequality gives ||H_i||_2<=Q; (14) gives
||H_i-Hhat_i||_2<=e_i. Applying (13) to S_hat produces Ghat obeying

    |G_ij-Ghat_ij|
     <=epsilon_S+2 Gamma[Q(e_i+e_j)+e_i e_j].                 (16)

If beta bounds every right side and p counts all boxes including the target,

    G <= U := Ghat+p beta I                                  (17)

in Loewner order, since the spectral norm of the error is <=p beta. This also
proves U positive semidefinite without claiming an inferred empirical rank.

For any chosen weights a and finite reports |yhat_i-y_i|<=eta_i,

    |y* - sum_i a_i yhat_i|
      <=sqrt[2E (-a,1)^T U(-a,1)] + sum_i |a_i|eta_i.          (18)

This holds for every allowed state/realization on the response and meter
certificate events. Meter backaction must be absent or charged in the declared
model/error/energy ledger. Subtracting a forced component adds its response
uncertainty to eta_i; zero applied force avoids that subtraction error.

### Finite computation

For rational piecewise-linear S_hat on m intervals, all of (13) is exact
rational integration. Let F(z)=int_0^|z|(|z|-u)S_hat(u)du. Then

    int_a^b int_c^d S_hat(|t-s|)ds dt
      =F(b-c)+F(a-d)-F(b-d)-F(a-c).                           (19)

Each Hhat_i is piecewise linear, so products integrate as piecewise quadratics.
Sorting shifted knots gives O(p^2 m log m) arithmetic operations; merging
sorted lists removes the logarithm. Bit work is polynomial in p,m and all
rational input bit lengths. Outward rational bounds for Q,sqrt(L),beta and
the final square root supply finite certificates. For supplied rational a no
optimization oracle is needed. The optional convex norm-plus-weighted-l1
minimization has its own requested precision cost.

For small epsilon_S,

    beta=O(epsilon_S[1+sqrt(Gamma L/mu)/w_min]
             +Gamma L epsilon_S^2/w_min^2).                  (20)

To make the inflated part of a radius at most rho, the response certificate
must satisfy

    2E p beta ||(-a,1)||_2^2 <= rho^2.                        (21)

Narrow boxes, many records, large weights and tiny desired errors amplify
the response-precision cost. Exact kernel conditioning is not earned by a
coarse table.

## 6. Physical and computational ledger

The construction consumes the accepted response-acquisition certificate; its
loading, private timing, force, metrology, ADC, clock, table storage and error
probability remain payable. It does not create a response oracle. A physical
continuation adds p-1 position boxes with sensor initialization/reset, timing,
range, precision and backaction costs. It occupies the retained loaded plant
over [0,L]. Its total initial energy bound must hold after calibration. A new
hidden state needs a new record or the original worst-case radius. Continuous
unbudgeted heat input is outside the finite-energy model.

Storage is O(m+p^2) rational scalars, plus streamed meter reports. Arithmetic
depends on the acquired table and chosen boxes, not hidden dimension. Physical
hidden-state storage remains the retained plant. The retained plant is not
replaced by a small numerical state merely because S is compact.

The accompanying execution has two scopes: floating finite-matrix diagnostics
of (3), and exact rational integration of the preserved acquired response table
with its actual uncertainty. Neither is a new laboratory acquisition. The
finite-error computation is conditional on the prior certificate and leaves
that certificate and its sources unchanged.

In the executed inherited-table calculation, epsilon_S=0.0562185, L=1 and four
width-0.1 boxes give beta=5.764832900050874. The certified predictor radius is
4.873211089055686 at E=1/2 and new meter-error allowance 0.001 per record, while
the universal energy-only displacement-box bound is 1. The operation should
therefore fall back to the energy-only center/radius at this precision. This
shows failure of this sufficient inflation certificate to improve that bound;
it does not prove that every inference from the same raw reports must fail.

The independent floating checks give maximum identity error 7.50e-16 for a
six-dimensional conservative source. For a third-order dissipative source,
its eight-time maximum preparation Gram has smallest eigenvalue 5.75e-6,
whereas the actual source Gram has rank at most three; the smallest eigenvalue
of their PSD difference is 6.28e-9. These are diagnostic numerical values,
not substitutes for the proofs above.

## 7. Primary comparison

Unitary dilation is classical. Mielke, Peletier and Zimmer, *Deriving a GENERIC
system from a Hamiltonian system*, arXiv:2404.09284, Appendix C, gives a directly
relevant modern physical construction, including infinite-dimensional
conservative extensions of finite dissipative systems.

Ball, Kurula, Staffans and Zwart, *De Branges--Rovnyak realizations of
operator-valued Schur functions on the complex right half-plane*,
arXiv:1307.7408, and Ball, Kurula and Staffans, *A conservative de
Branges--Rovnyak functional model for operator Schur functions on C+*,
arXiv:1703.04705, provide broader passive realization/functional-model theory.

Hilbert optimal recovery already supplies the projection/radius calculation.
Foucart and Liao, *Radius of Information for Two Intersected Centered
Hyperellipsoids and Implications in Optimal Recovery from Inaccurate Data*,
arXiv:2401.11112, treats modern finite optimizations for inaccurate information.
Formula (10) is basic Hilbert geometry, not a new algorithmic primitive.

Accepted Astra N997 already treats exact/uncertain operator histories and
task-directed experiments, explicitly tying equally informed optimal recovery.
Another quadratic record optimizer therefore cannot be called a major advance
by renaming it or overlooking its existing comparator.

The completed assembly here is the explicit response-only maximum kernel (3),
its physical attainment over unknown realizations, and the derivative-free
finite-data bridge (13)--(18). It makes the uncertainty object and precision
cost explicit. The strongest equally informed conservative-realization and
optimal-recovery method can use the same construction. Historical novelty and
a practical advantage are not established. This remains a useful completed
companion, rather than the selected major capability.

### Primary links

* https://arxiv.org/abs/2404.09284
* https://arxiv.org/abs/1307.7408
* https://arxiv.org/abs/1703.04705
* https://arxiv.org/abs/2401.11112
* https://github.com/harjassand/astra-research-knowledge/blob/626bf0fb5da19c8eb62964f0d7949bb19bc64799/knowledge/current/packets/N997-p3-retained-uncertainty-task-directed-experiments.json
