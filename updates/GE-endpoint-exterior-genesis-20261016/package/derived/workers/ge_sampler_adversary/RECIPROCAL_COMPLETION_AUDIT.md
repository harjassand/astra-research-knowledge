# Focused audit of the reciprocal-rate boundary completion

Audited source: `root/RECIPROCAL_RATE_METRIC.md`, hash pinned separately in
`reciprocal_completion_sources.json`. This is a continuation of the independent
proof audit. Prior frozen files were not edited. Historical priority and
external correctness remain UNKNOWN.

**Finding: no mathematical blocker found in the completion, averaging
identification, quantum lift, or stated upper-budget optimization.** The
identification with averaging needs only one fixed-ratio comparison path;
the reciprocal Lipschitz estimate then handles every other approach, including
arbitrarily diverging ratios. A boundary extension need not be injective.

## 1. Precise completion statement and its proof

Fix the finite positive physical edge support E, its connected components C,
and T>0. Write theta_e=1/r_e. Let

    D_T(theta,eta)=sum_C c_C^2/T * max_(e in C)|theta_e-eta_e|,
    c_C=|C|(|C|-1)/4.

For nontrivial components this is a norm on their reciprocal coordinates;
isolated vertices have no edge coordinates. The source theorem says that the
map from theta in (0,infinity)^E to the endpoint kernel is 1-Lipschitz from
D_T to max_sigma TV of kernel rows. This is a finite product of finite
probability simplices and is complete in that kernel norm.

The domain's closure for finite reciprocal coordinates is [0,infinity)^E.
For any boundary theta*, take theta^(j)>0 converging to theta*. The Lipschitz
inequality makes the endpoint kernels Cauchy, hence convergent. If eta^(j) is
another such approach, the distance between the two endpoint kernels is at
most D_T(theta^(j),eta^(j)), which tends to zero. The limit is therefore
independent of approach. Define the extension by that limit. Applying the
same inequality to sequences approaching two arbitrary boundary points
proves the original Lipschitz bound on the closed domain. Uniqueness follows
from density of the strictly positive domain and continuity.

This proof is uniform over all initial permutations; it does not silently
pass from a pointwise-in-initial-state limit to a uniform kernel limit.
The finite initial-state set would also permit that passage, but the source
bound already supplies it. Common initial mixtures and fixed color maps
remain contractions under this completion.

This is completion of the reciprocal parameter domain and extension of its
endpoint map. It is not a claim that distinct boundary vectors produce
distinct endpoint laws, nor that the upper bound is an isometry. For example,
on the triangle, zero reciprocal coordinates on edges 01 and 12 already make
the whole graph one infinite-rate block. Every positive finite reciprocal
coordinate on edge 02 then gives the same uniform full-permutation endpoint.
The exact checker verifies the projection identities for this example.

## 2. Identification with exact averaging, without a ratio assumption

Let Z={e:theta*_e=0}. Its positive edge graph defines the actual fast
components. Put rate one on every edge of Z, forming the full interchange
positive generator A, and put rates 1/theta*_e on E minus Z, forming B. For
the comparison path

    r_e(W)=W on Z,    r_e(W)=1/theta*_e otherwise,

the kernel is exp[-T(WA+B)]. Let Pi be orthogonal projection onto ker A.
Because the transpositions of every connected graph generate its symmetric
group, Pi averages uniformly over independent permutations within the actual
fast components, including singleton components.

An elementary finite-dimensional estimate independently identifies this path's
limit. Let Q=I-Pi and let lambda>0 be the smallest eigenvalue of A on ran Q,
when Q is nonzero. Set u_W(t)=exp[-t(WA+B)]f. Both A and B are symmetric
positive semidefinite. The energy identity gives

    integral_0^T ||Q u_W(t)||_2^2 dt <= ||f||_2^2/(2W lambda).

Projecting the evolution onto ker A and using variation of constants gives

    ||Pi u_W(T)-exp[-T Pi B Pi]Pi f||_2
      <= ||B||_2 sqrt(T) ||f||_2/sqrt(2W lambda).

The Q equation has positive generator W A|_Q+Q B Q, at least W lambda I, so

    ||Q u_W(T)||_2
      <= exp(-W lambda T)||Q f||_2+||B||_2||f||_2/(W lambda).

Thus, for every T>0,

    exp[-T(WA+B)] -> Pi exp[-T Pi B Pi]Pi.

If Z is empty then Pi=I and no singular limit is needed. No numerical value
of lambda, no Aldous theorem, and no supplied mixing-gap lower bound are
needed to establish this finite-dimensional identification; lambda's positive
existence follows automatically from the fixed A on its kernel complement.

Now take any finite positive sequence r^(j) whose reciprocals converge to
theta*. Fast rates may diverge at unrelated, unbounded relative rates. Compare
it with any W_j->infinity on the fixed reference path above. Their reciprocal
distance tends to zero, so their endpoint kernel distance tends to zero by
the receiving theorem. The unique completion value is therefore exactly
Pi exp[-T Pi B Pi]Pi for *every* such approach. This proves that no fast-rate
ratio assumption was introduced by the fixed-ratio reference path.

Finite retained edges lying inside a fast component vanish under Pi B Pi.
Retained edges joining the same two blocks contribute through their summed
rates and conditional uniform endpoint-label exchange. The exact checker
verifies both facts on small full permutation generators. Zero physical rates
common to the original models were omitted before this construction; a rate
tending to zero corresponds to reciprocal infinity, outside this finite
completion. Joint continuity at T=0 is not claimed and is generally false.

## 3. Quantum lift and its boundary limit

Choose an actual unitary representation g -> U_g of the finite permutation
group; ordinary swaps of isomorphic tensor factors provide one. For the
identity-start increment law p_theta, define

    Phi_theta(X)=sum_g p_theta(g) U_g X U_g^*.

Each unitary channel has diamond norm one. Therefore

    ||Phi_theta-Phi_eta||_diamond
      <= sum_g |p_theta(g)-p_eta(g)|
       = 2 TV(p_theta,p_eta).

This proof covers arbitrary quantum inputs and arbitrary reference systems,
including the complete diamond norm rather than an unreferenced trace-norm
calculation. The bound persists on the reciprocal boundary by TV continuity;
the finite sum defines the limiting random-unitary channel directly.

The factor is sharp for a swap representation: identity and a two-factor
swap send |01> to orthogonal states. Distinct rational mixture weights give
output trace distance equal to the classical mixture TV, as checked exactly.
This does not extend to coherent exchange Hamiltonians, configuration- or
input-dependent noise, or an independently specified physical quantum-memory
model. The root's stated random-swap channel qualification is necessary and
sufficient for this mathematical lift.

## 4. Component cap allocation

Let m_C=|E_C| and a_C=m_C c_C^2 for nontrivial components. Giving component C
a cap-error budget epsilon_C>0 and choosing physical cap
K_C=c_C^2/(T epsilon_C) yields the candidate-attempt upper bound

    sum_C T m_C K_C = sum_C a_C/epsilon_C.

For sum epsilon_C=epsilon_cap, Cauchy-Schwarz gives

    (sum_C sqrt(a_C))^2
      <= (sum_C a_C/epsilon_C)(sum_C epsilon_C).

Equality holds precisely when epsilon_C is proportional to sqrt(a_C), namely
c_C sqrt(m_C). Hence the minimum of this stated *upper bound* is

    (sum_C c_C sqrt(m_C))^2/epsilon_cap.

Singleton components have m_C=c_C=0 and receive zero budget/cost. This does
not optimize the actual sum of min(r_e,K_C), which can have additional
plateaus from already small rates, nor certificate, random-bit, or output
costs. The source calls it an upper-budget allocation and is correct on that
scope.

For an executable rational choice, take positive rational upper weights
u_C>=c_C sqrt(m_C) and normalize them exactly:

    epsilon_C=epsilon_cap u_C/(sum_D u_D),
    k_C=T K_C=c_C^2/epsilon_C.

Then the error budgets sum exactly to epsilon_cap regardless of approximation
direction. If each u_C is at most (1+eta)c_C sqrt(m_C), the attempt upper bound
is at most (1+eta) times the ideal convex optimum: sum a_C/u_C is at most
sum sqrt(a_C), while sum u_C is at most (1+eta)sum sqrt(a_C). Integer ceilings
of the dimensionless k_C reduce cap error further and increase this candidate
attempt upper bound by less than sum m_C=|E|. Rational square-root enclosures
with polynomial bit length suffice. The exact checker verifies rational
normalization, cap budgets, integer-ceiling costs, and representative optimal
allocations.

## 5. Check receipt and freeze boundary

`reciprocal_completion_checks.py` is new standalone standard-library code;
neither root code nor packet code is imported or executed. Its exact receipt
is `reciprocal_completion_checks.json`. The checks supplement the universal
proofs above; they do not establish priority or replace external review.
The audited root source hash and old worker artifact hashes are recorded in
`reciprocal_completion_sources.json`. Old frozen artifacts were unchanged
through this continuation. This focused audit is now frozen after delivery.
