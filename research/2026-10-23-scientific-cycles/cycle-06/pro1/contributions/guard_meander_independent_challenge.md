# Independent challenge of the all-length guard/meander mechanism

This is a bounded Cycle6 internal proof check. The object is the bulk
charge-pinched second-order coefficient and its finite-prefix contraction,
not a finite reflecting bath, a numerical pattern census, or an externally
certified priority claim. The reviewer read the written toggling and endpoint
decomposition in `temporal_operator_dual.md` and independently reconstructed
the guard/meander token argument supplied by the owner. I then read the
complete helper source `temporal_constructive_structure.md`; its exact
word identities, sector projections and counting agree with this independent
reconstruction. No load-bearing gap was identified.

## 1. The exact operator block to be retained

Write `P_r=U_r...U_1` and `C_j=P_(j-1)^* U_j P_(j-1)`. On a deep core,
each `C_j` flips only the charge bit at site j. Thus, for i<j, the
restriction of the off-diagonal endpoint term from input bits
`(q_i,q_j)=(0,1)` to `(1,0)` is

    C_j^- C_i^+ - C_i^+ C_j^-.

No other endpoint pair has this input/output bit support. Consequently its
weighted Hilbert-Schmidt square is a nonnegative orthogonal summand of
`Tr(sigma H_tau^2)`, even after an arbitrary prefix-state contraction.

Take a guard at site i-1, require `q_(i-1)=1`, and write `g=U_(i-1)`,
`P=P_(i-2)`, `B=U_(j-1)...U_(i+1)`. Direct multiplication, using only
unitarity and the definition of the toggles, gives

    C_j C_i = P^* g U_i B^* U_j B g P,
    C_i C_j = P^* g B^* U_j B U_i g P.

These equalities avoid an ambiguous path diagram and fix the order of
both products. Restricted to the selected endpoint bits, the full products
equal the corresponding charge-selected products displayed above.

## 2. Why every balanced internal excursion cancels

For a binary Dyck word, regard a colored input as a push and a zero input
as a pop. Every pop consumes an input color pushed inside that word. The
ordered all-move device word therefore takes that binary input sector to
its bit complement by a permutation of its input color wires, tensor the
identity on the entire incoming bath. This is an exact linear isometry
between the two fixed-bit sectors, and it is independent of all bath
coordinates. The statement holds even for a bath entangled with other
registers, since it is an operator identity.

Every nonnegative meander has a unique decomposition

    D_0 1 D_1 1 ... 1 D_h,

where each `D_l` is a Dyck word, and the h unmatched upward steps carry
colors `a_1,...,a_h` in their temporal order. The Dyck isometries act only
on their own port coordinates and have identity bath action. In each
displayed `B^* U_j B` they commute past `U_j`, are paired with their
adjoints, and cancel. They also commute past `U_i` and the guard, which
act on other port coordinates. Thus one may remove all `D_l` when
comparing the two ordered toggles. This reduction is valid for every
length h and every Dyck decomposition, not just for a bounded list of
patterns.

## 3. The two remaining token computations

The remaining local input has the form

    [g, 0, a_1,...,a_h,z],

where the first token names the guard color and z is the color at j. Let
the incoming bath be any stack w.

For `g U_i B^* U_j B g` (rightmost factor acts first): the first guard
pushes g; B pushes `a_1,...,a_h`; `U_j` pushes z; `B^*` pops z and
then the later a-colors into the reversed middle calls; `U_i` pops a_1;
the final guard pops g. The final input-color array is

    [g,a_1,a_2,...,a_h,z,0],

and the final bath is exactly w.

For `g B^* U_j B U_i g`: the guard first pushes g, `U_i` immediately
pops it into slot i, and B then pushes the a-colors. After `U_j` and
`B^*`, the final guard pops a_1. The final array is

    [a_1,g,a_2,...,a_h,z,0],

with the same exact final bath w. For h=0, use a_1=z: the outputs are
`[g,z,0]` and `[z,g,0]` respectively. These two computations never
consume an original color from w.

After restoring the removed Dyck color relabellings, the difference is
an input-only isometry times `I-SWAP`, tensor `I_bath`, where SWAP
interchanges the guard color and the first unmatched color (or z if h=0).
The earlier prefix P acts only on earlier ports and the bath, so it
commutes with this input-only block and cancels against P*. An arbitrary
earlier input/bath entanglement therefore cannot destroy the identity.
There is no assumption that prefix colors are independent or that the
prefix density is diagonal, maximally mixed, separable, or full rank.

The coefficient itself is bulk. One may perform the toggling algebra on
an initial depth at least 4k so that the displayed expanded words avoid
the root, then use the established finite-prefix identity for the k-call
bulk coefficient. This does not discard the true root from the actual
device or coding theorem. It is also sufficient for coding to enlarge a
finite boundary region if the available representation is stated only
with that buffer.

This distinction is necessary: the raw local-word identity is whole-bath,
whereas its identification with individually charge-raising/lowering
toggles is bulk only. For three slots [g,0,z] with the first slot the
guard and an initially vacuum bath, C_i=U_g U_i U_g preserves total
input charge: its final U_g uses the vacuum exchange R, leaving guard
zero and slot i colored. Hence the global +1-charge component C_i^+
vanishes on this input even though the raw word C_j C_i still has the
token action above. The full-bath identity must therefore not be claimed
for the raising/lowering expression itself without the bulk premise.

## 4. Normalized weight, reverse orientation, and all-length counting

For two independent uniform binary colors,

    tr_norm((I-SWAP)^*(I-SWAP))
      = 2 - 2 tr_norm(SWAP) = 1.

All additional color wires are spectators up to permutations, so this
normalized square remains exactly one. Under sigma, every charge bit is
independent Bernoulli(1/2). For endpoint separation r+1, the probability
of the guard and endpoint pattern is 1/8, and the probability that the r
internal bits are a nonnegative meander is

    p_r = 2^(-r) binom(r,floor(r/2)).

The opposite endpoint orientation contributes the identical norm because
the full endpoint term is Hermitian and sigma is scalar on each charge
sector. This yields a factor two, not a new probabilistic assumption.
There are `k-r-2` choices of i>=2 with that separation. Orthogonality
of the endpoint supports and the fixed-charge input blocks therefore gives
for EVERY auxiliary prefix density tau

    Tr(sigma H_tau^2)
      >= (1/4) sum_(r=0)^(k-3) (k-r-2) p_r.

This is the required all-prefix lower. The minimization defining v_k
cannot remove these bath-independent blocks.

Here is an elementary bound with no asymptotic approximation. For m>=1,
`a_m=binom(2m,m)/4^m>=1/(2sqrt(m))`, by induction from a_1=1/2 and
`a_(m+1)/a_m=(2m+1)/(2m+2)>=sqrt(m/(m+1))`. The odd recursion gives
`p_(2m+1)>=1/(2sqrt(m+1))`, including m=0 directly. Therefore

    p_r >= 1/sqrt(2(r+1))

for every r>=0. Since r<=k-3,

    v_k >= (k-1)sqrt(k-2)/(8sqrt(2))
        >= 3 k^(3/2)/64
        >= k^(3/2)/32,       k>=4.

The middle inequality uses k-1>=3k/4 and k-2>=k/2. The proposed 1/32
constant is conservative. No finite-check count enters the bound.

## 5. Scope of acceptance and omission failure

The reviewed mechanism supplies growth of the operator susceptibility, and
the separate uniform-transfer review supplies exact input positivity,
nonlinear remainder, inward drift, bath-overflow control through the
inherited coding theorem, and the resulting full-diamond code. A growing
prefix-average norm alone would not have supplied those consequences.

The guard/nonnegative-meander premises are load-bearing. Positive net
height alone does not imply bath-independent toggles: the supplied short
counterexample with charge word 011 and endpoints 0,2 has one order
transporting an original bath color and the other an input color. This
example also omits the guard. There is a direct guard-present counterexample:
the charge word 100111, with endpoints i=1,j=5 in zero-based indexing,
has middle 011 of positive final height but negative first prefix. Give
its colored slots distinct formal labels [g,0,0,a,b,z] and the initial
bath [w_1,w_2,...]. The first ordered toggle has output
[a,g,0,b,z,0] and the original bath. The second has output
[w_1,g,0,b,z,0] and bath [a,w_2,...]. These formulas are statements
about wires and hence can be checked with actual binary colors chosen
to separate a from w_1. Thus a positive final displacement, even with
the guard retained, cannot replace the nonnegative path event. The proof
uses the stronger event exactly where original bath tokens must be
excluded from both branches.

Status: the operator token identity and counting above were independently
reconstructed from the written endpoint representation, then matched to
the constructive helper's complete final source. This is internal acceptance
of the displayed argument, not external certification, historical originality,
or an efficient code construction. No numerical job, paid resource,
outreach, or fresh physical initializer was used.
