# A finite-ring normalized-purity certificate from a thermal amplitude

The target is the actual spin-two periodic Heisenberg Hamiltonian
H_n=sum_i S_i dot S_(i+1), with no noise or reset. Its local bond spectrum is
{-6,-5,-3,0,4}. The certificate below is rigorous at its stated input scope.
The implemented small-collar input does not meet it. In particular, the
accurate ansatz readout is not an acquired target Gibbs purity.

**1. The all-Schatten residual inequality.** Let H be any finite-dimensional
Hermitian matrix and let A(s), 0<=s<=beta, be differentiable and invertible,
with A(0)=I. Define the left multiplicative residual

    E(s)=(A'(s)+H A(s)/2) A(s)^(-1),
    nu=integral_0^beta ||E(s)|| ds,
    eta=exp(nu)-1.

Then for every 1<=p<=infinity,

    ||A(beta)-exp(-beta H/2)||_p
        <= eta ||exp(-beta H/2)||_p.                         (1)

Here the norm on E is the operator norm. The same E and nu work for every p;
no unacquired tail estimate is substituted for a norm.

Proof: A'=(-H/2+E)A, so its convergent Dyson expansion about -H/2 has kth
error term equal to the integral over beta>=s1>=...>=sk>=0 of

    exp(-(beta-s1)H/2) E(s1) exp(-(s1-s2)H/2) ... E(sk) exp(-sk H/2).

For p<infinity use Schatten Holder with exponent p*beta/t_j on each
exponential factor of duration t_j, and infinity on every E. Since the
nonnegative durations sum to beta, the product of the exponential norms is
exactly ||exp(-beta H/2)||_p. Thus the kth term is bounded by that norm times
nu^k/k!. For p=infinity the same statement follows directly from the minimum
eigenvalue of H. Summing k>=1 proves (1). Zero durations are interpreted by
continuity. Finite dimension and an integrable residual justify the series.

There is no extensive exp(beta ||H||) factor. This is a derived perturbation
certificate using ordinary Dyson expansion and Holder; no priority claim is
made for those tools. Its hard input is the acquired multiplicative residual,
not merely a small Hilbert-Schmidt truncation at an earlier temperature.

**2. One amplitude supplies both temperatures in normalized purity.** Let
B=exp(-beta H/2), and define the positive normalized ansatz

    sigma_A=A A*/Tr(A A*).

The target thermal purity and the ansatz purity are

    T_H(beta)=Z_H(2beta)/Z_H(beta)^2=||B||_4^4/||B||_2^4,
    P_A=Tr[(A A*)^2]/Tr(A A*)^2=||A||_4^4/||A||_2^4.

If eta<1, applying (1) to p=2 and p=4 gives

    ((1-eta)/(1+eta))^4 <= P_A/T_H(beta)
        <= ((1+eta)/(1-eta))^4,                              (2)

and hence

    |log P_A-log T_H(beta)|
        <=4 log((1+eta)/(1-eta)).                            (3)

This does not assume a separately acquired approximation at 2beta. All trace
normalization is included. An error epsilon in log purity is guaranteed by

    nu <= log(1+tanh(epsilon/8)).                            (4)

For the accepted A4 restart the first-pair log-purity budget is approximately
7.44047619e-7, after reserving 3e-22 for the propagated warm initial error.
Equation (4) requires nu<=9.300594805589878e-8. The ring256/ring512 pair has
the same global tolerance. `rung_residual_budget.py` encloses all fourteen
pair budgets with interval arithmetic. The additional final T(512,96) still
needs an acquired lower bound; no point purity is assumed.

**3. A concrete entangled block amplitude has an exactly local residual.**
Partition the even periodic chain into blocks of length b>=2ell+2. Let H0
contain every within-block bond and V_j the single missing bond at block seam
j. Around seam j retain ell sites on each side. Write K_j for the within-
collar bonds excluding V_j, and L_j=K_j+V_j. Define

    C_j(s)=exp(-s L_j/2) exp(s K_j/2),
    P(s)=product_j C_j(s),
    A(s)=P(s) exp(-s H0/2).                               (5)

Different collars are disjoint. Each C_j is invertible, A(0)=I, and this is
an explicit amplitude, rather than supplied large-ring Gibbs marginals.
Let W_j be the two within-block bonds immediately outside collar j. The block
size condition makes each W_j commute with every C_k for k!=j. Farther bonds
commute with every collar factor. Differentiating (5) therefore gives exactly

    E(s)=sum_j e_j(s),
    e_j(s)=[W_j,C_j(s)] C_j(s)^(-1)/2.                    (6)

Indeed, C'_j C_j^-1=-L_j/2+C_j K_j C_j^-1/2 cancels all internal collar
terms in (A'+H A/2)A^-1. The remaining conjugated H0 terms are precisely W_j.
No global inverse is numerically supplied: the inverse in each e_j is the
known finite product exp(-s K_j/2) exp(s L_j/2).

Reflection equates the two one-edge commutator norms. Thus for m seams,

    ||E(s)|| <= m mu_ell(s),
    mu_ell(s)=||[h_out,C_ell(s)] C_ell(s)^(-1)||.           (7)

One-edge mu acts on only 2ell+1 physical spins. Every constituent is SU(2)
invariant. Therefore its squared singular-value operator commutes with
SU(2), and each integer-spin irrep has an M=0 vector. The complete norm is
present in its M=0 restriction: dimension19 at ell1 and381 at ell2. This
argument counts every representation; it is not a restriction to a favourable
magnetization sector. The five local collar sectors M=-2,...,2 used by the
code are exactly those needed when the added outside spin has M=-M_collar.

The same locality calculation applies to any differentiable invertible local
factor O_j, with an additional inside residual

    D_j=O'_j O_j^-1+L_j/2-O_j K_j O_j^-1/2.

This is used to test the ordinary bounded quantum-belief-propagation gauge.
It prevents mistaking a bounded local factor for a small temperature residual.

**4. The ring readout is a closed entangled transfer, including the square.**
The executed case is ell1,b4,n=4m. Then K_j=0 and C_j=exp(-beta V_j/2).
Let Gamma=exp(-beta H_open,4) on each block and F=exp(-beta h) across each
seam. In the bipartite Marshall basis both are entrywise nonnegative. Set
Gamma0=the tensor product of all Gamma and F_all=the tensor product of the
disjoint seam F factors. The amplitude in (5) satisfies exactly

    Tr(A A*)=Tr(Gamma0 F_all),
    Tr[(A A*)^2]=Tr(Gamma0 F_all Gamma0 F_all).             (8)

The second identity follows by cyclicity from
A A*=P Gamma0 P*, with P=P*=the product of exp(-beta V_j/2) and P^2=F_all.
It does not square a traced-out central marginal.

Here are the transfer indices explicitly. A four-site block is ordered
(left endpoint, central pair, right endpoint). Endpoint indices a,b,c,...
have five values, and the central-pair indices x,y have25 values. Factor F as

    F=sum_r L_r tensor R_r,
    r=(u,v), L_r=|u><v|, R_r[z,w]=F[u z,v w].

All25 matrix-unit factors are retained. Define the25-by-25 transfer

    T1[p,r]=sum_(a,b,c,d,x)
        Gamma[a x b,c x d] R_p[c,a] L_r[d,b].              (9)

For the squared density define the625-by-625 transfer

    T2[(p,q),(r,s)]=sum_(a,b,c,d,e,f,g,h,x,y)
        Gamma[a x b,c y d] Gamma[e y f,g x h]
        R_p[c,e] R_q[g,a] L_r[d,f] L_s[h,b].               (10)

The central indices cross between the two Gamma factors. This is the part
that would be lost by replacing a block by its one-copy endpoint marginal
and then squaring. Summing the seam labels between consecutive blocks,
including the seam from block m back to block1, gives

    Tr(T1^m)=Tr(A A*),
    Tr(T2^m)=Tr[(A A*)^2],
    P_A=Tr(T2^m)/Tr(T1^m)^2.                             (11)

These are full matrix traces; no leading-eigenvalue approximation or
overcomplete-frame projection is used. The actual source four-site check
independently applies the closing two-site operator to all625 physical basis
columns and agrees with (9)--(11). A separate eight-site spin-half control
checks the multiple-cut residual identity; it is only an index/locality
control, not evidence for a spin-two cold input.

For general ell, a dense implementation has endpoint operator dimension
5^(2ell) for the one-copy transfer and5^(4ell) for the squared-density
transfer. These costs are not assumed away. At ell2 the latter matrix has
dimension390625 and requires about1.22TB merely to store binary64 entries.
A useful wider-collar method would need an acquired structured contraction
or compression, including its omitted-mode/error bound.

**5. The supplied readout enclosures pay local and global numerical errors.**
The readout uses the true open four-spin Hamiltonian and the true seam bond.
It does not use the earlier quadratic reflection-positive gate. For b=2,4,

    B_b=4(b-1)I-H_open,b^Marshall >=0 entrywise,
    exp(-beta H_open,b)=exp(-4(b-1)beta) exp(beta B_b).

Every nonzero B entry is an integer or sqrt6. The saved code checks a rational
relative enclosure of the rounded sqrt6 by squaring its rational bounds.
It evaluates exp(beta B_b) by scaling to beta||B_b||_infinity<=2, a positive
Taylor polynomial of degree80, and repeated squaring. The entire physical
dimension5^b is included. Structural magnetization zeros are checked, and
every allowed entry is positive after the Taylor evaluation.

The matrix Taylor remainder per entry is bounded by

    8*2^81/81!.

The constant8 follows from exp(2)<8; for example the Taylor sum through
degree4 is7 and its remaining tail is at most (4/15)/(1-1/3)=2/5. The
per-bond bound ||4I-h^Marshall||_infinity<=10 is checked with a rational
upper bound for sqrt6, so ||B_b||_infinity<=10(b-1) has no fitted constant.
The
remainder is converted to a relative bound using the acquired minimum
positive polynomial entry. The term recurrence, positive sum, and repeated
squarings have their rounding bounds charged. Scalar bounds are Fractions,
rounded upward to a100-bit dyadic only when needed to prevent integer-size
growth. No rounded eigensolver output enters these enclosures.

The arithmetic model is IEEE754 binary64 round-to-nearest, with no overflow
or subnormal products in the counted operations. The implementation uses
explicit NumPy float64 multiplication and addition kernels for every positive
matrix product, rather than relying on a BLAS contraction order. A length-k
positive dot product is bounded by gamma_(2k), gamma_r=r*u/(1-r*u),
u=2^-53. Source normal-product checks are executed. The sparse Taylor multiply
has at most its checked row-nnz count. The transfer construction has fewer
than4000 accumulated positive dot/add operation depths along any term, giving
the deliberately loose gamma_4000 allowance in addition to local input error.

All rescalings are exact powers of two. Their scalar factors cancel from
(11): a factor c_G c_F appears per block in T1 and its square per block in
T2. Omitting those scalars would not be permitted for an absolute partition
function; the present output is explicitly the normalized purity.

Transfer powers use positive matrix multiplication and binary rescaling.
Entries below2^-400 are clipped before the next product. Their entire mass
is retained as an absolute error bound. In particular, clipping is not an
unreported sector/mode truncation. If exact normalized factors satisfy

    a_- Xhat-delta_X J <= X <= a_+ Xhat+delta_X J,

and analogously for Y, then with d the contracted dimension the product has
an absolute uncertainty at most

    d [a_+ max(Xhat) delta_Y+b_+ max(Yhat) delta_X
       +delta_X delta_Y],

in addition to its positive relative multiplication bound. The same symmetric
absolute bound is valid for the lower product: use positivity of the exact
factors when expanding around the lower matrix bounds. The code propagates
these rational coefficients through every rescaling/product, then pays the
trace sum and converts the final positive rational ratio to an interval
logarithm. Every transfer mode is included or explicitly bounded by this
clipped-entry tail.

Ten exact rational small-matrix power controls, including entries below the
clip threshold and powers through128, independently replay the enclosure
recurrence. The source four-site density check tests the physical tensor
indices separately. These controls do not turn an ansatz interval into a
target Gibbs interval.

**6. This particular small-collar certificate provably misses the cold rung.**
The failure is stronger than the numerical local norm samples. In the one-
magnon sector of a four-spin cell, use the basis in which the spin lowered
from2 to1 is at positions0,1,2,3. The central bond V=h_12 has matrix

    [4 0 0 0; 0 2 2 0; 0 2 2 0; 0 0 0 4].

For W=h_01+h_23, C(s)=exp(-s V/2), the local residual is
e(s)=(W-C W C^-1)/2. Since V has only eigenvalues0,4 in this sector, the
projectors I-V/4 and V/4 give an exact expression for C and its inverse.
With t=exp(s), the (1,0) entry of Herm(e) is

    -(t^2+t^-2-2)/4=-(cosh(2s)-1)/2.                     (12)

Thus ||Herm(e)||>=(cosh(2s)-1)/2. The block4 seam cells are disjoint and
identical. Extreme eigenvalues of their Hermitian parts add on tensor
products, so

    ||E_total(s)||>=||Herm(E_total(s))||
        >=(n/8)(cosh(2s)-1),
    nu>=(n/4)[sinh(2beta)/4-beta/2].                     (13)

At beta3/4 this is greater than10.068471281517077 for n256, and greater
than20.136942563034154 for n512. Both vastly exceed the approximately
9.30e-8 global budget. `exact_small_collar_limit.py` checks the finite source
matrix identities symbolically and encloses the scalar integrals. This rules
out using certificate (1)--(4) with this particular amplitude. It does not
prove a corresponding lower bound on its true purity error, or exclude a
different amplitude, wider collar, physical thermal method, or the gap.

**7. The executed repair and remaining cost.** Direct local imaginary-time
expansionals were evaluated at ell1 andell2. Their unweighted norms grow
sharply by beta1.5. The ordinary bounded QBP collar was then actually
constructed: for coupling lambda, H_lambda=K+lambda V, its generator in the
energy basis is

    g_beta(omega)=-tanh(beta omega/2)/omega,
    d_beta g_beta(omega)=-(1/2)sech^2(beta omega/2),

with continuous values at omega0. Integrating the coupled equations for O
and d_beta O gives the factor and its temperature derivative. The code checks
O exp(-beta K) O*=exp(-beta L) locally. The extra D_j term in section3 is
included when assessing this factor; simply quoting ||O||<=exp(beta||V||/2)
would miss it. The tested ell2 QBP factor reduces the large raw-factor growth
at beta1.5 but still has a substantial residual. Those ODE/norm values remain
numerical discovery data, not an accepted norm enclosure or target purity.

The operation (1)--(11) specifies a complete readout and a source-local
certificate input with explicit dimensions, rather than supplied noise,
product-state frames, or assumed pressure constants. The actual small-collar
input fails. A larger entangled amplitude must acquire its residual and its
closed squared-density contraction within the stated budget; those costs
are not supplied by this proof.

**8. A separate, coarse bracket concerns the true Gibbs purity.** This
corollary does not use a small residual or equate the ansatz to the target.
It uses the parent-accepted warm logZ bounds at beta1/2 and3/4, whose selected
rows and source hashes are frozen in `sources/ACCEPTED_WARM_LOGZ.json`.

For positive X,Y the ordinary Araki--Lieb--Thirring trace inequality gives,
for0<r<=1 andq>0,

    Tr[(X^r Y^r X^r)^q] <= Tr[(X Y X)^(r q)].

Set X=exp(-beta H0/2), Y=exp(-beta V), q=2/r, and let r decrease to zero.
The finite-dimensional Lie product formula gives exactly

    Z_H(2beta)<=Tr[(exp(-beta H0) exp(-beta V))^2].         (14)

This is the two-slice Golden--Thompson/Trotter upper bound, not a new trace
inequality. The right-hand side is precisely Tr(T2^m) from section4 with
all physical scalar factors restored. The weaker one-slice upper
Tr(exp(-2beta H0)exp(-2beta V)) is also computed. It is at least (14), since
their difference is half the Hilbert-Schmidt norm squared of the commutator
of exp(-beta H0) and exp(-beta V).

Restoration of the scalar factors is material. The local exponential routine
records the integer k for every power-of-two normalization; after a square,
k_new=2k+k_rescale. For b4 and a base inverse temperature beta,

    log Z_GT1(beta)=log Tr(T1^m)+m(k_G+k_F)log2-4n beta,
    log Z_ALT2(2beta)=log Tr(T2^m)+2m(k_G+k_F)log2-8n beta. (15)

The exp[-4(b-1)beta] block factors and exp[-4beta] cut factors are both
present in (15). The unscaled transfer trace is never used as an absolute
partition function. Independent full625-state calculations check both
restored absolute traces and the true-Z<=ALT2<=GT1 direction on the physical
four-site source.

Write g(t)=log Z_n(t). Finite-dimensional Gibbs convexity, g''(t)=Var_t(H)>=0,
implies

    g(3/2)>=4g(3/4)-3g(1/2),
    log T_n(3/4)>=2g(3/4)-3g(1/2).                       (16)

The ALT2 upper on g(3/2), together with the acquired lower on g(3/4), supplies
the upper bound on log T. Endpoint propagation uses exact binary values of
the outward warm endpoints and interval logarithms; the n log5 terms in the
source's normalized-Z convention are explicitly restored. The actual output,
rounded further outward here, is

| ring | lower log T_n(3/4) | upper log T_n(3/4) |
| ---: | ---: | ---: |
| 256 | -186.543892386 | -73.667364671 |
| 512 | -373.087784772 | -147.334729342 |

These are genuine bounds for the uniform spin-two Gibbs state, with all
sectors and all closed-transfer modes counted. Their widths are about112.88
and225.75, respectively, compared with the required approximately7.44e-7.
They do not acquire either first-pair input for the dyadic lift. The much
narrower intervals for P_A remain ansatz intervals, not interchangeable
target intervals. `coarse_true_purity.py` keeps the weaker GT1 comparator,
the stronger ALT2 value, and this failed precision test in the same output.
