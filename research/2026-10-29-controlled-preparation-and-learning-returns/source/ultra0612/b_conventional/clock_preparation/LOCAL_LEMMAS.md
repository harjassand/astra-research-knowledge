# Local moment and finite-order compiler details

29 October 2026. Companion to PROOF.md. These are proof-level bounds;
no finite Hamiltonian or dynamics is executed. Constants may depend on the
fixed native rank, degree, range, local dimension, and the indicated finite
orders. They are uniform in volume and in every classical syndrome assignment.

## 1. Fixed-order homological construction is an acquired finite algorithm

Write an interaction as a list of declared connected supports. Keep duplicate
supports separate if convenient, and use

    ||A||_k = sup_x sum_(X contains x) exp(k |X|)||A_X||.

The starting finite-range list has an explicit value/upper bound in this norm.
For 0<k'<k the elementary overlap count gives

    ||[A,B]||_k' <= 4/(k-k') ||A||_k ||B||_k.              (L1)

Indeed a nonzero term has X intersect Y; assigning an intersection site
costs |X| or |Y|, and r exp(-(k-k')r)<=1/(k-k'). The norm2 commutator and
the alternatives x in X or x in Y give the factor4. Scalar terms can be
retained separately since they never enter a commutator.

Both onsite homological maps in PROOF Section3 preserve each support and
have norm at most1 and pi/2. At a fixed order p, expand the finite product

    Y_p=exp(lambda^p S_p)...exp(lambda S_1).

In increasing order m, obtain the degree-m coefficient W_m by finite
polynomial multiplication of truncated adjoint series and set
S_m=Ical(W_m). This is a literal algorithm on the native matrices. Every
coefficient has connected declared support in at most m native supports.
Only integer differences of the onsite number appear in Ical. It does not
divide by an interacting many-body level spacing.

For completeness the analytic tail has a constructive majorant, not just
a formal order symbol. To bound exp(ad_S)A at a reserved loss d>0, distribute
the loss d/k across k nested commutators. Equation(L1) bounds its kth
Taylor term by

    (4k/d)^k ||S||^k ||A|| / k! <=(4e||S||/d)^k||A||.

For ||S||<=d/(16e) this is a convergent geometric majorant. Reserve finitely
many losses d across the p adjoint exponentials, for example one half of
the initial exponent divided equally between them. The W_m are finite
computed coefficient lists, so decreasing a positive lambda until every
geometric test holds is an effective finite search. Truncated coefficients
and the geometric tails give a computable C_p and lambda_nf with

    Htilde=N+D+R, [N,D]=0,
    ||D||_k <= C_p lambda, ||R||_k <= C_p lambda^(p+1).      (L2)

One can use rational upper bounds pi<4,e<3 throughout this compiler.
For (L2) the scalar part is harmless and the remaining onsite N has a
fixed interaction norm. A final exact application of Dcal defines D;
the same bounded map defines R=(1-Dcal)(Htilde-N). Thus exact number
conservation does not depend on discarding the analytic tail.

Native rational/algorithmically computable coefficients permit computation
to any specified finite precision. Exact coefficient lists through p have
O(n) translates times at most exp(O(p log(p d))) connected words, and each
local calculation uses matrices of dimension at most L^(q p). This is an
enormous but explicit fixed-order cost. The construction does not claim that
the previously compiled literal lambda_T already passes these new tests.

A dense local matrix is an upper-bound implementation, not a hidden required
input. There is also a direct operator-word implementation. If A has support
of k clocks, its charges with respect to N_X lie in [-k,k]. With K=2k+1 and
u_j=2pi j/K, define

    A_l=K^-1 sum_(j=0)^(K-1) exp(-il u_j)
                          exp(iu_j N_X)A exp(-iu_j N_X).

This discrete Fourier projector is EXACT because the integer charges do not
alias in a period K. Then Dcal(A)=A_0 and Ical(A)=sum_(l!=0)A_l/l.
All new conjugations are products of known one-clock diagonal phase gates.
The coefficients are explicit roots of unity and rational nonzero integers;
their finite precision can be budgeted. Nested commutators are finite signed
lists of operator words, with products implemented by block-encoding
composition if desired. Thus the homological compiler can work directly
from native block encodings without obtaining dense L^(q p) matrices. Its
word count may be very large, but depends on p and the bounded native catalog
rather than exponentially on the total number n of clocks. No interacting
energy eigenvectors are being smuggled into this alternative representation.

## 2. Why support-size information pays the spatial input here

Each native support has fixed spatial diameter R0 and connected interactions
remain connected in their native overlap graph. A declared connected set of
size k therefore has diameter at most C R0 k. The exponential support-size
majorant in (L2) consequently pays exponential spatial-distance weights and
every fixed spatial moment. This is an implication FROM the acquired
support-size norm, not a conversion in the reverse direction.

Choose a deterministic anchor for each connected term and telescope ordinary
normalized partial-trace expectations over balls about that anchor. Their
norms are at most1. This produces concentric-shell lists with a computable
uniform majorant

    J_m(A)=sum_r (1+r)^m sup_x ||A_x,r||.

All uses of J refer to these lists/majorants. No step interchanges a supremum
and an infinite sum in the wrong direction.

## 3. Clipped light cone, with polynomial rather than exponential time cost

Remove N in the interaction picture. It is onsite, hence does not spread
support or change the interaction norms. The remaining interaction has
exponential distance decay and strength at most C_p lambda. The ordinary
LR commutator/conditional-expectation estimate thus bounds the tail of an
operator supported on B_r(x) by

    C |B_r| ||A|| exp[-mu(R-r)+v lambda |u|].               (L3)

The trivial bound for the same conditional-expectation difference is
2||A||. Pick

    R_c = r + ceil((v lambda |u|+D log(2+r)+C0)/mu).

The expectation onto B_(R_c) is the first term in the shell list and has
norm <=||A||. Each additional shell has norm <=C||A||exp[-mu(R-R_c)].
Moreover 1+R_c<=C(1+r)(1+lambda|u|), using log(2+r)<=C(1+r).
Summing the shells proves the deliberately loose bound

    J_m(tau_u A) <= C_m(1+lambda|u|)^(m+2) J_(m+2)(A).     (L4)

For a global interaction, evolve each declared anchored term separately.
The same estimate holds for its uniform majorant; no sum over all volume
anchors is taken in (L4). The constants follow by finite local LR estimates
and a convergent geometric series. Onsite number degeneracies do not enter.

## 4. Overlap sums and the small remainder

For an interaction R=sum_(y,r) R_y,r and an operator A=sum_s A_i,s rooted
at i, a nonzero commutator has B_r(y) intersect B_s(i). Its union lies in
B_(s+2r)(i). There are at most C(1+r+s)^D possible y. Multiplying this
count with the norm2 commutator and the output moment gives

    J_m([R,A]) <= C_m J_(m+D+2)(R) J_(m+D+2)(A).          (L5)

This also bounds two interactions termwise with an anchored output list.
For [N,A] a single term merely costs its support size, which is paid by
J_(m+D)(A). Equations(L4),(L5), Duhamel, and the fixed time moments of the
negative filter prove the R contribution O(lambda^(p+1)) claimed in
PROOF Section6. The degree of a time polynomial in this use is irrelevant:
the negative filter is fixed and has ALL polynomial moments.

For the coherent correction apply (L4) to [Htilde,A], use (L5) and the
onsite estimate, then integrate once in time. In particular

    J_m(tau_u A-tau_(-u)A)
       <= C_m |u|(1+lambda|u|)^(m+2) J_(m+D+4)(A).        (L6)

For A=N, replace the last norm by C_p lambda^(p+1), because
[Htilde,N]=[R,N]. Equation(14b) of PROOF now gives its Eq(15). No raw
exp(v|u|) LR majorant is integrated against a scale-t kernel.

## 5. Local row sum of the supported generator difference

Filtered jumps have anchored shell lists. Expand a dissipator bilinearly
in those lists, retaining ALL cross terms. Each supported bilinear term

    A^* O B - (A^* B O+O A^*B)/2

annihilates I and has infinity-to-infinity norm <=2||A||||B||. The norm
of a product list is bounded by the product of fixed J moments, since the
union of concentric balls has the larger radius. The coherent pieces are
Hermitian because (14a) is a real kernel of Hermitian differences. They
are assigned to anchors only AFTER the total baseline N is canceled.

A radius-r supported term containing a fixed l has at most nu(1+r)^D
possible anchors j and |B_r|^2<=nu^2(1+r)^(2D). Consequently J_m with
m=3ceil(D)+4 pays the full quantity

    sup_l sum_(j,Z contains l) |Z|^2 ||E_j,Z||.

The supported terms in this last sum need not individually be GKLS or
positive. The COMPLETE term at each anchor IS GKLS, because it is its
full jump dissipators plus its assigned Hermitian Hamiltonian. This is
exactly the positivity fact needed when the direct oscillator proof
deletes an anchor; it does not discard unfavorable cross terms.

## 6. Effective but unoptimized smallness gate

The preceding operations are explicit finite coefficient arithmetic,
geometric sums, local LR constants and fixed filter-moment bounds. They
therefore yield computable constants C_p in Eq(18), rather than a hidden
global ground-space or eigenvalue oracle. Given fixed a,B, choose p by
Eq(21); increase T0 until the heating majorant is <=1/[24(L^2-1)], then
decrease a positive rational lambda until the cold majorant is also
<=1/[24(L^2-1)] and all finite normal-form tests in Section1 hold.

This procedure terminates by the positive exponent in Eq(21). It has not
been executed for q43,d344,L8, so lambda_cool is an UNEVALUATED extra gate.
The packet does not present an operationally useful literal hardware
parameter. What is acquired is a uniform finite-constant circuit theorem
in a cold polynomial window, with every representation and quantum
primitive specified instead of an assumed conditional-Gibbs oracle.
