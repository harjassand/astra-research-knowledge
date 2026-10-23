# Exact four-call representation and the non-scalar bulk obstruction

Author role: bounded independent representation contribution to Pro 1 Cycle5.
Source: unchanged Cycle4 model and exact Fock representation. This contribution
does not re-audit the previous coding theorem or claim an improved rate.

## 1. A finite matrix that is exact on the infinite bulk

Let `N(x)` be the number of nonzero symbols in the input word `x` of length n.
The actual one-call permutation sends `(a,w)` with a=1 or 2 to `(0,aw)`;
`(0,jw)` to `(j,w)`; and `(0,empty,seed)` to `(0,empty,1-seed)`.
Every call of V is a coherent sum of this move, amplitude alpha, and a stay,
amplitude i beta. The program `history` implements precisely these infinite-
bath rules, including the vacuum seed exchange. It is not a finite reflecting
boundary or stationary cutoff.

For initial depth at least n, split the bath word into its first n letters u
and an untouched tail v. During n calls no path can use the vacuum exchange:
a path can reach the vacuum only after its last call. Thus every path depends
on the n-letter prefix alone and acts as identity on the seed and untouched
tail. Write

`T_{y,x}(u -> w) = sum_h i^{r(h)} alpha^{n-r(h)} beta^{r(h)}`,

where `h` ranges over histories with the indicated output y and final prefix w,
and r is its number of stays. Define the input/prefix matrix

`D_{(x,u),(z,v)} = sum_{y,w} (|w|-n) conjugate(T_{y,x}(u->w)) T_{y,z}(v->w)`.

For a charge-preserving input density rho, the bulk bath drift is the input
partial expectation of D: its `(u,v)` entry is
`sum_{x,z} rho_{z,x} D_{(x,u),(z,v)}`. Only `N(x)=N(z)` sectors are needed.
This matrix is exact on every initial depth >= n, tensor identity on the seed
and untouched tail. Initial prefixes at different depths cannot couple after
the charge-preserving input expectation, as proved in Section 4.

The exact finite matrices are exported for n=4 in
`four_call_representation.json`. Input words and prefix words are supplied in
lexicographic order. A coefficient entry `[i,u,j,v,c]` means the corresponding
matrix entry is c in the polynomial coefficient D_k of

`D(b) = D_0 + b D_1 + b^2 D_2 + b^3 D_3 + b^4 D_4`, `b=beta^2`.

No numerical rounding is used in these coefficients. The complete unitarity
Gram matrix is independently assembled from the same histories and reduces
exactly to identity after alpha^2=1-b. This is a finite algebra check; the
infinite-bulk interpretation follows from untouched-tail factorization above.

## 2. Why no first-order beta bulk term survives

For a history away from the root, each move toggles the zero/nonzero status
of its port. Its bath depth change is N(input)-N(output). If a history has r
stays, the parity of its number of moves is n-r and is also the parity of this
net depth change. Two histories contributing to the same output and the same
charge-preserving input sector therefore have stay counts of the same parity.
Their product has even total beta degree. Its phase `i^(r2-r1)` is real.

This proves for every fixed n that the charge-compressed bulk drift is a
real matrix polynomial in b=beta^2. It applies to complex input coherences as
well; their expectations are taken against this Hermitian real matrix. Root
terms can have odd beta powers, because a root move need not change depth.
They remain confined to the finite layer subspace L<n and must not be dropped
from a global Lyapunov inequality.

At b=0 all calls move. For a fixed charge q, every history has depth change
2q-n, independent of input colors and initial prefix. Unitarity then gives
`D_0=(2N-n) tensor I`. For a coordinate-diagonal input word, the exact bulk
expected drift is `(1-b)(2N(input)-n)`, since each port moves with probability
1-b and its signed depth increment is fixed by its input zero/nonzero value.
The code checks this identity for every four-call input and prefix.

## 3. Charge preservation does not imply scalar depth closure

For two calls, the bulk drift matrix element between `10` and `01` is

`D_{10,01}=a b (I-P_1)`, where `P_1=S_1 S_1*`, a=1-b.

Here P_1 projects onto words with leading color 1. To derive it, retain the
common outputs in the exact two-call amplitude table. Output `00` contributes
`ab I` at net depth change +1. Output `11` contributes `-ab P_1` at change -1.
The other common outputs have net change zero and contribute no drift. This
also shows directly why summing equally over both colors restores a scalar:
`sum_j(I-P_j)=I` away from the root.

For the requested four-call space take

`rho = rho_c^tensor4 + epsilon (|1000><0100| + |0100><1000|)`,
`rho_c=diag(1/2,1/4,1/4)`, `0<epsilon<=1/32`.

Both affected diagonal entries are 1/32, so rho is a positive trace-one
charge-preserving density. The final two fixed zero symbols in the coherent
matrix element add only a scalar drift times its zero total trace, as the
bath remains away from root during those two calls. Hence the exact bulk drift
is `2 epsilon ab (I-P_1)`. It is zero on a top-color-1 word and
`2 epsilon ab` on a top-color-2 word at the very same depth. Thus Phi*L is not
a scalar function of L. The code verifies the entire prefix matrix, not merely
two chosen diagonal expectations.

This example disproves a general scalar-depth reduction but does not obstruct
an operator Lyapunov argument or the restricted color-symmetric pair family.

## 4. The exact operator replacement for scalar closure

Define total color charge `N=sum_j 1_{port_j != 0}`. The actual U, including
R, preserves `N+L`; so does V and the ordered W_n. If `[rho,N]=0`, choose an
eigenbasis for rho within its charge-q eigenspaces. For an eigenvector lambda
of charge q and output word y, the bath Kraus operator K_(y,lambda) is
homogeneous in depth of degree `Delta=q-N(y)`. This is exact at the root too:
R has degree zero, and its port input and output have color number zero.

For each Delta in [-n,n], set

`A_Delta = sum_(y,lambda:q-N(y)=Delta) K* K`.

Every A_Delta is positive, commutes with L, and `sum_Delta A_Delta=I`. Therefore

`Phi* L - L = sum_Delta Delta A_Delta =: D_rho`,

and, as a positive quadratic-form identity on finite-support vectors,

`Phi* exp(tL) = [sum_Delta exp(t Delta) A_Delta] exp(tL)`.

The same identity extends to the positive observable by monotone truncation.
The bracket is a positive block-diagonal bath operator, not necessarily a
scalar function of depth. The complete D_rho is bounded in norm by n.

For 0<=t<=1/n the elementary Taylor bound gives

`sum exp(t Delta) A_Delta <= I+t D_rho+(e n^2/2)t^2 I`.

Thus a uniform bulk inequality `D_rho <= -kappa I` on `L>=n` yields a genuine
operator exponential contraction there for sufficiently small fixed t. The
remaining finite-layer part `L<n` is bounded by a finite constant times its
coordinate projection, since n calls can increase depth by at most n. All
these observables commute with L, so the bulk and root inequalities combine
without cross terms. This is the honest replacement for scalar closure; it
requires a uniform operator bound, not just the trace under a comparison bath.
It can feed the inherited compression interface if that uniform bound is
established for a candidate with sufficient input entropy.

## 5. Four-call susceptibility and its precise limitation

Let `sigma=rho_c^tensor4`. Define the uniformly averaged leading correlation
matrix

`F_4=(1/16)Tr_prefix(D_1)+(2N-4)I`.

The diagonal correction removes the ordinary factor a=1-b from the drift.
`four_call_susceptibility.json` contains the 216 nonzero rational entries of
F_4, the exact sigma diagonal and the word ordering. Exactly,

`Tr(sigma F_4)=0`, `Tr(sigma F_4^2)=561/512`.

Since F_4 commutes with N, it commutes with sigma. Thus an input variation
`rho(t)=sigma(I+t X)`, with X commuting with N and Tr sigma X=0, has the
ordinary relative-entropy Hessian `Tr sigma X^2/(2 ln 2)` in bits. F_4 gives
the Riesz representative of the averaged leading drift in that metric.
It is an averaged susceptibility, not a uniform bath bound or a capacity
certificate. The distinction is material because of Section 3.

A separate exact finite-history replay yields the following diagnostics:

| n | Tr sigma F_n^2 | Per call |
|---:|---:|---:|
| 2 | 1/8 | 1/16 |
| 3 | 33/64 | 11/64 |
| 4 | 561/512 | 561/2048 |
| 5 | 7937/4096 | 7937/20480 |
| 6 | 97809/32768 | 32603/65536 |

These computations do not prove a growth law in n. They do show that replacing
the four-call perturbation by two independent copies of an averaged pair
susceptibility omits temporal terms. The scientific receiving use is to inform
the root's small-angle/longer-block analysis, while preserving the uniform
operator obligation.

## 6. Observed resources and source scope

The full exact four-call prefix-matrix replay took 0.1203 seconds and peaked at
22,144 KiB in the observed Python 3.12 environment. The n=6 averaged leading
coefficient replay took 2.1659 seconds and peaked at 15,108 KiB. Complete
machine-recorded numbers are in the accompanying JSONs. These are algebra
replay costs, not discovery/model costs, long-time bath simulation, or code
compilation costs; those totals were not measured here.

No bath cutoff, reflecting stationarity, physical reset, hardware spending,
external communication or historical-priority claim is used. The original
Cycle4 capacity theorem is preserved unchanged.

## 7. Independent check of the owner's non-scalar stable witness

The owner subsequently proposed

`rho4 = omega tensor omega - x c (|1000><0100|+h.c.)`,

where omega is the unchanged Cycle4 pair state, with its negative c. The span
of `1000,0100` is a reducing two-dimensional block for omega tensor omega:
its diagonal is `(xy,xy)`, its offdiagonal is xc, and there are no matrix
entries connecting it to any other word. Deleting that offdiagonal therefore
preserves positivity and trace. It strictly increases entropy by

`S(rho4)-2 S(omega) = 2xy [1-h2((1+c/y)/2)] > 0`.

This follows by normalizing the block of mass 2xy; its two initial probabilities
are `(1+c/y)/2,(1-c/y)/2`, while after pinching they are equal. All parameters
are positive as required for 0<beta<1, and c is nonzero.

The exact two-pair bulk drift is -2 kappa I on L>=4: before each pair the bath
remains in the pair's bulk throughout the other pair's two calls. Section 3's
cross matrix element adds `-2xc ab(I-P_1)=2x kappa(I-P_1)`. Consequently

`D_rho4 = -2 kappa I + 2x kappa(I-P_1) <= -2kappa(1-x) I < 0`.

This is non-scalar and uniformly inward. Here x=q^2<1/4. It provides a concrete
receiving use for the operator exponential-moment interface rather than a
counterexample alone. The coded implication is owned by the root and requires
that interface plus the inherited arbitrary-reference compression operation.
This construction improves a coefficient while remaining quartic in beta;
its structural role is removing the scalar-closure requirement.

`four_call_nonscalar_witness.py` independently contracts the complete exported
four-call matrix with the polynomial candidate rho4, over exact Fractions.
It verifies the displayed drift as a polynomial identity in b for all b, the
reducing-block structure, and the exact vanishing of all offdiagonal bath
prefix entries. Its observed replay was 0.1049 seconds with 13,724 KiB peak RSS.
This finite exact check supports, but does not replace, the analytic argument.
