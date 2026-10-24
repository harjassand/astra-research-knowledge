# Retained-trajectory acquisition: stopping and budget audit

This audits the zero-initializer refinement in `RETAINED_CONTEXT_ACQUISITION.md`. It uses one retained trajectory, a fixed public control schedule, noisy QND reads while the clock is held, and `UNKNOWN` on any row-coverage deficit. It does not assume a visit-frequency lower bound.

## Why the first-m bound survives adaptive visitation

For a row (r=(i,a,z)), let τ_{r,k} be the time of its (k\)-th update whose pre-update context is (z) and whose scheduled mode is (a). On the event that all majority reads through the public cap are correct, these are exactly the visible row assignments. The event that a time is a row visit is decided from the pre-update state and public schedule, before the current transition noise is drawn. For the true post-update bit Y_{r,k}, the supplied local Markov promise therefore gives
\[
 \mathbb E[Y_{r,k}\mid\text{history immediately before that update}]
 =p_i^a(z).
\]
Thus the response bits at successive visits are a bounded martingale sample with a constant conditional mean. They need not be iid, and no stationary distribution or mixing-time bound is needed for the confidence bound *if the visits occur*.

To include noncompletion correctly, extend the row sequence after the finite cap with proof-only independent Bernoulli\((p_i^a(z))\) bits whenever a further visit does not occur. At each row slot, whether an actual visit supplies the bit is determined before that slot's response; the padded length-(m) sequence still has conditional mean (p_i^a(z)). If the row is complete, all (m) bits are physical observations. Hoeffding-Azuma then implies
\[
 \Pr\!\left(N_r(T_{cap})\ge m\;\text{and}\;|\hat p_r-p_r|>w\right)
 \le 2e^{-2mw^2}.
\]
This is a joint completed-and-bad bound. It does not condition on eventual visitation or successful stopping.

For the sensor, the required contract is explicitly supplied in the refinement: conditional on the fixed true bit and the complete previous history, each read has error probability at most (e_s<1/2); the native clock holds the bit fixed during all reads. Azuma-Hoeffding gives one odd-(r\) majority error at most
\[
 \exp[-2r(1/2-e_s)^2].
\]
There are at most (T_{cap}(|C|+|B|)) majority decisions. A union bound controls every pre-round context and post-update response label, without assuming different decisions are independent. On the event that none is wrong, the observed row visitation/stopping rule is the true-context rule. Dependence between sensor errors and transition noise does not invalidate the final union bound.

For (M=|B||U|2^d) required rows, the resulting familywise statement is precisely, provided the stated interval-to-influence calculation is applied as written,
\[
 \Pr(\text{algorithm returns an invalid table or contraction certificate})
 \le T_{cap}(|C|+|B|)e^{-2r(1/2-e_s)^2}
       +2M e^{-2mw^2}.
\]
If a row is missing, the algorithm returns `UNKNOWN`; missing rows are not imputed. This does **not** bound the probability of `UNKNOWN`, nor does it imply a conditional-on-return confidence level. A rare, frozen, or unreachable context can make successful return arbitrarily unlikely. The fixed public schedule and the real visit log must establish coverage in each execution.

## Numerical cap and honest resource ledger

For the proposed values
\[
 m=2500,\quad w=0.05,\quad r=81,\quad e_s=0.1,\quad
 T_{cap}=100000,\quad |B|=15,\quad |C|=17,\quad |U|=2,\quad 2^d=8,
\]
the row count is (M=240). The response-estimation term is
\[
 2M e^{-2mw^2}=480e^{-12.5}\approx 0.0017887935.
\]
The sensor term is
\[
 T_{cap}(|C|+|B|)e^{-2r(1/2-e_s)^2}
 =3{,}200{,}000e^{-25.92}\approx 0.0000177108.
\]
Thus the unconditional upper bound on returning an invalid table/certificate is approximately (0.0018065043) (about (0.181\%\)). It is not a success-probability estimate: no visitation floor is assumed, and the probability of returning `UNKNOWN` is unquantified.

At the cap, the physical budget is:

- 100,000 synchronous rounds on one retained trajectory;
- at most 1,700,000 local update pulses on (C);
- 3,200,000 majority decisions and 259,200,000 raw sensor reads (137,700,000 before-round context reads and 121,500,000 post-update reads);
- at most 600,000 accepted response observations for the 240 rows (only running counts and sums need to be stored); and
- row counters and success counts requiring about 5,760 bits at 12 bits each, before keys, interval arithmetic, logs, and program storage.

All read/hold latency is a real cost. If reads are serialized, the cap incurs 259.2 million read-time units; if sites read in parallel, wall-clock cost depends on the actual parallel sensor/clock implementation and must be reported separately. No per-read duration is specified here, so this audit does not convert the count to seconds. The sensor term assumes all reads can be scheduled while the native state is held and that the held-cell promise is physically true.

This is a budget calculation, not an executed replay. Without an actual trajectory and its row-visit log, it cannot establish that the 240 rows fill by round 100,000. A replay should report the observed first-hit/coverage time for every row, the final `RETURN` or `UNKNOWN` state, raw read and update counts, and any guard/contraction margin; no synthetic coverage frequency should be substituted.

## Event precision and matched baseline

Once a table is valid, its simultaneous intervals feed the local influence upper bounds and the stated finite-guard coupling certificate. For a physically sampled future event on the retained system, repeat trials need only satisfy the certified conditional-mean bound; a bounded-difference martingale gives the future sampling term without an iid claim. If the event probability is instead computed from the fitted rows, a path with (J) local transitions adds at most (Jw) transition-kernel error by stepwise coupling, in addition to preparation TV and readout uncertainty.

An equally informed retained-state local-table learner receives the same single trajectory, public schedule, all noisy reads and update outcomes, and the same time/cap budget. It can use adaptive row allocation and anytime martingale intervals, while returning `UNKNOWN` if its required rows remain unvisited. It can also apply the same Dobrushin/coupling argument. This construction removes acquisition-time full initializations; it does not remove visitation dependence or establish a learning advantage over that comparator.
