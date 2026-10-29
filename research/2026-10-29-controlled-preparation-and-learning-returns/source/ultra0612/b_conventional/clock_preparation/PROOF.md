# Cold conditional-clock preparation by number dressing and band filters

29 October 2026. Constructive theorem, independently whole-read and accepted
by root at the parameter-qualified scope; separate C challenge pending.
No Hamiltonian fixture, quantum state or trajectory is run.
The earlier clock gap, stability and full-trace thermal packages are unchanged.

## 1. The missing input and a different cold window

The input is an EXPLICIT finite-range clock Hamiltonian, conditional on
known source signs s,

    H_s(lambda)=N+lambda V_s,
    N=sum_i Q_i, Q_i=I-|0><0|_i.                            (1)

The single-clock dimension L and native rank/incidence/range are fixed.
The clocks have a uniform polynomial-growth spatial metric of dimension D.
All norm bounds are uniform in the known sign assignment; no sign
probability or hidden microscopic reset is supplied. Let n be the number
of clocks. The target is the FULL state

    sigma_t,s=exp(-t H_s)/Tr exp(-t H_s), t=beta Delta,
    Delta=1/(4lambda^L).                                    (2)

The dynamical task is conditional clock preparation, NOT the slow full
source logical sampler. No global n exp(-t gap) approximation is used.

**Proposed theorem.** For every fixed a>0 and B>0, sufficiently small fixed
lambda admits an explicitly constructed exactly stationary algorithmic
Lindbladian that prepares sigma_t,s from ANY initial clock state in
O(log(n/epsilon)) parallel update time, uniformly in s and in

    T0<=t<=B lambda^(-a).                                   (3)

Constants, the normal-form order and T0 may depend on fixed input bounds,
a,B,L,D, never on n or s. The native clock regime has a=L, B=beta/4 for
any chosen fixed physical beta. The coupling threshold in this proposed
theorem is not numerically qualified for a frozen literal clock recipe.

This is a quantum algorithmic preparation model, not a native passive
bath. Hamiltonian simulation, the finite-order dressing, filtering,
precision and the inverse dressing all have to be paid below. No initial
ground overlap or conditional clock-Gibbs oracle is assumed.

## 2. Strong ordinary comparators and their actual boundary

[Smid--Meister--Berta--Bondesan2510.04954v2, TheoremIII.3](https://arxiv.org/html/2510.04954)
already gives rapid mixing for weakly interacting qudits. Its displayed
criterion is L^2 eta<gap0; the eigenmode bound has a factor
L^2 exp(2t DeltaE), and AppendixA bounds the generator change by quantities
proportional to t|lambda|. Thus its phrase 'arbitrary temperature' does
not give a temperature-UNIFORM coupling promise in (2). The usual narrow
Gaussian filter also suppresses atomic downward transitions when t is huge.

[Zhan et al.2503.15827v3](https://arxiv.org/html/2503.15827) prove rapid
GROUND cooling for weakly interacting spins, using oscillator norms and
negative-frequency filters. Ground cooling alone does not prepare (2)
uniformly for all n. The present route adds exact KMS heating and controls
its coherent correction without paying t lambda.

The number-conserving transformation is ordinary finite-order local
Schrieffer--Wolff/prethermal theory. A stronger almost-exponential theorem
is [ADHH1509.05386v3, Theorem3.1](https://arxiv.org/html/1509.05386).
Only a fixed finite order is needed here; Section3 gives its constructive
homological step. Flexible exact KMS filtering/coherent corrections are
ordinary [Ding--Li--Lin2404.05998v5](https://arxiv.org/html/2404.05998).
The new candidate operation is their particular cold-window composition,
not invention of those tools. Historical priority is UNKNOWN.

## 3. Finite-order number normal form, without a globally isolated band

For every FIXED integer p there is a computable product of unitaries Y_p,
preserving all classical source symbols, for which

    Htilde=Y_p H_s Y_p^*=N+D_p+R_p,
    [N,D_p]=0,
    ||D_p||_kappa<=Cp lambda,
    ||R_p||_kappa<=Cp lambda^(p+1).                         (4)

These are genuine local interaction norms with exponential SUPPORT-SIZE
weights, acquired from the finite native interactions and a fixed-order
commutator expansion. There is no spatial-to-support-size inference.
Constants are uniform in s,n. Connected declared supports can be retained,
so (4) implies any fixed polynomial spatial-moment bound as well.

For completeness, the elementary local homological maps are

    Dcal(A)=(1/2pi)integral_0^(2pi) exp(iuN)Aexp(-iuN) du,
    Ical(A)=(1/2pi)integral_0^(2pi) i(u-pi)exp(iuN)Aexp(-iuN) du.

They preserve a term's support, have norms <=1 and <=pi/2, respectively,
and [N,Ical(A)]=A-Dcal(A). Ical maps Hermitian A to anti-Hermitian A.
At each order m remove the off-diagonal coefficient W_m by conjugating
with exp(lambda^m Ical(W_m)). An onsite integer spectrum makes the
nonzero homological denominators nonzero integers; no many-body energy
spacing or spectral-band separation is used. The BCH coefficients through
order p are finite connected commutator sums. Reserving finitely many
fixed losses of kappa pays their convergent analytic remainders and gives
(4). Finally D_p=Dcal(Htilde-N), R_p=(1-Dcal)(Htilde-N), so number
conservation is exact in D_p, not only a formal-order statement.

The generator coefficient at order m has support contained in at most m
native supports. It can be obtained by finite matrix products and integer
charge denominators, or by the displayed period integral. For a finite
native rational catalog this is an actual finite compiler, with no global
diagonalization or presumed learned representation. Its very large
order/cluster costs are retained in Section9.

## 4. An EXACT finite-temperature band-filtered GKLS generator

Choose once a real Gevrey smooth fminus(omega), with values in [0,1],
supported in [-3/2,-1/2] and identically one near omega=-1. Its inverse
Fourier transform has all polynomial moments and a stretched-exponential
tail. No temperature-dependent negative-frequency narrowing is used.
Define

    h_t(omega)=fminus(omega), omega<0,
    h_t(omega)=exp(-t omega/2) fminus(-omega), omega>0,
    h_t(0)=0.                                              (5)

Then h_t(omega)=exp(-t omega/2)h_t(-omega). At clock i and excited
level b=1,...,L-1, put ai,b=|0><b|_i and Ai,b=ai,b+ai,b^*.
Work in the dressed frame (4), and define

    Li,b=h_t(ad_Htilde)(Ai,b),
    G=sum_(i,b) Li,b^* Li,b,
    B_t=(i/2)tanh[(t/4)ad_Htilde](G),
    L_t^*(rho)=-i[B_t,rho]+sum_(i,b)D_Li,b(rho).             (6)

The superscript here denotes Schrodinger action; D_L is the usual
L rho L^*-(1/2){L^*L,rho}. Spectral multipliers in (6) have time-domain
filter formulas and do not require knowing eigenvalues. B_t is Hermitian.

Stationarity can be checked without invoking a generic sampler theorem.
For sigma=exp(-t Htilde)/Z, (5) gives

    sigma^(1/2) Li,b^* sigma^(-1/2)=Li,b,
    sum L sigma L^*=sigma^(1/2)G sigma^(1/2).

In an energy pair with omega=E_i-E_j,

    [sigma^(1/2)G sigma^(1/2)-(G sigma+sigma G)/2]_ij
       =G_ij[ sqrt(sigma_i sigma_j)-(sigma_i+sigma_j)/2 ].

The choice B_ij=(i/2)tanh(t omega/4)G_ij cancels this expression
through -i[B,sigma]. At equal energies both expressions vanish. Thus

    L_t^*(sigma)=0                                         (7)

EXACTLY, including all excited states. Complete positivity is the explicit
GKLS form. Uniqueness and mixing will be proved rather than assumed.

## 5. Polynomial spatial moments and clipped light cones

Use anchored profiles A=sum_(x,r) A_x,r with declared support B_r(x),
and the majorant norm

    J_m(A)=sum_(r>=0)(1+r)^m sup_x ||A_x,r||.                (8)

For a single operator rooted at i, use the same norm for its concentric
shells. Statements below concern such uniform majorants, not an invalid
exchange of sup and summation. Connected support-size estimates from (4)
pay all the J_m inputs required at fixed p,m.

The dynamics of Htilde=N+D_p+R_p has spatial LR velocity O(lambda): onsite
N can be removed in the interaction picture and does not spread support.
Clipping the LR bound by the operator norm, then truncating first at radius
C lambda|u|+C log(2+r), gives the moment estimate

    J_m(tau_u A)<=Cm(1+lambda|u|)^(m+2) J_(m+2)(A).         (9)

It holds both for an anchored operator and for an anchored interaction
evolved termwise. The zero truncation has norm <=||A_x,r||; all further
shells have a geometric tail after the clipped cone. Polynomial growth
pays the finite support factors. This is the same ordinary LR-to-moment
operation at every use below; no exp(v|u|) bound is integrated blindly.
For a commutator of two anchored interactions, the overlap sum costs a
fixed extra spatial moment, bounded by J_(m+D+2) of each argument.

## 6. Downward filtering is insensitive to the small resonant dynamics

Let Href=N+D_p. Since [N,D_p]=0,

    tau_u^Href(ai,b)=exp(-iu) tau_u^Dp(ai,b),
    tau_u^Href(ai,b^*)=exp(iu) tau_u^Dp(ai,b^*).              (10)

Taylor-expand tau_u^Dp to order p-1 in ad_Dp. All nonconstant terms
integrate to zero against the fixed negative filter: every derivative of
fminus at -1, except order zero, is zero, and ALL derivatives at +1 are
zero. The fixed-order remainder uses ad_Dp^p Ai,b, whose local moment
norm is <=Cp,m lambda^p by connected commutator counting and (4).
Equation (9) bounds its propagation in the integral remainder. Since the
fixed filter has every time moment finite, this proves

    J_m(Lminus_i,b(Href)-ai,b)<=Cp,m lambda^p.               (11)

Duhamel's formula for Htilde-Href=R_p, using the same clipped LR/moment
bounds and the fixed filter moments, adds at most Cp,m lambda^(p+1).
No t enters (11). In particular a large t lambda does not change this
downward-cooling bound.

For the positive-frequency partner of (5), its kth frequency derivative
has L1 norm <=Ck(1+t)^k exp(-t/4). Integration by parts, or the elementary
Fourier Sobolev moment bound with two extra derivatives, therefore gives

    integral |fplus_t(u)|(1+|u|)^k du
        <=Ck(1+t)^(k+2) exp(-t/4).

Using (9) once more,

    J_m(Li,b-ai,b)
        <=Cp,m lambda^p+Cm(1+t)^(m+5)exp(-t/4).             (12)

The sum G in (6) consequently satisfies, at every fixed moment order,

    J_m(G-N)<=Cp,m[lambda^p+(1+t)^(m+5)exp(-t/4)].          (13)

Products of concentric-shell operators cost only a fixed polynomial
moment (their union is a ball of the larger radius). For large fixed T0
and small lambda the small-error products are absorbed in the constant.

## 7. The coherent correction: use TOTAL G and near conservation of N

Bounding each seed's coherent correction separately by t lambda would
lose the mechanism. The TOTAL baseline in (13) is N. It commutes with
Href exactly, and

    [Htilde,N]=[R_p,N].                                    (14)

With the inverse-Fourier convention of Section4 its exact kernel is

    k_t(u)=1/[t sinh(2pi u/t)],
    B_t=integral_0^infinity k_t(u)[tau_u(G)-tau_(-u)(G)]du.  (14a)

This is a principal-value representation before the odd difference is
taken. It has bound 1/(2pi|u|) at the origin and exponential cutoff on
scale t. The displayed difference makes it absolutely integrable in the
local moments used here. For any nonnegative integer r,

    integral_0^infinity k_t(u) u(1+lambda u)^r du
        <=(r+1)! t(1+lambda t)^r.                          (14b)

For example integral k_t(u)u du=t/16. Expand 1/sinh into positive odd
exponentials to obtain (14b); pi>3 and zeta(j+2)<2 already suffice for
the deliberately loose factorial bound. For N, Duhamel and (14) give

    tau_u^Htilde(N)-N=integral_0^u tau_v^Htilde(i[R_p,N]) dv.

Equations(4),(9) therefore bound its contribution to B_t by
Cp,m lambda^(p+1)t(1+lambda t)^(m+2). For A=G-N, the odd difference at u=0 is
O(u) times its commutator with Htilde, so the 1/|u| singularity is
integrable. At longer times apply (9) to A and the exponential cutoff.
This gives

    J_m(B_t)<=Cp,m t(1+lambda t)^(m+2)
                  [J_(m+D+4)(G-N)+lambda^(p+1)].           (15)

Combining (13)--(15), all these quantities are bounded by a fixed
constant times the sum of a cold and a heating error,

    lambda^p[1+t(1+lambda t)^(m+2)]+(1+t)^K exp(-t/4),
    K=2m+ceil(D)+14                                        (16)

as a safe common exponent. Constants may depend on p,m and the fixed
local/geometry bounds, never on n,s,t in the stated window. This retains
the large total N exactly; it is not a global operator-norm estimate
divided by volume.

There is a Hermitian anchored decomposition of B_t with these bounds.
Use the individual anchored terms of G-N in its linear multiplier and
the anchored terms of i[R_p,N] in the displayed Duhamel integral. Each
integrand is Hermitian. Thus the global cancellation of N is paid before
assigning the coherent pieces to cells.

## 8. A temperature-independent oscillator reference and rapid mixing

The reference is the product amplitude-damping generator

    Lcool=sum_(i,b)D_ai,b.                                  (17)

It is used ONLY for a contraction proof, not as an approximation to the
target Gibbs state. Its local Heisenberg modes are I (eigenvalue0),
E_0b,E_b0 (eigenvalue -1/2), and E_ab for a,b>0 (eigenvalue -1).
For a block matrix O on one clock, the nonconstant mode projections are

    P^ab(O)=E_ab tensor (O_ab-delta_ab O_00), a,b>0,
    P^0b(O)=E_0b tensor O_0b, P^b0(O)=E_b0 tensor O_b0.

Their norms are <=2 and they sum to O-I tensor O_00. They are independent
of t and avoid the exp(2t) condition number of a generic KMS eigenbasis.

Write the actual generator as sum_j L_j, assigning its Hermitian coherent
pieces from Section7 to anchors j. Each L_j is a GKLS generator (its
filtered jumps plus a Hermitian Hamiltonian), so deleting any anchor
leaves a unital CP semigroup. Each difference E_j=L_j-Lcool_j has a
decomposition into supported superoperators E_j,Z with E_j,Z(I)=0.
For dissipators, retain cross terms via the bilinear identity for
D_(a+deltaL)-D_a; each bilinear supported piece is unital. Its norm is
at most a constant times ||a||||deltaL||+||deltaL||^2.

Take m=3ceil(D)+4. Polynomial growth and (12),(15) give

    eta:=sup_l sum_(j,Z containing l)|Z|^2||E_j,Z||_(infty->infty)
       <=Cp[lambda^p{1+t(1+lambda t)^(m+2)}
                  +(1+t)^K exp(-t/4)].                    (18)

Indeed a shell B_r(j) containing l has <=nu(1+r)^D choices of j and
|B_r|^2<=nu^2(1+r)^(2D). The m moment pays this complete row sum.

Here is the direct perturbation proof; proximity alone is not being used
as a many-body mixing theorem. Put M0=L^2-1, o_i(O)=sum_alpha||P_i^alpha O||,
and C_i(O)=I_i tensor <0|O|0>_i. The C_i are commuting unital CP contractions.
Thus ||O-C_Z O||<=sum_(l in Z)||O-C_l O||<=sum_(l in Z)o_l(O).
For E_Z supported on Z and E_Z(I)=0,

    ||E_Z O||<=||E_Z|| sum_(l in Z)o_l(O).                 (18a)

Write L_ne_i=sum_(j!=i)L_j, which is a GKLS generator even though its
terms may act on i. If P=P_i^alpha and its product-damping decay rate
r_alpha is 1/2 or1, the exact operator identity is

    P L=(L_ne_i-r_alpha)P+R_i,alpha,
    R_i,alpha=P E_i+sum_(j!=i)[P,E_j].                     (18b)

It follows by variation of constants, with unital CP partial semigroups,
that P exp(uL)O is bounded by the corresponding decaying initial mode
plus the convolution of ||R_i,alpha exp(vL)O||. When i is outside Z the
commutator with E_j,Z vanishes. For i in Z, (18a) and ||P||<=2 bound the
P E term by 2||E_j,Z||sum_(l in Z)o_l; the E P term is bounded directly
by ||E_j,Z||||P_i^alpha O||. After summing i,alpha the coefficient for
this supported term is at most (2M0|Z|+1)||E_j,Z||sum_(l in Z)o_l.
Consequently it is bounded by 3M0 eta Osc(O). There is no inverse Gibbs
eigenvalue in this calculation. Integral Gronwall gives

    Osc(exp(u L_t)O)<=exp[-(1/2-3M0 eta)u] Osc(O),
    Osc(O)=sum_(i,alpha nonconstant)||P_i^alpha(O)||.        (19)

The explicit projections give Osc(O)<=2n(L^2-1)||O||.
If eta<=1/(12M0), (19) makes the limiting observable scalar. Stationarity
(7) identifies that scalar as Tr(sigma O), proving uniqueness as well.
Telescoping the same CP vacuum expectations and using stationarity gives

    sup_rho ||exp(u L_t^*)rho-sigma||_1
        <=4M0 n exp(-u/4).                                 (20)

No inverse minimum Gibbs eigenvalue, initial overlap, ground-state
replacement or n exp(-t gap) estimate is used in (20).

For the last factor4, first telescope the C_i to get ||O-cI||<=Osc(O).
Stationarity gives |c-Tr(sigma O)|<=Osc(O), and duality gives (20).
This establishes uniqueness, rather than presupposing irreducibility.

Choose the finite normal-form/filter order

    p>a+(m+2)max(a-1,0)+2.                                 (21)

For t<=B lambda^(-a), 0<lambda<=1, the cold term in (18) is bounded by
Cp(1+B)^(m+3)lambda^[p-a-(m+2)max(a-1,0)], which tends to zero. The hot
term is uniformly small for t>=T0 after choosing a sufficiently large
fixed T0. Then choose lambda small enough to pay eta<=1/(12M0).
For D=3, L=a=8 one may take m=13, K=43, p=116. These fixed constants
are large compiler costs, not empirically optimized choices. The number
normal-form constant and the resulting lambda_cool have not been
numerically evaluated for the literal previously frozen clock recipe.

## 9. Actual preparation interface and cost gates

Given the native clock graph/terms, lambda,t and the CLASSICAL known signs:

1. Compile the fixed-order homological generators and Y_p from Section3.
   Use finite products of local evolutions to the precision needed below.
2. Prepare any simple clock product state. Simulate the explicitly defined
   band-filtered GKLS dynamics (6) for 4log(C_L n/epsilon) update time.
3. Apply Y_p^* to obtain the target conditional state of the ORIGINAL
   H_s(lambda), not merely the number-conserving reference Hamiltonian.

R_p is retained in EVERY filter defining the actual generator. It is
used only as a small error in the contraction estimate, not dropped from
the target Gibbs state. Similarly all clock levels and the upward KMS
partner remain in the exact model.

The fixed-order compiler has connected words of order <=p on at most qp
native sites, bounded-degree enumeration exp(O(p)), local matrices of
size L^(O(qp)), and rational charge denominators. These are real, potentially
prohibitive fixed costs, not free effective-Hamiltonian input. Y_p can be
implemented by ordinary local Hamiltonian simulation of its known finite-
order generators. Htilde evolution can be implemented as Y_p exp(iuH_s)Y_p^*.

The finite simulation receiver is specified separately in IMPLEMENTATION.md;
it deliberately pays polynomial accuracy cost rather than borrowing the
more efficient DLL theorem outside its exact weighting assumptions. No
eigenvalue-resolution oracle is used. The coherent principal-value formula
is used for the norm proof only; compact Bohr support permits an ordinary
bounded smooth filter for its circuit implementation.

Independent challenge is not finished. No claim is yet made for the
literal lambda_T, a useful tolerance,
native cooling, conditional Gibbs preparation on actual hardware, or a
uniform guarantee as t grows faster than every fixed power of 1/lambda.
