# Independent theorem-only review: original constant-SPD Gibbs-conditioned MFPT

## Verdict, exact input and exclusions

**PASS, theorem-only**, for `constant_spd_mfpt_20261031/POISSON_CURRENT_CONSTANT_SPD_MFPT.md`, 11,025 bytes, SHA256 **`bf9e83e1f39f25758dc02b10a06d06a955b98e61de172f633ba5d4f341a7d8e0`**. Its immutable snapshot is `received_candidate.md` in this receipt directory.

This accepts the full-state dilation source current, inverse-mobility/virial/Jensen estimate, zero-resolvent/initial-law join, complete tails, and explicit quartic formula (12) for the stated original **constant-SPD Langevin** model. No source correction was required. It is separate from the engineered radial-gain MFPT whole acceptance.

No candidate numerical consumer was imported, run or accepted. A code freeze appeared while this theorem review was underway; its presence does not expand this receipt to code, square-root arithmetic, saved numerical widths, parsers or receiving. In particular the reported prototype approximately0.00478 width is not a numerical certificate established here. The exact analytic unit-parameter slab overhead0.004 at mu64 is verified, but it excludes other positive contributions and is not by itself a full interval-width claim.

The initial law is the **full conditional Gibbs law on A**. Matching only (Y,U), choosing a fixed ray, or using a small-total-variation approximate preparation is not an accepted substitute. There is no assertion of energy Markov closure, identical actual means across angular models, physical field acquisition, or new tensor actuation.

## 1. Actual model, conservative diffusion and invariant measure

The actual equations have potential F=v(y)U(z), longitudinal mobility1, zero cross covariance, and a fixed finite constant SPD transverse matrix M with acquired floor M>=mu I>0. Unlike the earlier engineered lift, there is no singular radial mobility or origin boundary to choose. The polynomial coefficients are smooth/local-Lipschitz and the fixed noise is elliptic.

Homogeneity gives z.grad U=pU. For K=1+kappa/p and V=1+y^2+K z^T M^-1 z,

    LV=2(1+Km)/beta-2[yv'+Kp v]U.

With t=y^2, the all-point coefficient has the nonnegative decomposition

    yv'+(p+kappa)v-p
      =kappa(2t-1)^2+(p+kappa)kappa(1-t)^2 >=0.

Therefore LV<=2(1+Km)/beta-2pU. V is proper for every fixed finite SPD matrix, so localization proves nonexplosion. No angular convexity or mixing estimate is required, and no uniform conditioning bound over all such M is inferred.

Coercivity ensures Z_U=int exp(-U) is finite. Spatial scaling gives Z(beta v)=(beta v)^(-alpha) Z_U, alpha=m/p. Thus the conditional fiber law is

    pi_y(z)=(beta v)^alpha exp(-beta v U(z))/Z_U,

and the y marginal is proportional to q=v^-alpha. It is integrable for alpha>1/4. Integration by parts gives the symmetric form of the actual conservative elliptic process; finite Gibbs mass then supplies invariance. No homogeneous partition constant is evaluated numerically or assumed to reveal angular relaxation.

The exact full-Gibbs initialization in the source is essential. Without exact energy closure, different points on the same energy level can have different future y-hitting behavior. The example U=z1^4+16z2^4+z3^4+z4^4 at e1 and e2/2 has equal U=1 but gradient-square16 versus64 and Euclidean energy drift -4 versus-16 at unit beta,v. The prior lift's fixed-ray permission cannot transfer.

## 2. The full-z current and the correct inverse mobility

For f=1_A or1_S, set J_f(y)=integral_-infinity^y q(s)f(s)ds and

    w(y,z)=-v'(y)z/[p v(y)],
    j_f=J_f pi_y (1,w).

The continuity identity holds pointwise in the full state. In logarithmic form,

    partial_y log pi_y=alpha v'/v-beta v'U,
    div_z w=-m v'/(p v),
    w.grad_z log pi_y=beta v' z.grad U/p=beta v'U.

Since alpha=m/p, their sum is zero. Consequently div j_f=rho f. This is a full-state current, not an assumed quotient diffusion or an angularly averaged approximate drift. The formula uses U and homogeneity directly; no Poisson solution, committor, conditional sample or reconstructed angular law is an input.

The form is

    E(h)=beta^-1 integral rho [h_y^2+grad_z h^T M grad_z h].

Weighted current Cauchy therefore gives

    Q_f<=D_f=beta integral J_f^2/q [1+d(y)]dy,
    d(y)=(v'/(p v))^2 E_pi_y[z^T M^-1 z].

The inverse mobility is the actual constant M^-1. No gamma*u denominator from the engineered model is reused. The beta factor in D_f is correct for this form.

From M^-1<=mu^-1 I and U>=c||z||^p,

    E[z^T M^-1 z] <=mu^-1 c^(-2/p) E[U^(2/p)].

The exponent2/p lies in (0,1], so Jensen goes in the required upper-bound direction. Differentiating Z(beta v), or a coercively justified radial virial integration, gives E U=alpha/(beta v). Hence

    d(y)<= C v'^2/v^(2+2/p),
    C=(alpha/(beta c))^(2/p)/(mu p^2).

This uses exact homogeneity, a supplied coercivity lower bound and the actual mobility floor. Neither a Poincare constant nor angular equilibration is hidden in the argument. A small mu legitimately worsens this sufficient bound; changing mu is changing known model information, not changing a numerical tolerance.

## 3. Actual mean via sources, including global tails

The killed full-state resolvent on Omega={y<b} has, for lambda>0,

    <1_A,R_lambda 1_Omega>
      =M_A E_A[integral_0^tau_B exp(-lambda t)dt].

The diagonal source variational formula and positive-resolvent Cauchy give `Q_A<=D_A`, `Q_S<=D_S`, and `0<=Q_AS<=sqrt(Q_A Q_S)`. Scalar trials h'=-beta J_f/q give `L_f=beta integral J_f^2/q<=Q_f` by finite-energy truncation, not by assuming an L2 inverse at zero.

Left of the slab J_S=0, while on the slab J_A=M_A and J_S<=M_S. Therefore `D_S<=(M_S/M_A)^2 D_A`. Once finite current energies are established, monotone convergence earns

    M_A T_A=Q_A+Q_AS<infinity,
    L_A/M_A<=T_A<=(1+M_S/M_A)D_A/M_A.

The occupation cross term is included. This is not capacity inversion or a mean assumed finite before the argument.

For x=-y large, q=Theta(x^-4alpha) and M(x)=O(x^(1-4alpha)), so the longitudinal source energy density is O(x^(2-4alpha)). The new full-z correction decays as

    v'^2/v^(2+2/p)=O(x^(-2-8/p)).

Thus alpha>3/4 suffices for the entire current energy and source tail. The quartic finite backend's alpha>=4 is stronger. On finite y intervals, coercivity controls all fiber polynomial moments and fiber boundary terms. Compact-domain exhaustion and zero-target-trace form closure are legitimate for the conservative process.

The scalar source trial grows quadratically on the left. Its energy and source pairings converge under the same alpha>3/4 condition, while its square need not be integrable near that threshold. Value truncation first, then compact y/z approximation, and taking lambda down before removing the finite test approximation avoid an invalid L2 assumption. There is no spectral-gap or bounded-domain substitute hidden here.

## 4. Quartic coefficients and all-point bounds

For the stated positive-coefficient aligned quartic grammar,

    U>=d_min sum z_i^4 >=(d_min/m)||z||^4.

The second inequality follows exactly from

    m sum z_i^4-(sum z_i^2)^2=sum_(i<j)(z_i^2-z_j^2)^2>=0.

All nonnegative interactions may be retained without estimating their mixing rate. Strictly positive listed coefficients and all pure terms are necessary sufficient-parser premises; this is not arbitrary quartic positivity recognition.

Putting p=4, c=d_min/m and alpha=m/4 in the general coefficient yields exactly

    C=alpha/[8 mu sqrt(beta d_min)].

On [0,b], W=v^alpha decreases, v>=a=1+9kappa/16, and -v'<=4kappa y. Thus

    C v'^2 v^(alpha-5/2)
      =(C/alpha)[-v'/v^(3/2)](-W')
      <=[4kappa C/(alpha a^(3/2))]y(-W').

Integration by parts gives integral y(-W')=integral W-bW(b)<=integral W. Evenness gives the full slab factor

    C_s=kappa/[2 mu sqrt(beta d_min) a^(3/2)].

No factor of two is missing and the dimension cancels because C is proportional to alpha. At beta=kappa=d_min=1 this is exactly32/(125mu), hence0.004 at actual mu64.

The slab estimate is not reused in the basin. For any real y, x=|y^2-1| satisfies y^2<=1+x. With r=sqrt(kappa)x,

    v'^2/v^(5/2)
      <=16[kappa r^2+sqrt(kappa)r^3]/(1+r^2)^(5/2).

Both r^2/(1+r^2)^(5/2) and r^3/(1+r^2)^(5/2) are at most1. Also kappa+sqrt(kappa)<=2max(kappa,1). Hence the global correction is at most

    D_max=32max(kappa,1)C
         =4alpha max(kappa,1)/[mu sqrt(beta d_min)].

This bound holds over the entire basin and both tails, not just a checked numerical grid.

## 5. Explicit formula (12)

For integer alpha>=4, let delta=1/alpha, c1=v(1+delta),

    S0=(1-b)a^alpha+delta c1^alpha,
    W_far=1/[64kappa^2(alpha-1)^2 delta].

On [b,1], v<=a; on [1,1+delta], v<=c1<=a, and M(x)<=M. This gives near-basin longitudinal source resistance at most M^2 S0. For x>1, convexity gives

    M(x)<=v(x)^(1-alpha)/[(alpha-1)v'(x)],
    v'(x)>=8kappa(x-1),

and v>=1 then bounds the far resistance by W_far. All cumulative tails have been eliminated by explicit global inequalities; none is a supplied oracle. Finally M_S<=a^-alpha.

The slab contribution to D_A is at most beta M^2 R(1+C_s), and the entire basin contribution is at most beta(1+D_max)(M^2 S0+W_far). Dividing by M and applying the source multiplier gives EXACTLY

    T_low=beta M R,
    T_high=(1+a^-alpha/M) * {
      beta M R(1+C_s)
      +beta(1+D_max)[M S0+W_far/M] }.

M is one basin mass and R is the complete slab. The positive basin resistance and A/S occupation correction remain present. All beta and mobility factors are consistent with the actual constant-SPD form. T_low is a scalar Poisson lower contribution; equality with the actual mean is not claimed.

The same formula is a uniform outer interval for all admitted U and M with matching m,beta,kappa,d_min and floor mu. It does not make their actual means equal, does not make (Y,U) Markov, and does not remove the full-Gibbs initial-law premise. A sufficient width miss is not a physical lower bound on achievable accuracy.

## 6. Independent checks, comparisons and next receiving boundary

`check_theorem.py` imports **no candidate receiver**. It passed **6,175 exact checks**, including symbolic full-z continuity and inverse-M norm identities for degree2/4/6 examples; global Lyapunov and quartic sum-square decompositions; exact C,C_s,D_max specialization; source-to-formula-(12) assembly; tail exponents; the same-energy nonclosure counterexample; and rational representative checks of near/far/slab/global inequalities. The general inequalities are proved above, not inferred from representatives.

The original constant-SPD process is a meaningful different model boundary: it requires no engineered radial tensor, but instead uses a full-state current, actual mobility floor and full-Gibbs initialization. Ordinary variational/current methods with this exact derivation reproduce the result. Gaussian radial reduction remains a strong simpler comparator, and verified elliptic Poisson/barrier solvers get the same raw model and analytic certificates. No source-priority or formal computational separation is accepted. The independently reviewed source is self-contained, so no new external retrieval or blocked-source retry was needed.

A future executable must separately receive the complete positive quartic program, actual isotropic/diagonal mobility floor, coercivity, fixed initialization, exact M/R with infinite tails, outward square-root constants, all budget/precision/refusal domains, and original external task/total width. None is accepted from this theorem-only receipt or from the previous radial code. Physical calibration, angular Gibbs preparation and weighted preparation-error control remain outside the result.

All source and previous audit files remain unchanged. This receipt is bound separately by `AUDIT_SHA256.json`.
