# Independent audit of the direct infinite-boost measure certificate

This addendum audits a candidate operation communicated by the root investigator
after this worker reconstructed the original finite-boost argument. No peer
artifacts were read. The derivation and exact matrices below are independent
checks, not agreement used as proof, formal verification, or a priority claim.

## 1. Statement with the necessary distinctions

Partition the physical vertices into the connected components C_1,...,C_k of a
chosen positive fast graph. Singleton components are allowed. Let a_e>0 be its
fixed internal edge weights, let b be a fixed nonnegative retained graph, and
let q_W=b+W a. The original graph r must agree with b on edges outside the fast
graph; its finite internal rates may be arbitrary nonnegative values.

Let H_A and H_B be the killed-pair generators of a and b. These are not the
full permutation generators. Put P=orthogonal projection onto ker H_A,
Q=I-P, R=H_A^+, and C=P H_B P restricted to ran P. For a fast edge e,
P e_e=0. Define

    h_e = e_e^T R 1,
    g_e(t) = -e_e^T R H_B P exp(-t C) P1.

For each fixed positive T,

    W S_(q_W),e(t) dt  -->  h_e delta_0(dt)+g_e(t)dt          (M)

weakly on [0,T]. The density g_e is nonnegative. If K_av is the exact full
permutation averaging endpoint kernel, the finite-boost Duhamel inequality
therefore yields

    sup_sigma TV(P_r(T)(sigma,.),K_av(T)(sigma,.))
      <= sum_(e fast) a_e [ h_e S_r,e(T)
            + integral_0^T S_r,e(T-t) g_e(t) dt ].           (D)

K_av uses the *full permutation* orbit projection Pi, namely
Pi exp(-T Pi L_B Pi) Pi. P in (M) is the different, smaller *pair* projection.
Confusing these two projections would invalidate an implementation.

## 2. Exact structure of the pair projection and Green rows

The fast killed-pair chain decomposes into:

* pairs in one fast component C, on which both walkers eventually meet and
  the internal killed generator is positive definite;
* pairs in distinct fast components C,D, on which two independent internal
  walks never meet. Their unique equilibrium is uniform on C x D.

Thus P is zero on intra-component pair blocks. On a cross-component block it
has all entries 1/(|C||D|). The pseudoinverse R can have signed rows on
cross-component zero-mean spaces. However, the row starting at a fast edge e
inside C lies entirely in the positive intra-component block:

    e_e^T R = e_e^T G_C,

where G_C is the inverse of the internal killed-pair generator on C, extended
by zeros. This row is nonnegative. Therefore h_e>=0. Moreover, H_B's entries
from intra-component pairs to cross-component pairs are nonpositive. Hence
the row -e_e^T R H_B P is nonnegative, and the coarse killed semigroup is
nonnegative. This proves g_e(t)>=0 without assuming that the entire
pseudoinverse is entrywise positive.

## 3. A positive and smaller representation of the correction

Let B_CD=sum_(x in C,z in D) b_xz and d_D(x)=sum_(z in D)b_xz. On the component
graph define a one-walker generator with jump rate C->D equal to B_CD/|C|.
Its invariant vertex weights are |C|. Kill two independent coarse walkers
when their components meet. On unordered distinct component pairs, the
killing rate at {C,D} is

    B_CD(1/|C|+1/|D|).

Noncolliding endpoint moves have the corresponding coarse one-walker rates.
Call this positive killed generator K. It is reversible with pair weights
|C||D|; it is generally not symmetric in unweighted coordinates. Lifting
component-pair functions to constants on the fine cross-pair blocks gives

    P H_B P lift = lift K.

For e inside C define the nonnegative leakage weights

    beta_e(C,D)
      = sum_({x,y} subset C) G_C(e,{x,y})[d_D(x)+d_D(y)].

Then the root's signed matrix formula is equivalently

    g_e(t)=sum_(D != C) beta_e(C,D) [exp(-tK)1]_{C,D}.       (P)

Only internal killed Green solves and the coarse killed-pair survival chain
are needed for this representation. This is a proved positive composition,
not a claim that its setup or quadrature cost is negligible or practical.
It also makes boundary excursions explicit: g records paths which escape an
initial fast component during the O(1/W) initial layer and survive for O(1)
coarse time with O(1/W) probability.

## 4. Block resolvent proof of the measure limit

For z>0 let D_W=z Q+W H_A|_Q+Q H_B Q. Its inverse satisfies

    W D_W^{-1} -> R|_Q.

The P-block Schur complement is

    F_W=zP+P H_B P-P H_B Q D_W^{-1}Q H_B P,

and F_W^{-1}->(z+C)^{-1} on ran P. Solving the resolvent equation with
right-hand side 1 and taking its Q part gives

    W e_e^T(z+W H_A+H_B)^{-1}1
      -> e_e^T R1-e_e^T R H_B P(z+C)^{-1}P1
       = h_e+integral_0^infinity exp(-zt)g_e(t)dt.           (L)

The left side is the Laplace transform of the nonnegative measure
W S_(q_W),e(t)dt. A uniform mass bound is available directly from the global
Green argument: the initial edge has direct killing 2W a_e, so

    W integral_0^infinity S_(q_W),e(t)dt
      <= binomial(n,2)/(2a_e).

If the physical graph is disconnected, restrict to the pair communicating
class reached from e; its two positions remain in the same physical connected
component and meeting is almost sure. This avoids applying an inverse to
unreachable singular pair blocks.

Nonnegative locally finite measures with this uniform mass bound have vaguely
convergent subsequences. (L) identifies every such subsequential limit by the
uniqueness of Laplace transforms. A possible mass at infinity has no effect
on compact time intervals. The identified limit has exactly one atom, at 0,
and a continuous density for t>0. Restriction to [0,T], T>0, is therefore weak
convergence there: the endpoint T has zero limiting atomic mass. This proves
(M). It is not merely pointwise convergence W S_W(t)->g(t), which would lose
the initial atom.

## 5. Passing the full endpoint inequality to the limit

The original finite-state permutation semigroup for b+W a converges, for
every T>0, to Pi exp(-T Pi L_B Pi)Pi. This is the standard finite-dimensional
fast/slow block-resolvent argument, now on the full permutation space. The
definition is conceptual; an endpoint can be sampled by conditional block
uniformization without enumerating this space.

For e fast, |W a_e-r_e|/W -> a_e. Substitute t=T-u in the valid finite-boost
Duhamel term. The test function S_r,e(T-t) is continuous on [0,T]. Apply (M)
and finite-state continuity of TV to obtain (D), with exactly the displayed
constant. No Aldous-gap tail remains in (D). The price is the nonzero
excursion density g, which cannot normally be discarded.

The formula is for positive T. At T=0 the true original kernel is identity,
whereas inserting initial Pi would change it; the positive-time singular
limit is not uniform down to zero. If k=1, P=0 and g=0, so only the initial
atom remains. This special case is consistent with the direct formula.

## 6. Exact three-vertex counterexample to dropping g

Take fast edge 0-1 of weight 1 and retained edge 1-2 of rate b>0. In pair order
(01,02,12),

    H_A = [[2,0,0],[0,1,-1],[0,-1,1]],
    H_B = b*[[1,-1,0],[-1,1,0],[0,0,2]],
    P   = [[0,0,0],[0,1/2,1/2],[0,1/2,1/2]],
    R   = [[1/2,0,0],[0,1/4,-1/4],[0,-1/4,1/4]].

The coarse surviving pair has decay rate 3b/2. Therefore

    h_01=1/2,
    beta_01({0,1},{2})=b/2,
    g_01(t)=(b/2)exp(-3bt/2).

Let the original 0-1 rate be zero. Its pair started at 01 never meets, so
S_r,01(t)=1. The atom-only proposed endpoint bound would be 1/2. The actual
original process only exchanges vertices 1 and 2, with probabilities
(1+exp(-2bT))/2 and (1-exp(-2bT))/2. In the averaged process the label at
external vertex 2 follows a three-state complete graph with off-diagonal rate
b/2, then the two internal labels are uniformly ordered. The averaged mass
on the two permutations reachable in the original process is

    1/3+exp(-3bT/2)/6.

For both permutations the original probability is at least the averaged one.
Consequently the exact full-permutation endpoint TV is

    2/3-exp(-3bT/2)/6 > 1/2,       bT>0.

This disproves the atom-only bound on a valid supplied symmetric three-vertex
model. The corrected direct certificate is

    1/2+(1/3)(1-exp(-3bT/2)),

which is larger than this actual TV and comes directly from h and g.

The accompanying independent exact checker verifies the displayed matrices,
projection/pseudoinverse equations, the positive leakage identity, and rational
resolvent transforms. These finite checks supplement the proof; they do not
replace it or establish novelty.
