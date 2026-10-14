# FL ancestry information result

**Status:** internal mathematical derivation and exact finite support check. The result is conditional on the supplied labeling assumptions. No experimental data, external proof review, novelty finding, or catalyst advantage is claimed.

The exact information boundary is now clear. If the actual heavy-label probability can be programmed throughout a nontrivial interval of values at every relevant age, the product-time clock is aligned, the label channel is calibrated, and every whole-product isotope-count probability is known exactly, then arbitrary controls identify the complete *unordered* law of the \(n\) carbon entry times. The top-count probability alone is the diagonal homogeneous polynomial \(H[p]=\mathbb E\prod_i p(A_i)\); polarization recovers the symmetric \(n\)-time law.

A finite experiment has a different boundary. Its count histograms measure a finite set of linear functionals of that law. A decision statistic is identifiable exactly when it lies in the span of those response functions. Otherwise an exact finite-support pair of ancestry laws produces every observed histogram identically but changes the target. On a five-node grid with four atoms, arbitrary laws have 70 unordered histories; 18 one-time whole-count readouts are necessary by dimension alone, and 70 unisolvent interval-valued top-bin queries suffice in exact arithmetic. Neither count includes precision or calibration cost. A finite control start also leaves any earlier constant-composition inventory exactly unidentifiable.

If controls are restricted to the source's two isotope levels, even all possible binary waveforms need not identify the full law. An exact six-atom, three-age-bin countermodel gives identical whole-product count histograms for every binary mask while the unordered ancestry laws differ. The telegraph code still acquires its selected \(Q_n(r)\); this restriction limits full-law reconstruction, not that specific identity.

The telegraph protocol is useful because it directly acquires one selected functional,
\[
Q_n(r)=\mathbb E e^{-2rL_n},
\qquad L_n=\sum_j(A_{(2j)}-A_{(2j-1)}),
\]
from the whole-product count parity. It does not identify the full ancestry law. At one \(r\), it gives one scalar; across every \(r>0\), it gives only the distribution of \(L_n\). Common shifts of all ages are invisible to this stationary-code statistic.

With a complete code known and \(N\) independent product draws, the corrected weight is bounded by \(B_n=((1+|b|)/a)^n\), giving a product-sampling variance term at most \(B_n^2/N\). This centers on the code-conditioned mean; shared-code variability and real reaction/detector covariance remain separate. I re-derived the parity identity and this sampling term, but did not independently audit the source note's separate geometric bound for shared telegraph-code variance.

The known-scale four-carbon E/O construction does not establish superiority over arbitrary isotope programs. For any deterministic normalized waveform \(u\), the full count-generating-function contrast is
\[
G_E(z)-G_O(z)=\frac{a^4}{128}(z-1)^4\prod_{k=0}^3(u_k-u_{k+1}).
\]
A single step or rectangular pulse has at most two boundaries across the five age nodes and gives identical whole-product count laws. A square wave with \(u(t-\tau)=-u(t)\) attains the maximal corrected parity contrast of 2, for any common delay \(C\). At \(a=0.98\), the ideal one-product even/odd classifier error is 3.8816%. The supplied telegraph setting gives only 0.1161 corrected contrast. This is an exact counterexample to ranking the telegraph code above a scale-tuned waveform on the synthetic laws; it does not compare total real-world cost.

A consequential result still needs two physically credible catalyst histories that survive optimized pulse, multipulse, periodic, nonlinear isotope-frequency and spectroscopic baselines; a selected ancestry functional that differs beyond measured uncertainty; and an explicit catalyst or process action that changes because of that difference. The four-carbon E/O laws are not fitted to a catalyst. The source packet has no actual boundary waveform, whole-product response matrix, campaign covariance, or action map.

The detailed proof, finite-span theorem, gauges, prehistory witness, and arbitrary-waveform E/O formula are in [IDENTIFIABILITY.md](IDENTIFIABILITY.md). Exact rational checks and finite outputs are in [finite_checks.py](finite_checks.py) and [finite_results.json](finite_results.json). The independent check covers all 14 proper E/O coordinate marginals, all 32 binary five-node masks, every mask with at most two internal switches, and the square-wave count laws at \(a=49/50\). It is finite evidence for this fixture only.

## Inputs that remain charged

A physical result would require the actual isotope waveform at the declared feed boundary, including mixing and dead volume; calibrated low/high isotope purities; constant chemical feed and isotope-neutral ancestry; prehistory, washout, and residual old carbon; stationary product selection; full parent-product isotope-count detection with natural-isotope, fragment, response, background, and normalization corrections; finite switching bandwidth; and measured product-level covariance. The estimator consumes the summary count bins \(P(K=0),\ldots,P(K=n)\) for each program; it does not observe carbon positions. Raw ion counts are not automatically independent product samples and must be mapped through the calibrated parent-product channel before being treated as those bins.

The observable concerns entry through the declared feed boundary. It does not automatically measure surface residence, bond-formation time, or a spatial location. The full-control polarization theorem is an ideal identifiability statement. Real finite programs recover only their response span, and imperfect purity amplifies the telegraph parity statistic by \(((1+|b|)/a)^n\).

## Prior-control boundary

The [Hartfelder et al. isotope-frequency-response paper](https://doi.org/10.1039/c2an35903k) has an accessible abstract that reports isotope-composition modulation under quasi-steady conditions with a linear response. Its full publisher paper was not retrieved, so no priority conclusion is made about nonlinear parity or its exact equivalence to earlier analyses. The [H-ZSM-5 isotope-pulse study](https://doi.org/10.1021/acscatal.3c00168) reports sequential labelled/unlabelled methanol pulses with online MS and fast-scanning pulse GC in its [institutional article record](https://research.tudelft.nl/en/publications/revealing-main-reaction-paths-to-olefins-and-aromatics-in-methano/). These papers support including frequency-response and pulse methods in the comparator set; they do not supply matched costs for this proposed whole-product statistic.

No N786 or N790 bound is transferred. Their original information contracts were read and differ from this isotope-control/count interface.
