# Correct-or-flag logical readout with the actual detector record

Author: producer-workspace/classical_capacity, 2026-10-29.

This is a separate authored addendum. The accepted main note, CONSTRUCTIVE_FINE_READOUT.md, and its proof, executable, data, receipt and independent review remain unchanged. Root requested independent review of this addendum after construction.

## 1. The operation being certified

The full fine-count comparison in the main note asks that every detected count match the count of an ideal detector. A final computing output need not demand that operation. Here the reference is **a correct logical Z result or an explicit erasure flag, with the same actual raw counts and the same count-conditioned retained memory as the real detector**.

On the entire admitted logical-times-syndrome space, one missed photon cannot cause an accepted wrong logical result. It may cause an erasure flag. Consequently the complete error relative to this correct-or-flag operation is bounded by a two-miss tail, while the declared erasure probability remains a separately charged first-order cost. The result holds for arbitrary coherent syndrome inputs, correlations with retained memory and references.

The port is exactly the main note's equal-efficiency independent vacuum attenuation followed by ideal mode-resolved destructive counting. The uncollected fields and any environment needed to make the stated record classical are genuinely retired at the declared interface. This is not a certificate for a returning loss-field purification, a general noisy detector, or an always-success readout.

Let q>=1, L=q+1, N=L^2 and n_max=N+q. Let

\[
J:L_{\rm log}\otimes S\longrightarrow A
\]

be the supplied admitted isometry. The main theorem gives, for each occupied ideal fine count \(\nu=(\nu_a,\nu_b)\),

\[
\langle\nu|J=\langle\ell_\nu|\otimes\langle v_\nu|,
\qquad
\sum_{\nu:\ell_\nu=\ell}|v_\nu\rangle\langle v_\nu|=I_S .
\tag{1}
\]

The raw output is \(m=(m_a,m_b)\). Write \(b(m)\in\{0,1,\perp\}\) for the same integer decoder and validity tests used in the main note, with \(\perp\) the declared invalid flag. No record is postselected away.

## 2. A one-miss exclusion on the actual readout geometry

For an occupied ideal count \(\nu\), let k be its unique original grid point. Its displacement from that point obeys

\[
\left|\nu_a-\nu_b-(2Lk-N)\right|\le q .
\tag{2}
\]

If zero or one photon is missed, then \(m=\nu-r\) with \(r_a,r_b\ge0\) and \(r_a+r_b\le1\), so

\[
\left|m_a-m_b-(2Lk-N)\right|\le q+1 .
\tag{3}
\]

Suppose the observed count m passes the decoder's validity tests and is attributed to grid point k'. Then

\[
\left|m_a-m_b-(2Lk'-N)\right|\le q .
\]

Combining the last two inequalities gives

\[
2L|k'-k|\le 2q+1<2(q+1)=2L ,
\tag{4}
\]

so k'=k. Therefore an accepted result after zero or one miss has exactly the correct original grid index and logical parity. Failing the total-number or imbalance tests instead produces \(\perp\). No assumption about a measured syndrome or a classical error path enters this support argument.

For two or more misses, an accepted wrong result can occur. The conclusion is a property of this decoder and its admitted space, not a lower bound on all possible detectors or recovery operations.

## 3. The complete reference instrument, including actual records

For arbitrary \(\rho_{LSM}\), with all references absorbed into M, define the positive fine-row substate

\[
\tau_\nu(\rho)=
(\langle\ell_\nu|\otimes\langle v_\nu|\otimes I_M)
\rho
(|\ell_\nu\rangle\otimes|v_\nu\rangle\otimes I_M).
\tag{5}
\]

The main note proves on the whole input operator algebra that the attenuation/count channel is ideal fine counting followed by the classical thinning kernel

\[
T_\eta(m|\nu)=
\binom{\nu_a}{m_a}\binom{\nu_b}{m_b}
\eta^{m_a+m_b}(1-\eta)^{|\nu|-|m|}
\tag{6}
\]

for \(0\le m_i\le\nu_i\). Here \(\eta\) is intensity transmissivity. The lost-field Kraus index is traced, not supplied as a free accessible record.

Thus the actual complete operation is

\[
\mathcal A_\eta(\rho)=
\sum_{\nu,m}T_\eta(m|\nu)
|b(m),m\rangle\langle b(m),m|\otimes\tau_\nu(\rho).
\tag{7}
\]

Define

\[
f(\nu,m)=
\begin{cases}
\perp,&b(m)=\perp,\\
\ell_\nu,&b(m)\in\{0,1\}.
\end{cases}
\]

The correct-or-flag comparison operation is

\[
\mathcal F_\eta(\rho)=
\sum_{\nu,m}T_\eta(m|\nu)
|f(\nu,m),m\rangle\langle f(\nu,m),m|\otimes\tau_\nu(\rho).
\tag{8}
\]

This is CPTP. It is implementable as an ideal logical Z instrument followed by its logical-outcome-dependent syndrome measurement, the same thinning kernel and the stated flag rule. It is a mathematical reference for the real operation, not an additional physical capability asserted for the noisy detector.

Equations (7) and (8) have exactly the same raw-count-plus-memory marginal:

\[
\operatorname{Tr}_{\rm semantic\ bit}\mathcal A_\eta(\rho)
=\operatorname{Tr}_{\rm semantic\ bit}\mathcal F_\eta(\rho)
=\sum_m|m\rangle\langle m|\otimes
\sum_\nu T_\eta(m|\nu)\tau_\nu(\rho).
\tag{9}
\]

They also have exactly the same flag event and flag-conditioned state. Any deterministic intermediate decoder record, including b(m) or the computed k(m), can be retained on both sides as actual garbage without changing the assertion. The comparison changes only the intended semantic answer label on accepted wrong paths. It does not silently change a raw record to an ideal one, delete a record, or replace a coherent memory update by a probability distribution.

The reference remains a **declared-erasure operation**. On a flag it does not supply the desired logical answer. Its flag probability may depend on the current syndrome and logical input. No independent erasure channel, fixed state-independent success probability, or useful postselection rate is inferred.

## 4. Exact complete-error effect and the two-miss bound

For each ideal count define its accepted wrong-label probability

\[
w_\nu=\sum_{\substack{m:\ b(m)\ne\perp\\ b(m)\ne\ell_\nu}}
T_\eta(m|\nu)
\]

and the positive input effect

\[
W=\sum_\nu w_\nu
|\ell_\nu\rangle\langle\ell_\nu|\otimes
|v_\nu\rangle\langle v_\nu| .
\tag{10}
\]

For the specified reference operation, the exact complete metric is

\[
\boxed{\quad
\tfrac12\|\mathcal A_\eta-\mathcal F_\eta\|_\diamond
=\|W\| .
\quad}
\tag{11}
\]

The domain here is \(L_{\rm log}\otimes S\); arbitrary references are allowed. Equivalently this is the restricted physical-input metric under J.

For the upper bound, couple identical CP submaps in (7) and (8). All non-wrong paths cancel. On each wrong path the difference is between two orthogonal classical semantic labels attached to the same positive memory substate. Its half trace norm is the trace of that substate. Summing and using \(W\le\|W\|I\) bounds the distance for every referenced input by \(\|W\|\).

For equality, W is block diagonal in the logical label. Choose a logical label \(\ell\) and a syndrome eigenvector attaining the largest eigenvalue of its block. On this input the reference's accepted label is always \(\ell\); every accepted wrong actual label lies in the orthogonal logical-output subspace. For every raw m, the two differing blocks are the same positive wrong-path state with opposite signs. Their half trace norms add exactly to \(\operatorname{Tr}(W\rho)=\|W\|\). No reference is required to attain the optimum.

This effect-operator reduction is reusable: whenever a complete destructive readout has rows supported in definite ideal logical-label sectors and a classical confusion kernel follows it, its distance to the same-record correct-or-flag refinement is the largest eigenvalue of the accepted-wrong effect. A diamond-norm optimization is unnecessary for this particular comparison. It does not assert that this is the best possible logical detector or best comparison under a different interface.

By Section 2 a wrong accepted path requires at least two missed photons. Since \(|\nu|\le n_{\max}\),

\[
w_\nu\le
\Pr\{\operatorname{Binomial}(|\nu|,1-\eta)\ge2\}
\le
\beta_2,
\]

\[
\beta_2=
1-\eta^{n_{\max}}
-n_{\max}(1-\eta)\eta^{n_{\max}-1}.
\tag{12}
\]

Equation (1) then gives \(W\le\beta_2 I\). Consequently

\[
\tfrac12\|\mathcal A_\eta-\mathcal F_\eta\|_\diamond
\le\beta_2
\le\binom{n_{\max}}2(1-\eta)^2 .
\tag{13}
\]

This is a uniform sufficient complete-channel bound. The finite geometric maximum over individual Fock counts need not be attainable by an admitted source state, and \(\beta_2\) need not equal the exact operator norm in (11).

## 5. Flags are a separate destructive cost

Let

\[
g_\nu=\sum_{m:\ b(m)=\perp}T_\eta(m|\nu),
\qquad
G=\sum_\nu g_\nu
|\ell_\nu\rangle\langle\ell_\nu|\otimes
|v_\nu\rangle\langle v_\nu| .
\tag{14}
\]

The actual and reference flag probabilities are both \(\operatorname{Tr}(G\rho)\). No loss gives the correct valid count, so

\[
G\le(1-\eta^{N+q})I,
\qquad
p_{\rm flag}\le1-\eta^{N+q}
\le(N+q)(1-\eta).
\tag{15}
\]

The possible first-order cost is real for this interface. The admitted space contains nonzero vectors of total number N-q, for example q annihilations applied to a nonzero code column. On any normalized vector in that sector every missed photon drops the total below the decoder's accepted band. Thus

\[
1-\eta^{N-q}\le
\sup_{\rho_{LS}}p_{\rm flag}(\rho)
\le 1-\eta^{N+q}.
\tag{16}
\]

This is a lower bound for the fixed readout/flag rule on its full admitted input space, not a physical lower bound for other interfaces. A dynamics model may put only a small weight in this lowest-number sector; that additional information can improve a workload-specific flag estimate and has not been assumed here.

A flag destroys the measured input. It does not leave an unknown state available for a free repeat. A restarted run needs a fresh authorized state or a complete re-execution of the computation, with preparation, execution, memory, supply and scheduling costs. No repeat-until-success performance is claimed. In particular, as \(\eta\) tends to zero the unflagged-error metric may tend to zero because almost everything is flagged; that is not successful computation.

## 6. A sharp q=1 complete-channel example

For q=1, N=4, use the standard ordered syndrome columns

\[
V_0,\quad aV_0/\sqrt2,\quad bV_0/\sqrt2,\quad
a^\dagger V_0/\sqrt3,\quad b^\dagger V_0/\sqrt3 .
\]

Let \(P_{\rm gain}\) project onto the last two syndrome vectors. The only ideal fine counts that can produce an accepted wrong result are:

| Ideal count \(\nu\) | True bit | Wrong observed count m | Conditional probability |
|---|---:|---|---|
| (1,4) | 0 | (1,2) | \(6\eta^3(1-\eta)^2\) |
| (4,1) | 0 | (2,1) | \(6\eta^3(1-\eta)^2\) |
| (3,2) | 1 | (3,0) | \(\eta^3(1-\eta)^2\) |
| (2,3) | 1 | (0,3) | \(\eta^3(1-\eta)^2\) |

In logical zero, the relevant gain-syndrome amplitudes at (1,4) and (4,1) are \(1/\sqrt6\); in logical one the corresponding gain columns are exactly the Fock states (3,2) and (2,3). No other syndrome has total number five. Therefore, as an identity for every \(0\le\eta\le1\),

\[
W=\eta^3(1-\eta)^2 I_L\otimes P_{\rm gain}.
\tag{17}
\]

Equations (11) and (17) give

\[
\boxed{\quad
\tfrac12\|\mathcal A_\eta-\mathcal F_\eta\|_\diamond
=\eta^3(1-\eta)^2 .
\quad}
\tag{18}
\]

An explicit saturating input is \(|1\rangle_L\) in the a-dagger syndrome, whose physical state is \(|3,2\rangle\). Missing both mode-b photons and none of mode a produces raw count (3,0), reported bit zero, with probability \(\eta^3(1-\eta)^2\). Actual and reference raw records and their probabilities are identical; their semantic bits disagree on this branch.

This exact value is for the stated correct-or-flag reference with every actual raw count kept. It is not an optimized readout error or a claim that the erasure probability is equally small.

## 7. Retained memory and composition with computation

The same-record equality preserves nonclassical conditional memory. For q=2, take logical zero and the syndrome-memory input

\[
(|0\rangle_S|0\rangle_M+|7\rangle_S|1\rangle_M)/\sqrt2,
\]

where syndrome 7 is the supplied orthogonalized word ac. At actual observed count m=(0,8), both (7) and (8) have retained-memory off-diagonal

\[
-\frac{9\sqrt3}{8}\eta^8(1-\eta).
\tag{19}
\]

Only the ideal count (0,9) contributes to that off-diagonal. The decoder accepts bit zero. Measuring or pinching the syndrome first would set (19) to zero despite leaving the corresponding diagonal count probabilities unchanged. That altered operation is not used in the proof.

If a computation has an already valid complete-channel distance \(\epsilon_{\rm dyn}\) to an admitted comparison output, apply the actual detector to both sides of that first hybrid. Compare the two detector operations only on the admitted comparison side. The complete composed distance to the correct-or-flag target is at most

\[
\epsilon_{\rm dyn}+\|W\|
\le\epsilon_{\rm dyn}+\beta_2,
\tag{20}
\]

capped at one. A compatible additional detector/control implementation error adds by another complete-channel hybrid. The physical flag probability is at most the comparison flag bound plus the corresponding pre-readout distance. Neither flags nor these distances may be added as if they were independent stochastic events; the estimates use worst-case channel contraction and the flag effect.

The environment boundary matters. Equation (6) as a complete classical thinning identity uses the retirement of the loss label. If the lost field or detector pointer purification later returns, it belongs to the output and can carry inter-count coherence. Equations (7)-(20) are not automatically certificates at that enlarged interface. One must use its full coherent dilation or prove a new comparison; the main note supplies a separate square-root coherent-output bound. Earlier returning baths already included in M remain included here and are not traced away.

The physical detector requirements in the main note remain: separate mode identification, single-quantum resolution, no saturation through N+q, specified acquisition time and actual readiness/reset/record retention. Noise during destructive acquisition is not automatically covered by the graded Hamiltonian lifetime theorem. This addendum changes the required semantic operation, not the photon-counting hardware port.

## 8. Exact evidence, ancestry and reproduction

The executable flagged_readout_checks.py reads the frozen serialized grades and imports the frozen decoder/arithmetic only. It does not execute any parent or predecessor validation suite or a numerical solver. For q=1,2,3 and \(\eta=3/4,99/100\), it checks 14,796 exact thinning atoms, including 924 zero-or-one-miss atoms with no accepted wrong result. It checks the atomic same-record coupling, the binomial tails and the lowest-number flag witness.

For q=1 it checks 100 complete bad-effect coefficients and 1,650 raw-record/memory matrix-unit coefficients across the two efficiencies, including the exact sharpness witness. All logical off-diagonal input matrix units vanish by the exact row support identity, which the executable also asserts; the syndrome matrix units include arbitrary complex coefficients. For q=2 it preserves the nonzero conditional-memory coefficient (19). The all-eta results and arbitrary-q bound are established analytically, not inferred by interpolation from these tests.

Run from this directory:

    python flagged_readout_checks.py > producer-workspace/flagged_readout_replay.json
    cmp flagged_readout_checks.json producer-workspace/flagged_readout_replay.json

The primary attenuation input is the one already read and pinned in SOURCE_SCOPE.md: Ivan, Sabapathy and Simon, [arXiv:1012.4266](https://arxiv.org/abs/1012.4266), Section IV Eq. (4.6), with intensity transmissivity \(\eta=\kappa^2\). The main note and its accepted independent review supply the full-operator thinning identity and fine-row instrument. No fresh primary claim or hardware value is imported.

The accepted main review also contains the reviewer's separately authored fresh-code-only comparison: when the input is guaranteed to have zero pre-existing syndrome, all up-to-q losses are handled before the flag, and after forgetting the fine count the erasure probability is \(\Pr\{\operatorname{Binomial}(N,1-\eta)>q\}\). That stronger special-input result is consistent with this addendum and is not promoted to arbitrary coherent admitted syndromes. It is not an independent review of this addendum.

The new authored contributions here are the one-miss actual-count exclusion on the full admitted space, same-record correct-or-flag reference, exact bad-effect complete-metric reduction, uniform two-miss bound, separate flag witness and q=1 sharp example. Their independent review status is recorded separately from FLAGGED_READOUT_AUTHOR_RECEIPT.json. No historical-priority claim is made.
