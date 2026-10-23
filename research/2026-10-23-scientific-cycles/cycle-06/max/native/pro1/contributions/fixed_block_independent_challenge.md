# Focused independent challenge: fixed-block order and operator coding bridge

Reviewer: fresh Cycle5 independent challenge. Date: 22 October 2026,
Australia/Brisbane. This is internal source-specific review, not external
certification, historical-priority verification, or evidence of efficient
implementation. The Cycle4 capacity theorem was used as the established
comparator; its entire old audit was not repeated.

## Source reviewed and decision

Read `fixed_block_obstruction.md` in full and the relevant actual Cycle4
`CORRELATED_CAPACITY_GAIN.tex` model and coding interface. Independently
reconstructed the new global drift/entropy argument, checked the constants,
and challenged the treatment of the vacuum, unbounded depth, nonidentical
inputs, and horizon-dependent optimization.

**Decision:** the fixed-k quartic coherent-information upper bound is valid
under its charge-preserving independent-input-block hypotheses. The stronger
version using bounded charge transfer is valid for **every normal initializer,
uniformly over the initializer**, without a finite depth or entropy assumption.
The arbitrary-reference *lower-code convergence* remains pointwise in the
initializer, as in the inherited construction. These are different quantifiers.

No known load-bearing gap remains in the reviewed upper argument. The
operator-Lyapunov extension, the explicit non-scalar four-call density, and
the entropy-Hessian-to-code interface described by the owner were separately
checked below. Final manuscript wording must retain the limits recorded here.

## 1. Bounded charge transfer resolves the infinite-depth obligation

Let Q count colors in a k-call input block. Conservation of L+Q gives
G_s=Q-W_s^*QW_s, with norm at most k. This bounded operator agrees with the
depth displacement on the finite-coordinate core; the proof must use G_s,
not subtract possibly infinite means of L.

For n blocks the exact bounded identity is

    Q_total-W_total^*Q_total W_total
      =sum_j W_<j^*(Q_j-W_j^*Q_j W_j) W_<j.

Indeed Q_j commutes with every block interaction except W_j. Interactions
after j cancel in W_total^*Q_jW_total; interactions before j conjugate the
remaining term. Thus its expectation is a well-defined accumulated charge
transfer for every normal bath density. Independent *input* blocks imply
that the jth term has expectation Tr[tau_(j-1) D_s(rho_j)]. Correlations
between the bath and previously emitted outputs do not change this marginal
identity. No physical-channel independence or reset is introduced.

The entropy inequalities also avoid infinite environmental entropies. Purify
the finite-dimensional full input by R. Both R and the complete external
output B are finite-dimensional, and

    I_c=S(B)-S(RB) <= S(R)=H_in,
    I_c <= 2 S(B)-H_in.

They follow directly from Araki--Lieb. An inaccessible purification of the
bath may be infinite-dimensional; no entropy of that purification is needed.
This justifies the all-normal upper theorem, including infinite-entropy and
infinite-mean bath states.

## 2. Root absorption and bulk parity are separate valid steps

At beta=0 the ordered device is a basis permutation. Every zero input at the
vacuum contributes one extra unit relative to the formal bulk drift. Hence
G_0 >= (2Q-k) tensor I on the whole bath, with equality on initial depth>=k.

For charge-preserving rho, covariance of W_s under exp[it(L+Q)] gives
[D_s(rho),L]=0. Therefore the low-depth and high-depth restrictions have no
cross terms. Without this covariance, two diagonal compression estimates
would not establish a global operator lower bound.

On initial depth>=k no U history encounters the vacuum before a call. Given
the same input charge and the same output word, all interfering histories
have the same parity of stay counts. Hence the input-charge compression of
the bulk drift is even in s, including complex charge-sector coherences.
This removes the first derivative only in the bulk. Root terms can have odd
powers and are not discarded.

For sigma=rho_c^tensor k the exact reference drift is

    B_s=(a/2) sum_{j=0}^{k-1}(T_s^*)^j P0.

It is scalar on each depth space, supported on depth<k, and is at least
(3/8)^k P_<k for beta<=1/2. At depth ell<k the path of ell consecutive
downward moves has probability (a/2)^ell and contributes in term j=ell.
This proves a positive margin for every seed/color vector, including coherent
ones. It is not merely a statement about radial expectations.

The producer's safe absorption uses
||D_s(rho-sigma)||<=k||rho-sigma||_1 and
|2 Tr(Q(rho-sigma))|<=k||rho-sigma||_1. Thus its 2k trace-distance loss and
threshold gamma/(2k) are sufficient. A sharper bound could use
H_s=kI-Q-W_s^*QW_s, whose norm is at most k; that sharpening is unnecessary.

## 3. Constants and entropy optimization checked

For V_s=cos(s)U+i sin(s)I, V_s, V_s', V_s'' have norm one. Thus
||W_s'||<=k, ||W_s''||<=k^2, ||G_s'||<=2k^2 and ||G_s''||<=4k^3.
Since arcsin(beta)<=2 beta/sqrt(3) for beta<=1/2, the stated
B_k=4k^2 and C_k=4k^3 are conservative valid constants.

The exact identity

    epsilon=S(rho)-3k/2=Delta-D_2(rho||sigma)

uses -log2 sigma=kI+Q. Quantum Pinsker in bits gives
||rho-sigma||_1<=sqrt(2 ln(2) D). Combining the near-reference operator
bound with the coarse far-reference bound yields the producer's global
relative-entropy-penalized drift inequality for every charge-preserving rho.

The output inequality S(B)<=3nk/2+sum Delta_j-transfer retains output
correlations through subadditivity; it does not assume independent outputs.
Taking three quarters of I_c<=H_in and one quarter of
I_c<=2S(B)-H_in eliminates the entropy-shift variable. Cauchy--Schwarz then
gives, with u=B_k beta/D0<=1/2,

    (I_c-3nk/2)/n
      <= -(1-u) Dbar/2
         +(C_k beta^2 sqrt(2 ln2)/2) sqrt(Dbar)
      <= (C_k^2 ln2/2) beta^4.

Dividing by k gives 8 k^5 ln2 beta^4. Every step is uniform in n and in
the individual rho_j, so nonidentical and horizon-dependent product blocks
are included. Entanglement/correlation between different input blocks is
not included.

The explicit beta_k deteriorates strongly with k. In particular its
conservative k=4 value is much smaller than 1/512. The theorem is a
fixed-k small-angle order statement, not a numerical quartic upper bound
at the selected actual angle without additional work.

## 4. Independent check of the owner's operator-Lyapunov coding extension

For any fixed charge-preserving k-call rho, choose its eigenvectors inside
charge sectors. Every Kraus amplitude K_(o,lambda) has exact depth grade
d=Q(lambda)-Q(o), including the vacuum exchange of grade zero. Set

    A_d=sum_{o,lambda with grade d} K_(o,lambda)^* K_(o,lambda).

Then A_d>=0, sum A_d=I, |d|<=k and [A_d,L]=0. On the finite-coordinate
core, and then as positive quadratic forms,

    Phi^* exp(tL)=[sum_d exp(td) A_d] exp(tL).

If D=sum d A_d <=-kappa I on depth>=k, with 0<kappa<=k, choose
t=kappa/(2k^2). Since kt<=1/2, the exponential Taylor remainder is at most
k^2 t^2 I. Therefore on the bulk the bracket is at most
lambda I, lambda=1-kappa^2/(4k^2). On depth<k it is at most exp(kt)I.
Consequently

    Phi^* exp(tL) <= lambda exp(tL)+exp(2kt) P_<k.

Normal monotone extension and iteration give a uniform moment bound and the
finite-coordinate tail bound needed by the inherited joint compression
interface. The cutoff is analytic, not a bath operation. Spectral types of
the fixed rho have polynomial maximum-type mass with exponent at most 3^k;
their domination transfers the average tail bound through the one W_(km).
The inherited r^2 factor, CPTP auxiliary normalization and polar repair remain
necessary. The same code sequence then works pointwise for every fixed normal
initializer, with rate S(rho)/k and full-diamond error tending to zero.

No scalar depth-chain or radial-state hypothesis is needed. If actual bath
entropy is also desired, finite mean depth implies
S(tau)<=2 Tr(L tau)+2 using the normalized Gibbs density whose eigenvalue
at each depth-ell vertex is 2^(-2ell-2). This applies to coherent states too.

## 5. The explicit non-scalar four-call density passes

Let omega be the established pair density with parameters x,y,z,c and c<0.
In omega tensor omega, the subspace spanned by |1000>,|0100> is a reducing
2-by-2 block with diagonal xy and off-diagonal xc. Define

    rho4=omega tensor omega
         -xc (|1000><0100|+|0100><1000|).

This removes that off-diagonal entry. It is positive and normalized; the two
eigenvalues xy +/- xc are replaced by xy,xy. Strict concavity proves that
its entropy is strictly larger than 2S(omega), with all other eigenvalues
unchanged.

The exact four-call drift matrix supplies the bulk correction
-2xc ab(I-S1S1^*). For the established c=-b/128 and
kappa=ab^2/128, this is 2x kappa(I-S1S1^*). The unmodified two pairs have
bulk drift -2kappa I. Hence

    D_rho4=-2kappa I+2x kappa(I-S1S1^*)
          <=-2kappa(1-x)I.

It is genuinely non-scalar (the top colors have different drifts), yet has a
strict negative operator bound. The general Lyapunov extension therefore
supplies actual infinite-bath control and arbitrary-reference codes. The
new receiving use is the loss of scalar closure together with a sufficient
operator replacement; the result is not inferred from entropy alone.

## 6. The local entropy-Hessian interface passes, with scope qualifications

For fixed charge-preserving trace-zero Hermitian X,Y, sigma commutes with
both, since it is scalar in each charge sector. Assume Tr(QX)=0 and set
rho_b=sigma+bX+b^2Y. Finite-dimensional Taylor expansion gives

    S(rho_b)=3k/2+b^2[m-H(X)]+O_k(b^3),
    m=Tr(QY), H(X)=Tr(sigma^-1 X^2)/(2 ln2).

The exact finite-prefix bulk polynomial gives

    D_rho_b=b^2[T_k(X)+2m I]+O_k(b^3)

in operator norm, where T_k(X) is contraction of the b-coefficient with X.
Thus H(X)<m<-lambda_max(T_k(X))/2 is sufficient: positivity follows for
small fixed b from sigma>0, the entropy excess and negative bulk drift both
survive, and the preceding Lyapunov/coding operation applies. One can realize
any desired m by Y=(4m/k)sigma(Q-k/2), because Var_sigma(Q)=k/4.

The expression

    sup_X [-lambda_max(T_k(X))/2-H(X)]/k

is consequently an attainable leading-coefficient supremum by strict-margin
approximation. It is not an equality formula for the full channel capacity,
nor for every finite-block input without the perturbative hypotheses. The
full prefix operator, not its normalized trace, enters lambda_max. All
remainders and positivity thresholds depend on fixed k and fixed X,Y; no
uniform large-k statement follows.

## Repairs and limitations to retain

The producer's revised source was re-read after it incorporated the bounded
charge-transfer proof, finite-R/B entropy proof, all-normal quantifier and
fixed-block-length wording repair. Those changes are accepted as written.
Its additional logarithmic-length corollary also passes: for
nu=2 ln(8/3), beta_k=exp(-nu k)/(64 k^4 ln2), and
k(beta)<=c ln(1/beta) with c<1/nu, one has

    beta/beta_k <=64 c^4 ln2 [ln(1/beta)]^4 beta^(1-nu c) ->0.

The main upper therefore yields O(beta^4 [ln(1/beta)]^5) uniformly over
that specified growing-block range. This excludes an excess of order
beta^p with p<4 within this restricted input class, but permits logarithmic
enhancements, faster block growth and the other explicitly excluded input
operations. It is justified by the actual quantitative threshold, not by
exchanging limits in an unspecified fixed-k big-O statement.

One wording repair was requested: 'fixed number of blocks' must say 'fixed
block length'. The number of blocks n is unrestricted. The all-normal upper
quantifier is a justified strengthening using bounded transfer and finite R,B;
it is not inherited from the lower-code convergence statement.

Removing charge preservation invalidates the bulk evenness lemma: the
one-site state rho_c+ig|0><1|-ig|1><0| has exact drift
aP0/2-alpha beta g(S1+S1^*), with a nonzero linear-beta expectation on a
superposition of adjacent positive-depth bath coordinates. That example does
not supply a rate gain and does not contradict the old iid theorem.

No general-capacity upper bound, feedback conclusion, terminal bath return,
efficient compiler, useful blocklength or historical first has been checked
or claimed. Fixed k and k growing with beta are different operations. Numerical
prefix averages or finite replay counts do not certify any asymptotic claim.

Review resource cost is analytic source review; total inference/discovery cost
is unmeasured. No numerical simulation, paid resource or outreach was used.

## Final assembled-source integration gate

The complete new main source `FIXED_BLOCK_ORDER.tex` was subsequently read in
full. The inherited appendix was not subjected to another old audit. The
review targeted Theorem `operatorcode`, the odd-length padded lower corollary,
the polynomial/Hessian proposition, logarithmic-window scope and all-normal
upper quantifier. Their integration is accepted.

The main source preserves the exact positive-effect exponential identity,
the finite boundary remainder, maximum-probability spectral types, the
correct `(rank rho + 16) ln(m+1)` cutoff exponent, and the initial-tail
comparison outside type domination. The actual-state entropy conclusion uses
the normalized density `g=4^(-L)/4`; its trace is one because the level-ell
degeneracy is `2^(ell+1)`. Finite mean therefore bounds even non-radial
bath entropy. These details close the operator drift-to-code implication.

For the odd-k lower construction, initial depth>=k implies depth at least two
before every constituent pair and at least one before the optional last
critical site, under every allowed history. Therefore all constituent bulk
identities apply on that compression; their scalar constants compose through
the trace-preserving duals. The resulting bulk drift is exactly
`-floor(k/2) kappa_2 I`, so the general operator criterion proves the claimed
coherent-information lower limit and hence the sharp fixed-k order.

The finite-prefix polynomial argument retains the first k bath colors and
the untouched tail. Equal input charge and common output fix the final prefix
length, so the tail factors out even when histories pop different numbers
of initial symbols. The entropy Hessian and the operator remainder in the
local proposition are consequently uniform over all deep bath vectors for
fixed k,X,Y. The actual upper and lower quantifiers are distinguished.

Two terminology clarifications were requested without changing any theorem:
`input-independent code` must be `initializer-independent code`; and the
functional A_k in equation (48) is per block, so attainable per-call leading
coefficients are A_k/k. The first repair was verified in the source during
this gate. No load-bearing mathematical repair was required.

The reviewed assembled source retains that the explicit k=4 upper threshold
is far below 1/512, that the logarithmic-window upper is an input-class
information result, and that the local variational functional is not a full
capacity formula. No new simulation or unrequested broad audit was performed.
