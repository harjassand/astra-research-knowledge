# Finite-noise de-embedding from an acquired positive reference

28 October 2026. New continuation of the scoped N1082/N1089 construction.
This is a proof under the same warranted fixed affine rank-one SPD source,
calibrated scalar-observation, finite actuation, and stability premises. It
does not establish those physical premises from finite fitting.

## 1. Reference acquisition and original domain

The physical source is

    Q(u)=Q0+sum_i u_i v_i v_i^T,   Q0>0,
    Z(u)=e^T Q(u)^-1 e,           R(u)=r0+1/Z(u),
    u>=0, sum u<=Delta.

Choose an actual feasible reference w>=0 with sum w<Delta. All acquisition
commands are w+x with x>=0 and sum x<=Delta-sum w. Apply the existing
interval singleton/pair/landmark acquisition to these increments, including
the calibration and preparation allowance of each actual nominal command.
If the singleton positivity tests fail, this theorem returns unresolved; it
does not classify the control as irrelevant.

When acquisition succeeds it supplies the relative baseline z=Z(w), positive
P_i=(e^T Q(w)^-1 v_i)^2, intervals Tii and Sii, the PSD nominal Sstar, and
the existing representation

    S=S0+E,  S0>=0, E>=0, Eii<=rho_i,
    |S0_ij-Sstar_ij|<=beta_ij.

Here S is the centered Gram at Q(w). Denote its physical Gram factors by
s_i, and put t_i=Q(w)^-1/2 v_i/h_i, h_i=e^TQ(w)^-1v_i. Then

    t_i=b/z+s_i,  b=Q(w)^-1/2 e,  b^T s_i=0,
    ||t_i||^2=Tii,  ||s_i||^2=Sii.

No factor or sign h_i needs to be observed.

## 2. An acquired uniform coercivity margin

Calculate from acquired interval endpoints

    a = sum_i w_i P_i^+ Tii^+.

If a<1, let gamma=1-a. Since

    Q(w)^-1/2 Q0 Q(w)^-1/2
      = I-sum_i w_i P_i t_i t_i^T >= (1-a)I,

every original-domain u>=0 satisfies

    Q(u) >= gamma Q(w).                             (1)

Thus the entire original simplex, including u=0 and coordinate faces, has
a scalar-acquired stability margin. Negative quantities below are
computational displacements, not negative physical actuations.

A separately warranted bound tau_i>=v_i^TQ0^-1v_i can alternatively give
gamma>=1/(1+sum_i w_i tau_i), because Q(w)<=(1+sum w_i tau_i)Q0.
This optional bound is not inferred from a few responses. The implemented
construction uses the acquired check a<1.

For the nominal centered Gram require the independently computable check

    gamma_star=1-sum_i w_i P_i^+ Sstar_ii > 0.        (2)

For every d_i=(u_i-w_i)P_i and every choice of P within its interval box,
the nominal factor operator I+sum_i d_i sstar_i sstar_i^T is then at least
gamma_star I. The true centered operator is at least gamma I by restriction
of (1). These checks are sufficient, not necessary; failure retains UNKNOWN.

## 3. Signed resolvents

For one original command u set x=u-w, d_i=x_i P_i. On nonzero coordinates,
let J=diag(sign d_i), A=diag(sqrt(|d_i|)), y=A*1 and K=A*S*A. The exact
centered response is

    F(d,S)=y^T (J+K)^-1 y,
    Z(u)=z^2/(z+F(d,S)).                            (3)

The formula is the signed Woodbury identity; zero doses are omitted.
If Y has columns sqrt(|d_i|)s_i, then

    (J+Y^TY)^-1 = J-JY^T(I+YJY^T)^-1YJ.

Consequently

    ||(J+K)^-1|| <= 1+||K||/gamma.                 (4)

This explicitly replaces the nonnegative-update contraction used previously.
It also shows why exact signed algebra alone did not justify the old noisy
certificate.

Use acquired upper weights a_i=|x_i|P_i^+, and define

    L=sum_i a_i,
    kf=sum_ij sqrt(a_i) beta_ij sqrt(a_j),
    ke=sum_i a_i rho_i,  kappa=kf+ke,
    B =1+(sum_i a_i Sii^+)/gamma,
    Bstar=1+(sum_i a_i Sstar_ii)/gamma_star.

The scaled Gram perturbation has norm at most kappa. The resolvent identity
and (4) therefore give, at the SAME actual d,

    |F(d,S)-F(d,Sstar)| <= L*B*Bstar*kappa.          (5)

All quantities on the right are acquired and computable. This is a
two-sided error bound; the earlier one-sided PSD remainder improvement does
not transfer automatically to signed updates.

## 4. Singleton-scale intervals and positive denominator

For each i take [d_i^-,d_i^+] to be the ordered interval x_i[P_i^-,P_i^+].
On the entire box, (2) ensures positive nominal centered operator and

    partial F(d,Sstar)/partial d_i = kstar_i(d)^2 >= 0.

Thus the nominal low-rank formula at d^- and d^+ bounds all scale choices.
Adding (5) gives [FL,FU] containing the true F. The nominal formula uses
only the retained r-by-r matrix

    H=Wmid+sum_i d_i c_i c_i^T,
    Fstar=sum_i d_i-q^T H^-1 q,  q=sum_i d_i c_i.

The denominator is protected by the physical acquired margin: (1) implies
Z(u)<=z/gamma and hence z+F>=gamma*z. For z in[zL,zU], take

    denominator_lower=max(zL+FL, gamma*zL),
    denominator_upper=zU+FU.

Ordinary interval division of [zL^2,zU^2] by this positive interval is sound.
Unlike the positive-increment case, z^2/(z+F) need not be increasing in z
through an arbitrary signed box; that shortcut must not be reused. Additional
valid physical bounds are

    zL/(1+sum_i u_i P_i^+Tii^+) <= Z(u) <= zU/gamma.

## 5. All original-coordinate derivatives

Let q=A(J+K)^-1y and k_i=1-(Sq)_i, including inactive i. At the same actual
d, using the prior beta/rho rowwise bounds and (4) gives

    |k_i-kstar_i| <=
      B*sqrt(L sum_j a_j beta_ij^2)
      +B*sqrt(L rho_i ke)
      +B*Bstar*kappa*sqrt(L sum_j a_j Sstar_ij^2).    (6)

Proof: split Sq-Sstar qstar into (S0-Sstar)q+Eq+Sstar(q-qstar).
The scaled q norm is at most B*sqrt(L); the difference norm is at most
B*Bstar*kappa*sqrt(L). Weighted Cauchy and PSD Cauchy give (6).

Let d0_i=x_i midpoint(P_i), and compute k0 exactly in the nominal r-dimensional
model. For fixed Sstar the identity

    kstar(d)-kstar(d0)
      =-(I+Sstar D)^-1 Sstar (D-D0)kstar(d0)

still holds. By (2), the symmetric matrix

    (I+Sstar D)^-1 Sstar
      =Sstar^(1/2)(I+Sstar^(1/2)D Sstar^(1/2))^-1 Sstar^(1/2)

is PSD and at most Sstar/gamma_star. Therefore the extra scale error is

    sqrt(Sstar_ii)/gamma_star *
      sum_j sqrt(Sstar_jj)|x_j|rad(P_j)|k0_j|.       (7)

Add (6) and (7), with outward square roots, to obtain each k interval.
The original physical derivative is

    -partial Z(u)/partial u_i = (Z(u)/z)^2 P_i k_i^2.

Positive interval multiplication and interval squaring give all marginal
benefit intervals. For reward G(u)=Z(0)-Z(u)-price.u, subtract price_i.
The same simplex tangent certificate then bounds global regret against every
original admissible u. Baseline Z(0), if desired for a reward interval, is
itself a signed prediction; no unmeasured exact baseline is supplied.

## 6. What is and is not removed

This construction removes the restriction to nonnegative increments around
an illuminated reference. Once finite acquisition resolves the desired
controls and the two displayed margins pass, it certifies the FULL original
simplex, including its unilluminated faces. It acquires the missing stability
margin from the scalar data rather than presuming signed extrapolation is
well conditioned.

It does not guarantee finite-noise excitation of every relevant control.
That separate obstruction and a tolerance-aware finite discovery procedure
are treated in shifted_excitation.md. Rank, raw acquisition, calibration,
control preparation, setting writes, reset/settling, stability duration,
arithmetic and coefficient precision all remain charged. The online
certificate uses the same O(nr^2+r^3) shared row moments as the prior model.

An equally informed shifted Woodbury / interval reduced-model method can
implement all these operations. The construction closes an interface gap;
it claims no universal algorithmic, photon, or statistical advantage.
