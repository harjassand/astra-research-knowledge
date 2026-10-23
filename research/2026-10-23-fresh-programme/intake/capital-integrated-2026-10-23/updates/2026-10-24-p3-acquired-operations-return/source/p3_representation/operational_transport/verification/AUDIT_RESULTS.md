# Exact operational-transport audit: results and handoff

Date: 23 October 2026. Native agent: /root/verification_primitive.

## Outcome

The stated open-loop transport theorem, conditional-fiber version, and
reversible-guard compiler are sound. Their assumptions are necessary in
substantive ways. The exact checker passed **88,818 checks**, with no failures
or reruns.

The complete proof is in
[OPERATIONAL_TRANSPORT_AUDIT.md](OPERATIONAL_TRANSPORT_AUDIT.md). It also
proves a worst-case source-acquisition lower bound of order T/eta for an
eta-accurate complete-path warrant at horizon T, including when every true
source map is a permutation.

The checker is an executable challenge of disclosed finite fixtures. It does
not establish priority, physical applicability, acquisition-optimality, or
advantage over a strong retaining program learner. Those claims remain
UNKNOWN or, for a universal advantage over that baseline, unsupported.

## Prospective scope and observed checks

[PLAN.json](PLAN.json) and [PRE_RUN_BINDING.json](PRE_RUN_BINDING.json) were
saved before checker execution. The binding was created at
2026-10-23T12:38:36.711503+00:00. All cases had been mathematically derived
and disclosed; this is not a hidden confirmation set.

| Group | Exact checks | Result |
|---|---:|---|
| Three-state open-loop transport | 71,442 | PASS |
| Guard mismatch-set identity | 16,384 | PASS |
| Guard reversibility iff product-control invariance | 64 | PASS |
| Single hidden error, exact horizon cardinality | 203 | PASS |
| Reversible two-error alternative, exact horizon cardinality | 168 | PASS |
| All query subsets for N=2,...,8 | 508 | PASS |
| Fiber chart, sampler, preservation, common parities | 29 | PASS |
| Required negative-control assertions | 15 | PASS |
| Scope/count checks | 5 | PASS |
| **Total** | **88,818** | **PASS** |

The transport check used a fixed noncommuting pair of candidate permutations,
every ordered pair of the 27 three-state functions, all 14 words of length
one through three, and all seven nonempty uniform-on-subset initial laws.
Of the 729 true-map pairs, 693 contain a nonpermutation map. There were
3,926 nonvacuous inequalities and 2,266 nonzero equalities in those
nonvacuous cases.

The guard check enumerated all four controls invariant under one fixed
two-bit translation and all sixteen guards. Exactly 36 of the 64 products
produce reversible maps. For each pair, every one of the 256 true maps was
checked against the exact identity
E_guard = E_base intersect {guard=1}.

The nonlinear four-bit chart fixture has two acquired direction vectors,
two independent parity constraints, and four exactly sampled four-state
fibers. One fiber separates into orbits of sizes one and three. This directly
demonstrates why an invariant fiber cannot be relabeled a reachable component.

The cycle checks verified full-path error T/N for a one-input defect and
(T+1)/N for a reversible output-swap defect. All 508 query subsets in the
specified small sizes obeyed the one- and two-alternative coverage counts
used by the information lower bound.

The negative controls retained in [RESULTS.json](RESULTS.json) show:

- One-step state-feedback failure probability one with per-action uniform
  error 1/4, even though the combined candidate is identity.
- A word selected from the initial state steering exactly into a rare error.
- Fiber-preserving but noninvertible compression invalidating the marginal
  audit budget.
- A conservation-only audit missing two-step escape probability one.
- A post-audit permutation refit agreeing at the sampled point but erring
  on three quarters of the space.
- Shared detector noise retaining pass probability 1/2 when an invalid
  independence calculation predicts 1/16.
- Unbudgeted retrying of one-sample audits producing false-warrant
  probability 1023/1024 after ten attempts.
- The exact additive transport budget exceeding an invalid product budget.
- A low-degree fit matching every fitting point yet missing a later
  degree-two observable on one quarter of a fiber.
- A globally small error concentrated in a selected fiber.

## Costs actually observed

One checker process was executed. It used Python 3.12.14 and standard-library
integer/rational arithmetic. No random simulation, physical measurement,
external source query, or new agent was used.

| Measured quantity | Value |
|---|---:|
| Wall time after standard-library imports, including results writing | 1.5787206829991192 s |
| CPU time on the same scope | 1.577493875 s |
| Transport enumeration | 0.9625320810009725 s |
| Guard enumeration | 0.5412925309938146 s |
| Horizon/coverage enumeration | 0.03586827700200956 s |
| Fiber checks | 0.0007245430024340749 s |
| Other counterexamples | 0.0007272469956660643 s |
| Results serialization and write | 0.035690219010575674 s |
| Peak traced allocation after imports | 1,432,091 bytes |
| Results size | 130,847 bytes |
| Failed checks / reruns | 0 / 0 |

Interpreter startup/import overhead and research, proof-writing, and tool
overhead are not included in that process timing. Exact serving-model,
token, and monetary usage are not exposed and are UNKNOWN. Raw process and
tool receipts are in [RECEIPT.json](RECEIPT.json) and
[TOOL_RECEIPTS.json](TOOL_RECEIPTS.json).

The source refuses to overwrite a prior result. Reproduction should copy
the bound plan/source to a separate directory, or deliberately use separately
named results; it should preserve this original run.

## Additional static refinement: retain the exact fitting addresses

Fresh audits are sufficient, but need not be acquisition-optimal. Suppose
the final candidate has been exactly checked against a deterministic source
on a retained set D inside S. Let q=mu(S minus D). All remaining error lies
outside D.

If q<=epsilon, an epsilon warrant is already deterministically valid.
If q=0, the source and candidate agree exactly on S. In particular, fitting
queries which cover an entire small fiber make a further statistical audit
unnecessary.

If q>epsilon and uniform sampling on the remaining set is available, an
audit there gives

\[
 \Pr(\mathrm{PASS}\text{ with }e>\epsilon)
 \le (1-\epsilon/q)^m.
\]

This follows because the conditional disagreement fraction is e/q.
Obtaining that sampler has a cost: rejection from S requires an average
1/q candidate draws, while direct rank/select or explicit complement
representations require their own preprocessing. Caching does not make
these costs disappear.

This refinement should be available to the strong retaining baseline.
It does not undermine the horizon lower bound: that lower bound charges
every earlier source query in the transcript, including retained fitting
addresses.

## Additional static obstruction: a strongly collapsing source cannot pass

The core theorem does not assume true measure preservation. It also does
not imply that every source admits a useful permutation approximation.
For any deterministic F:S -> X, put

\[
 K=|F(S)\cap S|.
\]

Then

\[
 \min_{P\text{ a permutation of }S}
 \mu\{x:F(x)\ne P(x)\}=1-K/|S|.                         \tag{A}
\]

Proof: any agreeing inputs must have distinct source outputs in S, since P
is injective. There can be at most K such inputs. Conversely, choose one
preimage for each distinct source output in S. Those K input-output pairs
form a partial bijection and extend to a permutation of S, attaining K
agreements. This proves (A).

For a source collapsing S to one state in S, every permutation candidate
has uniform error at least 1-1/|S|. The audit remains valid but has no
small-error candidate to certify. A scientific application with strong
dissipation must either find an appropriate expanded state/reference law,
use a different transport contract, or accept that this construction is
inapplicable. No such repair is supplied by this audit.

## Continuation recommendation

The bounded independent theory objective is complete. The parent can
continue warm with the end-to-end construction; no more finite enumeration
is needed to settle the present algebra.

The next useful investigation is a complete same-information acquisition
comparison on a scientific operation with available reset/read access,
nontrivial acquired fibers, and a downstream task that actually benefits
from those fibers. Include direct source rollouts, retained exact fitting
addresses, and the tailored retaining program/library baseline. The decisive
remaining uncertainty is scientific applicability and total acquisition cost,
not the proven finite-state composition inequality.

No background execution is implied by completion of this audit.
