# Sharp negative quartic: compatible counterconstruction audit

15 October 2026. Worker `fy_margin_counterconstruction`.

**The all-affine uniform fourth-power margin remains unresolved. No zero-margin sequence is constructed.** Two additional compatible escape families can be excluded analytically: a fixed slow-fast profile approaching a growing acoustic background, with the entire affine matrix optimized; and all critical constant-frequency target-logspirals, including frequencies and angular profiles varying together. The latter extends the old degree-half angular exclusion, but does not cover arbitrary radial changes of angular shape or growing effective backgrounds.

These are new internal derivations from the pinned quartic and the inherited N867/N876 heat certificate. External proof review, formal verification, historical originality, and physical capability are **UNKNOWN**. Exact supporting algebra and finite floating-point candidate diagnostics are separated below. No source, worktree, or Git changes were made.

## 1. Inputs and exact target

The read-only source checkout is
`/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015`,
with verified HEAD `b32943eeb62d0d79929a9e572a344219a785ebf9`.
Read `AGENTS.md`, `00_START_HERE.txt`, N867/N876 dossiers, the universal negative-branch report, the contact classification in `STRUCTURAL_PROOF.txt`, and N876 `PROOFS.md` plus its additive clarification. `INPUTS_SHA256.json` pins the decisive bytes.

For fixed real r < -2, set

    A=[[a,b],[c,d]], u=a²+c², j=ad-bc,
    alpha=3r/[8(r+2)]>0, beta=r(r-1)/6>0,
    C=r(r+2)/3>0,
    J(A)=alpha*((a-d)²+(b+c)²)²+beta*u²+j²+r*u*j.

The open target is one gamma_r>0 such that

    Gap_B(phi)=integral[J(B+Dphi)-J(B)]
              >=gamma_r integral|Dphi|⁴

for every affine B and every compatible compact/W0^(1,4)/periodic perturbation. The inherited result proves QC and strict individual gaps, not this quantitative target. It also gives the pointwise rank-one Bregman estimate

    J(A+R)-J(A)-DJ(A):R >= J(R)/3 >= alpha|R|⁴/3

for rank-one R. This estimate is repeatedly used with its exact scope.

## 2. Growing-contact slow-fast fields: full affine optimization still has a positive limit

This tests a specific missing geometry: a soft shear, small rank-two diagonal correction, and still smaller second-output x derivative, with an affine background allowed to diverge.

Let f(X,y) be a fixed smooth doubly periodic scalar function, with zero y mean. Define on a rectangle of x period 2pi/epsilon and y period 2pi

    phi1(x,y)=f(epsilon*x,y),
    phi2(x,y)=-(r+1)*epsilon*partial_X partial_y^(-1) f(epsilon*x,y).

Using normalized period averages, put

    P=f_X, S=f_y, Q=-(r+1)*partial_XX partial_y^(-1)f,
    q_epsilon=Dphi=[[epsilon*P,S],
                    [epsilon²*Q,-(r+1)*epsilon*P]].

This is exactly compatible. The determinant identity is

    <S Q>=-(r+1)<P²>.

If P is nonzero, q_epsilon has genuinely rank-two values. The compatible field is not replaced by an arbitrary matrix law.

### 2.1 Exact contact expansion

For q=[[p,b],[w,z]] and e=(r+1)p+z, the quadratic coefficient in J(I+tq) is

    e²+C*w²+(r+2)*det(q).

The cubic coefficient is exactly

    2p e²+[-2b w-(r+2)p²+r w²]e-C*p*(p²+w²).

In particular, there is no term p*b². A correction of the small first-column slope cannot directly cancel the leading quartic soft-shear cost. The coefficient of p²e is -(r+2), not -r(r+2).

On q_epsilon, e=0. For a background tI the averaged quadratic and cubic coefficients are

    M(I,I)=C*epsilon⁴<Q²>,
    L(I)=-C*epsilon³<P³+epsilon² P Q²>.

Thus restricted affine optimization subtracts only O(epsilon²), while

    K(q_epsilon)=alpha<S⁴>+O(epsilon²),
    <|q_epsilon|⁴>=<S⁴>+O(epsilon²).

This restricted calculation alone would be insufficient: off-diagonal or trace-free background components must also be allowed.

### 2.2 Entire affine matrix

Write B=tI+V, V perpendicular to I in the Frobenius metric, and use

    Gap_B=B^T M_epsilon B+L_epsilon^T B+K_epsilon.

The following block orders follow from the displayed cubic and the determinant identity:

    M_II=O(epsilon⁴),
    M_I,tracefree-diagonal=O(epsilon²),
    M_I,off-diagonal=O(epsilon³),
    L_I=O(epsilon³),
    L_tracefree-diagonal=O(epsilon),
    L_off-diagonal=O(1).

More explicitly, with Vd=diag(1,-1),

    M(I,Vd)=-r*epsilon²<P²>+r(r-1)*epsilon⁴<Q²>/3,
    M(I,e12)=0,
    M(I,e21)=-C*epsilon³<P Q>.

At epsilon=0 the quadratic form on V is positive definite:

    M_0(B,B)=<S²>[2alpha(a-d)²+6alpha(b+c)²+c²].

Its tracefree-diagonal/off-diagonal mixed block is zero at epsilon=0, and O(epsilon) at small epsilon. Consequently the diagonal part of M_VV^(-1)L_V is O(epsilon), while its off-diagonal part is O(1). The effective linear coefficient in the I Schur complement is therefore O(epsilon³).

A necessary lower bound on that Schur complement is available for every fixed nontrivial f. If P is nonzero, some Fourier coefficient of f has both k_X and k_y nonzero. Its gradient Fourier amplitude is a real rank-one matrix times a common complex scalar, with input frequency (epsilon*k_X,k_y) and target vector (1,-(r+1)*epsilon*k_X/k_y). Parseval expresses M_epsilon as a sum of nonnegative acoustic matrices. For this one mode, the complete acoustic determinant classification gives determinant comparable to epsilon⁴, while the trace is bounded. Its smallest eigenvalue is therefore at least c_f epsilon⁴ for sufficiently small epsilon. The full M_epsilon dominates this mode. In particular, the I Schur complement is at least c'_f epsilon⁴. This step uses the exact acoustic classification, not a numerical eigenvalue sample.

The additional reduction from optimizing the I component after V is only

    O(epsilon⁶)/Omega(epsilon⁴)=O(epsilon²).

If P=0, the original field is rank-one valued and the inherited rank-one lemma applies directly.

Let m_k=<S^k>. Taking epsilon to zero after optimizing **every** affine B gives the exact limit

    lim_epsilon inf_B Gap_B(q_epsilon)/<|q_epsilon|⁴>
       =alpha*[1-2*m_3²/(3*m_2*m_4)] >=alpha/3>0.

To compute it, minimize the limiting form on V: the minimizing c is zero, a-d is zero, and b+c=-m_3/(3m_2). Cauchy-Schwarz gives m_3²<=m_2*m_4. The optimum trace component can grow as epsilon^(-1), so this exclusion genuinely includes growing affine backgrounds.

**Failure scope.** The constants in the Schur lower bound depend on the fixed profile f. This does not cover f_epsilon whose frequency distribution or spatial concentration changes with epsilon, a sequence of increasingly deep laminates, or arbitrary backgrounds/profile combinations. A finite candidate computation is not a uniform bound over those larger classes.

## 3. Critical target-logspirals: a larger concentration route also has a positive margin

Let J_0=[[0,-1],[1,0]] denote the target quarter turn, and R_tau the target rotation through tau. For h in W^(1,4)(S1;R²), omega real, define

    phi(rho,theta)=rho^(1/2) R_(omega*log rho) h(theta),
    A_(h,omega)(theta)=[(.5 I+omega J_0)h | h'] R_theta^T,
    I_omega(h)=integral J(A_(h,omega)),
    N_omega(h)=integral|A_(h,omega)|⁴.

Then Dphi=rho^(-1/2) R_(omega log rho) A_(h,omega). These fields are exactly compatible, generally rank two, and have nontrivial log-radial variation. The old angular theorem was the omega=0 subcase.

**Claim.** For each fixed r<-2 there is delta_r^spiral>0 such that

    I_omega(h)>=delta_r^spiral N_omega(h)

for every real omega and every such h. The constant obtained below for large |omega| is explicit; the compact bounded-frequency portion is nonexplicit. This is an internally derived analytic claim, not an externally reviewed theorem.

### 3.1 Strictness for each omega

For fixed omega and smooth h, the homogeneous-up-to-target-rotation relation is

    phi(lambda*x)=lambda^(1/2) R_(omega log lambda) phi(x).

The inherited constant scalar input heat operator L commutes with target rotations. Thus its heat convolution has the scaling

    psi_t(x)=t^(1/4) R_((omega/2) log t) psi_1(x/sqrt t).

Since J is left-SO(2)-invariant, its truncated heat energy still satisfies
E_R(t)=E_(R/sqrt t)(1). The same annular small-time expansion as N876 has

    Dpsi_1(R e_r)=R^(-1/2) R_(omega log R)
                 [A_(h,omega)+O(R^(-2))].

The constants may depend on this fixed omega. Heat flux and exact-form boundary terms tend to zero as before: their circle integrals are O(R^(-2)), while the positive density is O(R^(-4)). Consequently

    I_omega(h)=2t integral D_r(Dpsi_t,D²psi_t)>=0.

A zero value implies the inherited analytic zero-density rigidity. The heat field has O(1+|x|^(1/2)) growth, so its gradient vanishes. Heat injectivity gives a constant initial map, hence h=0. Strong angular approximation and the same one-sided Fatou argument extend strictness to W^(1,4) h. No right rotational invariance is used.

### 3.2 Frequencies in a bounded interval

For |omega|<=Omega,

    |A_(h,omega)|²=(1/4+omega²)|h|²+|h'|².

A hypothetical N=1 sequence with I tending to zero has bounded W^(1,4) norm, a convergent omega subsequence, uniform convergence h_n -> h, and weak L4 convergence of h_n'. Rank-one convexity makes the integrand convex in h_n' at fixed h_n. The same one-dimensional lower-semicontinuity argument as N876 forces the limiting I to be zero, hence h=0. The rank-one Bregman estimate applied to h_n' then makes h_n' tend strongly to zero, contradicting N=1. Thus a positive margin exists uniformly on every bounded omega interval.

### 3.3 Uniform control as |omega| tends to infinity

Write Omega=|omega|, sigma=sign(omega), y=Omega*theta, and

    g(y)=Omega*h(y/Omega).

The leading gradient is

    A_0=[sigma J_0 g | g_y] R_theta^T, theta=y/Omega,

and the actual gradient adds [g/(2Omega)|0]R_theta^T.

At fixed theta minimize the rank-one-column energy in the second-column direction parallel to the first. Its scalar polynomial is

    P_theta(nu)=alpha(1+nu²)²+beta(cos theta-nu sin theta)⁴.

It has a unique smooth minimizer nu(theta), because P_theta''>=4alpha>0. Set

    q_theta=cos theta-nu(theta) sin theta,
    mu_sigma(theta)=sigma*[4alpha(1+nu²)-r*q_theta²].

At g=a e1 the radial derivative of
J([sigma J_0 g | a(t e1+sigma nu e2)]R_theta^T)/a⁴ at t=0 is exactly mu_sigma. The derivative in the direction sigma J_0 g vanishes by minimization in nu. By left target invariance, the remaining derivative for arbitrary g is radial. The rank-one Bregman bound therefore gives, for every g,v,

    J([sigma J_0 g | v]R_theta^T)
      >=P_theta(nu)|g|⁴
        +mu_sigma(theta)|g|² g dot v
        +(alpha/3)|v-nu sigma J_0 g|⁴.

This is the decisive compatible calibration. The middle term is not discarded pointwise. With v=g_y, periodicity gives exactly

    integral mu_sigma(theta)|g|² g dot g_y dy
      =-(1/(4Omega)) integral mu_sigma'(theta)|g|⁴ dy.

Thus the potentially negative circulation term is small at high frequency.

For explicit constants, put

    Lnu=sqrt(sqrt(1+beta/alpha)-1),
    Vnu=(beta/alpha)(1+Lnu)²(3+2Lnu),
    M1=8alpha Lnu Vnu+2|r|(1+Lnu)(1+Lnu+Vnu).

The minimizer equation is

    alpha*nu(1+nu²)=beta*sin theta*q_theta³.

It yields |nu|<=Lnu and |nu'|<=Vnu, hence |mu_sigma'|<=M1. For Omega>=M1/(2alpha),

    integral J(A_0)
      >=(alpha/2) integral|g|⁴
        +(alpha/3) integral|g_y-nu sigma J_0 g|⁴.

Also

    |A_0|⁴ <=(2+16Lnu⁴)|g|⁴
              +16|g_y-nu sigma J_0 g|⁴.

Define

    gamma0=min{alpha/[2(2+16Lnu⁴)], alpha/48},
    Cgrad=16alpha+4beta+1+2|r|.

The polynomial derivative bound |DJ(A)|<=Cgrad|A|³ follows separately for H,u²,j²,uj. For Omega>=1, the perturbation in the first column changes the energy by at most

    [27 Cgrad/(16Omega)] integral|A_0|⁴.

Therefore, for

    Omega>=max{1,M1/(2alpha),27 Cgrad/(8gamma0)},

    I_omega(h)>=(8gamma0/81) N_omega(h).

This is a positive explicit high-frequency bound for every angular profile, not a sample over h. Together with bounded-frequency compactness it proves the claimed positive all-frequency logspiral margin.

### 3.4 Annular consequence and its boundary

Multiplying these fields by the old inner/outer radial cutoffs on a log annulus of length T gives

    integral J(Dphi_T)=T I_omega(h)+O(N_omega(h)),
    integral|Dphi_T|⁴=T N_omega(h)+O(N_omega(h)).

The transition estimates are uniform in omega after normalization N_omega(h)=1: the cutoff adds a multiple of h, while the norm already controls h, omega*h, and h'. Thus no zero-margin sequence exists in this logspiral class at B=0, even with omega_T and h_T varying.

At fixed nonzero B and N_omega(h)=1, radial L2/L3 cross-term bounds are again uniform and O_B(1), so the normalized annular conclusion persists. Arbitrary shrinking amplitudes or growing B_T still require the old explicit amplitude/cross-term condition. General log-dependent changes of angular shape h(s,theta) are not covered by a constant target rotation rate.

## 4. Multiple contacts and laminate depth

The two exact acoustic background families are proportional to target rotations of I and K_r=[[0,(2r+1)/3],[1,0]]. They are distinct for every fixed r<-2. A simple laminate has rank-one-valued perturbation and is already excluded. Iterating the rank-one Bregman lemma along a rank-one martingale of depth n gives

    E J(A_n)-J(B)>=(alpha/3) E sum_k |d_k|⁴.

Since |sum_k d_k|⁴<=n³ sum_k|d_k|⁴, a fixed-depth laminate has margin at least alpha/(3n³). This elementary bound deteriorates with depth. It does not exclude an increasing-depth compatible laminate construction, or a nonlaminate rank-two concentration. The two-contact geometry alone does not supply a uniform depth-independent bound.

## 5. Evidence and exact remaining scope

Run

    python3 exact_and_candidate_checks.py

from this directory. `EXACT_SUPPORT_RECEIPT.json` records exact SymPy polynomial identities for the contact cubic, slow-fast block scaling, and both signs of the logspiral calibration. These checks support the written arguments; they do not verify the analytic limiting and compactness steps.

`COMPATIBLE_CANDIDATE_DIAGNOSTICS.json` tests one fixed periodic f at r=-5/2, with exact-in-exact-arithmetic trigonometric quadrature and floating-point affine minimization. The full affine ratio tends to the positive limiting formula derived in section 2. It supplies no global lower bound and no non-QC or zero-margin witness. Increasing this grid or Fourier cutoff alone would not discharge the remaining gate.

The global affine-minimized residual

    K(q)-L(q)^T M(q)^+ L(q)/4

is still not controlled uniformly over all compatible rank-two q. The genuinely unclosed possibilities include changing-profile slow-fast sequences whose Schur constants collapse, general shape-changing log-radial patterns, concentration at more than one interacting scale, and increasing-depth laminates. The logspiral result removes one explicit larger concentration family; it does not justify an N866 storage transfer or a claim of general coercivity.
