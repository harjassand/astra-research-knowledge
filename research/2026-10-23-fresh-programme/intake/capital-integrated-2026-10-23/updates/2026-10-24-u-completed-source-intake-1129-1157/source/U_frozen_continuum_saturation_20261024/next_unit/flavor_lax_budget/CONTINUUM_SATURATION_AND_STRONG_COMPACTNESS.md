# Boundary saturation and strong compactness of the homogeneous Lax fiber

24 October 2026. **Frozen: root full internal consequential review passed**, with four bounded support checks described below. The frozen all-time budget theorem and finite Case-D certificate are unchanged. This is a further deterministic continuum consequence of the same established invariant. It is internal mathematics for the stated model, not a novelty, hardware, astrophysical relaxation, or external-certification claim.

## 1. The consequential representation question

The relaxed Lax fiber originally allowed |D(v)|<=|G(v)| so that weak angular limits, including possible unresolved depolarization, were not excluded by assumption. Does that relaxation actually contain fields with a strictly shortened local ELN Bloch vector? If it did, arbitrarily late homogeneous evolution could conceivably hide order-one angular structure in finer and finer scales while preserving only a weak limit.

The answer is **no for the exact collinear-reference fiber**. Its complex cut-boundary invariant and the pointwise ball force length saturation almost everywhere. The fiber is consequently compact in strong L2, not only weak-*. All sufficiently small initial perturbations remain uniformly close to that strongly compact fiber at arbitrary times. A finite angular projection therefore resolves the whole small-seed evolution family to any prescribed L2 tolerance, with nonconstructive resolution/seed thresholds. This does not give their numerical sizes or a dephasing time.

## 2. Model, reference fiber, and exact conservation

Let I=[-1,1], G continuous and real, R=|G|, and q=integral_I G. The charge q may be zero. For a real vector field the homogeneous axisymmetric collisionless fast-limit equation is

    Ddot(v)=(D_0-vD_1) cross D(v),
    D_n=integral_I v^n D(v) dv.                              (1)

The interaction scale has been absorbed in time. There is no spatial transport, collision term, external control, or averaging operation in (1). The bounded initial-value problem has a global two-sided L-infinity flow: the vector field is locally Lipschitz and every pointwise |D(v)| is conserved.

For u outside I define

    L_D(u)=integral_I v D(v)/(u-v) dv,
    ell(u)=integral_I v G(v)/(u-v) dv.

The dot product of complex vectors is bilinear. As derived in the frozen source,

    D_0dot=0,
    Ldot_D=(D_0-uD_1) cross L_D,
    d/dt(L_D dot L_D)=0.                                    (2)

The exact reference fiber is

    K_G={D real L-infinity: |D|<=R a.e.,
         integral D=q z,
         L_D(u) dot L_D(u)=ell(u)^2 for all u outside I}.      (3)

It is nonempty because Gz belongs to it. No statement that every member is dynamically reachable is required below.

## 3. Boundary products are legitimate L1 identities

Extend f(v)=vD(v) and g(v)=vG(v) by zero outside I. They belong to L2(R). The Cauchy transforms have strong L2 upper-boundary limits

    L_D(x+i0)=A(x)+iB(x),    B(x)=-pi xD(x),
    ell(x+i0)=a(x)+ib(x),    b(x)=-pi xG(x),                  (4)

where A is a real vector principal-value transform and a is a real scalar principal-value transform. These are the standard L2 Plemelj limits, also obtainable from L2 convergence of the Poisson kernel and conjugate Poisson kernel.

There is no unsupported multiplication of distributional traces. If X_n->X in L2, then its bilinear squares converge in L1, because

    ||X_n dot X_n-X dot X||_1
       <=(||X_n||_2+||X||_2)||X_n-X||_2.

Apply this to (3) at u=x+i y and let y decrease to zero. The boundary square identity holds in L1 and hence almost everywhere. Its real and imaginary parts are

    |A|^2-|B|^2=a^2-b^2,
    A dot B=ab.                                             (5)

All norms and the dot product in (5) are now ordinary real Euclidean ones.

## 4. Exact saturation of the relaxed ball

**Theorem 1.** Every D in K_G satisfies |D(v)|=R(v) almost everywhere.

On the set where b!=0, the pointwise ball gives |B|^2<=b^2, and the first identity in (5) gives |A|^2<=a^2. If a!=0, real Cauchy-Schwarz yields

    a^2 b^2=(A dot B)^2<=|A|^2|B|^2<=a^2 b^2.

Equality forces |A|=|a| and |B|=|b|, as both scalar factors are nonzero. It also fixes the relative orientation A=(a/b)B. If a=0 and b!=0, the first identity instead gives

    |A|^2=|B|^2-b^2<=0,

so A=0 and |B|=|b| directly. Therefore |D|=|G| wherever vG(v)!=0. Where G=0, the ball already gives D=0. The single point v=0 has zero Lebesgue measure. This proves saturation.

In particular no nonzero-charge assumption, sign-crossing condition, complete-flip condition, quotient by ell, or analytic continuation through endpoints enters this result. It does not classify the fiber by poles or prove that it is a three-carrier family.

## 5. Strong compactness of the entire fiber

The ball |D|<=R is weak-* compact and closed in real L-infinity. Each charge component and each fixed-u transform is an L1 pairing. Each bilinear-square constraint is a continuous finite-dimensional polynomial of that pairing. Thus the intersection (3) is weak-* compact. L1(I) is separable, so bounded weak-* sets are metrizable and sequences admit subsequences.

Let D_n in K_G converge weak-* to D in K_G. Theorem 1 gives

    ||D_n||_2^2=||D||_2^2=integral_I R^2.

Weak-* convergence tests against D, which is in L1 on the finite interval. Therefore the Hilbert identity gives

    ||D_n-D||_2^2
       =||D_n||_2^2+||D||_2^2-2 integral_I D_n dot D ->0.      (6)

**Theorem 2.** K_G is compact in strong Lp for every finite 1<=p<infinity.

For p<2 use the finite-measure embedding. For p>2 use the uniform L-infinity bound and

    ||D_n-D||_p^p<=(2||R||_infinity)^(p-2)||D_n-D||_2^2.

Strong L-infinity compactness, continuity of D(v), a derivative bound, and a fixed analytic pole classification are not concluded.

## 6. Actual small seeds at arbitrarily late times

Let A_eta consist of all trajectories of (1) with

    |D_in(v)|<=R(v),
    ||D_in-Gz||_1<=eta.

For eta_n->0 choose any trajectories and any times t_n. Their current fields D_n(t_n) are uniformly bounded by R. Any weak-* subsequential limit D_* has charge qz. For each fixed u outside I, the initial transform error is at most

    ||a_u||_infinity ||D_in,n-Gz||_1 ->0,
    a_u(v)=v/(u-v).

Conservation (2) and weak-* continuity therefore put D_* in K_G. This argument uses every fixed off-cut u separately; it requires no convergence uniform in u near the cut.

The initial norm deficit obeys the exact bound

    0<=||R||_2^2-||D_in,n||_2^2
       <=2||R||_infinity ||D_in,n-Gz||_1 ->0.

These norms are preserved by the actual flow. Theorem 1 gives ||D_*||_2=||R||_2, so (6) also forces the current subsequence to converge strongly in L2 to D_*. Uniform boundedness again gives all finite Lp.

Define

    omega(eta)=sup_{D in A_eta, t in R} dist_L2(D(t),K_G).

If omega did not tend to zero, an eta_n->0 sequence with distance bounded below would have the strongly convergent subsequence just constructed, whose limit is in K_G, a contradiction. Hence

    omega(eta)->0 as eta->0.                                (7)

This is uniform over all times, not a finite-time perturbation estimate. It supplies no rate for omega and does not say that a particular fixed nonzero seed has exactly the reference invariants.

## 7. Consequence for finite angular resolution

Let P_N be the L2-orthogonal cell-average projection on the equal dyadic partition of I into 2^N cells. These finite-dimensional projections converge strongly to the identity, and ||I-P_N||<=1. Strong compactness of K_G makes convergence uniform on that set:

    tau_N:=sup_{F in K_G}||(I-P_N)F||_2 ->0.

A finite covering of K_G proves this from pointwise projection convergence. Combining it with (7) gives the explicit relation

    sup_{D in A_eta,t}||(I-P_N)D(t)||_2 <=omega(eta)+tau_N.     (8)

Thus for every tolerance epsilon>0 there are finite N and eta_0>0 such that every seed of size at most eta_0 is resolved to that L2 tolerance at every time. For a fixed-length trajectory the squared unresolved norm is exactly its angular polarization variance,

    ||(I-P_N)D||_2^2
       =integral_I R^2-sum_cells h_i |average_cell D|^2.

For shorter initial vectors replace the first term by the conserved integral |D_in|^2. No numerical N, eta_0, instrument resolution, or cost has been acquired. Equation (8) excludes an order-one unresolved angular contribution in the **joint infinitesimal-seed/arbitrary-time limit**. It does not exclude phase mixing of a finite seed, fine structure of vanishing L2 weight, or finite-resolution loss at a prescribed N.

The saturation here is of an ELN difference-vector length in the mean-field model. It must not be equated with the microscopic purity of all individual neutrinos and antineutrinos.

## 8. Averages, primary ancestry, and exact scope

K_G is not convex. An SO(2) phase ensemble of a converted member has diagonal mean D_z z and the same average conversion, while retaining the invariant in transverse covariance. That mean need not belong to K_G, retain its pointwise length, or satisfy the actual-trajectory distance-to-K conclusion. The uniform projection-tail bound itself does pass to linear averages of K members by contraction/Jensen, so no blanket loss of compactness under averaging is asserted. The separate `DIAGONAL_LIMIT_AND_PHASE_AVERAGING.md` gives the exact covariance identity and the standard hidden-coherence boundary; neither result refutes every diagonal averaged closure.

The established primary basis is [Fiorillo–Raffelt, PRD 107, 043024](https://doi.org/10.1103/PhysRevD.107.043024), [corrected arXiv:2301.09650v3](https://arxiv.org/html/2301.09650v3), with the [2026 erratum](https://doi.org/10.1103/js9s-fkfp). Its Lax/Gaudin invariants and finite-beam coherent/degenerate solutions are direct strong ancestors. The corrected invariant is independently derived in (2). [The soliton paper](https://arxiv.org/html/2303.12143v2) supplies coherent continuum families, but the present proof does not assume their selection.

Their discussion of generic Case–Van Kampen phase mixing concerns the linearized continuum response and integrated observables. It is compatible with (8): seed-sized fine structure can have vanishing L2 weight as eta->0, and fixed finite-seed or averaged dynamics are not assigned the exact reference fiber. No contrary source claim is manufactured. The spatial-wave quasilinear theory, transport, collisions, and changes to the physical invariant are separate models.

The scientific gain is an exact representation constraint: the full reference fiber cannot lose local ELN Bloch length in an actual angular weak limit, and the small-seed homogeneous evolution has no order-one angular-resolution escape in arbitrarily late limits. It is not a decay theorem, a practical simulation complexity estimate, an explicit finite-resolution certificate, or novelty clearance.

Bounded support: `luna_resolvent_algebra/BOUNDARY_SATURATION_L2_AUDIT.md` checks Plemelj/products/saturation; SinglePort checks the compactness/norm and uniform-sequence quantifiers; Boxcar checks angular-resolution versus averaging/readout scope; the source worker checks the existing strong primary comparison. Root independently checked the saturation core before final source review. No new numerical solve or changes to frozen predecessors were made.
