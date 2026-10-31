# Independent whole-bridge receiving review

## Exact binding and verdict

I read the entire `LAST_REFRESH_WHOLE_BRIDGE_AND_ENDPOINT_RACES.md` candidate, initially 16,748 bytes SHA-256 `39904b0e8f8ca489a76b4052a4fc0bed5539b9906f144dcc0c4c6471142849dd`, and the final grid-compatibility amendment. This receipt binds the final 17,121-byte source SHA-256 `8a9d53b84a53ae948255ed8526312fff000318b9846e53f1983a65d724c7a291`.

Verdict: PASS as a whole conditional-bridge and event-sector receiving construction inside the already reviewed sharp complete-instrument interface. It is not an automatic amendment to a frozen ledger, a new general Markov bridge oracle, a gate implementation, or evidence of a practical crossover. The author source's exact dependency manifest remains binding: sharp assembly 857672be..., fixed-window clock 16335629..., coherent dyadic clock 71a7d3ec..., and their review 6c8c13ee....

## 1. Exact last-refresh construction

For the two-state chain, Q=nu(Pi-I), with pi=(d/nu,s/nu), gives the desired visible rates s,d. A Poisson refresh changes the state only when its newly drawn label differs from the current label. Conditional on a last refresh at u=t-Y, all earlier Poisson increments and labels are unrestricted. The last label is independent with law pi, and the backward gap has the exponential law conditioned below t. Conditioning on the endpoint j therefore leaves an unconditioned visible chain before u. No hidden simulation of all nu*t refreshes is required.

For equal endpoints, the no-refresh posterior is z/[pi_i+(1-pi_i)z]. For distinct endpoints this atom is absent. These formulas, followed by a possible final visible flip, produce the complete conditional path law, not merely the endpoint transition probability.

A final refresh whose label agrees with the preceding state must be omitted from the Hamiltonian word. The adjacent equal-sector residences must also be merged before assigning normalized Q dwell kernels and generating QQ insertions. Otherwise the construction would introduce an erroneous phase or an extra factor-two dwell normalization. The final source states both requirements explicitly. Actual visible flips retain their -i factors; QQ insertions are generated on maximal Q residences. A real physical jump is still a separate retained output and is not another virtual phase.

At t=0, the equal-endpoint bridge is empty and the unequal-endpoint conditional limit contains its required instantaneous flip. The latter has zero outer endpoint weight at exactly zero time. Rounded zero durations use this declared limit and bypass normalization. No positive-probability assertion about an unequal-endpoint CTMC at zero duration is being made.

## 2. Both bounded races are correct

For the equal-endpoint no-refresh coin, let p=pi_i and t*=log(1/p)/nu. In the late regime x=z/p, so the weights x and 1-p*x give posterior x/[1+(1-p)x]. In the early regime y=p/z, so the weights 1 and y-p give posterior 1/[1-p+y]. Both equal the required no-refresh probability. Their sums are at least one; a fair-branch race thus accepts with probability at least one half. The interval and complement constructions realize actual bounded coins without evaluating exponentials of a coherent duration.

For the event-sector race, write D(t)=c+s+(d-c)z and a0=(c+s)/d. In the early regime y=a0/z, the raw weights reduce to c(1-z)/(d*z) and 1+s/(d*z), whose sum is D(t)/(d*z). In the late regime x=z/a0, their sum is D(t)/(c+s). Both accepted P probabilities are c(1-z)/D(t). Dividing each displayed weight by two and choosing a fair branch gives success at least one quarter. The individual weights do not exceed two. The stated separation implies a0<1 and d>c, so the event threshold is positive and all coins are valid.

The derivatives of the accepted probabilities are bounded by constants times nu; in particular p'(t)=c*nu^2*z/D(t)^2. More importantly for implementation, the raw weights and interval endpoints also have those local sensitivity bounds, and normalization has a constant lower success bound. There is no inverse pi_i or rare-endpoint normalization penalty. Very small stationary probabilities still require paid classical bits to acquire their logarithmic thresholds and fixed coins; they are not rounded to zero by fiat.

## 3. Actual complete-block cancellation

The event race prepares the positive entry weights E_Qi/S1, where S1 is the Q-row sum of the positive endpoint majorant. The conditional visible-word mean supplies the corresponding physical J K0 block divided by alpha_L*sqrt(mu)*S1. This is the same normalized block required by the sharp outer density w=alpha_L^2*mu*S1^2. Hence the apparent denominator cancels against the acquired outer amplitude, without an online S1, square-root, or rare transition-probability oracle.

All three outer exponential component labels remain private orthogonal coordinates and use this SAME total-density normalized block. They are not independently divided by their component densities and then combined coherently. The inherited common-bin comparison, retained physical jump output, prescribed controls, and private source memory remain intact.

The unconditioned prefix is stopped at the virtual cap. It has at most K accepted visible flips; a final forced flip can only add one and cannot repair an already overflowing word. QQ insertions are capped together with the visible insertions. Selecting zero on overflow therefore implements the original aggregate positive-word truncation. Because the last-refresh representation has the exact conditional visible-word law, the previously earned complete-instrument aggregate tail applies unchanged. No conditional endpoint tail division has been introduced.

## 4. Actual finite-register acquisition

I requested one concrete grid correction, which the final source incorporates: h is rounded down to a power of two, W is chosen as a power of two above every relevant horizon/threshold, and W/h is therefore an integer power of two. This is the actual domain of the product-bit uncensored clock circuit. Outer midpoint timestamps lie on the same grid by using a bin mesh that is an even multiple of h; any classical window rounding is separately charged to the physical-time budget. N=0 bypass remains explicit.

Fixed clocks at rates s,d,nu and the QQ rate use classically acquired angle lists and a tail atom beyond every comparison threshold. Conditional last-gap preparation uses the acquired dyadic envelope on the coherent duration N*h. Its acceptance is at least one half, not an endpoint probability. Endpoint race, no-refresh race, and last-gap normalization give at most three conditional factories per whole event bridge. The visible prefix and QQ stages require only O(K) unconditioned clock draws. Their loops and all arithmetic are padded and paid; unused seeds remain for reversal. There is no expected-query stopping shortcut or table over all durations.

The safe source-vector option uses the bounded polynomial on singular values at least one half. Degree O(log(1/eta)), good-polynomial factorization error O(eta^2), and actual total gate error O(eta) provide O(eta) full-source isometry error. The extra real-part signal ancilla and ordinary phase preprocessing are inherited from the separately read clock receiver. Generalizing the singular threshold from 1/sqrt(2) to 1/2 changes the geometric approximation constant, not the asymptotic claim.

## 5. Optional internal selected-mean normalization

This weaker option is sound only under its stated private-history convention. On x>=1/2, the same bounded odd polynomial has missing tail at most 4*(3/4)^(l+1). Approximating its good polynomial to O(eta) gives an O(eta) good-amplitude deficit and therefore O(eta) failed probability, but only O(sqrt(eta)) failed vector norm.

SELECT must be zero on every failure flag, and the same source PREP must be inverted after selection. Its success block has the target polar direction with a scalar amplitude depending on the preserved classical history label. Then the selected mean is weighted by the squared success amplitude, and its deviation is O(eta); the failed subspace contributes exactly zero. Any label-dependent success phase cancels between PREP and PREP dagger. With fresh flags and retained history, a constant number of such factories costs their summed probability deficits. Approximate polynomial blocks and actual gate errors are additionally charged in operator norm.

This does not justify an eta-close public source state, allowing failure branches to interfere back into success, discarding flags before unpreparation, or weakening the complete physical instrument's amplification tolerance. The safe source-vector option already proves the receiving construction independently of this optional optimization.

## 6. Finite-grid and physical-time error joins

The last-gap quantile is nonexpansive in the truncation duration. Its binned representative differs by at most h. Conditional on preceding clock history, the next exact visible wait is a fresh exponential with density at most nu. Thus a stop decision can change only in a strip proportional to accumulated timing error. Capped summation yields O(nu*D^2*h), D=K+4, for the visible prefix. Applying the same argument to each maximal Q residence gives the QQ contribution; the source's extra D slack covers the residence count.

On matching histories, state labels, visible events, phases and cap decisions agree. The final forced refresh is either omitted in both histories or is the same visible operator in both. Event positions move by O(D*h), and total interval displacement is O(D^2*h). Telescoping the ACTUAL normalized kernel and H0 interval factors yields the claimed Lword timing bound. Zero intervals retain the fixed chronological order; no minimum-spacing deletion or permutation of noncommuting events is licensed.

The proposed h<=eta/[10^7 D^3(Qrate+Lword)] is conservatively sufficient after the explicit circuit subdivisions. Absolute rate errors are controlled through their action over the finite comparison window W. Coin and threshold errors are also separately acquired to the stated raw-law budgets. Large W or very small positive rates cost bits and arithmetic, not a loop proportional to W or a reciprocal success probability.

Bad clock-law mass is charged linearly to an inner selected operator mean because every word is a contraction and its classical labels are retained. This is not converted into a false linear source-vector estimate. Factory errors and actual operator/gate errors use their own indicated budgets. The OUTER exact/finite Kraus comparison still uses its common-bin L2 embedding and the exact remaining-window channel's full physical generator bound. Lword alone does not pay the physical continuation error. No timestamp TV comparison is used.

With eta=beta/10^4 and beta=epsilon_step/(128A), these new source errors fit inside the sharp base-block budget; the complete isometry amplification bound multiplies them by at most 32A. Existing aggregate word tails, physical count/window caps, and prescribed-control composition remain separately paid. Nothing here removes their cost.

## 7. Independent diagnostics and scope

I separately evaluated 240 race instances across four coupling scales, four damping ratios and five times. The maximum algebraic race discrepancy was 4.45e-16; the same-endpoint acceptance minimum was 0.5, and all event-race acceptances were at least 0.25. I also read and reran `check_last_refresh_bridge.py` without rewriting its frozen JSON: all 16 bridge midpoint/count-PGF cases and 28 event-race cases passed; maximum visible-count PGF discrepancy was 5.87e-14. The PGF deliberately assigns no mark to an invisible self refresh. These are scalar diagnostics, not circuit synthesis or proof substitutes.

The earned consequence is a constant number of conditional normalization factories per whole two-state bridge and O(K) unconditioned clocks, with explicit finite source acquisition and complete-block receiving. This can remove repeated conditional next-event inversion and coherent event-entry normalization from this particular implementation. It does not remove physical kernels, operator words, retained memory, complete amplification, all scalar arithmetic, or real encoding/rotation costs. No current numerical ledger has been promoted or amended by this receipt. The ordinary refresh, geometric-clock and bounded-gap amplification ingredients are credited as such; no novelty or practical advantage is asserted.
