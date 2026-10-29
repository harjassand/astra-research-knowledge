# Independent review: metric-tree closure and complete finite witnesses

29 October 2026. New load-bearing review by the thermodynamic-alternative
agent. Reviewed `METRIC_TREE_EQUILIBRIUM_CLOSURE.md` and the written root
proof `../COMPLETE_EQUILIBRIUM_INFORMATION.md`, Sections 1–7. The only new
entropy-completion use checked was the equal-clock corollary in Section 8
of `../ENTROPY_COMPLETION_CONVERSE.md`. Prior accepted entropy material
and Astra N507 were not re-audited.

## 1. Verdict and remaining corrections

No substantive gap was found in the passive single-semigroup closure
theorem, its exact L2-strong-continuity corollary, or the new finite
entropy-witness inference. Root's written compact-bush proof provides a
complete representation route and is preferable to leaving the colored
labeling/locality argument implicit.

Two small operational hypotheses should be stated explicitly:

1. In `COMPLETE_EQUILIBRIUM_INFORMATION.md` Section 6, say **convex
   confidence region** when claiming that the joint data-law/equilibrium
   minimization remains convex. An arbitrary confidence region need not
   be convex. The joint KL objective itself is jointly convex.
2. For the eventual-detection enumeration, require a dovetailed schedule
   that revisits every valid rational certificate and makes its validation
   radius tend to zero. Increasing sample sizes alone, with arbitrarily
   shrinking failure budgets or a single validation per witness, would
   not imply this. Summable budgets can be chosen together with such a
   schedule, so this repairs the stated acquisition-completeness argument
   without changing the theorem.

Neither issue changes the closure characterization or the finite strict
separation result. T>0 may also be stated when writing the entropy/time
bounds; a strict equilibrium separator cannot depend on only one time,
since every finite-alphabet one-time distribution has an equilibrium
realization.

## 2. The compact-bush representation is sufficient

The construction in the written root proof correctly treats every rooted
partially labeled tree as an event in a copy of its underlying unlabeled
tree. It does not impose all copy-label assignments simultaneously. Leaf
consistency defines the law on the countable bush through finite connected
hulls, independently of the chosen larger hull.

The mixed-moment identity is valid. In products of empirical averages,
repeated pattern types can reuse a copy, but those collision terms have
vanishing relative count. All distinct-copy terms have the same glued
tree probability. Bounded convergence therefore gives

    E product_k M_Tk = ell(T_1*...*T_k).

Applying this identity to the square of M_T M_U-M_(T*U) makes its three
expanded terms identical glued-tree probabilities with coefficients
1,-2,1. The multiplication relation follows almost surely. A formal zero
pattern handles incompatible root labels, as the written proof states.
Root-label coordinates are actual indicators because the one-vertex
copies are the shared root itself.

Choosing the compact closed support of the coordinate law is valid:
the countably many algebra and indicator identities are continuous and
hold there. Coordinate functions separate points. Their unital algebra
is therefore uniformly dense in continuous functions and dense in L2.

The two-root bush produces symmetric edge couplings with marginal mu.
Marginal equality can be checked by all finite mixed moments; these
determine the law on the compact countable product. Disintegration gives
a reversible K_c. Pairing K_c f_T against every f_U yields the edge-prefix
coordinate, and L2 density proves K_c f_T=f_(edge_c T). Root gluing and
edge prefixing then reconstruct every finite tree pattern recursively.
Thus the proof obtains a common hidden space and kernels for all colors,
not just separate one-edge factorizations.

No additional branch independence, native cloning operation, or hidden
state preparation is needed for this mathematical representation.

## 3. Status of the original colored route

Joint separate exchangeability does imply conditional independence of
branches across all colors given the root label and color directing
measures. Test a finite branch-function product against a bounded
function of all directing records, then average independently over the
involved color families. The test function is unchanged by those finite
permutations, and distinct-index averages converge to the product of
directing integrals. Countably many colors need only finite tests.

For a fully intrinsic locality argument, define

    T_v = intersection_(finite F subset neighbors(v))
          sigma(Y_v, labels in components of U-v outside F).

This geometric branch-tail field is independent of coordinate labelings.
It contains the root and all directing measures. Conditional branch
independence and the conditional Kolmogorov zero-one law give the reverse
inclusion modulo null sets. Omitting the one branch back toward a cut
vertex proves the claimed component locality. This supplies an explicit
way to justify the draft's labeling-independent hidden record.

The root compact-bush argument avoids needing these simultaneous versions
and already proves the needed representation. No unresolved dependency
on an unstated colored extension of Aldous remains in the new root proof.

## 4. One semigroup, continuity, and finite approximation

Subdivision between arbitrary rooted patterns correctly gives equality
of <f,K_(s+t)g> and <f,K_s K_t g> on the dense branch algebra. It therefore
gives operator equality. The half-time identity makes every K_t positive
semidefinite, so unique positive roots justify K_q=K_1^q. Spectral
calculus gives positive real-time operators and the possible zero-time
projection P=1_(0,1](K_1).

That projection is a real issue without observed continuity. Vertex-iid
tree labels give iid observations at every distinct rational time and
K_t=P onto constants for all t>0. Finite reversible generators n(P-I)
approximate this law on positive-gap cylinders. It cannot be treated as
a continuous finite-rate process at zero.

Under the stated observed stochastic continuity, P fixes each sensor
indicator. Jensen plus stationarity closes the bounded range of P under
products. It contains all K_t images; recursive pattern construction then
puts the dense branch algebra in the range, forcing P=I. The claimed
exact C0 semigroup on L2(mu) follows.

The standard-Borel kernel statement is valid in its integrated, modulo-
null-set sense, which suffices for stationary hidden finite-dimensional
distributions. It does not establish one pointwise semigroup version at
every state and every real-time pair, a particular Feller topology, Hunt
paths, finite jump activity, or cadlag hidden paths. Both written notes
appropriately avoid those stronger conclusions.

For finite approximation, Poissonization converges strongly for every
positive time, including the spectral value zero. Sensor-refining finite
partitions exist and their conditional expectations converge strongly.
At fixed delta, bounded operator compression and the exponential series
give convergence of the lifted finite semigroups. The complementary
eigenvalue exp(-t/delta) disappears as the partition projections approach
I. Sensor multipliers commute with these projections, so finite word
probabilities converge. The order of choices—delta first, partition
resolution second—is sufficient; no uniform rate is inferred.

## 5. Finite LP separation and entropy constants

Compactness correctly turns failure of the full tree extension into
failure of a finite subsystem. Its projection to finitely many path
coordinates is a rational polytope, so a strict rational separator exists.
Taking the union of the finite observation grids turns it into one bounded
word score. Reducible equilibrium mixtures are allowed; the stated small
stationary refresh also makes the irreducible-closure claim valid.

The new additive-reversibilization comparison has the correct constants.
Q and A=(Q+Q*)/2 share pi and escape rates, so their stationary path KL is
T times the unaveraged flux-pair Jensen-Shannon bracket. The inequality

    B(f,g) <= (f-g)log(f/g)/4

is valid, with the stated derivative proof and locally sharp coefficient.
Pinsker therefore yields sigma>=8 gamma^2/(T L^2). The distinction from
the conventionally averaged probability Jensen-Shannon divergence is
handled correctly.

The time-symmetric linear transfer also checks: both the path mixture
(P_Q+P_Q*)/2 and P_A dominate the geometric path measure. Their TV distance
is at most its missing mass. The path Jeffreys/Hellinger inequality bounds
that deficit by T sigma/4, giving sigma>=4 gamma/(T L). The proof does
not confuse a mixture of path laws with the law of a mixed generator.

For a finite relaxation C_m(G), additive reversibilization supplies a
feasible equilibrium comparison r_A. Thus min_r D(p_G||r)<=T sigma/4,
giving the claimed convex information-distance lower bound. Nested
compact feasible sets and KL lower semicontinuity justify convergence of
the minima. The robust envelope is zero on equilibrium closure and
strictly positive outside it by the persistent finite witness margin.
No exact-record minimizer or optimal numerical entropy bound is implied.

## 6. New equal-clock corollary only

The new Section 8 of `ENTROPY_COMPLETION_CONVERSE.md` is correct. Equal
escape rates at parity partners force delta=0 in the exact-attainment
dwell argument. Conversely, delta=0 gives h=1 in the reversed phase-type
construction, preserving every paired escape rate. Constant directional
duration ratios are therefore the finite-attainment criterion in this
class. The already established paired Erlang approximations obey equal
clocks, so their closure floor is unchanged. This check does not extend
the thermodynamic interpretation beyond the stated reversal contract.

## 7. Scope of this review

The proofs establish a passive single-semigroup characterization and a
complete finite family for detecting a strictly positive robust entropy
floor in the declared all-even model class. They do not acquire the tree
extension, identify microscopic parity, construct a common control
family, or provide a useful state, clock, mixing, precision or sample
complexity bound. No control counterexample was needed to expose a flaw
in the passive theorem. Priority of the assembled result was not audited.
