# Fixed-coupling Gibbs preparation at all sufficiently low temperatures

29 October 2026. NEW theorem independently whole-read and accepted by root
at the stated parameter-qualified mathematical circuit scope. The frozen
polynomial-window packet in ../clock_preparation/ is unchanged. No quantum
state, native clock instance, or new dynamics is run in this continuation.

The target is still conditional clocks with known CLASSICAL syndrome signs.
No source-syndrome distribution is supplied by this theorem. All n clock
levels remain in the full Gibbs state, and neither a globally isolated
zero-ancilla band nor n exp(-t gap) ground-state approximation is used.

## 1. Input and proposed result

Use the explicit weak clock Hamiltonian H_s(v)=N+v V_s with fixed rank,
degree, range, local dimension L, polynomial-growth geometry, and the
previously proved uniform ground gap on 0<=v<=lambda. The source signs are
known input. At a smaller fixed coupling if necessary, the already acquired
exact ground spectral flow W gives

    K=W H_s(lambda) W^* - E_s = N+D,
    K Omega=0,
    (1-a)N <= K <= (1+a)N, a<=1/4.                       (1)

Here Omega is the clock product vacuum. D has spatially quasilocal
interaction norm O(lambda), with fixed stretched-exponential tails and
all polynomial moments. This is the vacuum-CP-martingale normal form of
the frozen clock_stability package, not an assumed number-conserving normal
form. In general [K,N] is NONZERO. The ground flow is constructible from
the native gapped path and real-time filters, independent of temperature.

The proposed theorem is: there are constants lambda_prod>0 and T0<infinity,
independent of n and all source signs, such that every fixed admitted
0<lambda<=lambda_prod permits an actual quantum Gibbs preparation circuit
for exp(-t H_s)/Tr exp(-t H_s), for ALL t>=T0. It has polynomial work in
n,t,1/epsilon and the supplied entry precision. Its algorithmic mixing
time is O(n(1+t)+log(1/epsilon)); logarithmic-in-n mixing is NOT asserted.

The new lambda_prod/T0 and their composed numerical constants have not been
evaluated for the old literal clock recipe. Priority, practical advantage,
physical cooling, native baths and arbitrary-error finite-T stability are
not claimed. This theorem, if accepted, removes the fixed-polynomial cold
window without increasing a Schrieffer--Wolff truncation order.

## 2. Exact band-filtered sampler, in the vacuum frame

Use exactly the explicitly evaluable flat band fminus of the frozen
IMPLEMENTATION.md. For A_i,b=a_i,b+a_i,b^*, a_i,b=|0><b|_i, define

    h_t(omega)=fminus(omega)              (omega<0),
             =exp(-t omega/2)fminus(-omega) (omega>0),
    L_j=h_t(ad_K)(A_j), G=sum_j L_j^* L_j,
    B=(i/2)tanh[(t/4)ad_K](G),
    L^*(rho)=-i[B,rho]+sum_j D_Lj(rho).                   (2)

Each j=(i,b) is an explicit one-clock seed in this frame. In the original
frame it is W^* A_j W; that dressing is implemented, not supplied free.
The exact KMS relation and stationarity are identical to the already
independently accepted proof. The operator K differs from H_s by a unitary
and scalar, so converting its Gibbs state back is exact.

Split the jump into negative and positive energy bands:

    L_j=L_j,-+L_j,+,  G_-=sum_j L_j,-^* L_j,-.             (3)

The negative filter is fixed, so L_j,- is quasilocal with temperature-
INDEPENDENT tails. Its action on the vacuum vanishes EXACTLY: the vacuum
is the lowest energy vector and fminus has strictly negative support.
Fixed-filter Duhamel and the small spatial interaction D show

    J_m(L_j,--a_j)<=C_m lambda                           (4)

at every fixed moment order. There is no t lambda in (4).

Consequently G_--N has O(lambda) spatial interaction tails and annihilates
Omega. Apply the already acquired vacuum-CP martingale to this difference.
Its supported terms satisfy T_Z=Q_Z T_Z Q_Z, Q_Z=I-|Omega_Z><Omega_Z|,
and sum_(Z contains i)||T_Z||<=b with b=C lambda. Thus

    (1-b)N <= G_- <= (1+b)N, b<=1/4                       (5)

after a further smaller fixed lambda. Both (1) and (5) are GLOBAL FORM
bounds acquired from absolutely summable, termwise vacuum-annihilating
lists. The large excited-clock terms are retained.

## 3. Exact KMS-parent cancellation gives a positive time average

Vectorize operators on a doubled clock lattice, grouping the two replicas
of a clock into one cell of dimension L^2. Conjugate the Schrödinger
generator by rho -> sigma^(-1/4) rho sigma^(-1/4), where sigma=exp(-tK)/Z.
This similarity is used for the proof only; it is never implemented as an
imaginary-time oracle.

The transformed jump is the HERMITIAN operator

    J_j=exp[(t/4)ad_K](L_j)
       =q_t(ad_K)(A_j),
    q_t(omega)=exp(-t|omega|/4) fminus(-|omega|).          (6)

The apparently dangerous imaginary-time factors in the coherent and loss
terms cancel EXACTLY. With x=t omega/4, the left coefficient is
exp(x)[tanh(x)-1]/2=-sech(x)/2; the right coefficient is the same. Thus
the Hermitian positive parent of -L^* is

    P(t)=1/2[S_t(G) tensor I+I tensor S_t(G)^T]
                         -sum_j J_j tensor J_j^T,
    S_t(A)=sech[(t/4)ad_K](A).                            (7)

Its positivity does not need a norm estimate: (7) is explicitly Hermitian
and similar to minus a GKLS generator, whose spectrum has nonnegative real
part after the minus sign. The vector sqrt(sigma) is a zero eigenvector by
exact stationarity. Finite n suffices for this spectral argument.

The decisive scalar identity is

    S_t(A)=integral_R p_t(u) exp(iuK)Aexp(-iuK)du,
    p_t(u)=2/[t cosh(2pi u/t)], p_t>=0, integral p_t=1.     (8)

Therefore S_t is unital CP, preserves order, fixes K, and annihilates the
vacuum whenever its argument does. From (1),

    K/(1+a) <= S_t(N) <= K/(1-a)                         (9)

for EVERY t, irrespective of small Bohr frequencies within excited sectors.
Using (5) then gives

    S_t(G_-) >= (1-b)(1-a)/(1+a) N >=9N/20.              (10)

No approximate conservation of N and no beta-growing SW order enters.

## 4. A uniformly coercive product-vacuum baseline

Separate the parent into

    P0(t)=1/2[S_t(G_-) tensor I+I tensor S_t(G_-)^T],
    V_t=P(t)-P0(t).                                     (11)

Let N2=N tensor I+I tensor N. It has product vacuum Omega2 and smallest
nonzero eigenvalue1. Equations(8),(10) imply

    P0(t) Omega2=0, P0(t)>=9N2/40.                       (12)

On grouped doubled cells define Q_i^(2)=I-|00><00| and Npair=sum Q_i^(2).
Then Npair<=N2<=2Npair, so in particular

    P0(t)>=c Npair, c=1/8                               (13)

is a safe common coercivity constant. This is stronger than a global gap.
A pinned ordered chain with a uniform gap but arbitrarily weak extensive
field instability does NOT satisfy such a defect-count form bound.

The parent baseline is generally not close to a product Hamiltonian in
absolute local norm uniformly in t. We do not assert that it is. Instead
its spatial locality parameters grow only polynomially in t, while its
product-vacuum coercivity (13) does not shrink.

## 5. Scaled locality and the exponentially small heated perturbation

We spell out what 'polynomially in t' means. A fixed stretched-exponential
exponent eta>0 and constants C,k suffice to give anchored shell lists for
the two interactions in (11) with

    ||P0_i,r(t)|| <= C(1+t)^k exp[-(r/ell(t))^eta],
    ||V_i,r(t)||  <= C(1+t)^k exp(-t/4)
                                      exp[-(r/ell(t))^eta],
    ell(t)<=C(1+t)^k.                                   (14)

Only spatial decay is claimed, never a support-volume exponential norm.
The same shape persists after finitely many products/commutators with
possibly smaller fixed eta and larger fixed k.

Here is the actual closure argument for (14). A stretched-exponential LR
tail can be written as exp[v|u|-c(r/ell)^eta] times polynomial support
factors, with v bounded by a fixed polynomial in the interaction amplitude
and ell. Clip by the operator norm, and split the time integral at
u_c=c(r/ell)^eta/(2v). A time filter with envelope
C_f exp[-(|u|/T)^zeta] yields an output spatial exponent eta*zeta and
scale at most C ell(1+vT)^(1/eta). All these scale changes are polynomial
for fixed eta,zeta. Polynomial r factors are absorbed in a slower fixed
stretched exponential, with a polynomial power of its scale in front.
This proves the required closure instead of integrating exp(v|u|) blindly.

The fixed ground flow W and negative filter give temperature-independent
tails for K and G_-. The positive-frequency partner has every frequency
derivative bounded by C^k(k!)^s(1+t)^k exp(-t/4), for a fixed Gevrey order s.
The symmetrized filter q_t has the analogous factor exp(-t/8). Thus each
J_j in (6) has spatial tails polynomial(t) exp(-t/8), and the product
J_j tensor J_j^T has factor exp(-t/4). Also
G-G_-=sum(L_-^*L_++L_+^*L_-+L_+^*L_+) has factor exp(-t/4).
Applying the positive kernel (8), whose time scale is t, preserves that
amplitude up to polynomial factors. This proves (14).

For example one may start with Gevrey2 fixed filters and finite-range native
inputs. Ground dressing has some fixed stretched-exponential exponent,
the negative/q filters multiply that exponent by1/2, and the sech time
average leaves a positive fixed exponent. Nothing here requires choosing
an exponent tending to0 with t. All constants follow from the explicit
filters and native LR bounds; no table of many-body eigenvalues occurs.

## 6. Product-COERCIVITY stability, with polynomial locality cost

**Lemma.** Suppose H0 is a spatially quasilocal Hamiltonian with unique
product vacuum Omega, H0 Omega=0, and H0>=c Npair with fixed c>0. Suppose
its interaction and a Hermitian perturbation V have scaled stretched-
exponential shell bounds with fixed exponent eta, respective amplitudes
J and epsilon J, and scale ell>=1. There is a computable fixed polynomial
P in 1+J,ell,c^-1 (depending only on eta and the polynomial-growth geometry)
such that epsilon P<=c/4 implies a uniform gap >=c/2 for H0+V. Local Hilbert
dimension does NOT enter P. No local ground-space assumption is imported.

This lemma is not the false statement 'a global gap is stable.' The extra
defect-count form bound and exact product vacuum are essential.

SCALED_LOCALITY.md makes the polynomial bookkeeping literal: the convolution
constant, pair-norm/LR velocity, fixed finite moment orders, scale/amplitude
updates, small parameter-flow velocity, final relative-defect sum and a
closed all-real-temperature gate are displayed there. It is part of this
lemma's proof, not an assumed continuity/modulus oracle.

**Proof.** For each finite volume use the path H(s)=H0+sV. Bootstrap a gap
>=c/2 above its simple ground eigenvalue. Choose a fixed ordinary exact
ground spectral-flow filter with inverse-frequency values outside c/2.
Its scale/moments are polynomial in c^-1. It transports the ground vector
back to Omega; write that unitary as U(s). It is a PROOF device in this
lemma, not an input oracle or the sampler's actual circuit.

For precision, the LR/filter closure of Section5 bounds the rooted
interaction moments of its generator by epsilon times a polynomial in
J,ell,c^-1. Its stretched-exponential scale is bounded by another such
polynomial, with a smaller but FIXED exponent. The derivative of
U(s)H(s)U(s)^* is the conjugate of V plus the commutator of the flow
generator with H(s). The overlap sums cost only polynomial spatial moments.
Its interaction strength is therefore epsilon times a fixed polynomial.
Conjugation by U(s) for parameter length<=1 retains this bound whenever
epsilon times a larger such polynomial is<=1: the flow generator is small,
so its own LR exponent over this parameter interval is bounded by a constant.
Equivalently use the clipped light cone; its scale remains polynomial.

It follows that the interaction

    D(s)=U(s)H(s)U(s)^* - E(s) - H0                       (15)

has a stretched-exponential anchored majorant epsilon times a polynomial
in J,ell,c^-1. To subtract E(s) locally, subtract each term's vacuum
expectation; their sum is E(s). This changes norms by at most2. Exact
ground transport gives D(s)Omega=0, with Hermiticity retained.

Now use the elementary vacuum-CP martingale on D(s): order the cells,
telescope the vacuum expectations outside successive prefixes, then
localize each difference to concentric balls. Every resulting Hermitian
T_i,r satisfies

    T_i,r=Q_(B_r(i)) T_i,r Q_(B_r(i)),
    ||T_i,r||<=epsilon P1 exp[-(r/ell1)^eta1],             (16)

where P1,ell1 are fixed polynomials and eta1>0 is fixed. A term can survive
the prefix difference only if it contains that cell. Both CP expectations
have norm1, giving factors2 and4, not a Hilbert-dimension normal-order cost.
Since Q_B<=sum_(j in B)Q_j^(2),

    |D(s)|_form <= [sup_j sum_(i,r: j in B_r(i))||T_i,r||]
                                      Npair
                <=epsilon P Npair.                     (17)

Indeed the final sum is bounded by
C epsilon P1 sum_r (1+r)^D exp[-(r/ell1)^eta1], a fixed polynomial in ell1.
One may overpay with exponent2D+2; all powers are finite constants. This
is why geometric locality is adequate here, without exponential support-
volume control or a local Hilbert-dimension factor.

Equations(13),(15)--(17) imply

    U(s)H(s)U(s)^* -E(s) >= (c-epsilon P)Npair
                                  >=3c Npair/4.          (18)

Thus the bootstrapped gap is actually >=3c/4>c/2. Continuity extends the
bootstrap to s=1, uniformly in volume. This proves the lemma. All exact
flow/LR imports are the ordinary BMNS and NSY tools already specified in
the frozen stability proof. The polynomial dependence is paid by the
scaled clipped-cone estimates above, rather than left as an arbitrary
constant that could grow exponentially in t.

Yarotsky's [math-ph/0412040, Theorems1--2](https://arxiv.org/pdf/math-ph/0412040)
is a strong controlling antecedent for relative perturbations; its displayed
framework has finite range and translation invariance. It is not invoked
outside those hypotheses here. Our direct CP/spectral-flow proof pays the
quasilocal scaled-range interface actually needed in (14).

## 7. The all-cold parent gap and a finite Gibbs preparation operation

Apply the lemma to P0(t) and V_t in (11). Their relative perturbation
parameter is epsilon_t=exp(-t/4), while J(t),ell(t),c^-1 and all further
locality costs are polynomial in 1+t. Consequently a single finite T0 can
be chosen so that epsilon_t P(t)<=c/4 for EVERY t>=T0. No SW order grows
with t, and lambda stays fixed. The parent P(t) has a unique zero vector
sqrt(sigma) and gap at least c/2=1/16.

The final gate can be made literal: if the composed majorant is
C0(1+t)^k exp(-t/4), take T0 as SCALED_LOCALITY Eq(S13). Its proof uses
log(1+t)<=sqrt(t), not a sampled temperature grid. The coefficients C0,k
are finite compositions of the displayed envelope updates, but have NOT
been numerically tabulated for the native catalog.

The parent similarity need not be implemented to get a mixing bound.
Schatten Holder and the spectral gap give, for any clock state rho,

    ||exp(uL^*)rho-sigma||_1
       <= exp(-u/16)[sigma_min^(-1/2)+1].                 (19)

For the native H_s, use E=sum_X||H_X||=O(n) and dim=L^n. Then

    log(sigma_min^(-1/2)) <= t E+(n/2)log L.              (20)

Unlike an exponential prefactor left in a runtime, its logarithm only
costs O(nt) update time. For instance

    U=16[ceil(tE)+Ln+ceil(log2(16/epsilon))]              (21)

is a safe finite time giving trace error <=epsilon/8. Faster logarithmic
mixing from arbitrary states is left OPEN in this all-cold continuation.

Now implement (2) with the already paid scalar band filters, constant
Bohr-support g cutoff, LCU, reset-dilation and finite error allocations in
the frozen IMPLEMENTATION.md, using update time(21). All cost expressions
remain polynomial in n,t,1/epsilon. Replace its finite-order Y_p by the
known exact ground flow W and its inverse. This flow has a temperature-
independent gapped native path; fixed-gap filter quadrature, path-order
discretization and ordinary native Hamiltonian simulation implement it to
any allocated finite precision in polynomial(n,precision^-1) cost. One can
use slower quadrature/product formulas rather than assuming an oracle.
Every Hbar evolution is W exp(iuH_s)W^*. Final W^* returns the ORIGINAL
conditional full Gibbs state. The original finite-depth prefix gauge can
then be restored if desired. No spectral projector or parent-ground
preparation oracle is called by the actual sampler.

The normal-form flow and all signs are computable from the supplied local
term list. This operation requires quantum coherent gates, fresh ancilla
resets and classical coefficient computation. It is not a passive thermal
controller or a presently executed hardware initializer. The full source
syndrome marginal is a separate input/operation. The extra fixed coupling
and temperature constants are UNEVALUATED for the old literal clock recipe.
The present all-cold theorem and scaled stability lemma received root's
independent whole challenge/acceptance. No numerical simulation is offered
as a substitute, and no broader physical scope is inferred.
