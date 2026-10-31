# Scalar prediction needs an exit and a return

31 October 2026. Follow-up to the measured closure certificate in
`geometry_acquisition.md`. This note proves the quadratic task-error bound,
its exact adjoint requirement, sharpness in the common-stationary bounded-report
case, and its effect on experimental precision. It does not acquire a subspace
or an efficient planner by assumption.

## 1. The operator statement

Let P be an orthogonal projection on a real or complex Hilbert space and
Q=I-P. Let T_1,...,T_H be contractions; their order is chronological, so the
full word is U=T_H...T_1. Write S_i=P T_i P and

    a_i = ||Q T_i P||,
    b_i = ||P T_i Q|| = ||Q T_i* P||.

Then

    ||P T_H...T_1 P - S_H...S_1||
       <= sum_(1<=i<j<=H) a_i b_j.                         (1)

In particular, if every primitive is self-adjoint, a_i=b_i=e_i and

    ||P T_H...T_1 P - S_H...S_1||
       <= sum_(i<j) e_i e_j
        = [(sum_i e_i)^2-sum_i e_i^2]/2
       <= H(H-1)e^2/2                                    (2)

when e_i<=e. No commutativity is needed, and the product itself need not be
self-adjoint. For unit vectors f,g in range(P), the same bound applies to

    |<g,T_H...T_1 f>-<g,S_H...S_1 f>|.

For H=1 the closure contribution is exactly zero. The universal bound may be
capped at two, since both compared compressed operators are contractions.

### Proof

Insertion of the first omitted projection, starting from the input end,
gives the exact identity

    P T_H...T_1 P - S_H...S_1
      = sum_(i=1)^(H-1)
          P T_H...T_(i+1) Q T_i P S_(i-1)...S_1.          (3)

The empty compressed prefix is P. This is ordinary product telescoping:
(T_i-S_i)P=Q T_i P, and the i=H term vanishes after left multiplication by P.

For the suffix, adjointing yields

    ||P T_H...T_(i+1) Q||
       = ||Q T_(i+1)*...T_H* P||
       <= sum_(j=i+1)^H b_j.                              (4)

To prove (4), propagate a norm-at-most-one vector initially in range(P)
backward through T_H*,...,T_(i+1)*. At step j, its Q component has norm at
most the preceding Q norm plus ||Q T_j* P||=b_j, because all operators are
contractions. The same argument works in operator norm, applying it to every
initial unit vector in range(P).

Each compressed prefix in (3) is a contraction. Taking norms in (3), using
||Q T_i P||=a_i and (4), gives (1). Self-adjointness identifies the two
leakages and gives (2).

The mechanism is explicit. An error invisible to a readout in P must first
leave P and subsequently return. The two factors are forward leakage and
adjoint leakage. Bounding the full state-vector error before applying the
readout discards this second factor and gives the unnecessarily linear He
bound for this task.

## 2. Seed and readout projection errors

Exact containment is not required, but its replacement must be charged.
Put

    p_f=Pf, q_f=Qf, alpha=||q_f||,
    p_g=Pg, q_g=Qg, beta=||q_g||.

Then

    |<g,Uf>-<p_g,S_H...S_1 p_f>|
      <= ||p_f||||p_g|| sum_(i<j) a_i b_j
       + beta ||p_f|| sum_i a_i
       + alpha ||p_g|| sum_i b_i
       + alpha beta.                                     (5)

Proof: decompose the scalar into its PP, QP, PQ, and QQ contributions.
The PP term is bounded by (1). Forward propagation gives
||Q U P||<=sum_i a_i. The adjoint version gives
||P U Q||<=sum_i b_i. Finally ||Q U Q||<=1. These four bounds prove (5).

For self-adjoint primitives and unit-norm f,g, a convenient upper bound is

    sum_(i<j)e_i e_j + (alpha+beta)sum_i e_i + alpha beta. (6)

Thus small seed/readout projection debts can also combine quadratically;
the conservative alpha+beta estimate is not always necessary. This does not
allow an arbitrary unrepresented readout for free. For H=1, P onto e_1,
T=[[0,e],[e,0]], f=e_1, g=e_2, the true scalar is e while the projected
scalar is zero. Here beta=1 and the beta*a_1 term is necessary. The alpha*beta
term is also necessary: take T=I and f,g with aligned Q components.

## 3. Non-self-adjoint actions require the reverse leakage

Equation (1) already handles arbitrary contractions if both a_i and b_i are
acquired. In an alphabet closed under genuine adjoints, a measured forward
leakage bound for T_a* supplies the needed b_a. For a word of primitives,
use the ordered products a_(a_i) b_(a_j), i<j. A common bound e on the
forward leakages of both the actions and their adjoints restores (2).

Forward leakage alone is insufficient. On R^2 with P=diag(1,0), take

    T_1 = [[0,0],[e,0]],
    T_2 = [[0,1],[0,0]],     0<e<1.

Both are contractions. Their forward leakages are a_1=e and a_2=0.
But b_2=1, and

    <e_1,T_2 T_1 e_1> = e,
    <e_1,(P T_2 P)(P T_1 P)e_1> = 0.

The correct ordered bound a_1*b_2=e is attained. Replacing b_2 with a_2
would falsely give zero; using only max a_i=e would falsely give e^2.

The adjoint extension is algebraic, not an assertion that adjoint
experiments are cheap. Weighted return implementations retain their actual
word-dependent report ranges, numerical weights, preparation costs, and
depths. The fixed bounded-report common-stationary case stays distinct.

## 4. Sharpness with physical reports in [-1,1]

The leading constant H(H-1)/2 cannot be improved uniformly, even for a
single self-adjoint Markov primitive and a two-dimensional reachable space.

Take a uniform state (x_1,x_2) in {+1,-1}^2. Let S swap the two coordinates
and let

    T_e=(1-e)I+e S,   0<e<=1/2,
    f(x)=x_1, h(x)=x_2,   P=projection onto span{f}.

The functions f,h are orthonormal in L2 of the common stationary law and
are each bounded by one. The kernel T_e is a symmetric Markov contraction.
On the cyclic span of f,h,

    T_e = [[1-e,e],[e,1-e]],
    ||Q T_e P|| = e,
    P T_e P = (1-e)P.

The true and reduced scalar responses are

    <f,T_e^H f> = [1+(1-2e)^H]/2,
    <f,(P T_e P)^H f> = (1-e)^H.

Their difference D_H(e) satisfies

    binom(H,2)e^2(1-e)^(H-2)
       <= D_H(e) <= binom(H,2)e^2.                        (7)

The lower bound follows by expanding ((1-e)I+e S)^H: after subtracting the
zero-swap term, only even positive numbers of swaps contribute, and the
two-swap term is the displayed lower bound. The upper bound is (2).
For H=2 equality holds exactly. For any fixed H, the ratio in (7) tends to
one as e decreases to zero. More quantitatively, that ratio is at least
1-(H-2)e, so the bound is nearly sharp throughout the small-He regime.

This is a literal common-stationary physical source. Each episode prepares
a fresh uniform pair, performs H identity-or-swap primitive transitions, and
reports f(X_0)f(X_H) in {-1,+1}. No report rescaling, hidden normalization,
or weighted adjoint is needed.

Sharpness here concerns the projection-error inequality, not the statistical
cost of identifying this particular two-state cyclic model. An ordinary
learner given that family promise can infer e from one-step flip counts,
whose success probability is e/2, and exploit their small variance. The
generic residual-certification bill below is not asserted optimal for this
special family.

## 5. What changes in the acquired Gram certificate

Let an actually acquired word frame V define P, with measured

    G=V*V, K_a=V*T_a V, L_a=(T_a V)*(T_a V).

The earlier two-coordinate certificate proves

    ||Q T_a P||^2 <=1024 zeta

from entrywise moment uncertainty zeta and its explicit Gram-margin,
coefficient-norm, and residual tests. It also pays for constructing V; this
lemma does not supply a useful frame. For self-adjoint primitives the same
measurement bounds the reverse leakage. Therefore its contribution to every
scalar task of horizon H is now at most

    512 H(H-1) zeta.                                    (8)

Taking

    zeta = epsilon/(4096 H^2),

makes (8) at most epsilon/8. The earlier numerical fit bounds add at most

    64 zeta+256H zeta <=5epsilon/64

for H>=1. A separate epsilon/4 budget for guarded matrix computations is
still sufficient. The frame tests continue to require zeta<=1/4096, which
this choice satisfies for epsilon<=1. On the exact reflection family, the
same termination proof for the validation tests continues to apply.

For a report bound B, a new scalar entry costs

    O(B^2 zeta^-2 log(Q/delta))
      = O(B^2 H^4 epsilon^-2 log(Q/delta))

shots, including the report-rounding allocation. The previous linear-state
analysis used zeta=O(epsilon^2/H^2), giving epsilon^-4 instead. This is an
actual experimental precision improvement for the scalar task. It does not
improve the separate cost of finding the frame or an unrelated planner.

For the two-coordinate frame (f,R^q f), there are at most 17 distinct entries
before cache reuse, and every return has length at most 4q+2. Thus multiply
the scalar-shot bill by its actual return depth and add one stationary
preparation and the endpoint readouts for every episode. Precision now needs
O(log(H^2/epsilon)) fractional bits, together with the acquired Gram inverse
bound. All unsuccessful candidate frames and residual tests remain charged.

For a general non-self-adjoint action, the adjoint residual is measured from
the actual vectors T_a* V. With K_a=V*T_a V, its raw matrix is

    (T_a*V)*(T_a*V) - K_a G^-1 K_a*.

Whitening by G^-1/2 gives b_a^2. Forward and adjoint residual measurements
must both be included in the cost before applying (1).

## 6. Errors that remain first order

Suppose the true compressed operators S_i and learned operators S_hat_i are
all contractions in the acquired geometry, with
||S_i-S_hat_i||<=xi_i. Product telescoping gives an additional

    sum_i xi_i

error for unit seeds and readouts. In-span seed/readout estimation errors
also add linearly after norm clipping. These are separate from the projection
debts in (5). For H=1 and P=I, replacing T=I by (1-xi)I already creates
scalar error xi despite zero projection leakage. A blanket claim that every
estimation error becomes quadratic would be false.

The theorem is uniform over arbitrary later words when the action and adjoint
leakage certificates hold simultaneously. It does not give an efficient
algorithm for optimizing a word over exponentially many candidates. A supplied
word can be evaluated with the acquired compact matrices; planning still
requires its own constructive algorithm and bill.

## 7. Relation to ordinary reduced-model methods

The mathematical principle has strong established relatives. Ordinary
primal-dual output estimates use a product of primal and dual residuals,
and projection memory formulas contain both an exit and a return coupling.
No novelty claim is made for this general principle. The useful refinement
here is the explicit all-word contraction bound, its acquired scalar-Gram
certificate, and the resulting precision change for this information contract.

Primary sources inspected:

* Feng, Chellappa, Benner, *A posteriori error estimation for model order
  reduction of parametric systems* (2024),
  <https://link.springer.com/article/10.1186/s40323-024-00260-8>.
  Their discussion and proofs explicitly use quadratic primal-dual residual
  products. They work with specified discretized systems, projection matrices,
  and appropriate dual problems; some bounds require symmetry/positive
  definiteness or inverse conditioning. The displayed equation (24) and its
  proof differ in how the inverse-matrix norm is printed, so no numerical
  constant is imported. The elementary proof above is independent.

* Harlim and Li, *Parametric Reduced Models for the Nonlinear Schrodinger
  Equation*, Phys. Rev. E 91, 053306 (2015), accepted manuscript
  <https://link.aps.org/accepted/10.1103/PhysRevE.91.053306>.
  Equations (2.7)-(2.10) state the exact Mori-Zwanzig projected equation and
  its orthogonal dynamics/memory terms. They emphasize that this exact identity
  itself does not make estimating or evaluating the memory cheap. Their reduced
  NLS models use a physical ansatz and noisy low-mode observations, a different
  acquisition interface from the present return-Gram source.

## 8. Executable checks

`quadratic_scalar_closure_check.py` verifies the sharp Markov example with
exact rational arithmetic, preserves the non-self-adjoint forward-only
counterexample, checks the boundary and in-span-fit limitations, and performs
finite-matrix numerical checks of (1) and (5). The random matrix checks are
diagnostics; the proofs do not rely on them. No hidden-coordinate data is
provided to an acquisition algorithm by these theorem checks.
