# A crossing-count bound for a native killed local race

Contributor: `/root/cycle11_composition`.
Scientific date: 23 October 2026. This is a new finite inequality, not a claim
that the complete Cycle11 phase problem is closed.

## 1. Exact scope and consequence

The original native graph need not be a tree, layered, acyclic, symmetric, or
strongly lumpable. The following result keeps the number of **accepted local
jumps** and allows arbitrary fan-in, fan-out and revisits. It retains actual
local rejection/holding probabilities by integrating them out in a race against
a fixed killing hazard. Its optimized bound is the same crossing cost that
appeared in the restricted forward-control theorem, but is now a finite
operator bound for any reciprocal native proposal.

This is not yet a bound for the sum of all first-hit crossing counts. Nor does
it silently replace the actual independence-MH moves within the low-weight
set by holds. Those two interfaces remain explicit below. It is a proof
operation, not a new sampler or a free access primitive.

## 2. Definitions

Let X be a finite set, q_x>0, and Q a row-stochastic matrix with reciprocal
off-diagonal support. Let 0<eta<1 and d>=0. For x!=y with Q_xy>0 put

    r_xy = q_y Q_yx / (q_x Q_xy).

Let accepted local probabilities be L_xy=Q_xy a_xy, where

    0 <= a_xy <= min(1, exp(d) r_xy^eta).

This bound holds for the actual Cycle11 two-stage Hastings acceptance with
d=|kappa-eta| A. The theorem does not require any additional target table or
target normalizer. Target reversibility of L, though true in the native class,
is not needed for this particular inequality. Put

    o_x = sum_{y!=x} Q_xy a_xy <= 1,
    L_xx = 1-o_x.

Fix r>0 and define a substochastic off-diagonal matrix

    M_xy = Q_xy a_xy/(r+o_x),   x!=y,
    M_xx = 0.

Its row sum is o_x/(r+o_x); missing mass is killing. This is exactly the
embedded accepted-jump kernel of the following discrete race. At an attempt,
kill with probability k>0, use the actual local kernel L with probability
l>0, and otherwise hold, where k+l<=1 and k/l=r. At state x the probability
that the next event other than a hold is the jump x->y is

    l L_xy / (k+l o_x) = M_xy.

Thus all local rejection and common laziness are paid through the denominator
r+o_x. No rejected row is normalized to one. At every visited state the next
non-hold event occurs almost surely because k>0. The same formula works when
the killing ratio r_x is state dependent with r_x>=r, by entrywise domination.

One may remove any desired off-diagonal transitions after forming M, to count
first hits or paths avoiding prescribed sets. The resulting matrix is bounded
entrywise by M and inherits all upper bounds below.

## 3. Exact conjugated operator inequality

For 0<c<1 set theta=c eta, p=1/(1-theta), and D=diag(q^theta). Define

    h(a)=log(1+r exp(a)),  a>=0,
    V_c=exp(dc) sup_{a>=0} exp(c a-h(a)).

Then for every nonnegative row vector v,

    ||v D M D^-1||_p <= V_c ||v||_p.                  (A)

There is no factor 2^(p-1), support-size constant, minimum-atom constant, or
assumption that Q has a known invariant law. The same bound for signed vectors
follows from positivity.

### Proof

At output y use reverse-proposal Jensen coefficients Q_yx over x!=y. Their
sum is at most one. Add a dummy zero term to make the coefficients sum to
one. If T=D M D^-1, Jensen gives

    (sum_x v_x T_xy)^p
      <= sum_{x!=y} v_x^p T_xy^p / Q_yx^(p-1).

Zero edges contribute zero. Direct calculation, using p-1=theta p, gives

    T_xy^p / Q_yx^(p-1)
      = Q_xy a_xy^p r_xy^(-theta p)/(r+o_x)^p.

The screen inequality gives, for a_xy>0,

    a_xy^p r_xy^(-theta p)
      <= exp(dc p) a_xy^[p(1-c)].

At a_xy=0 the original term is zero. Put tau=p(1-c). Since eta<1,
0<tau<1 for 0<c<1. Concavity of z^tau, with all unused row weight assigned
the value zero, yields

    sum_{y!=x} Q_xy a_xy^tau <= o_x^tau.

Rows with o_x=0 are zero. Summing the output bound over y gives

    ||vT||_p^p
      <= exp(dc p) sum_x v_x^p o_x^[p(1-c)]/(r+o_x)^p
      <= [exp(dc) sup_{0<z<=1} z^(1-c)/(r+z)]^p ||v||_p^p.

Writing z=exp(-a) identifies the bracket with V_c. This proves (A).

The endpoints are legitimate limits. At c=0, p=1, the row-sum bound is
||vM||_1 <= ||v||_1/(1+r), equal to V_0. At c=1, theta=eta<1, one can
either take limits from below, or use the screen bound directly: the row
term is at most exp(dp)/(r+o_x)^p times the sum of positive-edge Q weights,
and hence at most (exp(d)/r)^p. Thus V_1=exp(d)/r is valid, with its scalar
supremum approached as a tends to infinity. No 0^0 convention is needed.

## 4. Fixed-crossing transport bound

Let A,E be any subsets with b=q(A)>0, e=q(E)>0. Start with the actual
restricted initial subprobability q1_A. For every integer J>=1,

    (q1_A M^J)(E)
      <= b exp[-J h((eta log(b/e)/J-d)_+)].            (B)

If desired cap this by b or by the trivial total surviving mass. The formula
also bounds first arrival in E at accepted-jump count J: kill any previous
visits to E before the last multiplication. It does not require A and E to be
disjoint for the unrestricted landing event; first-hit applications use them
disjoint. Empty sets are handled directly as zero.

### Proof

The transformed initial vector is q1_A D^-1=q^(1-theta)1_A. Its pth-power
norm is b because p(1-theta)=1. Iterating (A) J times and then applying
Holder on E gives

    (q1_A M^J)(E)
      <= b^(1-theta) e^theta V_c^J
      = b exp[-c U + J sup_{a>=0}{c(d+a)-h(a)}],
    U=eta log(b/e).

This remains true if transitions were removed to enforce first arrival.
Optimize over c in [0,1]. The optimization can be checked without invoking
a duality theorem. For z=U/J-d>=0, take c=h'(z)=r exp(z)/(1+r exp(z)).
Strict convexity of h makes a=z the unique scalar maximizer, so the exponent
is -J h(z). Convexity also implies every other c gives at least that value.
If z<0, c=0 gives -J h(0); for every c>=0 evaluation of the scalar supremum
at a=0 gives an exponent at least -J h(0)-J c z >= -J h(0). Hence the
minimum is -J h(z_+) in all cases. This proves (B).

The result is a genuine arbitrary-geometry statement for a **fixed crossing
count**. In particular merging and cycles cannot improve that fixed-count
source-to-boundary bound. The reverse-Q row budgets, not a presumed directed
progress coordinate, provide the required multiplicity control.

## 5. What the theorem does not prove

The full first-hit probability is a sum over J of nonnegative terms. Applying
(B) separately with the entire source mass b at every J gives only the valid
but generally loose bound

    P_q(hit E before killing)
      <= min{b, sum_{J>=1} b exp[-J h((U/J-d)_+)]}.

Replacing that SUM by MAX requires another argument. First-hit events are
disjoint under the forward probability law, but the reverse-Q path measures
used by Jensen are not automatically disjoint across J. Starting from q1_A
at every A vertex makes this especially important. No artificial allocation
b_J with sum b_J<=b is assumed here.

The original native C also has independence-MH transitions **inside** A.
They are not just holds in arbitrary geometry. Formula M exactly integrates
local holds against a constant kill, not those additional moves. The native
global killing rate into A^c is constant from A={W<h}, but that fact alone
does not license removal of within-A G transitions. A full-chain reduction
must pay them, direct global hits, and all original-chain post-hit returns.

No step in (A)-(B) modifies the native sampler, spends a second KL budget,
claims practical speedup, or turns a proof counter into an oracle. The ordinary
IMH comparator remains unchanged.

## 6. Relation to accepted source and current continuation

Read and used:

- Cycle10 CRITICAL_TRANSPORT_THEOREM.md Sections 2 and 6: the already closed
  restricted forward-control value and the explicit missing native reduction.
- The actual Cycle8 ASYMMETRY_BUDGET_THEOREM.md Sections 3-4: reverse-Q Jensen,
  accepted-outflow subtraction, and original-chain first-hit scope.

New operation: integrate **actual local holds** before conjugation. This
removes the factor from adding the rejection diagonal to the reverse-Q
counting column and gives a crossing-count operator inequality with an exact
scalar convex dual. It neither improves nor disputes the previously accepted
full-chain energy theorem.

Continue at the remaining scientific interface: couple different crossing
counts with their shared source and boundary budgets, and account for internal
global moves. A power inequality at one c cannot by itself decide whether
the unrestricted class can fill the known native phase troughs.

No computation, old fixture replay, native graph materialization, target call,
new primary-literature claim, or external delivery was performed for this
bounded lemma. Total inference and discovery costs are unavailable.

## 7. Bounded challenge of the subsequently proposed native path bridge

The principal communicated a different, stronger construction after (A)-(B)
were derived: tag transitions and reverse their proposal path measure. I
checked that proposal at its two load-bearing interfaces, not a complete
future principal proof. The following observations identify exactly what was
checked.

For an actual finite first-hit path from A={W<h} to E subset A^c, tag each
off-diagonal move by its global or local mixture component and keep the
combined actual diagonal. Define auxiliary reversed coefficients by

    local:   beta Q_yx/2,
    global:  alpha q_x/2,
    diagonal: C_xx.

The auxiliary coefficient matrix has row sums at most 3/2: the actual
diagonal is at most one and each of the two off-diagonal proposal rows has
mass at most its mixture share. Its coefficients are proof weights, not a
Markov kernel, and must not be renormalized.

Multiplying a tagged path's probability by q at its initial endpoint, then
dividing by q at its terminal endpoint and by the reversed auxiliary path
weight, leaves the factor a_xy/r_xy at each local move, the ordinary IMH
acceptance at each global move, and one at each diagonal. Thus, with local
signed progress x_xy=-eta log(r_xy), the product is at most
exp(sum_local x_xy/eta). If signed progress is less than U, summing all
lengths j<=N and all reversed paths gives at most

    3 q(E) exp(U/eta) (3/2)^N.

This counts the full native multiplicity. Reverse paths may fail the forward
first-hit restriction; removing that restriction only enlarges the upper.

For the complementary high-progress paths, replace negative local increments
by zero. A positive increment x has actual acceptance at most
sigma(x)=exp[-(x-d)_+]. Use control shares

    t_y=Q_xy a_xy/sigma(x_xy)   for x_xy>0,

whose sum is at most one. From A every global proposal into A^c is accepted,
so its killing probability is exactly alpha(1-b)/2. The local coefficient is
beta/2. These agree with the closed control after common thinning with
lambda=[beta+alpha(1-b)]/2 and r_b=alpha(1-b)/beta.

Internal global moves, negative/zero-progress local moves and actual rejections
are history-bearing holds. They may change the state and therefore the next
choice of outgoing control. This is allowed by the already proved control
theorem, which permits choices after holds based on the full history. If a
local move hits A^c outside E before completion it can be terminated as an
extra failure; adding such failures cannot increase success. If the final
first hit of E is global, it contributes zero progress, so high accumulated
progress means the threshold was already reached strictly before that global
exit. If the final hit is local, that move can be the completing crossing.

With these qualifications, I found no flaw in the proposed event/control
mapping. It potentially resolves both gaps left by the per-J inequality:
shared source/boundary mass is handled by a single path partition, and actual
internal global moves are retained as history-bearing holds rather than
deleted. Acceptance of a complete all-class phase theorem still requires the
principal to state and check the cutoff error, one-KL allocation and original
post-hit-return interface. This subsection is a bounded challenge record,
not a substitute for that complete proof or its source-bound review.
