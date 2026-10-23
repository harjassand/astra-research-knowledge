# Independent challenge of the nonlinear endpoint response

Reviewer: /root/cycle8_independent_challenge  
Date: 22 October 2026, Australia/Brisbane

## Verdict and boundary

I independently reconstructed the two-history charge selection, the exact
cancellation of the output-charge factor, the endpoint weighted trace norm,
and the resulting uniform operator remainder. I then read the actual
contributor proof WEIGHTED_BERNSTEIN_BOUND.md. No surviving gap was found in
that new all-k lemma. The sharper one-quarter trace bound is valid; it does
not follow merely from a Hilbert--Schmidt estimate.

The proof uses the original k-call H in every deletion-mask term. Replacing it
by a newly optimized shorter-block H would be a different, unproved identity.
The physical root is outside this bulk word identity and remains present in
the coding theorem. The analytic symmetric-prefix density is never prepared.

The inherited exact v_k and scalar first coefficient were read in the actual
Cycle7 source and treated as already established, rather than reviewed again.
This document is a new load-bearing challenge, not an entire capacity audit.
Internal review is not external certification or a historical priority claim.

## 1. Independent phase and output-charge check

Fix an initial complete binary charge pattern x with endpoint charges 01,
and y obtained by exchanging those endpoints to 10. On initial depth at least
k, each nonidentity call flips its own port charge; each stay preserves it.
Given a common output charge word, the two histories therefore use the same
choice at every spectator call and opposite choices at both endpoints.

For this independent derivation let s=(s_i,s_j) denote the ket STAY mask.
The common endpoint factor in the paired amplitudes is b(1-b), with signs

| ket stay mask s | bra stay mask | phase sign | output endpoint charge |
|---|---|---|---|
| 00 | 11 | -1 | 1 |
| 01 | 10 | +1 | 2 |
| 10 | 01 | +1 | 0 |
| 11 | 00 | -1 | 1 |

For a fixed spectator stay mask S, the remaining scalar weight is exactly
b^|S| (1-b)^(k-2-|S|). The phases arise from the amplitudes i beta, not from a
classical replacement of coherent moves.

Let R_s be the raw cross-history operator, compressed between x and y. It is
a product of two unitary histories with orthogonal charge projections, so
||R_s|| <= 1. The full circuit with the spectator calls fixed to U or I and
only the two endpoints equal to alpha U+i beta I remains unitary. Its x,y
offdiagonal block in W*W is zero. Since the four endpoint terms have the
same b(1-b) factor, this proves

    -R_00 + R_01 + R_10 - R_11 = 0.

All spectator output charges are fixed by x and S. Their common contribution
to W*QW cancels by this identity. Subtracting one from the endpoint output
charge cancels as well. The surviving contribution to Q-W*QW is

    R_10 - R_01,

a difference of two contractions. Its norm is at most two, with no factor k.
The contributor uses MOVE masks, so its A_01-A_10 is the same operator.
This convention difference changes labels, not signs in the physical claim.

This cancellation is the essential point that an elementary bound on ||Q||
would miss. It holds before choosing a bath vector or taking an expectation.

## 2. Coherent-prefix and direct-sum check

At a fixed endpoint pair, the complete charge patterns form disjoint pairs.
Adding each oriented block and its adjoint therefore gives an operator
B_ij^S of norm at most two. Summing pattern blocks does not add a factor
2^(k-2): it is an orthogonal direct sum.

Every raw physical history is evaluated with its actual final bath state.
The contractions retain the overlap of the two final bath words. Thus the
proof applies to every complex coherent prefix and its entanglement among
coordinates. It does not assert a scalar depth chain.

The finite-prefix representation follows from the native physical bulk
history: at most k original colors are consumed, and the equal total input
charge makes the untouched tail lengths agree. An initial depth of k may
reach vacuum only after the final pop; it cannot undergo a root exchange
earlier. A deeper temporary core can identify the finite coefficient but
does not move the physical coding boundary.

## 3. Independent verification of the one-quarter trace norm

Write H=sum H_ij as in the actual Cycle7 source. The two endpoints have
opposite charge with total sigma probability 1/2. Conditional on a complete
charge pattern with q colored sites, sigma is uniform on its 2^q color wires.

In the h>d case the oriented block is K=P(I-SWAP), with P unitary. Hence

    |K|=I-SWAP,
    2^(-q) Tr |K| = 1/2.

The last equality uses two distinct input color qubits: SWAP has normalized
trace 1/2. Equivalently its symmetric and antisymmetric multiplicities are
3 and 1. This is a trace-norm calculation, not an operator-norm estimate.

In the h=d case K=P/2, whose normalized trace norm is also 1/2. In the h<d
case K=0. The Hermitian orientation pair has absolute value with diagonal
blocks |K| and |K*|; both have the same singular-value sum. Thus there is no
extra orientation factor after accounting for the two charge sectors.

Because [H_ij,sigma]=0,

    ||sigma H_ij||_1 = Tr(sigma |H_ij|) <= (1/2)(1/2) = 1/4.

For any finite-dimensional trace-class input X and bounded joint operator B,

    ||Tr_A[(X tensor I)B]|| <= ||X||_1 ||B||.

For Hermitian X this follows by diagonalizing X and applying the operator norm
bound to each input diagonal block. It holds with an infinite bath as well.
Consequently the actual k-call contractions

    A_ij,S = Tr_A[(sigma H_ij tensor I) B_ij^S]

have norm at most 1/2. They are Hermitian by input partial-trace cyclicity;
commutation with B_ij^S is unnecessary.

## 4. Exact all-b identity and contracted remainder

The charge selection gives, with a=1-b and N=k(k-1)/2,

    Tr_A[(sigma H tensor I) G(b)] = b a F_k(b),

    F_k(b)=sum_{i<j} sum_S b^|S| a^(k-2-|S|) A_ij,S.

Here H always remains the original k-call input observable. The mask S is a
term in an exact algebraic sum, not an omitted physical call or a free reset.

The empty mask has weight a^(k-2), and the actual Cycle7 scalar certificate is

    sum_{i<j} A_ij,empty = v_k I.

Since all remaining normalized weights are nonnegative and
||A_ij,S|| <= 1/2,

    ||F_k(b)-v_k I||
       <= N [1-a^(k-2)]
       <= N(k-2)b,              0 <= b <= 1.

No small-b expansion or finite-k evidence proves this inequality; the exact
finite sum and its norm bounds do. It includes k=2, where the right side
vanishes.

If R_b=G(b)-G0-bG1, the actual contracted remainder is

    Tr_A[(sigma H tensor I)R_b]
       = b a (F_k(b)-v_k I)-b^2 v_k I.

Therefore

    ||Tr_A[(sigma H tensor I)R_b]||
       <= b^2 [v_k + N(k-2)].

This controls the entire nonlinear remainder, not just G2. Its order is
O(k^3 b^2), uniformly on the full prefix. The coefficient identity

    Tr_A[(sigma H tensor I)G2]
       = sum_{i<j} sum_{r notin {i,j}} A_ij,{r} -(k-1)v_k I

also follows by differentiation, but is weaker than the all-b result.

## 5. Exact diagonal correction and transfer constants checked independently

For a fixed computational input word of total charge q, different move/stay
histories have distinct output charge words in the bulk. The depth change
has expectation (1-b)(2q-k), independently of the bath vector. Consequently

    D_b(sigma)=0,
    D_b(Y)=2m(1-b)I

for the actual diagonal Y=(4m/k)sigma(Q-k/2), where Tr Y=0 and Tr QY=m.
The second identity is exact. In particular T_k(Y)=-2mI and every higher
coefficient of D_b(Y) vanishes.

For the actual rho=sigma+bX+b^2Y, X=-(ln2/2)sigma H and
m=3(ln2)v_k/16, the exact bulk drift is

    D_b(rho)=(ln2)b^2(1-b)[3v_k I/8-F_k(b)/2].

Using v_k>=N/8 gives

    ||F_k(b)-v_k I||/v_k <= 8b(k-2).

Under the parent's proposed uniform window bk^2<=1/16, k>=2,

    b(k-2) <= 1/128,

because k^2>=8(k-2). Thus the relative response error is at most 1/16,
and the drift is at most

    -3(ln2)v_k b^2(1-b)I/32,

which is stronger than the proposed retained margin
-(ln2)v_k b^2(1-b)I/16.

For the same rho, the inherited entropy calculation requires only a uniform
bound on Z=sigma^(-1)(rho-sigma), rather than the old bk^4 window. Here

    ||Z|| <= (ln2)bk^2 <= (ln2)/16 < 1/16,
    u=b^2 v_k/k <= 1/2048,

using the deliberately coarse v_k<=k^2. The old relative entropy remainder
bound becomes

    (9/8)u + ||Z||[8/3+(3/2)u]
       < 1/6 + 39/65536
       < 1/2.

This proves the same entropy margin S(rho)-3k/2 >= (ln2)v_k b^2/32.
Positivity is strict because ||Z||<1/2. Charge preservation and normalization
are unchanged.

If k=floor(1/(4 beta)) and 0<beta<=1/8, then k>=2,
bk^2<=1/16 and k>=1/(8 beta). The retained v_k>=k^2/32 therefore gives

    S(rho)/k >= 3/2 + (ln2/8192) beta^3.

The new drift has 0<kappa<=k, so it satisfies the existing operator coding
interface. The fixed-before-horizon rule is essential: beta, k and rho are
fixed before the spectral-type/code limit. The inherited proof then provides
the same initializer-independent code sequence with pointwise full-diamond
convergence for each fixed normal initializer, including the actual tau_pi.
No terminal bath return is added. The physical root remainder, r^2 compression
factor, auxiliary CPTP normalization and polar repair remain necessary.

This is my independent check of the proposed transfer constants. The assembled
parent source still needs to match this checked argument.

## 6. Explicit omitted-premise boundary

The bulk charge-flip premise fails at the actual root. With one call, port
input |0>, and the vacuum seed in the +1 eigenvector of R, both U and I preserve
port charge zero. V acts by the phase alpha+i beta and the actual depth drift
is zero. The extrapolated bulk formula would instead give -(1-b), which is
nonzero for b<1. Thus the bulk identity cannot be applied globally or used to
erase the finite root term in the Lyapunov argument.

A general charge-preserving H with four differing endpoint bits does not have
the two-endpoint history selection above. The proposed reusable interface must
state pair support, the actual signed input trace norm, and a known first
operator certificate. A favorable average is insufficient.

I independently verified the concrete four-endpoint witness supplied by the
constructive contributor, using a separate raw prepend/pop implementation with
no inherited representation import. Let x=0101, y=1010 and initial bath=1211.
The input patterns differ at all four sites. Complementary stay masks are the
only possible matched histories, all with scalar weight b^2(1-b)^2. Of the
16 mask pairs, 14 have identical complete output and bath. Summing their exact
signed depth increments gives one. Therefore

    <x,1211|G(b)|y,1211> = b^2(1-b)^2.

For K=|x><y|+|y><x|, the diagonal bath entry of E_sigma[K G(b)] is consequently
b^2(1-b)^2/32, even though K has no pair-supported component. Thus deleting
the pair-support premise and keeping the same pair formula gives a false
identity. The standalone four_endpoint_witness.py and its JSON list all
matched histories and phases; this is an exact finite counterexample, not a
finite-check proof of the all-length lemma.

## Cost and acceptance scope

This challenge used analytical reconstruction, actual source reads, and one
independent 16-mask counterexample verification. I ran no old capacity suite or
numerical search. That witness script measured 0.00004646899469662458 seconds
and 8576 KiB peak RSS; these are replay costs. Total inference and
review resource costs are unmeasured. Hashes record the exact reviewed source
versions, not mathematical truth. The result is internal scientific acceptance
of the stated new lemma and proposed transfer, subject to final-source matching.
It is not historical novelty, external peer review, efficient implementation,
finite-code usefulness, receiver integration, or a capacity converse.

## Principal transfer and actual comparator source review

I read the actual work/cycle8/UNIFORM_TRANSFER.md after the independent
reconstruction above. Its uniform input, exact drift, entropy and coding
conclusion match the checked argument. In particular beta is fixed before k
is chosen and both are fixed before the coding horizon. No unknown initializer
tail is multiplied by a type-probability penalty.

For the new ordinary-comparator claim I additionally read the original
Cycle4 CORRELATED_CAPACITY_GAIN.tex Eq. (19) and Cycle5 FIXED_BLOCK_ORDER.tex
Eqs. (37)--(41). The stated four-call entropy formula is exactly the inherited
deletion of one reducing coherence, not a weakened diagonal comparator.

The upper comparison follows analytically. With delta=b^2/512, c=-b/128,
x=q^2<=1/4, y=q(1-q)/2>=1/16 and q=1/2-delta:

    S(omega)/2-3/2 <= delta,
    S(rho4)/4-S(omega)/2
      =(xy/2)[1-h2((1+c/y)/2)]
      <=x c^2/(2y ln2)
      <=b^2/(8192 ln2).

Thus the retained explicit four-call rate is below 3/2+b^2/256. At beta=1/512,
the new theorem's excess (ln2)2^(-40) exceeds 2^(-44), since 16 ln2>1.
This comparison concerns the actual known rho4, not every possible four-call
state. Its mathematical conclusion is valid.

The bound on the binary entropy used here comes from the NATURAL-LOG
function f(t)=((1+t)ln(1+t)+(1-t)ln(1-t))/2, for which
f''(t)=1/(1-t^2)<=4/3 when |t|<=1/2. Hence
1-h2((1+t)/2)=f(t)/ln2<=t^2/ln2. I requested that explicit convention in the
parent's prose; no inequality or theorem constant needed correction.

The selected next question about the one-sided spectrum of H is stated as an
unresolved continuation, not incorporated into the new rate. The current proof
does not claim that the sufficient positivity scale is a structural converse.


## Final assembled-source match

I read NONLINEAR_ENDPOINT_RESPONSE.tex in full and checked it against the
accepted endpoint and principal transfer sources. The integrated stay-mask
phase convention, unitarity cancellation, Fidentity/Bernstein equations,
quarter trace budget, exactdrift inequality, entropy constants and code
quantifiers match the reviewed arguments. The natural-log comparison wording
is repaired. The four-endpoint mask table matches the independent raw replay.

The all-order coefficient formula follows by coefficient extraction from the
same exact Bernstein identity. The finite nonscalar and skipped-optimizer
counterexamples are explicitly presented as finite witnesses. They are not
used to prove the all-length response or its rate consequence.

Both inherited TeX files are byte-identical to the actual Cycle7 versions.
The merged COMPLETE_PROOF.tex.txt is exactly the principal TeX source with its
two input directives replaced by those complete inherited files; there is no
missing appendix or altered coding interface.

Accepted assembled scientific source identities:

- NONLINEAR_ENDPOINT_RESPONSE.tex: 28,352 bytes, SHA256
  2d519d19c661e54f327126cd9f6e56812f7c456bd979ceaf7b9aeb9d16140bea.
- COMPLETE_PROOF.tex.txt: 39,142 bytes, SHA256
  28ee6f1bddff19cbd8727e10d99e5f756863d007aefbe7d6dc65a0561d0eeaf8.
- INHERITED_OPERATOR_CODING.tex: SHA256
  d61719a490ff0dd206c7a4a3d09aed91f604b4aafe4d38344efe71f591a3884e.
- INHERITED_COMPRESSION.tex: SHA256
  278f881e709240f029720835960295e8f4dab721c6347109974d351e154e3101.

No surviving mathematical gap was found in the assembled new argument under
its stated premises. The cubic exponent remains an achievable lower bound.
The next spectral question remains open. This final match does not certify
historical originality, practical finite-code performance, receiving use,
external acceptance, or repository integration.



