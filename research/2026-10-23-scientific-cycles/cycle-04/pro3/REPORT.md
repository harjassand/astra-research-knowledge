# The vanishing-screen coefficient is now sharp

Astra PRO3, 22 October 2026, Australia/Brisbane.

The incoming killed-operator upper proofs are accepted. A new symmetric
branching-tree lower matches them, closing the finite-positive-class
accuracy-policy coefficient:

\[
 \lim_{\varepsilon\downarrow0}\varepsilon\log T_{\rm policy}(\varepsilon)
 =\max\left\{K,\frac1{d c_*}\right\}.
\]

Here the screen remains fixed throughout each run,
`eta(epsilon)/(epsilon log(1/epsilon))->d` in (0,infinity), beta=1-alpha,
and c_*=1 when alpha exp(-K)>=beta; otherwise it is the unique root of

\[
 c_*(1-c_*)^{(1-c_*)/c_*}=\alpha e^{-K}/\beta.
\]

At K=1,alpha=1/2,d=1 the coefficient is **1.542211419737745...**. The
preceding lower 1.0884827657... was a valid path bound but did not describe
the worst symmetric geometry. The exact implicit expression, not numerical
root precision, defines the result.

## Why the new construction matters

The incoming upper improved the proof by coupling local transport with the
global escape in the actual killed operator. It also showed that its uniform
strict one-step q-power norm method cannot exceed c_*. That obstruction did
not itself show poor mixing: its test vector need not be reachable from q,
and its amplified state was not a long-lived trap.

The new construction supplies those missing properties. On a rooted D-ary
tree, put Q=1/(D+1) in both directions of every edge. Each interior vertex
has one parent and D children. The full proposal is symmetric, but aggregate
forward mass is D/(D+1), approaching one. A line graph had only one half.

The root holds a fixed substantial proposal mass b, while proposal mass
shrinks rapidly down the tree. Target mass instead increases down the tree
but stays tiny until a terminal high-weight leaf set. Most target mass lies
at a separate star state. The entire forward KL tends to -log(1-b)<K. All
laws are finite, strictly positive and normalized; support grows explicitly.

At level i there are D^i vertices. Dividing both level masses by D^i leaves
likelihood weights unchanged, but it changes the actual local acceptance
ratios. This distinction is essential. The forward screen is `(z/D)^eta`;
reverse acceptance is `D n^-2 (z/D)^eta`. After counting children and the
single parent, forward mixture mass is f and backward mass is f/n². Exact
lumping retains same-level global moves as holds. The proof charges every
other global/local exit, bounds the time required for successive forward
captures, and keeps the entire leaf union until the horizon.

The resulting capture exponent is

\[
 \phi_r(v)=\frac{\log(1+r e^v)}v,\qquad
 r=\frac{\alpha(1-b)(D+1)}{\beta D}.
\]

Its infimum approaches c_* when b approaches its admitted entropy boundary
and finite D grows. For every strict bound, all parameters are chosen before
the horizon tends to infinity. This is an actual adverse family for the
native chain, with its returns and rejection probabilities intact.

The same construction establishes a more detailed risk statement. For
`eta_n log n/loglog n ->lambda` in (0,infinity),

\[
 \frac{-\log R_{\eta_n}(n)}{\log\log n}
   \longrightarrow\min\{1,\lambda c_*\}.
\]

Below lambda=1/c_*, the risk is asymptotically larger than 1/log n. Above
that threshold its coefficient is K. At equality the logarithmic power
is determined but the leading amplitude requires a finer argument.

## A further result at that finer boundary

The next question was begun in the same checkpoint. When
`r0=alpha exp(-K)/beta<1` and

\[
 \eta_n\log n=\frac{\log\log n}{c_*}+s+o(1),
\]

the separately proved lower is

\[
 \liminf (\log n)R_{\eta_n}(n)
 \ge\max\{K,(1-e^{-K})e^{-c_*s}\}.
\]

This uses controlled degree growth D_n of order u_n², KL slack of order
u_n^-2 and the optimal integer depth. The first derivative with respect to
depth vanishes at the variational optimum, reducing its rounding loss from
O(1) to O(1/u). Cumulative screening, timing and retention errors all vanish.

This is a lower bound, not an assertion that the displayed envelope is the
exact critical law. The chosen next investigation is to determine whether
that law exists and equals this envelope, or whether a heterogeneous
transport geometry produces a larger amplitude. A successful upper must
control reachable first-hit mass at the endpoint, keeping constants and
the single KL budget; retuning a strict one-step norm is insufficient.

## Checks, sources and ordinary comparison

The principal read and accepted both incoming proofs. A distinct contributor
developed the tree lower, which the principal read in full. An independent
challenger checked the principal main proof and the critical refinement,
binding both verdicts to their exact source hashes. These are internal
mathematical checks, not proof-assistant certificates or external acceptance.

The independent finite test reconstructs a 22-state rational tree and its
four-state quotient. It checks native proposal symmetry, detailed balance,
all twelve-step laws, TV equality and an exact KL bound below one. The
principal additionally froze and evaluated five rational admitted families.
Their probabilities, kernels, KL inequalities and finite lower bounds use
exact fractions. Decimal binary matrix powers at 80 and 120 reserved digits
agree to over 70 relative decimal places across 145 values.

The largest implicit diagnostic graph has 69,810,262,082 states but eight
quotient states. It was calculated through a proved symmetry reduction;
no enormous target table was materialized and no 2^680-step trajectory was
executed. The finite checks validate formulas and arithmetic, not the
asymptotic theorem. Exact inputs and full code are included.

Pure IMH already has sharp coefficient K. At K=1,alpha=1/2,d=1, the new
theorem therefore establishes a worse worst-case exponent for the weakly
screened hybrid. All five diagnostic examples also favor pure IMH, including
at n/4 steps, which matches the hybrid's expected global proposal attempts.
This last comparison does not match cache misses or measured target costs;
it is not a runtime benchmark. Initialization, proposals, uniforms, q ratios,
target calls, cache memory and numerical precision are accounted for in the
contract, with unavailable costs explicitly unknown.

The local sampler is an established delayed-acceptance factorization; the
contribution is the sharp robustness analysis and its explicit adverse
geometry. The relevant primary references and the exact closest incoming
theorem are identified in `SOURCES.md`. Historical originality is not
established by this limited source check.

## Failures and observed resources

The initial tree sketch omitted the factor D in reverse acceptance. Both
contributors identified it before the complete proofs were written. The
delivered proof retains it and preserves the other critical distinctions:
per-vertex versus level probabilities, full-state versus quotient exits,
all-child capture versus one selected ray, and leaf-union retention.

One principal invocation completed its numerical work but failed while
serializing a fraction exceeding Python's default integer-to-string digit
limit. A bounded allowance repaired serialization. Its source and partial
output remain preserved; the later 80-digit output is byte-identical. No
mathematical case or gate changed. That failed invocation's unrecorded body
time and peak memory remain unknown.

The successful principal runs took about 2.8833 and 3.5986 seconds of measured
body wall time, at 80 and 120 reserved digits respectively, with 2,882 small
matrix products and 15 row products per run. Peak recorded RSS was 13,056
and 12,032 KiB. The independent exact checks took about 0.0231 and 0.0242
seconds. These are calculation costs, not discovery costs. Full inference,
token, monetary and historical programme costs are unknown. The archive
records observed checkpoint spans separately from numerical runtimes.

## Preservation and handoff

The complete incoming capsule, its unchanged 831,074-byte original owner
archive, earlier proofs, code, rejections, query records and receipts remain
preserved. The B3 pISO correction remains alongside the failed full halo
acceptance gate; the metadata and R3/anMC cases remain closed. No protected
other-owner programme, halted Morrey work or closed physical/guide method
was restarted. No purchase, public sharing or outreach occurred.

The private handoff contains this report, complete proofs, source-bound
reviews, exact input laws, executable checks, failures and cost records.
`README.md` gives receiving and replay instructions. The separate delivery
receipt records exact ZIP identity and private readback. Delivery does not
mean Max has read, scientifically accepted or integrated the result.
