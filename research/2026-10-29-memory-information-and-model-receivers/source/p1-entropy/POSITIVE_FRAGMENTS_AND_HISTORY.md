# Positive fragments, nonlinear entropy bounds and history tests

29 October 2026, Brisbane. Root's next attack after the acquired scalar
certificate. This develops the representation beyond one Horn matrix.
The classical CP cone and its dual are retained explicitly.

## 1. How much positive mass is incompatible with equilibrium?

For a symmetric entrywise nonnegative matrix C define

    d_CP(C)=min {sum_ij(C_ij-B_ij): B is CP, 0<=B<=C entrywise}.   (1)

The feasible set is compact. This deficit is zero iff C is CP.
It is homogeneous and has the conic dual

    d_CP(C)=sup {-<H,C>: H copositive, H_ij>=-1}.                 (2)

For weak duality, C-B is entrywise nonnegative and <H,B>>=0, so
-<H,C><=sum(C-B). For equality, write (1) as sum C minus the maximum
CP mass B dominated by C. The dual of this latter maximization has
Y>=0 and Y-J copositive. Set H=Y-J. Strict dual feasibility follows
from taking Y to be a sufficiently large positive multiple of J:
a positive multiple of J lies in the interior of the copositive cone.
Finite-dimensional conic duality therefore applies even when C has zeros.

No polynomial algorithm for CP membership or its dual is implied.
A supplied witness is inexpensive to evaluate, while finding the best
witness may be difficult.

Geometric path comparison produces a particular feasible B, so the
earlier bounds become

    sigma >=4 d_CP(C_sym(t))/t,                              (3)
    E >=4 d_CP(C_phi,sym),                                  (4)
    E >=2 d_CP(M_sym)^2/c.                                  (5)

The first uses normalized stationary lag probabilities, the second
bounded positive-duration excursion weights, and the third the paired
residence first moment and residual c. The separate units and observation
interfaces must not be conflated.

For M=I+(17/30)Adj(C5), the deficit is exactly2/3. The Horn witness
attains the dual. A primal optimum is B=I+(1/2)Adj(C5): sum over the
five edge vectors (e_i+e_j)/sqrt(2) gives this CP matrix, and B<=M.
Thus the chosen linear witness is optimal within (4), not merely one
unexplored candidate on this example.

## 2. A nonlinear refinement from the same geometric comparison

Let

    psi(s)=2 sqrt(1-s^2) atanh(sqrt(1-s^2)),  0<s<=1,
    psi(0)=infinity.

This function is decreasing and convex. With z=sqrt(1-s^2),

    psi'(s)=-2s atanh(z)/z-2/s,
    psi''(s)=2[1/s^2-(atanh(z)-z)/z^3]>0.

The series for atanh gives
(atanh(z)-z)/z^3<=1/[3(1-z^2)], proving the last sign.
Limits define the value and derivatives at s=1.

For any two nonnegative microscopic path densities p,q, put
m=(p+q)/2 and a=sqrt(pq)/m. Then

    (p-q)log(p/q)/2=m psi(a).

On every ordered path bin, apply Jensen to the nonnegative symmetrized
Jeffreys density (p-q)log(p/q)/2. Its contribution is at least c psi(b/c),
where c is the symmetrized probability/flux mass and b its geometric-mean
mass. An off-diagonal endpoint bin need not itself be reversal invariant;
equivalently pair it with its reversed bin and count the two entries
consistently. This is a conventional scalar divergence inequality; it is
not claimed as new.

Applying the inequality entrywise and then relaxing the unknown geometric
matrix to every compatible CP matrix gives

    E >= F(C):=min_{B CP, 0<=B<=C}
                sum_ij C_ij psi(B_ij/C_ij).                 (6)

Terms with C_ij=0 are zero, since B_ij must also vanish. Here C is the
symmetrized hidden-excursion flux matrix in a declared duration bin with
weight in [0,1]. The same expression bounds sigma*t for a normalized lag
joint. Multiple disjoint duration bins may be summed. Convexity of the
perspective makes the relaxation a convex conic problem, although the
CP cone remains computationally difficult.

Since psi(s)>=4(1-s), (6) is at least4d_CP(C). Keeping separate bins
cannot weaken the Jensen bound. Compatibility of the CP matrices across
bins with ONE physical generator is not imposed by (6); hence it is a
lower bound, not a general realization theorem.

## 3. Exact benchmark and collision with the conventional optimum

For the five-cycle matrix above, average any candidate B over the cycle
symmetries. CP feasibility is preserved and convexity cannot increase the
objective. An optimum may therefore have diagonal x<=1, neighboring
entries y<=17/30, and zero other entries.

Because the support graph is triangle-free, every nonnegative Gram vector
has support on a single edge or vertex. This gives x>=2y; conversely that
condition is sufficient for this symmetric family. Since psi decreases,
x=1 and y=1/2 optimize (6). The resulting lower bound is

    F(M)=10*(17/30)*psi(15/17)
        =(16/3)log(5/3).                                  (7)

The explicit mirror-star generator attains it. Thus at this exact endpoint
population matrix, (6) determines the minimum entropy over ALL finite
even-state CTMCs, without the earlier hidden clock ceiling. The statistical
assay does not infer exact zeros in M and does not silently use this
population optimization.

This same endpoint optimum is obtainable using Skinner and Dunkel's
2021 hidden-star reduction and ordinary scalar optimization. That
antecedent was found during construction and takes priority over a
claim that endpoint-star reduction is new. Their stronger population
comparison is preserved in controlled_frontier. The useful remaining
addition is the short copositive certificate, its rigorous duration-bin
and lag versions, its sharp uniform constant, and its acquired confidence.

## 4. Reflected history tests

The lag theorem is a special case of a finite-history principle.

Observe a stationary hidden CTMC during [-T/2,T/2]. Apply the SAME finite
partition of half-path observations to the right half in forward time
and the left half in reverse time. Let C_ab be their joint label matrix.
Observation mapping and noise must commute with the physical reversal.
Labels are deterministic, or independent randomized kernels conditional
on the half paths. Their sum is one.

For the geometric reversibly killed process, condition on the midpoint
hidden state x. Reversibility makes the two reflected half-path weights
equal functions v_a(x)>=0. These are UNNORMALIZED surviving half-path
weights. The Markov property gives conditional factorization. Hence

    C_geo,ab=sum_x pi_x v_a(x)v_b(x)

is CP. If s(x)=sum_a v_a(x) and the half weights are normalized by s(x),
the midpoint weights must become pi_x s(x)^2, not pi_x. A shared random
midpoint reading y can be included by conditioning on (x,y) and integrating
pi_x r(dy|x) v_a(x,y)v_b(x,y). General correlated sensor memory across the
midpoint requires its own conditional factorization and is not included
merely because the sensor output is reversal symmetric.

The same microscopic path AM-GM comparison gives
C_sym-C_geo>=0 entrywise, with total deficit no larger than the full-path
affinity deficit. Therefore every copositive witness with gamma>0 gives

    sigma >=4gamma/(T h_minus).                            (8)

The entropy-horizon product is sigma*T, not sigma*T/2. Arbitrary memory
in the observed process is allowed; conditional independence is used
only at the microscopic midpoint.

This furnishes a hierarchy of bounded witnesses as history tests are
enlarged. It does NOT assert that CP feasibility of all pair or history
matrices is sufficient for one finite equilibrium hidden generator.
The earlier constructive converse proves only closure for a single
two-time joint matrix at a specified lag. Joint temporal consistency and
finite-clock realization remain separate constraints.

Reflection positivity and the nonnegative half-path Gram structure are
classical antecedents: Jorgensen, Neeb and Olafsson (2016), Lemma 3.21,
already displays the integral of two nonnegative half-word semigroup
products. The prospective addition is their use with the geometric path
measure for quantitative entropy certification, not the bare nonnegative
factorization. The independent review in intervention_challenge/
POSITIVE_HISTORY_INDEPENDENT_REVIEW.md checks this extension and Sections
1-2. Its exact 243-path controls are discrete skeleton controls, not CTMC
embeddings or native acquisitions. The review's frozen source hash refers
to the version before these clarifications were applied.

## 5. Sharpness and physical scope

The independent review constructs a five-cycle near-equilibrium family
with full positive-duration Horn gap gamma and E/gamma tending to4.
Thus no larger universal coefficient can replace4 in (4), even for
observationally reversible, PSD kernels.

No visible-path test supplies the correct microscopic parity convention.
The exact PARITY_SCOPE_COUNTEREXAMPLE.md shows that the same native
15-state generator has zero generalized entropy under a different
odd-state involution fixing all observed ports. The all-even source
class must be justified physically before interpreting these bounds
as heat or energy consumption.

