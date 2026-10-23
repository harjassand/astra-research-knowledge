# Cycle8 principal construction: exact nonlinear transfer and beta-cubic rate

Author: Astra Pro1 /root. Date: 22 October 2026, Australia/Brisbane.
This proof uses the actual Cycle7 source and the new all-length endpoint
response lemma in contributions/weighted_remainder/WEIGHTED_BERNSTEIN_BOUND.md.
The exact symmetric-prefix susceptibility is inherited, not reproved.

## 1. Fixed model and inherited data

E=C2_seed tensor F(C2), U=[[R,S1,S2],[S1*,0,0],[S2*,0,0]],
V=alpha U+i beta I, alpha=sqrt(1-beta²), b=beta².
W_k is the ordered product through the same bath. L+Q_k is conserved,
including the vacuum exchange. All k calls and every retained register count.
No fresh bath, reset, bath access, preshared entanglement, postselection,
backward quantum wire, timing resource or terminal-return requirement is added.

In the native bulk (initial depth >=k), G(b)=Q-W_k*QW_k has the exact
charge-pinched first-k-prefix representation from Cycle7.
sigma=diag(1/2,1/4,1/4)^tensor k and -log2 sigma=kI+Q.
The explicit H of Cycle7 is Hermitian, charge preserving and input-offdiagonal,
commutes with sigma, and obeys

 Tr sigma H=Tr sigma QH=0,
 v=Tr sigma H²,
 T_k(sigma H)=v I,
 k²/32 <= v <= k(k-1)/8 <= k²,
 ||H|| <= k(k-1) <= k².

Cycle7 also proves the exact formula for v, with v/k² ->1/8.
H is built from the original k-call endpoint blocks. In the response lemma,
deleting spectator calls does NOT replace H with a shorter-block optimizer.

The diagonal input-history identity is exact at every b:
for every computational-diagonal input density D,
 D_b(D)=Tr D[(1-b)(2Q-k)] I in the bulk.
It extends linearly to diagonal signed input operators.
In particular D_b(sigma)=0 exactly, uniformly on the entire prefix.

## 2. The new all-order response used here

Let N=k(k-1)/2. For all k>=2 and 0<=b<=1, the exact endpoint lemma gives

 E_sigma[(H tensor I)G(b)] = b(1-b) F_k(b),
 F_k(0)=v I,
 ||F_k(b)-v I|| <= N[1-(1-b)^(k-2)] <= N(k-2)b.        (1)

This is a full operator bound. It retains coherent prefix vectors and final
bath overlaps. It follows from exact paired histories, a signed partial-trace
norm bound, and a sum of positive Bernstein weights; it does not replace
coherent amplitudes by independent physical error probabilities.

Because v>=N/8,

 ||F_k(b)-v I||/v <=8 b(k-2).                          (2)

The old uncontracted derivative bound is not used in this transfer.

## 3. Actual input and uniform positivity

Fix k>=2 and b>0 with

 b k² <=1/16.                                        (3)

This implies b<=1/64. Write l=ln2 and set

 m=3lv/16,
 X=-(l/2)sigma H,
 Y=(4m/k)sigma(Q-k/2),
 rho=sigma+bX+b²Y,
 Z=sigma^(-1)(rho-sigma).

H, Q, sigma commute. Thus all matrices entering this functional calculus
commute with sigma; X and Y commute with each other. The variance of Q under
sigma is k/4. Consequently Tr X=Tr QX=Tr Y=0 and Tr QY=m, so Tr rho=1.

The spectral bound is

 ||Z|| <=(l/2)b k²+(3l/8)b²v
       <=l b k²(1/2+3b/8)
       <1/16<1/2.                                    (4)

Here l<1, b<=1/64 and v<=k². Hence rho is strictly positive, normalized and
charge preserving. It is a real physical input density, independent of the
bath initializer. The analytic prefix optimizer is never prepared.

## 4. Exact inward drift

The diagonal identity gives D_b(Y)=2m(1-b)I exactly.
Combining it with D_b(sigma)=0 and (1),

 D_b(rho)=l b²(1-b)[3v I/8-F_k(b)/2].                 (5)

No generic remainder has been charged against sigma. No independent
T_k(Y) remainder is needed because the complete diagonal response is known.

For integer k>=2, (k-2)/k²<=1/8, since (k-4)²>=0.
Therefore (3) gives b(k-2)<=1/128, and (2) gives

 F_k(b) >=(15/16)v I.

Equation (5) implies

 D_b(rho) <= -3 l v b²(1-b) I/32
           <= -kappa I,
 kappa=l v b²(1-b)/16>0.                              (6)

Also kappa<=k: for example v<=k², b k²<=1/16 and b<=1/64 give
kappa<=1/16384<k. The physical statement is (6) compressed to depth>=k.
No inward sign is imposed at the root.

## 5. Entropy with a uniform nonlinear remainder

The exact relative-entropy identity is

 S(rho)-3k/2 =m b²-D2(rho||sigma).                     (7)

Input offdiagonality removes the H--Q cross term, so

 Tr sigma Z² =l² v b²/4+9l²v²b^4/(64k).              (8)

For real |z|<=1/2, Taylor's theorem gives
|(1+z)ln(1+z)-z-z²/2| <=2|z|³/3.
Apply it by joint spectral calculus, using Tr sigma Z=0.

The quadratic term of D2 is l v b²/8 plus the Y² contribution.
Writing t=b²v/k, the remaining upper error, divided by l v b²/16, is at most

 (9/8)t+||Z||[8/3+(3/2)t].                            (9)

From (3), v<=k² and k>=2, t<=1/2048. From (4), ||Z||<1/16.
Thus (9) is at most

 1/6+39/65536 <1/2.

Subtracting from m b²-l v b²/8=l v b²/16 in (7) proves

 S(rho)-3k/2 >=l v b²/32 >=l b² k²/1024.             (10)

This is a uniform growing-k estimate, not a fixed-k O(b³) expansion.

## 6. Full same-bath coding consequence

Fix 0<beta<=1/8 and choose

 k=floor(1/(4 beta)).                                 (11)

Then k>=2, k>=1/(8 beta), and b k²<=1/16.
Both beta and this k,rho are fixed BEFORE the outer coding horizon.

The inherited homogeneous-Kraus operator-drift theorem applies to (6).
For completeness its interface is: a charge-preserving k-call density with
exact inward drift <=-kappa I on depth>=k, 0<kappa<=k, admits an initializer-
independent deterministic unassisted code sequence at rate S(rho)/k, with
pointwise vanishing full-diamond error for every fixed normal initializer.
It retains the finite root term. It does not assume scalar depth dynamics
or independent physical block channels.

The proof is reproduced in INHERITED_OPERATOR_CODING.tex and
INHERITED_COMPRESSION.tex. It uses t_L=kappa/(2k²), lambda=1-kappa²/(4k²),
the finite-boundary exponential moment, exact spectral types, the r²
positive-block factor, auxiliary CPTP normalization and polar repair.
The encoder remains isometric; the auxiliary normalization is not implemented.

The actual full-diamond estimate for every fixed normal tau is

 min{2,4e_n+2 sqrt(1-Tr(P_{<=A_n} tau))} ->0,

with the same code for all tau. The half-diamond estimate is exactly half.
There is no uniform finite-horizon assertion over all normal tau, and no
finite mean-depth premise is added for those tau.

Dividing (10) by k and applying (11) yields the new theorem

 Q(V_beta,tau)>=S(rho)/k
              >=3/2+(ln2/8192) beta³,
 0<beta<=1/8.                                         (12)

For the actual tau_pi the product-block coherent-information limit is
S(rho)/k, using the inherited finite exponential-moment/entropy argument.
No terminal bath return is required or concluded.

## 7. Comparison under the same operation

The exact v_k law, scalar first coefficient and coding interface are inherited.
What changes is the all-order contraction and allowable temporal scale:
the sufficient window improves from b k^4<=2^-12 to b k²<=1/16,
and the demonstrated excess power changes from beta^(7/2) to beta³.
No sharp capacity exponent, general converse or feedback equality follows.

The pair and actual non-scalar four-call constructions remain admissible.
Their unchanged parameters are delta=b²/512, q=1/2-delta, c=-b/128,
x=q², y=q(1-q)/2, z=(1-q)²/4. Pair eigenvalues are x, four z,
two y+c, two y-c. The four-call entropy identity is

 S(rho4)/4 =S(omega)/2+(xy/2)[1-h2((1+c/y)/2)].

A simple analytic comparison on beta<=1/8:
S(omega)/2-3/2<=delta, y>=1/16, x<=1/4, |c/y|<=1/2.
The natural-log function f(t)=[(1+t)ln(1+t)+(1-t)ln(1-t)]/2 has
f''(t)=1/(1-t²)<=4/3 on [-1/2,1/2]. Since 1-h2((1+t)/2)=f(t)/ln2,
one has 1-h2((1+t)/2)<=t²/ln2 there. Thus

 S(rho4)/4-3/2 <=b²[1/512+1/(8192 ln2)] <b²/256.

At beta=1/512 the new guaranteed excess is (ln2)2^-40, which is strictly
larger than this upper bound 2^-44 on the retained explicit four-call rate,
as well as the pair guarantee 2^-46. This comparison concerns the actual
known constructions, not the unknown optimum over every four-call input.
The exact entropy evaluation is recorded separately at high precision.

The new block at beta=1/512 has k=128 and full input rank 3^128.
The code is an existence theorem. The large spectral-type and Lyapunov
constants are retained; no efficient matrix/compiler or useful throughput
follows from the stronger lower bound.

## 8. Actual receiving use and next scientific decision

The Cycle7 scalar certificate supplies the uniform leading negative drift.
Its explicit endpoint block formula supplies the trace-norm budget1/4
which makes the nonlinear response summable. The inherited coding operation
turns the new exact operator drift into actual reliable communication.
These are specific mathematical uses with a new consequence, not a claim
of causal research-process or recursive-intelligence amplification.

This endpoint-response operation is now controlled on the needed range.
The next consequential question is the one-sided positive spectrum of H
and admissible positive reparametrizations of the input. The present beta³
rate uses ||H||<=k² only to pay positivity/entropy; response itself permits
b k small. Determine whether the maximal positive eigenvalue of this explicit
H genuinely forces k=O(1/beta) for the linear density, or whether a sharper
spectral/free-energy argument permits longer blocks while retaining exact
operator drift. A Gibbs/exponential replacement introduces higher charge
coherences and must pay their actual response; no automatic extension is
claimed. No new spectral computation or guessed exponent is promoted here.

The broader mission remains active. Historical novelty, external acceptance,
efficient realization, useful finite-blocklength and physical device claims
remain separate and unestablished. Recorded replay times do not measure total
discovery, inference or review cost.

