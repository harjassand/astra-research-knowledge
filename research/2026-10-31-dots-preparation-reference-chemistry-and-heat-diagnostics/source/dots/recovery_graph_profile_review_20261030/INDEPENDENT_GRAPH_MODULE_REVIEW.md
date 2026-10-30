# Independent raw-graph module challenge

30 October 2026. Scope: the frozen sources in `SOURCE_SHA256.txt`; theory-only independent challenge, not a finite-state numerical test and not a review of broader recurrence. All seven sources were copied before verdict. Author confirmed the core files were frozen and identified the transfer ledger. The earlier reserve compiler is background only, not a dependency of the tagged proof.

## Verdict

**Accept the restricted local acquisition statements with the explicit proof completions below.** I found no graph counterexample under the stated restrictions: fixed finite irreducible conversion generator; only linear birth `a+D -> 2a`; clearing with positive constant times `(a)_2`; fixed competing nonlinear seeds; positive `2D -> a+D` whenever the two-type-removing seed is allowed for the tagged result, and unconditionally positive reverse channel for the reset/grades result. Physical clock and connector are exactly those specified in the tagged note. Constants depend on this fixed graph, its rates, offsets, and the finite requested grade set, not on population or b.

This does not accept arbitrary births, the older unrestricted auxiliary absorption sentence, a full feedback transfer, recurrence of a larger network, historical novelty, or polynomial certificate bit complexity.

## 1. Actual stopped labeled-particle law

The original-a particles can be labeled so that a linear birth retains its parent and creates one new particle. Conversions have independent Q-chain driving processes in the common D-clock; births and changing D alter the map from operational to common time, not these reference chains. Continue a seed-deleted tag fictitiously using its unused independent conversion randomness. Pathwise, actual surviving tags are a subset of the independent reference cohort, with at most two deletions per seed. No independence conditional on episode survival is needed or asserted.

The all-time lower bound on a-reference occupancy follows from a fixed-time positive transition kernel plus the initial no-jump event. At a deterministic common-clock time the reference count is genuinely binomial. A downward threshold crossing must have a preceding near-threshold count; its counting compensator is at most C times cohort size times the small-binomial-tail integral. This proves the finite-horizon supremum bound. Choosing an exponentially long deterministic horizon and paying its overrun with the independently earned common-clock moment is valid despite the random stopped horizon. Geometric seed-mark control remains valid under dormant/connector stops, which only truncate the count.

Births from a non-a type are not harmless extra reference particles for the return estimate: with initial M copies of C and D=1, competing C-to-a conversion rate qM and C-consuming-D birth rate bM, the first event is the birth with probability b/(b+q), already producing D=0 before any clearing. This disproves population-vanishing return rarity in that enlarged class. The exclusion is essential, not a technical convenience.

## 2. Polynomial absorption moments: explicit completion

The tagged note's accessibility cases are correct. With at least two type particles, prescribe paths for two labeled particles to a and then clear, allowing no intervening unwanted jump. With one type, prescribe its path to a then birth; D=1 terminates dormant, otherwise clear. With zero types, the reverse channel supplies a type when D>=2. The only zero-type D=1 case has no active fast path and is excluded; it cannot be reached from an active fixed-n shell by a two-type seed. Thus H=2L+3 is sufficient.

To avoid any unspoken independence between holding durations and the successful jump-count block, strengthen each prescribed step by requiring its holding time to be at most one. At any nonabsorbed active state the required rate is at least a fixed positive number, total operational rate is at most C n^2, and total fast rate is bounded below. Hence the conditional probability of the prescribed next jump within one unit is at least c n^-2. The full path exits within H time units with conditional probability at least c n^-2H. Apply the Markov property at deterministic H-unit blocks. This directly gives E(sigma_op^j)<=C_j n^(2Hj) for every fixed j, without independent blocks or assumed recurrence. Connector stopping only shortens this construction. Physical duration is bounded by C sigma_op/(b)_q and common-clock duration by n sigma_op.

**Literal dependency defect:** the earlier `GRAPH_ACQUIRED_DORMANT_RETURN_BOUND.md` says its own raw graph always gives finite-shell absorption. That statement is false when `2a -> 2D` is allowed without reverse `2D -> a+D`: from two type particles there is positive probability of reaching the all-D absorbing face. The asserted path length L+1 is also not the general two-particle path count. Its probability-of-dormant-return result does not require absorption and is unaffected. The tagged note explicitly adds the paired-channel requirement and proves its own corrected H bound. Acceptance here excludes the older auxiliary sentence; it is not silently inherited as a lemma.

## 3. Low-a arrival and restart accounting

In the D>n/2 regime below a=K, the positive reverse channel has common-clock rate c(D-1)>=cn for large n; a-consuming conversions cost at most CK. Stopping on a seed is legitimate; freezing a at its pre-jump value at terminal clearing/connector events removes their artificial loss from this drift computation. The expected duration before threshold/regime/seed/terminal exit is O(K/n). Overshoots are bounded.

Once D<=n/2, at least n/2 genuine type particles exist at the restart. Before the next seed, they can all be retained as reference Q-chains; births add particles. At t*=C(K/n)^(1/L), independent reference a occupancy has mean at least 4K. The event of no earlier stop and no threshold hit is contained pathwise in the small reference-occupancy event. This uses unconditional reference concentration, not the false assertion that survivors are independent after conditioning.

For clarity, the positive iteration can be made quantitative. Let N count common-clock chunks, S seed interruptions, F full-horizon failures, and R high-D-to-low-D transitions. Before a seed D never increases, so R<=S+1. Each second-regime horizon failure has conditional probability at most rho=exp(-cK); consequently E F<=rho E N, first for a truncated count. The global seed-vs-clear marking gives E S<=C, independently of how many chunks are attempted. The count identity gives E N<=C(1+E S)+E F. Thus E N<=C/(1-rho). Each chunk has expected cost at most C t*, proving E u_low<=C t*. This closes the actual-seed restart argument without unpaid regime cycling or a conditioning shortcut.

## 4. Return, reset, and occupation checks

The sharpened high-stage argument correctly counts order K consuming conversions, rather than charging the first conversion. Its expected count is O(J/K), giving high-to-low probability O(J/K^2). Dormant entry occurs only from D=1, so its high-stage hazard costs O(1/K), with no spurious J factor. The upper-D escape requires order J seeds and is paid once globally. Setting J=K=n^(1/(2L+1)) balances K(K/n)^(1/L) with 1/K. Changes in D caused by births and reverse channel are negative and cannot invalidate this seed-count accounting.

For reset, low clearing rate is bounded by CK^2 in common time; low dormant rate by CK; connectors by a constant after dividing out `(b)_q (A)_a0 D`. Thus all low terminal events cost O(K^2 t*). High continuation after the first threshold hit uses the actual strong-Markov state and new original-a tags. High terminal changes to A are bounded, including clearing's physical offset. It follows that the all-output inverse-s reset exponent is exactly s/(Ls+2L+1). The selected alpha is strictly inside the necessary arrival range for every s>0.

The high time and A-occupation bounds follow from ratios to the actual clearing intensity, not from an upper bound on A: respectively 1/lambda_clear<=C/[(b)_q K^m] and A/lambda_clear<=C/[(b)_q K^(m-1)]. After a cohort failure, either strong Markov with uniform remaining moment bounds or Cauchy-Schwarz with the earned higher moments pays the polynomial-times-exponential remainder. Low physical time is at most C u_low/(b)_q, because D>=1 and the catalyst factor has a fixed positive lower bound. The claimed common choice alpha=1/(4L+2) makes both t* and Kt* decay by positive powers. Thus no operational/common/physical clock substitution is unpaid.

For the occupation ratio V_m/U, the predictable pre-depletion terminal-jump compensator is the correct device. Multiplying a compensator by a future good-event indicator would not be valid; the source does not do that. The initial holding-time lower bound on U is uniform in b>=q under the specified connector rates, so exponential cohort error divided by U is absorbed on the log-squared good set.

## 5. Fixed grades and constants

For a fixed finite set of s, take moment exponents first, then the depletion exponential constants, then logarithmic threshold constants large enough for each required inverse power. Uniform polynomial time/occupation/output resets dominate every fixed inverse-log power below the threshold. Above it, pointwise ratios to `(A)_m` pay the stopped time and activation grades; remaining costs are polynomial times exp(-cx). This argument is noncircular and spends only finitely many higher moments/grades. No uniformity in s or in graph/rate conditioning follows.

The transfer ledger's Cauchy-Schwarz output bound is legitimate: use the acquired f_(2s) preservation on the same actual terminal law and then sqrt(f_(2s)(A_in))=f_s(A_in). The off-diagonal small-gain expression in that ledger remains a proposed transfer, not established here. One must choose its eta after fixing all required reset/profile exponents.

The acquisition-cost note correctly obtains explicit finite-chain constants by prescribed uniformization paths. The Poisson-reserve compiler is not needed in this proof. Polynomial graph work does not imply polynomial bit size or moderate constants; the source acknowledges this limitation.

## Final scope

The restricted raw graph determines a constructive local certificate: finite episode moments, population-vanishing return probability, fixed-grade profile and occupation bounds, uniform reset powers, and same-episode good-input occupation ratios. The proof uses conventional labeled-particle concentration, paths, geometric marks, and stopped compensators. The full signed source, dormant Green/preconditioning, tilted seed phases, complementary strips and Foster patch remain outside this acceptance. The prior four-species review does not certify any of those transfers for this graph family.
