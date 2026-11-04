# Output-only Hamiltonian calibration without source burn-in, and decoding an earlier unknown payload

**Construction note, 5 November 2026.** This is a companion to the parent's general fixed-arity construction. It uses the accepted P1 continuous-Hamiltonian output collector and reverse-reset decoder as premises. It does not revalidate them, claim historical priority for their components, or claim a practical implementation. Its additional mathematical assumption is a uniformly bounded *complete candidate interaction neighborhood*. All artifact paths and source links refer to the fixed source revision indicated below.

## 1. Concrete question and result

An arbitrary unknown quantum specimen, possibly entangled with an inaccessible reference, is already evolving under an unknown static local Hamiltonian. The receiver can collect calibrated pure, lossless local Weyl output, but cannot prepare or read the source. Can it first archive enough output to preserve that specimen, learn the dynamics from the later output of the same source, and then decode the archive?

Under the explicit assumptions below, the answer is yes, with a finite receiver construction and polynomial total work for fixed interaction-neighborhood size. No new preparation of the original specimen, source equilibration, or independent second specimen is required. The calibration measurements can remain correlated with the early archive; independence is not needed for the final channel guarantee.

Two ingredients close the acquisition gap:

1. A local reset leaves an accessible Bell purifier of the reset source qubit. Retaining these purifiers gives an actual preparation-and-readout experiment through output ports alone.
2. A freshly randomized interpolation experiment has a source-state-independent conditional mean. This makes learning valid for a single continually changing, correlated source, without treating its trials as independent.

The complete result is an asymptotic capability theorem. Its explicit conservative constants can be extremely large. It is not evidence of a presently competitive experimental method or of a civilization-scale consequence already achieved.

## 2. Physical and mathematical premises

There are n qubits and a static Hamiltonian

\[
H=\sum_{P\in\mathcal P}\theta_P P,
\qquad |\operatorname{supp}P|\le k.
\]

The candidate list contains distinct, nonidentity Pauli strings, with known lab wire labels and axes. Unknown real coefficients may vanish. The scalar identity component is physically irrelevant here. Let D be the list length.

For each source site i, a known set C_i contains the support of **every candidate term touching i**. Write

\[
s=\max_i |C_i|,
\qquad
J\ge \max_i\sum_{P:i\in\operatorname{supp}P}|\theta_P|.
\]

Assume J>0, and that k and s are fixed in the polynomial-complexity statement. The no-burn-in result is stronger in operation but narrower in structure than a theorem assuming only fixed arity: a dense two-body candidate graph can have s of order n. The entire list is known to be complete; completeness is not inferred from short observations. In this setting D=O(n c_{k,s}), and the global bound \(\sum_P|\theta_P|\le nJ\) is available.

The source has independently calibrated pure local Weyl output ports. In the qubit convention used here,

\[
L_{i,\mu}=\frac{\sqrt r}{2}\sigma_{i,\mu},
\quad \mu\in\{X,Y,Z\},
\]

so its reduced generator is

\[
\mathcal L_H(\rho)=-i[H,\rho]
+r\sum_i\left(\frac{I_i}{2}\otimes\operatorname{Tr}_i\rho-\rho\right).
\]

The synthetic reset rate is r. The physical nonidentity-Weyl jump intensity is \(R=3nr/4\). The receiver has the pure output, its known phases, and coherent lossless access. An ordinary classical noise record is not this resource.

A known inherited operator-growth bound \(\beta_0<r\) is supplied. For example, a conservative bound can be computed from k and J using the accepted P1 normalization. Write \(\kappa=r-\beta_0>0\). The actual H need not be known to the collector.

The receiver can initialize its own finite registers, perform calibrated local quantum operations, retain the output registers required by P1, measure their Paulis, and preserve early quantum memory throughout calibration and decoding. Control strength, timing resolution, compiled operation count, storage age, receiver faults, loss, and calibration errors are resources or error terms, not free consequences of this theorem. The ports and H remain static over the full experiment. Additional unknown noise or drift is outside these premises unless separately bounded.

## 3. The accessible reset purifier

For a noise-only time bin of length \(\Delta\), the accepted local output instrument implements

\[
|\psi\rangle_S\longmapsto
\sqrt{e^{-r\Delta}}|\psi\rangle_S|0\rangle_F
+\sqrt{1-e^{-r\Delta}}|1\rangle_F
|\Phi_2\rangle_{SA}|\psi\rangle_B.
\]

The flag probability is independent of the payload. B carries the old source state, including its correlations with arbitrary references. A is the accessible Bell partner of the new source qubit. The source is maximally mixed only after A is ignored.

Measuring A in a conjugate Pauli basis remotely prepares a known random Pauli eigenstate on S. The measurement may instead be deferred: A is isolated after collection, and the source receives no feedback, so the final joint statistics are the same. Thus an output port supplies more than an error flag or an exported mixed state. The Bell purifier is a substantive physical resource.

## 4. An unconditional finite record machine

Fix a target P. Choose \(i\in\operatorname{supp}P\) and a one-qubit Pauli B_i that anticommutes with the Pauli of P at i. Define the signed Hermitian Pauli

\[
Q=iPB_i,
\qquad i[P,B_i]=2Q.
\]

Put \(C=C_i\), \(b=|C|\), and \(m=b+1\). Q is extended by identities to C.

A trial starts with the actual current source state, which can be arbitrary and correlated with the early archive, an inaccessible reference, and all previous outcomes. Only receiver work registers and success bits are initialized afresh.

- **Front interval w.** At every successful reset of each j in C, keep its newest Bell purifier A_j and overwrite its previous retained purifier. Set a success bit for j. Discard its exported old payload and any overwritten purifier. The final retained A_j is therefore the purifier of the last reset of j in the interval.
- **Middle interval tau.** Retain A but discard the intervening output. The source evolves under its actual generator.
- **Back interval w.** At the first reset of i, freeze the exported old state in a receiver register B and set a back-success bit. Subsequent resets do not overwrite B.
- **Readout.** Measure \(Q_A^T\) and B_i on the retained output. Return their signed product if every required front success and the back success occurred; return zero otherwise.

The transpose is in the calibrated computational basis and includes the sign change for Y. The observation \(Y_0\) belongs to \(\{-1,0,1\}\). Failed trials are included; no conditional acceptance cost is hidden.

These instructions define finite-dimensional CPTP reset-update maps on the source plus finitely many receiver registers and classical bits. Front overwriting and back freezing are physical channels, not formal signed histories. Their generators \(G_F,G_M,G_B\) satisfy the conservative complete-norm bound

\[
\|G_F\|_\diamond,\|G_M\|_\diamond,\|G_B\|_\diamond
\le \Lambda:=2n(J+r).
\]

For every normalized initial state sigma, including arbitrary external correlations, the expected unconditional observation has the form

\[
f_\sigma(w,\tau)
=\ell e^{wG_B}e^{\tau G_M}e^{wG_F}
(\sigma\otimes\omega_{\rm fresh}),
\qquad \|\ell\|\le1.
\]

No exponentially large matrix is formed by the algorithm. This expression proves analyticity and a dimension-independent norm estimate; the physical experiment evaluates it.

The success probability is exactly

\[
p(w)=(1-e^{-rw})^m,
\]

independent of sigma and H. Independent state-independent reset clocks give the b front occurrences and one back occurrence in disjoint intervals. Consequently

\[
\mathbb E[Y_0^2\mid\sigma,w,\tau]=p(w)\le(rw)^m.
\]

### 4.1 The universal mixed-derivative identity

Every nonzero measurement record requires at least b distinct front resets and one back reset. Therefore all powers of w below m vanish. At order exactly m, there is no Hamiltonian action or additional reset within either window: either would consume an extra power of w. The b! front orderings cancel the simplex factorial, and the distinct-site reset maps commute at this order. Thus

\[
\partial_w^m f_\sigma(0,\tau)
=m!r^m\operatorname{Tr}\!\left[
B_i e^{\tau\mathcal L_H}
\left(\frac{Q_C}{2^b}\otimes\sigma_{\bar C}\right)
\right].
\]

External references can be included throughout and traced at the final scalar observation. The front resets erase the C part of any prior source-reference correlation and replace it by the known Bell pairs. This explains why only the reduced state outside C remains in the displayed expression.

At tau=0 the trace vanishes. Its first derivative has three kinds of term. Terms of H not touching i commute with B_i. Every term touching i is supported inside C by the complete-neighborhood promise. Pauli orthogonality inside C then isolates P, and the local depolarizing term is orthogonal to Q. Hence, for **every sigma**,

\[
\boxed{
\partial_w^{m}\partial_\tau f_\sigma(0,0)
=2m!r^m\theta_P.
}
\]

This also proves the parent's support-only identity when the source outside the prepared support is maximally mixed. Preparing the entire known neighborhood removes that equilibrium requirement.

The neighborhood condition matters. For example, let

\[
H=\theta X_1+gX_1Z_2,
\qquad P=X_1,\quad B_1=Z_1,\quad Q=Y_1.
\]

Resetting only site 1 yields derivative \(2\theta+2g\langle Z_2\rangle\). Resetting the full neighborhood \(C_1=\{1,2\}\), while measuring identity on the unused purifier, removes the confounder. A claim of arbitrary-state calibration from the support of every lower-weight term alone would be false.

## 5. Finite precision estimation with freshly randomized experiments

The derivative is estimated from finite, nonzero intervals. This is not a limit requiring infinitesimal experimental timing.

Take

\[
h=\frac1{8\Lambda},\qquad x,y\in[0,1].
\]

From the matrix-exponential expansion,

\[
\left|[x^a y^c] f_\sigma(hx,hy)\right|
\le\frac{(2\Lambda h)^a(\Lambda h)^c}{a!c!}
=\frac{4^{-a}8^{-c}}{a!c!}.
\]

Let t_L keep the tensor Taylor coefficients with a,c at most L. Uniformly in sigma,

\[
\|f_\sigma(h\cdot,h\cdot)-t_L\|_\infty
\le R_L:=\frac{2e^{3/8}4^{-(L+1)}}{(L+1)!}.
\]

For L at least m, t_L has exactly the desired derivative at the origin.

Use Chebyshev-Lobatto points \(z_j=\cos(\pi j/L)\), \(x_j=(1+z_j)/2\), and the Lagrange basis \(l_j\) for the z points. Define the physical coefficient weights

\[
a_{j\ell}
=\frac{(2/h)^{m+1}}{2m!r^m}
 l_j^{(m)}(-1)l_\ell'(-1),
\qquad A_L=\sum_{j,\ell}|a_{j\ell}|.
\]

Interpolation is exact on t_L, so

\[
\left|\sum_{j,\ell}a_{j\ell}
 f_\sigma(hx_j,hx_\ell)-\theta_P\right|
\le A_LR_L.
\]

A_L is explicitly computable from a small interpolation table. Using its computed value and the factorial remainder is preferable to using an extremely loose worst-case Markov bound. For a simple certified complexity bound, discrete cosine coefficients of the interpolant to data of magnitude at most one have magnitude at most two. Its supremum norm is at most \(2L+1\). Repeated Markov inequalities then give

\[
A_L\le
\frac{(2/h)^{m+1}}{2m!r^m}
(2L+1)^2L^{2m+2}.
\]

Choose L at least m until \(A_LR_L\le\nu/8\), where nu is the desired absolute coefficient accuracy. Factorial decay ensures that

\[
L=O_m\!\left(1+\log_+\frac{\Lambda^{m+1}}{r^m\nu}\right)
\]

suffices. This estimate is intentionally conservative. It is a finite classical computation of polynomial bit complexity for fixed m.

### 5.1 Why sampling fixed nodes consecutively is insufficient

The source after one trial need not equal the source after another. Therefore values collected at different fixed nodes need not belong to a single function \(f_\sigma\). The Taylor cancellation alone does not justify such a procedure.

At **each raw trial**, draw the node freshly, independently of the entire past, with probability

\[
q_{j\ell}=|a_{j\ell}|/A_L.
\]

Run that experiment and return

\[
Z=A_L\operatorname{sgn}(a_{j\ell})Y_0.
\]

Conditional on any past record, there is one current residual state sigma before the node is chosen. Consequently

\[
|\mathbb E[Z\mid\mathrm{past}]-\theta_P|\le\nu/8,
\quad |Z|\le A_L,
\quad \mathbb E[Z^2\mid\mathrm{past}]\le A_L^2p_{\max},
\]

where

\[
p_{\max}=(rh)^m\le1.
\]

This is a bounded martingale experiment, valid for the same source and arbitrary quantum correlations. There is no iid premise.

For a per-coefficient failure budget alpha/D, Freedman's inequality with bounded differences at most \(2A_L\) gives a sufficient raw-trial count

\[
N_P=\left\lceil
\left(\frac{32A_L^2p_{\max}}{\nu^2}
+\frac{16A_L}{\nu}\right)
\log\frac{2D}{\alpha}
\right\rceil.
\]

The sample mean differs from the mean of its conditional expectations by at most nu/2 except with probability alpha/D. Interpolation bias, finite arithmetic, and node-sampling and timing errors can be assigned the remaining nu/2. Clip the final estimate to [-J,J]; this cannot increase its distance to the true coefficient. A union bound gives all D coefficient errors at most nu, with failure probability at most alpha, uniformly over the original input and reference.

This is an unconditional variance bound: failure-zero records reduce the variance by one factor of success probability. All raw trials are counted. With fixed m, its leading precision dependence is

\[
N_P=
\widetilde O_m\!\left[
\frac{\Lambda^2}{\nu^2}
\left(\frac{\Lambda}{r}\right)^m
+\frac{\Lambda}{\nu}
\left(\frac{\Lambda}{r}\right)^m
\right],
\]

with logarithms in precision, dimension, and confidence suppressed. The exact A_L formula and N_P above, rather than this notation, specify the construction.

### 5.2 Arithmetic, timing, and source exposure

One trial takes at most 3h of source evolution. It may be padded to exactly 3h by discarding extra output, since the next-trial guarantee holds for every source state. Thus

\[
T_{\rm cal}\le3h\sum_PN_P
\]

is a deterministic bound for the ideal experimental horizon. Actual hardware readout, reset, and controller latency must be added to source exposure and memory age. The theorem remains valid when such latency changes the next initial source state, but the corresponding output collection and storage costs must still be counted.

Changing any one window duration by at most delta_t changes its expectation by at most a constant times \(\Lambda\delta_t\); a conservative three-window bound is \(3\Lambda\delta_t\). For example \(\delta_t\le\nu/(100A_L\Lambda)\) is sufficient after assigning a modest bias budget. Sampling probabilities can be rounded to total-variation error at most \(\nu/(100A_L)\). Computing weights, probabilities, and observations to a further inverse-polynomial error uses a finite number of bits polynomial in logarithms of the displayed quantities. An implementation should track an explicit error budget rather than assuming exact real arithmetic.

## 6. Capture first, then calibrate and decode

Apply the inherited H-independent P1 collector first. With early capture time

\[
T_A=\kappa^{-1}\log\frac{4n}{\epsilon_A^2},
\]

the known-H reverse-reset decoder has error at most epsilon_A in diamond norm, using the inherited bound \(2\sqrt{n e^{-\kappa T_A}}\). The early exported payload registers and clock record gamma are archived. This collector uses supplied bounds and port calibration, not the unknown coefficients.

Next perform the output-only calibration above on the same residual source. Choose

\[
\nu\le\frac{\epsilon_H}{2DT_A}.
\]

On the good estimate event,

\[
\|H-\widehat H\|\le\sum_P|\theta_P-\widehat\theta_P|
\le D\nu.
\]

For each early clock record gamma, the reverse-reset decoder uses the same reset SWAPs regardless of coefficients. Its inverse-Hamiltonian intervals have total length T_A. Duhamel's inequality and a hybrid of its unitary segments give

\[
\|\mathcal D_{\gamma,\widehat H}
-\mathcal D_{\gamma,H}\|_\diamond
\le2T_A\|\widehat H-H\|
\le\epsilon_H.
\]

This comparison concerns an implementable decoder, not an existence-only information-disturbance statement.

### 6.1 Calibration independence is unnecessary

Let \(\sigma_{\gamma,y}\) be the subnormalized positive state of the early archive and inaccessible reference, conditioned on the early clock record gamma and later calibration outcome y. These states may be strongly correlated with y.

Compare the approximate decoder and true-H decoder on each *same* state. On good outcomes the trace-norm difference is at most \(\epsilon_H\operatorname{Tr}\sigma_{\gamma,y}\). On bad outcomes it is at most \(2\operatorname{Tr}\sigma_{\gamma,y}\). The uniform calibration confidence gives total bad probability at most alpha for every initial payload/reference. Summing gives at most \(\epsilon_H+2\alpha\).

Later operations act only on the residual source and fresh receiver registers. Averaging their outcomes leaves the marginal of the early archive and reference unchanged. Therefore the true-H decoder applied after these averaged later operations has exactly the same input as in the early P1 guarantee. No statistical or quantum independence of the calibration record and early archive is required.

Including receiver realization and decoder simulation errors yields

\[
\boxed{
\|\mathcal R_{\rm learned}-\mathrm{id}\|_\diamond
\le\epsilon_A+\epsilon_H+2\alpha
+\epsilon_{\rm phys}+\epsilon_{\rm sim}.
}
\]

Any actual memory noise, collection loss, port calibration error, and bounded model mismatch must be added with their justified whole-protocol norms. A rare bad outcome can destroy the original specimen; the error guarantee counts that event and does not promise a retry on a new original input.

## 7. Finite physical execution and its cost

There are two different approximations. They must not be conflated by observing that two constructions have the same reduced Lindbladian.

### 7.1 Record-machine approximation by finite reset layers

The analytic machine uses continuous-time reset updates. Its individual front and back reset maps are CPTP and idempotent. Distinct sites' reset updates commute. For one such update T_j,

\[
e^{r\Delta(T_j-\mathrm{id})}
=e^{-r\Delta}\mathrm{id}+(1-e^{-r\Delta})T_j.
\]

For a back update, applying it twice leaves the first B export frozen and merely resets an already maximally mixed source, so idempotence still holds. Thus its reset layers are exactly the finite flagged updates supplied by the local instrument.

Split the Hamiltonian and these reset layers into bins of maximum length Delta_max. A bounded CPTP Lie-product estimate and telescoping give the conservative complete-channel error

\[
\epsilon_{\rm machine}
\le 2\Lambda^2T_{\rm cal}\Delta_{\max}.
\]

Randomized nodes are included as a classical controller in this unconditional channel. Because the node probabilities are fixed and every draw is independent of past outcomes, all node choices may equivalently be sampled before the run. The resulting time partition is independent of the source and its output records. Per-use hybrid bounds remain valid under the record-machine controller. Logical windows can each be partitioned into equal sub-bins at most Delta_max, avoiding any need for an arbitrarily tiny remainder bin.

### 7.2 Actual output versus the split output process

The accepted P1 theorem compares the full coherent physical Weyl output to the finite unitary/reset-output network. Let chi bound the sum of Hamiltonian commutators with a local output jump isometry. Under the present normalization, \(\chi\le2J\) is a conservative choice. For total exposure T and maximum bin Delta_max, it supplies

\[
\epsilon_{\rm split}
\le 2\chi\Delta_{\max}\sqrt{RT+(RT)^2}.
\]

This is a full isometry/output comparison. It is the required reason that the same receiver works on the physical output. It does not follow merely from equality of the reduced source master equations. The bound includes multiple events within a bin.

Take a horizon T including early capture, calibration, and any chosen latency periods in which the source output is processed. Choose Delta_max to make both displayed errors fit allocated budgets. Let K be the resulting finite number of bins. If each of at most nK local collector applications has implementation error at most \(\eta_{\rm col}\), its total error is at most \(nK\eta_{\rm col}\). Choose the local accuracy accordingly. Summing these terms, source-independent timing/rounding errors, and other declared receiver errors defines epsilon_phys.

In units with r=1, T_cal, inverse Delta_max, K, and inverse local accuracy are polynomial in n, D, J/r, r/kappa, inverse target error, and the relevant classical bit lengths for fixed k,s, with logarithmic confidence factors. The inherited local collector compilation therefore gives a polynomial finite construction. Restoring units multiplies source time by 1/r. Dependence on a very small physical reset rate or margin is a real exposure cost; bit length alone does not make it cheap. This can nevertheless be a very large polynomial.

The calibrated decoder uses at most polynomially many local inverse-unitary operations, reset SWAPs, and classical processing steps. Standard local Hamiltonian simulation with the acquired finite-precision coefficients controls epsilon_sim. The receiver must retain the early quantum archive for at least

\[
T_A+T_{\rm cal}+T_{\rm classical}+T_{\rm decode}
\]

plus hardware latency. The theorem supplies neither a fixed-bandwidth receiver nor a noise-free physical memory. A chosen memory implementation must meet its declared error budget over this full duration. P1's separate bounded-hardware work is not assumed to be solved by this note.

There is **no division of these complete-channel errors by a heralding probability**: the experiment records failures as zero, and the final output channel includes every record. Normalized branch claims could require such a division; they are not used here.

## 8. Comparison with existing operations

This is not a new claim that local Hamiltonians can be learned, that Markov output identifies dynamics, that Bell pairs remotely prepare states, or that derivative estimation works. Each is substantial prior machinery. The completed added operation is a finite, explicitly acquired route for preserving the *first arbitrary payload* before its static dynamics have been learned, then recovering it using later observations of the same source.

| Applicable approach | What it already supplies | Access or conclusion that differs here |
| --- | --- | --- |
| Guţă and Kiukas, quantum Markov output identification | Stationary-output equivalence classes, gauge structure, and local asymptotic statistics | Does not by itself give the displayed many-body local cost, nonstationary arbitrary-state experiment, or archive-and-decode initial-payload construction |
| Haah, Kothari, and Tang, efficient Hamiltonian learning | Efficient learning from high-temperature Gibbs states and real-time evolution access | Its experimental queries include supplied state/evolution access; this note constructs relevant queries from the actual later output of one source |
| Gong et al., *Out-of-control Hamiltonian Learning* | Strong recent restrictions on source control still compatible with learning | Uniform source preparation and measurement, or structured computational-basis preparation/readout, are distinct resources from no source access |
| Liu et al., *Learning Many-Body Hamiltonians Using a Local Probe* | A single measurable qubit can learn many-body interactions with strong precision guarantees | It assumes fast single-qubit controls and a connected reference backbone, and uses synthesized transfer operations; its source access is stronger in ways not available here |
| Accepted P1 known-H recovery | H-independent collection plus constructive reverse-reset decoding | Requires H for executing the decoder; the output experiment supplies it after collection |
| Classical homodyne or other Markov-output estimation | May already be sufficient to learn local H under appropriate port and observability assumptions | This note does not establish that coherent purifiers are necessary for calibration. Coherent early output remains the supplied resource for arbitrary quantum-payload recovery |

The source labels and known Pauli ports fix the relevant parameter gauge; an unknown simultaneous system rotation can otherwise make H identification operationally ambiguous. The local-probe alternative may be far more efficient where its controls and backbone exist. No separation against every possible same-output-access calibration algorithm is proved. A stronger existing polynomial algorithm under exactly these source and output restrictions would replace the calibration component without invalidating the payload-preserving composition.

No historical novelty claim is justified by this limited comparison. The precise contribution of this companion is the arbitrary-state mixed derivative on complete neighborhoods, the fresh-node martingale, the independence-free decoder composition, and a finite-resource accounting that connects them to the accepted receiver.

## 9. Primary sources and governing premises

- Accepted P1 source package at fixed revision: [scalable many-body acquisition](https://github.com/harjassand/astra-research-knowledge/tree/324acb589443002bf8d529cc15e160129c5e36d2/research/returns/2026-11-05-p1-scalable-many-body-acquisition).
- Accepted [continuous-Hamiltonian reverse-reset decoder](https://github.com/harjassand/astra-research-knowledge/blob/324acb589443002bf8d529cc15e160129c5e36d2/research/returns/2026-11-05-p1-scalable-many-body-acquisition/package/construction/continuous_hamiltonian_reverse_reset_decoder.txt).
- Accepted [finite local depolarizing-port collector](https://github.com/harjassand/astra-research-knowledge/blob/324acb589443002bf8d529cc15e160129c5e36d2/research/returns/2026-11-05-p1-scalable-many-body-acquisition/package/construction/finite_local_depolarizing_port_collector_note_2026-11-04.md).
- M. Guţă and J. Kiukas, [*Equivalence classes and local asymptotic normality in system identification for quantum Markov chains*](https://arxiv.org/abs/1402.3535), Communications in Mathematical Physics (2015), DOI [10.1007/s00220-014-2253-0](https://doi.org/10.1007/s00220-014-2253-0).
- J. Haah, R. Kothari, and E. Tang, [*Optimal learning of quantum Hamiltonians from high-temperature Gibbs states* / real-time extensions](https://arxiv.org/abs/2108.04842); published as [*Learning quantum Hamiltonians from high-temperature Gibbs states and real-time evolutions*](https://www.nature.com/articles/s41567-023-02376-x), Nature Physics 20, 1027–1031 (2024).
- W. Gong, M. Ma, S. Chen, J. Cotler, and H.-Y. Huang, [*Out-of-control Hamiltonian Learning*](https://arxiv.org/abs/2610.06709), October 2026.
- S. Liu, Z. Xu, A. V. Gorshkov, X. Wu, Y.-X. Wang, and Z.-Y. Wei, [*Learning Many-Body Hamiltonians Using a Local Probe*](https://arxiv.org/abs/2610.02157), October 2026; [institutional publication page](https://quics.umd.edu/publications/learning-many-body-hamiltonians-using-local-probe-0).

The parent's finite two-qubit diagnostic in `next_root/finite_derivative_diagnostic.json` checks its support-only derivative interpolation numerically. That check is not a simulation of this entire single-payload construction, a noisy receiver, or its full resource budget. The results proved here are analytic conditional theorems under the stated access and model premises.
