# Independent review: acquired normalized weighted mass

## Verdict and exact binding

**Accepted within the explicitly stated raw-list family and algebraic-cone scope.** I independently reconstructed the ordinary generator proof, finite acquisition argument, nonexplosion/recurrence/moment consequences, and mediated-family obstruction. The independent rational verifier rebuilt the cone from raw reactions, performed its own exact basis acquisition, and checked the returned coefficients and Foster constants. No substantive mathematical correction was needed. The final proof adds the explicit input restriction `m>=1`, matching the existing `n>=2` receiver assertion.

This is an internal mathematical and executable audit, not external refereeing, historical-priority clearance, a general weak-reversibility theorem, or a complete stability algorithm.

Final frozen objects:

| Object | SHA256 |
|---|---|
| `ADAPTIVE_MASS_THEOREM.md` | `ce22e824cde38c55b37072c83669afa840f76698d62278b12662d97febb8b826` |
| `adaptive_mass.py` | `56af50d7bb8f29d1fef7730e1d2608dee4161720a018fbb2824f2c1fb967a6a1` |
| `results.json` | `6bc460364bdcec6112b0b467f9f1980f503c7f55686d46fdd84d343ab4378918` |
| `baseline_results.json` | `acdc4c404c56441127b7c8af60afaf3bb16f3f719d6e50501c70df9c93dd7f11` |

The initially reviewed proof had SHA256 `af6d77c9cf4d0bd860b7e43a800dc0656263f0a7ba0e434635c8843450818297`. A byte diff confirms that the only amendment is the first sentence of Section 1, making `m>=1` and the excluded scalar implementation case explicit. Both snapshots are preserved under `independent_audit/`; the unqualified `frozen_ADAPTIVE_MASS_THEOREM.md` is the final version. Code and original results did not change.

## 1. Acquisition is real, but its completeness is cone-specific

The raw recognizer enumerates the open coordinate rather than receiving it as an oracle. It requires positive immigration/death only at that coordinate, conservative internal reactions, and weak reversibility. Null channels are discarded; duplicate rates aggregate correctly. This is a trusted `int`/`Fraction` research interface, not a hardened arbitrary-input service.

For an acquired pivot A, I independently regenerated all affine forms in the variables `(v_B1,...,v_Bm,beta)`:

- `0<=v_j<=1`, `v_A=1`, and a finite non-excluding upper bound on beta;
- every pure quadratic satellite coefficient at least beta, including the zero coefficient of an absent source;
- every mixed quadratic satellite coefficient nonnegative;
- both signs of every individual higher-order weighted-increment equality.

The all-ones weight and beta zero make this bounded polytope nonempty. For a binary conservative channel, the weighted increment is at most two, so the chosen upper bound on beta cannot remove a positive feasible witness. If positive beta is feasible, maximizing beta on the compact polytope gives a positive-beta vertex. Active normals at a vertex span the ambient space, including in a lower-dimensional polytope: otherwise a sufficiently small two-sided displacement would preserve all active and inactive inequalities. Thus the finite nonsingular-basis enumeration is complete for positivity of this specific polytope.

The independent solver uses forward elimination and back substitution, separate from the constructor's Gauss–Jordan implementation. It reproduced the first accepted basis, all residuals, basis counts, and recorded solved-fraction sizes. It also exhaustively checked two rejected cones.

This does **not** decide recurrence outside the cone. For the stable network `0<->A, A<->B`, all rates one, the recognizer succeeds but the cone exhausts all ten bases because the pure `2B` source is absent. Independently,

    V=3^A 4^B,       LV/V=2-A/3-B/4,

proves the ordinary geometric drift directly. The output correctly retains network stability UNKNOWN. A basis limit of 61 on the mediated demo, which needs 62 attempts, also returns UNKNOWN, not infeasibility. No finite-budget termination guarantee is inferred.

## 2. Full generator reconstruction

Let `a=A`, `b=sum B_j`, `N=a+b`, and `P=v dot x`. Verified weights give `a<=P<=N`. Grouping raw coefficients by source, the negative unary contributions are bounded below by `-K1 N`. Negative binary terms containing A are bounded below by

    -K2[(a)_2+a b] >= -K2 a N.

Pure boundary sources supply `beta sum_j (b_j)_2`; mixed boundary coefficients are nonnegative. Every accepted higher-order channel has weighted increment zero individually, not merely cancellation at one test state. Therefore

    L_internal P >= beta sum_j (b_j)_2-K2 a N-K1 N.

For `h=1-e P/(N+1)` and `W=t^N h`, internal conservation of N gives the exact identity

    (L_internal W)/W = -e L_internal P/[(N+1)h].

This identity is global, including extinct and first-copy boundary layers. It is not a stationary-fiber or asymptotic approximation.

Immigration decreases h and contributes at most `lambda(t-1)`. At `a>=1`, death increases h by `e(N+1-P)/[N(N+1)]`; multiplying by its rate gives the claimed upper correction `d e/[t(1-e)]`. Death is absent at N zero, which is checked separately. Splitting falling factorials as squares minus counts, and using `sum b_j^2>=b^2/m`, gives

    LW/W <= C0-D a/2-e beta b^2/[m(N+1)].

The sign-sensitive uses of `h<=1` for negative terms and `h>=1-e` for positive terms are correct. The epsilon choice ensures `e K2/(1-e)<=D/2`, including its cap at one half. For `N>=1`, splitting at `a>=N/2` gives the stated uniform bound `C0-kappa N`. At N zero the immigration bound remains valid. No limit exchange or real-valued substitution for discrete falling factorials is needed.

## 3. Foster consequences and moment domain

The explicit radius satisfies `C0-kappa R<=-zeta`. Since `h<=1`, the factored rational constant `(C0+zeta)t^R` controls the entire finite exception region without enumerating it. Large constants may remain factored: arithmetic checking of this expression is not a claim that its full numerator has been materialized.

Nonexplosion has a simpler conventional comparator in this class. Only constant-rate immigration can increase N. Initial N plus its Poisson count bounds population on every finite time interval, hence confines the process to a finite state set with bounded rates. Even arbitrarily high-order neutral channels cannot produce explosion on such a finite set. This basic nonexplosion fact is not the substantive new obstruction crossed.

Every enabled reaction has a feasible return path from weak reversibility, by translating the reverse complex path by the nonnegative residual population. Thus communicating classes are closed. The normlike Foster bound yields positive recurrence on each class; global irreducibility is neither needed nor claimed.

The stationary moment argument does not assume the desired integrability. Stopped exponential Dynkin and nonexplosion yield `P_s W<=a W+b` for `a=exp(-zeta s)<1` and `b=C_F(1-a)/zeta`. With `phi_n(w)=min(w,n)`, invariance and concavity imply

    integral [phi_n(W)-phi_n(aW+b)] d pi <=0.

The integrand is bounded below by `-b`. Fatou applied after adding b therefore yields `(1-a)pi(W)<=b`. Consequently `pi(W)<=C_F/zeta` and, since `W>=(1-e)t^N`, `pi(t^N)<infinity`, including the endpoint exponent `log t`. Repeating the scalar construction with the same acquired weights and any larger rational t proves all finite exponential total-count moments. No uniform-in-exponent constants, mixing rate, or efficient sampling claim follows.

## 4. What the mediated example establishes

For `0<->A`, `A+B<->B+C`, `A+C<->2B`, `B+C<->2C`, all rates positive, the explicit proof-only witness `v=(1,eta,0)`, with `eta=min(1/4,beta1/(2 alpha3))`, has strictly positive pure-boundary coefficients and a positive mixed coefficient. Thus exact unbudgeted acquisition succeeds throughout this whole rate family. The constructor does not receive that witness.

The executed asymmetric example acquires `v=(1,1/3,0)`, beta `1/3`, epsilon `1/8`, `C0=47/42`, `kappa=1/384`, and `R=431`. Non-complex-balance was independently checked: the separate linkage balances force incompatible values `a=c=1`, `b=1/2`, and `ac=b^2`. The all-ones direction also witnesses failure of strong endotacticity: its maximal quadratic complexes have no descending outgoing edge, and this direction is not orthogonal to the full stoichiometric space because of the open core.

The actual missing control is composition/clearance after activation. First activation of A is easy through direct immigration. At `(1,0,n)`, last-copy loss occurs at rate proportional to n; at pure C the internal restoration first creates mediator B rather than A. This is why the acquired weight differs materially from an A-only correction.

## 5. Strong obstruction and conventional comparator

I authored the independent `MEDIATED_AGGREGATE_NO_GO.md`, SHA256

    f53a4d50e83a4b645f5cde8304fece51d092a53ccdbcaf4294fa94326f9b9aa6.

The main agent independently reconstructed it and proved its closed-class scope in `AGGREGATE_NO_GO_MAIN_REVIEW.md`, SHA256

    67c568b967ff16bae3e14d9a33ad068f2abe4ea1894c66f33efda95a46e75115.

The conclusion is stronger than the separable obstruction in the frozen main theorem: **no positive normlike one-step geometric Foster function `F(A,N)`, even nonseparable, can work on the relevant positive-satellite class.** At pure C, the proposed geometric drift forces `F(1,n+1)<=r F(0,n)+constant`, with `r<1`. At the A-one pure-C comparison state, fast A loss forces the reverse comparison up to a factor `1+O(1/n)`. Substitution gives a strict contraction bounding `F(0,n)`, contradicting normlikeness.

I checked every arrow and reverse in the main agent's paths connecting C, 2C, 3C and successive pure-C states. All comparison states and destinations lie in one closed class containing C. An exact test checked 26 edges with enabled reverses, including the generic path at counts up to one million. The argument does not illegitimately combine the separate A-only class with the positive-satellite class.

This is a one-step geometric-Foster obstruction, not impossibility of additive, sampled-time, excursion, queueing, tier or path methods. Nor is full-state information mandatory: the different aggregate `(P,N)` suffices. The easier direct-return family retains a conventional unbounded service-radial correction proved in `CONVENTIONAL_COMPARATOR.md`; it is not claimed that normalized composition is the only unbounded route in that easier setting.

## 6. Independent exact execution evidence

The original candidate and same-input baseline outputs replay byte-identically. The initial batch tool output was context-truncated; I inspected the already-existing complete JSON results and compared their hashes rather than blindly re-running an uncertain command. The complete final JSON prints follow all assertions. Subsequent inspection and additional control commands returned exit zero.

`independent_audit/verify_adaptive.py` independently checks raw recognition, graph return paths, cone acquisition, all exact finite forms, coefficients, higher-order neutrality, K1/K2, epsilon and tail inequalities, Foster expression/bit bounds, and exception-set cardinality. It additionally reconstructs the exact raw generator and tests both the stronger intermediate quadratic bound and the final linear bound.

| Case | Acquired weights | R | Ordinary exact states | Huge/targeted states |
|---|---|---:|---:|---:|
| Mediated demo, t=2 | `(1,1/3,0)` | 431 | 969 | 25 |
| t=65/64 | same | 260 | 969 | 25 |
| t=100, compact constant | same | 19223 | 969 | 25 |
| Added asymmetric unary B/C pair | same; K1=5/3 | 523 | 969 | 25 |
| Neutral cubic `A+2C<->3B` | same | 431 | 969 | 25 |
| Species permutation | `(0,1,1/3)` | 431 | 969 | 25 |
| Strongly heterogeneous rates | `(1,3/500,0)` | 4806 | 969 | 25 |
| Easier direct-return family | `(1,0,0)` | 283 | 969 | 25 |
| Four-species mediated/direct-return | `(1,1/3,0,0)` | 646 | 4845 | 30 |

Totals are **12,597 ordinary exact generator checks**, **230 targeted checks** reaching counts `10^50`, and **574 direct small-state checks using expanded W values**. These supplement, rather than prove, the all-state inequality. The original demo separately contains its 5,456-state check and 25 targeted states; counts overlap and are not represented as disjoint state coverage.

Additional controls:

- Nine receipt mutations rejected: weight, beta, basis, raw-derived constraint, residual, K2, higher-order equality omission, Foster coefficient, and bit bound.
- A raw separately reversible cubic `3B<->3C` forces `v_B=v_C`, contradicting positive production at 2C. Independent and constructor searches both exhaust all 286 bases and retain network stability UNKNOWN. Conservation and WR alone do not bypass higher-order neutrality.
- A full-WR but nonconservative added `2B<->3B` pair is rejected by the raw architecture.
- Splitting one immigration rate into two positive rational channels and adding a null channel leaves the certificate exactly unchanged.
- `n=1` is explicitly rejected by the receiver assertion, consistent with the revised theorem scope.
- The basis-budget and compact-constant modes behave as stated. Compact storage is accepted without expanding its rational power.
- Plain `P=A` and the easier family's unbounded A-only correction have exact positive generator quotients on the mediated obstruction rays, including counts `10^50`.

The independent verifier is separate mathematical checking code, not a claim of universal malicious-input security. Finite test coverage, assertion-based API assumptions, and source binding are explicit.

## 7. Costs, literature scope, and stopping boundary

The accepted demo uses 62 exact basis attempts, 41 nonsingular, among 84 candidate bases in dimension three with nine constraints. Its finite exception region has 13,436,856 possible states but is bounded analytically, not enumerated. The original factored Foster bound has conservative unreduced numerator/denominator bit bounds 872/441. The t=100 challenge deliberately crosses the expansion budget and remains factored. No cost polynomial in species dimension, reaction degree, requested exponent, or bit length is proved.

The same-input old terminal-cone compiler returns UNKNOWN after 3,188 candidates; protected/coverage raw recognizers reject. These are sufficient-architecture comparisons, not instability evidence or historical novelty.

The independently accessible [Anderson–Cappelletti–Kim (2020) publisher abstract](https://doi.org/10.1017/jpr.2020.28) states a binary single-linkage-class result; this mediated example has three linkage classes, so that stated theorem is not a direct application. Only abstract-level scope was inspected for this comparison, not the inaccessible full proof; no broader exclusion of that paper's techniques or priority claim follows. The parent's separate `SOURCE_SCOPE.md` records other source checks under their own inspected scope. No blocked transfer was retried and no uninspected paper is a premise of this proof.

This closes the requested receiver/audit boundary. The accepted consequence is a constructive, exact, restricted-family recurrence principle crossing a genuine last-copy/mediator obstruction, together with a proof that one natural aggregate information choice cannot support geometric Foster drift. Earlier accepted files and delivered archives were not altered. No further theorem expansion is part of this verdict.
