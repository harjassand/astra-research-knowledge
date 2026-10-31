# Independent review: direct immigration–death bridge source
31 October 2026. Reviewer: independent mathematical review.

## Verdict and exact source
PASS at the local mathematical-existence level: the endpoint-conditioned immigration–death path law, endpoint-independent event cap, direct finite-bit coherent source construction, and its local ordering/time/phase estimates are sound. This is not acceptance of a complete bosonic simulation compiler.

I read the complete actual source:
damped_bosonic_reservoir_opening_20261031/THINNING_IMMIGRATION_DEATH_BRIDGE.md
11,488 bytes, SHA-256 beb4cfb5a5ae77b096d712d12c7ebdbce1ad2a73de16ffebd1fab65bd444a458.
I independently verified its byte count and hash. The source's “Unreviewed” header is preserved; this separate receipt records the later scoped review.

## 1. Exact conditional law
For positive immigration rate nu, per-particle death rate delta and duration t, put p=exp(-delta t) and beta=nu(1-p)/delta. The initial survivors are Binomial(n,p), independent of the Poisson(beta) immigrants alive at the endpoint. Conditioning their sum to be m gives exactly the displayed posterior on k=0,...,min(n,m).

Its ratio to k=0 is binom(n,k)(m)_k[p/((1-p)beta)]^k. Thus the source's finite relative-weight computation is correct. Conditional on k, the n-k initial deaths are independent exponentials truncated at t. The m-k surviving immigrant arrival times are t minus independent truncated exponential ages.

Poisson marking splits the immigrant process into independent alive-at-t and dead-before-t processes. A fresh Poisson(nu t) candidate process with uniform births and independent exponential lifetimes, retaining only deaths before t, realizes the latter exactly. Rejected candidates must not be reused for the conditioned alive population. The source explicitly prohibits that mistake. Summing chronological births and deaths gives the exact occupation bridge; particle labels need not be retained in the selected operator word.

The zero-time, pure-death and pure-birth branches are correctly separated, with impossible endpoints assigned zero kernel weight. No logarithm of zero is required.

## 2. Cap and truncation semantics
For every endpoint pair the number of retained events is at most n+m+2C, C Poisson(nu t). Across modes the candidate counts sum to a Poisson variable of mean t sum nu_i, independently of endpoint rarity. Exponential Markov at parameter one proves the displayed H and K cap with the asserted error margin. There is no inverse endpoint probability.

Finite Poisson CDF scans through the remaining cap are legitimate: all omitted mass is an overflow flag, not a renormalized law. The bosonic windows make their means bounded; no large-mean or rejection oracle is being assumed.

Likewise assigning zero good block to a path crossing the Fock cube keeps the untruncated positive path kernel as a majorant while selecting precisely the allowed truncated Dyson paths. Conditioning the source on avoiding the cube would instead be incorrect and is not proposed.

## 3. Stable posterior arithmetic
Compute log p=-delta t directly, and log(1-p) using log(-expm1(-delta t)) with the small-argument branch. It is essential not to round p to zero or one and then use ordinary logarithms. Subtracting the largest log weight leaves a normalizer at least one; exponentially small terms may be discarded under an absolute mass budget. Factorials involve only finite endpoint counts. Large negative exponents are never exponentiated to a large positive intermediate.

The log-odds derivative is exactly -delta-2delta p/(1-p), of magnitude at most delta+2/t. A finite exponential-family derivative therefore bounds posterior total-variation change by L(delta+2/t_min)|dt| for endpoints at most L and durations at least t_min. This bound is conservative and sufficient. It is a direct fixed-duration estimate, not a recursive conditioned-kernel estimate.

## 4. Times, retention and ordering
The truncated-exponential quantile has duration derivative
u exp(-delta t)/(1-u+u exp(-delta t)), between zero and one. Both a death time and a surviving-immigrant arrival t minus that quantile are therefore 1-Lipschitz in duration.

Its density is bounded by delta+1/t. Candidate birth densities are 1/t and candidate death densities are at most 1/t before retention. A candidate's own birth-to-death gap has exponential density bounded by delta; it must be treated separately rather than falsely declaring its two times independent. The source does this.

Conditional on capped counts and the survivor count, different particles are independent. Union bounds over the capped finite set give the stated polynomial near-boundary, near-retention and near-tie error. This is a bound in the already conditioned direct source law; no rare endpoint probability divides it.

For duration changes, candidate counts couple with mismatch at most nu|dt|. Given matching counts, shared uniform birth fractions and shared lifetimes give retention mismatch at most K delta|dt| and event-time movement at most |dt|. Together with posterior coupling and the tie cut this supplies the required local time-stability estimate.

Finite uniform words, certified probability lists and independent lifetime acceptance uniforms give absolute mass/error control. Uniform tails are explicitly priced. The lifetime retention test can precede division by delta, so a discarded candidate does not require constructing a huge lifetime. Small positive rates and short positive times cost their input and precision bits, not inverse-rate iteration counts.

## 5. Coherent use and phase
The capped arithmetic, sorting and flags can be implemented reversibly with padded work. Both sides of the later row/column construction must use identical endpoint-conditioned seed registers and computations. SELECT preserves these labels; uncomputation then produces the intended arithmetic operator average. The local source does not measure or reset the physical reservoir.

A uniform per-input classical coupling controls the associated selected-word average; when a coherent source-state norm rather than its averaged block is used, the usual square-root conversion of bad seed mass must be paid. There is no exponential union over endpoint/time basis inputs. Final whole-block control still belongs to the separate compiler's positive-majorant and norm argument.

For signed occupation jumps, integral n(s) ds = n_final t - sum sign_j time_j. This gives the exact known number-frequency phase. Internal time rounding costs O(K Omega_max h), with the external-duration contribution paid separately. Large known frequencies are handled by arithmetic precision and phase synthesis, not a claimed generic fast-forwarding oracle.

## 6. Alternative source
For dead immigrants directly, the mean is nu t-beta and the lifetime density is proportional (t-ell)delta exp(-delta ell). A truncated-exponential proposal with acceptance 1-ell/t has mean acceptance at least one half because that decreasing density has mean at most t/2. Conditional birth time is uniform in [0,t-ell]. The alternative is mathematically correct; its rejection and cancellation costs would have to be paid if used. The primary thinning construction avoids those additional choices.

## 7. Boundaries
The result uses ordinary independent-particle and marked-Poisson structure, not a new stochastic identity or a novelty claim. It does not require preparing a coherent Perron vector or its stationary Poisson distribution; a large stationary mean at small damping is irrelevant to the finite-window construction.

This receipt does not establish the remaining factorized endpoint block preparations and normalizers, complete physical first-event isometry, outer common-uniform L2 quadrature, private future/channel composition, total circuit resource ledger or a full bosonic compiler. No implementation, empirical accuracy, or practical efficiency claim is made. Those consumers must receive this source with its caps, zero branches, time cuts and precision costs intact.
