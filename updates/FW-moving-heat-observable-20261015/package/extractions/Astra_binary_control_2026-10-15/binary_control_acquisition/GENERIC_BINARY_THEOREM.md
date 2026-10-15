# Generic exact binary acquisition by response-field generation

Status: a mathematical construction with a polynomial number of exact scalar queries, but potentially exponential or worse offline symbolic work. No practical acquisition schedule, uniform finite-noise bound, priority, or hardware advantage is established. This does not modify the existing noisy obstruction or the measured-data gate.

## Binary interface and normalization

Write the normalized binary map, for S contained in [m], as

    f(S) = f0 - g_S,
    g_S = a_S^T (I + B_SS)^(-1) 1,
    B_ii = 0.

This follows from the supplied fixed-amplitude resolvent normalization whenever its diagonal normalization factors are nonzero. The binary map itself is the target. No prediction between binary states, original diagonal self-terms, or physical directed-edge recovery is needed. Restrict to parameters for which all 2^m binary inverse matrices exist. This is a nonempty Zariski-open condition, since B=0 satisfies it. Baseline gives f0; singleton queries give g_{i}=a_i.

For a symbolic generic matrix B and symbolic a, let k=Q(a_1,...,a_m), K=k(B_ij : i != j), and

    L = k(g_S : S contained in [m]).

The g_S are explicit rational functions in n=m(m-1) independent B entries over k. Their numerator and denominator degrees in B are at most m: use the adjugate and determinant. The actual unknown a and B need not be rational; rational symbolic formulas apply to generic real or complex parameter values.

## The theorem

For each m>=2, there is a deterministically computable list of actual binary configurations, depending only on m, with at most

    Q <= 1 + m + n + floor(n log_2 m),   n=m(m-1),

queries, from whose exact scalar readings every binary response is recoverable by rational functions on a nonempty Zariski-open parameter set. A sharper count is

    Q <= 1 + m + r + floor(log_2 D),
    r = trdeg_k L <= n,
    D = [L : k(g_{S1},...,g_{Sr})] <= m^r,

for the transcendence-basis configurations chosen below. Query counts count distinct settings, and the stated bound can be replaced by min(Q,2^m).

The reconstruction need not identify B, even up to weighted transpose. It identifies its complete binary response table. Rational reconstruction formulas may have huge degree and size and may be arbitrarily poorly conditioned. All computation, exact-number precision, switching, settling, reset, and model-validity requirements remain charged.

## Proof of the finite-extension degree bound

A general lemma suffices. Let h_1,...,h_N be rational functions of n independent variables over an infinite characteristic-zero field k, with numerator and denominator degrees at most d. Let L=k(h_1,...,h_N), and let h_1,...,h_r be any maximal algebraically independent subset among these functions. Put F=k(h_1,...,h_r). Then L/F is finite and

    [L:F] <= d^r.

To prove this, consider the dominant rational map from affine n-space to the irreducible output variety whose function field is L. Its generic fiber has dimension n-r. A sufficiently general affine linear subspace E of dimension r meets the generic fiber in a nonempty finite set, so restriction to E is still dominant. One justification is to intersect successively with generic affine hyperplanes: at every stage of positive-dimensional generic fiber, a generic hyperplane cuts that fiber properly and nontrivially; after n-r cuts its dimension is zero. The choice can be made over k because k is infinite; equivalently first work with generic coefficients and then specialize off the finitely many bad algebraic conditions.

Restriction therefore embeds L into k(E), and the algebraically independent chosen h_1,...,h_r give a generically finite rational map E -> affine r-space. For generic target values y_j, its finite fiber is cut out by

    N_j(z) - y_j D_j(z) = 0, j=1,...,r,

each of degree at most d, away from all denominator-zero sets. Affine/projective Bezout bounds the number of isolated solutions, with multiplicity, by d^r. Characteristic zero makes the generic field extension separable. Consequently [k(E):F] <= d^r, and the tower law yields [L:F] <= d^r. Base-locus components of the cleared equations do not increase the number of isolated solutions away from denominators; use the saturation by their product if needed. For r=0, the only rational functions in k(x) algebraic over k are in k, so L=k and D=1.

Apply the lemma with d=m and n=m(m-1).

## Constructive selection of configurations

All steps in this paragraph are offline symbolic operations, not plant measurements.

1. Enumerate all 2^m explicitly known formal rational functions g_S using symbolic a and B. Scan them in a fixed order. Retain a function exactly when it is algebraically independent over k of the retained ones. Algebraic independence is decidable by elimination or the Jacobian criterion in characteristic zero. At the end there are r retained configurations. Their functions form a transcendence basis F, and L/F is finite.
2. Start E0=F. Scan the remaining functions. Whenever g_S does not lie in the current field Ej, retain its configuration and enlarge Ej+1=Ej(g_S). Field membership is an exact symbolic question, decidable by rational-function field algorithms/elimination. Because every element is algebraic over F, a genuine enlargement has [Ej+1:Ej]>=2. Hence [L:Ej+1] <= [L:Ej]/2. There can be at most floor(log_2 D) such enlargements. After the finite scan, all generators lie in the final field, which is therefore L.
3. For each target S, compute a rational expression g_S=R_S(a, selected g)/T_S(a, selected g), with T_S not the zero field element. Existence follows from field equality. Even a brute-force enumeration of polynomial pairs R,T and exact symbolic identity tests terminates, so no unproved efficient algebraic subroutine is required to assert computability. A more useful implementation would use elimination and rational inversion.
4. Only now measure the baseline, m singletons, and selected configurations. Insert the acquired values into the precomputed rational expressions.

The step-2 membership test can also be implemented by computing the degree of the generically finite graph projection before and after adjoining a generator; equality of fields means relative degree one. This is computable by Groebner bases over the function field, even though its resource cost may be enormous.

For every target, the symbolic denominator T_S is nonzero. Pulling back its zero locus to parameter space gives a proper algebraic exceptional set. There are finitely many targets and arithmetic denominators. Excluding their union and the physical inverse/normalization singularities leaves a nonempty Zariski-open set where all formulas hold simultaneously. This proves exact generic prediction of ALL binary configurations, rather than merely a finite candidate model or a parameter-count heuristic.

## What this establishes and what it does not

- Every actual oracle call is binary. No second nonzero actuator amplitude and no arbitrary-field oracle query is smuggled in. Arbitrary field values occur only in offline symbolic algebra.
- A polynomial measurement-count theorem exists for generic exact binary prediction, without resolving the proposed two- or three-anchor Schur-complement construction.
- The generic set is specified implicitly by finitely many nonzero algebraic conditions. It is not a known uniform separation margin or a test of the supplied physical premises.
- This construction may enumerate all 2^m targets offline and may perform much more computation. It is not a polynomial-time learner, a practical closed-form schedule, or an improvement over fitted rational models.
- The theorem permits the same generic real normalized parameter domain as the original model. A particular reciprocal or other lower-dimensional physical subclass should instead be parameterized and the field construction rerun on that irreducible family; genericity in the ambient unrestricted family does not certify membership of that subclass.
- Nongeneric low-order/fixed-anchor failures remain valid. Likewise, arbitrarily close generic perturbations can retain severe finite-precision indistinguishability. The proof relies on exact equality, rational field membership, and potentially badly conditioned rational inversion. It supplies no uniform noise robustness, precision cost, or favorable finite-noise stopping time.
- Existing physical binary-metasurface rational-model fitting remains the strong comparator. This theorem supplies an exact query-complexity statement and a logically complete, impractical symbolic acquisition operation; it establishes no novel scalar-control hardware capability.

## Relation to anchor-context schedules

The proposed schedule measuring all configurations of a constant anchor set together with at most two other activated controls is not universally sufficient. Use the normalized three-node pair-switch example from N854 section 3, detailed with exact rational responses and accretivity checks in AUDIT.md. Place that block outside the anchors and disconnect it from them. All acquired configurations see at most a pair from the block and therefore agree, while the full three-node response differs. This refutes universal anchor-schedule identification within the nonsingular normalized family, not generic identification. It does not refute the theorem above, whose symbolically chosen settings can have arbitrary support. The earlier directed-cycle citation was unsuitable because that example had a singular gauge; the pair-switch example corrects it.
