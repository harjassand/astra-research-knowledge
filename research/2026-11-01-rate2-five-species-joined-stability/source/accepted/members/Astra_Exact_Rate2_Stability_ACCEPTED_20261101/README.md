# Accepted stability theorem — exact five-species rate-2 tree

**Completed restricted-model mathematical theorem, not merely a component
checkpoint.** The actual chain has a unique invariant probability pi, is positive
recurrent, and satisfies

    pi[(1.000001)^S] < infinity,    S=A+B+C+D+E.

The finite population head and its additive Foster constant are proved to exist
but **UNEVALUATED**. There is no numerical tail/moment bound, practical efficiency,
general weak-reversibility theorem, or historical novelty claim.

## Exact model and two independently received routes

State space: nonnegative integer counts (A,B,C,D,E). Unit-rate port 0<->A;
internal pairs 2A<->AC, 2A<->AD, 2A<->AE, AE<->CD, CD<->AB have coefficients one
except **CD->AE has coefficient two**. The 2A propensity is A(A-1), not A^2 or
A(A-1)/2. Every proof concerns these actual twelve channels and physical time.

### Direct continuous-time Foster route: explicit potential, unevaluated head

The exact quadratic-debt proof `069fcf0b...` and complete independent whole audit
are in `sources/quadratic_debt_global_audit_20261101_dp9w20ix/`.
With r=1000001/1000000, c=A+C, d=A+D, H=(B-A-99E)/100, let tau=0 when H<=0,
otherwise solve

    2[cd tau+(c+d)tau^2/2+tau^3/3]=H.

The potential is explicit:

    W=r^S {exp(tau)[1+20 A^2 min(tau^2/4,1)/(B+1)]
           +10[1/(c+1)+1/(d+1)]-A/[1000(c+1)(d+1)]}.

The accepted ordinary proof establishes `LW<=-W/60000` outside a finite
UNEVALUATED head. All actual successor values, kink/clip crossings, grouped AE
costs, reverse arms and true deaths are paid. The uniform escaping-sequence
argument, not finite tests, proves the all-state statement.

`PROBABILISTIC_CONSEQUENCE.md` receives this with nonexplosion, irreducibility,
finite-horizon integrability, tight occupation averages and Fatou. It constructs
pi without subtracting unknown infinite stationary expectations. The symbolic
bound contains a finite unevaluated K; it is not a numerical moment estimate.
The historical mathematical binding's RUNNING replay field is superseded by
`FINAL_BINDINGS.json` and the terminal replay receipts, all preserved unchanged.

### Separate all-start physical reduction and sampled-consumer route

The accepted block `a0e09b39...`, its source-bound receipt `1be863ee...`, and all
received dependencies are under `sources/return_path_construction_20261101/`.
For every actual initial composition above a finite threshold,

    d_N=1+10^8 sqrt(N),
    P[S(d_N)>15N/16] <=32 exp[-sqrt(N)/10^6].

This now includes the previously missing arbitrary-boundary seed, qualified
activation/macro entrances, actual interior removal, all adverse exits and unused
deterministic time. One original immigration event pays the entire block. Neither
state nor reference N is reset; attempts are not assumed independent.

The independently received `CONSUMER_APPLICATION.md` uses sampled theta=10^-16
and the exact Poisson MGF to obtain the separate continuous-time result
`pi[exp(5*10^-17 S)]<infinity`. The occupation conversion uses an exponent strictly
below the sampled exponent. This route does not claim the stronger direct-Foster
tilt; the stronger 1.000001 tilt comes from the separate global proof above.

The old conditional-consumer receipt correctly said network (H) was not verified
at its own freeze. The new exact composition and application now supply (H).
Earlier author-PENDING headers and filenames remain historical bytes; controlling
later independent receipts supply their precisely bounded current acceptance.

## Corrections and true failures remain visible

- Macro upper overshoot `[delta N,delta N+1]` applies only to a first crossing
  from below, not every already-macro initial state. The actual short-window
  error retains its factor 10 and threshold `N>=28 exp(100)/eta`.
- Initial-growth/activation components have disjunctive outputs. The new
  composition proves the extra global seed and actual receiving arguments;
  it does not simply rename a B-half or upper-band exit as removal.
- The all-unit comparison model has a product-Poisson law; that law is **not
  transferred** to this rate-2 chain. Deterministic drift equivalence supplies
  only the specified internal complex-balanced ODE machinery.
- The exact rate-2 bounded-comparability Foster obstruction is retained. There
  is no conflict: W has an unbounded subexponential debt multiplier, and the
  other route uses real-time sampling plus an occupation measure.
- `ANGULAR_BASELINE_FAILURE.md` preserves the failed linear clip/angular proposal.
  Positive finite-head drift is also retained: (1000,1000,0,0,0) has a certified
  normalized drift in [39.949029,39.949030]. No head-free theorem is asserted.

## Evidence, reproduction, and exclusions

`SOURCE_ALLOWLIST.json` freezes every source/audit byte and provenance.
`PACKAGE_RECEIPTS.json` and `HASH_ALIASES.json` give short navigation aliases;
they are new package indexes, not rewritten reviewer receipts. Full historical
manifests and source-bound dependency trees are retained. `MANIFEST.json` binds
all delivered payloads.

Run `python verify_package.py` for read-only bindings, dependencies and safety.
Run `python replay_checks.py` for disposable-copy lightweight/ordinary replays.
Python 3, SymPy 1.14.0 and mpmath 1.3.0 were used; no network is required.
Finite checks support, not replace, the included ordinary proofs.

The expensive whole global checker already passed its initial run and an
independent fresh-directory replay (316.10s and 280.47s), with byte-identical
canonical JSON. The auditor's terminal receipt is preserved and hash-verified;
packaging did **not** duplicate that operation. Its lightweight structural checker
is replayed on extracted copies. An explicit `--include-expensive-global` option
is available for a deliberate full rerun; timings are not canonical evidence.

`ORDINARY_METHOD_COMPARISON.md` credits existing methods and preserves the source
access boundaries. The sFSP manuscript timeout remains stopped. No induction-clock,
future corrector, accelerated simulator, or solver candidate is included in this
freeze. No external upload, publication, hardware action, or novelty clearance
was performed. No statement is extended to other rate choices or networks, and
no claim of all positive exponential moments is made.
