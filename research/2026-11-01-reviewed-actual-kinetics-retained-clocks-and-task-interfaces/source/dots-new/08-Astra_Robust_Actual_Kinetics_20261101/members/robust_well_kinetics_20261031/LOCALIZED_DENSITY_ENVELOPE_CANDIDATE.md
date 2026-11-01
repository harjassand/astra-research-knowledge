# Robust ordinary passage kinetics from a received localized geometric defect

Status: new author theorem candidate, not part of any accepted package. The
root positive-source comparison is retained as an ordinary starting point.
This construction derives the actual density, source, global-process and full
passage-law joins rather than transplanting a capacity-only comparison.

## 1. Actual uncertain model, not a perturbed nominal certificate

Let m=4alpha, integer alpha>=4; beta,kappa,d0,mu>0. U and V are homogeneous
quartic polynomials with

 U(z)>=d0||z||^4/m, 0<=V(z)<=U(z) for every z.

A cheap exact global certificate is the complete nonnegative even quartic
atom program U=sum_i c_i z^e_i, with c_i>=0, all pure terms>=d0, and
V=sum_i r_i c_i z^e_i with each0<=r_i<=1. Here r_i may be known exact numbers
OR declared closed interval parameters contained in[0,1]. In the latter case
the task concerns every actual fixed choice, not a reconstructed point model.
The complete program, exponent degree/parity, coefficient signs and ranges
must be acquired. No unrestricted positivity oracle or finite local-probe
inference is supplied. Missing atoms/pure terms and unknown external terms
cannot be silently ignored. The theorem itself allows any genuinely received
coercivity and global0<=V<=U proof, beyond this cheap grammar.

Fix an exact uncertainty amplitude 0<=e<kappa and define

 v(y)=1+kappa(1-y^2)^2,
 g(y)=y^2(1-y^2)^2/(1+y^2),
 b(y)=v(y)+e*g(y),
 F(y,z)=v(y)U(z)+e*g(y)V(z).                           (1)

Unless V is proportional to U this is genuinely nonfactorized geometry. The
actual reversible diffusion has constant block mobility diag(1,M_z), where
M_z>=mu I is finite SPD, and drift -diag(1,M_z)grad F. Its initial law is
EXACT FULL actual Gibbs conditioned on A={y<=-1/2}; B={y>=1/2}, S=(-1/2,1/2).
Neither the Gibbs law nor generator is silently replaced by the nominal U/v
model. The time-independent unknown r_i affect the actual model, not noise or
an adversarial time-varying control.

Put Z0=int exp(-beta U(z))dz, an unknown finite constant, and use the common
unnormalized scale

 w=exp(-beta F)/Z0,
 w_v=exp(-beta v U)/Z0, w_b=exp(-beta b U)/Z0.

Then w_b<=w<=w_v exactly. All integrals below use this SAME scale. Homogeneity
cancels Z0 from their scalar marginals: q_t=t^-alpha. The actual conditional
partition need not be computed or sampled.

## 2. Global process and entire-domain mass access

Write x=y^2. The exact derivative is

 b'(y)=2y(x-1)[2kappa+e(2x^2+3x-1)/(1+x)^2].           (2)

The rational expression in brackets after e is >=-1 for x>=0, hence b has
precisely the same monotonicity intervals as v because e<kappa<2kappa.
Both minima are1 at y=+-1, and both have value v*=1+kappa at y=0.
On the transition slab b<=v*. Also0<=g<=(v-1)/kappa<=v/kappa.
Thus all scalar profiles below are positive and monotone on their stated
half-intervals. Their rational evaluation and finite tail bounds are explicit.

For actual nonexplosion, yv'>=-kappa. Negative yg' occurs only with0<x<1;
there (2x^2+3x-1)/(1+x)^2<=1, so yg'>=-1/2. Since0<=V<=U,
y F_y>=-(kappa+e/2)U and F>=U. With

 H_L=1+y^2+K_L z^T M_z^-1 z,
 K_L=1+(kappa+e/2)/4,

Euler homogeneity gives

 L H_L=2(1+K_L m)/beta-2yF_y-8K_L F
       <=2(1+K_L m)/beta.

H_L is proper for each actual finite SPD matrix. Local smoothness and this
Lyapunov bound earn nonexplosion; w<=w_v and the full polynomial tail of v
make the Gibbs measure finite. Reversibility is for the ACTUAL potential(1).
No conditional energy Markov closure or angular mixing is assumed.

Define computable masses and nominal resistance

 M_v=int_A v^-alpha=int_(1/2)^infinity v^-alpha,
 M_b=int_A b^-alpha=int_(1/2)^infinity b^-alpha,
 S_v=int_S v^-alpha, R_v=int_S v^alpha.

Then M_b<=M_actual<=M_v and S_actual<=S_v. The b tail is bounded by the same
infinite-tail majorant as v because b>=v. Global evenness justifies computing
the left basin from the right tail. No compact-domain truncation is asserted.

## 3. Construct an upper source; price it against a lower density

Let pi_s=s^alpha exp(-beta s U)/Z0. Retain the already explicit well-current
j_A of the nominal v model, whose distributional divergence is w_v1A; retain
the nominal conditional S-current j_S, divergence w_v1S. Source domination,
not an unknown actual source oracle, is what is used here.

For nonnegative compact form-core f,

 <1E,f>_w <= int_E f w_v =-int grad f . j_E.

Cauchy using the actual energy and w_b<=w implies

 <1E,f>_w^2 <= E_actual(f) * beta int j_E^T D^-1 j_E/w_b.

Positive-part contraction restricts the inverse-form variational supremum to
nonnegative tests. Finite priced-current energy therefore earns the ACTUAL
zero-resolvent Q_E<=B_E, by the same positive exhaustion argument as before.
No unearned bounded inverse or spectral gap is inserted.

Set L_e=(1-e/kappa)^-1 and H_e=L_e^(alpha+1/2). For every s>=v,

 2s-b=(2s-v)-e*g >=(1-e/kappa)(2s-v)>0.                (3)

The exact homogeneous identities are

 int pi_s^2/w_b dz=[s^2/(2s-b)]^alpha,
 int z^T M_z^-1 z*pi_s^2/w_b dz
   =[s^2/(2s-b)]^alpha E_(pi_(2s-b))[z^T M_z^-1z].    (4)

The last moment scales EXACTLY as(2s-b)^-1/2, independently of the angular law.
Therefore each longitudinal price is at most L_e^alpha times its nominal
price and each linear-z transverse price at most H_e times its nominal price.
For the well's positive scalar mixture times z, apply the inherited integral
Cauchy/triangle bound with these norms; it gains at most H_e. Alternatively
cross terms pi_s*pi_t have the same formula with s+t-b and satisfy(3).
The same factor covers the conditional far tail and S-current. These are
integrated homogeneous identities, NOT a false bounded pointwise Gibbs-density
ratio (which would be impossible for unbounded U).

Crucially do not charge this coarse H_e on the rare slab A-current. Its
transverse component is zero and j_y=M_v pi_(v*) there, so its EXACT price is

 beta M_v^2 R_e,
 R_e=int_S [v*^2/(2v*-b(y))]^alpha dy.                (5)

This is one monotone rational scalar integral; denominator>=v*>0 on S.
It is not a new angular partition or Poisson oracle.

## 4. Explicit whole-source and mean bounds

Retain the accepted nominal constants (use d0 and mu as acquired lower bounds)

 a=1+9kappa/16, d=1/alpha,
 G1=v*^2/(2v*-1), Gb=v*^2/(2v*-a),
 K=alpha/(8mu sqrt(beta d0)),
 Dmax=4alpha max(kappa,1)/(mu sqrt(beta d0)),
 C_s=kappa/(2mu sqrt(beta d0)*a^(3/2)).

Let the nominal non-slab current-energy bound WITHOUT beta be

 E_rest=M_v^2(1/2+d)Gb^alpha
  +[v*^2/(128kappa^2(alpha-1)^2d^2)+K*kappa^2]G1^alpha
  +(1+Dmax)/(16kappa^2(alpha-1)^2).

The genuine robust source upper bounds are

 B_A=beta[M_v^2 R_e+H_e E_rest],
 B_S=H_e beta S_v^2 R_v(1+C_s).                       (6)

All source and pricing joins in(6) concern the ACTUAL killed form. They bound
finite inverse forms before any mean assertion. Positivity gives
Q_AS<=sqrt(Q_A Q_S), hence

 E_actual,A tau_B <=[B_A+sqrt(B_A B_S)]/M_b.           (7)

An outward rational alternative uses eta_v=S_v/M_v:

 upper <=[(1+eta_v/2)B_A
             +(eta_v/2)H_e beta M_v^2 R_v(1+C_s)]/M_b. (8)

This follows from2sqrt(XY)<=X+Y with the displayed eta factor, not from the
false claim B_S<=eta_v^2 B_A.

For a LOWER mean, use the nominal scalar transition trial h, with h=1 on A,
h=0 on B and energy C0=1/(beta R_v) under w_v. Its actual energy is <=C0
because w<=w_v and the longitudinal mobility is1. Its actual A overlap is
EXACTLY M_actual, not only a supplied bound. Optimizing c*h gives
Q_A>=M_actual^2/C0. Therefore

 E_actual,A tau_B >=M_actual/C0 >= beta M_b R_v.       (9)

This improves the valid but weaker root bound M_b^2/(C0 M_v).
The full exact Gibbs|A starting-law distinction remains essential.

## 5. All-time actual CDF, not just an energy comparison

The nominal scalar h belongs to the actual killed form domain,0<=h<=1, h1A0B,
and energy<=C0. Use k0=C0/M_b and rho=S_v/M_b. Its spectral measure has
E X<=1 and an inverse moment bounded by

 1+epsilon=C0(sqrt(B_A)+sqrt(B_S))^2/M_b^2.

Thus the accepted trial/separate-current spectral lemma and actual initial-law
comparison give, for every t>=0,

 |P_actual,A(tau_B<=t)-(1-exp(-k0 t))|
       <=epsilon+rho+sqrt(rho(1+rho)).                 (10)

A fully rational source bound is

 epsilon <= (1+eta_v) [B_A+eta_v H_e beta M_v^2 R_v(1+C_s)]
                        /(beta R_v M_b^2)-1.          (11)

Upper mass/current and lower M_b,R_v values must be substituted consistently.
If an exact point k0 is replaced by the midpoint of an outward scalar-rate
interval, the independently received additional3/16 relative-rate-width error
is paid. Queries additionally pay outward exponentials. Formula(10) concerns
absolute all-time error, not relative tail accuracy, exact exponentiality,
exponential moments or arbitrary starts. No approximate preparation is earned.

## 6. Why localization can avoid exp(alpha*e) sensitivity

This is a consequence candidate, not a finite certificate. For fixed kappa>0
and0<=e<kappa, expansion at the well and barrier gives

 b(1+h)=1+(4kappa+2e)h^2+O(h^3),
 b(y)=v*-(2kappa-e)y^2+O(y^4) at y=0.

The entire-domain dominated convergence arguments extend: b>=v dominates the
basin, while the exact derivative factor in(2) gives Gaussian domination of
R_e after barrier scaling. Therefore

 M_b/M_v -> sqrt(2kappa/(2kappa+e)),
 R_e/R_v -> sqrt(2kappa/(2kappa-e)).                   (12)

The near-well exponent remains below the main barrier whenever
L_e*Gb<v*. Under this explicit sufficient condition, all H_e-inflated basin
terms in(6) vanish relatively, and eta_v H_e also vanishes because
Gb>=v*/a (verify directly for kappa>0). Thus the conservative spectral defect
has limiting upper bound

 (1+e/(2kappa))/sqrt(1-e/(2kappa))-1,                  (13)

which is O(e/kappa), not exp(alpha*e). The sufficient condition is
0<=e<kappa*(1-Gb/v*); at kappa1 it is e<7/39.
The mean upper/lower ratio has the SAME conservative limiting bound+1.
No sharpness, optimality, empirical error budget or finite tolerance follows
from these limits alone; exact scalar integration is still required.

Uniform energy-amplitude comparison would charge the coarse L_e^alpha on the
main barrier as well. The present gain comes from retaining localization in
that one dominant integral, while honestly overpaying less important well
terms. Ordinary density/Dirichlet comparison with this same localization and
explicit source gets the same benefit. This is not a proprietary separation
or a claim that generic perturbations are harmless. A tiny unrestricted hidden
barrier still defeats finite local probes; a global acquired envelope is the
substantive information interface.
