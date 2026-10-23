# Independent challenge: uniform susceptibility-to-code transfer

Reviewer role: fresh bounded Cycle6 challenge. This is internal mathematical
review, not external certification, priority assessment, or an efficient-code
claim. The established Cycle5 capacity audit was not repeated.

## Decision and exact scope

Updated after the all-length constructive proof was available: I read the
actual owner note UNIFORM_GROWTH_TRANSFER.md, the relevant actual Cycle5
operator-drift coding theorem, local variational construction and inherited
compression appendix, plus both current contributions
temporal_operator_dual.md and temporal_constructive_structure.md. I found
no load-bearing gap in the full chain now supported by those sources:

    v_k >= k^(3/2)/32, k>=4,
    Q(V_beta,tau) >= 3/2+(ln2/4096) beta^(64/17),
    0<beta<=2^-11.

The second inequality uses the explicit growing block length in section 6,
fixed before the communication horizon. The whole-bath/root and pointwise
normal-initializer qualifications are unchanged. The proof is internally
accepted; this review is not external certification.

Sections 1--5 record the initial conditional-quadratic development route and
the general transfer mechanism. Their stronger beta^(7/2) result remains
CONDITIONAL and is not the completed theorem. In particular this decision
DOES NOT certify v_k >= k^2/32. The initial calculation used:

    k^2/32 <= v_k <= k^2,
    ||H_zeta|| <= k^2,    ||G1|| <= k^2,

The current all-length endpoint decomposition does establish the displayed
upper and norm bounds. The completed lower is k^(3/2)/32, not k^2/32.
Both transfer versions also use the inherited charge-preserving bulk
representation, exact zero bulk drift of sigma at all b, and the exact
diagonal drift identity. A finite pattern check cannot replace any of those
all-length proofs. Section 7 records the independently challenged growth
mechanism; a separate expanded token review is also supplied.

Use zeta_* for the auxiliary prefix minimizer where convenient. It is an
analytic dual state; it is never physically prepared and is not the actual
bath initializer tau. This distinction should be explicit in the final
manuscript, where both objects otherwise use the letter tau.

## 1. The minimizer supplies a full operator inequality

Let F_zeta=Tr_prefix[(I tensor zeta)G1], H_zeta=F_zeta+(2Q-kI),
and v(zeta)=Tr(sigma H_zeta^2). The exact diagonal identity means H_zeta
has zero input diagonal. It is Hermitian and charge preserving. Because
sigma is scalar on each charge sector, it commutes with H_zeta and with
every variation H_xi-H_zeta. In particular,

    Tr(sigma H_zeta)=Tr(sigma Q H_zeta)=0.

The prefix state space is compact and finite dimensional, so a minimizer
zeta_* exists. Write H=H_zeta_* and

    M=Tr_input[(sigma H tensor I)G1].

For each prefix density xi the right derivative along
(1-t)zeta_*+t xi is

    2 Tr[sigma H (H_xi-H)]
       =2 Tr[(xi-zeta_*)M] >=0.

The equality at the minimizer is

    Tr(zeta_* M)=Tr[sigma H F_zeta_*]
               =Tr[sigma H(H-(2Q-kI))]=v_k.

Thus Tr(xi M)>=v_k for every density xi, proving M>=v_k I.
This is the required worst-prefix operator statement. It is not an average
bound and it does not assume an interior or full-rank minimizing state.
Convexity makes the first-order condition sufficient as well, but only
necessity at an actual minimizer is needed here. No minimax exchange is
needed for this implication.

## 2. The uniform remainder is correctly normalized

All derivatives of each V_s have norm one. The product rule gives
||W_k^(r)(s)||<=k^r and, for the bounded charge displacement,

    ||G^(r)(s)|| <= 2^r k^(r+1), r>=1.

Charge pinching and fixed initial-depth compression are norm contractions.
The inherited exact bulk evenness removes the first and third derivatives
at zero. Since b=sin^2(s)=s^2+O(s^4), G1=G''(0)/2. The Banach-valued
Taylor estimate therefore gives

    ||G(s)-G0-s^2G1|| <= (2/3)k^5 s^4.

For beta<=1/2, s=arcsin(beta) obeys
s^2<=b/(1-b), s^2-b<=4b^2/3 and s^4<=16b^2/9. The coarse bound
||G1||<=2k^3 then yields

    ||G_k(b)-G0-bG1||
      <=[(8/3)k^3+(32/27)k^5]b^2 <=4k^5b^2.

The derivation uses a bounded charge observable, so it makes no invalid
subtraction of unbounded depth means. The final bound is uniform over all
prefix vectors. Its k dependence is explicit and is actually charged in
the growing-k choice.

## 3. Positivity and exact inward drift pass

Put l=ln2, v=v_k,

    X=-(l/2)sigma H,
    m=3lv/16,
    Y=(4m/k)sigma(Q-k/2),
    rho=sigma+bX+b^2Y.

All these matrices commute with sigma. Also H commutes with Q, so the
particular X and Y commute with each other; this is stronger than the
general fixed-k Hessian construction requires. Their trace and charge
constraints follow from the preceding orthogonality and
Var_sigma(Q)=k/4.

For Z=sigma^-1(rho-sigma), the stated premises give

    ||Z|| <=(l/2)bk^2+(3l/8)b^2k^2 <= l b k^2.

Under b k^4<=delta=2^-12 and k>=2 this is much smaller than 1/2.
Consequently rho is an actual strictly positive, normalized, charge-
preserving input density, not a formal perturbation with unchecked sign.

The leading bulk drift is bounded above by

    b^2[T(X)+2mI] <=-lv b^2 I/8.

Because sigma has zero exact bulk drift for every b, there is no residual
sigma contribution to the nonlinear remainder. The complete residual is

    b^3 Tr_input[(Y tensor I)G1]
       +Tr_input[((bX+b^2Y) tensor I)R_b],

where ||R_b||<=4k^5b^2. The trace-norm estimates are

    ||X||_1 <= l sqrt(v)/2,
    ||Y||_1 <=3lv/(8sqrt(k)).

Dividing the resulting residual bound by lv b^2/8 gives exactly

    3bk^(3/2)+16bk^5/sqrt(v)+12b^2k^(9/2).

Using v>=k^2/32 and b k^4<=delta bounds this by
(3+16sqrt(32)+12)delta, which is less than 0.026 and hence less than 1/2.
The exact bulk drift is therefore at most -lv b^2 I/16.
This is a strict operator inequality for the actual input and actual
nonzero beta. It does not come from a prefix average.

The resulting margin kappa=lv b^2/16 is positive and <=k under these
same bounds, so it meets the numerical hypothesis of the inherited coding
criterion. If a separate new representation is first proved only above a
larger finite threshold such as 2k, that threshold must be stated: the same
Lyapunov proof permits it with an enlarged finite boundary remainder. One
must not silently equate depth>=2k with depth>=k.

## 4. The entropy estimate and rate exponent pass

Weighted charge orthogonality eliminates the cubic cross term exactly:

    Tr(sigma Z^2)=l^2v b^2/4+9l^2v^2 b^4/(64k).

For |z|<=1/2, Taylor's theorem for (1+z)ln(1+z)-z gives a remainder
of magnitude at most 2|z|^3/3 after its z^2/2 term. It applies by joint
spectral calculus because sigma commutes with Z. After division by ln2,
the relative-entropy correction beyond lv b^2/8, measured relative to
the intended entropy excess lv b^2/16, is bounded by

    (9/8)b^2 v/k +||Z||[8/3+(3/2)b^2v/k].

With v<=k^2, k>=2 and b k^4<=2^-12 this is less than 1/2 by a wide
margin. The exact entropy identity against sigma consequently gives

    S(rho)-3k/2 >=lv b^2/32 >=l b^2 k^2/1024.

For k=floor(beta^(-1/2)/8), beta<=1/256 ensures k>=2,
b k^4<=2^-12 and k>=beta^(-1/2)/16. The actual coded rate is therefore

    S(rho)/k >=3/2+(ln2/16384) beta^(7/2),

CONDITIONAL on the stated all-k susceptibility and norm bounds.

The coding bridge is used at each fixed beta and its resulting fixed k.
Only afterwards is the communication horizon taken to infinity. The
outer family beta->0 may change k. This respects the fixed-before-horizon
contract. The same constructed code works pointwise for every fixed normal
initializer; no uniform finite-horizon initial-tail estimate is asserted.
All calls and physical outputs remain those of the original device.

The inherited full-diamond estimate retains the r-squared positivity factor,
auxiliary CPTP normalization and polar repair. Its half-diamond version is
one half of the full-diamond expression. No truncation, normalization or
dual-state preparation is implemented as a bath operation.

## 5. General superlinear susceptibility transfer

A quadratic lower is not essential for a new exponent. Suppose instead,
for all sufficiently large k, that

    v_k >= c k^(1+nu),  0<nu<=1,
    v_k <= C0 k^2,
    ||H_zeta|| <= C1 k^2,  ||G1|| <= C2 k^2,

with constants independent of k. Use the same minimizer and X,Y above.
The exact KKT inequality remains M>=v_k I. The dominant relative drift
remainder is at most

    (16/sqrt(c)) b k^p,  p=(9-nu)/2.

The other drift terms are O(bk^(3/2)) and O(b^2k^(9/2)). The relative
entropy correction is O(bk^2+b^2k), and positivity requires only
O(bk^2+b^2k^2)<1. Choose

    k=floor(epsilon b^(-1/p)),

where epsilon>0 is fixed small enough that
(16/sqrt(c))epsilon^p<1/4. Since p>=4, all the other corrections tend
to zero as b->0. For sufficiently small beta the exact drift is negative,
rho is positive, and S(rho)-3k/2>=lv_k b^2/32. Hence an actual reliable
rate satisfies

    Q-3/2 >= c' beta^[4-4nu/(9-nu)]

for a fixed c'>0. One possible asymptotic lower constant is
(ln2)c epsilon^nu/(32*2^nu), after increasing the small-beta threshold
enough to absorb the remaining errors and the floor.

For nu=1 the exponent is 7/2. For nu=1/2 it is 64/17. Every polynomially
superlinear v_k lower with nu>0 therefore suffices to improve the quartic
small-angle power by this safe remainder method. A merely linear lower
does not do so. This is a conditional transfer theorem, not evidence that
any of those growth premises holds for the device.

## 6. Concrete k^(3/2) transfer with explicit constants

The newer constructive premise is weaker than the conditional quadratic
premise above but still gives a stronger small-beta power than quartic.
Assume, for k>=4,

    k^(3/2)/32 <= v_k <= k^2,
    ||H_zeta|| <= k^2,    ||G1|| <= k^2.

Choose

    k=floor(beta^(-8/17)/8),    0<beta<=2^-11.

Then beta^(-8/17)/8>=2^(37/17)>4, so k>=4. The elementary
floor bound floor(x)>=x/2 for x>=2 gives

    k>=beta^(-8/17)/16,
    sqrt(k)>=beta^(-4/17)/4.

Also

    b k^(17/4)<=8^(-17/4)=2^(-51/4)<2^-12=:delta.

The relative drift remainder from section 3 is bounded by

    3 b k^(3/2)+16sqrt(32) b k^(17/4)+12 b^2 k^(9/2)
      <=(3+16sqrt(32)+12)delta <0.026<1/2.

Indeed the first term uses k^(3/2)<=k^(17/4), and the third obeys
b^2k^(9/2)=(bk^(17/4))^2/k^4<=delta^2<=delta. Thus the exact
bulk operator drift is at most -lv_k b^2 I/16. Positivity and the
entropy remainder estimates from sections 3 and 4 remain valid because
bk^2<=delta and b^2k<=delta^2. In particular,

    S(rho)-3k/2 >= (ln2)v_k b^2/32
                 >= (ln2)b^2 k^(3/2)/1024.

The full operator-drift coding theorem therefore supplies

    Q(V_beta,tau)>=3/2+(ln2/4096) beta^(64/17)

for every fixed beta in that interval and every fixed normal initializer,
with the same code sequence and pointwise vanishing full-diamond error.
The k^(3/2) all-prefix lower is now supported by the separately written and
independently checked all-length proof recorded next. No quadratic
susceptibility lower is needed. Nothing in this exponent calculation
licenses beta or k to vary with the coding horizon.

## 7. Independent all-length guard/prefix challenge

I read the final constructive note and independently reproduced its core
operator identity. This acceptance is analytic and does not rely on the
bounded symbolic replay or the preceding small-k coefficient tables.

On a deep core the interaction-frame toggle C_j changes exactly the charge
bit at j. The second-order charge-pinched coefficient is
G1=[C_-,C_+]; its same-index terms are kI-2Q. The distinct endpoint
terms have disjoint input/output charge-pattern supports. Each full pair
term has norm at most two, its square is supported on endpoint-charge
probability 1/2, and the diagonal coefficient has norm k. Therefore
v_tau<=k(k-1), ||H_tau||<=k(k-1), and ||G1||<=k². This also verifies
the uniform endpoint upper/norm bounds that were conditional in the initial
transfer challenge.

Use 1-based indices and choose i>=2 with q_(i-1)=1, q_i=0, q_j=1.
Assume the middle bits form a nonnegative meander. With P the product of
all calls before the guard g=i-1, and B the ordered middle calls, pure
word cancellation gives

    C_j C_i = P* U_g U_i B* U_j B U_g P,
    C_i C_j = P* U_g B* U_j B U_i U_g P.

Every balanced Dyck subword of the middle all-move word acts as a
permutation of its own color wires tensor the identity on the entire
bath. Such subwords cancel between B and B*. Only unmatched pushes
a_1,...,a_h remain. If the guard color is g and the endpoint color is z,
the two inner words take [g,0,a_1,...,a_h,z] respectively to

    [g,a_1,a_2,...,a_h,z,0],
    [a_1,g,a_2,...,a_h,z,0],

with EXACTLY the original bath in both cases. For h=0 use a_1=z.
Every local pop takes a locally pushed token. This proves the identity
on an arbitrary color basis and arbitrary bath basis, hence by linearity
on coherent bath vectors and states entangled with an untouched tail.

The difference is an input-only isometry times I-SWAP, tensor I_bath.
It commutes with the earlier prefix P and cancels P*P. Thus it survives
every auxiliary prefix-state contraction, with no diagonality, product,
separability, rank, or symmetry premise. The identity of raw local words
retains the root; its use as the selected block of G1 is a bulk statement.
The actual finite root region remains in the inherited coding theorem.

The normalized color Hilbert-Schmidt square of I-SWAP is one. The guard
and oriented endpoints have product-state probability 1/8. Hermiticity
gives an equal disjoint reverse-orientation contribution. For middle
length r, the meander probability is p_r=2^-r binom(r,floor(r/2)).
Orthogonal endpoint-pattern supports therefore give, for EVERY prefix tau,

    v_tau >= (1/4) sum_(r=0)^(k-3) (k-r-2) p_r.

The elementary binomial induction p_r>=1/sqrt(2(r+1)) yields

    v_tau >= (k-1)sqrt(k-2)/(8sqrt2)
           >=3 k^(3/2)/64 >= k^(3/2)/32, k>=4.

This proves the lower needed in section 6 uniformly over the full prefix
state space. The closest-point/KKT argument then converts it to the full
operator drift direction. No bath-state average is substituted for an
operator constraint.

The guard/meander requirements cannot simply be dropped: net positive
middle height allows a branch to consume an original bath token, invalidating
the input-only difference. The expanded independent token proof, complete
norm/count derivation and omission discussion are in
guard_meander_independent_challenge.md. The all-length source argument and
the explicit nonlinear transfer leave no surviving gap identified by this
bounded review. The stronger quadratic growth conjecture remains open.

## 8. Bounded integration review of the assembled proof

I read the actual assembled TEMPORAL_GROWTH.tex and
INHERITED_OPERATOR_CODING.tex. This was an integration check of claims,
indices, boundary scope, constants and error conventions, not a repeat of
the old capacity audit or a new historical-priority assessment.

The first assembled version had two repairable integration defects:

1. The copied coding section retained numeric equation references that
   now pointed to unrelated formulas in the new main proof. These were
   replaced with distinct C1--C12 tags and corresponding references.
2. The sentence following equation (18) could promote the bulk
   charge-raising/lowering identity to the entire bath. The final version
   distinguishes whole-bath raw word permutations from their bulk-only
   identification with the raising/lowering coefficient. It also records
   the vacuum C_1 counterexample showing why that distinction is necessary.

I inspected the corrected actual files. The guard/endpoints use consistent
zero-based indices, the exact prefix coefficient applies at depth>=k after
its deeper algebraic proof buffer, and the actual root remains inside the
Lyapunov boundary remainder. The state, nonlinear remainder, beta range,
floor and ln2/4096 coefficient match the accepted transfer. The stronger
quadratic growth/beta^(7/2) claim is explicitly conditional. The additional
coherent-information equality is restricted to the actual tau_pi, where
the included finite bath-entropy argument applies.

The coding section retains full-diamond error

    min{2, 4 e_m + 2 sqrt(1-Tr(P_(<=A_m) tau))}

and now states its half-diamond conversion explicitly:

    min{1, 2 e_m + sqrt(1-Tr(P_(<=A_m) tau))}.

The initializer-independent code quantifier remains pointwise. Beta and
the resulting block length stay fixed before the horizon. The included
INHERITED_COMPRESSION.tex is byte-identical to the actual Cycle5 source,
with its r² factor, auxiliary normalization and polar repair preserved.

Decision: integration accepted after the two recorded repairs; no further
load-bearing integration gap was identified. The receipt records SHA256
identities of the exact main and included sources inspected. This decision
does not certify compiled-PDF rendering, primary-reference priority, or
later edits to different source hashes.

## Resource and status record

This challenge was analytic source review. No additional numerical sweep,
long-time cutoff simulation, paid resource, or external outreach was used.
Total inference, discovery and independent-review costs are unmeasured.
The original all-k growth gate has been met by the guard/meander operator
identity and counting argument. The remaining stronger questions concern
the optimal susceptibility growth/order and tighter admissible nonlinear
windows, not a missing finite-check count. No claim of efficient minimizer
computation, useful blocklength or physical device implementation follows.
