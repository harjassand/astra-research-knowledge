# Sampling geometry: event-promotion action profile

**Status:** internally reconstructed mathematical note; no novelty or priority claim. The event-promotion action curve is already covered, in dual form, by Blanchet–Murthy for general Polish-space baselines and closed events. This note retains it as an accounting coordinate, then separates that coordinate from conditional-law fidelity.

## Candidate and decision

The candidate operation takes a baseline law, an event, and a cost for transporting one state to another. It returns the least expected transport action needed to make the event occur with a requested probability. The exact answer is the integral of the lower quantiles of the cost-to-event under the baseline law.

The early novelty gate failed twice. Chen, Kuhn, and Wiesemann's Theorem 2 gives the exact empirical version. Blanchet–Murthy's Theorem 1 and Section 2.4 already give the general-law, general-transport-cost robust event probability, including path-dependent first-passage applications. The note does not present the action curve as a new rare-event theorem or algorithm. Its useful output is a direct cost-profile proof and an exact separation between event promotion and conditional-sampler quality.

## Exact interface

Input: a baseline sampler; a measurable event; a measurable transport or path-action cost; a certified cost-to-event function; and an approximate map into the event that realizes this cost within a stated tolerance. The threshold and tie rule selecting the cheapest requested amount of baseline mass are acquired inputs. Their acquisition and evaluation costs must be counted separately.

Output: an induced law with at least the requested event probability, or the exact infimal action required of every such law. The minimum expected cost is the submeasure minimization in [the note](action_profile.md). Under the measurable approximate-realization condition, it is exactly the infimum of transport cost over all laws with at least the requested event mass.

## Hard limits

The action profile certifies only the cheapest event-mass promotion in the chosen cost geometry. It does not certify that the proposal's event-conditioned law resembles the target's event-conditioned law, that an importance sampler has bounded relative variance, or that a path edit remains dynamically realizable. A finite example in the note keeps the proposal acceptance fixed and makes the transport action arbitrarily small while the conditional chi-squared divergence, and hence relative variance, grows without bound.

For a physical or path-space application, the metric or action, map, cost-to-event oracle, quantile certificate, sampler, and conditional-fidelity certificate must all be supplied and costed. If reaching the event requires solving the original rare-event dynamics, the formula is an accounting identity, not a computational shortcut.

## Files

- [action_profile.md](action_profile.md): definitions, theorem, proof, acquisition interface, examples, and failure tests.
- [source_audit.md](source_audit.md): primary-method inspection and prior-art boundary.
