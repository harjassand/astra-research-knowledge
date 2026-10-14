# Source normalization, graph cuts and the limit of correlated completion

14 October 2026. Internally derived synthesis; external correctness and historical
novelty remain UNKNOWN. Fractional programming, positive quadratic graph cuts,
variational error estimates and NP reductions are established machinery. This
account supplies exact interfaces and proofs for the new compact-kinetics packet,
not a claim of inventing those general principles or acquiring a molecular model.

## 1. Keep the numerator and its actual source mass together

Consider the finite retained counterpart of the packet's conditional-envelope
theorem. There are m explicitly represented retained values, an arbitrary
normalized unrepresented bath measure nu, source vectors s(y) satisfying
ell<=s(y)<=u with ell_i>0, and retained positive operators A_- and A_+.
The full weighted form dominates A_- tensor I on every full field and is bounded
above by A_+ on retained-only fields. Inverses and source integrals exist.
Let G_-=A_-^{-1}, G_+=A_+^{-1}; G_- is entrywise nonnegative as required by the
source positivity-preservation hypothesis. The normalized equilibrium-source
mean is tau=<w,A_theta^{-1}w>/<w,1>, with reference weights folded into s and
the symmetric retained form matrices. It is not an arbitrary prepared-source mean.

The original closure separates a numerator endpoint from a normalization
endpoint. A stronger interval is

    Lsharp = min_{ell<=s<=u} s^T G_+ s/(1^T s),
    Usharp = max_{ell<=s<=u} s^T G_- s/(1^T s),
    Lsharp <= tau <= Usharp.                              (1)

For the upper bound, inverse order gives numerator<=integral q_-(s(y))nu(dy).
By the definition of Usharp, q_-(s)<=Usharp(1^T s) pointwise in y. Integration
and division by the SAME actual mass proves the assertion. Averaging s before
applying the quadratic upper bound would generally be wrong.

For the lower bound, write bar_s=integral s(y)nu(dy). Restrict the full variational
principle to retained fields and use the upper form bound. Optimizing that field
gives numerator>=bar_s^T G_+ bar_s. Its denominator is exactly1^T bar_s,
and bar_s lies in the retained source box, proving the lower bound.

These endpoints are optimal for the abstract source-box/form-comparison
relaxation: for consistent A_-<=A_+, take a one-point bath and use A_theta=A_-
with a maximizing source for the upper, or A_theta=A_+ with a minimizing source
for the lower. A physical completion class may impose further source/form
coupling and exclude these models. Equation(1) is not asserted sharp for such
a smaller class, the packet's min-weight edge law, or arbitrary atomistic inputs.

## 2. An exact polynomial upper compiler

The quadratic-over-linear map q(s)/(1^T s) is convex on positive mass when
G_- is positive semidefinite. Its maximum on a box occurs at a vertex. This
does not require enumerating the2^m vertices: positivity of G_- gives an
attractive binary quadratic problem.

Drop fixed coordinates, let d_i=u_i-ell_i>0 for the remaining M coordinates,
and write s=ell+D z with z_i in{0,1}. Set

    q0=ell^T G_- ell, Z0=1^T ell,
    a_i=2d_i(G_-ell)_i+d_i²(G_-)ii,
    b_ij=d_i d_j(G_-)ij>=0 (i!=j),
    alpha_i=a_i+sum_{j!=i}b_ij>=0.

Then

    q(s)-t Z(s)
      =q0-tZ0+sum_i(alpha_i-t d_i)z_i
                   -sum_{i<j}b_ij|z_i-z_j|.               (2)

For t>=0 construct an s-t network with source->i capacity alpha_i,
i->sink capacity t d_i, and both directed i-j arcs of capacity b_ij.
With z_i=1 on the source side, its minimum cut C(t) gives

    max_z[q(s)-t Z(s)] = q0-tZ0+sum_i alpha_i-C(t).        (3)

The pair capacity is b_ij, not2b_ij. Rational capacities permit exact arithmetic.
The implementation uses ordinary exact Edmonds-Karp and verifies flow=cut.

Start t0=0. At each step maximize(2). If its excess is zero, t is exactly
Usharp. Otherwise set t=q(s)/Z(s) for the returned maximizing vertex. This
strictly increases t and never exceeds Usharp.

There are at most M+2 cut calls, including the final zero-excess certificate.
To prove nesting, let H_t(S) denote(2) for an active set S. It is supermodular.
If S maximizes at t and T maximizes at t'>t, supermodularity and optimality give

    H_t(T)-H_t(S intersect T)<=0,
    H_t(T)-H_t(S intersect T)>=(t'-t)sum_{i in T\S}d_i.

Thus T is contained in S. Different positive-excess updates strictly remove
at least one uncertain coordinate; if the same set returns after its ratio
update, its excess is zero. A greatest-source-side tie rule is implemented,
although strict positive d_i also establishes nesting across distinct t for
any maximizers. Fixed d_i=0 coordinates are excluded from this count.

Construction uses the represented dense Green matrix, O(m²) cut capacities,
and at most m+2 polynomial max-flow computations, in addition to matrix inversion.
For rational input, determinants/minors bound the inverse entry bit lengths;
each updated ratio belongs to one input-defined vertex and has polynomial
encoding length. Capacity normalization and exact rational flow therefore give
polynomial bit complexity. The implementation is a bounded prototype, not a
competitive optimized max-flow benchmark.

This is closely related to established weighted maximum-density/ratio-closure
algorithms. [Gallo, Grigoriadis and Tarjan](https://doi.org/10.1137/0218003)
explicitly treat parametric flow, fractional programming and nonlinear zero-one
optimization. The publisher abstract and bibliography were read, not the full
paywalled proof. Our derivation above is self-contained; priority of this
particular kinetic-envelope application is unresolved.

## 3. A certified lower field and its exact optimum

For any retained trial vector v, set c=v^T A_+v. The full variational principle
gives

    tau >= L(v)=min_{ell<=s<=u}[2s^T v-c]/(1^T s).         (4)

No positivity assumption on v is needed for this direct source-box minimization.
For v=G_+ell it is positive and improves the original lower endpoint. An exact
prefix algorithm evaluates(4): sort the values2v_i, start all s_i=ell_i, and
turn them to u_i in that order. The minimum over these m+1 profiles is L(v).
Indeed, at an optimal ratio t, minimization of the affine excess selects u_i
where2v_i<t and ell_i where2v_i>t. Ties do not alter the excess. Sorting and
prefix sums cost O(m log m) comparisons/arithmetic; rational bit work is paid.

The full lower problem in(1) is convex and may have an interior irrational
optimizer. For example G_+=diag(100,1), ell=(1,1),u=(1,20) has minimizer
(1,sqrt(101)-1), with Lsharp=2(sqrt(101)-1). The best vertex value500/21 is
strictly larger and would be an UNSOUND lower bound. Upper vertex reduction
must not be copied to lower minimization.

There is no gap in the trial-field formulation. If s* minimizes(1), put
v*=G_+s*, L*=q_+(s*)/Z(s*). Convex first-order optimality gives
(2v*-L*1)^T(s-s*)>=0 throughout the source box. Since

    2s^T v*-v*^T A_+v*-L*Z(s)
      =(2v*-L*1)^T(s-s*),

equation(4) attains L(v*)=Lsharp. Numerically finding s*, then rationalizing v
and recomputing c exactly, yields a rigorous bound through(4), even without a
proof of numerical optimality. A failed optimizer affects tightness only;
it cannot replace exact energy and source-box checking.

## 4. Executed improvement and remaining limitations

The independent root compiler reconstructs the packet's16-state retained
gate forms using Fraction arithmetic. Its six source-envelope instances retain
the same physical bounds and construct no bath states. For R=100, the original
and coupled-source upper/lower ratios are approximately:

| Specified feature | Original closure | Coupled source certificate |
|---|---:|---:|
| All four retained bits open |1.019221646|1.018894491|
| First retained bit open |883.523116|44.686020|
| All four retained bits closed |5,528,817.597|754.092907|

The first two rows use dyadic trial-field refinement; the last retains the
better original field after a numerically inferior proposal. Every accepted
bound uses exact field energy and exact prefix minimization. The upper uses
two or three exact cuts. Eighty additional small rational grounded networks
match exhaustive upper and fixed-field lower enumeration. These finite tests
support the implementation; the universal argument is Sections1–3.

The dominant-trap interval remains unusably broad. This does not acquire
global interaction envelopes or locate their support. The cut compiler needs
an explicit m-state retained Green matrix; it does NOT solve the packet's open
general nonconstant-envelope128-coordinate tensor problem. It removes neither
retained dimension, physical model acquisition, inverse conditioning nor bit cost.

## 5. Global R² and R⁴ powers cannot be universally improved

Let an exterior vertex of mass1 connect to a trap of mass delta through
conductance c=delta²/T, and to ground through conductance1. Then

    A0=[[1+c,-c],[-c,c]],
    G0=[[1,1],[1,1+1/c]],
    tau0=[(1+delta)²+T]/(1+delta).

Use the SAME source/form input ell=(1,delta),u=R ell and
A_-=A0,A_+=R A0. An upper completion with source(1,Rdelta),A=A0 has

    tauU=[(1+Rdelta)²+R²T]/(1+Rdelta).

A lower completion with source(R,delta),A=R A0 has

    tauL=[(R+delta)²+T]/[R(R+delta)].

Both are grounded reversible networks and obey the identical input bounds.
As T tends to infinity and then delta tends to zero,

    tauU/tau0 -> R², tauL/tau0 -> R^-2, tauU/tauL -> R⁴.

Thus source normalization alone cannot remove these global powers. More
informative localized geometry, mobility or source/escape relations are needed.
This sharpness concerns the abstract CE form class. The lower completion is
not claimed to obey the packet's particular min(weight)-edge law, nor have we
constructed a fixed-unit-mobility smooth continuum realization.

## 6. General source correlations can make sharp completion hard

An exact source mass can help information while changing the optimization
class. The relaxed box-only upper is polynomial above; a sharp upper with the
additional constraint sum s=n+k is NP-hard, even for a genuine grounded
reversible network, at inverse-polynomial additive precision. This does NOT
mean extra information worsens inference: the safe unconstrained cut upper
remains available. It limits a proposed universal sharp correlation compiler.

For a CLIQUE instance on n vertices with adjacency matrix Adj and degree deg_i,
let B have off-diagonals Adj_ij and diagonal n-(2/3)deg_i. All entries are
nonnegative. Set epsilon=1/(256n³), A=I-epsilon B, and G=A^{-1}.
A is strictly diagonally dominant with negative edge off-diagonals and
positive row sums1-epsilon(n+deg_i/3), so it is exactly a grounded SPD
conductance matrix. Source s_i in[1,2] gives reversible edge rates
epsilon Adj_ij/s_i and killing rates[1-epsilon(n+deg_i/3)]/s_i.

The source constraint sum s=n+k defines a translated hypersimplex. Convexity
of s^T Gs makes its maximum occur at a vertex s=1+1_S,|S|=k. Let e(S) be the
number of graph edges inside S. Direct expansion gives

    s^T Bs=C_B+3nk+2e(S), C_B=n²+2|E|/3.

Since ||B||2<=||B||infinity<2n and ||s||²<=4n, the Neumann series yields

    q(s)=n+3k+epsilon[C_B+3nk+2e(S)]+T_S,
    0<=T_S<=16n³epsilon²/(1-2n epsilon)<epsilon/4.

The tail is nonnegative because B is entrywise nonnegative and s positive.
A one-edge difference in e(S) dominates this tail. Write
base=n+3k+epsilon(C_B+3nk). For the exact optimal mean R*,

    e_max=floor[((n+k)R*-base)/(2epsilon)].

An approximate mean with additive error<epsilon/[4(n+k)] still recovers e_max
by flooring[((n+k)Rtilde-base+epsilon/2)/(2epsilon)]. Equivalently a threshold
at q=base+2epsilon*binom(k,2)-epsilon/2 decides CLIQUE. Construction and required
precision have polynomial encoding length. Hence a universally polynomial
algorithm at this precision would imply P=NP, using the established
NP-completeness of CLIQUE as the only complexity premise.

The precision is O(n^-4), not constant accuracy. This reduction does not claim
hardness for every molecule, every local interaction class, tensor proposal,
or useful fixed-percent certificate. Exact small rational checks reconstruct
90 cases and 1,100 candidate subsets; they verify the reduction implementation,
not the complexity premise itself.

## 7. Reproduction and research status

`source_normalization_cut.py` and `correlated_source_hardness.py` use the standard
library. `refine_lower_certificate.py` uses NumPy/SciPy only for proposals, then
exact Fraction certification. All accept `--output-dir`; run in an owned scratch
directory. Reports preserve exact fractions, active cut sets and trial fields.
An independent worker reconstructs the proofs and implementation separately.

The result is a sharper finite source-aware closure and a precise boundary on
general correlated refinement. It is not a new general maximum-flow principle,
historical novelty clearance, a calibrated physical acquisition operation,
an atomistic prediction or a civilisation-enabling breakthrough.
