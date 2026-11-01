# Independent whole predictable-box executable audit

## Decision and exact boundary

**PASS for the separately frozen v2 whole executable and its stated model-level receiving contract. V1 is not whole accepted.** The original v1 defects and all old bytes remain preserved. The unchanged theorem-only acceptance is a mathematical gate, not retrospective code acceptance.

Controlling v2 directory: `stochastic_predictable_box_receiver_v2_20261101`.

- `AUTHOR_MANIFEST.json`: SHA256 `e54a3514c15a8ce5b0a62c18e28ab0c4b286339f52d880cde952e1c1c40c7112`; 33 payload bindings, 34 strict members including the manifest.
- `common_box.py`: SHA256 `774f89413ac6bf3cf2f194c82e06abe878de15b9681fb6c4d36b345f5e41a4bc`.
- Exact source delta: `ddf8b00a6447a1ccdf3149fcb849ee554fb67312c9b5bef1d03e055ea6bcf061`.
- Controlling `V2_RECEIVING_CHANGES.md`: `25fe5d766dfc7cb9efb0b2edb5ec11b3f37a14191e6fde9d6e00c63a52766f2c`.

The v1 manifest `16c0b44e613b2b779422ac81c7356d6b31ed61f47180d8ad177154527bfe9a44` and code `a5b1049d3af540c8cf6df2f1cf3f540ccc48827d27bf68830154637daeb1845e` remain unchanged. All 22 v1 and 33 v2 payload bindings were verified and copied to `frozen_v1/` and `frozen_v2/`. Only distinct copied execution directories were used for tests; no frozen source was edited.

The mathematical gate is `audit_common_box_theorem_20261101_0255_7ag5kuma/SOURCE_BOUND_ACCEPTANCE.md`, SHA256 `6c1793584c66020e3349b7eab76031d695e2c07222557469e3dc8da638f30e7b`, for theorem `d53758d6f0a7f311e4a3d06e38882b113680ea5604f74f4e4132d17b8542c7de`. Its full copied audit manifest and inputs were checked. Its **4,046 exact theorem assertions** are separate from the executable counts below. The source-bound clarification concerning exact Poisson domination controls the theorem's shorthand: thinning or the bounded backward-Poisson supermartingale earns full tail domination; mgf order alone does not.

Final-v2 independent executable evidence: **22,367 assertions**, comprising 9,375 arithmetic/model checks, 12,751 core receiving/control checks, 189 repair-boundary checks and 52 final supplementary checks. They include **1,044 expected negative exception/refusal tests**, plus the separately counted protocol-status rejections within the tests. The numerical/core checks also ran against v1; their repeated execution is retained but not double-counted in this final-v2 total.

All **four** copied v2 author entrypoints ran successfully. Their four reports, scalar fixture certificate and resource-budget examples reproduce their frozen bytes exactly. The earlier three v1 entrypoints likewise reproduced their frozen reports/data. These are actual replays, not transcript-only claims or independent tests inferred from author declarations.

## Supported mathematical input and service

The raw model is a finite explicit list of directed channel boxes `(source, target, lower, upper)`. Complex entries are exact nonnegative integers; rates are exact integers/Fractions with strictly positive lower endpoints and finite upper endpoints. Floats, BOOL aliases and unsupported complexes are not substitutes. Duplicate directed channels are summed exactly and all support is scanned.

There is one reversible port `0 <-> A`, a nonempty square-free hub graph, every hub is reversibly amplified with `2A`, all other internal channels join a hub to `A+satellite`, and every satellite has a positive outgoing arm. Internal channels conserve total count. The port coordinate is acquired from the raw data, not assumed first. The internal graph need not be connected. The independently tested boxes include reordered/split duplicates, arbitrary admitted hub choices and nonfirst port axes.

The acquired scalar object defines ONE common state function and one common positive tilt, not a different function for each selected rate vector. The actual mathematical process must have the stated simple pure-jump increments and predictable intensities `k_r(s) * (X(s-))_(source_r)`, with the coefficients actually in the acquired box. No unmodelled batch/exogenous jumps, anticipating rate choice or different actuator-to-intensity mapping is inferred from a numeric request.

The theorem supplies conditional per-time exponential-count moments and finite-horizon maximum-count/reaction-firing bounds from continuing-history stopping times. It does not infer a nonstationary invariant law, all-tilt moment bounds, independent episodes or a finite maximum over an infinite future. The reaction counts do not include controller decisions, observation work or physical resources not in this mathematical model.

A resource request needs a **genuinely received history-measurable total-count upper bound** U>=N(tau), horizon T>=0 and failure alpha in (0,1). The arithmetic receiver checks their exact types and their use, not whether U is true. An initial bound plus complete accounting of actual successful immigration can earn such a bound because internal firings conserve N and deaths lower it. Commands, missed arrivals and a bare integer payload do not establish that observation contract. No sensing, timing completeness, hardware or calibration is acquired here. A fallible observation enclosure would need its own separately justified risk charge.

## Whole source/formula review

### Raw endpoint acquisition and acyclic constants

The recognizer correctly acquires lower/upper immigration and death coefficients, the sum of upper `2A->hub` coefficients, minimum lower reverse amplification, maximum complete outgoing hub upper sum, minimum/maximum outgoing arm sums over all satellites, and the total directed internal upper-rate sum. Both directions and duplicate aggregates enter the correct quantities. Normalized box identity is canonical; it is not a claim that different literal row orders or split rows are distinct mathematical boxes.

The implementation follows the exact acyclic scalar sequence: M, q, resource weights, g/h, source-step prices, T/B/R, K/Pbar and residual prices; then face-cover constants; only then the small tilt, death correction, inactive correction, finite head, nu/zeta and factored C. It expands neither `q^M` nor the astronomical final `t^(Nstar+1)`. Its `Pbar=(K+1)^n` is a ceiling on the complete face-weight sum, not a replacement of the actual independent-set function by an arbitrary profile.

The crucial endpoint choices were checked against the proof and independently reconstructed with algebraically equivalent formulas:

- favorable arm/amplification gaps use lower endpoints;
- adverse source, step, head and death costs use upper endpoints;
- D=mu_lower*eps/(1+eps), while CA, Cbirth and the last-copy threshold use mu_upper;
- inactive cancellation retains the same actual immigration coefficient through both terms and finally uses lambda_lower;
- Nstar retains every residual, last-copy and interior threshold;
- nu=min(lambda_lower,1,sstar/8), zeta=nu/Htot;
- C remains `(zeta+lambda_upper+mu_upper*Nstar+S_upper*Nstar^2)*Htot*t^(Nstar+1)` as a factored exact expression.

The independent reconstruction covered **48 raw boxes**, comparing all 16 acquired model/endpoint fields and all 36 scalar fields individually, including duplicates and nonfirst port coordinates. The geometric independent-set weights, complete actual multiplier and rate-linear worst drift were also independently evaluated on small actual states, including inactive and last-copy states. Those finite checks supplement the uniform theorem; they do not replace its arbitrary-state proof.

`worst_scaled_drift` uses the proper falling factorial, not ordinary powers, and selects the upper coefficient precisely for positive channel increments and the lower for negative ones. Its witness is an admitted vector. Zero-propensity channels are skipped before calling the function on a potentially negative destination. `RateGuard.intensities` applies the same exact model map.

The supplied full-function large-tier author test was genuinely replayed: 14 states beyond the 1,125-bit head, 11 actual independent faces, all 50 channels, 32 upper-endpoint and 75 lower-endpoint contributions, and no ambiguous interval signs. Its tail-profile ceiling uses the valid Bernoulli inequality `q^M>=2`; it does not expand the enormous count-dependent power. No process simulation or stationary-fiber solve occurred.

### Exact count and firing caps

For beta=alpha/2, the Foster cap uses

    L=max(U,Nstar+1) if T>0, otherwise U,
    block=ceil(1/eps),
    k=least nonnegative integer with
        2^k >= (4/3)*(Htot+CF_prefactor*T)/beta,
    RF=L+block*k.

Bernoulli gives `t^block>=2`, so the maximum-count tail at RF is at most beta without evaluating huge powers. The zero-horizon branch retains a positive confidence margin rather than incorrectly setting the count level to U.

The ordinary immigration comparator is retained, not weakened: with v=lambda_upper*T,

    RP=U+2ceil(v)+ceil_log2(1/beta).

The exact dyadic cap follows from `E 2^Poisson(v)=exp(v)<=2^(2ceil(v))`. Choosing `R=min(RF,RP)` chooses between two separately valid history-measurable caps; it is not a minimum of Lyapunov functions requiring a new drift argument. The total stopped firing intensity is then recomputed at the **selected** R:

    Lambda_R=lambda_upper+mu_upper*R+S_upper*R^2,
    firing_level=2ceil(Lambda_R*T)+ceil_log2(1/beta).

One beta pays count exit and one beta pays the stopped-firing tail. Exit is not charged twice: on no exit, the stopped and full firing counts agree. The guarantee is for the event `max_count>=R OR firings>=firing_level`, with the initial time included in the count maximum and reaction firings over the subsequent interval. Simultaneous count exit and firing does not require independence. The stopped Poisson clock includes the exit-causing firing using its pre-jump intensity bound.

The independent code checked **288 resource tasks**, including zero horizon, huge U, exact rational confidence and large horizons, as well as 4,116 brute minimal-dyadic-ceiling fixtures and 100 exact Poisson cap formulas. Every saved resource example was additionally received with independently supplied literal external task values, not merely values copied from its claim.

### Strong ordinary comparison and actual output

For the exact supplied 50-channel, five-satellite box, U=10, T=1, alpha=1/100:

- chosen method: **ordinary immigration Poisson**;
- count level: **24**;
- firing level: **116462**.

The common-Foster head has 1,125 bits and is dramatically worse at this short horizon. Independently reproduced neighboring dyadic tasks show the ordinary cap still wins at **2^1121**, whereas the common-Foster cap wins at **2^1122**. This is about 10^338 mathematical time units, not an operationally useful crossover or an exact continuous-horizon crossover. A compact symbolic expression does not make a huge numerical bound practical.

The genuinely additional statement is one common drift/moment certificate for all actual predictable choices within the box. Ordinary common-Lyapunov, conditional compensator and Poisson methods receive full credit and all the same input. No separation from informed conventional methods or historical novelty is asserted.

## Real v1 failures and exact v2 repair

The v1 numerical formulas passed, but its whole executable boundary did not. `V1_FINDINGS.md`, `api_v1_diagnostic.py/.json` and immutable source copies preserve the actual findings:

1. A returned `tail_recipe` included the original acquired `CF_expression` dictionary by alias. Editing a returned coefficient to zero changed the source certificate and subsequent tail recipes.
2. Public ledger allocations were a mutable backing list, with writable total/spent. Public mutations could invalidate the recorded invariant and permit spending after resetting spent.
3. Deep JSON leaked RecursionError; a zero-denominator QHEX leaked ZeroDivisionError; malformed tag arity/JSON leaked uncategorized parse exceptions.
4. The old resource receiver used U/horizon/failure from the claim itself. It checked self-contained arithmetic, not a separately supplied original client request.

These were reported before acceptance and fixed only in a separate additive v2 package. The original manifest, code, output and diagnostic are not overwritten or relabeled as passes. The theorem and scalar formulas did not need correction.

V2 detaches the returned source expression and the two returned tail branches. Independent mutation tests verified that source certificate bytes and later recipes remain unchanged. Resource receipts contain no mutable alias into scalar proof state. The input scalar dictionary remains a trusted acquired object; intentionally replacing its own fields is not a newly supported way to acquire different constants.

The ledger uses read-only public properties and immutable tuple snapshots. Public assignment/deletion/list-style mutation fails; returned receipt mutation does not alter internal reservations; old snapshots remain unchanged after new reservations. The trust boundary is a single-owner sequential in-process API, not resistance to private Python-state introspection or unsynchronized concurrent mutation.

The resource receiver now requires external keyword values `initial_total_upper_bound`, `horizon`, and `failure`, reacquires from the raw box and that external task, and compares the entire canonical expected receipt. Independent tests reject changed external fields and internally valid receipts for three different tasks. All 27 resource proof leaves were independently mutated and refused. Missing required keywords produce the ordinary Python signature TypeError, which is distinct from malformed data reaching a receiving parser. This new request binding does not transform the supplied U into an observation proof.

The final low-level power helper also requires an exact positive rational base and an exact integer exponent, preventing implicit float-power evaluation. Its strict base/exponent aliases and exact budget boundaries were independently exercised.

An AST comparison verified that the recognizer, full scalar constructor, model/rate guard, resource-cap formulas, profile/drift formulas and ordinary comparator are unchanged. The theorem, raw box, 10,948-byte fixture certificate and resource examples remain byte-identical between v1 and v2.

## Wire, tree, typed receiving and refusals

The scalar receiver reacquires expected constants from raw input, not stored endpoints. V2 checks the claimed finite tree before reconstruction. Wire receiving first checks bytes and the byte allowance, then scans lexical depth/tokens/string bytes before JSON parsing. It rejects floats, NaN/infinity, BOOL/null atoms and duplicate keys; exact canonical numeric tags are then decoded under independent logical budgets.

The structural guard is iterative, accepts exact built-in admitted types, charges dictionary keys as nodes, rejects active-ancestor cycles, and charges repeated aliases at **every expanded occurrence**. Crucially its cumulative scheduled-node counter is checked before materializing/pushing child collections. The independently tested saturated-pending-stack case proves that queued siblings cannot be forgotten when deciding whether to expand a child. Exponential DAG expansion is refused without traversing the hypothetical exponential tree.

For the actual decoded scalar certificate, independent measurement gives 1,002 nodes, depth 5, maximum atom 3,306 bits and maximum string 64 characters. The encoded wire tree has 1,558 nodes, depth 6 and maximum string 829 characters. Exact corresponding allowances admit; one below refuses. The wire is exactly 10,948 bytes and one-byte-short receiving refuses. These are bounds for the specific representation, not a portable Python heap-size meter.

QHEX requires two canonical lowercase hexadecimal strings, positive denominator and reduced fraction; ZHEX is reserved for integers above 4,096 bits. Leading zeros, negative zero, alternate signs/case, nonreduced fractions, extra keys, malformed arity and invalid encodings are refused. Decimal JSON integers remain within the existing finite conversion boundary; no global decimal-digit safety limit is disabled. Independent tests cover the 4,096/4,097-bit boundary and a >5,000-bit reduced rational. Oversized or deep values yield controlled Unsupported/BudgetRefusal, not the v1 recursion/division leak.

The core independent tests mutated **all 774 scalar-certificate proof leaves**, checked malformed raw models and budgets, and verified 6,000 exact model intensity enclosures under 120 admitted vectors. RateGuard copies raw/request containers into immutable rate data. Modifying a supplied mutable request afterward does not alter its active vector. Invalid request types, counts or out-of-box coefficients retain the entire previous positive admitted vector, never turn channels off or reset the process. The public `active` value is immutable. RateGuard does not prove future predictability or actual physical realization merely by returning ADMIT.

The actual malformed/deep receiving tests use forbidden-constructor sentinels only to establish rejection before scientific recomputation; valid receiving and proof mutations genuinely execute reconstruction. No stub is used to claim a valid model/resource receipt. Author extreme-scalar tests deliberately disable face/profile/drift helpers to prove scalar acquisition needs none of them; that disabling is stated rather than confused with full-function evaluation.

## Continuing-history risk accounting

The ledger admits only positive exact rational reservations while spent+requested<=total<1, and refusal leaves prior reservations unchanged. Independent tests covered 2,048 history-dependent prefix allocations across 256 finite branches, 2,048 overspend rejections and 1,536 invalid-request rejections. The final repair adds public immutability rather than changing the arithmetic allocation rule.

Reservations must actually be made predictably before the relevant episode and that episode must use its admitted failure allowance and true count bound. The code does not infer temporal ordering, observation truth, actual rate adherence or use of a reservation by a future external process. Reusing one reservation for several uncharged episodes does not earn a guarantee. Under the stated contract, the pathwise sum of admitted alpha_j is bounded by total; tower, Tonelli and the countable union bound then cover overlapping, history-dependent episodes without reset or independence. No invariant law or free repeated risk budget is inserted.

Infinite mathematical sequences are treated by limits of paid finite prefixes. Maintaining an actual infinite ledger is not finite work, and the resource levels may grow without bound. The common moment theorem does not supply a finite cap on the infinite-future maximum.

## Costs and explicit trust boundaries

The explicit raw support and rational rate lengths are the acquisition input cost. Scalar construction has the proved polynomial input-bit formula cost: `2^n` has n+1 bits; `(K+1)^n` may be huge numerically but has the charged polynomial bit length. The final exponential C stays factored. Exact Fraction arithmetic, gcd, comparisons, canonical serialization and output bytes retain their ordinary costs. No universal wall-time/heap limit for raw scalar construction is provided by a wire-byte or profile-power allowance.

Full function evaluation may enumerate exponentially many independent sets. `faces` pays its conservative `2^n` mask bound before enumeration. `power` separately pays exponent magnitude and numerator-plus-denominator power-bit precheck; exact thresholds and one-below failures passed. `multiplier(p,x,fs=...)` treats an explicitly supplied face cache as a trusted internal diagnostic input; it is not an untrusted-cache receiver and bypasses default enumeration. Likewise `worst_scaled_drift(...,fn)` accepts a trusted diagnostic function, not an externally certified arbitrary Lyapunov oracle. Acceptance concerns the default acquired function and stated internal uses, not promotion of those overrides into free validation services.

Actual extreme author replays retain their costs:

- Rates from 2^-200 to 2^200: M has 406 bits; head 15,598 bits; maximum retained scalar numerator+denominator 51,888 bits; certificate 76,062 bytes.
- Thirty-satellite scalar acquisition: 120 channels, head 8,188 bits, certificate 62,127 bytes; zero independent sets enumerated during scalar/resource acquisition.

These maxima are recorded retained-value sizes, not a measurement of every temporary or peak memory. Wire byte/depth/node/atom/string limits apply to receiving data. Prefix lexical scanning and JSON/typed reconstruction are paid; they are not a universal meter for all trusted raw arithmetic.

A ledger snapshot property read is O(1), but reservation j creates a new tuple and copies O(j) references. J reservations can therefore cost O(J^2) cumulative copying. Current ledger storage is O(J); retaining all prefix snapshots can retain O(J^2) references. Rational bit work is additional. These controller costs are expressly excluded from the reaction-firing cap, not hidden inside it.

## Evidence, preservation and exclusions

Evidence includes full source snapshots, all copied author stdout/stderr/results, initial/final source readbacks, exact v1 regression witnesses, independent arithmetic/control/repair/supplement scripts and reports, the accepted theorem gate, and this review. The first independent arithmetic draft compared an unsorted edge-index tuple derived from sorted hub vectors; its first fixture failed on ordering. Its source/error are preserved. The corrected independent reference uses canonical edge sorting; no candidate formula changed. One launch initially used a nonexistent cwd-relative script path and stopped before execution; the correct copied-tree launch then completed. There was no denied or uncertain operation.

The inherited source-access quarantine remains controlling. This audit made no external retrieval and did not use quarantined material for new novelty/significance claims, but it does not award blanket source-process compliance to historical packages. No source-denial retry, helper, operational chemistry/biology, experiment, hardware, publication or outreach occurred. The task is an exact mathematical count-process/code audit.

Final acceptance is limited to the frozen v2 raw grammar, common-function formulas, exact scalar/resource acquisition, safe typed/wire receiving, ordinary in-process rate/ledger API and explicitly supplied original task. It does not certify external observation or actuation, arbitrary model changes, unbounded rates, zero lower floors, nonstationary invariant distributions, practical astronomical caps, infinite-future maxima, arbitrary profile caches, controller overhead or historical novelty. V1 failures remain real and visible. Final immutable readback of both original manifests, all 55 payload bindings and every audit artifact completes this receipt; no unresolved blocker remains at that boundary.
