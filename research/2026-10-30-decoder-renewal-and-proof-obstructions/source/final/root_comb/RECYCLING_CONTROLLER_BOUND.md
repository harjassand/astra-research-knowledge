# A quadratic approximate-recovery barrier for SWAP-controlled recycling

30 October2026. Root proof extension of C's independently derived exact
recycling recurrence. Its separate whole challenge is pending until actually
recorded. No source, solver or numerical case is used by this argument.

This is a specified physical-history-disposal architecture. It is not a
quadratic lower bound for all approximate native-query algorithms.

## 1. Precisely allowed operations

Let N_U(X)=U(X tensor I_r/r)U*, logical dimension k>=2, r>=1, D>=kr.
U is arbitrary unknown isometric and the source is memoryless. One encoded
payload is in physical register B0. Initially prepare ANY known state on a
logical query input and arbitrary known memory M, independently of the
payload, and make one forward source call, obtaining B1. This initial query
may be offline. No U-dependent advice is given free.

There are m further cells, so total native query count is Q=m+1. In cell t,
the retained physical carriers are the target B0 and current programme B_t.
On them and ALL known memory M apply a known isometry

    W_t=P_+^(B0,Bt) tensor V_(t,+)
                   +P_-^(B0,Bt) tensor V_(t,-),          (R1)

where V_(t,+/-):M -> A_new tensor M_new are arbitrary known isometries,
A_new has dimension k, and P_+/- are the whole-register physical SWAP
sectors. Send A_new through one ordinary forward N_U call to produce
B_(t+1), then DISCARD the spent B_t. Retain B0,B_(t+1) and all M_new.
Known memory may grow without any bound. Arbitrary known-memory controls,
ancillas and discarded known environments can be absorbed by dilating M.
No scalar-angle assumption on V_+*V_- is imposed.

Until the final decoder there are no OTHER interventions on the physical
carriers: (R1), their source encoding and the displayed disposal are the
model. The final decoder may be ANY known CPTP map on both retained physical
carriers and all memory. The theorem does not include measurements that
first transfer a spent physical carrier's frame information into an extra
memory and then merely rename that carrier as discarded. General operations
outside(R1), free U-dependent programmes, or different joint source memory
are also outside this class.

For m>=1, the Haar-average entanglement fidelity of every such decoder is

    F_e <= min{1, 1/k^2 + sqrt(m)/r}.                    (R2)

For m=0, the separate complete one-query optimum is (1+1/r)/k^2.
Consequently a uniformly accurate inverse of half-diamond error at most
epsilon<1-1/k^2 in THIS architecture requires

    Q-1 >=r^2(1-epsilon-1/k^2)^2.                       (R3)

All calls, including the initial programme, are counted. This is an
approximate, full-throughput obstruction with arbitrarily large known
reference history. It does not forbid a better controller retaining more
unknown-frame physical history or changing the permitted interventions.

## 2. Exact logical recurrence; the cross-free parts form an instrument

Put A_t=(V_(t,+)+V_(t,-))/2 and B_t=(V_(t,+)-V_(t,-))/2. Then

    W_t=I_phys tensor A_t + SWAP_phys tensor B_t,
    A_t* A_t+B_t* B_t=I,
    A_t* B_t+B_t* A_t=0.                                (R4)

The starred products in(R4) are operators on all of M. A_t and B_t need
not be normalized isometries and their branch weights may depend on the
known-memory state. Scalar Pauli-sector amplitudes are a special case.

Move temporarily into U's logical/junk frame. All physical operations in
(R1) are permutations, so U factors through them and through subsequent
source calls. At each cell the TWO retained junk registers are exactly
I_r tensor I_r/r^2, independent of the entire logical/reference history.
This is true initially. For the next step, write the physical swap as
S_logical tensor S_junk. Diagonal terms give partial junk trace I_r/r,
whereas EACH cross term gives

    Tr_(spent junk)[S_junk/r^2]=I_r/r^2.                 (R5)

The new source appends another independent I_r/r. Thus the same reduced
junk factorization holds after the cell, including cross terms, proving
the induction. It is not a reset assumption about the logical carriers.

On the target logical carrier L0, current programme carrier Lold and M,
let K_A=I_(L0,Lold) tensor A_t and K_B=S_(L0,Lold) tensor B_t. Define

    a_t(X)=Tr_Lold K_A X K_A*,
    b_t(X)=Tr_Lold K_B X K_B*,
    x_t(X)=Tr_Lold [K_A X K_B*+K_B X K_A*].

Outputs are the updated target L0, the new query A_new and M_new. Their
EXACT physical-source recurrence is

    T_(r,t)=a_t+b_t+(1/r)x_t,
    T_(0,t)=a_t+b_t.                                    (R6)

T_(r,t) is CPTP because it is the literal physical cell in the input
frame. T_(0,t) is ALSO CPTP: a_t,b_t are completely positive and(R4)
makes their trace sum the input trace. Furthermore x_t is Hermiticity
preserving and trace annihilating, since the physical/logical swap commutes
with operators on M and the last identity in(R4) cancels its trace.

For EVERY positive subnormalized X, also with any external reference,

    ||x_t(X)||_1 <=2 sqrt[Tr a_t(X) Tr b_t(X)].           (R7)

Indeed trace norm contracts under partial trace, the two cross terms are
adjoints, and Schatten Cauchy gives
||K_A X K_B*||_1<=||K_A X^(1/2)||_2 ||K_B X^(1/2)||_2.
This proves(R7) with the ACTUAL branch probabilities. It introduces no
operator norm depending on a small postselection probability.

## 3. Before the first cross, only one branch can retain the payload

For the Bell test let R be the inaccessible k-dimensional target reference.
Initially, in this logical frame,

    Z0=Phi_(R,L0) tensor zeta_(Lold,M),

where zeta is known and independent of U and of the target. Put
Z_t=a_t ... a_1(Z0), p_t=Tr Z_t and p_0=1. Every a_t acts as the identity
on L0 before discarding Lold, so

    Z_t=Phi_(R,L0) tensor zeta_t,
    p_t<=p_(t-1),
    d_t:=Tr b_t(Z_(t-1))=p_(t-1)-p_t>=0.                (R8)

zeta_t is a known subnormalized state, independent of U. Operationally all
older source outputs have been discarded WITHOUT physical interaction on
an all-a prefix; their traced channels are just input traces. Hence only
the current single-query programme remains. Conditioning that known
preparation on its U-independent probability p_t supplies no U-dependent
advice. There is no source query hidden in zeta_t.

By contrast the first b_t after an all-a prefix SWAPS L0 into the spent
Lold register, which is then traced out. B_t acts only on M. The reference
becomes I_R/k in PRODUCT with everything retained. Later operations on
the controller side cannot restore a reference correlation. Every word
of cross-free maps containing b therefore has Bell fidelity exactly1/k^2
times its trace, whatever U or the final decoder.

For the all-a word at the end, the current programme is obtainable from
ONE known-input source query with arbitrary reference memory. The complete
one-query upper bound from ROOT_MECHANISM.md gives its normalized
Haar-average fidelity at most (1+1/r)/k^2. Thus the entire cross-free
controller followed by any final decoder has

    F_0 <=1/k^2 +p_m/(k^2 r).                           (R9)

This step uses the strong one-query bound allowing arbitrary programme
states and memory, not only a fixed normalized Choi programme.

## 4. First-cross telescoping pays the accumulated coherent effect

Expand the difference of the products of T_(r,t) and T_(0,t) by the exact
telescoping identity with FULL T_r maps after the first displayed cross
and cross-free T_0 maps before it. A cross-free prefix is the positive sum
of its all-a word Z_(t-1) and words already containing b. On the latter,
R is I_R/k in product with the rest. Applying x_t produces a trace-zero
operator still with that product reference, and every future complete
map preserves those facts. Its final Bell expectation is zero.

Only the all-a prefix therefore contributes to the fidelity difference.
Its cross operator H_t=x_t(Z_(t-1))/r is Hermitian, trace zero, and obeys

    ||H_t||_1 <=(2/r) sqrt(p_t d_t).                     (R10)

Future T_r maps, re-embedding by the SAME U and the final CPTP decoder
contract its trace norm. For a trace-zero Hermitian operator H, a Bell
projector has |Tr(Phi H)|<=||H||_1/2. Hence, pointwise in U, its Bell
contribution has magnitude at most sqrt(p_t d_t)/r. Combining with(R9),

    F_e <=1/k^2 +p_m/(k^2 r)
                         +(1/r) sum_t sqrt(p_t d_t).

Since sum_t d_t=1-p_m and sum_t p_t<=m, Cauchy gives

    F_e <=1/k^2 +[p_m/k^2+sqrt(m(1-p_m))]/r.             (R11)

For m>=1,k>=2 the bracket is decreasing on p_m in[0,1]: its derivative
is 1/k^2-sqrt(m)/(2sqrt(1-p_m))<0 away from the endpoint. Its maximum is
sqrt(m), proving(R2). No assumption of scalar, predetermined angle
weights or a logical Markov reset was used in this extension.

Finally, complete half-diamond error is at least the logical Bell-input
error, which is at least1-F_e for each U. A uniform error epsilon would
therefore require average F_e>=1-epsilon, giving(R3).

## 5. What has and has not been decided

The bound explains a genuine failure of this economical history policy:
all known reference registers may be retained, but each disposal of the
spent physical carrier limits useful coherence by1/r, while the cross-free
branch that swaps out the target erases its original information. Their
instrument/Cauchy tradeoff permits only O(sqrt(Q)/r) gain.

The result grants arbitrary final processing and arbitrary growing known
memory inside(R1). It does not grant an arbitrary physical preprocessing
network between cells. It therefore does NOT classify all processors with
two laboratory registers, all covariant memory representations, all possible
known physical measurements, or all approximate native inverses. Retaining
old source-frame information in another physical representation is a real
change of architecture, not a relabeling that this theorem rules out.

Fresh flat junk is essential to(R5). Nonflat spectra do not give a scalar
1/r cross factor, and persistent source labels do not give the stated
product junk marginal. Neither case is silently included here. The separate
exact-heralding theorem has a different, stronger universality scope and
does not supply this approximate-recycling result by itself.
