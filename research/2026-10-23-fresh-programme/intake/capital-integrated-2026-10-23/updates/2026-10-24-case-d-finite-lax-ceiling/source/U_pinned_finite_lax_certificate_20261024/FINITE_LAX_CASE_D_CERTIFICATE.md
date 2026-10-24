# A quantitative all-time conversion ceiling for published homogeneous Case D

24 October 2026. **Frozen: root full internal consequential review passed.** Root independently regenerated the scalar JSON byte-identically and replayed the pinned final verifier, obtaining the same exact certificate and 72 positive LDL pivot intervals. Root also manually checked the scalar enclosure arithmetic/derivative budgets and compared 125 independent high-precision values with the certified intervals; those decimal comparisons are diagnostic, not proof premises. The result is for the stated continuum collisionless mean-field equation. Floating optimization discovered the dual weights; exact scalar enclosures and a rational/interval dual proof establish the bound. This is internal mathematical evidence, not external certification, novelty clearance, an empirical neutrino saturation law, or an experimentally acquired capability.

## 1. Consequential question and result

The preceding frozen Lax argument proved a strictly positive all-time gap from the conserved-charge conversion budget, but supplied no usable size. The question here is whether finitely many actual continuum invariants can certify a substantial gap for an already published, homogeneously unstable continuous spectrum. A positive result constrains arbitrary later homogeneous excursions, rather than fitting a first soliton pulse. A failed outer relaxation would not imply attainability or refute the existential theorem.

Use literal Lebesgue measure on I=[-1,1] and the published Case-D spectrum

    G(v) = 11/100 - (1/2) exp[-(25/2)(1-v)^2],
    R(v) = |G(v)|,
    q = integral_I G(v) dv.

Let z be the fixed unit flavor axis. The dynamics are

    Ddot(v) = (D_0 - v D_1) cross D(v),
    D_n = integral_I v^n D(v) dv.                              (1)

**Certified statement.** Every real L-infinity solution of (1) with

    |D_in(v)| <= R(v) almost everywhere,
    ||D_in-G z||_L1 <= eta := 1/1,000,000                       (2)

satisfies, for every real time t,

    C(D(t)) := (1/2) integral_I [R-sgn(G) D_z] dv <= 141/1000.   (3)

In particular this includes the physical fixed-length seeds |D_in|=R. No seed shape, fastest-mode selection, finite observation horizon, or soliton ansatz is assumed.

The scalar enclosures prove q>0 and A_+>A_-, where A_+=integral_{G>0}G and A_-=integral_{G<0}(-G). Thus the reference charge-only budget is B=2 A_-. The certified lower bound gives

    B > 0.1535838159266311,
    B - 0.141 > 0.0125838159266311,
    1 - 0.141/B > 0.0819345.                                  (4)

The ceiling removes more than 8.19% of that budget. For the nearby actual axial charge q'=D_0^z, its charge-only budget differs from B by at most eta/2; the gap remains greater than 0.0125833. These are bounds on **ELN-weighted difference-vector conversion**, not the number of all neutrinos and antineutrinos that changed flavor.

This does not exclude an equipartition-like integrated value: half the total R-mass is approximately 0.1241262, below 0.141. It does not select a final state, quantify spatial-wave relaxation, or claim that the finite outer optimum is reachable.

## 2. Primary model and normalization

The exact spectrum is Appendix D.3, Eq. (116), of Fiorillo and Raffelt, [*Flavor solitons in dense neutrino gases*, PRD 107, 123024](https://doi.org/10.1103/PhysRevD.107.123024), [arXiv:2303.12143v2](https://arxiv.org/html/2303.12143v2). Its unique crossing is

    v_c = 1-sqrt(log(50/11)/(25/2))
        = 0.6519623316214435... .

The same appendix states that both sufficient homogeneous-instability conditions hold and gives the normalized unstable root Omega/M_1^z=-0.203994-0.211175 i. Thus the chosen spectrum is not merely an arbitrary crossing profile. The paper's quoted 100-mode moments are 50 times the literal dv moments used here; its absolute frequencies are not spliced into this calculation.

The complex two-flavor Lax invariant has established ancestry in [Fiorillo and Raffelt, PRD 107, 043024](https://doi.org/10.1103/PhysRevD.107.043024), [corrected arXiv:2301.09650v3](https://arxiv.org/html/2301.09650v3), with the [2026 erratum, PRD 113, 069901](https://doi.org/10.1103/js9s-fkfp). The off-real-parameter invariant used below is retained by that correction and is derived directly in Section 3.

The source's exact first-soliton profile already predicts an excursion below B. Integrating that profile using the normalized root gives approximately C_peak=0.1228212; this is a support-worker calculation using rounded source parameters, not a source-reported or interval-certified integrated number. Our all-time ceiling is looser than that first-pulse value, but applies to every trajectory satisfying (2), at arbitrarily late times, without assuming a single soliton.

The new [*Quasilinear Theory of Fast Flavor Instabilities*, PRL 137, 171001](https://doi.org/10.1103/f1dk-yk6g) concerns statistically homogeneous **spatial** flavor waves and quasilinear backreaction. It is a different evolution class; (3) neither establishes nor refutes its relaxation predictions.

## 3. Invariants and finite-seed errors

The vector field in (1) is locally Lipschitz on L-infinity. Pointwise |D(v)| is conserved, giving a global flow. Integration of (1) gives D_0 constant. For any nonreal u define

    a_u(v)=v/(u-v),
    L_D(u)=integral_I a_u(v) D(v) dv,
    ell(u)=integral_I a_u(v) G(v) dv.

Here complex dot products are **bilinear**, without conjugation. The identity v^2/(u-v)=u v/(u-v)-v gives

    Ldot_D(u)=(D_0-u D_1) cross L_D(u),
    d/dt [L_D(u) dot L_D(u)]=0.                               (5)

Write eta for (2). Since |v|<=1 and |u-v|>=Im u>0 at the selected poles,

    ||L_Din(u)-ell(u)z||_2 <= rho_u := eta/Im u.

Consequently every later state satisfies

    |L_D(u) dot L_D(u)-ell(u)^2|
       <= rho_u (2|ell(u)|+rho_u).                            (6)

This error includes arbitrary transverse seed components. It does not assume that the actual conserved charge is parallel to z.

## 4. A continuum-safe 72-vector Gram representation

There are 36 cells: 24 on the prescribed positive-side portion and 12 on the prescribed negative-side portion. Their endpoints are the exact dyadic numbers in `rational_candidate.json`, inherited from the single exploratory mesh. The physical crossing is not rounded into an exact sign assumption. The tiny strip where the prescribed signs sigma_i differ from sgn G is charged explicitly by its R-mass. The true cell midpoint and width are c_i=(lo_i+hi_i)/2 and h_i=hi_i-lo_i, computed rationally from those endpoints.

For a current state define actual vector moments

    d0_i=integral_cell_i D(v) dv,
    d1_i=integral_cell_i (v-c_i)D(v) dv.

Let rhat_i>0 be the dyadic numbers called `normalizations` in the candidate. They are arbitrary rational normalizations, **not assertions that floating quadrature returned exact cell masses**. Let q0 be the candidate's dyadic reference charge. Certified scalar intervals give upper bounds r_i^+ on integral_cell R and B_i^+ on integral_cell R^2, and a bound delta_q on |q-q0|.

Shift only the first zeroth moment by the actual vector

    Delta=q0 z-D_0,
    d0tilde_0=d0_0+Delta,
    d0tilde_i=d0_i for i>0,
    |Delta| <= d := delta_q+eta.

Set

    u_i=d0tilde_i/rhat_i,
    v_i=2d1_i/(h_i rhat_i).

Then sum_i rhat_i u_i=q0 z exactly. Eliminate u_0 as

    u_0=(q0 z-sum_{i=1}^{35}rhat_i u_i)/rhat_0.                (7)

The retained real Gram matrix X is for the 72 vectors

    [z,u_1,...,u_35,v_0,...,v_35].

It is positive semidefinite and X_00=1. Its actual rank is at most three; dropping that rank restriction enlarges the feasible set, which is safe for an upper bound.

Bessel's inequality for the orthogonal cell functions 1 and v-c_i gives

    |d0_i|^2/h_i+12|d1_i|^2/h_i^3 <= integral_cell_i R^2.

The shifted moments therefore obey the affine Gram inequalities

    |u_i|^2 <= N_i := (r_i^++1_{i=0}d)^2/rhat_i^2,
    |u_i|^2+3|v_i|^2 <= K_i
       := [h_i B_i^++1_{i=0}(2r_i^+d+d^2)]/rhat_i^2.          (8)

The verifier rounds these bounds outward. It verifies N_i<=2 and K_i<=2, hence

    Tr X <= 1+sum_{i=1}^{35}N_i+(1/3)sum_{i=0}^{35}K_i
         < 100.                                             (9)

No displacement collocation or pointwise angular discretization of the dynamics has occurred.

## 5. Seven actual continuum invariant constraints

The fixed rational poles are

    -3/4+i/4, -1/4+i/4, 1/4+i/4, 1/2+i/4,
     2/3+i/8,  5/6+i/8, 1+i/8.

Approximate the transform by the actual two cell moments:

    Ldisc(u)=sum_i rhat_i[a_u(c_i)u_i+a'_u(c_i)h_i v_i/2].

This is a rational complex row applied to the retained real vectors. The exact identity

    a_u(v)-a_u(c)-a'_u(c)(v-c)
       = u(v-c)^2/[(u-c)^2(u-v)]

and the shifted cell-0 moment give

    ||Ldisc(u)-L_D(u)||_2 <= e_u
       := sum_i |u| J2_i^+ /[|u-c_i|^2 dist(u,cell_i)]
          +|a_u(c_0)|d,
    J2_i^+ >= integral_cell_i R(v)(v-c_i)^2 dv.                (10)

Also

    ||L_D(u)||_2 <= M_u
       := sum_i r_i^+ max_{cell_i}|v|/dist(u,cell_i).

Thus, together with (6),

    |Ldisc dot Ldisc-ell^2|
       <= e_u(2M_u+e_u)+rho_u(2|ell|+rho_u).                  (11)

Certified rectangular intervals for Re ell and Im ell enclose Re ell^2 and Im ell^2. Equation (11) widens each resulting lower/upper slab. All square roots used only for coefficient bounds are enclosed by integer-square-root rational bounds.

If the complex row for Ldisc is r+i s, the two real Gram forms are exactly

    Re(Ldisc dot Ldisc) = (r r^T-s s^T) bullet X,
    Im(Ldisc dot Ldisc) = (r s^T+s r^T) bullet X.              (12)

Using conjugated products here would constrain a different, nonconserved quantity. The verifier uses (12).

The objective obeys

    C(D) <= C0^+ + Cmat bullet X,
    C0^+=(1/2)sum_i r_i^+ + d/2 + m_mismatch,

where m_mismatch bounds the mismatched-sign R-mass. Under the prescribed signs and (7), the only nonzero objective entries are

    Cmat_00=-q0/2,
    Cmat_0i=Cmat_i0=rhat_i/2 for minority cells i=24,...,35.    (13)

Every current continuum state in (2) maps into this finite outer relaxation, including arbitrary-time and weak phase-mixed states satisfying the same finite constraints. The relaxation need not describe all dynamical orbits sharply.

## 6. Exact dual proof; solver status is not a premise

One exploratory CLARABEL solve of this prescribed relaxation returned an estimated upper value 0.1405754104487. Its tiny floating PSD margin was not used as evidence of positivity. No parameter or pole search followed.

Its scalar multipliers were rounded to exact 48-bit dyadic rationals and saved in `rational_candidate.json`. The verifier checks all inequality weights are nonnegative. Write the retained upper-form inequalities as A_k bullet X<=b_k; a lower slab uses -A_k and the negative lower endpoint. If y is the free multiplier of X_00=1, the verifier builds

    S=y E00+sum_k lambda_k A_k-Cmat+lambda_I I,
    lambda_k>=0, lambda_I=1/1,000,000.                         (14)

For any feasible X, if S is positive semidefinite then

    C(D)<=C0^++y+sum_k lambda_k b_k+100 lambda_I.              (15)

The final term pays for the added identity using (9); it is 0.0001, not a free numerical repair. Lower/upper slab multipliers combine as lambda_hi-lambda_lo in S and lambda_hi*upper-lambda_lo*lower in (15). Negative combined coefficients are allowed and are enclosed with sign-aware interval arithmetic.

`verify_continuum_dual.py` rebuilds (7), (12), (13), and (14) from rational data. It uses 192-bit fixed-point **outward intervals** to enclose S. `fixed_interval_ldlt.py` carries out a no-pivot LDL^T factorization with interval multiplication, squaring, and division only by pivots with strictly positive lower bounds. Inductively each exact LDL pivot lies inside its interval; 72 positive lower endpoints prove S positive definite. This establishes weak duality independently of the numerical solver, primal rank, or reported eigenvalues.

The replay gives

    dual upper < 0.140694813925 < 0.141,
    minimum LDL pivot lower > 0.0000484240.                   (16)

All errors in (2), (8), (10), (11), the crossing, scalar quadrature, dyadic coefficient assembly, and positivity repair have been charged. The scalar source separately proves the interval bounds using exact arithmetic: exponential alternating Taylor series after range reduction and seven outward squarings, plus composite Simpson with explicit fourth-derivative remainders. Floating quadrature error estimates and independent high-precision decimal comparisons are not premises of that proof.

Combining (15)-(16) with the continuum inclusion proves (3). Equation (4) follows from the certified B interval. There is no limiting exchange between time and angular mesh, and no numerical integration of (1) in this proof.

## 7. Proof artifacts and hash contract

The exact rational candidate, scalar proof, verifier, and LDL checker are the proof inputs. The generated result records the intervals, all 72 LDL pivot enclosures, and the exact rational upper bound. SHA-256 identifies the reviewed bytes; a hash is not itself a mathematical correctness claim.

| File under `work/next_unit/flavor_finite_certificate/` | SHA-256 |
|---|---|
| `rational_candidate.json` | `037ad9d067b3be052c3537f94d0709d107df61c1a18cbdcece4f1aa00225bca4` |
| `root_scalar/certify_scalars.py` | `f250fcb8ab3e879946423b7ea0ac9781f4c5eafed71b5397097445d440c8ed5f` |
| `root_scalar/scalar_enclosures.json` | `35beea2cfc8948ac8972317aec5b991545a4a7bf1a404c7b8a5beba93ff872fa` |
| `verify_continuum_dual.py` | `3a12774bbecbc4926f8aa736e57a2597fea89651cba3a17a5873edb5dc71ebb1` |
| `luna_single_port/fixed_interval_ldlt.py` | `26db2a6b82be72b5f636cc7deebe1e5547570e1c15ac43fa187bdec330196801` |
| `verified_certificate.json` | `aceb968d5cd79c9c4abffd2e59a08f16fce0f517352160b73138e4cfb6342038` |

From the workspace root, the final rational/PSD replay is

    python3 \
      work/next_unit/flavor_finite_certificate/verify_continuum_dual.py

It requires only the Python standard library. It checks the pinned scalar-source and interval-JSON hashes. Recomputing the scalar JSON uses `root_scalar/certify_scalars.py`; NumPy there only loads the historical NPZ's stored dyadic endpoints. Every scalar bound thereafter uses integers and exact Fraction arithmetic. The discovery packages/solver are not needed for the final rational/PSD replay.

The discovery archive and `export_rational_candidate.py` preserve how candidate weights were found; they are not additional proof axioms. The four bounded support roles were algebra/inclusion, exploratory finite solve and ordering, exact PSD-checker/dual arithmetic, and primary normalization comparison. Root independently supplied and checked the scalar enclosure source. Bounded check paths are:

- `luna_boxcar/EXPLORATORY_SDP_README.md` and `luna_boxcar/result/`;
- `../flavor_lax_budget/luna_resolvent_algebra/FINITE_GRAM_DUAL_AUDIT.md`, plus the charge-shift/two-moment readbacks;
- `luna_single_port/fixed_interval_ldlt.py`, its tests, and the verifier readback;
- `luna_random_lag_sources/CASE_D_PRIMARY_PIN.md`;
- `root_scalar/certify_scalars.py` and `root_scalar/scalar_enclosures.json`.

## 8. What the bound changes, and what remains open

The positive outcome is an explicit all-time ceiling, more than 8.19% below the reference charge-only budget for this published unstable continuous spectrum, with a priced nonzero seed neighborhood. The preceding compactness theorem did not provide that size. The certificate uses only finitely many continuum moments/invariants, so its conclusion is checkable without integrating a particular orbit or assuming a first-pulse endpoint.

This is still a ceiling, not an acquired final conversion level or a lower bound on attainable conversion. It leaves equipartition-like aggregate values, the actual late-state distribution, sharp optimality, larger seeds, and all spatial/collisional evolution open. In particular it must not be exported as a spatial kinetic relaxation or astrophysical conversion law. Established Lax/Gaudin and homogeneous-soliton ancestry remains explicit; no claim that this construction is absent from the literature is made.
