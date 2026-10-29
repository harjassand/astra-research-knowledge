**The strongest advance is now a separation between statistical evidence and physical reversal information—and a theorem showing how an additional operation can cross that separation.** I developed a sharp certificate that constrains every compatible hidden model, acquired a numerical instance, then pursued the physical ambiguity exposed by that certificate into an exact impossibility result and a constructive intervention theorem.

The scientific destination is a theory of **which information makes a consequential physical claim identifiable**, with observation, preparation, intervention and precision included in the statement. The previous mean records, positive representatives, clock criteria and directed composition remain intact.

## A certificate across hidden dimensions

For a finite stationary continuous-time Markov chain whose microscopic states are **even under physical time reversal**, equilibrium observations satisfy a nonnegative Gram constraint. Certain matrices of return events, lagged observations or reflected histories must have the form

\[
C=\sum_k v_kv_k^\mathsf T,\qquad v_k\ge0.
\]

This is the classical *completely positive* cone. It is stricter than positive semidefiniteness. The underlying positive Markov factorization is established mathematics; the construction here combines it with a quantitative comparison of microscopic forward and reversed path measures. The geometric generator used in that comparison is also an established entropy half-tilt. :chatgpt-content-reference{index="0"}

Let \(H\) be a supplied **copositive witness**, meaning \(x^\mathsf THx\ge0\) for every nonnegative \(x\), and let \(h_-=\max(0,-\min H_{ij})\). For a normalized lag or reflected-history record of duration \(t\), the resulting theorem is

\[
\boxed{\displaystyle
\sigma\ge
\frac{4[-\langle H,C_{\rm sym}\rangle]_+}{t\,h_-}.
}
\]

A corresponding native-excursion theorem bounds entropy **per departure**. Neither exact theorem requires a hidden-state-count bound or a microscopic clock ceiling. The coefficient \(4\) is sharp in the excursion class.

The demanding example is a fifteen-state source whose **entire observed port/interior process is time-reversal symmetric**, and whose return kernel is positive definite, yet violates the nonnegative Gram condition. Visible reversal asymmetry and ordinary positive-semidefinite tests both miss this violation.

The proof, its extensions and their limits are in :chatgpt-content-reference{index="6"}[COPOSITIVE_PATH_CERTIFICATES.md](producer-workspace/COPOSITIVE_PATH_CERTIFICATES.md).

## An acquired certificate, with its costs retained

The numerical native assay retained **262,144 individual excursions**, requiring the same number of reset preparations, **524,288 native jumps**, and **384,505.59294931183 native clock units**.

Reusing its full positive-duration endpoint record gives the simultaneous certificate

\[
\frac ER\ge0.22322365
\quad\text{nats per departure},
\]

\[
\sigma\ge0.14297416
\quad\text{nats per native clock unit},
\]

with failure allowance at most \(1/1000\). The stronger reuse required no additional source observations.

The consumer used only the public instrument contract and retained observations. An independent reconstruction of the raw record and confidence arithmetic was completed **before** inspecting private source truth.

The substantive conditions remain attached: resolved microscopic ports, flux-weighted resetting, independent repetitions, calibrated port clocks, direct-jump markers and timestamp intervals. The bounded per-departure score needs no lifetime-tail bound; conversion to a rate per time uses the supplied tail envelope. This is a synthetic floating-RNG acquisition with an ideal-law statistical guarantee, rather than a physical calibration or a complete floating-point sampling-law proof.

**The strongest conventional method remains stronger on the exact population example.** Skinner and Dunkel already established hidden-network entropy minimization and inference from time-symmetric observations. Their machinery recovers the population optimum here, approximately \(0.17389808\) per native time, compared with \(8/47\approx0.17021277\) from the linear population certificate. :chatgpt-content-reference{index="1"}

The prospective addition is the explicit, dimension-independent witness and its acquisition guarantees. I have established no full-task speedup over equally informed hidden-model optimization.

## The physical ambiguity became an exact theorem

The acquired record does **not** determine the correct microscopic time-reversal convention. The same example has zero generalized entropy when reversal swaps its paired hidden states.

I pursued this beyond the example. Starting from any finite irreducible source with a reciprocal complete native-return law, the construction keeps every resolved port as one state and doubles only the hidden interior into forward and reversed copies. It produces an exact generalized-equilibrium completion preserving:

- The complete native return-time and endpoint law, including reciprocal direct-port events.
- Known singleton-port resets and arbitrary concatenations of excursions.
- Native port holding rates and every escape-rate ceiling.
- Total stationary mass.

The completion uses at most \(|B|+2|I|\) states. Independent rational checks verified the construction, including nonuniform stationary weights and twenty Laplace-kernel identities.

Consequently, **unlimited observations through that same reciprocal native interface cannot universally distinguish hidden dissipation from generalized-reversible transport**. A physically justified all-even source class excludes the alternative; the baseline observations alone do not establish that class.

There is also a sharp fixed-horizon statement. If hidden parity is unrestricted, then for a stationary visible law \(P\) from a finite source,

\[
\inf_{R\in\overline{\mathcal E_{\rm parity}}}
\operatorname{TV}(P,R)
=
\frac12\operatorname{TV}(P,P^{\rm rev}),
\]

where the closure contains visible laws of finite irreducible generalized-equilibrium models. The forward/adjoint lifting ingredient is established; the observation consequence and the exact port-preserving construction are the claims developed here. :chatgpt-content-reference{index="2"}

These are abstract model-class results. They do not construct a native passive physical device or invalidate the qualified all-even certificate.

## An additional operation restores the constraint

The positive response to that failure is a **midpoint parity-operation theorem**.

Suppose the true microscopic reversal operation \(\Theta\) is independently known and can be applied at the midpoint of a fixed observation horizon. Assume stationary preparation, \(\pi\Theta=\pi\), and an observation map compatible with reversal. Evolve under the same generator \(Q\) before and after the operation.

At generalized equilibrium, the controlled endpoint matrix again becomes a nonnegative Gram matrix. For arbitrary \(Q\), the same geometric-path comparison gives

\[
\boxed{\displaystyle
\sigma_\Theta\ge
\frac{4[-\langle H,C_{\Theta,\rm sym}(t)\rangle]_+}
{t\,h_-}.
}
\]

The additional operation supplies information that identical baseline samples cannot provide. Its action on hidden states must be calibrated; assigning a reversal label to a fitted model does not supply that access.

The proof also makes precision consequential. If the actual endpoint law is within total variation \(\nu\) of the ideal experiment, the witness loses at most

\[
(\max H-\min H)\nu.
\]

A sufficient error budget includes preparation error, pulse error, readout error and a timing term \(2\Lambda\kappa\), where \(\kappa\) bounds midpoint error and \(\Lambda\) bounds native escape rates. Without a rate or continuity bound, a small clock error has no uniform guarantee.

Independent review passed the full path-reversal argument, the holding-rate terms and this calibration treatment. An exact six-state control with odd hidden variables retains a positive corrected population certificate under a stated pulse-and-readout error budget. **No native parity operation or finite-sample acquisition was executed for that new interface.** The pulse apparatus’s implementation cost remains separate from the generator’s intrinsic generalized entropy.

Echo constructions themselves have substantial precedents. In particular, freely redesigning reverse dynamics can produce echoes for nonequilibrium systems; the present theorem fixes the physical operation and leaves \(Q\) unchanged. :chatgpt-content-reference{index="3"} The candidate contribution is the controlled endpoint certificate and its explicit information and precision contract.

The complete construction is in :chatgpt-content-reference{index="7"}[REVERSAL_INFORMATION_AND_INTERVENTION.md](producer-workspace/REVERSAL_INFORMATION_AND_INTERVENTION.md).

## Preserved continuation

The full continuation contains the ordinary proofs, both native acquisition records, executable controls, independent reviews, conventional comparisons, source receipts and useful failures:

[:chatgpt-content-reference{index="5"}](https://chatgpt.com/library?file_id=libfile_627b517495c88191a4b6d005d8b6ed17&account_id=personal)

The earlier complete snapshot remains unchanged. The present frontier is a physically warranted source class or a feasible calibrated operation that makes these certificates consequential beyond synthetic models. Passing selected nonnegative-Gram tests also remains weaker than constructing one finite equilibrium model consistent with the entire observed process.