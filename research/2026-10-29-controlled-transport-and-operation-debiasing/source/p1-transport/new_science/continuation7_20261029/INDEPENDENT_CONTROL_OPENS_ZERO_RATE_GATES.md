# Independent control supplies coercivity even when native gates close

29 October 2026. Receiving extension. The continuous-phase form
inequality was supplied and proved by the complementary role in
`record_geometry/PHASE_ENERGY_SUPPLIES_EXCHANGE_COERCIVITY.md`.
Root supplies the corresponding sign calculation and the full-action
receiving check below. This is a population structural result, not a
claim that a laboratory gate can be closed or reversed perfectly.

## 1. The native positivity premise can be replaced

The primary action proof used |alpha_i|<=a<1 only to transfer ordinary
occupation replacement by uniform native ellipticity. All other
estimates need bounded nonnegative native rates, own-swap symmetry,
and the actual independent phase/sign operation.

Allow now |alpha_i|<=1, including N-dependent amplitudes arbitrarily
close to one. For the circle supplier, define

    D_ex=(1/2)sum_i int|f^i-f|^2,
    D_native=(1/2)sum_i int r_i|f^i-f|^2,
    D_theta=sum_i int|partial_i f|^2.

The complementary proof establishes

    D_ex <=(4/s)D_native+8 D_theta.                    (1)

Consequently D_native+kappa_N D_theta dominates (s/4)D_ex once
kappa_N>=2s. This bound is uniform in volume and frozen context.
It does not assert positive instantaneous rates or native mixing.

## 2. Independent sign kicks give the analogous bound

For rates r_i=(s/2)(1+beta_i sigma_i), |beta_i|<=1, beta_i phase
independent and own-swap invariant, let

    D_sign=(1/2)sum_i int|f^(flip_i)-f|^2.

Then

    D_ex <=(4/s)D_native+4 D_sign.                     (2)

Proof: for one bond put h=f^i-f, I=int|h|^2,
J=int|h-h^(flip_i)|^2 and W=int(1+beta_i sigma_i)|h|^2.
Sign symmetry gives

    |int beta_i sigma_i |h|^2|
       <=(1/2)sqrt(J) sqrt(int|h+h^(flip_i)|^2)
       <=sqrt(I J).

Thus I<=W+sqrt(IJ)<=W+I/2+J/2, so I<=2W+J.
Native exchange commutes with its sign flip and preserves the reference
measure; hence J<=4 int|f^(flip_i)-f|^2. Sum over bonds and divide by
two to obtain (2). The proof applies to complex form-domain functions
as well, using real parts in the square-difference identity.

Therefore D_native+gamma_N D_sign dominates (s/4)D_ex once
gamma_N>=s. Only eventual positivity of this fixed form constant is
needed in the occupation block limits.

## 3. Receiving audit

Replace the c_min comparison in Section 2 of
`CONTROLLED_MACROSCOPIC_ACTION.md` by (1) or (2). Its phase-independent
Feynman--Kac potential is still bounded by the ordinary exchange
variational problem, with fixed coefficient s/4 for all sufficiently
large N. The full joint form, rather than native dynamics alone,
supplies this comparison. Applying the visible variational inequality
at each fixed phase remains legitimate after this form inequality.

The preceding phase-potential bound is unchanged: it already discarded
the nonnegative native form. Its constant remains bounded at amplitude
one. The likelihood L2 identity allows zero native rates, since both
comparison laws have the same zero-rate transitions and the formula
uses r_i(e^xi-1), not division by r_i. Tilted occupation replacement
can therefore still be transferred from the actual law.

Upper rate bounds, current jump sizes, the exact continuity relation,
active circle initialization, and the finite sign initial density
ceiling are unchanged. The ordinary tilted hydrodynamic receiving
argument uses the transferred exchange form and the vanishing phase
drift, not pointwise positivity of every instantaneous native edge.
Its limiting parabolic coefficient is still s/2. The Riesz/action
identification and smooth-path lower approximation are macroscopic
arguments with the same action.

Accordingly the full density/current action, scalar circulation LDP
and SCGF extend to the exact amplitude class |alpha_i|<=1 for the
independent circle supplier, and |beta_i|<=1 for independent sign
kicks, with their respective strengths tending to infinity at any
rate. The initial-profile quantifier and all record/calibration/port
restrictions remain those of the primary receiving theorem.

This extension does not automatically include arbitrary additive
implementation errors at a closed native gate: nonnegativity and
the form comparison must still be checked for the actual perturbed
generator. The earlier reciprocal-error theorem retains its stated
uniformly positive scope unless separately extended.
