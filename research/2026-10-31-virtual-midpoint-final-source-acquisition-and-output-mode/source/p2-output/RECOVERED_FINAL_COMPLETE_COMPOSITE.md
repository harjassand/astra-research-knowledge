The proof, programs, numerical outputs and independent audits are intact. The strongest completed result is a **reusable sector-measurement theorem for an unprepared linear receiver driven by a positive, dynamically evolving quantum gain source**.

The work reached three connected conclusions:

1. **Exact rejection of the receiver’s initial state.** A suitable measured output mode contains none of the receiver’s initial quantum operators, including their unknown correlations with the computation.
2. **Reliability without tracking the quantum gain.** A positive operator lower bound gives a uniform readout guarantee even when the gain does not commute with the source Hamiltonian.
3. **A construction using coarse calibration.** With a finite receiver-energy bound, ordinary settling and integration suffice with only a linewidth interval. The complete duration grows logarithmically with inverse requested error and initial energy.

These are working mathematical results for the stated physical models, with ordinary proofs and executable checks. Historical priority, a complete microscopic device window and a practical advantage over the strongest conventional implementation remain unestablished.

The complete derivation is preserved in :chatgpt-content-reference{index="9"}[OUTPUT_MODE_THEOREM.md](producer-workspace/OUTPUT_MODE_THEOREM.md).

## 1. The capability and its exact assumptions

The desired operation measures an involution

\[
W=P_+-P_-,
\qquad W^2=I,
\]

while preserving the useful quantum information inside each eigenspace. The eigenspaces may be degenerate—for example, the three-dimensional triplet sector of two spins.

The retained auxiliary system consists of a quantum source \(E\) and a receiver. They may initially be arbitrarily correlated with the data and an external reference.

The central one-mode interaction is

\[
H_{\mathrm{int}}
=
\hbar W\otimes G_E(t)\otimes(a+a^\dagger),
\qquad
0<g_-I\le G_E(t)\le g_+I.
\]

The source has its own forward Hamiltonian \(H_E(t)\). In particular,

\[
[H_E(t),G_E(t)]\ne0
\]

is allowed.

The assumptions that carry the result are:

| Component | Required structure |
|---|---|
| Logical action | Every physical operation acts identically on all logical vectors inside a given \(W\) sector. |
| Receiver | A passive linear oscillator or finite stable network, with the stated output coupling. |
| Gain source | A positive bounded operator gain throughout the admitted evolution. Its internal dynamics need not be learned. |
| Incoming field | Fresh vacuum or a specified Gaussian thermal field, independent of retained systems and the actual previous record. |
| Measurement | Physical output collection and homodyne detection of the specified temporal mode. |
| Microscopic validity | The Hamiltonian, bandwidth and occupied-domain approximations must hold over the complete operation. |

This is a longitudinal-receiver resource setting. It is not a compilation of the original signed Pauli handles into a newly assumed force apparatus.

The distinction between commutation and sector protection remains essential. A Hamiltonian can commute with \(W\) and still rotate states within a degenerate sector. The required condition is stronger.

## 2. Exact removal of the receiver’s initial quantum state

For one resonant receiver,

\[
\dot a
=
-\frac{\kappa}{2}a-iWG_E-\sqrt{\kappa}\,b_{\mathrm{in}},
\qquad
b_{\mathrm{out}}=b_{\mathrm{in}}+\sqrt{\kappa}\,a.
\]

These are standard quantum input-output equations. Their unitary system-field interpretation is retained; the gain is not replaced by a classical stochastic amplitude. :chatgpt-content-reference{index="0"}

For an observation duration \(T>0\), define

\[
V=T-\frac4\kappa
\tanh\!\left(\frac{\kappa T}{4}\right)
\]

and

\[
w(t)=
\frac{
1-\dfrac{2e^{-\kappa t/2}}
{1+e^{-\kappa T/2}}
}{\sqrt V}.
\]

The weight obeys

\[
\int_0^T w(t)^2\,dt=1,
\qquad
\int_0^T w(t)e^{-\kappa t/2}\,dt=0.
\]

It is the normalized projection of a constant temporal weight away from the cavity’s initial transient.

Now use the passive receiver evolution as a mathematical interaction picture. Its selected output mode satisfies the exact operator identity

\[
B
=
\int_0^T w(t)b_{\mathrm{out,free}}(t)\,dt
=
-\int_0^T w(T-t)b_{\mathrm{in}}(t)\,dt.
\]

**There is no \(a(0)\) term.**

This removes the entire initial receiver operator—not merely its expectation value. The identity therefore covers unknown non-Gaussian receiver states and initial correlations with the data, source and reference.

The receiver itself has not been reset. Instead, the measured field mode has been chosen so that its initial noise comes entirely from the newly supplied field.

For a fresh thermal input with occupation \(n_b\), the quadrature

\[
Y=i(B^\dagger-B)
\]

has Gaussian variance

\[
v=2n_b+1.
\]

Freshness is substantive. An unconditional Gaussian marginal is insufficient if the field is correlated with the logical sector or previous record. The audit includes a counterexample in which correlating the logical sector with the pointer’s initial sign nearly doubles the naive one-tail error.

### The quantum-gain proof

The gain source can become entangled with the receiver during the interaction. Consequently, it would be wrong to infer a Gaussian distribution shifted by an independent random gain.

The proof instead follows the probability current of the selected field quadrature.

The free commutator is

\[
[a_{\mathrm{free}}(t),B^\dagger]
=
\sqrt{\kappa}\,k(t),
\]

where

\[
k(t)=
\frac{
(1-e^{-\kappa t/2})
(1-e^{-\kappa(T-t)/2})
}{
(\kappa/2)(1+e^{-\kappa T/2})\sqrt V
}
\ge0.
\]

Writing \(X=B+B^\dagger\), with \([X,Y]=2i\), the interaction in sector \(s=\pm1\) has the form

\[
H_s(t)
=
s\sqrt{\kappa}\,k(t)G_E(t)X
+
V_s(Y,t).
\]

The second term is Hermitian and local in \(Y\). It includes the source Hamiltonian and the remaining receiver modes.

In the \(Y\) representation, the first term produces transport. The local term can rotate and entangle internal components, but it does not contribute a probability current across a \(Y\) boundary. Positivity of \(G_E\) bounds that current uniformly.

The minimum directed displacement is

\[
\mu_-
=
2\sqrt{\kappa}\,g_-\int_0^T k(t)\,dt
=
4g_-\sqrt{\frac V\kappa}.
\]

Therefore,

\[
\boxed{
p_{\mathrm{wrong}}
\le
Q\!\left(
\frac{\mu_-}{\sqrt{2n_b+1}}
\right),
}
\]

where \(Q\) is the standard Gaussian upper tail.

No norm of \(H_E\), or of \([H_E,G_E]\), appears in this model theorem. Source evolution may be rapid and noncommuting.

The earlier Astra positive operator-force principle is doing real work here: the current cannot reverse while the operator lower bound remains positive. The new construction applies that principle to an emitted field mode after removing the receiver’s initial operators.

Two useful extensions follow directly:

- A common unwanted source force \(F_E\), with \(\|F_E\|\le f<g_-\), is covered by replacing the gain interval with \([g_--f,g_++f]\).
- A known nonnegative switching envelope \(u(t)\) is included inside the displacement integrals. Ramps and collection tails remain part of the physical duration.

Neither extension supplies an unqualified source or instantaneous switching.

## 3. Interacting receivers and known dispersive shifts

The cancellation extends to a finite passive linear network,

\[
\dot{\mathbf a}
=
A\mathbf a-i\ell WG_E-C^\dagger\mathbf b_{\mathrm{in}},
\qquad
A=-iK-\frac12C^\dagger C,
\]

with stable \(A\) and all loss ports included.

For an observed output row \(C_o\), the unknown initial receiver operators appear through the finite set

\[
(C_o e^{At})_j.
\]

Projecting the constant function away from the real and imaginary parts of these transients removes all initial receiver modes.

The required receiver information is its observable transient space. A microscopic reconstruction of the retained gain source is unnecessary. Existing quantum linear-system identification supplies relevant machinery for acquiring transfer information; its acquisition is still a resource. :chatgpt-content-reference{index="1"}

### The signed-kernel correction

An interacting or detuned receiver generally produces a real force-response kernel \(\beta(t)\) with both signs. Its guaranteed displacement is

\[
\mu
=
2\int_0^T
\left[
g_-\beta^+(t)-g_+\beta^-(t)
\right]dt.
\]

The adverse parts must be charged against \(g_+\). An unknown source could apply its largest allowed gain on those portions.

For every fixed finite stable receiver with a nonzero usable DC response, I proved

\[
V=T-O(1),
\qquad
\int_0^T\beta^-(t)\,dt
\le \frac{B_0}{\sqrt V}.
\]

With a suitable fixed homodyne phase and positive DC response \(\chi\),

\[
\boxed{
\mu
\ge
2g_-\chi\sqrt V
-
2(g_+-g_-)\frac{B_0}{\sqrt V}.
}
\]

Thus the useful displacement grows as \(\sqrt T\), while the negative-kernel penalty decreases as \(T^{-1/2}\). A fixed finite gain interval permits exponentially improving label accuracy.

This covers interacting *linear* receiver modes. It does not cover arbitrary nonlinear auxiliary dynamics merely because those dynamics are called a receiver.

### A necessary failure and a corrected convention

Known sector-dependent dispersive shifts give scalar poles

\[
\lambda_s=\kappa/2+i\delta_s.
\]

One real filter can cancel a finite collection of such poles. Different sector-associated free modes are proof coordinates for the same physical homodyne statistic; they do not require choosing a filter after learning the sector.

However, if \(\delta_s\ne0\), exact rejection of both initial quadratures generally prevents the response kernel from being nonnegative everywhere. The negative pieces are a structural feature, not numerical noise.

The audit also caught a conjugation error. With

\[
k_s(t)=\int_t^T w(u)e^{-\lambda_s(u-t)}\,du,
\]

the correct identity is

\[
[a_{\mathrm{free},s}(t),B_s^\dagger]
=
\sqrt{\kappa}\,k_s(t)^*.
\]

This changes the sign of a local quadrature potential. It leaves \(\operatorname{Re}k_s\), the transport bound and the probability conclusion unchanged. The correction is incorporated in the preserved proof.

A distinct unresolved case is

\[
W\otimes D_E\otimes a^\dagger a
\]

with source-dependent, noncommuting \(D_E\). This is a quantum-controlled receiver pole. Its dynamics cannot automatically be represented by a finite list of scalar poles merely by bounding \(D_E\)’s eigenvalues.

## 4. Coarse calibration with a finite energy bound

Exact cancellation has an unavoidable qualification: a small residual coefficient of \(a(0)\) is not uniformly small over unbounded initial receiver energy.

The program preserves a concrete witness. Changing the actual linewidth from \(1\) to \(1.01\), while using the \(T=8\) nominal annihilator, leaves an initial-mode coefficient of about \(-0.004085\). An arbitrarily displaced initial state can amplify it.

That is a continuity obstruction on an unbounded domain, not a device error floor.

The second construction uses a finite energy bound and avoids exact pole calibration.

Assume a resonant receiver with a static but unknown linewidth

\[
0<\kappa_-\le\kappa\le\kappa_+,
\]

and initial mean occupation at most \(E\). The source and receiver may remain correlated with the computation.

Keep the positive force on throughout \([0,t_0+L]\). Discard the output during \(t_0\), then integrate a normalized boxcar over the final interval of length \(L\).

The free measured mode is

\[
B=\zeta a(0)+B_{\mathrm{fresh}},
\]

with

\[
\zeta=
\frac{
2e^{-\kappa t_0/2}(1-e^{-\kappa L/2})
}{
\sqrt{\kappa L}
}.
\]

The response kernel remains nonnegative. A uniform lower displacement is

\[
\mu_0
=
4g_-\sqrt{\frac L{\kappa_+}}
\left[
1-\frac{2e^{-\kappa_-t_0/2}}{\kappa_-L}
\right].
\]

Any oscillator state of mean occupation at most \(E\) has quadrature second moment bounded by

\[
V_E=2E+1+2\sqrt{E(E+1)}.
\]

The old receiver quadrature and fresh-field quadrature commute. Combining their tail bounds gives, for \(0<r<\mu_0\),

\[
\boxed{
p_{\mathrm{wrong}}
\le
Q\!\left(
\frac{\mu_0-r}{\sqrt{2n_b+1}}
\right)
+
\frac{4e^{-\kappa_-t_0}}{\kappa_-L}
\frac{V_E}{r^2}.
}
\]

This bound applies to the total wrong-label probability on the joint input state. It does not assign the same energy ceiling separately to every rare normalized conditional sector.

An explicit sufficient sizing gives

\[
T=t_0+L
=
O\!\left(
\log\frac1p+\log(1+E)
\right)
\]

for fixed coarse receiver, gain and field-noise bounds.

The source continues evolving during both intervals. The receiver may remain populated by the applied force and thermal field. Purification is unnecessary.

Resonance and the correct force/homodyne quadrature remain separate control qualifications. A linewidth interval alone does not establish them.

### Feasible numerical schedules

Take a nominal rate \(\kappa_0\), with

\[
\kappa/\kappa_0\in[0.8,1.2],
\qquad
G_E/\kappa_0\in[0.3,0.5],
\qquad
E\le10,
\]

and fresh vacuum input. Durations below are in units of \(\kappa_0^{-1}\).

| Target label bound | Discarded interval \(t_0\) | Integrated interval \(L\) | Complete duration | Full-instrument bound \(p+\sqrt p\) |
|---:|---:|---:|---:|---:|
| \(10^{-3}\) | 15.27 | 11.49 | 26.76 | \(3.262\times10^{-2}\) |
| \(10^{-6}\) | 24.06 | 22.32 | 46.38 | \(1.001\times10^{-3}\) |
| \(10^{-9}\) | 32.75 | 33.45 | 66.20 | \(3.1624\times10^{-5}\) |

These are floating-point feasible witnesses evaluated against the analytic inequality. They are not certified rounding enclosures, global duration optima or hardware forecasts.

The physical operation is ordinary dissipative settling and integration. The added theorem supplies its quantum-gain and correlated-history guarantee. An equally informed conventional controller can use the same result.

## 5. The complete instrument and repeated use

The required fine-history structure is

\[
K_r
=
P_+\otimes V_{r,+}
+
P_-\otimes V_{r,-}.
\]

Every logical vector within a sector experiences the same auxiliary operator. This preserves the distinction between obtaining the correct label and preserving the quantum information that should survive that measurement.

For the full comparison, let \(V_{r,\alpha,s}\) denote the physical coarse outcome \(r\), unobserved fine history \(\alpha\), and true sector \(s\). Define an ideal comparison instrument by

\[
\mathcal I_s(\rho)
=
\sum_{r,\alpha}
(P_s\otimes V_{r,\alpha,s})
\rho
(P_s\otimes V_{r,\alpha,s})^\dagger,
\]

and report label \(s\).

This comparison is fixed, completely positive and input-independent. Summing over \(s\) is trace preserving. It retains the actual sector-conditioned auxiliary channel, including all physical histories. It requires no bath inverse, input-dependent normalization or source restoration.

Relabeling the wrong diagonal mass costs at most \(p\) in half trace norm. The cross-sector blocks contribute at most \(\sqrt p\). Therefore,

\[
\boxed{
\frac12\|\mathcal M-\mathcal I\|_\diamond
\le p+\sqrt p.
}
\]

The exact annihilator gives the uniform ideal-model statement. The coarse-calibration result gives the corresponding energy-constrained statement.

Fine records can still steer pre-existing data–source correlations. The theorem does not assert an unchanged normalized logical marginal after every fine outcome. Nor does this measurement instrument automatically become the coherent oracle needed by phase-estimation protocols.

### A real energy bound supports reuse

The bounded force gives

\[
\frac{d}{dt}\langle N\rangle
\le
-\frac{\kappa}{2}\langle N\rangle
+\kappa n_b+\frac{2g_+^2}{\kappa}.
\]

A mean-energy ceiling is therefore

\[
E_{\max}
=
\max\!\left\{
E_{\mathrm{initial}},
\,2n_b+\frac{4g_+^2}{\kappa^2}
\right\}.
\]

Departed-output measurement does not change the nonselective retained mean energy. Individual rare records can produce hotter conditional states; the ceiling is not a pathwise assertion.

Actual weighted histories still suffice. The energy-dependent tail bound is concave in \(E\), allowing the probability-weighted error to be controlled by the actual mean-energy envelope for a fixed schedule.

Composition uses actual physical prefixes and ideal completely positive suffixes. Each error estimate is evaluated on a real preceding state. The proof does not require fictitious ideal source histories to remain qualified.

Fresh input field is needed on each interval. The retained source and receiver need not be reset or become independent between measurements.

The scope is **reusable sector measurement**. A residual \(Z a^\dagger a\) interaction can be harmless during \(Z\) readout and harmful during an \(X\) rotation. Interleaving other logical operations still needs a physical switch, an earned robust gate or a complete error bound for that gate interval.

## 6. Physical interfaces, conventional methods and costs

### Existing longitudinal readout supplies meaningful hardware

Pumped Josephson longitudinal readout already supplies conditional displacement, an output port, amplification and digital weighting. Its effective Hamiltonian also contains a residual dispersive term, and the reported calibration used \(3\times10^5\) prepared-state trajectories. These are real operations and acquisition costs. :chatgpt-content-reference{index="2"}

The new filter can augment that stack. Known scalar dispersive shifts fit the finite-pole construction. Arbitrary source-dependent poles, higher levels, spectator interactions and the subsequent gate interval do not disappear.

Exchange offers a useful symmetry for a different implementation:

\[
H_{\mathrm{ex}}
=
J\,\mathbf S_1\cdot\mathbf S_2
=
\frac J2\,\mathrm{SWAP}-\frac J4.
\]

A genuinely scalar exchange modulation can distinguish singlet from triplet while preserving all triplet orientations.

Longitudinal spin–resonator coupling has been demonstrated, but the desired force and dispersive response can arise from the same exchange curvature. An \(S\)–\(T_0\) demonstration therefore does not establish a full-triplet instrument or solve the source-dependent-pole problem. :chatgpt-content-reference{index="3"}

For example,

\[
J''(\epsilon)
=
\frac{2t_c^2}{(\epsilon^2+4t_c^2)^{3/2}}>0
\]

provides a positive curvature. Making \(\epsilon\) a quantum source operator can give a positive noncommuting gain—but typically also a quantum-controlled receiver shift. That coupled microscopic calculation remains necessary.

### Ordinary methods receive the same information

For a known empty resonant receiver, the ordinary optimum matched filter has signal norm squared

\[
B(T)
=
T-\frac4\kappa(1-e^{-\kappa T/2})
+\frac1\kappa(1-e^{-\kappa T}).
\]

The exact initial-state-rejecting filter has \(V(T)\), so its amplitude-SNR ratio is

\[
\sqrt{\frac{V(T)}{B(T)}}.
\]

This tends to \(1/2\) at short times and to one at long times. Exact rejection has a real sensitivity cost.

A prepared-receiver controller can also use the positive quantum-gain guarantee. Ordinary settling can use the coarse-calibration theorem. Neither receives artificially worse information or fewer legal operations.

Established optimal QND filtering also treats relaxation as a substantive duration tradeoff. :chatgpt-content-reference{index="4"} The new benefit is a guarantee for broader initial receiver states and source dynamics; a practical speed advantage has not been established.

### Complete physical cost

The operating budget must retain source preparation and maintenance, field preparation, collection efficiency, amplification, phase stability, digitization, ramps, loading, intervening gates, holding and return.

For vacuum input in the one-port model, the mean emitted photon count is

\[
\kappa\int_0^T\langle N(t)\rangle\,dt.
\]

The energy envelope bounds this quantity. It does not determine the full pump, local-oscillator or electronic work. The discarded settling interval contributes real source work and physical exposure.

A sufficient implementation budget has the form

\[
\epsilon_{\mathrm{total}}
\le
p(T)+\sqrt{p(T)}
+\epsilon_{\mathrm{physical}}(T)
+\epsilon_{\mathrm{loading/gates/holding}}.
\]

Longer observation lowers the readout terms while potentially increasing symmetry-breaking and holding errors. This sufficient bound is not a measured floor.

Several qualifications cannot be acquired by naming them:

- A uniform \(g_->0\) needs a structural operator argument or a justified accessible domain. Finite prepared-state samples cannot exclude a dark state in an unvisited source subspace.
- A finite mean energy controls the readout tail, but does not by itself bound every correction, such as a Kerr term proportional to \(N^2\).
- The mathematical absence of \(\|H_E\|\) from the result does not validate a microscopic rotating-frame approximation at arbitrary source frequencies. The local orbit of the actually coupled operators remains relevant.
- Detector saturation, finite bandwidth and physical collection impose domains even when an ideal filter cancels an arbitrarily large initial operator exactly.

## 7. Molecular corrections preserved from the same investigation

The molecular route produced useful results and failures rather than a completed warm cycle.

The full 24-state atomic-manifold calculation retains the excited-atom label, electronic \(J=1\) and both nuclear spins. It is complete within that manifold, not the entire molecular spectrum.

For a fixed pair geometry, the response is spin scalar through its first three moments. A later moment contains a triplet tensor with

\[
\|\mathcal N_t\mathcal R(\Delta)\|
=
\frac{5A_{\mathrm{hf}}^2|J_d|}{6|\Delta|^4}
+O(|\Delta|^{-5}).
\]

The audit corrected an earlier projected calculation that predicted a spurious lower-order anisotropy. The omitted channel supplies the term

\[
PF(I-P)FP
\]

in

\[
PF^2P=(PFP)^2+PF(I-P)FP.
\]

Warm motion supplies a separate witness:

\[
\frac{A_{\mathrm{hf}}[B,K]}{\Delta^4},
\qquad
[B,K]=-\frac{3J_dk}{2}
\,\sigma_y^{\mathrm{orbital}}\otimes I_{\mathrm{tot},y}.
\]

It preserves the singlet/triplet label while disturbing information within the triplet. This witness admits two axes; it is not an unavoidable term in an exactly fixed-axis one-dimensional model. Establishing the narrower contact domain is itself a physical requirement.

Complete Franck–Condon closure also cancels the nominal useful \(1/\Delta\) amplitude:

\[
\langle f|(\Delta-H_e)^{-1}|i\rangle
=
\frac{\langle f|(H_e-H_g)|i\rangle}{\Delta^2}
+O(\Delta^{-3}).
\]

Thus isolated-level association strength cannot be combined with complete-manifold cancellation. In the fixed-vacuum-Stokes bad-cavity regime, useful absorption and some surviving spin disturbances are co-suppressed as \(\Delta^{-4}\). Detuning alone then stops improving their ratio.

Final molecular parity still provides a useful selected output channel. It does not establish transparency of every unobserved history. Effective-Hamiltonian and physical-jump calculations must remain separate, as in the standard effective-operator formalism. [arxiv.org](https://arxiv.org/abs/1112.2806?utm_source=chatgpt.com) Existing cavity-assisted association supplies real heralding and output machinery within its stated model; it does not establish the warm one-dimensional instrument by transfer from a cold calculation. [arxiv.org](https://arxiv.org/abs/1803.10004?utm_source=chatgpt.com)

The source-unit correction is also preserved: the primary \(^{171}\mathrm{Yb}\) spectroscopy value is \(-0.15(19)\,\mathrm{nm}\), not \(-0.15\) Bohr radii. [arxiv.org](https://arxiv.org/abs/0708.0752?utm_source=chatgpt.com)

None of these sufficient disturbance bounds is being promoted into a measured error floor or a universal impossibility theorem.

## 8. Preserved proof and executable record

The recovered files are:

- **Complete central derivation:** OUTPUT_MODE_THEOREM.md[OUTPUT_MODE_THEOREM.md](producer-workspace/OUTPUT_MODE_THEOREM.md).
- **Main executable and results:** output_mode_checks.py[output_mode_checks.py](producer-workspace/output_mode_checks.py) and output_mode_results.json[output_mode_results.json](producer-workspace/output_mode_results.json).
- **Independent mathematical audits:** OUTPUT_MODE_AUDIT.md[OUTPUT_MODE_AUDIT.md](producer-workspace/OUTPUT_MODE_AUDIT.md), SETTLING_EXTENSION_AUDIT.md[SETTLING_EXTENSION_AUDIT.md](producer-workspace/SETTLING_EXTENSION_AUDIT.md) and audit_output_mode.py[audit_output_mode.py](producer-workspace/audit_output_mode.py).
- **Molecular derivations and failures:** MOLECULAR_AUDIT.md[MOLECULAR_AUDIT.md](producer-workspace/MOLECULAR_AUDIT.md) and DERIVATION.md[pair-response derivation](producer-workspace/DERIVATION.md).

The principal programs run with NumPy and SciPy:

```bash
python p2_interface/output_mode_checks.py
python p2_interface/audit/audit_output_mode.py
```

They check operator cancellation, canonical field normalization, complete source-space wrong-outcome effects, signed kernels, interacting receivers, the correlated-reference CP comparison, the freshness counterexample and coarse-calibration schedules.

The source propagation checks use finite sequences of rotations and translations. The inequality applies to those sequences themselves; they are not a certified convergence study of an arbitrarily fast continuous Hamiltonian. All numerical results remain floating-point diagnostics alongside the proofs.

The governing Astra force source is pinned in the main note to commit `ceaef853be46099e0e3446d0778160f26ef962fe`, with its accessible source reference and the primary research references preserved. No unavailable original raw derivation has been presumed transferred.

**The completed scientific consequence is a separation between auxiliary preparation and the response structure needed for useful measurement.** The receiver’s old quantum state can be excluded from the observation, and a positive gain source can remain unlearned and dynamically active. The remaining physical target is a sector-preserving coupler whose source fluctuations retain that structure throughout readout, switching and reuse—especially when the same microscopic interaction also changes the receiver’s pole.