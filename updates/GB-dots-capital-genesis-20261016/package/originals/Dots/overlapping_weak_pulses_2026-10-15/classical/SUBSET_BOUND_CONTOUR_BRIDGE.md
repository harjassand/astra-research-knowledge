# Local-stochastic subset bounds replace global iid domination

Status: conditional mathematical bridge reconstructed 2026-10-15. The classical probability interface closes. It does not establish that a particular temporally extended shared-bath pulse implementation supplies its required joint subset bound. The coherent norm-only route is separately conditional below.

## 1. Verdict and exact sufficient hypothesis

Global iid domination and sequential conditional bad-label bounds are stronger than needed for the memory's contour/escape argument. It suffices that the ACTUAL coarse death flags satisfy, for every finite set W of distinct coarse spacetime sites,

    P(B_v=1 for every v in W) <= q^|W|.                 (LS)

The constant q must be sufficiently small depending on the fixed attractive eroder and coarse connectivity. No stationarity, Markov property, finite-range dependence of B itself, or independence of separated marks is required. The probability bound must hold uniformly over the initial logical-bath-reference state if used for a quantum-channel conclusion.

A microscopic sufficient condition is: conditional on the exogenous clocks h, every finite set S of DISTINCT actual parent starts obeys

    P(M_i=1 for every i in S | h) <= p^|S|.             (MS)

Here M_i is an actual instrument-record bad mark; starts not carrying that instrument may be assigned M_i=0. The inequality is required almost surely for every finite subset of the realized, canonically indexed starts, including subsets selected measurably from h. It is not enough to bound individual marginals. The actual record/instrument and its supported Pauli expansion must still be valid; a bare formal label distribution cannot replace that quantum interface.

For the finite-duration model, each parent has a deterministic bounded-delay birth window and bounded memory patch. The original clock law and geometry are retained. Section 2 proves (LS) from (MS), paying a fixed coloring loss. Section 3 supplies the contour argument without asserting iid domination.

## 2. Microscopic marks to coarse local-stochastic flags

At coarse site v write

    B_v = A_v OR H_v,

where A_v is the original primitive base flag (slow/fast, conflict, external noise, local terminal/startup strips as applicable) and H_v means that at least one marked parent belongs to the candidate set I_v(h) capable of producing a guarded birth. Let K_v=|I_v(h)|.

Choose a deterministic bounded-degree packet graph so that nonadjacent packets use disjoint exogenous primitive increments and have disjoint candidate-parent sets. Color it properly with Q colors, where Q<=D_packet+1. Fix this degree bound before choosing b. The base flags A_v are measurable functions of their local primitive packets. Assume P(A_v=1)<=d0, and E K_v<=mu. For independent Poisson starts on N candidate locations in a window of length w, one may use

    mu = kappa N w,

with w<=Delta+2tau in the fixed-duration construction. A finite terminal flag must remain local in its own candidate window; an unrestricted global terminal event would violate packet independence.

### Lemma 2A: marked flags on a separated set

For a finite same-color set J, all I_v are disjoint. Conditional on h, union over one witness parent from each I_v and apply (MS) to those |J| distinct parents:

    P(H_v=1 for all v in J | h) <= p^|J| product_(v in J) K_v(h).

The K_v are independent functions of disjoint clock packets. Averaging gives

    P(H_v=1 for all v in J) <= (p mu)^|J|.             (2)

This uses factorial/subset information, not an independent-thinning law. Unbounded Poisson counts cause no extra problem: only the product of independent first moments appears. A single parent cannot pay for two chosen same-color sites because their candidate sets are disjoint.

### Lemma 2B: strongest clean combination

If (MS) holds conditional on ALL exogenous primitives, including external-noise records, then A_v is deterministic under that conditioning. Expanding which sites use A versus a marked-parent witness gives

    P(B_v=1 for all v in J | h) <= product_(v in J) [A_v(h)+pK_v(h)].

Independent complete packets now imply

    P(B_v=1 for all v in J) <= (d0+p mu)^|J|.

For arbitrary W, choose its largest color class J, with |J|>=|W|/Q. If d0+p mu<1, dropping requirements at W\J proves (LS) with

    q = (d0+p mu)^(1/Q).                              (3)

### Lemma 2C: clocks-only hypothesis, arbitrary base/mark correlation

If (MS) is known only conditional on clocks, do not silently condition it further on external-noise records. Equation (2) still holds. The base flags on any same-color set are independent, so their subset probability is bounded by d0 to the subset cardinality. For an assignment J=U disjoint-union V, Cauchy-Schwarz gives

    P(all A_U=1 and all H_V=1)
       <= d0^(|U|/2) (p mu)^(|V|/2).

Union over all assignments gives

    P(all B_J=1) <= [sqrt(d0)+sqrt(p mu)]^|J|.

Thus when the bracket is below one, a fully sufficient bound is

    q = [sqrt(d0)+sqrt(p mu)]^(1/Q).                   (4)

This weaker recipe needs no independence between marks and external-noise/base flags. All constants remain uniform in L,T. Small d0 and p still produce arbitrarily small q after the fixed Q loss. The fixed-duration/coherent budget is consequently not automatically the earlier linear iid-domination budget: use (3) or (4), and the appropriate small-q contour tolerance.

## 3. Correlated-death contour theorem

Let theta be the cold all-healthy trajectory of the fixed local attractive eroder driven by B. Assume (LS). Then, for each fixed finite connectivity radius k, constants q_star,c,C>0 exist such that q<=q_star implies

    P(the zero component containing x has diameter >=ell)
       <= C exp(-c ell),                              (5)

uniformly in the spacetime anchor x and finite horizon. One may retain a positive power q^(c'ell) instead of the exponential after reducing q_star. There is no stationary upper-invariant-law assumption.

### Named deterministic imports, and exactly what changes

Use the Toom contour existence, distinct-sink/size, and exponential enumeration facts from Swart-Szabo-Toninelli, arXiv:2202.10999v1, Theorem 7 and Lemmas 13-14. Use the deterministic disjoint-chain extraction in Hartarsky-Toninelli, arXiv:2212.08437v2, Lemma 9.15. These are the same contour imports already named in the memory proof. The probabilistic replacement is the joint bound (6) below; Corollary 9.5 is NOT invoked as a theorem about correlated deaths.

Primary sources:
https://arxiv.org/html/2202.10999v1
https://arxiv.org/html/2212.08437v2

In abstract form the required deterministic facts say: every zero has a decorated contour with finite support Z, bounded edge lengths, and distinct sink set S(Z) contained in Z; |S(Z)|>=|Z|/C1. Contours containing a specified point, of support size r, have at most a^r decorations. A long k-connected path covered by such contours has a chain of pairwise disjoint contour supports whose enlarged supports connect across that distance. This paragraph fixes the exact combinatorial interface; these deep contour facts have not been independently re-proved here.

The cold finite history fits deterministic contour existence. Set deaths to zero at all negative times and extend the rule there. Its maximal trajectory is all healthy before time zero and agrees with the cold forward recursion. Thus the contour existence statement applies to each realized history, with no probabilistic assumption about its law.

### Noninjective contour embeddings: support-size conversion

The enumeration is in embedded SUPPORT size, not abstract vertex count. To make the conversion explicit, let n be the number of edges per charge, s the distinct sink count, r=|psi(V)| the embedded support size, sigma the fixed number of charges, and a_edge=1+R/epsilon the SST edge/sink constant. Its embedding rule makes sinks distinct. The imported estimates and connectedness give

    n<=a_edge(s-1)<=a_edge(r-1),
    r<=|V|<=sigma*n+1<=sigma*a_edge*(s-1)+1.

Hence s>=r/max(1,sigma*a_edge). Summing the exponential edge-count enumeration over n<=a_edge(r-1) gives an exponential bound in r. To count contours whose support contains a prescribed point rather than whose root equals that point, allow root positions within O(r); the resulting polynomial factor is absorbed into the exponential constant. Noninjectivity of sources/internal vertices therefore introduces no missing sink multiplicity or superexponential count.

For the cold convention, define the death field on output spacetime sites by xi(x,t)=B(x,t-1) for t>=1 within the finite horizon, and xi=0 for t<=0 and beyond the finite horizon. This deterministic shift/zero extension preserves (LS). The maximal full-field trajectory agrees with the cold history at the times being bounded.

### Joint contour-family estimate

For pairwise disjoint contour supports Z_1,...,Z_m, their sink sets are disjoint as well. A present contour requires every sink to be a death. Ignore any additional non-sink requirements. Consequently (LS) gives

    P(all these contours are present)
       <= q^|union_j S(Z_j)|
       <= q^[(sum_j |Z_j|)/C1].                      (6)

This is a bound for the whole family, not a product of its actual marginal probabilities. The latter product/negative-correlation statement need not hold. Equation (6) replaces the probabilistic factorization at the contour-chain union bound. Therefore no new correlation theorem is required once the deterministic contour interface and (LS) are supplied.

### Explicit summability argument

Let r_j=|Z_j| and R=sum_j r_j. Bounded contour edge lengths and the enlarged-chain connection give R>=n/J0 for a chain starting near anchor x and reaching distance n, for a fixed geometric constant J0. Count chains by their ordered positive sizes r_j. There are at most 2^R choices of their composition. The first contour's distinguished point lies within O(r_1) of x; consecutive distinguished points are within O(r_j+r_(j+1)+k). In spacetime dimension d+1, these choices contribute a product polynomial in consecutive r_j. Since every r_j>=1, use r_j+r_(j+1)<=2r_jr_(j+1) and r_j^a<=exp(a r_j) to bound that entire position count by K_position^R. Shapes and decorations contribute at most a^R. Hence the number of chains of total size R is at most K^R for a fixed K.

The union bound with (6) is therefore

    P(an anchored zero path reaches distance n)
       <= sum_(R>=ceil(n/J0)) [K q^(1/C1)]^R.

Choose q_star with K q_star^(1/C1)<1, preferably <=1/2. This is a convergent geometric series with exponential distance decay. A component of diameter ell containing x has a point at distance at least ell/2 from x; applying the path bound proves (5). This proof uses actual distinct sink counts. Counting an overlap of contours repeatedly as several independent sink requirements would be invalid; disjoint-chain extraction is precisely what prevents that mistake.

## 4. Finite-torus replay without a fictitious independent mark extension

Prove (LS) for the native torus coarse flags using wrapped packet coloring. Degree bounds are uniform and coincident periodic packet indices are counted only once.

The existing first-crossing/closed-zero-ancestry argument is deterministic. For each prospective anchor, its stopped zero witness lies in a fixed spatial patch that lifts injectively. Copy the ACTUAL COARSE flags from that patch over the relevant finite time interval to the lift, and set every other death flag to zero. This lifted inhomogeneous field still satisfies (LS): a prescribed finite set outside the copied patch has all-death probability zero; a set inside corresponds injectively to distinct native torus sites, with probability bounded by q to its cardinality.

No independent extension of globally correlated marks is claimed. The closed ancestor witness reproduces under the copied flags because all required zero parents and deaths lie in the copied patch. Apply the arbitrary-LS cold contour theorem to that lifted field, then union over prospective anchors. This recovers the previous form

    P(macroscopic escape by coarse time N)
       <= C N M^4 exp(-c M).

The deterministic whole-slab support cover and accumulated-homology proof are unchanged, with whatever bounded patch enlargements the microscopic model requires. An implementation must still establish their deterministic support interfaces; (MS) alone says nothing about which memory errors a label represents.

## 5. Actual CP good map and quantum conclusion

Assume an actual physical Kraus/instrument representation with the already required support property: conditional on its actual primitive and mark records, the robust envelope certifies ALL supported Pauli terms, including coherent sums and arbitrary locally charged bad gates. Define G on those actual records by the fixed no-escape predicate. G must be independent of the input state and of any analysis coupling.

The record sum selected by G is CP trace-nonincreasing and has logical factor identity after the common decoder. The complementary actual record sum is CP. If (MS), hence (LS), holds uniformly over every initial joint state, the escape estimate bounds the complementary effect uniformly. The existing CP-good-map completion then supplies the pointwise recovered joint-input diamond bound of the same exponential-lifetime form.

No iid-mark coupling is used anywhere in this version. In particular this bridge could replace the sequential-character coupling if a finite-duration pulse analysis supplies uniform ACTUAL joint subset probabilities plus the deterministic supported-history interface. Neither premise is established here for crossing/shared-bath pulses.

## 6. Why weaker statements do not suffice

- One-point marginals alone: take B_v=X for every spatial v in one time layer, with X a Bernoulli(q) variable. Every marginal is q, but with probability q the entire torus dies in that layer. An exponential-in-L escape bound fails. This violates (LS) for large specified sets.
- (LS) need not imply domination by any nontrivial iid density: in a block of n sites put exactly one uniformly selected death. Then (LS) holds with q=1/n, since intersections of two distinct deaths have probability zero. But the increasing event 'at least one death in this block' has probability one, while every iid density r<1 gives it probability less than one. Sequential conditioning can make the last site's death probability one. Independent repetition over blocks gives the same obstruction for arbitrarily small q.
- Distinct-parent counting is essential. Several coarse flags can share one microscopic marked start. The coloring loss handles this. Omitting it can falsely replace p by p raised to the number of flags.
- A conditional subset inequality cannot be conditioned on additional, correlated noise or quantum records without proof. Lemma 2C is the safe clocks-only alternative.

## 7. Separate norm fault-path route: exact remaining gate

A coherent amplitude/norm hypothesis is NOT a probability hypothesis. In particular

    ||F(S)|| <= epsilon^|S|,

where F(S) is a sum of fault paths containing specified locations S with all other locations unrestricted, does not automatically provide (MS), a positive bad-record decomposition, or a union bound for selected bad amplitudes. Cancellation can make an unrestricted sum small while a restricted sub-sum is large. Even scalar terms +a and -a show this loss of monotonicity under sub-selection. No CP good-map argument may select signed Pauli-expansion terms as if they were classical outcomes.

Here is one EXACT sufficient, but stronger, norm interface. After fixed recovery and a Stinespring dilation, require a decomposition U=G+E with G=Id_logical tensor g and a deterministic witness assignment

    E=sum_w E_w,   ||E_w||<=epsilon^m(w),

where rooted witnesses satisfy m(w)>=c0 L and their number of size m is at most K0^m per spacetime anchor. This must be an actual equality or a proved triangle-norm cover of the BAD amplitude; it cannot merely be a list of overlapping possible fault subsets. Then triangle inequality gives

    ||E|| <= (#anchors) sum_(m>=c0 L) (K0 epsilon)^m.

If the resulting bound eta is below one and U is an isometry, the singular values of g lie within eta of one. Its polar isometry v satisfies ||g-v||<=eta, so ||U-Id_logical tensor v||<=2eta. The induced joint channel is then within 4eta in diamond norm of the logical identity tensor the comparison auxiliary channel. This is a sufficient amplitude route, distinct from the CP/probability route and with different constants.

To deduce that witness decomposition from an inclusive standard local non-Markovian fault-path norm bound, one must prove a bounded-overcount regrouping/first-witness theorem controlling each RESTRICTED bad amplitude, or a suitable inclusion-exclusion expansion whose coefficient-weighted count stays exponential in witness size rather than total spacetime volume. The classical disjoint-sink union bound by itself proves neither. We have not established that regrouping theorem here and do not claim the norm-only bridge closes.

An absolute-sum norm bound for all restricted path families would suffice, but it is substantially stronger than a cancellation-sensitive inclusive fault-path estimate and should not be assumed silently. Any norm route must also account for classical base-clock failures and random fault-location counts; replacing p by epsilon in a probabilistic formula is not justified.

## 8. What is closed and what is still an obligation

Closed, conditional on the named deterministic contour imports: microscopic actual subset probabilities -> coarse local-stochastic flags -> joint contour-family estimate -> exponential cold spacetime escape -> stopped torus bound. This avoids global stochastic domination entirely and survives arbitrarily long-range mark correlations satisfying the uniform subset bound.

Still required from the finite-duration physical proposal: an actual full-joint record construction, uniform subset effect/probability bounds for distinct starts, and deterministic support/ordering correctness. Crossing echoes may defeat a sequential conditional proof without defeating this alternative, but they do not establish the alternative's hypotheses. For coherent norm bounds alone, the restricted-amplitude witness regrouping gate remains open.
