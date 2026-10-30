# A finite local interface to an uninitialized interacting medium

These are root-working derivations, with executable checks. They do not change the status of earlier accepted Astra foundations. No priority claim is made for quantum interrogation, Zeno convergence, heralded entanglement, or their established protocols.

## 1. Scope and the construction chosen

The new result is a sufficient physical-interface law. A local exchange whose unknown coupling is a positive operator can be turned into an absorber with a uniform opacity bound, despite arbitrarily fast, noncommuting, common memory evolution. Known quantum-interrogation circuits can use that absorber. Keeping the memory operators throughout gives a full parity-instrument bound and a more economical task-specific Bell-resource bound. A further operator inequality makes the resource guarantee survive repeated use with correlated memory histories.

The medium is never prepared, measured, reconstructed, reversed, or reset. The photons, auxiliary levels, outgoing drain modes, computational input qubits, and classical optical controller are separate physical resources. Renewal occurs in the drains and input preparations; it is not free restoration of the medium.

This is a different setting from both the original signed spin handles and the positive operator-force apparatus. In particular, neither a positive bias, a qutrit optical transition, a photon source, a pure optical rotation, nor a local computational-qubit preparation follows from the old signed spin handles.

The earlier force support theorem and its complete sector-instrument condition remain intact. This construction supplies an approximate parity interface from local couplings instead of assuming a native two-data-qubit operator Q in a force Hamiltonian. The earlier dirty-ancilla gate identities still require their actual measurement bank and their full-instrument error budgets. An approximate parity interface alone is not a universal computer.

## 2. Local physical model, finite region, and source

At one node let the stationary system have states 0, 1, e, and let b be a local risky optical mode. In the rotating frame use

\[
H_{\rm tap}(t)=I\otimes H_M(t)
+\bigl(|e\rangle\langle1|b+|1\rangle\langle e|b^\dagger\bigr)\otimes G_M(t),
\qquad 0<g_-I\le G_M(t)\le g_+I.
\]

Only one photon is supplied. The active block is spanned by \(|1,1_b\rangle,|e,0_b\rangle\). The state 0 is dark. The safe optical rail never enters this transition. When the optical mode is empty and the auxiliary level is unoccupied, both computational levels experience the same memory propagator.

The requirements are local selection rules and a common idle Hamiltonian, rather than a two-qubit parity interaction. They are substantive: a supposedly dark branch that scatters, or a persistent logical-state-dependent bath potential, violates the model.

An effective cavity dipole Hamiltonian provides a concrete origin for a real operator-valued G. For example, on a confined motional region,

\[
G=g_0\cos(k\hat x)\exp[-(\hat y^2+\hat z^2)/w^2].
\]

If the admitted position domain obeys \(|k x|\le a<\pi/2\) and \(y^2+z^2\le R^2\), then

\[
g_0\cos(a)e^{-R^2/w^2}I\le G\le g_0I.
\]

Unknown kinetic motion and interactions belong to H_M; they need not commute with G. A hard confinement domain is an exact theoretical example. A finite-depth trap with a small escape probability is only a qualified approximation, not an all-state promise. Its leakage must be controlled over the entire reuse history. State-insensitive trapping is a relevant established technique, but its demonstrated small differential shifts are not an exact common-Hamiltonian certificate [6,7].

Another sufficient construction is a real identity bias, \(G=g_0I+E\), with a structural bound \(\|E\|\le a g_0<g_0\). The real coupling phase, the bias, and the norm qualification all cost resources. An arbitrary complex operator multiplying the optical transition is not covered by naming its smallest singular value.

To remove e, couple it to a fresh drain mode d through

\[
H_{\rm drain}=I\otimes H_M+
(|0\rangle\langle e|d^\dagger+|e\rangle\langle0|d)\otimes G_d.
\]

The drain starts in vacuum and leaves after its interaction window. Absorption followed by draining can change logical 1 into 0. Failed gates can therefore damage live data. The Bell factory below discards or resets its operands after failure.

A real source can likewise start a separate emitter in its excited state and exchange one excitation into an initially empty probe mode. The transfer lemma below gives a nonzero emission probability without fine gain calibration. The source is then isolated, preventing late emission. In the one-excitation model an eventual probe detection excludes a drain photon or residual auxiliary excitation. Preparing the source excitation, resetting source and data systems, supplying vacuum modes, and releasing a fixed optical mode are physical operations. Multiple photons, dark counts, and memory-dependent release shapes are separate errors.

The rigorous matrix theorem below applies to every finite memory dimension. A continuum motional version needs the stated common self-adjoint propagation and a convergent approximation that preserves the bounded coupling inequalities. A finite-dimensional numerical truncation alone does not establish that qualification.

## 3. Uniform opacity from a positive local exchange

Let U_+ and U_- be the propagators of \(H_M(t)+G(t)\) and \(H_M(t)-G(t)\) over a tap of duration tau. On the active two-level block,

\[
U_{\rm active}=\begin{pmatrix}A&B\\B&A\end{pmatrix},\qquad
A=(U_++U_-)/2,\quad B=(U_+-U_-)/2.
\]

A is the amplitude for the probe to remain in the risky mode; B transfers its excitation into e. Unitarity gives \(A^\dagger A+B^\dagger B=I\).

**Opacity lemma.** For \(0<g_-\tau\le g_+\tau<\pi\),

\[
\|A\|\le r(\tau):=
\max\{|\cos(g_-\tau)|,|\cos(g_+\tau)|\}<1.
\]

In particular, choose

\[
\tau_*={\pi\over g_-+g_+},\qquad
r_* =\cos\!\left({\pi g_-\over g_-+g_+}\right)<1.
\]

Then every initial memory/reference state transfers at least probability \(1-r_*^2\) into e. No bound on \(\|H_M\|\), \([H_M,G]\), or the speed of the memory orbit appears.

Within the first-return window \(0<\tau<\pi/g_+\), this is the minimax fixed-duration tap: scalar couplings at the two interval endpoints already impose the two cosine terms, and their maximum is minimized when \(g_-\tau+g_+\tau=\pi\). This is a local one-tap optimality statement, not a lower bound on arbitrary control. A wide gain ratio R=g_+/g_- has \(1-r_*\sim\pi^2/(2R^2)\); a very broad coarse box therefore carries a substantial cost even without fine calibration.

**Proof.** The relative propagator \(W=U_-^\dagger U_+\) obeys

\[
\dot W=-2i\,U_-^\dagger G U_-W.
\]

Its instantaneous generator lies between \(2g_-I\) and \(2g_+I\). Every continuously unwrapped eigenangle therefore lies in the clockwise interval \([2g_-t,2g_+t]\). At an eigenvalue degeneracy, diagonalize the generator compressed to the degenerate eigenspace; its possible eigenangle velocities obey the same bounds. Piecewise smooth approximation then covers piecewise continuous H_M and G. The upper bound \(2g_+\tau<2\pi\) excludes a complete return of any eigenangle.

Since

\[
A^\dagger A={2I+W+W^\dagger\over4},
\]

its eigenvalues are \(\cos^2(\varphi/2)\) for angles in that interval, proving the claim. Equivalently, at tau_* remove the scalar generator \((g_-+g_+)I\). The remaining unitary path has angular length at most \((g_+-g_-)\tau_*<\pi\), and the removed phase equals pi. This gives the same spectral arc. QED.

For timing in an interval \([\tau_l,\tau_h]\), use the worst endpoint of the enlarged arc \([g_-\tau_l,g_+\tau_h]\). Thus coarse timing windows are legitimate. For gains in [1,2] and a 5% timing window around pi/3, \(r\le0.587785253<0.6\).

Finite switching ramps are also allowed. Replace the endpoint angles by \(\Gamma_\pm=\int g_\pm(t)dt\), require \(0<\Gamma_-\le\Gamma_+<\pi\), and use \(r=\max(|\cos\Gamma_-|,|\cos\Gamma_+|)\). The lower envelope may vanish at the start and end of a pulse. The theorem needs a qualified integrated window, not an instantaneous switch.

**Active-channel model errors.** Suppose an additional bounded Hamiltonian acts only in the active photon/auxiliary block, preserves excitation number and the dark/idle branch, and has integrated norm at most xi_tau. Duhamel's estimate gives \(\|A_{\rm real}\|\le r+\xi_\tau\). If this remains below one, all subsequent proofs apply with the worse r. Auxiliary detuning therefore need not be learned to the final logical accuracy; it needs a coarse enough bound to retain opacity. A permanent logical-state-dependent potential is outside this argument.

## 4. Arbitrary operator contractions inside a known Zeno circuit

Use a qualified optical rotation

\[
R_\theta=\begin{pmatrix}c&-s\\s&c\end{pmatrix},\quad
c=\cos\theta,\ s=\sin\theta,\ \theta=\phi/N.
\]

The optical controller acts on the meter alone. It is not a free consequence of the dirty-medium coupling. After each rotation, the tap and its drain act. Conditioned on no photon loss, the bright computational state 1 has a stage matrix

\[
T_j=\operatorname{diag}(V_j,A_j)(R_\theta\otimes I),
\quad V_j\text{ unitary},\quad\|A_j\|\le r<1.
\]

The dark state 0 has \(R_\theta\otimes V_j\). The V_j include all common forward memory evolution during tap, drain, and holding windows. They and A_j may vary at every visit. No commutation, stationarity, bath preparation, or independent-history assumption is made.

Write the bright product as \(M_N=\begin{pmatrix}u&v\\w&z\end{pmatrix}\), and \(V=V_N\cdots V_1\). Put

\[
q=r c,\quad L={1-q^N\over1-q},
\]

\[
D=N(1-c)+{rs^2\over1-q}(N-L),\quad
\alpha=sL,\quad\beta=rsL,\quad
\gamma=q^N+{rs^2(1-q^N)\over(1-q)^2}.
\]

Then, for N at least two and \(0<\theta\le\pi/2\),

\[
\|u-V\|\le D,\quad\|v\|\le\alpha,
\quad\|w\|\le\beta,\quad\|z\|\le\gamma.
\]

**Proof.** Conjugate each stage by the accumulated common V. This leaves the rotations unchanged and replaces A_j by an arbitrary contraction of the same norm. For a safe input, \(u_j=c u_{j-1}-s w_{j-1}\) and \(w_j=A'_j(su_{j-1}+cw_{j-1})\). Contractivity implies \(\|u_j\|\le1\), so

\[
\|w_j\|\le rs\sum_{k=0}^{j-1}q^k.
\]

Telescoping u gives D. For v, apply the adjoint product to a safe input. The order is reversed and the contraction precedes each inverse rotation. Its risky amplitude obeys \(x_j\le s+q x_{j-1}\), giving alpha. Finally the risky-input lower block obeys \(\|z_j\|\le q\|z_{j-1}\|+rs\|v_{j-1}\|\), giving gamma. QED.

The leading safe-block error is

\[
D={\phi^2\over2N}{1+r\over1-r}+O(N^{-2}).
\]

This convergence rate and its scalar imperfect-absorber antecedent are established Zeno machinery [1,2,4]. The use here is a uniform operator certificate for arbitrary retained-memory histories, tied to the finite local opacity lemma.

## 5. Full parity instrument, including within-sector coherence

Use phi=pi at each of two local nodes, a reference rail bypassing both nodes, and a balanced final interferometer. Route a residual risky-rail photon out after each node. This is an outgoing reject port, not a nondestructive detector secretly supplied on the safe rail.

The photon starts in an equal reference/signal superposition. Define \(V=V_2V_1\). For computational states 00,01,10,11 the accepted signal blocks are

\[
V,\quad-u_2V_1,\quad-V_2u_1,\quad u_2u_1.
\]

Consequently, for \(Q=Z_1Z_2\),

\[
\|W_{\rm signal}-Q\otimes V\|\le d:=D_1+D_2.
\]

The two detected branches are

\[
K_\pm={I\otimes V\pm W_{\rm signal}\over2},
\quad
\|K_\pm-\Pi_\pm\otimes V\|\le d/2.
\]

This is a joint operator statement, not merely a parity-bit error bound. It preserves coherence within each parity sector to the stated error for arbitrary data-memory-reference inputs.

When \(d\le1\), the heralded failure probability is at most \(d-d^2/2\). Indeed the success effect is \((I+W_{\rm signal}^\dagger W_{\rm signal})/2\), and the smallest singular value of W_signal is at least 1-d. A full flagged-instrument half-diamond bound is

\[
{d\over\sqrt2}+{d-d^2/2\over2}.
\]

To see this, stack K_+ and K_- coherently. Its difference from the ideal stacked isometry has norm at most d/sqrt(2). The accepted completely positive maps differ in half-diamond norm by at most that amount; the failure CP map adds at most half its maximum probability. Recording/dephasing the pointer cannot increase the distance.

These statements assume a supplied single probe. A source vacuum component adds its actual heralded failure process. A detector's wrong-bit or false-accept contribution is separate. Normalizing an arbitrarily improbable individual outcome is not a uniform operation and is not licensed by the unnormalized branch bound.

At finite N, a lost photon may have flipped a data atom. An error flag is not a harmless retry instruction on an unknown live state.

## 6. A stronger useful task: a Bell-resource factory

Use the established two-node quantum-interrogation entanglement protocol [1], with phi=pi/2, no bypass reference, and a photon initially in the safe rail. Prepare the two computational inputs in \(|++\rangle\), and accept only a final safe-rail photon. These are real logical input preparations; they are not supplied by the medium.

The exact accepted blocks are

\[
F_{00}=-V_2V_1,\qquad F_{01}=v_2V_1,
\]
\[
F_{10}=-V_2w_1,\qquad F_{11}=u_2u_1+v_2w_1.
\]

The ideal successful output is

\[
|\Phi_-\rangle={-|00\rangle+|11\rangle\over\sqrt2},
\]

with probability one half. The sign is fixed and may be recorded as a frame; no correction pulse is hidden here.

For equal node bounds define

\[
d_B=2D+\alpha\beta,\quad
s_*={1+(1-d_B)_+^2\over4},\quad
b_*={\alpha^2+\beta^2\over4}+{d_B^2\over8}.
\]

Let S be the success effect on M, and B the joint effect for success with a bad Bell projection. Then

\[
S\ge s_* I,\qquad B\le b_* I\le {b_*\over s_*}S.
\]

Thus the worst conditional Bell infidelity is at most \(e=b_*/s_*\), uniformly for every memory/reference state. The ratio is a statement about conditional infidelity, not a diamond error.

**Proof.** The accepted preparation map is \(J=\frac12\sum_{xy}|xy\rangle F_{xy}\). Therefore \(S=\frac14\sum F_{xy}^\dagger F_{xy}\). Its Bell component is \(T=(-F_{00}+F_{11})/(2\sqrt2)\). An exact noncommuting identity gives

\[
B=S-T^\dagger T
={F_{01}^\dagger F_{01}+F_{10}^\dagger F_{10}\over4}
+{(F_{00}+F_{11})^\dagger(F_{00}+F_{11})\over8}.
\]

The block bounds give the stated b_*. F_00 is unitary, and the smallest singular value of F_11 is at least \((1-d_B)_+\), giving s_*. Positivity makes these inequalities valid with an arbitrary reference. QED.

The leading infidelity is O(1/N^2), whereas the coherent joint error is O(1/N). Small Bell infidelity also implies closeness to a Bell pair decoupled from some memory state on a square-root error scale; it does not promote the diamond error to O(1/N^2).

For \(\phi=\pi/2\), the leading uniform coefficient is

\[
C_B(r)={\phi^2(1+r^2)\over2(1-r)^2}
+{\phi^4(1+r)^2\over4(1-r)^2}.
\]

The actual scalar case \(A_j=rI, V_j=I\) attains this leading coefficient. It is a physically allowed endpoint-gain example. Thus the leading bound is sharp for this unfiltered architecture, not a general lower bound on all possible control protocols.

## 7. Finite drain renewal and its correct exposure bound

A drain need not perform a fine-calibrated pi/2 swap. Give it m fresh collisions, each with residual auxiliary amplitude at most r_d. The remaining auxiliary map R has norm at most \(r_d^m\). Stack all emitted-mode amplitudes into E. Unitarity implies \(E^\dagger E=I-R^\dagger R\).

Define the comparison isometry \(\widetilde E=E(I-R^\dagger R)^{-1/2}\), which completely empties e. This is a proof construction, not an extra operation to implement. The physical and comparison drain isometries differ by at most

\[
\left\|\binom{R}{E}-\binom{0}{\widetilde E}\right\|
\le\sqrt2\,r_d^m.
\]

Indeed their squared difference is \(2I-2\sqrt{I-R^\dagger R}\le2R^\dagger R\). The difference acts only on input in e; on idle levels both drains give the same free V.

For a node starting in the safe rail, the ideal-prefix risky amplitude before each tap is at most \(s/(1-r c)\). For a possibly risky input there is an additional transient bounded by \(c q^{j-1}\). The second node of the Bell factory can have such an input. It must be counted.

Telescoping actual suffixes against ideal prefixes therefore gives the two-node Bell-factory isometry error

\[
\delta_d\le\sqrt2 r_d^m
\left({2Ns\over1-q}+{c(1-q^N)\over1-q}\right).
\]

The bracket stays bounded as N grows at fixed r<1. Counting a full-size reset error on every cycle loses the excitation-support information. Conversely, dropping the second-node transient is incorrect.

For a total additional isometry error delta (finite dump, optical rotation, input/model errors with an actual joint-isometry qualification), the factory satisfies

\[
p_*=(\sqrt{s_*}-\delta)_+^2,\qquad
e_*\le\min\left(1,{(\sqrt{b_*}+\delta)^2\over p_*}\right).
\]

Take m=O(log(1/epsilon)) if the drain contribution needs to shrink with a requested precision. A fixed m gives a fixed residual budget. Idle-state phase errors are not excitation-supported and cannot be put into delta_d.

Fresh drain modes are essential. Two complete coherent swaps with the same retained drain return the excitation with probability one. A drain that can re-enter the port is not an irreversible absorber.

## 8. Reuse with arbitrary correlated memory histories

The following lemma is independent of the Zeno implementation. Let each attempt, for every allowed preceding history and every state of M/reference, have effects

\[
S_h\ge p_*I,\qquad B_h\le e_*S_h.
\]

All failed outcomes may act arbitrarily on M. After failure, fresh computational inputs are genuinely reset/prepared. The next attempt must obey the same operator qualifications, not merely the same averaged experimental fit.

Then the probability of no success in k attempts is at most \((1-p_*)^k\), and the expected attempt count for repeat-until-first-success is at most \(1/p_*\). To prove the quality claim, pull \(B_h\le e_*S_h\) backwards through each completely positive failure-prefix map and sum over all possible first-success times. The returned pair has infidelity at most e_*. No independence of the memory states or success events is used.

There is also a finite-program statement. Cap each production at k attempts. On exhaustion, return an explicit erasure flag. This is a trace-preserving output channel when the erasure branch is included. Counting either a bad Bell projection or erasure as a defect gives

\[
\Pr(\text{defect})\le e_*+(1-p_*)^k.
\]

If earlier outputs are held untouched, apply their Bell-defect projectors before subsequent factory operations. The uniform bound holds for the resulting subnormalized, possibly correlated memory state. Induction yields, for every subset A of production locations,

\[
\Pr(\text{defects at every location in }A)
\le \left[e_*+(1-p_*)^k\right]^{|A|}.
\]

This is a joint probability bound for the corresponding projectors and flags. It is not an independent-output assertion and not yet a complete circuit-level fault model. A supplied bilateral Pauli twirl can turn Bell coherences into a classical Bell-error description, but its random bits and logical operations are additional resources.

Conditioning later on a selected entire record can bias earlier errors. The above trace-preserving/capped statements do not authorize arbitrary such postselection. Holding earlier pairs, moving them to storage, and supplying fresh addressable data atoms are also real interface requirements. In the ideal model, a disconnected stored qubit is protected by the common idle Hamiltonian; a real device needs a bound on departures from that model over its entire storage time.

## 9. A finite resource example, with the controller exposed

Use the qualified gain box [1,2] and a 5% tap-time window about pi/3. Use the conservative r=r_d=0.6 and m=20 drain collisions after every tap. The table includes finite-drain error. It initially assumes exact qualified optical rotations, ideal |++> preparation and holding, and no false accepts.

For illustration only, include a finite one-pulse photon source with emission probability at least 0.64, a state-independent detector efficiency 0.9, and balanced, memory-independent transmission 0.999 per complete Zeno cycle. The balanced-loss assumption is stronger than merely knowing an average optical loss.

| N per node | Conditional Bell infidelity upper bound | Tap/drain success lower bound | Mean source attempts upper bound |
|---:|---:|---:|---:|
| 32 | 0.0440420 | 0.3722645 | 4.9721 |
| 64 | 0.0098605 | 0.4291261 | 4.5985 |
| 128 | 0.0023507 | 0.4624699 | 4.8499 |
| 256 | 0.0005873 | 0.4804210 | 6.0316 |

For N=64, one attempt has 128 tap windows, 2,560 fresh drain windows, and one source window: 2,689 interaction windows. If all have the same upper duration 1.05 pi/3 in inverse-g_min units, their total is at most 2,956.71 such time units per attempt. Optical rotations, routing, propagation and drain escape, data/source preparation, detector integration, and storage add their own durations. The mean numbers in the table do not erase these operations. Two computational preparations are paid per attempted pair.

On the one-excitation subspace each exchange is bounded in norm by g_max. For a prescribed scalar envelope that rises from zero to one and returns to zero, its switching-work contribution obeys \(|W|\le g_{\max}\int|\dot u|dt=2g_{\max}\). This is only a model bound on that switching contribution, not an accounting of photon energy, refrigeration, preparation, amplification, or record erasure. Those source operations remain physical resources.

Allow instead a total optical-rotation isometry budget 0.02 across the two nodes. At N=64 the stated bound becomes infidelity at most 0.0179344, tap/drain success at least 0.4033230, and mean source attempts at most 4.8927 under the same source/loss assumptions. This illustrates a finite coarse-quality resource, not a threshold claim.

Including those source and detector factors, the per-attempt success lower bound is about 0.2043892. A cap of 61 attempts gives erasure probability below 8.77e-7 in this example. It costs at most 164,029 interaction windows per requested output, plus the preparations, rotations, propagation, readout, and holding already specified. The finite-program defect bound from Section 8 then includes both the Bell-error contribution and this erasure contribution.

Ordinary optical calibration can supply such a controller qualification, but it is not free. For a constant coupler angle theta, switch the tap off and pass a probe through N/2 copies. With alpha=N theta, the measured probability is \(p=\sin^2(\alpha/2)\). On a separately qualified monotone branch \(\alpha\in[\pi/4,3\pi/4]\), \(|dp/d\alpha|\ge1/(2\sqrt2)\). Hoeffding gives a sufficient detected-probe count

\[
M\ge {4\log(2/\zeta)\over\eta^2}
\]

for total-angle error eta per node with failure probability zeta. Eta=0.01 and zeta=0.01 give 211,933 detected probes. At N=64 each uses 32 coupler passes, totaling 6,781,856 detected-probe passes. Under the illustrative source/detector/loss assumptions the mean number of prepared source attempts is about 379,910. This count assumes unbiased qualified preparation/readout, identical surviving-path attenuation, and controller stability through reuse; SPAM bias needs a separate budget.

This is a deliberately ordinary sufficient method, not a calibration lower bound. Corrected robust phase estimation [8] is a serious alternative on the meter-only controller, where coherent repetitions are physically separated from the medium. Its longest surviving probes, optical loss, branch qualification, and 2021 correction must be included. Fine calibration of G or H_M is absent; precision and stability of the clean optical controller remain.

A source with at most one photon can have a vacuum component without spoiling conditional quality, because it cannot falsely herald. Multiple photons and dark counts are different: a false-accept probability f can contribute as much as f divided by the guaranteed genuine-accept probability to conditional error. A detector filter correlated with memory is not automatically a scalar efficiency. Nor can asymmetric path loss be silently used as the balanced scalar factor in this table.

## 10. The remaining cost obstruction is genuine

For fixed balanced cycle transmission eta<1, the two-node genuine-success probability carries \(\eta^{2N}\). In the allowed scalar endpoint example, Bell infidelity is \(C_B(r)/N^2+o(N^{-2})\). Thus this unfiltered direct factory requires \(N=\Omega(\epsilon^{-1/2})\) in the worst case, and its expected interrogations grow at least as

\[
\Omega\!\left(\epsilon^{-1/2}\exp[c\epsilon^{-1/2}]\right)
\]

for fixed nonzero loss per cycle and a positive constant c. This is an obstruction for this architecture and loss model, not a lower bound for all quantum control. Finite drain accuracy and optical precision also cannot be held fixed while claiming arbitrary logical accuracy.

The justified capability is a finite-quality, state-uniform source whose failures and reuse are controlled. Better final accuracy should use a separately supplied, qualified purification or error-correcting layer, or a better native interaction. That layer is not constructed or paid for by simply invoking its name.

Known scalar attenuation can sometimes be corrected by ordinary filtering. For example, equalizing an even-sector pair with amplitudes V and W by fixed scalar weights requires \(aV=bW\). This cannot hold nontrivially for both \(W=w_1V\) and \(W=w_2V\) with distinct unknown w values. A uniform unknown operator W is a stronger obstruction. This observation does not exclude more elaborate coherent or encoded protocols; it explains why a calibrated scalar filter cannot be imported unchanged into the present all-history model.

## 11. Failed shortcuts and the earlier distinctions retained

1. **A singular-value gap is insufficient.** Let G=X_M and H_M=Omega Z_M. Every singular value of G is one, but the tap transfer probability is at most \(1/(1+\Omega^2)\). A fast common bath can make the node transparent. Sign-definite order, or another actual uniform-opacity mechanism, is the relevant resource.

2. **An auxiliary Hamiltonian gap is not a full adiabatic theorem.** Take \(H_M=\operatorname{diag}(0,1.5)\), \(G=\begin{pmatrix}2&1\\1&2\end{pmatrix}>0\). Then H_M and H_M+G share eigenvalue 1.5, with nonzero overlap between the relevant memory eigenvectors. Positivity of G does not separate all dark and bright bath bands. This invalidates a shortcut based only on the local gap; it does not refute established adiabatic protocols under their additional hypotheses [6].

3. **A retained drain is not a renewed meter.** A second complete swap returns the first emitted excitation. The outgoing boundary condition is essential.

4. **Correct parity can coexist with destroyed sector coherence.** An unrecorded memory tag distinguishing 00 from 11 preserves the parity bit and destroys a Bell state. The force-bank counterexample with a positive coefficient depending on logical Z_1 remains valid. The full K_± bounds above address this missing quantum condition; a bit-error measurement alone does not.

5. **State-averaged calibration does not certify an all-state coupling gap.** With H_M commuting with the test state, G=diag(1,0) and G=I are indistinguishable in experiments confined to memory state |0>. They differ completely on |1>. A finite tested family cannot certify an untouched sector by naming a coarse box. Geometry, symmetry, or a genuine operator qualification must supply it.

6. **Quiet-branch errors can accumulate.** Active absorption errors may be folded into r, but a bath-dependent potential on logical levels during idle or dark traversal grows with interrogation and holding time. The earlier local-orbit estimates may bound a specified local residual where their hypotheses apply. They do not turn a sampled bath state into a uniform promise.

7. **Scalar effects alone do not make coherent access.** The earlier scalar-effect examples and full Kraus/Gram distinction are unchanged. This construction obtains its optical path coherence from an explicitly supplied optical controller and source, not from a classical outcome probability identity.

## 12. Comparison to strong existing constructions

Quantum interrogation and entangling separate objects with a photon are established [1]. Azuma's imperfect-absorber analysis [2] already gives the scalar leading Zeno loss coefficient \(\pi^2(1+\sqrt\eta)/(4N(1-\sqrt\eta))\) for the quarter-turn circuit. Here r plays the role of scalar survival amplitude, and the safe-block probability reproduces that coefficient. The circuit's pulse-count reduction is not the new claim.

General contraction-based Zeno convergence is also established [4]. The contribution developed here is the combination of a concrete local positive-exchange opacity guarantee, explicit complete operator blocks for arbitrary changing retained-memory histories, finite drain renewal, and the heralded-resource composition law. These are working results, not a claim to have superseded that literature.

Duan, Wang and Kimble's cavity-scattering gates [5] are a particularly strong ordinary comparator: they already address uncertain coupling and herald photon loss, including time-varying coupling examples beyond a frozen-atom model. Their resonant cavity response, mode shape, cooperativity, selection rules, and collection are legitimate resources. The present certificate treats an arbitrary quantum operator G and common H_M without a small commutator, but pays many visits and fresh drains. No speed or physical advantage over their architecture has been established.

Leung and Ralph [3] use offline optical distillation to obtain unit conditional fusion fidelity in their modeled Zeno architecture at nonunit success probability. That controller must receive the scalar information, filters, and offline operations their construction actually uses. It would be unfair to compare it only to an uncorrected optical circuit. Their specified absorption model is also not a free all-history operator equality in the present setting.

Higher-order multi-product Zeno methods [9] improve expectation-value estimates through postprocessing under their hypotheses. They do not automatically implement a coherent physical gate or a positive accepted instrument for an arbitrary changing sequence of contractions. If a physical implementation supplies that extra capability, it is a different comparator and should be charged accordingly.

The old 25- and 72-segment controllers are not matched comparators for this source architecture. They have different handles, information, bath promises, preparation requirements, and numerical qualification. Their counts establish no advantage here.

## 13. Executable checks and their limits

Run `python p2_interface/run_checks.py` from the containing workspace. The implementation uses Python's standard library, numpy and scipy. The exact noncommutative certificate uses rational word polynomials and needs no symbolic-algebra package.

The checks verify the four accepted Bell blocks and the positive bad-effect identity exactly. They also check 120 two-node cases with arbitrary varying matrix contractions, 30 positive-coupling cases through bath norm 1,000, the indefinite-coupling and coherent-drain-return witnesses, and the scalar asymptotic coefficient. A full one-excitation simulation retains every finite drain mode and every initial-memory amplitude; it tests the finite-renewal bound without replacing the bath by sampled classical states.

The physical-opacity checks had maximum bound excess 3.34e-16, attributable to ordinary floating-point arithmetic, with a sampled commutator norm as high as 737.95. The finite-drain simulation had full-isometry error 0.0001156 below its deliberately conservative 0.18173 bound; its unitarity defect was about 6e-14. These are consistency checks, not interval-certified numerical proofs. Uniform conclusions come from the analytic inequalities.

Files: `finite_ports.py` supplies exact finite-matrix propagation and the bounds; `finite_dump_check.py` retains the fresh outgoing modes; `run_checks.py` reproduces the symbolic checks, witnesses, and resource tables; `results.json` records the finite numerical output.

## Primary references

1. A. Gilchrist, A. G. White, W. J. Munro, *Entanglement creation using quantum interrogation*, Phys. Rev. A 66, 012106 (2002). https://arxiv.org/abs/quant-ph/0112101
2. H. Azuma, *Interaction-free measurement with an imperfect absorber*, Phys. Rev. A 74, 054301 (2006). https://arxiv.org/abs/quant-ph/0608066
3. P. M. Leung, T. C. Ralph, *Improving the fidelity of optical Zeno gates via distillation*, Phys. Rev. A 74, 062325 (2006). https://doi.org/10.1103/PhysRevA.74.062325
4. T. Moebus, C. Rouze, *Optimal convergence rate in the quantum Zeno effect for open quantum systems in infinite dimensions*. https://arxiv.org/abs/2111.13911
5. L.-M. Duan, B. Wang, H. J. Kimble, *Robust quantum gates on neutral atoms with cavity-assisted photon scattering*, Phys. Rev. A 72, 032333 (2005). https://arxiv.org/abs/quant-ph/0505054
6. L.-M. Duan, A. Kuzmich, H. J. Kimble, *Cavity QED and quantum-information processing with hot trapped atoms*, Phys. Rev. A 67, 032305 (2003). https://arxiv.org/abs/quant-ph/0208051
7. J. McKeever et al., *State-insensitive cooling and trapping of single atoms in an optical cavity*, Phys. Rev. Lett. 90, 133602 (2003). https://doi.org/10.1103/PhysRevLett.90.133602
8. S. Kimmel, G. H. Low, T. J. Yoder, *Robust calibration of a universal single-qubit gate set via robust phase estimation*, Phys. Rev. A 92, 062315 (2015), corrected arXiv v3; erratum Phys. Rev. A 104, 069901 (2021). https://arxiv.org/abs/1502.02677 and https://doi.org/10.1103/PhysRevA.104.069901
9. T. Moebus, *Multi-product Zeno effect achieving higher order convergence rates*, Quantum 10, 2148 (2026). https://arxiv.org/abs/2410.16260
