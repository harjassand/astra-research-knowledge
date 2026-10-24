# An all-time angular-conversion obstruction from the Lax invariant

24 October 2026. **Frozen: full internal consequential review passed**, with four bounded support checks listed below. This is an internally checked theorem for the written continuum mean-field model, not external certification, a numerical useful-size gap, novelty clearance, or astrophysical validation.

## Scientific need and the selected representation

The consequential question is whether arbitrarily late homogeneous collisionless fast-flavor evolution can reach its absolute conserved-charge conversion budget. The existing capital source proves a strict continuum gap for one soliton pulse, but explicitly does not answer the all-time question. A global obstruction would constrain homogeneous relaxation/maximum-conversion closures even after arbitrarily many pulses or weak phase mixing. It would not predict an actual final state or transfer to the spatial/collisional kinetic equation.

The capital is `work/astra-capital/web/pages/d-26fd8855e5b315eb.html`, exact UTF-8 extraction titled `BP: work/natural/frozen_snapshot_01/n02_neutrino_flavor/v1.txt`; this is a worker label, not a stable N02 dossier. The corrected primary basis is Fiorillo–Raffelt, [PRD 107, 043024](https://doi.org/10.1103/PhysRevD.107.043024), [arXiv:2301.09650v3](https://arxiv.org/html/2301.09650v3), and the [official 2026 erratum, PRD 113, 069901](https://doi.org/10.1103/js9s-fkfp). The off-real-parameter two-flavor bilinear invariant used here is retained by the correction and independently derived in (5). Lax/Gaudin ancestry is established there. The [soliton paper](https://arxiv.org/abs/2303.12143v2) supplies the known one-swing dynamics underlying the narrower capital. The argument below is an owned deduction, not a claim that those invariants or pulses were invented here.

## 1. Exact model and input contract

Let I=[-1,1], G in C(I;R), R=|G|. Assume both sign sectors have positive mass and

    A_+ = integral_{G>0} G > 0,
    A_- = integral_{G<0} (-G) > 0,
    q = integral_I G = A_+ - A_- != 0.

Write zhat for the fixed flavor axis. A vector field D(v,t) obeys the homogeneous axisymmetric collisionless two-flavor fast-limit equation, with the interaction scale absorbed in time:

    Ddot(v) = (D_0 - v D_1) cross D(v),
    D_n = integral_I v^n D(v) dv.                              (1)

There is no transport, collision operator, external drive, vacuum-mass term or flavor detector in (1). Initial data satisfy |D_in(v)|=R(v). Small seeds mean ||D_in-G zhat||_{L1} tends to zero; no fastest-mode or soliton-selection assumption will enter.

Equation (1) is an ODE on real L-infinity vector fields: its vector field is locally Lipschitz, each |D(v)| is preserved, and this uniform bound gives a global flow. Direct integration gives D_0 constant. Thus the pointwise ball |D|<=R also contains weak-* limits of every orbit with these lengths.

Define the fixed-reference conversion functional

    c(v;D) = [R(v) - sgn(G(v)) D_z(v)]/2,
    C(D) = integral_I c(v;D) dv.                              (2)

This is ELN-weighted lepton-charge conversion in the two-flavor difference-vector model. It is not the total count of individual neutrinos and antineutrinos that changed flavor when their initial populations cancel in G.

For the ideal charge q, conservation of D_0^z=q gives C_+=C_-, hence

    C(D) <= B := 2 min(A_+,A_-).                              (3)

Equality requires c=R almost everywhere on the minority sign sector. Because |D|<=R, this means D=-G zhat there, including zero transverse components. For nearby seeds the conserved charge can differ slightly from q; the conclusion below is stated relative to the ideal B and remains strictly below it for sufficiently small seeds.

## 2. The complete bilinear spectral invariant

For u in C\I define

    L_D(u) = integral_I v D(v)/(u-v) dv,
    ell(u) = integral_I v G(v)/(u-v) dv.                      (4)

The dot product for complex vectors is bilinear, not Hermitian. From
v^2/(u-v)=u v/(u-v)-v,

    Ldot_D(u) = (D_0-u D_1) cross L_D(u),
    d/dt [L_D(u) dot L_D(u)] = 0.                            (5)

Consider the relaxed invariant fiber

    K_G = { real D in L-infinity(I;R^3): |D|<=R a.e.,
            integral D=q zhat,
            L_D(u) dot L_D(u)=ell(u)^2 for every u outside I }.
                                                                  (6)

It is nonempty because G zhat belongs to it. The diagonal state itself is stationary; nontrivial members of its singular invariant fiber include seed-limit nonlinear excursions. We do not assert that the whole fiber is dynamically reachable.

## 3. Local complete-flip rigidity

**Lemma.** If D belongs to K_G and D=-G zhat almost everywhere on a nonempty open interval J with G nowhere zero there, then D=-G zhat almost everywhere on I. In particular, this is impossible when q!=0.

Shrink J if necessary so |G|>=g_min>0 and |v|>=v_min>0 on it. This is always possible from a nonzero continuous sign sector; v=0 is one point. The densities vD and vG belong to L2. The Cauchy boundary values exist almost everywhere and satisfy the L2 Plemelj formulas

    L_+(x)-L_-(x) = -2 pi i x D(x),
    ell_+(x)-ell_-(x) = -2 pi i x G(x).                     (7)

The individual transforms have L2 boundary values, so their bilinear-square identities have L1 boundary values. On J, transverse D=0, hence L_x,L_y have no jump. Also

    L_z,+ - L_z,- = -(ell_+ - ell_-).

Subtracting the upper/lower boundary versions of the invariant in (6) cancels the transverse squares. Since xG(x)!=0, division by the nonzero jump gives

    L_z,+ + L_z,- = -(ell_+ + ell_-).                       (8)

Therefore M=L_z+ell has both zero jump and zero boundary value on J. Its Cauchy density v(D_z+G) vanishes on J. M consequently extends holomorphically through J: on any compact subinterval its remaining integration density is a positive distance away. The extension is zero almost everywhere on that real subinterval, hence identically zero there by the identity theorem. The complement in C of the remaining real support is connected, so M=0 throughout C\I. Cauchy-transform injectivity (equivalently its jump) yields

    v(D_z(v)+G(v))=0 almost everywhere.

Lebesgue measure has no atom at v=0, so D_z=-G a.e. The ball constraint then gives D_x=D_y=0 a.e. Finally integral D_z=-q contradicts integral D_z=q unless q=0. This proves the lemma.

The interval is a sufficient regularity condition; no extension to a positive-measure set without an interval is asserted here. No global analytic dependence of D on v is assumed.

## 4. A strict uniform budget gap on the whole relaxed fiber

The pointwise ball |D|<=R is weak-* compact in L-infinity on the finite interval. It is weak-* closed, for example by testing each rational-direction linear inequality against nonnegative L1 functions. Each fixed-u Cauchy transform is weak-* continuous, so each complex bilinear-square constraint in (6) is closed. The charge constraint is closed too. Thus K_G is weak-* compact. The objective C is weak-* continuous because sgn(G) is an L1 test coefficient on I.

It follows that C attains a maximum C_max on K_G. If C_max=B, Section 1 forces full reversal on the minority sector, which contains an open interval with G!=0. The lemma contradicts q!=0. Hence

    Delta_G := B - max_{D in K_G} C(D) > 0.                (9)

This is a fixed-spectrum existence result. It does not supply a numerical Delta_G, a gap uniform over spectra, or a selected late-time morphology. It is stronger than nonattainment at each finite time: weak phase-mixed limits were included from the start through the relaxed ball.

## 5. Uniformity over sufficiently small physical seeds and all times

There exist eta_G>0 and delta_G>0 such that every solution of (1) with |D_in|=R and ||D_in-G zhat||_L1<eta_G obeys

    C(D(t)) <= B-delta_G for every real t.                (10)

For a proof take delta_G=Delta_G/2 and suppose no eta_G works. Then there are initial data D_in,n tending to G zhat in L1 and times t_n with C(D_n(t_n))>B-Delta_G/2. The states at t_n lie in the fixed pointwise ball. L1(I) is separable, so the bounded weak-* compact ball is metrizable and a weak-* convergent subsequence has limit D_*. Conservation gives integral D_*=q zhat. For every u outside I, L1 convergence at preparation makes the initial Cauchy transforms converge to ell(u) zhat; exact conservation (5) and weak-* continuity at t_n give the invariant constraints of (6). Therefore D_* belongs to K_G. Continuity of C contradicts its maximum B-Delta_G. This proves (10), with no restriction on the size/sign of t_n or number of nonlinear excursions.

More precisely, if q'=integral D_in,z, then (2) gives C_+-C_-=(q-q')/2. For the same reference sign partition its charge-only feasible upper budget is

    B(q') = min{2A_-+(q-q')/2, 2A_+-(q-q')/2}.

It satisfies |B(q')-B|<=|q'-q|/2<=eta_G/2. Shrinking eta_G below Delta_G/2, (10) therefore leaves at least Delta_G/4 below that nearby charge-only budget too. This does not assert that an unseeded diagonal equilibrium leaves itself or that all nearby seeds are unstable.

## 6. Essential boundaries and the consequential output

- q!=0 is essential to this proof. When q=0, D=-G zhat itself belongs to K_G and attains B. This is an invariant-fiber counterexample to extending (9), not a claim of dynamical reachability from infinitesimal seeds.
- A continuous angular interval matters. The capital's three atomic beams (-1,1/3,1) with G=(-4,-4,1) have a first pulse attaining B=2; the Cauchy jump/continuation step is unavailable for that atomic measure.
- The gap can collapse as q tends to zero, a minority band collapses to an atom, or the spectrum otherwise changes. No uniformity over those limits is claimed.
- Spatial transport, collisions, injection, changing matter/geometry, quantum many-body correlations and finite-neutrino statistics are absent from (1). The homogeneous Lax invariant cannot simply be evaluated on a local spatial distribution.
- The preparation is a specified near-diagonal continuum mean-field ensemble and its seed; no experiment, realistic supernova source, or acquired seed is inferred. The readout is the bounded angular integral (2), not a laboratory detector implementation.
- Full minority reversal is stronger than minority flavor equipartition. This theorem does not rule out equipartition, crossing removal, or a quasisteady value below the absolute budget.

The internally checked result is a time-uniform homogeneous continuum obstruction beyond the first-pulse capital result: neither unlimited waiting nor weak phase mixing can erase enough of the fixed spectral information to attain the absolute charge budget. It determines no full astrophysical saturation law and carries no novelty conclusion.

## 7. Strong relaxation comparison and proof status

Fiorillo–Raffelt's [Quasilinear Theory of Fast Flavor Instabilities, PRL 137, 171001 (21 October 2026)](https://doi.org/10.1103/f1dk-yk6g), [full primary manuscript](https://arxiv.org/html/2603.28854), concerns spatial flavor waves and their statistical/random-phase backreaction on a homogeneous background. Its relaxation toward zero in affected angular bands is distinct from exact pointwise homogeneous evolution (1). The present theorem neither establishes nor refutes that spatial-wave closure. In particular, it cannot be applied to a local angular distribution by dropping spatial terms after they have changed its invariant data.

The three inspected primary works establish Lax/Gaudin ancestry, the exact soliton pulse, and a distinct spatial-wave relaxation approximation. The bounded source check found no statement or contradiction of the precise relaxed-fiber maximum argument here. That absence is not novelty clearance.

Root completed a full consequential read of the original proof, including the Plemelj/L1-square algebra and weak-* arbitrary-late sequence argument, and independently read the corrected primary/erratum. The four existing supports checked these bounded dependencies:

- `luna_resolvent_algebra/SECTIONS1_3_AUDIT.md`: exact EOM/Lax algebra, conversion equality, Plemelj signs, zero-charge and atomic boundaries; pass.
- `luna_single_port/LOCAL_RIGIDITY_AUDIT.md`: L2 boundary limits, equivalent factorization with M=L_z+ell, jump, analytic continuation and injectivity; pass under the stated open-interval hypothesis, without a Hardy-set extension.
- Boxcar's independent Sections 4–5 readback: global L-infinity flow, real weak-* ball/constraint closure and metrizability, weak phase mixing, small-seed all-time contradiction; pass. This check is retained in the team message history.
- `luna_random_lag_sources/PRIMARY_CHALLENGE_NOTE.md`: corrected invariant primary and erratum, one-soliton scope, and the new spatial-wave quasilinear comparison; no contradiction or exact all-time gap found in those named works, with no general priority conclusion.

These are internal mathematical checks, not external peer review or empirical validation. No parameter grid, numerical fixture, laboratory action, public release, or export is part of this unit.
