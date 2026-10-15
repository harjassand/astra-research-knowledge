# Universal negative-branch QC and contact-face audit

15 October 2026. Separate continuation; the earlier interval and tangent
audit files are preserved unchanged. Same-team internal review only.

Author report SHA-256:
`db2b42e895e4e01df8be72225e83600a040b6cff936d0df37a8d32a738a8e61b`.
Universal JSON SHA-256:
`f45149312e694f6080a179b77d322aceabf0d7c2a55ed60c5e102037e55f6ee7`.
Independent exact audit report SHA-256:
`4d5bd9fcee7977079274391f84e8fb72120fbb8cca8da346b8066de1e4217210`.

**Verdict:** the fixed-parameter heat-to-QC proof and its extension to the
entire delta<=0 contact-face sector are valid. The independent algebra auditor
reports exact all-branch PASS for the coefficient identity, closure/primitive,
denominators, diffusion, kernel/complement, rational congruence, off-block
zeros and recomputed LDL pivots. This audit reconstructs the analytic
consequence and its quantifiers. No required correction to the frozen author
report was found. External correctness, formal verification and priority are
unresolved.

## 1. Fixed r is the correct analytic quantifier

For every finite real r<-2 the diffusion is

    d1=(2r+1)/(r-1), d2=-3/(r-1), d1+d2=2.

Both are strictly positive. They are fixed constants during the heat proof.
As r tends to negative infinity, d1 tends to 2 and d2 tends to zero; there
is no ellipticity constant uniform over the branch. As r approaches -2,
the quartic coefficients themselves diverge. The author correctly does not
assert a uniform heat estimate, Gram lower bound, coefficient bound, or
quantitative Jensen constant over the unbounded parameter set.

For a fixed r, every certificate coefficient is finite. The closed
homogeneous quadratic two-form has the global cubic polynomial primitive
eta=i_A omega/4. Let B be any constant matrix, phi compact smooth, and
q_tau=D exp(tau(d1 partial_xx+d2 partial_yy))phi. The relative energy

    E(tau)=integral[J_r(B+q_tau)-J_r(B)-DJ_r(B):q_tau]

is finite and differentiable for tau>0. The primitive pullback contains
D2phi_tau; its coefficients converge to constants at spatial infinity,
where the derivatives decay rapidly. Thus its boundary flux vanishes and
the integrated form correction is zero. Integration by parts and the
verified positive corrected density give E'(tau)<=0.

Quartic growth is bounded by a fixed-r constant times

    |B|^2 ||q_tau||_2^2+|B| ||q_tau||_3^3+||q_tau||_4^4.

Anisotropic Gaussian convolution yields
||q_tau||_p<=C_(p,r) tau^(-(1-1/p))||Dphi||_1 for p=2,3,4, so E(tau)
tends to zero at infinite time. Strong L2,L3,L4 continuity at zero gives
E(0)>=0. The integrated linear term vanishes. This proves QC at every
affine background.

Strong W1,4 approximation on bounded Lipschitz domains passes the quartic
integrals, using
|J_r(B+X)-J_r(B+Y)|<=C_r(|B|+|X|+|Y|)^3|X-Y|.
Periodic heat and Stokes give the analogous periodic inequality. No
parameter-uniform estimate is needed for these pointwise-in-r conclusions.
The explicit acoustic test below the floor proves necessity, and convex
addition of (alpha-alpha_*)H proves sufficiency above it.

## 2. The entire negative-delta sector, including its closure

For F=alpha H+beta u^2+gamma j^2+delta u j, set

    P=[[6beta+delta,delta],[delta,gamma]],
    Q=[[8alpha,delta],[delta,2beta+delta]].

The independent acoustic proofs give P,Q>=0 as necessary conditions for
ROC, and QC implies ROC. If delta<0 and P,Q>=0, put

    p=6beta+delta, s=2beta+delta,
    rho=p/delta, lambda=delta^2/p,
    mu=gamma-lambda, nu=alpha-delta^2/(8s).

Because the off-diagonal delta is nonzero, PSD forces p,s>0. Also
rho+2=3s/delta<0, so rho<-2. Both mu and nu are nonnegative by the two
determinant inequalities. Exact matching gives

    F=lambda J_rho+mu j^2+nu H.

J_rho is QC by the fixed-r universal proof, j^2 is polyconvex, and H is
convex. Positive addition proves QC with the same affine/domain/trace
quantifiers. No division by zero occurs for delta<0.

At delta=0 the two LMIs reduce exactly to alpha,beta,gamma>=0, and the
nonnegative combination of H,u^2,j^2 is polyconvex. Thus the closed
delta<=0 sector is fully covered. This boundary is handled directly,
rather than by an unjustified limit of parameter-uniform heat estimates.
It proves QC iff ROC iff P,Q>=0 on this four-dimensional sector. It does
not prove that equivalence on the remaining positive-delta sector or the
whole nine-dimensional invariant space.

## 3. Non-PC, extreme and nonexposed statements need separate proofs

The universal heat report only asserts interval non-PC, conservatively.
The separate current `contact_face_priority_audit/STRUCTURAL_PROOF.txt`
supports the stronger synthesis claims. Its non-PC and dual-cone reasoning
was reconstructed in this audit as follows.

For every sharp J_r with r<-2 or r>0, a finite polyconvex representation
would have a supporting hyperplane at (I,1) in (A,det A). A finite lift
exists on all of R5: every point (A,z) is the midpoint of the minor lifts
of A+B,A-B for a matrix B with det B=z-det A. The support gap must have
PSD Hessian. Its e12 diagonal entry is zero, so its e12/e21 cross entry
forces the determinant multiplier to be lambda=r+2. Along the null
direction diag(1,-r-1), that gap has leading term

    -r(r+2)t^3/3,

nonzero on both allowed branches. One sign of sufficiently small t gives
a negative gap. Hence every such sharp ray is non-polyconvex. This proof
does not rely on pointwise negativity of J_r(I), which fails to hold on
parts of the negative branch. The cubic identity was also checked in
this auditor's `check_continuation_corollaries.py`.

Extremality holds in the nine-dimensional left-SO(2)-invariant ROC cone K,
as the earlier contact-face/rank-one-PSD proof shows. When QC is established
(currently r<-2), it is also extreme in the invariant QC subcone. No
unrestricted noninvariant extremality claim follows.

Nonexposure in K requires more than the two contacts alone. Normalize the
background, target and spatial vectors to unit length. Their acoustic
evaluations form a compact set T. The invariant quartic |A|^4 has every
such evaluation at least 4, so cone(T) is closed: it bounds the total
nonnegative mass of any convergent conic combination. Bipolarity and finite
dimensional Caratheodory then give K*=cone(T). The acoustic matrix of J_r
is nonsingular when both spatial components are nonzero; on the two axes
its only background kernels are span I and span A_r. At both contact
families the acoustic value of j^2 is zero. Therefore every nonnegative
functional on K that vanishes on J_r also vanishes on j^2. No such
functional can expose the sharp ray alone.

The sum of the two contact evaluations exposes exactly cone{J_r,j^2}:
the first places a ROC polynomial in the four-dimensional contact face;
the second fixes the rank-one kernel of Q, determining alpha,beta,delta
up to a nonnegative multiple of J_r, while P leaves precisely an additional
nonnegative j^2 coefficient. Since every supporting functional also kills
j^2, this is the minimal exposed face containing J_r. Inside the
four-dimensional contact face the ray itself is exposed by the two
block-kernel quadratic forms. These ambient-cone distinctions in the root
synthesis are mathematically correct.

No conclusion about QC of r>0 is inferred from its ROC, extremality,
non-PC, nonexposure or discrete elliptic symmetry.
