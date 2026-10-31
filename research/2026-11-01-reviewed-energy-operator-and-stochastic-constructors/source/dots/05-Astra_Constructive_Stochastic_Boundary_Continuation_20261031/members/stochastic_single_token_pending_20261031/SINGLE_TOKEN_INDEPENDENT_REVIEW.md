# Independent review: single logical first-hub token

## Verdict and binding

**ACCEPTED as the stated first-hub clock comparison and safe substitution into
the already accepted protected-family constructor.** This is not a replacement
for the simultaneous support-coverage table and not a new unrestricted stability
theorem.

| Object | SHA-256 |
|---|---|
| `SINGLE_TOKEN_COMPARISON.md` | `19f78190c698a2a7d1b61dc1aff406c353b4c5b9d73ecdf99d5048c30bfaa699` |
| `compare_clock.py` | `612f9794034f4800fd1955e54d7a6c2b64e5593389a305d43966d92043ce9602` |
| `results.json` | `af14664be7eb1d668f608f2332ef04e204677784e2d311bc2de93ce4a0d21f33` |

The comparison imports the adjacent accepted `protected_boundary.py`, bound to
SHA `5b1c44fb4c1cc8c748463a37b7272edba02aca9f0da4fd379d4c76d60a7e59eb`.
This dependency was checked and not edited. Frozen copies, byte-identical replay,
independent clock/coupling checks and hashes are in `independent_audit/`.
The audit script also uses the already bound independent protected-family
verifier to recheck the complete original patch certificates. This is a local
comparison with explicit adjacent-package dependencies, not a claimed standalone
application.

## Mathematical comparison

When absent, the logical token accepts the next immigration. When at inactive
phase i, it follows protected conversion events at rate k_ij and protected death
at rate d_i, while ignoring other arrivals. The remainder rates are
k_ij*(y_i-1) and d_i*(y_i-1), which are nonnegative because presence of the token
implies y_i>=1. The remainder cannot remove the last actual support of its phase.

Every positive-count-preserving extra transition leaves at least one actual
survivor in any phase it decreases. Therefore an existing logical token can
remain at that phase, relabeled onto a survivor. This is a valid coupling of
**unlabeled count processes**, not an assertion that a fixed physical individual
or immutable independent lineage survives nonlinear removal. Increases and
transitions in other coordinates do not compromise the token's support.

The actual-count marginal is unchanged and the logical marginal is autonomous.
At logical absorption into a hub, that hub is actually occupied, so first actual
hub activation occurs no later. Starting absent is valid from every initial
actual population. Earlier actual hub visits caused by ignored arrivals only
improve this inequality.

The finite token states are absent plus the inactive phases. Its matrix is the
linear core killed at H, with arrivals ignored while a token is present. Strong
connectivity through0 supplies a path to H from every token state, including
possible death back to absent followed by immigration. The finite killed system
is transient and its solved mean from absent is a genuine uniform first-hub
bound. In the protected-family application, standalone core nonexplosion was
already independently obtained from the tail before this clock is used.

## Exact implementation and replay

The independent audit reconstructs the single-token matrix directly from the
raw linear reactions, checks all hitting equations and positivity, and verifies
graph reachability to absorption. The comparison was replayed at its original
path with its bound dependency and reproduced `results.json` byte-for-byte.
Only in-memory function substitution was used; functions were restored and no
accepted source file was modified.

Both binary-based patch certificates were independently reverified in full.
For each single-token substitution, every returned field except activation
clock, termination witness and work metadata was compared for literal equality.
The changed one-sided excess and scalar termination inequality were then
independently checked using the single-token bound. Thus actual patch equations,
trial decisions, head values, fringe tests, epsilon and Foster C were not merely
assumed insensitive to this substitution.

| Input | Binary / single clock dimensions | Binary / single mean | Actual patch |
|---|---:|---:|---:|
| Frozen positive-cycle demo | 4 / 3 | 24 / 24 | R=4, head10; identical |
| Parallel arrivals | 4 / 3 | 5/4 / 3/2 | R=17, head153; identical |

The second case correctly demonstrates that smaller clock dimension does not
imply a better mean bound. The mean calculations are exact, not simulations.
Both conservative scalar radii also replayed as reported.

An independent local coupling audit checked **3,250 joint count/logical-token
states** and **38,300 split event terms**. It included **250 enabled nonlinear
survivor-decrease events**: service counts reached4, so the actual 4A->A channel
was exercised. Actual-count marginal rates, autonomous logical rates and
presence of actual support under each nonabsorbed token all checked exactly.
These finite checks supplement the ordinary coupling argument above.

An altered clock mean was rejected. A two-state clock budget returns UNKNOWN
when the required system has three states. No instability or universal resource
advantage is inferred.

## Scope

The clock is for **first occupation of any hub**, not simultaneous occupation
of enough hubs to cover multiple satellite directions. The one-token state
cannot itself encode that latter target. The accepted tilted-support coverage
theorem and its very large compact constants remain separate and unchanged.

The comparison does not claim historical novelty, a universally tighter mean,
independent immutable particle survival, or an uncharged speedup of the full
constructor: the actual head search and its exact arithmetic still cost work.
All work was local mathematical verification; no upload or external action was
performed. This closes the requested comparison without extending the theorem
family further.
