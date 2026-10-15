# Localized positive regularization and its moment price

Root reconstruction, 2026-10-15. Internally proved corollary candidate; historical originality unresolved. This extends the moment-domain interpretation of the already supplied PR94 cone theorem, rather than claiming a new infinite-dimensional criterion.

Let E be a real Banach space, C a closed convex cone with nonempty interior, e in int C, and T an E-valued compactly supported distribution with T(1)=e. Write H(g)=T(exp(g·y)). Fix a>0. Then the following are equivalent:

1. H(g) belongs to int C for every |g|<a.
2. There is a smooth positive radial strictly log-concave scalar probability density p for which T*p is C-positive and the set of finite exponential moments of p is exactly the open ball |g|<a.

Every derivative of p, and of T*p in norm, is integrable against exp(g·x) for |g|<a. The conclusion concerns existence, not an efficient procedure for accessing positivity margins.

## Necessity

The compact-test cutoff proof in PR94, Section 3, requires only the single moment m_p(g)<infinity at the point being tested. Choose nonnegative increasing smooth cutoffs chi_R. Distributional convolution and the finite-order compact seminorm imply in norm

    (T*p)(exp(g·x) chi_R(x)) -> m_p(g) H(g).

At g=0 the corresponding limit is e, so for some finite A the element Q_A=(T*p)(chi_A) is interior. For R>=2A,

    exp(g·x) chi_R(x) >= exp(-2A|g|) chi_A(x).

Cone positivity and closedness therefore put m_p(g)H(g) above an interior cone element. Since m_p(g)>0, H(g) is interior. No moment at -g or analytic continuation is required.

## Sufficiency: bounded slow slope in the existing proof

Retain the finite-order bound ||T(h)|| <= C_T ||h||_{C^N(B_b)} and the compact-tilt interior margin mu(t)=min_{|g|<=t} dist(H(g),E\C)>0, for t<a. Let q_n=a(1-2^{-n-1}), n>=0. Choose a fixed smooth monotone step theta, zero below zero and one above one. Define

    q(s)=q_0 + sum_{n>=1}(q_n-q_{n-1}) theta(s-S_n), s>=0.

The finite thresholds S_n can be chosen at least two apart and sufficiently large that

    G(q(s)) <= C_G exp(s/2),
    G(t)=max(1, exp(b t)(1+t)^{N+1}/mu(t)), q_0<=t<a.

Indeed, during the nth transition and following plateau q(s)<=q_n, so it suffices to impose S_n>=2 log G(q_n). All derivative orders of q are uniformly bounded; q_0<=q(s)<a and q(s)->a.

Set rho(z)=sqrt(1+|z|^2), f(z)=integral_1^{rho(z)} q(log v) dv, V_L(x)=L f(x/L), p_L=exp(-V_L)/Z_L. Exactly as in PR94 Sections 5–6,

    D^2 f = q D^2 rho + (q'/rho) grad rho tensor grad rho >0,
    |D^k f| <= C_k q(log rho) rho^{1-k}, k>=2.

With g=grad V_L(x), the local logarithmic remainder F_x(y)=V_L(x-y)-V_L(x)+g·y satisfies

    ||F_x||_{C^N(B_b)} <= (C_0/L)(q(s)+1) exp(-s), s=log rho(x/L).

The product and chain estimates consequently give

    (T*p_L)(x)/p_L(x) = H(g)+E_x,
    ||E_x||/mu(q(s)) <= (C_1 C_G/L) exp(-s/2).

Choose finite L so this ratio is less than any specified epsilon in (0,1). Homogeneity of the interior distance gives the cone sandwich (1-epsilon)p_L H(g) <=_C T*p_L <=_C (1+epsilon)p_L H(g). Thus positivity follows globally, including remote tails.

Finally V_L(x)/|x| -> a, while V_L(x)<=a|x|. For |g|<a, choose |g|<b'<a and use V_L(x)>=b'|x|-C outside a ball to prove finite moments. All derivatives of p_L are bounded by constants times p_L because all positive-order jets of V_L are bounded. The same weighted norm statement for T*p_L follows from the compact-distribution seminorm and local integral estimates.

For |g|=a, write x=t u+z, u=g/a, t>=1, z perpendicular to u and |z|<=1. Then

    g·x-V_L(x) >= a t-a sqrt(t^2+|z|^2) >= -a/(2t).

Integrating over this infinite cylinder proves divergence. Outside the ball the same cylinder proves divergence. This establishes the exact open moment domain, including the boundary.

## An explicit sign-changing Laplace symbol

In one dimension set T=delta_0-a^{-2} delta_0'', so H(g)=1-g^2/a^2. Its transform is positive precisely for |g|<a and zero at the endpoints. The logistic density

    p(x)=(a/4) sech^2(a x/2)

has exact moment domain (-a,a), and direct differentiation gives

    T*p = p-a^{-2}p'' = (3a/8) sech^4(a x/2) >0.

Both integrate to one. Thus no all-exponential noise can regularize this T, while finite-domain noise does. Its output has the larger moment domain (-2a,2a): positive convolution can cancel a boundary singularity of the scalar noise transform. This is an explicit illustration, not a historical novelty claim about logistic identities.

## Consequence and limits

Define a_* as the supremum of radii a for which H is interior on the open ball B_a. The theorem identifies the largest open-ball exponential-moment domain obtainable by radial strict log-concave positive regularization, in the supremal sense. It does not claim attainment of a_* with finite moments at its boundary, efficient computation of a_*, or measurement advantage. General anisotropic domains need a separate argument; they are not implied by replacing the Euclidean norm in this proof without controlling the potential's higher jets.
