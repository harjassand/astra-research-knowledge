# Prefix-dependent affine frames, rather than one global flag

26 October 2026. Owned continuation of
AFFINE_CHECKPOINT_BOOTSTRAP_FIRST_CONSTRUCTION.md. The mechanism was chosen
after the global-checkpoint proof and its source comparison. Root separately
supplied the simple common-control separation in Section 6 after the local
mechanism was chosen. No source, target, simulator, fixture, or observation
is added. The first construction's bytes and original results are preserved.

## 1. The next remaining cost

An affine fibre does not have to be parallel to all OTHER fibres. Requiring
one global translation-period space can therefore overprice even an entirely
affine conditional preparation problem. Previously fixed prefix values may
select a different native affine frame, which can itself be computed from
the acquired programs. A useful representation can retain that conditional
frame CONSTRUCTOR, instead of expanding a full tree of all contexts.

Use exactly the same native F_2^n, unknown quadratic permutation Q, chosen-pair
lexicographic comparator, quadratic promise and actual fair-bit interface as
the first checkpoint construction. Coordinates are acquired in their actual
rank significance order. No block/control labels, context distribution,
hidden basis, conditional frame, or target coefficients are supplied. The
ANFs used below must first be acquired by the same comparison bootstrap.

The source class and finite native-control contract remain supplied, with
all actual source latency/preparation additional to the logical comparison
count. Conditional-affine structure is not assumed by the algorithm. Its
appearance changes the algorithm's computed preparation procedure and cost.

## 2. Acquiring an exact frame inside an already certified fibre

Suppose the current prefix h_s=(Q_1,...,Q_s) has a certified full fibre

    A=x+U=h_s^-1(h_s(x)),    dim U=n-s.                  (1)

The certificate is an inductively justified mathematical implication under
the correct acquired-prefix and permutation promises, not an independent
recognition certificate for arbitrary source orders. Initially s=0, U=V
and A=V for any native x.

For a later acquired prefix length j>s, restrict the NEW coordinate block
to this known native carrier. Its period space is

    P(A,j)={v in U: Q_i(z+v)=Q_i(z)
                   for every z in A, s<i<=j}.           (2)

This is paid finite linear algebra on acquired quadratic programs. More
explicitly, compute

    L={v in U: B_i(w,v)=0 for all w in U, s<i<=j},
    ell_x(v)=(Q_i(x+v)+Q_i(x))_(s<i<=j),  v in L,
    P(A,j)=ker ell_x.                                   (3)

Choose the actual acquired basis of U. Every restricted polar matrix has
entries B_i(u_a,u_b). On L the displayed response is a linear map, and
the quadratic expansion proves (2)--(3) exactly. No derivative, global
coordinate oracle, hidden-input chart, or fibre enumeration is used.

The period space is independent of the origin chosen in A. If x'=x+w_0
with w_0 in U, its response on L changes by B_i(w_0,v)=0. Thus both the
test and its successful subspace depend on the actual affine carrier A,
which is determined by the fixed earlier prefix, rather than on an
unobserved choice of its witness.

Each coset z+P(A,j) in A lies in a j-prefix fibre. Every such fibre has
exactly 2^(n-j) points because Q is a permutation, so

    dim P(A,j)<=n-j.                                    (4)

If equality holds, it follows that EVERY j-prefix fibre inside A is one
whole P(A,j) coset. In particular, the new certified carrier for x is

    h_j^-1(h_j(x))=x+P(A,j).                            (5)

Every extension of the fixed s-prefix occurs inside A. Equation (5) is
therefore valid for all its extension labels, not just the currently
requested witness. The argument uses the known balanced-prefix sizes;
having a large period space alone would not suffice without that promise.

## 3. The conditional checkpoint chain and its exact sampler

For a complete native witness x, define its GREEDY chain inductively.
Start at (s_0,A_0)=(0,V). Given A_l=x+U_l at prefix s_l, let

    s_(l+1)=the smallest j>s_l for which
                    dim P(A_l,j)=n-j,
    A_(l+1)=x+P(A_l,s_(l+1)).                           (6)

There is always such a j by j=n: injectivity of Q on A_l forces the period
space of the full output to be zero. The chain ends at n. Define the
uniform structural parameter

    g_cond(Q)=max_(x in V) max_l(s_(l+1)-s_l).           (7)

The maximum over all native contexts is NOT claimed cheaply computed from
finite visited contexts. Every LOCAL matrix/test used by the algorithm is
computed from acquired code, but the worst-context maximum in (7) is an
analysis parameter. An observed small gap is not a uniform runtime promise
for unseen future targets. The algorithm needs no supplied value of (7).

All literal scans of acquired models are bounded. If a tested dimension
exceeds n-j, return UNKNOWN. During acquisition at t<n, absence of a new
equality by t is legitimate: keep the last certified carrier and use the
rejection sampler below. A COMPLETE inverse/deployment scan tests at most
the remaining indices through n; if an erroneous acquired model has no
equality even there, return UNKNOWN. Only on the true promised Q does
injectivity justify existence of the next checkpoint. This explicit
failure rule is part of the unconditional finite cap used in (13).

At learned stage t<n and requested native x, compute the chain only as far
as the currently acquired coordinates allow: scan j<=t, advance at each
successful equality, and stop with its last certified (s,A=x+U). This is
exactly the truncation of (6), because the earlier tests never depend on
unacquired later coordinates. Draw Z=x+Uniform(U), filter the learned
coordinates s+1,...,t to match x, and repeat on failure.

The proposal is uniform on the whole earlier fibre. Therefore the EXACT
acceptance probability is

    2^(n-t)/2^(n-s)=2^(-(t-s)),                          (8)

and every accepted Z is uniform on the whole current prefix fibre. Since
the next greedy checkpoint is beyond t,

    t-s<=g_cond(Q)-1.                                   (9)

Each proposal consumes dim U=n-s fresh bits, plus paid basis multiplication
and acquired code evaluation. All rejected bits/evaluations are retained
as costs. For one weak-label request, the same computed carrier can serve
all of its fresh median/short-collection preparations. It is not recomputed
for every proposal, but its construction is still paid for that request.

Every GLOBAL checkpoint of the first construction remains a candidate in
every containing conditional carrier. Its global period space lies in U
and already has dimension n-j, so (4) forces equality. The greedy chain
cannot skip such a candidate. Hence

    g_cond(Q)<=g(Q).                                    (10)

No comparison query or hidden-feature observation is added to obtain this
improvement. The old known-witness input is used more effectively.

## 4. Full acquisition confidence and actual computation

Use the original quadratic median/cube/interpolation procedure unchanged,
except for the exact sampler (8). The proof does not supply the next bit
as a free label: K=511 fresh same-prefix samples yield an averaged weak
threshold label; seven marginally uniform cube vertices give one corrected
trial with error below 1/4; fresh independent trials and majority yield
exp(-R/8) error per requested value. Interpolation needs D_n=1+n+binom(n,2)
values per coordinate. Exact short fibres are collected with their known
size, not assumed to be enumerated by a latent program.

Use all the literal caps and error allocations of the first construction:
L=7nD_nR weak-label requests, J_N=N ceil_log2(NL/eta_2) short-fibre accepted
draws, M=L max(511,J_64) conditional preparation calls, and
S=ceil_log2(M/eta_1). With the current carrier (s,A), cap each preparation
at 2^(t-s)S proposals and return UNKNOWN on failure. The true-prefix failure
bound is still at most eta_1/M by (8). Short-collection failure remains at
most eta_2; interpolation failure at most delta_a.

Coupling to the ideal uncapped TRUE-prefix run, rather than conditioning
on its successful tapes, gives the simultaneous guarantee

    Pr[correct completion and all caps respected]
        >=1-delta_a-eta_1-eta_2.                         (11)

Per weak-label request, a straightforward dense scan of restricted polars,
response maps and kernels costs at most O(n^5) bit operations. Start with
the n acquired n-by-n polar matrices. At each of at most n frame changes,
pull back at most n still relevant matrices by the current basis using
ordinary O(n^3) binary matrix multiplication per matrix. Response rows
are computed by explicit ANF evaluations on at most n basis vectors.
At each of at most n tested j, eliminate a stack with at most n^2 rows
and n columns, in O(n^4) bit operations. The total of these costs is
O(n^5); no assumption of free reuse of a hidden chart enters the bound.
More precise implementation may improve it; no timing is claimed.

Thus an explicit conservative successful-run work bound is

    poly(n) + O(L n^5 + M 2^(g_cond(Q)-1) S n^3),        (12)

plus actual source comparator costs. At most 32,200 nD_nR exact comparisons
are made, as before. Offset bits and proposal bits have the bound

    3n*nD_nR + M 2^(g_cond(Q)-1) S n.

The full ANFs, current restricted matrices/carrier, at most 511 median
points or J_64 short-collection requests, and interpolation state occupy
polynomial space. No context tree with 2^n leaves is stored. All-branch
finite work remains bounded by poly(n,log(1/epsilon))2^n when the internal
allowance is epsilon; erroneous prefixes can cause a much larger computed
gap than the true source's g_cond, but cannot cause an uncapped loop.

Root's standard confidence-amplification consequence applies unchanged:
run with internal epsilon=delta 2^(-n). Its logarithm is only
O(n+log(1/delta)). The correct capped event costs poly*2^g_cond, while its
complement has probability at most epsilon and work at most poly*2^n.
Consequently the expected known-code/bit work, plus charged logical
comparisons, is

    poly(n,n+log(1/delta)) (2^g_cond(Q)+delta),           (13)

with correctness at least 1-epsilon>=1-delta. This is bounded-error
expected work, not Las Vegas correctness or all-branch fixed-parameter
work. Unbounded physical source latency cannot be hidden in the polynomial.
An external smaller budget can still produce UNKNOWN on correct tapes.
The complete original argument is ROOT_CHECKPOINT_EXPECTED_RUNTIME_WRAPPER.md.

## 5. Closed inverse after expiry, without enumerating all contexts

A witness-dependent frame does not force deployment to retain a live source
or to receive a witness for the requested output y. A complete acquired Q
can invert y by following its prefix branch, with every step constructed
from the acquired ANFs.

Start at any x and A=V, s=0. Compute the first later j whose restricted
period test is an equality. Write

    U=T direct-sum P(A,j),    dim T=j-s.

Enumerate the 2^(j-s) vectors x+T a. Exactly one matches the next output
block y_(s+1:j): all earlier bits are preserved, and (5) says those vectors
represent every possible extension fibre once. Change x to that vector,
set A=x+P(A,j), and continue with s=j. At s=n the fibre has one point, so
the result is Q^-1(y).

The chosen later j and subspace P depend only on the parent carrier, not
its selected origin. Inductively, this computed chain is exactly the chain
(6) that would have been obtained from the as-yet-unknown actual inverse
witness Q^-1(y). Its enumeration width is therefore at most g_cond(Q).
The inverse uses at most n 2^g_cond trials, polynomial paid matrix/code
work per block/trial, polynomial storage, and ZERO expired-source calls.

This is a compact CONDITIONAL frame constructor. It does not store every
branch. Appending n-t fresh suffix bits to an arbitrary requested prefix
and applying the inverse gives an exact uniform prefix sampler using
exactly n-t fair bits, on the correct acquired branch. Conversely, while
acquiring Q the native witness sampler (8) avoids paying that full inverse.
Missing/multiple representatives in an erroneous learned model can return
UNKNOWN; unique matches do not remove the original error allowance.

## 6. A supplied source promise is not a supplied context or frame

The meaningful strictness of (10) can be seen without new observations.
Root supplied the following symbolic all-size consequence after the local
mechanism was chosen. Let n=2m+1 and let the actual significance order be

    Q(a,b,c)=(a, b_1+a c_1,...,b_m+a c_m, c_1,...,c_m).

This is a quadratic permutation: given its output and a, recover c then
b. After fixing a, EVERY remaining coordinate is affine on the current
carrier, and each must be a nonconstant linear response there by prefix
balance. Thus (6) advances one bit at every step and g_cond(Q)=1.

Globally, immediately after a is acquired, the new coordinate b_i+a c_i
forces BOTH its global period components delta b_i and delta c_i to be
zero. At the prefix containing a and the first k such coordinates, the
global period dimension is 2m-2k, strictly smaller than n-(k+1)=2m-k for
k>=1. After all m such coordinates the global period is zero; the later
c_i do not restore any period. There is no subsequent global checkpoint
until n, so g(Q)=2m. Unknown invertible affine INPUT hiding preserves both
arguments and is not given to the learner.

This separates uniform versus conditional affine flags, and two proved
cost parameters, at all sizes. It is not a lower bound on the strongest
same-oracle retainer. In fact a conventional conditional-affine decoder
with these very learned coefficients can tie the construction. Reordering
the hidden output bits to move c before b would make a different source
order; no such semantic reordering is supplied during acquisition.

## 7. Incumbent and completeness boundaries

The primary Boolean linear-structure algebra is established:
[Carlet's monograph, Definition 25 and Propositions 28--29, pp120--122](https://www.math.univ-paris13.fr/~carlet/book-fcts-Bool-vect-crypt-codes.pdf)
defines constant-derivative subspaces and relates them to affine changes
of variables. Restrictions to acquired affine carriers use that same
algebra. No novelty is claimed for their kernel calculations.

The preserved N780 governing COMPARISON_DECODER_THEOREM.txt gives the
stronger comparison bound D+6 binom(n,2) on a complete GLOBAL scalar
triangular flag. Its class is precisely g=1 in the quadratic case: the
nested global period spaces give a native complement basis in which each
new output bit is its own input bit plus a polynomial in earlier bits,
and conversely that form makes every prefix a global affine checkpoint.
It remains the incumbent wherever applicable. The conditional construction
is not allowed free labels, source programs, context decisions, or the
frame that those ordinary decoders would have to acquire too.

Known global/conditional triangular maps, adaptive parity decision trees,
and model-based Gaussian elimination are strong ancestry/comparator
directions. This note proves the full legal acquisition/deployment
composition and its conditional cost parameter, not priority over every
such method. An equally informed retaining implementation may make all
the same native matrix, filtering, median/correction and inverse choices.

There is no generic promise of small g_cond, no cheap recognition of its
worst-context bound, no arbitrary-polynomial/physical-interface extension,
and no new historical confidence for the separate expired six sources.
The earlier scalar savings, derivative slowdowns, and defeated current-
query advantage remain intact. What changes here is an actual preparation
capability: acquired prefix information can select the affine frame of
later experiments, without a supplied global latent representation or
an exponentially expanded context catalogue.
