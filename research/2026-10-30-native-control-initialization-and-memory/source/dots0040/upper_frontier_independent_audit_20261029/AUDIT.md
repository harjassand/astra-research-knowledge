# Independent whole-proof audit: upper-frontier moving fugacity
2026-10-29. Exact source versions are pinned in SOURCE_SHA256.txt and were rechecked unchanged at completion. No publication, priority, or general-two-dimensional novelty claim.

## Verdict
**Accepted under the stated upper-frontier contract.** The construction supplies a positive summable dual measure with strictly negative actual adjoint defect outside a finite set. The embedded-chain argument then establishes nonexplosion and positive recurrence on each communicating class. The factorial envelope also transfers, with class-dependent constants, to the invariant probability.

I found no substantive error in the face-rate intervals, simultaneous fugacity choice, moving-coordinate interpolation, actual finite-shift expansion, neighbor crossings, boundary strips, or recurrence implication. This is a whole-proof reconstruction, not an inference from numerical negatives or other reviewers' acceptance. The scope is strictly the strongly connected two-species antichain with pure-axis endpoints and strictly increasing adjacent normal slopes. It is not a proof for general two-dimensional or higher-dimensional networks.

One minor presentation convention should be made explicit: **if there is no face normal on one side of r=1, extend the central fugacity constantly all the way to that endpoint.** The instruction to extend the 'first/final face value' otherwise lacks a referent. This is an immediate construction completion, not a new mathematical premise or an obstruction; the central exposed vertex is then precisely the required endpoint vertex.

## 1. Exact adjoint formula, including disabled reactions
For mu(x)=exp(F(x))/(a!b!) and an edge y_i→y_j, incoming mass exists exactly when x>=y_j coordinatewise. Its ratio to mu(x) is

    k_ij exp(F(x+y_i-y_j)-F(x)) (x)_{y_j}.

The predecessor is then nonnegative and has enough molecules to fire that edge. If x is not above the target complex, its falling factorial is zero and no shifted F needs to be evaluated. Thus grouping incoming terms by target complex gives the asserted local defect coefficients. There is no missing factorial ratio, approximate intensity, or incoming contribution from a negative population.

When F is affine with gradient log c, this is exactly sum_i d_i(c)(x)_{y_i}. For the moving construction, the same identity remains exact; only the finite shift of F is estimated.

## 2. Every exposed face has a compatible strict coefficient choice
For adjacent u,v, strong connectivity of a graph with at least three vertices forces eventual escape from the pair. In particular at least one of its two total exit rates strictly exceeds its internal cross rate, so k_uv k_vu<k_u k_v. This includes the cases where one or both cross rates vanish. The interval

    k_uv/k_v < rho < k_u/k_vu

is therefore nonempty, with upper endpoint infinity when k_vu=0. Choosing rho strictly inside gives two strictly negative within-pair margins. No detailed balance or direct reverse edge is assumed.

The normal w=(r_i,1) exposes just that adjacent pair: every other complex z satisfies w·(z-u)<0. A tangent adjustment fixes c^{v-u}=rho, while scaling log c outward along w sends every off-face incoming ratio to zero. Thus the two acquired margins remain strictly negative for a finite sufficiently large scale.

The common-M construction is compatible across all faces. On a right face, fixing log c_A=S gives log c_B=S/r_i+constant. On a left face, fixing log c_B=T gives log c_A=r_i T+constant. S and T both grow like log M, and every off-face exponent has a strictly negative coefficient of log M. There are only finitely many faces and inequalities, so one finite M meets them all. The central single-vertex case follows by total-degree domination; the central two-vertex case admits the stated tangent adjustment because delta_a+delta_b=0 and delta_b is nonzero.

This verifies finite rate-interval compatibility for arbitrary fixed positive rates. It supplies no uniform small bound on M.

## 3. Interpolation preserves margins
For a fixed c_A, each d_i(c_A,exp t) is convex in t; similarly with the other coordinate fixed. The vertex between two adjacent face plateaus belongs to both faces, so its defect is strictly negative at both acquired endpoints. Every intermediate value between those logarithmic fugacities keeps it below the larger negative endpoint value. A zero-end-derivative cubic interpolation stays between its endpoint values.

The same argument connects the central plateau to the first face on either side, because the intervening vertex is exposed at the central endpoint too. All nonconstant interpolation intervals can be chosen compactly inside a unique-vertex cone and strictly away from r=1. Face plateaus can be chosen disjoint, small, and separated from all other face normals. The central plateau is constant in both coordinates. The completed profiles are bounded C1 functions with bounded derivatives, constant near 0 and infinity.

## 4. Uniform bounded shifts: the key global check
Take any finite reaction shift z and restrict first to a compact slope strip l<=r<=u with 0<l<u<infinity. Outside finite sets both coordinates tend to infinity uniformly: a+2=(b+2)^r. Every segment x+t z stays in a slightly enlarged strip for sufficiently large b. On that segment,

    |grad r| <= C[1/(a log b)+1/(b log b)].

All constants may depend on the fixed strip and shift list.

On a right nonconstant interval, U=S and r>=1+epsilon. The two gradient corrections are b V'/((a+2)log(b+2)) and -[b/(b+2)]r V'/log(b+2). Their suprema tend to zero uniformly because a grows at least like b^{1+epsilon}. On a left interval, V=T and r<=1-epsilon; the analogous corrections are [a/(a+2)]U'/log(b+2) and -a r U'/((b+2)log(b+2)), again uniformly vanishing. At r near 1 both profiles are constant, so no dangerous correction occurs.

Bounded profile derivatives also give uniformly vanishing changes in U(r),V(r) along the segment. Integrating the gradient therefore yields

    F(x+z)-F(x)=z_A U(r(x))+z_B V(r(x))+o(1)

uniformly on every finite interior strip. This includes segments crossing a plateau endpoint: the profile is C1, its changing part satisfies the same estimates, and its constant part has no gradient correction. No assumption that the target and predecessor choose the same interpolation piece is needed.

For the left endpoint strip choose a slope bound strictly inside the constant endpoint plateau. If b stays bounded, that slope bound bounds a, so only finitely many states occur. For b→infinity, all valid bounded shifts remain inside the constant plateau outside a finite set. This remains true when a is bounded or zero. The symmetric assertion holds on the right, including bounded b: as a→infinity, all finitely shifted denominators log(b+z_B+2) stay bounded, hence every valid predecessor eventually lies in the same right plateau.

These endpoint thresholds are genuinely neighbor-aware. Target slope alone at a moderate population does not imply that its predecessors use the same fugacity. This is exactly why the finite-axis diagnostics can be positive without contradicting the theorem.

## 5. Uniform monomial domination and actual tail sign
On each unique-vertex interpolation region, the chosen dominant vertex has a fixed strict negative coefficient and a positive uniform logarithmic gap from every other vertex. Compact containment in the cone is essential and is provided by the construction. On a face plateau, both adjacent coefficients are strictly negative; the *maximum of their two monomials* has a uniform gap from all remaining vertices. It is unnecessary and generally false to require either one of the pair individually to dominate throughout the whole plateau.

On compact interior strips, a/b^r→1 uniformly as b→infinity, and fixed falling factorials are uniformly comparable to their monomials. Since the profiles are bounded, all coefficient terms are uniformly bounded. The finite-shift errors vanish uniformly, so they preserve the acquired negative margins; the positive non-dominant terms vanish relative to the negative dominant monomial(s). This proves strict actual adjoint negativity, not merely negativity of a frozen coefficient.

For an explicit boundary bound, choose r_L below the first face normal. Relative to the pure-B endpoint y_0=(0,b_0), every other falling-factorial monomial is bounded by

    C b^{r_L a_i+b_i-b_0},

and all displayed exponents are strictly negative. This uses only an upper monomial bound for the other terms and a lower bound on (b)_{b_0}; a may be bounded or zero. For a right slope cutoff r_R above the last normal, comparison with the pure-A endpoint gives exponents a_i-a_last+b_i/r_R<0. Thus no infinite disabled-reaction boundary staircase is discarded.

Finite interior-strip thresholds and the two endpoint thresholds together leave only a finite exceptional set. The proof establishes existence and finite computability of such thresholds for the specified computable/rational data; it does not establish a practically useful scale or polynomial encoded cost.

## 6. Recurrence, nonexplosion, and factorial tails
Bounded U,V imply

    0<mu(a,b)<=exp(C(a+b))/(a!b!),

and the finite reaction list gives polynomially bounded q. Hence both sum mu and sum mu q are finite. Pure-axis source complexes ensure every state outside a finite rectangle has an enabled non-null reaction; all absorbing states are confined to that rectangle.

Weak reversibility gives an enabled return path for each enabled state transition: hold the nonnegative residual population x-y_source fixed while following the complex return path. Therefore all communicating classes are closed, including boundary classes.

On a nonabsorbing class, nu=mu q is strictly positive and finite, and the embedded kernel obeys nu P-nu=L*mu. A class disjoint from the exceptional finite set would contradict conservation of total nu after summing the strict negative defect. On its finite intersection A with that set and complement C,

    nu_C >= nu_C P_CC + nu_A P_AC.

Iteration bounds nu_A P_AC sum_{n>=0}P_CC^n by nu_C. Each excursion from any a in A therefore has finite expected embedded length and returns almost surely. The successive-visit chain on finite A is irreducible; this yields finite expected embedded returns and positive recurrence of the full embedded class. The argument does not assume continuous-time nonexplosion in advance.

The recurrent embedded chain visits a fixed finite-rate state infinitely often. Its independent exponential holding times there have an almost surely divergent sum, so explosion is impossible. Every nonzero enabled integer falling-factorial rate is at least the smallest positive reaction constant; holding-time means are consequently uniformly bounded above. Finite expected embedded return lengths imply finite expected physical return durations.

For the tail assertion, take regenerative embedded occupation g at a state in A. Since A is finite, g_A<=c nu_A for some finite class-dependent c. Excursion decomposition and the Green bound give g_C<=c nu_C. Dividing by q yields physical occupation bounded by c mu, and normalization changes only the constant. Thus the invariant probability inherits the factorial envelope and all linear exponential population moments. This is not a uniform envelope constant over networks, rates, or communicating classes.

## 7. Explicit four-complex example and finite-atlas obstruction
The explicit moving-fugacity example satisfies the claimed defect coefficients and its low/middle/high-region domination exponents. The shift calculation is a specialization of the uniform argument above. In its middle strip, the y2 coefficient has the stated fixed negative frozen margin, but the actual shift correction can remain large at very large a with only moderately large b.

The finite rational-Poisson-minimum obstruction is also sound under its stated positivity/domain assumptions. On every generic integer logarithmic ray a=n^p,b=n^q with p>q, the lexicographically smallest fixed base beats all other bases exponentially, uniformly over the finite shift list. Avoiding finitely many Newton-weight ties makes each positive rational correction asymptotically shift-invariant. The finite minimum retains that property even if its minimizing correction changes between neighboring states. Each of the four complexes is uniquely exposed on one such ray, forcing all four fixed-base defect coefficients nonpositive. Their positive weighted sum is zero, forcing all to vanish, which contradicts the affine rate-cycle relation 1=2.

The communicating-class qualification is valid: the stated integer combinations produce buffered moves (4,0) and (0,48), their negatives are enabled via weakly reversible return paths, and all sufficiently large points in the corresponding untranslated sublattice communicate. Choosing n divisible by 48 places all four generic ray families in that same class. Thus the contradiction is not manufactured by mixing unrelated classes.

## 8. Threshold warning: independently reproduced, not bypassed
The warning file is in the sibling directory `chemical_unbounded_background_20261029/`, not the theorem's `unbounded_background/` directory. Its exact version is included in the source manifest.

An independently written 160-digit implementation of the exact grouped adjoint formula reproduces:

- B=100, A=B^25: normalized defect +0.23070177512141598356.
- A=10^6, B=0,1,2: normalized defect +1.97198857827389684960.
- B=1000, A=B^25: normalized defect -0.13246827870585357073.
- A=10^60, B=0,1,2: normalized defect -0.5.

The positive cases remain in check_diagnostic.json. These checks establish only the finite-point warning and formula implementation; they are not evidence for a uniform tail cutoff. In particular, neither a negative grid nor the A=10^60 axis examples certify all later states. The analytic shift, gap, and boundary thresholds are indispensable.

## Final scope receipt
This acceptance binds the four source hashes in SOURCE_SHA256.txt. It does not broaden the prior finite-strip acceptance, establish historical novelty, or cover interior complexes, neutral closed exposed faces, three-plus collinear exposed vertices, arbitrary linkage decompositions, or dimensions greater than two. The only noted construction-edit request is the explicit empty-side constant-extension convention stated above.
