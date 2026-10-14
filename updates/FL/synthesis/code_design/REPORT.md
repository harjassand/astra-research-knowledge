# FL code design: finite-slew limit and target-matched result

**Scope and status.** This is an independent mathematical and numerical analysis of the supplied four-carbon even/odd (E/O) ancestry example. It is not a fitted catalyst model, experimental result, external proof review, novelty finding, or technology claim. The result addresses a concrete missing comparison: how much of the known-scale square-wave advantage survives finite isotope-switching slew, and what can be guaranteed when the ancestry scale is unknown or multiscale.

## Result

For the E/O benchmark with actual feed purities $p_{low}=0.01$, $p_{high}=0.99$, let $a=0.98$ and let $\tau$ be the equal spacing in the four synthetic age choices. I derived the exact total-variation distance between the complete five-bin carbon-count distributions for any measured deterministic isotope waveform. At fixed output phase it is the product of the four feed-probability differences across the adjacent age choices. Thus the full isotope-count histogram cannot recover information that the input waveform did not put across all four gaps.

For a code that remains phase-robust under an unknown common delay, the natural matched condition is $u(t+\tau)=-u(t)$, with $p(t)=(1+a u(t))/2$. If the **measured feed waveform** has maximum normalized slope $M$, the largest achievable averaged fourth-order signal within this target-matched class is

\[
q_{max}(M\tau)=\begin{cases}(M\tau)^4/80,&M\tau\le2,\\1-8/(5M\tau),&M\tau\ge2.\end{cases}
\]

It is attained by maximum-slew linear ramps, with plateaus when the bandwidth permits and a triangular wave below the plateau threshold. The actual one-product histogram distance is $a^4q_{max}$, and the model parity means differ by $2a^4q_{max}$. This quantifies the bandwidth cost rather than assuming instantaneous switching.

This is a target-specific optimum among phase-robust antiperiodic codes. It does not supersede the supplied result that a tuned square wave beats telegraph coding on the known-scale example. It refines that comparator for finite transitions and gives an acquisition limit for missing age-scale information.

## Numerical comparison at the supplied contrast

The table uses $z=M\tau$, where $M$ is measured after mixing at the declared carbon boundary. The sinusoidal competitor is $u(t)=A\cos(\pi t/\tau)$, with the same slope limit and $A=\min(1,z/\pi)$. “95% count” is a conservative Hoeffding sufficient count for a majority-parity test on independent whole-product observations; it is not an exact minimum. Single-observation Bayes error is exact for the E/O pair.

| $z$ | Ramp/triangle $q_{max}$ | Single-tone $q_{sin}$ | Ramp histogram TV $a^4q$ | Exact error with one product | Conservative independent products for ≤ 5% majority error |
|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.000781 | 0.000241 | 0.000721 | 0.499640 | 11,538,367 |
| 1 | 0.012500 | 0.003850 | 0.011530 | 0.494235 | 45,073 |
| 2 | 0.200000 | 0.061596 | 0.184474 | 0.407763 | 177 |
| \(\pi\) | 0.490704 | 0.375000 | 0.452610 | 0.273695 | 31 |
| 5 | 0.680000 | 0.375000 | 0.627210 | 0.186395 | 17 |
| Ideal binary limit | 1.000000 | 0.375000 | 0.922368 | 0.038816 | 9 by Hoeffding; 1 by exact one-product error |

At $z=\pi$, the maximum-slew ramp code has 1.31 times the one-product TV of the matched sine. Under the parity-mean variance scaling, the sine needs about 1.71 times as many independent products to match precision. At $z=2$, those factors are about 3.25 and 10.54. The sine still has an operational advantage: it has no discrete switching edges. The total catalyst time, detector precision, switch wear, and boundary-waveform calibration needed to choose between them are platform-specific and remain unknown.

The script also integrates the full $K=0,\ldots,4$ distributions exactly, segment by segment, using three-point Gaussian quadrature. The largest residual between the computed five-bin total variation and the closed form $a^4q_{max}$ was $3.6\times10^{-16}$. This is a finite numerical identity check, not an independent validation of the proof or the chemical assumptions.

## What is and is not robust to unknown scales

For any input waveform with measured heavy-fraction slew $S=\sup|p'(t)|$, the exact histogram identity implies

\[
\operatorname{TV}(P_E^K,P_O^K)\le \min(S\tau,0.98)^4.
\]

For unequal temporal gaps $\delta_0,\ldots,\delta_3$, replace the right side by $\prod_j\min(S\delta_j,0.98)$. If the target includes arbitrarily small gaps, the worst-case information is zero for every finite-slew code. A periodic code also has exact nulls at resonant gaps equal to its period. Therefore no single finite-bandwidth code can promise separation across an unspecified, multiscale age range. A useful guarantee needs a measured lower scale bound, a scale-estimation pilot followed by retuning, or a frequency sweep over a declared range.

Those paths have different costs. A frequency scan over $K$ scales needs $K$ response measurements or a calibrated multisine model; sequential frequency blocks must each wait out the maximum memory/prehistory before their outputs can be assigned to the new code. A multi-tone input can start once, but its fourth-order cross-frequency terms must be calibrated. An adaptive pilot adds its own products and preparation. The evidence supplied here does not select a cheaper path without a scale prior and a measured product flux.

## Matched protocol and resource comparison

For a known $\tau$, a target-aligned pulse train or periodic frequency-response input can reproduce the same four feed values at the ancestry grid. When those values and their phase coverage match, the resulting five-bin count laws are the same: per-product total variation is $a^4q$, regardless of whether the input is named a pulse sequence, ramp square wave, or frequency-response code. The maximum-slew ramp code saturates the stated antiperiodic, phase-robust bound; it does not gain information by relabeling an optimized multipulse protocol. A finite pulse experiment can instead win on run duration if the common delay is known and the retained product window is narrow. That comparison requires an actual delay bound and flux.

The periodic code has period $2\tau$, one sign change per $\tau$, and mean heavy fraction $1/2$. Over $T=2n_c\tau$, it uses $2n_c=T/\tau$ transitions and supplies heavy-carbon dose $FT/2$ at feed rate $F$. Relative to continuous $p=0.01$ feed, the excess heavy-carbon dose is $0.49FT$. The prehistory for this synthetic age grid must cover $C_{max}+4\tau$; if $C_{max}$ is unbounded or unmeasured, preparation cost remains UNKNOWN and the unresolved-history fraction must be carried as bias. Over a $2000\tau$ measurement with $C_{max}=100\tau$, total coded duration is at least $2104\tau$, with about 2,104 transitions and heavy dose $1,052F\tau$, ignoring endpoint alignment and discarded products.

If the independently detected product rate is $R_{eff}$, a campaign collecting $N$ valid products needs $n_c=\lceil N/(2\tau R_{eff})\rceil$ complete cycles and $T=2n_c\tau$. $R_{eff}$ is not the raw ion-count rate: detector response, fragments, background, correlated chemistry, and calibration determine the effective independent count. No rate, isotope price, dose cost, detector precision, or wash-in cost is provided, so no economic ranking is available.

The code can be deterministic and pre-recorded, which removes random-code variance. It does not make different products conditionally independent if the catalyst or detector has campaign-level noise. A random phase or frequency chosen once per campaign is shared campaign randomness; it must not be treated as an independent draw for each product. Results below therefore condition on a deterministic waveform and count only independent product histories.

## Calibration and failure scope

The input $p(t)$ must be measured after feed mixing at the boundary where entry times are defined. Commanded switching is not enough. The value $a=0.98$, waveform slope, transition shape, and phase/timebase must be calibrated. If the objective is to estimate a normalized ancestry quantity by dividing the raw parity mean by $a^4q$, small relative calibration errors enter at first order as approximately $4\,\delta a/a+\delta q/q$; when $q$ is small, waveform calibration becomes ill-conditioned. Calibration uncertainty is not included in the product-count sample totals.

Computation after acquisition is a five-bin tally and alternating sum, with constant memory and linear work in the number of independently recorded products. The waveform schedule itself is generated from $\tau$ and the measured slew limit; recording and calibrating it are physical control costs. Energy per switch, controller energy, isotope price, and detector cost are UNKNOWN because no platform values were supplied.

The complete five-bin isotope-count response, natural-isotope corrections, fragmentation, and detector cross-talk must be calibrated. Isotope-neutral chemistry and stationary product selection remain assumptions. If the code changes hidden reaction pathways, or if product flux is phase-dependent, the pooled model above no longer applies without a richer observation model. The present work provides no experiment or mechanism identification.

## Prior comparison and continuation decision

The supplied ancestry report identifies isotopic frequency response as existing prior art and says its author located the 2012 paper’s abstract but not the full text. I independently read the PubMed abstract and the ACS Publications abstract/methods synopsis for the supplied H-ZSM-5 isotope-pulse study. These sources support only the existence of periodic isotope-response methods and strong labelled-pulse competitors. The exact nonlinear E/O parity construction's priority remains unresolved; this analysis makes no novelty claim.

The useful continuation is to obtain a real platform's measured inlet waveform and a scientifically justified interval for the four-carbon gap(s), then compare the ramp code, sine/multisine, and optimized multipulse data at equal effective product count, isotope dose, catalyst time, prehistory, and calibration. Without that interval, the finite-slew minimax limit is the strongest defensible conclusion: a positive advantage cannot be guaranteed across all scales.
