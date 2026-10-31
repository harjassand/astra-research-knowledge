# A restricted physical simulator acquired from reversible calibration data

## What was constructed, and what was not

This work began with the desired ability to learn a small reusable simulator of an unknown controlled process, then safely use it for long adaptive experiments. Low observable rank alone does not make that possible: it does not locate a well-conditioned experimental core, supply a stable norm, or supply a positive realization. A raw signed spectral model can amplify errors or assign negative probabilities. A finite classical positive realization need not exist even for a rank-three coherent process.

The completed construction here is narrower. After a genuine rank-four core has been acquired, reversible calibration controls determine the qubit Bloch geometry up to one scalar. Searching that scalar and repairing each instrument independently produces an actual positive simulator. A residual certificate then controls every classical feedback transcript. The simulator is used to optimize and execute a finite conditional recovery task in a synthetic experiment. The construction permits a mixed unknown starting state and rank-deficient Choi matrices.

This is a constructive restricted route, not an established new scientific primitive. Common invariant metrics, linear gate-set tomography, scalar SPAM gauge fixing, projected process tomography, and true-prefix/fitted-suffix perturbation are established machinery. The search below did not find a defensible major consequence unavailable to those methods under the same added assumptions. The useful deliverable is an explicit composition, executable learner, and exposed cost/failure boundary. No practical advantage, historical novelty, rank-only acquisition theorem, or efficient general planner is claimed.

The original pure-start version is preserved in `results_pure_anchor.json`. The final learner removes that extra premise by paying for a one-dimensional scale search. Its numerical source starts with Bloch radius 0.73, unknown to the learner.

## 1. Exact input, output, and cost contract

### Source and legal experiments

There is a stationary finite action/outcome interface. A native branch is (z=(a,o)). Independent whole-process restarts are available. Four normalized legal preparation procedures (p_j) are chosen, with (p_0) the empty preparation. Four future event tests (t_i) are chosen, with (t_0) the trace test. A supplied upper bound of four on the full observable rank applies to this entire action/test interface. The rank bound is architectural information, not a conclusion of numerical rank estimation.

Define the exact probability tables

\[
 H_{ij}=\Pr(t_i\mid p_j),\qquad
 (H_z)_{ij}=\Pr(z, t_i\mid p_j).
\]

The future test follows the native branch in the second table. Its probabilities are joint probabilities, so no postselection denominator is hidden. The trace row of (H) is exactly (mathbf 1^T). The trace row of (H_z) records the native outcome probability. The native maps may have outcomes that retain memory.

Counts produce simultaneous entrywise confidence bands

\[
 |H-\widehat H|\le D_H,\qquad
 |H_z-\widehat H_z|\le D_z. \tag{1}
\]

All inequalities between matrices in this note are entrywise unless an operator order is written explicitly. A finite pool must be covered before data-dependent core choice, or a fresh-sample/sequential confidence allocation must be specified. Every failed core, repeated preparation, word length, and precision stage is charged.

### Additional promise for eventual success of the proposal algorithm

Soundness of a returned certificate uses only the rank/core/probability contract above and a valid fitted physical candidate. Eventual success of the particular candidate constructor uses more:

* The source has a full-observable-rank qubit realization.
* A declared subset of deterministic native controls consists exactly of unitary channels.
* Their rotations on the three-dimensional traceless space act irreducibly. Equivalently for the argument below, the common fixed-point system has a positive smallest singular value and the invariant symmetric forms have dimension one.
* The legal core is genuinely nonsingular.

No unitary axes, angles, initial state, effects, Kraus operators, physical gauge, pure state, or exact expectation oracle is supplied. The other native instruments can be arbitrary qubit CP instruments. No strictly positive Choi eigenvalue is required. The unitary and qubit promises cannot be validated just by a low numerical residual.

### Returned object

The output is a density matrix (sigma_0), full fitted instruments (Phi^f_{a,o}), and a number (b). It is an ordinary classical program that stores and updates a two-by-two density matrix and samples native outcomes. On (1), for every classical feedback controller with at most (L) native calls,

\[
 \operatorname{TV}(P_{\rm source},P_f)\le \min(1,bL). \tag{2}
\]

For a stopping rule, (L) can be replaced by the source's expected active call count if both complete records terminate almost surely. A separately paid abort clock guarantees that condition. This is a classical transcript theorem. It does not identify the physical source memory or provide closeness against arbitrary external coherent references.

### Costs

For (K) uncertain probability slots and (N) independent starts per slot, Hoeffding widths are

\[
 w=\sqrt{\log(2K/\alpha)/(2N)}.
\]

The physical bill is (KN) starts and (Nsum_s\ell_s) native interventions, where (ell_s) is the full length of the experiment for slot (s). A fixed core has fixed conditioning constants, but they can be large. The candidate computation uses small linear solves, eigendecompositions, and a scalar search. A complete global scalar mesh with spacing proportional to the desired matrix error costs inversely in that error. The implemented heuristic uses a coarse global mesh and five local refinements; it does not certify global optimality. Its *final residual certificate* is independent of how it proposed the candidate.

The finite planner implemented here explicitly enumerates a policy tree. Its cost grows exponentially with horizon. This construction does not remove that separate planning cost.

## 2. Acquiring the exact observable representation

Because (H) is nonsingular and the full observable rank is at most four, the four preparations span the entire observable quotient. In preparation coefficients, every true native branch is

\[
 C_z=H^{-1}H_z. \tag{3}
\]

To see this, apply all four tests to each prepared basis state after the branch. The result is (H_z), and invertibility identifies its coordinates. Linearity and rank exhaustion then extend the identity to all reachable states and all future words. Merely observing four sizable singular values in one noisy table would not justify this extension.

Write (	au=mathbf 1^T), and let (e_0) denote the empty-preparation coordinate. True causality gives (sum_o	au C_{a,o}=	au). If (h) is a true prefix, its unnormalized coordinate is (c_h) and probability is (p_h=	au c_h). Positivity of *actual future events* gives

\[
 (Hc_h)_0=p_h,\qquad 0\le(Hc_h)_i\le p_h. \tag{4}
\]

The coefficients (c_h) themselves may be negative. Equation (4), not positivity of those coefficients, is the source of the later stability estimate.

Set (U=widehat H^{-1}), (A=|U|D_H). If (|A|_infty<1), the Neumann expansion proves

\[
 |H^{-1}|\le M=(I-A)^{-1}|U|,
 \qquad |H^{-1}-U|\le R=M-|U|. \tag{5}
\]

For example, an acquired bound on true normalized coefficients is

\[
 K_{\rm core}
 =\max_{v_0=1,\;v_i\in\{0,1\}}
       \big(\|Uv\|_1+\mathbf1^TRv\big).
 \tag{6}
\]

Convexity extends this finite maximum over eight vertices to the whole probability cube, and (4) gives (|c_h|_1\le K_{\rm core}p_h). The dependence on inverse-core conditioning is real and remains in every cost statement.

## 3. Recovering the Bloch shape without calibrated axes

This section is a proposal mechanism. Its correctness as a geometry reconstruction uses the reversible-qubit promise. The final law bound in Section 6 does not assume that its approximate metric is correct.

Choose a fixed Euclidean-orthonormal matrix (V\in\mathbb R^{4\times3}) whose columns span (ker\tau). First estimate (widehat C_a=widehat H^{-1}widehat H_a) for the deterministic calibration controls, and repair their trace row to exactly satisfy (	auwidehat C_a=	au). Every repair is charged by the final measured residual.

### Common center

In the exact model, there is a unique common trace-one fixed point (c_*), the coordinate of the maximally mixed state. Write (c_*=e_0+Vu_*). Let

\[
 B_a=V^TC_aV,
 \qquad d_a=V^T(C_ae_0-e_0).
\]

Then ((I-B_a)u_*=d_a). Stack these equations and solve them by least squares. Uniqueness follows because a difference of two solutions would be a vector fixed by every irreducible three-dimensional rotation. The numerical method records the smallest singular value and residual of this system.

### Invariant metric

Let the physical Bloch-coordinate map on (ker\tau) be (W\), so the exact controls satisfy (WB_a=R_aW), with (R_a\in SO(3)). The form (G=W^TW) obeys

\[
 B_a^TGB_a=G. \tag{7}
\]

All symmetric invariant forms are scalar multiples of this one. Indeed (W^{-T}G'W^{-1}) is symmetric and commutes with every (R_a); each of its eigenspaces is invariant, so irreducibility forces it to be scalar. Fix the scale provisionally with (operatorname{tr}G=3). The resulting six-variable linear system has a unique solution. Its smallest singular value is another explicit conditioning parameter.

Apply the same system to the estimated controls and reject if the resulting symmetric (widehat G) is not positive definite. Put (widehat L=widehat G^{1/2}), and form provisional coordinates

\[
 S_0c=\begin{pmatrix}\tau c\\
 \widehat L V^T(c-(\tau c)\widehat c_*)
 \end{pmatrix}. \tag{8}
\]

In the exact limit the physical Bloch coordinates have the form (operatorname{diag}(1,sO)S_0c), where (s>0) and (O\in O(3)). Proper rotations are unitary conjugations. Improper rotations are a unitary conjugation combined with transposition. Conjugating both input and output of a CP map by that transposition preserves CP: its Kraus matrices are complex-conjugated. Thus either orientation is usable for a physical candidate.

This is ordinary simultaneous unitarization. Rebranding it as an acquired norm would not create a new learning operation.

## 4. Paying for the remaining physical scale

The common metric has not determined the Bloch-ball radius. Setting the starting state's radius to one is valid only with a supplied pure-start promise. That earlier version fails on the mixed-start fixture; its residual does not vanish. The final method searches the remaining scalar.

In exact provisional coordinates let (y_j) be the spatial part of (S_0e_j). Every prepared state is physical at the true scale, so

\[
 s\le u:=1/\max_j\|y_j\|_2. \tag{9}
\]

For a future test, write (H_iS_0^{-1}=(a_i,b_i^T)). In physical Bloch coordinates its effect has vector (Ob_i/s). Since an effect lies between zero and identity,

\[
 \|b_i\|_2/s\le\min(a_i,1-a_i)\le1/2.
\]

Consequently (s\ge2\beta), where (eta=max_{i>0}\|b_i\|_2>0). The strict positivity follows from invertibility of (H); otherwise all test rows would be proportional to trace. Thus

\[
 2\beta\le s\le u. \tag{10}
\]

An estimated range ([min(widehat u/4,widehateta/2),1.2widehat u]) contains the true scale once the core estimates are sufficiently accurate. The numerical constants merely leave slack. They are not confidence bounds on the hidden scale. They are unnecessary for the soundness of a final successful certificate.

For each tested scale (s'), project each provisional vector (s'widehat y_j) onto the closed unit ball and use the resulting four density matrices as columns of a map (T), or equivalently a real Pauli-coordinate matrix (S). Reject singular (S). The Euclidean projection is nonexpansive, so a grid scale approaching the true scale and consistent metric data give (S\to S_{m true}) up to the harmless orthogonal orientation.

Searching this one scalar is a substantive cost but not a new conceptual primitive: the isotropic SPAM-scale freedom is expressly discussed in ordinary GST. A one-dimensional mesh replaces a generic nonconvex gauge search only because the exact reversible-calibration promise has already eliminated the other gauge degrees of freedom.

## 5. Boundary-safe physical instrument repair

For a fixed candidate basis (S), transform the raw observable estimate into Pauli transfer matrices

\[
 \widehat F_z=S\widehat C_zS^{-1}.
\]

Their Hermitian Choi matrices need not be positive. The following explicit repair uses no strictly positive Choi eigenvalue.

For each action, clip the negative eigenvalues of each branch Choi matrix, obtaining (J_z^+\succeq0). In the input-first Choi convention put

\[
 T_a=\sum_o\operatorname{Tr}_{\rm out}J_{a,o}^+.
\]

If (T_a\) is singular, reject the proposal. Otherwise define

\[
 J^f_{a,o}=(T_a^{-1/2}\otimes I)
                J_{a,o}^+
             (T_a^{-1/2}\otimes I). \tag{11}
\]

These are positive and their summed output partial trace is identity, so they are the Choi matrices of a genuine instrument. The resulting fitted operators (F^f_z) give (C^f_z=S^{-1}F^f_zS). The initial density matrix is column zero of (S). Because (S) is square and invertible, (TC^f_z=Phi^f_zT) exactly. No hidden candidate-rank search is needed in this square lift.

For the designated unitary controls, the implementation instead takes the nearest proper orthogonal matrix to the estimated spatial block, sets the affine translation to zero, and fixes the trace row. This is a genuine unitary channel. Its entire residual is still charged. A completely general implementation could use (11) for these branches too.

### Why this repair remains consistent on the CP boundary

Suppose the raw Hermitian Choi matrices approach true (J_z\succeq0). Projection onto the PSD cone is nonexpansive in Frobenius norm:

\[
 \|J_z^+-J_z\|_F\le\|\widehat J_z-J_z\|_F.
\]

For input dimension two, output partial trace has Frobenius norm at most (sqrt2) times the input Frobenius norm. Hence (T_a\to I). Its inverse square root is continuous in a neighborhood of identity, so (11) converges to (J_z). Zero eigenvalues of individual branch Choi matrices cause no discontinuity. Only invertibility of the *summed normalization marginal*, which converges to (I), is used.

For a quantitative estimate, if (|T_a-I|_{m op}\le\eta<1), then

\[
 \|T_a^{-1/2}-I\|_{m op}\le (1-\eta)^{-1/2}-1.
\]

Expanding the congruence bounds the repair error by the original PSD-projection error plus ((2q+q^2)|J_z^+|_F), where (q=(1-eta)^{-1/2}-1). This is a local Lipschitz estimate with no minimum positive eigenvalue of (J_z).

The repair is standard process-tomography machinery. It is not an independent novelty claim. Its role here is to ensure the candidate is positive before using it in an adaptive experiment.

## 6. A full classical-transcript certificate

The following is a square-lift specialization of Astra's existing physical-residual simulator argument. It is included in full so the precise consequence and information bill are reviewable.

For any fitted physical candidate from Section 5, compute

\[
 E_z=M\big[D_z+D_H|C^f_z|
             +|\widehat H C^f_z-\widehat H_z|\big]. \tag{12}
\]

The exact identity

\[
 H(C_z-C^f_z)=H_z-HC^f_z
\]

and (1),(5) prove (|C_z-C^f_z|\le E_z). This charges raw count uncertainty, gauge choice, state projection, CP repair, TP normalization, and numerical repair residuals, if the last are included in the implementation's bounds. Define

\[
 g_a=\max_j\sum_{o,i}(E_{a,o})_{ij},
 \qquad b=\tfrac12K_{\rm core}\max_ag_a. \tag{13}
\]

**Theorem.** On the simultaneous confidence event, the complete classical feedback laws of the true source and fitted simulator from their respective empty starts obey (2). The controller may be chosen after seeing all calibration data.

**Proof.** Each column (sigma_j=T(e_j)) is a density matrix. Therefore, for every real vector (v),

\[
 \|T(v)\|_1
 =\|\sum_jv_j\sigma_j\|_1\le\sum_j|v_j|=\|v\|_1. \tag{14}
\]

A fitted feedback continuation is a CPTP map from a signed Hermitian input to its complete classical outcome record. Trace-norm contraction bounds its output signed-measure (\ell_1) norm by (14).

Telescope word/tree probabilities using **true prefixes and fitted suffixes**. At a true prefix (h), action (a), the local insertion is ((C_{a,o}-C^f_{a,o})c_h). Its total fitted continuation has signed-measure norm at most

\[
 \sum_o\|(C_{a,o}-C^f_{a,o})c_h\|_1
 \le g_a\|c_h\|_1
 \le2bp_h. \tag{15}
\]

At each time the sum of true active prefix probabilities is at most one. Summing (15) over at most (L) times and dividing by two proves (2). The intermediate telescoping expressions need not be positive probability laws; only true prefix probabilities are used as weights. Private randomization is a convex average. Every controller uses the same action on the same observed prefix in both endpoint processes, so adaptive choice introduces no extra factor or union bound.

For unbounded but integrable stopping, truncate with a labelled censor outcome. The finite bound sums the true probabilities of making each call, producing (b\mathbb E_{m true}\min(L,n)). Almost-sure termination of both endpoints removes the censor tails, and monotone convergence gives (b\mathbb E_{m true}L). An independent abort coin of probability (delta) before each call gives (\mathbb E L\le(1-delta)/\delta). This does not imply a bound for normalized rare postselected histories. QED.

**Square-lift point.** The four candidate density matrices do not have to be the states generated by replaying the source's core-preparation words on the candidate. They are a physical basis assigned to the four source coordinate labels. Exact (TC^f_z=Phi^f_zT), the specified initial column, and (14) are enough. This eliminates the candidate-rank obligation of a larger non-invariant physical realization. It does not eliminate the source rank/core obligation.

## 7. Eventual acquisition and its quantitative dependencies

Fix a source satisfying the reversible-qubit promise and a genuinely nonsingular legal core. Shrinking simultaneous count bands gives (widehat C_z\to C_z). The fixed-point solve and the normalized invariant-metric solve are continuous because their exact stacked matrices have positive smallest singular values. Positive definiteness and basis invertibility therefore hold eventually.

The true scale lies in the limiting interval (10). A global grid whose mesh tends to zero supplies a candidate scale approaching it. State projection is continuous; Choi clipping and marginal normalization are continuous at the true source; consequently (C^f_z\to C_z). Equations (12)–(13) then give (b\to0). This is an actual candidate-acquisition route, rather than a supplied physical-gauge oracle.

The local perturbation bounds are ordinary finite-dimensional ones. For a linear system (Fx=y), with observed (widehat F,widehat y), bounds (|F-widehat F|\le\Delta_F), (|y-widehat y|\le\Delta_y), and (sigma_{min}(widehat F)>\Delta_F), any chosen (widehat x) obeys

\[
 \|x-\widehat x\|\le
 \frac{\|\widehat F\widehat x-\widehat y\|
       +\Delta_F\|\widehat x\|+\Delta_y}
      {\sigma_{\min}(\widehat F)-\Delta_F}. \tag{16}
\]

For the metric equation, if (|B-widehat B|\le d), the induced perturbation on symmetric forms satisfies

\[
 \|B^TXB-\widehat B^TX\widehat B\|_F
 \le(2\|\widehat B\|d+d^2)\|X\|_F. \tag{17}
\]

Positive square roots obey the usual denominator involving the sum of the smallest square roots of the two positive matrices' eigenvalues. These estimates, inverse-core bounds, the scale lower bound, and the candidate basis singular value give a finite local Lipschitz bill. Thus for a fixed sufficiently conditioned instance, the required count accuracy is proportional to (epsilon/L), with a source-dependent constant, and the Hoeffding start count scales as (epsilon^{-2}L^2). The scalar grid costs a further inverse-accuracy factor if used globally. No conditioning-free claim is made.

The implemented scalar proposal is faster than the full mesh and often finds a lower residual, but its success is empirical. It is never used as a proof that no better gauge exists. A rejected candidate returns UNKNOWN.

### Finite arithmetic

The proof defines exact-real candidates. A rigorous implementation can use rational approximations to Kraus factors after PSD clipping, then an exact/algebraically represented two-by-two normalization of their summed effect. This preserves CP and TP by construction. Rational-quaternion approximations can similarly make calibration controls exactly unitary. Directed interval bounds must cover all coordinate, inverse, and residual computations. The present NumPy/SciPy implementation does **not** perform that directed-interval work; its numbers are reproducible numerical diagnostics, not independently verified finite-bit certificates. Near-zero Choi eigenvalues at floating precision are reported, not treated as an exact PSD proof.

## 8. Downstream decision actually performed

For any terminal reward in ([0,1]), (2) implies a policy-value error of at most (epsilon=bL). If an exactly optimal fitted policy is chosen from a declared policy class, its true regret against the true optimum in that same class is at most (2\epsilon). The proof is the two value discrepancies on either side of the fitted optimality inequality. An approximate planner adds its own optimization error.

The experiment fixes a unitary excitation call (X), then a monitored damping action (D). After seeing (D)'s outcome, it permits three recovery calls selected adaptively from (X,Y,M,D), and finally reads (M). The objective is final outcome one. The candidate planner enumerates the full tree, including histories whose candidate probability is tiny. A valid fallback posterior specifies its action on every such history. The same fixed policy tree is then evaluated against the synthetic source. This is an actual feedback task, not merely an endpoint matrix comparison. The planner visits 518 states in this small case. Its horizon dependence is exponential.

## 9. Numerical experiment and retained failures

Run `python run_experiment.py` in this directory. `learner.py` imports no source fixture or truth probabilities. `source_fixture.py` generates independent aggregate binomial counts. `run_experiment.py` passes only those counts and the legal architecture labels to the learner; it uses the plant only for separate evaluation and oracle comparison.

The source contains two noncommuting exact unitary controls, a projective readout instrument, and a monitored amplitude-damping instrument. Every branch Choi matrix has rank one. The starting Bloch radius is 0.73. Legal core preparations are the empty word, (X), (Y), and (XX); future event tests are trace and three (M)-outcome tests. There are exactly 100 uncertain probability slots. The longest experiment has five native calls. The source uses 328 native calls per one repetition of every slot.

Each row below is a separately calibrated run with nominal confidence failure (alpha=0.01); it is not a single simultaneous guarantee across all rows.

| Starts per slot | Total starts represented | Native calls represented | Actual six-call transcript TV | Numerical uniform TV bound |
|---:|---:|---:|---:|---:|
| (10^6) | (10^8) | (3.28\times10^8) | (0.00735075) | (1) |
| (10^8) | (10^{10}) | (3.28\times10^{10}) | (0.000738038) | (1) |
| (10^{10}) | (10^{12}) | (3.28\times10^{12}) | (0.0000738317) | (0.0993643) |

The source-optimal value of the declared recovery task is approximately 0.9778259476. All three learned policies attain that value on this fixture; this does not establish performance on other plants or policies. The largest run's fitted value is approximately 0.9777581488. The computation proposes a candidate in about four tenths of a second in this environment, but this speed excludes physical data acquisition and does not justify the enormous count bill.

Only 100 binomial aggregate draws are performed per run. No billion-trajectory experiment was executed. The count totals are the mathematical acquisition charge that those sufficient statistics represent. The conservative confidence bound is much worse than the observed error. This result supplies no practical sample advantage.

Two useful failures are retained in `results.json`:

1. The first proposed core used the empty word, (X), (Y), and (XY). Its four prepared Bloch points are affinely dependent: (R_YR_Xz=R_Xz+\cos(\theta_X)(R_Yz-z)). The true table has rank three. Sampling noise made the numerical matrix invertible, but the Neumann confidence gate rejected it. This failed trial represented another (10^8) starts and (3.28\times10^8) native calls. It cannot be silently omitted from an end-to-end acquisition strategy.
2. Applying the earlier pure-anchor normalization to the final mixed-start counts gives a physical candidate with a nonvanishing residual and a vacuous six-call bound. The extra scalar cannot be fixed from a metric normalization alone. The final scale search uses the same already paid counts.

The replay also checks the Choi/transfer conversion, actual candidate normalization, observed residual-band containment, and negative three-branch predictions in the raw signed model. These finite checks do not prove the universal theorem. The source condition number, metric/fixed-point gaps, fitted eigenvalues, full policy tree, and all numerical diagnostics are retained in `results.json` and `fitted_model.json`.

## 10. Strongest established route and the remaining opening

The literature comparison changes the interpretation of this work:

* **Linear GST already acquires the observable representation.** Nielsen et al., *Gate Set Tomography*, Quantum 5, 557 (2021), Sections 3 and 6, derives the simultaneous gauge freedom and discusses physicality, gauge fixing, and isotropic SPAM scaling. Its full MLE problem is nonconvex, but LGST is deliberately a linear-algebra initialization. It would be incorrect to present (3), ordinary unitarization, or scalar SPAM fixing as a new discovery. [Primary text](https://arxiv.org/html/2009.07301v2).
* **Physical projection already has developed theory and implementations.** Surawy-Stepney et al., *Projected Least-Squares Quantum Process Tomography*, Quantum 6, 844 (2022), analyzes physical Choi projection with nonasymptotic error guarantees. Knee et al. (2018) provides a CPTP-projection algorithm. Afham, Sen, and Tomamichel (September 2026) explicitly identify the inverse-marginal congruence as folklore and prove a stronger fidelity-projection result. Our simple repair does not supersede these. [PLS](https://arxiv.org/abs/2107.01060), [CPTP projection](https://arxiv.org/abs/1803.10062), [partial normalization](https://arxiv.org/abs/2609.39941).
* **Stable predictive learning already supports broad statistical consequences.** Chen, Bai, and Mei, *Partially Observable RL with B-Stability* (ICLR 2023), supplies sample-efficient all-policy model estimation under its structural conditions and associated optimization operations. A stable signed coordinate system is not itself a new all-policy learning theorem. [Primary paper](https://arxiv.org/abs/2209.14990).
* **Astra already has the law argument and a general candidate existence route.** The pinned N1166 physical-residual source permits boundary CP maps and proves (b\mathbb E L) transcript error. It pays a costly physical candidate/rank search. The square qubit constructor here makes the candidate step explicit under extra reversible-calibration structure; it does not solve the general source's search problem. The complete source is preserved in `sources/ASTRA_PHYSICAL_RESIDUAL_SIMULATOR.md` with original repository revision `cb87e72296824ae2a677ccd337025d02d20cbb0a` and source SHA-256 `59b53f8b7a4d54e2f38cb7eb3d643c13d4b356646a3de14967dfa1df6d0da6f2`.
* **Astra N1515/N1521 already acquired stable signed/Euclidean coordinates with conditioning paid.** Their endpoint-scalar guarantee and their explicit lack of an efficient general planner must remain distinct from the actual full instrument/policy law considered here. Their packet routes at the same revision were read to avoid mistaking stable coordinates for a new downstream capability.

The strongest equally informed conventional route is therefore **LGST, structural unitarization and SPAM-scale fitting, established CPTP repair or constrained fitting, followed by the existing residual certificate and ordinary finite-policy planning**. That route can reproduce this construction. No experiment against mature GST software was performed, and no computational or statistical advantage over that route has been established.

The remaining research opening is considerably harder: acquire a useful positive/operational geometry and a low-cost all-policy certificate from noisy experiments without exact reversible controls, a qubit shape promise, an already accessible conditioned core, or a generic nonlinear realization oracle. The present scalar search does not accomplish that. The billions-to-trillions represented count bill also shows that constructing the state representation is only one obstruction; a sharp, useful acquisition-to-decision uncertainty calculation is another. These are the remaining operations, not claims already earned by this note.
