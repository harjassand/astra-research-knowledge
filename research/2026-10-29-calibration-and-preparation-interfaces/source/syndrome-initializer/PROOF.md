# Polynomial nominal-syndrome initialization by decoder-history polymers

29 October 2026. Constructive application of established low-temperature
polymer sampling. The new source-specific input is a local, unique-history
presentation of EXACT admissible RX/RZ syndromes. KP convergence alone is
not asserted to provide a sampler. No hardware or noisy-preparation result
is claimed, and world priority is UNKNOWN.

## 1. Target and theorem

Fix the PRIMARY-QUALIFIED odd subdivision ell, its accepted recursive family,
and its nominal commuting Hamiltonian H0,k=sum_j(I-S_j)/2. Let Sigma_k be
the actual admissible joint syndrome space, including all redundant-check
relations. The target is the classical law

    pi_beta(sigma)=exp(-beta|sigma|)/Z_syn, sigma in Sigma_k.   (1)

There is one sufficiently low FIXED temperature, beta=4ln B0, independent
of level k, at which the construction below samples (1) within TV error
epsilon in time polynomial in n_k and 1/epsilon, with explicit costs.
The constants depend on the actual fixed ell and source degree/cell bounds;
they may be enormous. Beta can also be chosen above the already specified
memory counting threshold. This supplies a polynomial ideal preparation
contract for the NOMINAL corrected thermal encoder. It does not sample the
full Gibbs state by physical time evolution.

The algorithm uses the public finite complexes and local rules. It is not
given a global generator, a microscopic state, a thermal sampler, or an
unpaid polymer-generation oracle. Global syndrome membership is used only
as an independent finite consumer check, not in the production predicates.

## 2. Auxiliary decoder: sampling histories are not recovery actions

For each CSS syndrome sector, use the primary coarse-graining maps of
Theorems 4.6--4.7 all the way down to the constant seed C0. These are
AUXILIARY sampling maps. The final quantum encoder/decoder still uses the
same memory recovery C_sigma as before; auxiliary histories only sample its
input syndrome law. Thus the primary modification of the memory decoder
at level 2 is not silently undone.

The literal local choices can be fixed without an optimization oracle:

* At RX, in each X block enumerate local solutions f_x of
  delta_x f_x=sigma_x until finding one with outgoing syndrome weight
  <=|sigma_x|. Primary Lemma4.8 guarantees existence for a valid input.
  Fix the order once; zero input returns the zero correction.
* Update each Q-block syndrome by the adjacent X-block outflows. Enumerate
  local f_q solving delta_q f_q=sigma_q with outgoing weight <=|sigma_q|.
  Primary Lemma4.12 guarantees existence after successful valid cleaning.
* At each coarse Z location require the two remaining fine Z-point bits
  to coincide, and output their common bit. Otherwise reject locally.
* At RZ, output the parity of the fine syndrome in each connected Y_z
  vertex block. No global membership test is performed at this step.

These rules are totalized with a failure symbol on invalid local inputs.
All local search spaces have fixed size for fixed ell. The implementation
solves a binary affine system and enumerates its nullspace, at worst
2^(C_cell) candidates for a cell. This finite cost is explicitly charged.
It is not claimed efficient as ell itself grows.

## 3. Local predicates pay ALL admissibility relations

Introduce only syndrome bits sigma_i at every level, in each sector. A
history assignment is accepted by the following bounded-arity factors:

1. Each RX X-block fill is valid.
2. Each RX Q-block fill is valid after its neighbouring X-block updates.
3. Each RX final paired Z bit agrees with the associated coarse bit.
4. Each RZ coarse bit equals its block parity.
5. The constant-size seed syndrome is in the seed's actual image space.

Corrections are evaluated within the factors; they are NOT sampled variables.
All-zero input satisfies every factor. Every admissible top syndrome has
exactly one accepted history, by the deterministic primary maps.

The converse is essential and follows locally, not by assuming cocycles.
At RX, successful factors explicitly give

    sigma_i=delta_i f_i+F_RX^2 sigma_(i-1),                 (2)

where F_RX^2 duplicates each coarse Z bit into its two fine Z points.
Its explicit F_RX^1 lifts a coarse qubit to the all-one cochain on Y_q,
so delta_i F_RX^1=F_RX^2 delta_(i-1). If the coarse syndrome is admissible,
(2) gives a fine preimage. Local fill failures reject the inputs for which
the required local coboundary property would not hold.

At RZ, the quotient of each local degree-two block by its local boundaries
is its single parity bit, because the corresponding Y_z graph is connected.
The incoming Q-block map on these classes is exactly the old coboundary
matrix (primary Lemma3.11 and proof of Theorem4.6). Conversely, lift a coarse
preimage to local Q representatives; its fine boundary has the prescribed
block parities. The difference from the input has even parity in every
connected Y_z block and is filled by local edge paths. Thus

    fine RZ syndrome admissible iff its coarse parity syndrome is.   (3)

Inducting upward from the seed proves that accepted histories project
BIJECTIVELY to the complete top admissible space. Equations (2)--(3) pay
redundant parity relations. Base admissibility alone, without these local
conditions, would not have sufficed.

## 4. Bounded graph and a uniform energy inequality

Make the primal graph G of the factors: variables sharing any factor are
adjacent. It need not be the physical check graph. Each variable is binary;
its nonzero value is uniquely 1, so no hidden decoration multiplicity occurs.

For explicit source bounds let D=7, E=4, F_*=DE=28,
t=(ell-1)/2, and C_cell=8F_*(t+1)^2, which bounds every local block's
total cell count. RX X factors have <=C_cell inputs. Q factors read at
most D adjacent X blocks. An RX coarse-Z factor reads its two fine Z bits,
at most D Q-block inputs and their at most D^2 X-block inputs, plus one
coarse bit. RZ factors read one vertex block plus its coarse bit. Therefore

    arity <=a=3+(D+D^2)C_cell,
    factors per variable <=f=2+D+D^2,
    max_degree(G)<=Delta_bar=f(a-1).                      (4)

The constant seed factor is included in these loose bounds. Each new code
has at least two Q-block vertices per old qubit, in either replacement.
Thus sum_i n_i<=2n_top. The two sectors together have at most Dn_i supplied
check bits at level i, so the number N of history variables satisfies

    N<=2D n_top.                                         (5)

The source maps give |sigma_(i-1)|<=|sigma_i| at RZ and at most half at RX;
the dual sector exchanges the roles. Consequently EVERY accepted history h
obeys

    |h|=sum_(sectors,i)|sigma_i| <=4|sigma_top|.            (6)

This is why intermediate correction bits were not introduced. Their
potentially large weight would unnecessarily worsen the energy ratio.

## 5. Exact positive polymer representation

Take connected components of the 1-valued support of h in the primal graph.
Every factor sees nonzero variables from at most one such component. Keeping
that component and zeroing the rest therefore leaves every factor either
unchanged or at its accepted all-zero input. Each component is itself a
valid history; by Section3 its top syndrome is individually admissible.

Conversely, any family of valid connected nonzero supports which are
disjoint and nonadjacent has an accepted union: the same factor argument
applies. Thus histories correspond EXACTLY to compatible polymer families.
This proves admissibility and recombination without incorrectly assuming
physical connected syndrome components are valid by themselves. Merely
using the original active decoder graph could miss nonlinear cooperative
activations; the complete predicate primal graph includes those dependencies.

For a polymer gamma define E(gamma)=its number of TOP-level 1 bits and

    w_gamma=exp[-beta E(gamma)].

The weight factors over components. The history-to-top bijection means the
polymer partition function equals Z_syn exactly, with no multiplicity factor.
By (6), E(gamma)>=|gamma|/4>0. At beta=4ln B0,

    w_gamma=B0^(-4E(gamma)) <=q^|gamma|, q=1/B0.           (7)

## 6. Paid finite polymer generation and truncation

Let Delta be either the computed maximum degree of the literal graph or
its uniform bound (4), and put A=4max(1,Delta). Rooted connected ell-vertex
sets are at most A^(ell-1): enumerate plane rooted trees (Catalan bound
4^(ell-1)) and neighbour choices (at most Delta per tree edge), then discard
repeated embeddings. Alternatively grow connected sets and deduplicate.
This is an explicit algorithm, not an enumeration oracle.

Enumerate every connected support up to cutoff K. Test only factors whose
scopes meet that support; all other factors see zero. At most fK factors
need testing, each using the fixed finite local rules. Let T_rule bound one
rule evaluation, including its local fill search. The generation cost is

    O[N A^K poly(K,Delta) T_rule],
    T_rule<=2^(C_cell) poly(C_cell,D),                    (8)

plus the polynomial finite-complex construction. The number M of valid
listed polymers is <=N sum_(ell<=K) A^(ell-1). No global image-space test
occurs in this production procedure.
These counts use sparse vertex lists/local coordinate arrays with O(log N)
addresses. The literal finite consumer uses full N-bit integers for convenient
shifts/masks; it pays an additional polynomial N-bit arithmetic/storage
factor. It is not a unit-bit-cost O(N²/epsilon) implementation.

In a positive hard-core polymer law, Pr(gamma occupied)<=w_gamma. Hence
deleting all polymers longer than K changes the distribution by TV at most

    tail_K<=N q(Aq)^K/(1-Aq).                            (9)

The truncated Gibbs law is exactly the full law conditioned on no omitted
polymer. Choose K so (9)<=epsilon/4, or K=N if the bound asks for more.
Then K=O(log(N/epsilon)) at fixed sufficiently large B0.
If the cutoff is capped at N, N is no larger than this logarithmic bound,
so the same polynomial enumeration conclusion holds.

## 7. Explicit ordinary heat-bath sampler and mixing proof

On the finite listed polymer variables, choose one uniformly. If all other
occupied polymers are compatible with it, put it in the configuration with
probability w/(1+w); otherwise put it absent. This is ordinary hard-core
heat bath, reversible at the desired truncated law. Start from empty.
When M=0 the empty law is already exact and no update is performed.

Couple configurations differing by one polymer gamma and measure discrepancy
by |gamma|. Updating gamma removes it with probability 1/M. Updating an
incompatible eta can add at most |eta|w_eta/M in expectation. Uniformly,

    S=sup_v sum_(eta contains v)|eta|w_eta <=q/(1-Aq)^2,
    sum_(eta incompatible gamma)|eta|w_eta
       <=(Delta+1)|gamma|S.

Thus with c=(Delta+1)q/(1-Aq)^2<1/2, path coupling contracts by at least
(1-c)/M per update. Weighted Hamming diameter is at most 2N, since each
compatible configuration has total polymer size <=N. It follows that

    TV_after_T<=2N exp[-(1-c)T/M].                        (10)

This size weighting is essential: an unweighted maximum-incompatibility
count would spuriously require a temperature growing with log N.

Choose ONE integer B0>=A_bar^2, where A_bar=4max(1,Delta_bar), and, if
composing with memory, also satisfy the primary rational counting criterion.
Then c<=2/9<1/2 uniformly in k. Moreover A^K grows at most polynomially
in N/epsilon, with exponent ln A/ln(B0/A)<=1. In particular the finite-list
generation is O(N^2/epsilon) times the explicit fixed-rule and logarithmic
factors in (8); M has the same polynomial bound. This is a genuine fixed-
temperature polynomial algorithm, not a temperature scaled with system size.

Set T=2M ceil(log2(8N/epsilon)). Then (10)<=epsilon/4. The toggle probability
is the exact rational coin 1/[1+B0^(4E)]. Its denominator has
O(K log B0) bits. Exact uniform-integer rejection supplies it with polynomial
expected bit cost. For a bounded-time version, cap each of the at most 2T
integer samplers at R=ceil(log2(8T/epsilon)) trials. Their total failure
probability is <=epsilon/4; return the empty configuration on failure.
The resulting output has TV error <epsilon after adding (9)--(10).
No real-number, Poisson, or perfect-sampling oracle is supplied for free.

The finite-list/path-coupling engine is established ordinary polymer
machinery; root independently supplied the same coupling. Primary
algorithmic controls are credited in PRIOR_AND_COST.md. The source-specific
operation is the exact admissibility/unique-history/energy compiler above.

## 8. Nominal encoder and remaining scope

Project the sampled history to its top syndrome. TV error cannot increase.
Using that classical sample in the SAME corrected thermal encoder changes
its channel by diamond norm at most 2epsilon. Composition with the accepted
fixed-controller storage theorem gives

    logical diamond error <=2epsilon
                 +Kdiamond n t exp[-(ln2)2^k/2].

For any fixed desired error budget this is now a polynomial ideal nominal
preparation contract. The executed finite-list bounded-time engine pays its
explicit 1/epsilon dependence. STRONG_ORDINARY.md additionally reconstructs
the established rooted proposal at a still colder fixed B0: it has expected
cost polynomial in N and log(1/epsilon), and therefore can match exponential
logical accuracy in expected polynomial work. No corresponding bounded
worst-case/high-probability work improvement is inferred. The sampler need not rapidly equilibrate
the physical logical degree of freedom, so the full quantum sampler's slow
mixing is no obstruction to this classical task.

The literal implementation supports the source's local construction for
fixed odd ell. Small ell=3 executions test this new interface's algebra,
not the primary's much larger spatially qualified constants or hardware.
No noisy encoding, efficient native control, physical preparation time,
practical threshold or civilisation-level advantage is established. On
small very-cold inputs the ordinary all-zero approximation can be better;
the actual finite comparison must report that, rather than hiding it.
