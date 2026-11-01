# Moving the Poisson source redistribution into the well

Status: new constructive candidate; independent review pending. This is separate
from every earlier freeze. It retains ORIGINAL constant-SPD Langevin dynamics;
the current below is a variational witness, NOT an imposed physical drift,
feedback protocol or new mobility tensor.

## 1. Actual model, target and inherited rigorous foundations

Use the already received ordinary model F(y,z)=v(y)U(z),
v(y)=1+kappa(1-y^2)^2, b=1/2, beta,kappa>0, U positive coercive homogeneous
quartic in m variables, alpha=m/4 integer>=4. Its actual transverse mobility
is a fixed SPD matrix M_z>=mu I, with unit longitudinal mobility and zero cross
mobility. In the raw consumer M_z is positive constant isotropic or diagonal.
A={y<=-b}, B={y>=b}, S={-b<y<b}. The target remains the ACTUAL mean

    T_A=E_{FULL Gibbs conditioned on A} tau_B.

No fixed-ray initialization, empirical membership, angular sampler, energy
Markov closure, conditional mixing bound or physical parameter accuracy is
supplied. The old constant-SPD theorem's global Lyapunov/nonexplosion,
reversibility and zero-resolvent/hitting-time join apply to this SAME process.
Nothing is changed physically to make a narrow interval possible.

Write q(y)=v(y)^(-alpha), M=int_A q, M_S=int_S q, eta=M_S/M and
R=int_-b^b v^alpha. To avoid a matrix/mass collision, the mobility is M_z while
M alone always denotes one basin mass. Homogeneous scaling yields normalized
fiber densities

    pi_s(z)=(beta s)^alpha exp(-beta s U(z))/Z_U,
    rho(y,z)=q(y)pi_v(y)(z),

where Z_U=int exp(-U) is finite but unknown and NEVER evaluated. A complete
positive quartic raw program supplies d_min>0 and U>=c||z||^4 with c=d_min/m.
The prior virial/coercivity estimate gives

    E_pi_s[z^T M_z^-1 z] <= mu^-1 sqrt(alpha/(beta c s)).  (1)

Define K=alpha/[8mu sqrt(beta d_min)]. The ordinary conditional-dilation
current has resistance correction K v'^2/v^(5/2), globally bounded by

    D_max=4alpha max(kappa,1)/[mu sqrt(beta d_min)],        (2)

and its integrated transition-slab correction is at most

    C_s=kappa/[2mu sqrt(beta d_min) a_b^(3/2)],
    a_b=v(b)=1+9kappa/16.                                (3)

These are already derived all-point moment/profile inequalities, not a mixing
or conditional Poisson oracle.

## 2. An explicit source-A current with no transverse slab flow

Let v_*=v(0)=1+kappa and J(y)=int_-infinity^y q(s)1_A(s)ds. On A set

    a(y)=max(v(y),v_*),

and on S set a(y)=v_*. Put j_y=J(y)pi_a(y). In A where v<v_*, define

    F_v(z)=-(z/4) int_v^(v_*) pi_s(z)/s ds,
    j_z=q(y) F_v(z).                                    (4)

In A where v>=v_*, set

    j_z=-J(y) v'(y) z pi_v(z)/(4v(y)).                    (5)

On S set j_z=0. These formulas specify the whole current from an analytic
homogeneous density family; no fiber PDE has been solved or supplied.

Indeed, differentiation of pi_s gives

    partial_s pi_s = div_z[z pi_s/(4s)],
    div_z F_v=pi_v-pi_(v_*).

Where v<v_*, a is constant and partial_y j_y=q pi_(v_*), so (4) gives
partial_y j_y+div_z j_z=q pi_v. Where v>=v_*, ordinary conditional continuity
cancels the y-density derivative and gives the same source. In S, J=M and a=v_*
are constant, so divergence is zero. Thus throughout the killed domain

    div j=rho 1_A.                                     (6)

The longitudinal component is continuous at v=v_* and y=-b. The transverse
component may jump across these y-interfaces, but its divergence differentiates
in z, not y. Hence there is no delta source: the normal component across a
constant-y interface is j_y and it matches. This also verifies the distributional
source identity without pretending the piecewise witness is globally smooth.
Smoothing/exhaustion in the energy form or direct H(div) integration is legitimate
once the finite resistance below is established. There is no singular origin.

The interval v<v_* within A is exactly -sqrt(2)<y<-b, independent of kappa.
All fiber integrations have coercive exponential tails. The current is a dual
mathematical witness; its uncomputed common Z_U cancels analytically between
current norms and basin mass, not through an assumed normalizer oracle.

## 3. Exact slab resistance and explicit well redistribution cost

On S the current has only its y-component M pi_(v_*). The normalized density
ratio is exact:

    pi_s^2/pi_v = [s^2/(v(2s-v))]^alpha pi_(2s-v),

whenever 2s-v>0. Therefore the whole transition contribution is

    beta M^2 R_plus,
    R_plus=int_-b^b [v_*^2/(2v_*-v(y))]^alpha dy.         (7)

R_plus is ONE extra monotone scalar integral. Its denominator is at least v_*>0
on the slab. No transverse transport is paid in the rare transition region.
Also R_plus>=R since v_*^2/(2v_*-v)-v=(v_*-v)^2/(2v_*-v)>=0.

For the source redistribution (4), Cauchy in s and (1) give, for1<=v<=v_*,

 q int F_v^T M_z^-1 F_v/pi_v dz
 <= K(v_*-v) int_v^(v_*) [s^2 sqrt(2s-v)]^-1
                     [s^2/(v^2(2s-v))]^alpha ds.

The function s^2/(2s-v) increases for s>=v. Also
v_*^2/[v^2(2v_*-v)] decreases on1<=v<=v_*, since its logarithmic derivative
is 1/(2v_*-v)-2/v<0. Hence, with

    G_1=v_*^2/(2v_*-1),

and v_*-v<=kappa, s>=v>=1, the preceding norm is at most

    K kappa^2 G_1^alpha.                                (8)

The redistribution interval has length sqrt(2)-b<1. Its ENTIRE transverse
resistance is consequently at most beta K kappa^2 G_1^alpha. The exact
homotopy integral in (4) need never be numerically evaluated: (8) pays its
complete norm analytically. This is the critical acquired replacement for a
high-dimensional fiber Poisson solve.

## 4. Full longitudinal basin and infinite-tail bounds

Set delta=1/alpha<=1/4 and

    G_b=v_*^2/(2v_*-a_b).

For x=-y in[b,1+delta], J(-x)<=M and v(x)<=a_b, because the profile increases
away from its well at1 and v(1+delta)<=a_b. Thus the longitudinal resistance
there is at most

    beta M^2 (1+delta-b) G_b^alpha.                       (9)

For x>1, convexity and v'>0 imply the full cumulative mass bound

    J(-x)=int_x^infinity v(t)^(-alpha)dt
          <=v(x)^(1-alpha)/[(alpha-1)v'(x)],
    v'(x)>=8kappa(x-1).

For x in[1+delta,sqrt(2)], its interval length is<1/2, v<=v_* and v'>=8kappa delta.
Combining with the exact density-ratio norm gives the longitudinal contribution

    <= beta v_*^2 G_1^alpha/
          [128 kappa^2 (alpha-1)^2 delta^2].             (10)

For x>=sqrt(2), the current is the old conditional current. Since alpha>=4,
v^(2-alpha)<=1 and the cumulative bound gives a longitudinal integrand at most
1/[64kappa^2(alpha-1)^2(x-1)^2]. Extending this bound down to x=5/4 is conservative
and yields a total far resistance, including (2), at most

    beta(1+D_max)/[16kappa^2(alpha-1)^2].                 (11)

All tails are integrated to infinity. The split at sqrt(2) is used only in the
proof; the finite backend needs no algebraic irrational cutoff or sampled tail.
The chosen rational extensions/split estimates give the displayed constants.

Combining(7)--(11) proves the actual source form Q_A<=B_new, where

 B_new=beta { M^2 R_plus + M^2(1+delta-b)G_b^alpha
       + [v_*^2/(128kappa^2(alpha-1)^2 delta^2)
                                      +K kappa^2]G_1^alpha
       +(1+D_max)/(16kappa^2(alpha-1)^2) }.               (12)

## 5. A SEPARATE source-S current, not an invalid inherited comparison

The new source-A current does NOT automatically give Q_S<=eta^2 B_new.
For S instead retain the old conditional current

    j_S=J_S(y)pi_v(y)(1,-v'(y)z/[4v(y)]),
    J_S(y)=int_-infinity^y q(s)1_S(s)ds.

It vanishes left of the slab, and J_S<=M_S on the slab. Using(3) only there,

    Q_S<=B_S=beta M_S^2 R(1+C_s).                        (13)

This proof is separate from (12), with its own actual divergence and energy.
It avoids importing the much larger old A-basin estimate unnecessarily.
Positivity and zero-resolvent Cauchy then give

    T_A <= [B_new+sqrt(B_new B_S)]/M,
    T_A >= T0=beta M R.                                 (14)

Let U_A=B_new/M. A rational outward-friendly sufficient mean upper is

    T_A <= (1+eta/2)U_A +(eta/2)T0(1+C_s),               (15)

by2sqrt(ab)<=a+b. The upper is not capacity inversion. The lower follows from
the scalar Poisson source trial, retaining the exact full Gibbs|A initial law.
Finite source energies first earn the finite mean through the existing killed
resolvent identity; no spectral gap or arbitrary-start moment is assumed.

At beta=kappa=d_min=mu=1, G_1=4/3 and G_b=64/39, both strictly below v_*=2.
Thus all explicitly bounded well redistribution costs grow exponentially more
slowly than the principal slab resistance. The unavoidable supplied numerical
integral R_plus/R approaches one at large alpha. This is a candidate route to
sub-one-percent full MFPT accuracy for the ORIGINAL UNIT mobility, not a change
to mu64 or an implicit control intervention. Actual finite acceptance still
requires paid outward arithmetic and the original total-width check.

## 6. Optional distribution interface: distinct source bounds must stay distinct

The separately frozen root trial/separate-current spectral theorem can use
B_new and B_S, not the old same-current hypothesis. With b_new=B_new/(M T0),
its spectral defect is bounded by

    (sqrt(b_new)+eta sqrt(1+C_s))^2-1
    <= (1+eta)[b_new+eta(1+C_s)]-1.                     (16)

The initial-law comparison eta+sqrt(eta(1+eta)) is unchanged. Finite reference-
rate uncertainty and optional CDF queries require their separately received
arithmetic corollary. Equation(16) is NOT permission to reuse a previous
wrapper's epsilon formula whose source-current hypothesis differs. A new
consumer must bind this source split explicitly. Relative extreme tails,
exponential moments and arbitrary-start laws remain excluded.

## 7. Acquisition, comparisons and boundaries

Only M,R,R_plus and ordinary explicit powers/roots are needed. The complete raw
quartic/mobility program supplies homogeneity, coercivity, beta,kappa,alpha,mu;
all such receiving/read costs remain. The current's favorable density is chosen
analytically as pi_(max(v,v_*)); it is not a learned oracle or an uncharged
precomputed optimal flux. Physical probability conservation and the full
inverse-mobility cost were checked, including the discontinuity interfaces.

The mechanism combines ordinary conditional dilation, mixtures/density ratios,
Poisson-current duality, source Cauchy and scalar quadrature. Its parallel slab
resistance is the same scalar R_plus already earned in the earlier finite-Jensen
conductance construction. That prior operation did not by itself establish this
full Gibbs|A mean: the new hard step is explicit finite-cost source redistribution
and the separate S-current join. An ordinary implementation given this derived
witness reproduces the theorem. No historical priority or universal algorithmic
separation is claimed; strong variational, verified PDE, averaging and simulation
methods receive the same complete model and all analytic certificates.

As mu->0 the well corrections still grow like1/mu. No assertion of a uniform
finite mean at zero mobility is made, and the earlier latency-divergence example
is not contradicted. Coefficient/model error, incomplete microscopic programs,
full Gibbs preparation and real implementation remain substantive unearned
premises. The flow is a proof of a prediction, not a demonstrated physical device.
