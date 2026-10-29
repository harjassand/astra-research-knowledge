# Direct complex marks for Maxwell sampling

29 October 2026. Root construction, independent review PENDING. Same centered
covariance-mixture Maxwell equation as t_collision_operation. Supplied
independent covariance law aI<=Sigma_0<=bI, 0<a<b<infinity. This is an ideal
real/random operation, not finite-bit exact output, native gas or novelty.

## 1. Complex query and branching

For Haar R in SO(3), A=(I+R)/2, B=(I-R)/2, the ordinary collision smoothing
is Sigma_new=A Sigma_1 A^T+B Sigma_2 B^T. AA^T+BB^T=I preserves the interval.
Set c=(a+b)/2, h=(b-a)/2, E=(Sigma-cI)/h, so E is real symmetric, ||E||<=1.
For complex Hermitian-unit z, estimate F_q(z,t)=E[(z^T E_t z)^q], using
TRANSPOSE inside the quadratic form. Its absolute value is <=1.

At block (q,z,t), q>=2, draw S~Exp(1). If S>=t, return (z^T E_0 z)^q from
a fresh initial draw. Otherwise draw Haar R, set U=||A^Tz||^2 and
1-U=||B^Tz||^2, and draw J~Binomial(q,U). Normalize occupied child vectors
z_A=A^Tz/sqrt(U), z_B=B^Tz/sqrt(1-U). Split into independent J and q-J
blocks if 0<J<q, multiplying outputs. Otherwise continue the occupied child
with unchanged q and time t-S. Do not normalize unused zero vectors.
The binomial identity for z^T E_new z proves the correct gain.

Compress q1 algebraically. Covariance evolution is
M_t=e^(-t/2)M_0+(1-e^(-t/2))(Tr M_0/3)I. Draw E_0; with probability e^(-t/2)
return z^T E_0z, otherwise (Tr E_0/3)z^Tz. Both have modulus <=1 and the right
mean. Every resulting product therefore has modulus <=1.

## 2. The uniform separation operation

Write z=u+iw, ||u||^2+||w||^2=1. Pointwise U=||u||^2 U_u+||w||^2 U_w, where
U_u=||A^T(u/||u||)||^2 is Uniform[0,1] marginally (and likewise for w).
The marginals can be correlated. Convexity of x^q+(1-x)^q gives

    Pr(J=0 or q | z)<=2/(q+1).

Thus every attempted collision separates with conditional probability >=1/3
for q>=2, uniformly over changing complex directions. Time termination only
reduces attempts. There are <=q-1 splits, <=2q-1 blocks, <=3(q-1) expected
collision draws, and <=q initial draws. Terminal power work is O(q).
First-collision conditioning plus the exact q1 closure proves unbiasedness;
bounded mild solutions are unique by ordinary gain-Lipschitz iteration.
Call the bounded unbiased complex result H_q(z,t). Expected ideal work is
O(q), independent of finite elapsed time; worst-case work is unbounded.

## 3. Full-density ratio with no covariance-contrast restriction

For proposed v from Gaussian G_b, draw xi~N(0,a^-1 I), z=xi-i v/b,
r=||z||, K~Poisson(h r^2/2), and C=(b/a)^(3/2). Put H=1 for K0, otherwise
draw H_K(z/r,t). Return

    W(v)=C Re[(-1)^K exp(i(c/b-1)xi.v) H].            (1)

Then |W|<=C and E W=f_t(v)/G_b(v) for EVERY finite positive a,b.

Shift the covariance-mixture Fourier contour to xi-i v/b. The base cI
contributes phase exp(i(c/b-1)xi.v) and v factor
exp[-(b-c)|v|^2/(2b^2)]. Expand exp[-h z^T E_t z/2]; direct complex marks
estimate each normalized power with modulus one, with no 4^q polarization.
Poissonization contributes exp(h||z||^2/2). The frequency part changes
precision c to c-h=a, and the velocity part cancels since b-c=h. The
remaining factor is C. Positive a pays absolute Gaussian domination,
contour shift and Fubini. No radial closure or angular quadrature is needed.

Independently each covariance in [aI,bI] has G_Sigma/G_b<=C by determinant
and inverse ordering; hence 0<=R(v)<=C. Conditional expected degree is

    E[K|v]=(h/2)[3/a+|v|^2/b^2],

averaging to (3h/2)(1/a+1/b) under proposal G_b. Input covariance draws and
all collision work are paid by this degree and the supplied initial draw cost.

## 4. Exact ideal sampling if b<2a

The ordinary lower envelope R(v)>=ell(v)=exp[-|v|^2(1/a-1/b)/2] and a W
query give a p-coin with p=(1-R/C)/2. Huber1308.1562v2's multiplier2 factory,
margin ell/C, complemented, produces an acceptance coin of mean R/C using
<=19C/ell queries on average. Repeated independent G_b proposals return
exact iid f_t velocities in the ideal model. Full expected cost integrates:

    I=integral G_b/ell=[a/(2a-b)]^(3/2),
    E queries/output<=19 C^2 I,
    E degree/output<=19 C^2 I (3h/2)[1/a+a/(b(2a-b))].

This improves the old sufficient b<7a/5 to b<2a. Divergence of this bound
beyond 2a is not a no-go. Stopping/renewal charges rejected proposals and
outcome-correlated query work: a fresh query is requested using only previous
outcomes. Its conditional mean cost is therefore charged correctly.

## 5. Positive approximate iid sampling for ARBITRARY contrast

For each v~G_b draw FIXED M independent W queries. Put
Y=clip(mean(W),0,C), and accept with probability Y/C. Clipping is 1-Lipschitz
and R in [0,C], so E|Y-R|<=sqrt(Var(W)/M)<=d=C/sqrt(M).
Let gtilde(v)=G_b(v)E Y and alpha=integral gtilde. Then
||gtilde-f_t||_1<=d and |alpha-1|<=d. The accepted density is gtilde/alpha,
with

    TV(gtilde/alpha,f_t)<=d/(1-d).

M>=C^2(1+epsilon)^2/epsilon^2 gives TV<=epsilon. Repetitions are iid from
this one approximate law. No lower envelope or factory is required.
Expected proposals<=C/(1-d), queries<=CM/(1-d), and degree<=that times
(3h/2)(1/a+1/b). These costs include rejections and are uniform in elapsed
time. This is ordinary clipped-mean positivity applied to the new bounded
query, not a new generic Monte Carlo theorem. The cost grows with b/a and
1/epsilon; it is not constant in requested accuracy.

Both samplers use ideal continuous primitives/arithmetic. Floating consumers
are diagnostics. Certified quantized output, fair-bit work, initial-law
fitting, non-Maxwell/spatial kernels and many-particle trajectories remain
distinct interfaces. Exact short-time Wild sampling and ordinary moment
hierarchies remain strong alternatives. World novelty remains UNKNOWN.
