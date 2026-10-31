# Independent review: protected-support activation and finite-collar stability

## Verdict and source binding

**ACCEPTED at the frozen versions below.** The protected-token comparison,
acquired tail bounds, actual finite Dirichlet corrections, full collar search,
nonexplosion and stationary-moment conclusions are sound for the stated raw
architecture. No substantive repair to the frozen proof or implementation was
needed. This is not acceptance of arbitrary nonlinear cores, general weak
reversibility, historical novelty, or a universal efficient compiler.

| Parent object | SHA-256 |
|---|---|
| `PROTECTED_BOUNDARY_THEOREM.md` | `c8eb1fcaf9292fe7535c250d42de98c8337abbc6b95bc080c0560b115d68e4cd` |
| `protected_boundary.py` | `5b1c44fb4c1cc8c748463a37b7272edba02aca9f0da4fd379d4c76d60a7e59eb` |
| `results.json` | `382db591b77ec64eb947630473d9d64b683b80838bb634b982f4ff15e8391c9b` |
| `coupling_checks.py` | `01b3cc88f7ff8ce1b6ff6c42ae9ea4ff243b2a985be90b89425ecb7c5587283a` |
| `coupling_results.json` | `38d836652c391e1da873d57223f55343c9c711067d221908fbbeacaa42ca4ed3` |

Frozen copies, byte-identical replay, independent verifier, independent coupling
challenges, additional network receipts and a checksum manifest are in
`independent_audit/`. The frozen JSON was independently verified directly, not
only reconstructed by calling the parent constructor. Earlier accepted packages
were left unchanged.

## 1. Protected-token lemma: the main new interface

The rate split is valid, including occupied destinations. Write the occupied
token coordinates as a set B. A protected conversion i->j transforms it to
`(B\{i}) union {j}`. If i and j are both occupied, this removes i but retains j:
**coalescence**, not exclusion or suppression. The protected and unprotected
rates sum exactly to k_ij*x_i. Unprotected removal has x_i>=b_i+1 and therefore
cannot remove a token's final actual support. Death has the analogous split.
Immigration adds the destination to B.

Every extra reaction in the recognized class preserves a positive service
coordinate whenever it decreases it. Indeed if u_i>v_i then v_i>=1. With b_i<=1,
leaving B unchanged is therefore legitimate. Increases and unchanged coordinates
are harmless. This argument applies to the lemma's broader support-preserving
extra transitions as stated; the full compiler's separately acquired tail is
still restricted to its univariate-WR class.

The X marginal is exactly the original generator. The binary marginal consists
only of the protected linear transitions and is autonomous. There are no
unaccounted B-only events, and nonexplosion of the service process makes the
joint construction valid. That nonexplosion is proved independently from its
tail before the clock is invoked; the full satellite process is not assumed
nonexplosive in order to prove itself so.

Starting B=0 is valid for **every** initial actual service state. Pathwise
hub occupation by X occurs no later than hub occupation by B. Consequently the
uniform bound is the single finite quantity t(0), not an assumed supremum of
infinite-fiber expectations and not a claim that t(0) happens to be the largest
finite-state hitting mean. The binary killed chain has 2^|I| nonabsorbing states.
Its transience follows from finite positive-rate words in the strongly connected
linear graph; token coalescence does not obstruct continuing a path from the
occupied destination. Thus the exact killed solve really acquires the clock.

A wrong occupied-destination rule fails concretely: at actual service state
(A,E,B,D)=(1,1,0,0), tokens=(1,1,0,0), an A->E event gives actual state
(0,2,0,0). Leaving tokens unchanged violates b<=x; the correct tokens are
(0,1,0,0). The independent tests detect both this dominance failure and an
altered binary matrix omitting the coalescing transition.

## 2. Tail acquisition from the raw positive-count graphs

The linear killed equations correctly yield Qv<=-1, q_i>=T, and common hub
weight q_h=T. They are used only to obtain weights, not as a fictitious
independent-particle representation of the nonlinear process.

For a negative jump of size d,

    g(r-d)/g(r) = product_(k=r-d,...,r-1) (1+c/k).

Each factor decreases as r increases. Once the acquired finite ratio test holds
at R_nl>J, it holds at every larger total. Positive jumps have g(r+d)<=g(r).
Hence the exact signed falling-factorial polynomial in the proof is a valid
uniform upper bound for each univariate subnetwork.

A nonempty weakly reversible positive-count graph has its largest complex as a
source of a non-null edge, and every edge leaving that largest complex is
decreasing. This proves the strictly negative leading coefficient, including
multiple linkage classes. The finite polynomial maximum acquisition is also
valid: for n>=1, every positive lower-degree monomial is bounded by its coefficient
times n^(degree-1); the reported cutoff therefore makes the polynomial
nonpositive for every larger integer. The remaining values are enumerated
exactly. No maximization oracle or asymptotic sign guess is supplied.

The resulting actual-core drift and normlike h0 establish standalone
nonexplosion, closing the prerequisite of the protected-token lemma. Adding
stars gives the stated linear negative radial term and exact negative satellite
slopes. The finite r=1 layer is never treated with an invalid 1/(r-1) formula.

## 3. Actual Dirichlet heads and the entire jump collar

The head solve uses the actual nonlinear generator and h0 at **all** exits,
including jumps that overshoot the head boundary by more than one. Subtracting
h0 gives the forcing equation with zero exit values. Positive killed resolvents,
the acquired uniform clock, and an acquired finite positive-forcing support give
`u_R-h0<=M*t(0)` for every R. Only this upper bound is needed; large negative
corrections cannot create harmful incoming leakage.

An inactive state can enter the head from levels R through R+J-1, not just R.
The implementation and verifier enumerate every composition at every such
level. All decreasing inactive rates are bounded by K_leak*r^p. The conservative
radius test at R is sufficient for the whole collar because

    [T^(r+1)g(r+1)/(r+1)^p] / [T^r g(r)/r^p]
       = T [r/(r+c)] [r/(r+1)]^p

is increasing in r. Once it is >=1 and the scalar leakage inequality holds, the
ratio remains favorable for every larger radius. Exponential growth beats the
polynomial leakage, proving unbudgeted termination of the actual checked search.
This sufficient witness is not misreported as the actual cost or stopping
radius.

Positive-count univariate reactions, like stars, cannot extinguish a hub's
presence. The finite active service layers checked by the code cover all
possible incoming patch effects (with harmless extra coverage). Each satellite
coordinate has a strictly positive negative-drift coefficient because hub rows
are complete. The independent verifier derives these coefficients from raw
rates rather than trusting the listed rows. Neutral reactions preserve V
exactly, including high-degree ones.

## 4. Probabilistic conclusion and scope

The head, inactive collar, finite active service layers and analytic tail cover
all integer states. V is positive and normlike, with exponential growth outside
a finite service head and positive exponential satellite coefficients inside it.
The global Foster bound proves full-chain nonexplosion by stopped finite
sublevels, even when neutral rates are of high degree. Weak reversibility makes
each enabled reaction returnable by a feasible path, so communication classes
are closed; finite-set return gives classwise positive recurrence.

The invariant moment argument is valid without initially assuming pi(V)<infinity.
Stopped exponential Dynkin yields P_tV<=aV+b, a<1. Invariance and concavity of
min(V,n), then Fatou with difference bounded below by -b, yield
`pi(V)<=b/(1-a)=C/epsilon`. A fixed T certifies exponential exponents below log T.
All finite exponents follow by a new terminating construction with larger
rational T, not by extrapolating one numerical certificate. No uniform cost or
uniform moment bound in T is implied.

The example is non-complex-balanced already from b=d at the two hub complexes
and the incompatible star requirements c=b and c=2d. The stated value
b=d=1/45 also follows under hypothetical complex balance after internal
positive-cycle flows cancel at A; the positive cycle shares A with the linear
complex graph, so "linear linkage" in the example should be read as those
conditional linear-subcore balance equations, not as a separate connected
component. This is a terminology clarification, not a gap in the non-CB claim.
The maximal B,C direction also correctly obstructs strong endotacticity. These
comparisons do not constitute a historical priority search.

## 5. Exact computational evidence

The independent `verify_protected.py` does not call the submitted recognizer,
constructor, solver, value function or generator while verifying a receipt.
It independently checks raw shape/connectivity, complete hub rows, separate
univariate weak reversibility, weights, negative-jump ratios, polynomial
coefficients and cutoffs, binary killed matrix and hitting equation, all head
equations, forcing support, scalar leakage witness, complete collar coverage,
active-layer slopes and the original raw generator. The constructor is used
only to propose receipts.

Seven cases passed **14,216 additional exact full-generator state checks**,
separate from the original 1,050:

| Case | T | R | Head states | Active service rows | Full-generator states |
|---|---:|---:|---:|---:|---:|
| Positive three-cycle; another inactive phase remains linear | 2 | 4 | 10 | 182 | 1,980 |
| No extra subnetworks: affine recovery | 2 | 4 | 10 | 55 | 840 |
| Empty I with nonlinear hub | 2 | 3 | 1 | 14 | 112 |
| Nonlinear active hub plus inactive cycle | 2 | 4 | 10 | 182 | 1,980 |
| Larger exponential base | 3 | 5 | 15 | 294 | 2,860 |
| Two satellites and degree-seven neutral pair | 2 | 4 | 10 | 182 | 5,940 |
| Exact previously audited two-inactive cubic network | 2 | 3 | 6 | 25 | 504 |

The generator challenges extend beyond the collar into the analytic tail.
The original three-cycle is separately weakly reversible but not a collection
of reversible pairs. The I-empty case has one binary-clock state and mean10/3.

The independent coupling challenge checks **13,122 joint count/token states**
and **177,876 split event terms**. Counts reach4, so the actual 4A->A decrease
is enabled, rather than being hidden outside the tested box. There are20,412
enabled extra-decrease events and10,368 occupied-destination events. Original
count marginals, autonomous binary marginals and coordinate dominance all hold.
These checks supplement the ordinary coupling proof, not replace it.

Rejected certificate mutations: omitted collar layers, deleted coalescing clock
transition, false clock mean, zeroed polynomial maximum, invalid negative-jump
radius and altered head value. A reversible support-erasing raw mutation is
rejected structurally. All three separate budget tests return UNKNOWN:

- clock budget3 versus required4;
- polynomial budget11 versus required12;
- head budget9 versus required10.

### Same-network clock comparison

`same_network_comparison.py` uses the exact raw network from the earlier
independently audited two-inactive cubic case, bound by that receipt's SHA.
The earlier bounded-return construction acquired a 300-state clock with solved
fractions up to4,769 bits. The protected construction acquires a four-state clock
with solved fractions up to11 bits and uniform mean bound1715/82. Its successful
head remains R=3 with six states, and the whole new certificate is independently
verified. This is direct evidence that the new mechanism changes acquisition,
not merely the constants in an assumed clock. It is not a uniform complexity
or mixing-speed claim. Observed runtimes in the receipts are not theorems.

## 6. Limitations and accounting

The support-domination lemma is broader than the proved compiler. General
cross-species nonlinear cores are not accepted merely because they preserve
support: their nonexplosion and compatible exponential tail must still be
acquired, and this package does so only for the stated univariate-WR class.
Direct hub deaths and complete satellite rows remain substantive restrictions.

Raw partition search, exact polynomial expansion and finite enumeration, ratio
search, binary matrix solution, all failed head solves, forcing enumeration,
collar/active compositions and rational arithmetic are actual work. The three
budgets do not bound every operation; in particular they do not cap every
intermediate rational numerator, forcing enumeration or generated Foster
constant. Reported fraction-bit fields concern final solved values, not a full
peak-memory/time certificate. The constructor is a trusted research API, not a
hostile-input parser, complete stability decision procedure or polynomial-time
algorithm.

All acceptance is mathematical and non-operational. No new external source,
upload, outreach, publication or modification of earlier accepted artifacts was
needed for this review.
