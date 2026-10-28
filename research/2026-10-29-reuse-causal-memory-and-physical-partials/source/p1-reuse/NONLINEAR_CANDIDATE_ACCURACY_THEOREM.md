# Separate the learned dynamics from the noise control variate

29 October 2026, Brisbane. Ordinary proof and complete interface construction.
This nonlinear extension has not been executed in a new numerical fixture.
The affine specialization is the completed accuracy-interface experiment.

## 1. Representation change and target

The paired-energy certificate initially used an affine candidate because its
stationary law is an explicit Gaussian. The actual requirement is weaker:
an executable Lipschitz function of independent Gaussians, together with a
bound on its distance to a candidate stationary law. A finite contractive
nonlinear chain provides both. Also separate the candidate b, which models
the dynamics, from a matrix A, which controls native observation noise.

The target is the invariant law pi_g of

    K_g(x,.)=N(m_g(x),sigma^2 I),  m_g(x)=E g(x+G),

with G~N(0,I), sigma>0 and supplied global Lip(g)<=L<1. Only original
entire-vector values g(z) are available. After paid training, freeze an
evaluable b with a justified global Lip(b)<=beta<1 and an evaluable matrix A
with known ||A||<=a. Both may be learned from the same data. The candidate
kernel is directly K_b(x,.)=N(b(x),sigma^2 I), not a heat average of b.
This distinction eliminates a hidden candidate-mean oracle. Each kernel has
a unique invariant law in P2 by its strict contraction.

## 2. Actual finite candidate preparation

Execute Y_0=0, Y_(t+1)=b(Y_t)+sigma Z_(t+1) for exactly T steps. Let nu_T
be its law. As a map of the T independent Gaussian vectors, Y_T has global
Lipschitz constant sqrt(C_T), where

    C_T=sigma^2 sum_(j=0)^(T-1) beta^(2j).

Indeed, synchronous trajectories differ by at most
sigma sum_t beta^(T-t)||Z_t-Z'_t||; Cauchy--Schwarz gives the assertion.
This is an actual Gaussian preparation, not an inference of concentration
from an abstract Poincare constant.

Evaluate the known candidate at zero. Minkowski and stationarity give

    B_b=(||b(0)||+sigma sqrt(d))/(1-beta),
    [E_pi_b ||Y||^2]^1/2 <= B_b.

Contraction from a stationary coupling then gives

    W2(nu_T,pi_b)<=e_b=beta^T B_b.                 (1)

Every independent preparation pays T candidate steps and Td Gaussian
scalars. It uses no original source values, which does not make it free.

## 3. Acquire two consequential quantities

At a freshly prepared X~nu_T acquire two independent smoothing noises and
the original values needed for

    D_X(G)=g(X+G)-b(X)-A G,
    r(X)=E[D_X(G)|X]=m_g(X)-b(X).

Let R_T^2=E_nu_T||r(X)||^2, S_T=E_nu_T tr Cov(g(X+G)-A G),
w=L+beta and v=L+a. With Y+=(D1+D2)/sqrt(2), Y-=(D1-D2)/sqrt(2),
conditional independence proves

    E||Y+||^2=2R_T^2+S_T,  E||Y-||^2=S_T.         (2)

For M independently prepared centers/pairs let F+,F- be their empirical RMS
norms. Valid global Lipschitz constants on all preparation/smoothing seeds are

    K+^2=[2C_T w^2+v^2]/M,
    K-^2=[2C_T L^2+v^2]/M.                       (3)

For plus, its center constant is at most sqrt(2)w, while each inner block
has constant v/sqrt(2). For minus, b(X) cancels, giving center constant
sqrt(2)L. Compose with the preparation map, telescope over independent
blocks, apply Cauchy--Schwarz, and take the normalized stacked norm. No
derivative or private source equation is needed.

Choose three positive tail budgets delta_+,delta_l,delta_u summing to delta,
and t_j=sqrt(2log(1/delta_j)). Gaussian concentration and Poincare imply
simultaneously, except with probability delta,

    U+=(F+ + K+ t_+)^2+K+^2 >= E||Y+||^2,
    L-=max(F- - K- t_l,0)^2 <= E||Y-||^2,
    U-=(F- + K- t_u)^2+K-^2 >= E||Y-||^2.

Hence acquire

    R_bar=sqrt(max((U+-L-)/2,0)),  S_bar=U-.       (4)

The tail events may be dependent; their union bound is sufficient. The
proof conditions on frozen training and then integrates over it. A supplied
norm-error warranty xi per observed D is handled by adding sqrt(2)xi to
each RMS used in an upper bound and subtracting it in the lower bound.
Candidate/source input errors must be included in a valid warranty or
handled separately. Source-call counts do not supply numerical accuracy.

## 4. Transfer to the intended invariant law

The residual r=m_g-b is w-Lipschitz. RMS coupling using (1) gives

    [E_pi_b||r||^2]^1/2 <= R_T+w e_b.

The standard invariant-law perturbation proof uses K_g's contraction:

    (1-L) W2(pi_b,pi_g)
       <= W2(pi_b K_b,pi_b K_g)
       <= [E_pi_b||r||^2]^1/2.

Thus the actual finite preparation has, on the acquired event,

    W2(nu_T,pi_g) <= A0
      = e_b+(R_bar+w e_b)/(1-L)
      = [R_bar+(1+beta)e_b]/(1-L).                (5)

Finite candidate burn-in is explicit. Merely being close to pi_b would not
allow dropping the residual's w e_b transfer term.

### Stronger finite-law defect certificate, adopted after focused review

The preceding bound is valid, but comparison with pi_b is unnecessary.
For any actually prepared law nu and any justified
kappa>=W2(nu,nu K_b), the ordinary contractive residual argument gives

    W2(nu,pi_g)
      <= W2(nu,nu K_b)+W2(nu K_b,nu K_g)
         +W2(nu K_g,pi_g K_g)
      <= kappa+R_nu+L W2(nu,pi_g).

Therefore

    W2(nu,pi_g)<=(kappa+R_nu)/(1-L).              (5a)

This elementary fixed-point estimate does not require existence of pi_b or
contraction of K_b. Those are one convenient way to construct a justified
defect bound; an unknown kappa cannot be treated as available for free.
For the actual finite candidate preparation in Section 2,

    W2(nu_T,nu_T K_b)
      =W2(delta_0 K_b^T,(delta_0 K_b)K_b^T)
      <=beta^T W2(delta_0,delta_0 K_b)
      =beta^T sqrt(||b(0)||^2+sigma^2 d)=:kappa_T.

Thus prefer the sharper fully constructed initial radius

    A0_finite=[R_bar+kappa_T]/(1-L).              (5b)

It uses the already paid b(0), no additional original values and no additional
confidence event. It never exceeds (5). Substitute A0_finite for A0 in all
subsequent noise-transfer and accuracy formulas. The representation has
become a prepared law, a justified one-step law defect and acquired residual
information. It no longer needs an intermediary candidate invariant law.
The Gaussian preparation and all statistical bounds remain unchanged.

## 5. Source correction at any subsequent requested accuracy

Use fresh original values in

    mhat_q(x)=q^-1 sum_j [g(x+G_j)-A G_j],
    Q_q(x,.)=Law(mhat_q(x)+sigma Z).

For fixed G_j the correction A G_j is independent of x. Therefore Q_q is
L-contractive, independently of b's complexity or beta, and its drift is
unbiased for m_g. Put s(x)^2=tr Cov(g(x+G)-A G). The centered L2 difference
at x,y is the centered version of g(x+G)-g(y+G), so s is L-Lipschitz.
Coupling nu_T to pi_g using (5) proves the integrated transfer

    [E_pi_g s^2]^1/2 <= sqrt(S_bar)+L A0.          (6)

The empirical noise has Gaussian Poincare constant at most v^2/q and trace
covariance s(x)^2/q. The accepted Gaussian-convolution inequality, transport
bound and mollification limit give

    W2(Q_q(x,.),K_g(x,.)) <= sqrt(log(2))v s(x)/(q sigma).

Initialize a production chain by a fresh independent nu_T preparation.
Integrating squared kernel errors under pi_g and contracting with Q_q gives

    e_0<=A0,
    e_t<=L e_(t-1)+c/q_t,
    c=sqrt(log(2))v[sqrt(S_bar)+L A0]/sigma.       (7)

One acquired event supports every deterministic schedule chosen from that
acquired record and every tolerance met by (7). It does not cover sampling
budgets or stopping rules selected from production outcomes. If A0 meets
the requested tolerance, return fresh nu_T samples directly. Otherwise pay
every original source correction. The measured average S_T has never been
replaced by a uniform statewise covariance bound.

T and the candidate preparation are frozen before validation. Changing T
changes the validated law; that change is not covered merely by the reuse
statement for later source-correction schedules.

## 6. Complete cost and limitations

Pay training for b,A and their justified global norm bounds. In addition to
one evaluation of b(0), M validation centers require M independent T-step
candidate preparations, M candidate residual values, 2M matrix actions and
exactly 2M original source values, each returning d scalars. N production
outputs require N fresh T-step candidate preparations and N sum_t q_t source
values/matrix actions. Each step pays its Gaussian preparation, arithmetic,
reading and storage. A dense A can cost O(d^2) per action; diagonal A need not.
Validation centers cannot be reused as fresh production seeds while silently
retaining the stated conditional law.

Learning a useful b,A for arbitrary sources remains open. A finite sample of
Jacobian norms does not establish global contraction of a learned candidate.
As beta approaches one, both preparation and C_T may become costly; as L
approaches one, (5) and (7) deteriorate. The theorem controls W2 consequences,
not relative rare tails or lifetime means. Its finite-bit and physical
instrument implementation still requires actual primitive warranties.

The new representation separates nonlinear candidate preparation, acquired
mean/noise information, and source correction whose contraction survives.
It removes the requirement of an exactly Gaussian candidate invariant law
from this interface. Concentration, control variates and perturbation theory
remain established ingredients, and no universal efficient discovery or
critical-dynamics theorem is claimed.

The original extension and the stronger finite-law defect proof received a
focused independent review in
../different_opening/NONLINEAR_CANDIDATE_AND_FINITE_DEFECT_REVIEW.md. The
uncached candidate-evaluation count includes the leading b(0):
1+M(T+1)+NT. Omitting that leading one requires actually reusing an already
counted evaluation.
