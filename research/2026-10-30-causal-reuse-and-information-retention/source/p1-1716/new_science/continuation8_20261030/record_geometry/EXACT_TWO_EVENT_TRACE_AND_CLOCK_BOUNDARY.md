# Exact reversible two-event trace and the physical-clock boundary

30 October 2026. Constructive alternative and obstruction. The trace representation is exact; it is a standard Schur-complement construction specialized to the supplied event-memory process. It is not an exact Markov projection of the physical-time visible process.

## 1. Every event changes the memory layer

Use the even ring with actual state `(eta,u)`, native rates `c(1+alpha u delta_i)`, and an optional external bit-flip clock of rate `gamma>=0`. Every actual event flips `u`. The only transitions in a fixed memory layer are therefore diagonal holding terms.

Let `A=sum delta_i^2`, and define operators on occupancy functions

\[
D(\eta)=cA(\eta)+\gamma,
\qquad
R_\pm=\gamma I+c\sum_{i:\,a_i=1}(1\pm\alpha\delta_i)T_i.
\tag{1}
\]

Relative to the two memory layers, the full physical generator is

\[
L=\begin{pmatrix}-D&R_+\\R_-&-D\end{pmatrix}.
\tag{2}
\]

Uniform canonical occupancy is invariant under every swap, and `delta_i` changes sign under that swap. Hence `R_-=R_+^*`. The full process is reversible for canonical occupancy times a fair `u`, whether or not it is irreducible.

Keep only the time spent in `u=+1`. Every excursion through `u=-1` consists of one holding interval followed by exactly one actual event back to `u=+1`. The occupancy trace is an exact Markov process with generator

\[
L_{\rm tr}=-D+R_+D^{-1}R_-.
\tag{3}
\]

It has nonnegative off-diagonal entries and row sum zero because `R_-1=D` and `R_+1=D`. It is self-adjoint under uniform canonical occupancy. Formula (3) is thus a reversible **positive** Markov generator, not a signed projected approximation. Preserve the two event marks to get the corresponding exact Markov additive current process; reversed two-event paths have the same conductance and opposite current marks.

For `gamma=0`, the explicit marked native-pair rate is

\[
c\,\frac{(1+\alpha\delta_i(\eta))
       (1-\alpha\delta_j(\eta^i))}{A(\eta^i)}
\quad\text{for }\eta\to\eta^i\to\eta^{ij}.
\tag{4}
\]

Each pair preserves the occupancy parity `p(eta)`, so at zero external clock the trace has the associated parity sectors. Its stationary mixture is still uniform canonical; sector weights are not reset by taking a trace.

The general trace/Schur-complement mechanism is established. A primary source explicitly stating both positivity and reversible trace interpretation is Avena–Castell–Gaudillière–Mélot, [Random Forests and Networks Analysis](https://doi.org/10.1007/s10955-018-2124-8), Proposition 13 and Section 5.3.1. The special feature here is the absence of within-layer moves, which makes the inverse diagonal and every excursion exactly two events.

## 2. Leading pair covariance without a lower activity cutoff

To compare with a potential half-speed physical-time trace, temporarily use the generator `L_tr/2`. For fields `H,G`, attach to a native-native pair the actual marks

`H_i delta_i(eta)+H_j delta_j(eta^i)` and the analogous `G` mark.

At `gamma=0`, its instantaneous marked covariance rate equals

\[
c\left[A_{HG}+\frac{S_HS_G-\alpha^2 A_HA_G}{A}\right]+O_{c,H,G}(1),
\tag{5}
\]

uniformly in every nontrivial configuration, where `S_H=sum H_i delta_i` and `A_H=sum H_i a_i`. No assumption `A` proportional to `N` enters this bound.

Here is the uniform error argument. A first swap changes `A` by at most two and gives `A(eta^i)>=A/2`. Replacing the second-stage denominator `A(eta^i)` by `A` has total paired-rate error bounded by a constant: summing its absolute difference over the second event cancels its denominator against the total second-stage activity, leaving `|A(eta^i)-A|/A`; the sum of the first-stage weights is `A`. Changing the second-stage local occupancies back to their pre-first-event values affects at most three bonds, again costing a constant after summation and division by `A`. All marks are bounded by twice their test sup norm.

In the resulting product sum, the first and second orientation-weighted means are `(S_H+alpha A_H)/A` and `(S_H-alpha A_H)/A`. Their second moments sum to `2A_HG/A`. Multiplication by the half-trace pair intensity `cA/2` gives exactly the main expression in (5).

For nonzero `gamma`, native-clock and clock-native pairs have total rate `O(gamma)` under `L_tr/2`; replacing native-native denominators `cA(eta^i)+gamma` by `cA(eta^i)` has the same `O(gamma)` total-rate bound. Therefore

\[
V_{H,G}^{\rm tr/2}
=c\left[A_{HG}-\alpha^2 A_HA_G/A\right]
+O_{c,H,G}(1+\gamma)
\tag{6}
\]

for smooth fields, since summation by parts makes `S_H,S_G=O(1)` and `A>=2`. If `gamma=o(N)`, the error divided by `N` vanishes uniformly.

Equation (6) gives an independent positive-process view of the candidate nonlocal covariance. It is not yet a physical-clock LDP or a proof of the pair process's hydrodynamic drift. The exact pair drift is generally nongradient and contains the same configuration-dependent activity averages. Reversibility alone does not turn it into `cS_H` at finite `N`.

## 3. What time was changed

Let

\[
C_+(t)=\int_0^t1\{u_v=+1\}dv,\qquad
\tau(a)=\inf\{t:C_+(t)>a\}.
\tag{7}
\]

The trace in (3) is the process observed at `tau(a)`. It erases every holding interval in the other memory layer. Its original physical execution has not become faster. At stationary fair memory, `E C_+(t)=t/2`; if concentration were established, the physical process at time `t` would correspond to the trace at time `t/2`, hence to generator `L_tr/2`. The inverse convention must not be reversed.

At finite `N`, even stationarity does **not** justify a deterministic half-clock at zero external rate. Take `N=4,M=2`, `gamma=0`, and `alpha<1`. The conserved variable is `sigma=u p(eta)`. Under the uniform canonical visible law, `P(p=+1)=1/3` and `P(p=-1)=2/3`. Conditional on `sigma=+1`, ergodicity of the visible chain gives `C_+(t)/t -> 1/3`; conditional on `sigma=-1` it gives `2/3`. The full stationary fair-sign mixture has mean one-half but retains this random sector-dependent limit. This is an exact obstruction to identifying a trace time from its stationary mean alone.

For large interior sectors the parity imbalance is small: if `M` is odd it is zero, and if `M` is even it is

\[
\mathbb E p=(-1)^{M/2}\binom{N/2}{M/2}/\binom NM.
\tag{8}
\]

This follows by taking the coefficient of `z^M` in `(1-z^2)^(N/2)`. At fixed interior density it is exponentially small. Formula (8) removes the finite-sector mean obstruction asymptotically; it does not bound the temporal fluctuations of the occupation clock on time `N^2`.

With a positive external clock the ordinary fair-sign form estimate proves

\[
\sup_{t\le T}|C_+(N^2t)/N^2-t/2|
\quad\text{is superexponentially negligible at speed }N
\tag{9}
\]

whenever `N gamma_N -> infinity`. Indeed the source `u=sigma p` is odd in `sigma`, and the divided fixed-multiplier Feynman–Kac cost is `O(1/(N gamma_N))`. Initial density ceilings `exp(O(N))` are absorbed by the final Chernoff multiplier. The uniform-time assertion follows from bounded integrands and a fixed time grid.

During each erased excursion there are only its entry and return events; the discrepancy between current/density at a matching trace time and the physical path is at most a fixed number of visible jumps. A further deterministic-time replacement uses (9) **and** exponential continuity of the trace or physical visible paths. The positive-clock weighted-current theorem supplies that continuity, so the trace can be used as a derived representation in that regime. It is not an independent proof avoiding the weighted-current estimates, and (9) gives no zero-clock receiver.

## 4. The physical visible process is not an exact Markov projection

A simple stationary example prevents that shortcut. Take one particle on a ring with `N>=6` and `alpha>0`. Its total native rate is `2c`, independent of `u`. Conditional on an observed native step of orientation `delta=+1` or `-1`, Bayes' rule gives `E[u_after | step]=-alpha delta`. If the elapsed time since that step is `t` and there has been no further native event, the unobserved clock gives

\[
\mathbb E[u\mid\text{last direction }\delta,\text{ wait }t]
=-\alpha\delta e^{-2\gamma t}.
\tag{10}
\]

Consequently the hazard of a next native direction `delta'` is

\[
c[1-\alpha^2\delta\delta'e^{-2\gamma t}].
\tag{11}
\]

Two observed histories ending at the same visible position, with different previous directions, have different future laws. The visible physical-time process is therefore not Markov, even though its stationary path law is time-reversible as a projection of the reversible full process. Observing two-event endpoints in erased time is a different interface. The dilute one-particle example is not used as an interior-density hydrodynamic counterexample.

## 5. Operational and validation scope

The exact trace can be implemented as an event-pair observation program if the bit and every selected event are known, or represented mathematically without an observation actuator. Its physical time and intermediate event records remain real. Declaring the trace generator as a new direct jump operation would require an additional actual supplier; two finite holding times do not automatically become one exponential clock.

The finite exact checker in this directory verifies 5,360 marked pair reversals at `N=4,6,8`, as well as the separate local-divergence and quotient identities. These are population algebra checks, not an acquired data set, an apparatus run, or validation of a limiting time change.

The zero-external-clock spatial receiver remains open in this representation. The trace gives a genuine positive reversible reduced process in its own occupation clock and the right leading covariance; the unresolved physical-clock and nongradient-drift steps remain explicit.
