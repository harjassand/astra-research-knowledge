# Complete equilibrium records of a continuous physical port do not determine its nonlinear controlled response

29 October 2026. New complementary construction by the port-information agent.
Ordinary proof below. This is an exact native reversible SWITCHING DIFFUSION:
one continuous observed coordinate and three unobserved internal states. It is
not claimed to be an all-continuous hidden diffusion. Temperature, mobility,
equilibrium preparation and conjugate potential control are the same on both
sides. There are no rare-event or enormous-timescale assumptions.

## 1. Consequence

Two equilibrium models below have:

* exactly the same COMPLETE stationary continuous-coordinate path law;
* the same calibrated scalar mobility and thermal diffusion coefficient;
* the same observed equilibrium law after every common static potential bias;
* different finite-time response to the SAME bounded force from an observed
  potential, beginning at quadratic response order.

Thus the independent white thermal noise acting on a visible coordinate does
not, by itself, repair the missing intervention information. Harmonic reciprocal
bath closure in the companion note is a substantive additional source promise.

## 2. Explicit native equilibrium construction

Let x be a circle of length 2pi, let i in {1,2,3} be an unobserved internal state,
and fix temperature tau=1 and mobility one. Define

    O = (1/3) [[2,-1,2],[-1,2,2],[2,2,-1]],
    a = (1,2,4)^T,        a_tilde=Oa=(8,11,2)^T/3,
    epsilon=1/10,        c=10,
    psi_i(x)=1+epsilon a_i cos x,
    psi_tilde(x)=O psi(x)=1+epsilon a_tilde_i cos x.

O^T=O, O^2=I and O1=1. Every psi_i is >=3/5 and every psi_tilde_i is >=19/30.
Introduce the symmetric matrix potential

    W(x) = -c 11^T + diag(D_i(x)),
    D_i(x) = [psi_i''(x)+c sum_j psi_j(x)]/psi_i(x),
    H = -partial_x^2 I + W(x).

By construction H psi=0. Define W_tilde=O W O and H_tilde=O H O. Then
H_tilde psi_tilde=0. All off-diagonal entries of W are -10. Moreover

    D_i(x)-30 = epsilon (70-31a_i)cos x/[1+epsilon a_i cos x],
    max_i,x |D_i(x)-30| <=9.

Since O fixes 1, W_tilde=30I-10 11^T+O diag(D_i-30)O. Every off-diagonal entry
of the last perturbation has magnitude <=9, so W_tilde_ij<=-1 for i!=j.
This proves, uniformly in x, strictly positive jump rates in BOTH constructions.

The two Markov generators are the ground-state transforms

    (Lf)_i = psi_i^-1 [-H(psi f)]_i
           = f_i'' + b_i(x) f_i'
                            +sum_(j!=i) q_ij(x)(f_j-f_i),
    b_i=2psi_i'/psi_i,       q_ij=-W_ij psi_j/psi_i.           (1)

Use tildes for the second model. Coefficients are smooth and bounded on the
compact circle, the scalar diffusion coefficient is the same sqrt(2), and all
internal jump rates are strictly positive and bounded. Thus each is a standard
nonexplosive uniformly elliptic switching diffusion with a unique equilibrium.

Let

    Z=int_0^(2pi) sum_i psi_i(x)^2 dx = pi(6+21epsilon^2).

Their stationary joint densities are rho_i=psi_i^2/Z and
rho_tilde_i=psi_tilde_i^2/Z. Diffusion detailed balance follows from b_i=partial_x
log rho_i. Jump detailed balance follows from

    rho_i q_ij = -W_ij psi_i psi_j/Z = rho_j q_ji.

These are thermal potentials U_i(x)=-2log psi_i(x), and correspondingly for the
second source. The symmetric rate prefactors -W_ij are positive. Each source
therefore has ordinary equilibrium thermodynamic interpretation with all
variables even under reversal and zero baseline entropy production.

## 3. Exact equality of every baseline observed path law

For any scalar bounded observable f(x), its multiplication operator M_f commutes
with the constant internal rotation O. For 0=t0<t1<...<tm, the stationary
observed correlation is

    E_rho product_k f_k(X_(t_k))
       = Z^-1 <psi, M_f0 exp[-(t1-t0)H] M_f1 ...
                               exp[-(tm-t_(m-1))H] M_fm psi>_(L2(dx)). (2)

Insert O^2 between every factor. Since psi_tilde=Opsi and H_tilde=OHO, expression
(2) equals the tilded expression exactly. Orthogonality also gives
sum_i psi_i^2=sum_i psi_tilde_i^2 pointwise, so the normalization agrees.
All finite-dimensional observed distributions agree; continuity of X gives
equality of the complete path measures, including all exact path statistics and
any number of baseline samples. Hidden states themselves are not observed.

This is a unitary statistical equivalence, not a hidden-state permutation.
The rotation is not a positive coordinate relabeling. Both ORIGINAL and ROTATED
generators nevertheless have genuine positive Markov rates, as proved above.

## 4. One actual common conjugate potential operation

Choose the visible potential v(x)=cos x. Apply external energy -alpha v(x),
the same operation in both sources. It changes every internal-state potential
by the SAME scalar function and produces bounded force

    u(x)=alpha v'(x)=-alpha sin x,
    L_alpha=L+alpha D,             D=v'(x)partial_x.          (3)

The internal jump rates remain unchanged: at a fixed x the energy difference
between any two internal states is unchanged. A symmetric transition barrier
receives the same external potential shift, so its detailed-balance ratio and
rate are unchanged. This specifies the actuation mechanism, rather than choosing
different hidden implementations of the nominal command after the fact.

Each biased stationary law is proportional to rho_i(x)exp(alpha v(x)). Hence
the biased observed equilibrium marginal is proportional to

    exp(alpha cos x) sum_i psi_i(x)^2,

which is exactly identical for the two sources for EVERY alpha. Static bias
experiments therefore do not resolve this ambiguity either.

The sources are both initially in their baseline equilibrium. We now prove that
their finite-time controlled expectations of the same bounded output f(x)=cos x
are different for every nonzero alpha at sufficiently short positive time.

## 5. Explicit nonlinear-response separation

Write nu(x)=sum_i psi_i^2/Z for the common observed density, and let an overbar
denote conditional averaging over internal state given x. The following two
conditional quantities are invariant under the constant orthogonal rotation:

    (sum_i psi_i^2) b_bar = 2 sum_i psi_i psi_i',
    (sum_i psi_i^2) (b')_bar
                               =2sum_i(psi_i psi_i''-psi_i'^2).        (4)

The second spatial derivative is different:

    (sum_i psi_i^2) (b'')_bar
      =2sum_i[psi_i psi_i'''-3psi_i'psi_i''+2psi_i'^3/psi_i].          (5)

The first two sums in (5) are invariant, but the last is not. With
t=epsilon cos x, define

    DeltaS(t)=sum_i a_i^3/(1+t a_i)
                        -sum_i a_tilde_i^3/(1+t a_tilde_i).

Exact rational algebra gives

    DeltaS(t) = [(40/27)(3+14t+14t^2)]
                   / [product_i(1+t a_i) product_i(1+t a_tilde_i)].    (6)

For |t|<=1/10 every denominator is positive, the numerator is at least 116/45,
and the denominator is at most 479864/140625. Thus

    DeltaS(t)>=90625/119966>0.                                      (7)

Equations (5)--(6) imply

    nu(x)[(b'')_bar-(b_tilde'')_bar]
                       = -4epsilon^3 sin^3(x) DeltaS(epsilon cos x)/Z. (8)

To locate the effect in the response, use equilibrium reversibility and the
diffusion product rule. Since v has no internal-state dependence,

    E_rho[Dg] = -E_rho[v Lg]                                      (9)

for every smooth vector function g. This is integration by parts, or the
Dirichlet-form identity for the continuous coordinate.

Let F_alpha(t)=E_rho f(X_t) under (3), and similarly F_tilde. Their derivatives
at t=0 are E_rho[(L+alpha D)^k f]. For k<=2 all terms agree: the terms with
leftmost L vanish by stationarity; the remaining linear terms are reduced by
(9) to baseline observed correlations and their derivatives; purely D terms are
functions of x and use the same nu.

At k=3,

    E_rho[(L+alpha D)^3 f]
       =alpha E[D L^2 f]
        +alpha^2 {E[D L Df]+E[D^2 Lf]}+alpha^3 E[D^3f].       (10)

The linear and cubic terms agree by the same reasoning. E[D L Df] agrees because
Df is again a scalar observed function and (9) makes it a baseline correlation.
Expanding D^2 Lf, all terms involving b or b' agree by (4). The ONLY remaining
difference is

    C=int nu(x) v'(x)^2 f'(x)
                         [(b'')_bar-(b_tilde'')_bar]dx.

For v=f=cos x, (8) gives

    C = (4epsilon^3/Z) int_0^(2pi) sin^6(x) DeltaS(epsilon cos x)dx
      >= [5epsilon^3/(2(6+21epsilon^2))]*(90625/119966)
       = 90625/297995544 >0.                                   (11)

The exact rational lower bound is approximately 0.0003041152857. Therefore

    F_alpha(t)-F_tilde_alpha(t) = alpha^2 C t^3/6 + O(t^4).      (12)

All coefficients are smooth on a compact state space, so this short-time
expansion has an ordinary uniform remainder bound for each fixed alpha. Thus
for every alpha!=0 the two finite-time endpoint laws differ for sufficiently
small t>0. Since |f|<=1, their endpoint TV is at least half the absolute mean
difference. No fine-path classifier, hidden-state intervention or rare event is
needed to expose the distinction once the common physical bias is applied.

## 6. Scope and conceptual obstruction

The baseline record supplies a Hilbert-space/semigroup equivalence. The control
needs pointwise multiplication of hidden functions, which the orthogonal
rotation does not preserve. In symmetrized coordinates,

    psi D psi^-1 = v' partial_x - v' diag(psi_i'/psi_i).

The derivative commutes with the constant rotation but the final diagonal
operator does not. Its missing multiplication is exactly the obstruction.
The above example carries that obstruction into a continuous, directly
thermalized observable with a specified conjugate potential operation.

The construction does NOT prove a counterexample with every hidden coordinate
continuous and purely diffusive. It DOES refute a general claim covering
reversible hidden internal kinetics, a common physical model of conformational
or chemical-state switches, even when the observed coordinate is fully resolved.
No claim about a particular material or native specimen is made.

This is independent new source science, not a re-audit of unchanged Astra
predecessors. The finite-state similarity mechanism was reached independently
by root and this agent; this note develops its continuous-port consequence.
Historical priority has not been established. It fits the primary warning from
coarse-grained nonlinear-response theory: equilibrium fluctuation information
does not automatically supply the time-symmetric intervention activity.
