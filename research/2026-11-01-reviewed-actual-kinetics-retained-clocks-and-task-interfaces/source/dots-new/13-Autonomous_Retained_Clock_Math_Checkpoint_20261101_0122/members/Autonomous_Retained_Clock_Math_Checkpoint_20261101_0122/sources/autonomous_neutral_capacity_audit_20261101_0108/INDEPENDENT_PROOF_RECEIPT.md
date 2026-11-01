# Independent audit: autonomous transverse neutral circulation and actual capacity

Date: 2026-11-01. Auditor: `producer-workspace/audit_sampled_clock_process`.

Frozen source:
`sampled_clock_process_pending_20261101/AUTONOMOUS_NEUTRAL_CAPACITY_ROOT.md`.
SHA-256:
`17e122c905e45297967ee33c845577e55c9209b3481136181f4f4cdb1064c50a`.
The source and earlier freezes were not edited.

## Verdict

**PASS for the stated autonomous smooth compact transverse perturbation of the
received constant-SPD diffusion.** In particular, the actual new forward
committor has finite symmetric energy at most the explicit neutral trial energy.
This conclusion does not substitute the old reversible committor. The
nonreversible stationary square-reset count identity then applies with the
regularity and stationary augmentation earned below. No equality of forward and
backward committors is used.

The key completion of the terse root argument is to extend each bounded-domain
committor by h outside its truncation. Its zero-trace difference from h gives a
GLOBAL form-domain function of energy at most C0. Weak compactness and actual
exit-law convergence then identify the finite-energy limit without presupposing
finite energy for the desired committor.

The final vector/correlation-to-clock join remains conditional on the separately
received neutral observable bounds and their domain premises. This receipt
does not certify arbitrary time-varying control, feedback, a physical processor,
a numerical current certificate, or hardware preparation.

## 1. Actual model and conventions

Use the received diffusion on R^(1+d), d>=2, with smooth coercive homogeneous
U>=0, constant SPD transverse mobility M, inverse temperature beta>0, and

    dY = -v'(Y) U(Z) dt + sqrt(2/beta) dW,
    dZ = [-v(Y) M grad U(Z)+c_z(Y,Z)]dt + sqrt(2M/beta) dB,
    v(y)=1+kappa(1-y^2)^2.

Let D=diag(1,M), rho=exp(-beta vU), and let m be rho times any fixed positive
normalization constant. Its finite total mass is Ztot and pi=m/Ztot. Define

    E(f,g) = beta^(-1) integral grad f^T D grad g dm,
    Gamma(f) = beta^(-1) grad f^T D grad f.

Let A={y<=-b}, B={y>=b}, S={|y|<b}, b=1/2. The explicit h is 1 on A, 0 on B,
in [0,1], smooth inside S, and has finite global form energy C0. Its neutral
property is Ch=0, where C=c dot grad and c_y=0. The perturbation is autonomous,
smooth, globally compactly supported, weighted divergence-free, and of any fixed
finite strength. The broader cases of merely formal skewness or uncontrolled
noncompact drift are not being admitted.

The local model/old Lyapunov argument was checked in
`constant_spd_mfpt_20261031/POISSON_CURRENT_CONSTANT_SPD_MFPT.md`, SHA-256
`bf9e83e1f39f25758dc02b10a06d06a955b98e61de172f633ba5d4f341a7d8e0`.
This audit uses only that concrete original model/form interface, not approval
of an unfinished subsequent global odd-current construction.

## 2. An explicit normalization-free admissible drift

The claimed class is nonempty and does not need the unknown partition constant.
Choose chi in C_c^infinity(R^(1+d)) and a constant nonzero antisymmetric d by d
matrix J. Set, with an optional arbitrary finite strength multiplier,

    c_y=0,
    c_z = J grad_z chi - beta v(y) chi J grad U(z).

Then

    rho c_z = J grad_z(rho chi),
    div_z(rho c_z)=trace(J Hess_z(rho chi))=0.

The full weighted divergence is therefore zero. All coefficients are smooth
and compactly supported, so c and its required derivatives are bounded. Since
h depends only on y, Ch=0. Multiplying m by a constant changes neither conclusion.
Nontrivial chi/J choices give nonzero circulation. No angular mixing estimate
or projected-coordinate Markov property is needed.

## 3. Nonexplosion, invariant law, and the actual perturbed semigroup

For the received original model a proper quadratic Lyapunov function is

    V=1+y^2+K z^T M^(-1)z,  K=1+kappa/p,

where p is the homogeneous degree of U. Its old drift has a finite global upper
bound. The added CV=c dot grad V is bounded because c has compact support and
V is smooth. Hence `(G0+C)V` also has a finite global upper bound. Stopping at
compact exits and applying the standard Lyapunov estimate proves nonexplosion.
Smooth locally Lipschitz coefficients then give a unique actual global SDE law.

Weighted divergence-freeness must be promoted from an integration-by-parts
symbol to the actual invariant semigroup. One precise route is the received
closed symmetric form and its bounded first-order perturbation. On its domain F,
define

    B(u,v)=E(u,v)-integral (Cu)v dm.

Because D is a fixed SPD matrix and c is bounded,

    |integral (Cu)v dm|
      <= sqrt(beta) ||D^(-1/2)c||_infinity E(u,u)^(1/2)||v||_2.

Thus the perturbation is continuous in the E_1 form norm. Compact support and
div(mc)=0 imply skewness, first on smooth functions and then by form closure,
so B(u,u)=E(u,u). B is consequently a closed sector form on the SAME domain.
The usual truncation/chain rule for the first-order term makes it a Markov form
and likewise for its adjoint. In particular the skew contribution for a
truncation test is an integral of C applied to a scalar function of u and
vanishes by div(mc)=0.

Since the original finite-mass conservative form contains 1 with E(1)=0,

    B(1,v)=0,  B(v,1)=0.

Both the form semigroup and its adjoint preserve 1, so m is genuinely invariant,
not just formally infinitesimally invariant. On smooth compact tests the
generator is G0+C. Local elliptic martingale-problem uniqueness and nonexplosion
identify this semigroup with the actual perturbed SDE, at least m-almost
everywhere as needed for stationary laws. This supplies the actual Markov and
invariant-law interface used later.

## 4. Slab exit is finite: stopped Y values remain bounded

Write tau_S for the first exit from S and start at x=(y,z) in S. For |y|<b,

    -y v'(y)U = 4kappa y^2(1-y^2)U >=0.

The transverse perturbation leaves the Y equation unchanged. Itô's formula,
stopped at t, tau_S, and a nested compact exit sigma_R, gives

    E Y_stop^2
      = y^2 + E integral_0^stop [-2Y_u v'(Y_u)U(Z_u)+2/beta]du
      >= y^2 +(2/beta) E stop.

The stochastic integral has zero mean: its integrand is bounded by a constant
times b up to this stop. Crucially, even if the spatial localizer fires first,
the stopped Y lies in [-b,b], because tau_S is also in the minimum. Therefore

    E(t wedge tau_S wedge sigma_R) <= beta(b^2-y^2)/2.

Nonexplosion makes sigma_R increase to infinity. Monotone convergence in R and
then t proves the stronger pointwise statement

    E_x tau_S <= beta(b^2-y^2)/2 <= beta b^2/2 < infinity.

No transverse equilibration is used, and the bound is independent of the fixed
circulation strength. It also applies to the reversed perturbation -c.

## 5. Bounded-domain energy estimate before global energy is known

Choose nested bounded slab truncations D_R tending to S; cylinders
`(-b,b) times ball_R` are bounded Lipschitz domains, which already suffice for
the weak proof, or one may use smooth roundings/exhaustions. Give the actual
G0+C Dirichlet problem boundary values h on the entire boundary, including h=1
or 0 on the physical basin faces.

On each fixed bounded truncation the coefficients and weight are smooth, locally
elliptic, and bounded above/below as required. Let w_R in H_0^1(D_R,m) solve

    E_R(h+w_R,phi)-<C(h+w_R),phi>_(m,D_R)=0

for every zero-trace test phi. Weighted Poincare on this bounded domain and the
skew cancellation give the standard coercive weak Dirichlet solution. The weak
maximum principle gives 0<=q_R=h+w_R<=1. The same actual bounded-domain solution
has the stopped boundary-value representation

    q_R(x)=E_x h(X_(tau_D_R)).

Testing with w_R is legitimate at this finite-domain stage. Since Ch=0 and

    <Cw_R,w_R> = (1/2) integral C(w_R^2) dm =0,

we get exactly

    E_R(w_R,w_R)=-E_R(h,w_R),
    E_R(q_R,q_R)=E_R(h,h)-E_R(w_R,w_R)<=E_R(h,h).

The zero trace of w_R is enough to remove the artificial drift boundary term;
one need not claim the artificial boundary is a reflecting boundary. Taking R
large enough to contain the compact drift support is an additional simple option.

## 6. Extend by h, identify the ACTUAL limit, and control infinity

Extend w_R by zero outside D_R, and set qtilde_R=h+w_R on the entire space.
Zero trace gives membership in the global received form domain. Across the
artificial boundary there is no Sobolev jump. Moreover,

    E(qtilde_R)
      =E_R(q_R)+E_(D_R complement)(h)
      <=E_R(h)+E_(D_R complement)(h)=C0.

All qtilde_R lie in [0,1], so their global L2 norms are uniformly bounded by the
finite mass of m. This is the essential GLOBAL uniform estimate, not just a
formal integral over changing domains.

Define the actual forward committor

    q(x)=P_x(X_(tau_S) in A) in S,  q=1 on A, q=0 on B.

The finite exit result makes this exhaustive. For fixed x, on a path with finite
tau_S the stopped nonexplosive trajectory has compact range up to tau_S.
Therefore it eventually encounters no receding transverse/artificial boundary
before its actual basin exit. For cylinder truncations, directly

    |q_R(x)-q(x)|
      <=P_x(artificial boundary reached before tau_S) -->0.

The analogous stopped-boundary convergence holds for regular smooth exhaustions.
Thus the limit is the actual hitting probability of the new diffusion, not a
different weak solution selected at infinity. Globally qtilde_R converges
pointwise to q, and dominated convergence using finite m gives strong L2
convergence.

The uniform global E_1 bound has weakly convergent form-domain subsequences;
their L2 limit must be q. Closedness and weak lower semicontinuity give

    q in F,  E(q,q)<=C0.

No finite-energy committor was assumed in obtaining this estimate. This also
controls infinity without unproved pointwise flux decay or an artificial
reflecting wall. Under the standard core density for the slab Dirichlet domain,
one may subsequently test the global weak equation with q-h and recover the
stronger identity `E(q)=E(h)-E(q-h)`, but the inequality above already suffices.

## 7. Local boundary decomposition and nonreversible stationary augmentation

Local elliptic regularity makes q harmonic and smooth in S, with regular
one-sided derivatives up to each flat physical boundary. The domain-boundary
data are constants there. Extend q by its constants in A/B. Generalized Itô--
Tanaka on compact localizations then gives q(X) as its continuous local
martingale plus continuous finite-variation boundary terms, supported on the
two physical boundaries. Its interior drift is zero because the ACTUAL
generator G0+C annihilates q in S. The transverse first-order operator creates
no additional surface distribution: q itself is continuous, and the boundary
conormal term comes from the diffusion derivative jump.

Only local finiteness of those boundary terms is needed before compact stopping.
The finite global energy just earned gives the martingale bracket integrability
needed to unstop. One must not replace this local regularity argument by an
unsupported assertion that every abstract Fukushima zero-energy part is
finite variation.

The actual invariant diffusion admits a two-sided stationary realization.
Local ellipticity/irreducibility and finite invariant probability provide its
usual stationary ergodicity and past basin visits. There is also a direct
specialized past-visit route here: time reversal under pi has generator G0-C;
the same slab-exit argument applies to -c. Thus its first past hit of A union B
is finite almost surely. Taking this at every integer time gives a last basin
visit before every real observation time on one probability-one set.

Let I_t=1 for last visited A and 0 for last visited B, matching THIS q's boundary
values. This is a well-defined stationary Markov augmentation. The conditional
law of I given X is determined by the BACKWARD committor qminus of G0-C:

    mu(dx,1)=qminus(x) pi(dx),
    mu(dx,0)=(1-qminus(x)) pi(dx).

No assertion qminus=q is made or needed. The actual future dynamics still use
the forward generator G0+C and its forward committor q.

## 8. Count identity without reversibility

Basins are separated, so a continuous nonexplosive path has finitely many
completed full-basin transitions on each compact horizon. This is a pathwise
statement, not yet an expected-count estimate. Let N_t count those transitions
and set F_t=(q(X_t)-I_t)^2 in [0,1].

At each completed transition F jumps from 1 to 0, contributing -1. On each
physical boundary the current I equals q. The predictable old I differs only
at the locally finite switching instants; the continuous boundary local-time
measures have no atoms there. Thus the boundary finite-variation contribution
to the square formula vanishes. The localized identity is

    F_t-F_0
       =2 integral_0^t(q(X_u)-I_(u-)) dM^q_u
         +2 integral_0^t Gamma(q)(X_u)du-N_t.

The forward committor and actual forward quadratic variation are the only
committor ingredients. Reversibility never appears in this identity.

Stop at compact exits and the m-th count. Base stationarity gives

    E integral_0^T Gamma(q)(X_u)du = T E(q)/Ztot,
    E N_stopped <=1+2T E(q)/Ztot.

Fatou earns integrability of N_T before removing its stop. Alternatively the
martingale bracket is bounded in expectation by `8T E(q)/Ztot`, so it is a true
L2 martingale after localization. Bounded F, finite expected energy, earned
count integrability, and nonexplosion permit unstopping. Augmented stationarity
then cancels E F_T-E F_0, proving

    E_stationary N_T = 2T E(q)/Ztot <=2T C0/Ztot.

The backward committor would enter an explicit formula for E F_t, but this
expectation is stationary regardless, so neither computing it nor identifying
it with the reversible formula is necessary.

Conditioning on X_0 in A fixes I_0=1 and gives augmented/full-future-path density
bound R=1/pi(A). That conditioning is not stationary: use domination of already
bounded stationary bad events, not the count equality under the conditioned
law. Finite stationary intensity excludes deterministic-time count atoms and
domination preserves that property.

## 9. Scope, credit, and remaining joins

The weak test is an ordinary skew-neutral energy cancellation, and the count
identity is an ordinary stationary capacity/transition-frequency calculation.
Neither claims historical novelty. The useful result here is that all of them
refer to the NEW actual autonomous diffusion and its actual forward committor.

To obtain the proposed autonomous processed clock, separately receive the
neutral scalar/vector semigroup estimates and their actual domain hypotheses,
the old symmetric global source certificate used by those estimates, the
sampled-record entropy bound, slab mismatch charge, both actual and comparison
multi-jump charges, preparation domination, and numerical outward enclosures.
The capacity/intensity result supplies one join, not all of them automatically.

Time-varying controls generally have no stationary augmented label law of this
kind. A stationary random phase or autonomous controller changes the full
state, invariant law, and preparation interface; a fixed phase can be singular
relative to a continuous stationary phase distribution. None is licensed by
this autonomous proof. Arbitrary adaptive feedback is likewise excluded.

## 10. Action/target/reason/outcome receipt

* **Action:** use zero-trace extension by h before taking the global limit.
  **Target:** bounded-domain energy paragraph of the frozen construction.
  **Reason:** an estimate over changing domains alone must be connected to the
  actual global closed form. **Outcome:** supplied above; finite actual
  committor energy <=C0 is earned without circularity.
* **Action:** bind the compact smooth weighted divergence-free drift to the
  actual conservative invariant semigroup. **Target:** perturbed model interface.
  **Reason:** formal skewness alone is not an invariant-law proof.
  **Outcome:** Lyapunov and sector-form/SDE identification supplied above for the
  stated class; noncompact/singular perturbations remain unadmitted.
* **Action:** use the backward committor only for stationary past-label law and
  the forward committor for square reset. **Target:** nonreversible augmentation.
  **Reason:** those committors need not agree. **Outcome:** no reversibility gap
  remains in the count proof for this autonomous class.
* **Action:** independently receive all neutral observable and physical/numeric
  inputs before announcing a processed clock. **Target:** proposed downstream
  construction. **Reason:** this source explicitly leaves those joins separate.
  **Outcome:** capacity/intensity proof passes; no unreceived hardware, arbitrary
  protocol, or numerical capability is promoted by this audit.

No external retrieval, helper agents, numerical substitutes for proof, source
mutation, permission escalation, denial, or retry were used.
