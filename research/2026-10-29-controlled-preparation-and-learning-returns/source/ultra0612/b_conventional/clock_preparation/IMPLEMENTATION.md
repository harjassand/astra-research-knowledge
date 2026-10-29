# Finite circuit receiver, with no Gibbs or eigenvalue oracle

29 October 2026. This is an algorithm specification and resource theorem,
not an executed quantum circuit or physical initialization. Its correctness
uses the cold-window contraction in PROOF.md, including its additional
small-coupling gate. It applies to the exact full conditional Gibbs state,
not a truncation to its ground band. No native Davies bath is presumed.

## 1. Input and ordinary primitive contract

Input: an explicit bounded-rank finite-range list for H_s=N+lambda V_s,
known CLASSICAL syndrome signs s, fixed local dimension L, rational or
otherwise efficiently computable local entries, lambda,t, and 0<epsilon<1.
The geometry/coupling promises of PROOF.md are required. A global energy
norm upper bound is E=sum_X||H_X||=O(n); this is directly available from
the term list. For native q43,d344 clocks with lambda<=1, E<=345 n suffices.

The output is a quantum circuit on n clock registers, temporary ancillas,
and a classical description of that circuit. It prepares a state within
trace norm epsilon of exp(-tH_s)/Tr exp(-tH_s), from any clock input.
It does not prepare the distribution of source syndromes. If the target
physical gauge is the earlier two-body endpoint, apply its already specified
finite-depth prefix unitary after this conditional preparation. All such
gates are retained; no logical-source mixing is inferred.

The ordinary quantum primitives used are controlled real-time Hamiltonian
simulation, linear-combination-of-unitaries block encodings, and simulation
of a Hermitian block-encoded matrix. They require only the supplied local
term list and explicitly computed scalar coefficient tables. For example,
the constructions and LCU interfaces in
[Ding--Li--Lin2404.05998, Section3.3](https://arxiv.org/html/2404.05998)
and its AppendixB give exactly these interfaces. No unrestricted Gibbs
algorithm, fast mixing oracle, state overlap promise, or rounding promise
is substituted for the newly proved contraction.

For clarity an elementary, slower first-order reset circuit is given below.
It suffices for polynomial complexity in n,t,1/epsilon. It does NOT claim
the stronger polylogarithmic precision cost of modern Lindblad simulation.

## 2. An explicitly evaluable flat filter

Let b(x)=exp(-1/x) for x>0 and b(x)=0 for x<=0, and define the smooth step

    S(x)=0 (x<=0), S(x)=1 (x>=1),
    S(x)=b(x)/[b(x)+b(1-x)] (0<x<1).

Put

    fminus(omega)=S(4(omega+3/2)) S(4(-1/2-omega)).        (I1)

It has support [-3/2,-1/2], is exactly1 on [-5/4,-3/4], and is Gevrey.
All derivatives at -1 beyond order0 vanish, and all at +1 vanish. Thus it
is the filter used in the cancellation proof, not an approximate plateau.
Use h_t from PROOF Eq(5).

For the coherent filter define the real even smooth cutoff

    kappa(omega)=S((6-|omega|)/3).

It is identically1 for |omega|<=3 and0 for |omega|>=6; the apparent absolute
value singularity lies in an open constant plateau. Let

    Wg_t(omega)=(i/2)tanh(t omega/4) kappa(omega).          (I2)

The exact jump L=h_t(ad_Htilde)(A) has matrix elements only at Bohr
differences in [-3/2,-1/2] union [1/2,3/2]. Therefore every L^*L, and
their sum G, has Bohr support within [-3,3]. Consequently

    Wg_t(ad_Htilde)(G)=(i/2)tanh[(t/4)ad_Htilde](G)        (I3)

EXACTLY. This is the ordinary compact-frequency observation of DLL
Section3.2; it avoids an extensive energy cutoff. The principal-value
kernel in the norm proof need not be simulated.

All scalar constants needed here can be acquired with integer arithmetic.
Write b^(k)(x)=exp(-1/x) P_k(1/x), where

    P_0(y)=1, P_(k+1)(y)=y^2[P_k(y)-P_k'(y)].

On 0<x<1, |b^(k)(x)|<=B_k=sum_j |[y^j]P_k| j!, since
y^j exp(-y)<=j!. At least one of x,1-x is >=1/2, so the step denominator
is >=exp(-2)>1/8. Thus a derivative majorant is

    S_0=1,
    S_k=8[B_k+2 sum_(j=1)^k binom(k,j)B_j S_(k-j)].        (I4)

An admissible derivative majorant for fminus is

    F_k=4^k sum_(j=0)^k binom(k,j)S_j S_(k-j).             (I5)

For h_t, derivatives of the positive-frequency branch have the bound
exp(-t/4)sum_j binom(k,j)(t/2)^j F_(k-j), and the negative branch F_k.
For (I2), the derivative polynomials of tanh give finite explicit constants
using |tanh|<=1. Equations(I4),(I5), their finite convolutions, and support
lengths1 and12 produce an integer C_* such that for W=h_t or Wg_t,

    A=C_*(1+ceil(t))^4 >=1

dominates the following quantities: ||W||_1, ||W''||_1, ||W^(4)||_1,
||omega W||_1, and the analogous constant needed for ||W'||_infinity.
The code compiles a deliberately conservative such C_*. Higher fixed
moments in the proof use the same finite recurrence at higher order.
There is no unevaluated filtering-function oracle.

## 3. A fully finite quadrature and precision budget

For the inverse Fourier transform f_W(u)=(1/2pi)integral W(omega)
exp(-i omega u)domega, the chosen A implies

    |f_W|<=A, |f_W'|<=A,
    |f_W(u)|<=A/|u|^2 and <=A/|u|^4,
    integral |f_W(u)|du<=4A.                              (I6)

Set alpha=8A, m=n(L-1), M0=L^2-1, and choose the INTEGER update time

    k=ceil(log_2(32 n M0/epsilon)), U=4k.                  (I7)

Because exp(1)>2, PROOF Eq(20) bounds its exact mixing error by epsilon/8.
For the common operator/filter tolerance take

    delta=epsilon/[1024 U m alpha^2].                     (I8)

Given an input contraction A0, truncate its filtered integral at

    T=ceil(8A/delta)

and use a uniform paired time grid of spacing at most

    delta/[64 A(1+E)T].                                  (I9)

The fourth-derivative bound gives the discarded tail <=2A/(3T^3),
which is <delta/8. The integrand derivative norm is <=2A(1+E).
The rectangle-rule error is consequently <=delta/16. Compute every scalar
f_W(u_j) to absolute error <=delta/(16T), costing <=delta/8 in the
integral. Approximate each selected Heisenberg evolution to error
<=delta/(64alpha); the coefficient l1 mass is <=alpha, so its total
contribution is <=delta/32. The remaining margin covers endpoints and
coefficient normalization/rounding. The resulting operator error is <delta.

The scalar Fourier coefficients themselves are not free. They are
integrals over an interval of length at most12. Their integrand derivative
is bounded by C(1+t+|u|), with C computed from (I4),(I5). Ordinary interval
rectangle quadrature to error xi therefore uses
O((1+t+T)/xi) frequency samples. With xi=delta/(16T), this is polynomial
in t,T,delta^-1. Computable exp/tanh and fixed-dimensional local matrix
entries are evaluated to that absolute error; very small positive
exponentials may be bounded by the error budget before evaluation. This
cost is intentionally charged rather than an assumed state-preparation
oracle. No finite random-law sampling is used in this deterministic
coefficient computation.

The time grid has at most

    K=2+ceil[128 A(1+E)T^2/delta]                          (I10)

points. Finite table state preparation and SELECT can use O(K) ordinary
gates per lookup without QRAM. This is a slow polynomial bound, not an
assertion that coefficient tables have unit cost.

## 4. Approximate jumps, coherent term, and the exact target

Use LCU of the known one-clock contractions A_i,b and their controlled
Heisenberg evolutions to implement each approximate jump Lhat_i,b. Its
block normalization is <=alpha, and ||Lhat-L||<=delta. Products and a
uniform sum give a block encoding of Ghat=sum Lhat^*Lhat, normalization
<=m alpha^2. Then use the g-filter on Ghat/(m alpha^2), at tolerance
delta, and multiply back. Symmetrize the result to define Hermitian Bhat.

Even though quadrature makes Lhat not exactly frequency limited, the
comparison still works: (I3) is used only for EXACT G; the cutoff filter
has induced operator norm <=integral|f_g|<=alpha on Ghat-G. Thus

    ||Ghat-G||<=3m alpha delta,
    ||Bhat-B||<=4m alpha^2 delta.                         (I11)

The full approximate generator is GKLS. The elementary product estimate
for dissipators gives

    ||Lhat_gen-L_gen||_diamond
       <=6m alpha delta+8m alpha^2 delta
       <=14m alpha^2 delta.                              (I12)

The exact and approximate semigroups are both channels, so Duhamel bounds
their time-U distance by U times (I12), <epsilon/64. This comparison does
not require a Gibbs-state condition number or division by a small gap.
The exponentially small upward branch is retained to the requested
GLOBAL tolerance; it is not dropped on the argument that the per-site
excited population is small.

## 5. Reset dilation: an elementary actual channel circuit

Put Q=16m alpha^3. It upper-bounds the sum of induced diamond norms of
the approximate coherent and dissipative pieces. Use

    R=ceil[1024 U^2 Q^2/epsilon]+ceil(UQ), ds=U/R.          (I13)

At each of these R steps, apply the Bhat unitary for time ds and then
one fresh-ancilla channel for every Lhat. The latter uses

    Gamma_L = |1><0| tensor Lhat + |0><1| tensor Lhat^*,
    exp(-i sqrt(ds) Gamma_L), ancilla initialized |0>,
    discard/reset that ancilla.                           (I14)

The initial ancilla column makes its Kraus operators

    K0=cos(sqrt(ds) sqrt(Lhat^*Lhat)),
    K1=-i sqrt(ds) Lhat sinc(sqrt(ds) sqrt(Lhat^*Lhat)).

Hence the channel is I+ds D_Lhat+O(ds^2 alpha^4). More explicitly the
odd terms vanish on tracing the ancilla; the exponential Taylor remainder
for ||Gamma_L||<=alpha and ds alpha^2<=1 bounds the channel's distance
from exp(ds D_Lhat) by 256 ds^2 alpha^4. First-order splitting of all
pieces costs <=2 ds^2 Q^2 per step. Summing the reset errors and using
Q^2>=256m alpha^4 gives total error <=3U^2 Q^2/R<epsilon/256.

The block encoding of Gamma_L is obtained from that of Lhat and its
adjoint; Bhat is already Hermitian block encoded. Ordinary block-encoded
Hamiltonian simulation implements (I14) and the coherent unitary. Demand
operator-norm error <=epsilon/[128R(m+1)] per unitary; converting to
channel error and summing gives at most epsilon/64. This never conditions
on a successful block-encoding outcome or an exponentially unlikely Gibbs
projection. Fresh ancilla resets are ordinary circuit operations.

The ideal fixed-order dressing Y_p and its inverse are themselves compiled
from the finite local generators in LOCAL_LEMMAS. Implementing a total
precision epsilon/64 gives <=epsilon/32 channel error at the final output.
Every occurrence inside a controlled Htilde evolution is charged the
smaller per-query error in Sections3--5. The identity

    exp(iu Htilde)=Y_p exp(iu H_s) Y_p^*

supplies those evolutions without diagonalizing Htilde. Ordinary local-term
Hamiltonian simulation, even a low-order product formula, has polynomial
gate cost in n,|u|,precision^-1 and the fixed compiler constants. Classical
Hamiltonian simulation is not presumed: these are quantum gates on the
actual n registers.

The discrete onsite-charge projectors in LOCAL_LEMMAS Section1 also permit
compiling Y_p as explicit finite LCU/operator-word lists from the native
interactions. This alternative avoids treating a dense L^(q p) local matrix
as an already supplied primitive. It has O(k) onsite phase rotations per
charge projector on k<=q p clocks and explicit finite coefficient lists;
all such word/table costs remain in the fixed-order compiler constant.

Adding mixing, generator approximation, reset/splitting, scalar arithmetic,
and dressing errors stays below epsilon. Exact stationarity identifies the
limit, so no partition function is required. All heating levels remain.

## 6. What complexity is and is not acquired

For FIXED p,q,d,L,D,a,B and an admitted sufficiently small lambda, the
algorithm has classical preprocessing and quantum gate count polynomial
in n,t,1/epsilon and input-entry bit cost. It prepares the actual global
conditional state with a fixed coupling and penalty independent of n.
The update-time mixing bound is logarithmic, but the circuit is emphatically
NOT claimed logarithmic depth or nearly linear total work. For example the
deliberately loose receiver has A=O(t^4), alpha=O(t^4), delta^-1=O(t^8),
T=O(t^12), R=O(t^24), and K=O(t^36), suppressing n,U,epsilon constants.
Scalar coefficient computation and Hamiltonian simulation add further
polynomial factors. The tiny frozen clock penalty therefore entails an
astronomical time constant, even if its additional coupling gate were paid.

The finite-order compiler order116 has huge connected-word/local-matrix
cost. Its full native coefficient catalogue has NOT been generated here,
and lambda_cool has NOT been numerically evaluated. The new theorem permits
a smaller fixed lambda; it is not an executable numerical qualification
of the old literal lambda_T. The scalar receiver code only executes exact
filter/oscillator/resource arithmetic, and is labeled accordingly.

No useful hardware budget, native bath, classical sampler, physical thermal
initialization, arbitrary-beta limit at fixed lambda, perturbed finite-T
stability, or practical advantage is inferred. The useful new interface is
the fixed-coupling, polynomial-cold-window ALL-n quantum circuit construction
from a native weak product Hamiltonian, rather than a supplied Gibbs oracle.
