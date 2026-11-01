# Independent audit of the damped force-loop retained-state theorem

Audited source: `phase8/physical_mechanisms/PHYSICAL_MECHANISM_AND_EXACT_PARITY.txt`.

## Verdict

The nominal two-sided-closure product-channel theorem is sound under its declared linear passive input-output model, independent fresh homogeneous thermal/vacuum input, and tracing of the gate-radiation outputs. It holds on arbitrary data–retained-apparatus–reference input operators. The nominal pair-parity CP decomposition is also sound on both parity sectors; its bad-data effect is sector-dependent and uniformly bounded, rather than a hypothesized independent coin.

I found no decisive algebraic fault in those two nominal claims. The following scope distinctions are essential:

1. Incoming-only closure is enough for reduced-data semicausality. For postselected apparatus records, the semicausality condition must apply to the **record-inclusive instrument**, not merely its outcome-summed channel.
2. The factorization is a channel statement after gate radiation is traced. A retained measurement record of that radiation requires a measurement-specific instrument proof. This is relevant even for vacuum, not only unequal-temperature ports.
3. Exact static-gain closure is robust to arbitrary initial mediator state. Pole/shape residuals are not: a tail bound on noise-added excitation alone cannot control a surviving coefficient multiplying arbitrary initial coherent amplitude.
4. The orientation-averaged gain twirl is correct with the required frame. Retaining the key retains coherent conditional errors. The gauge-only Kraus observation does not by itself prove a stochastic report-fault interface for the full future record history.

## 1. Full product-channel proof

Use a one-particle input space consisting of the old oscillator direction \(e_0\) and fresh field directions \(\mathsf F\). The free damped-oscillator dilation over the gate window is a passive unitary scattering map S on this space. Let \(e_r\) denote the retained oscillator direction in the output space. Its input preimage is

\[
 S^\dagger e_r=c e_0+w,\qquad c=e^{-\kappa T/2},\quad w\in\mathsf F.
\]

The driven conditional evolution is, up to its known geometric phase,

\[
 U_z=U_0D(\xi_z),\qquad \xi_z=\sum_j z_j\xi_j.
\]

Here \(U_0\) implements S. The two closure conditions have distinct geometric meanings:

\[
 \langle e_0,\xi_j\rangle=0 \quad\text{(incoming)},
 \qquad
 \langle e_r,S\xi_j\rangle=0 \quad\text{(outgoing)}.
\]

Incoming closure makes \(\xi_j\) a fresh-field vector. Combining both conditions gives

\[
 \langle w,\xi_j\rangle=0.
\]

Let \(\mathsf C=\operatorname{span}\{\xi_j\}\subset\mathsf F\). The controlled fresh-mode subspace C is orthogonal to the fresh-mode combination w that enters the retained oscillator. In addition, \(S\mathsf C\) lies entirely in the discarded output-field space. The free passive evolution maps the input C modes into output modes disjoint from the retained oscillator, while the input old oscillator and the complementary fresh directions determine the retained output.

A homogeneous thermal field has covariance proportional to identity in its one-particle mode space and zero anomalous covariance. Therefore it factors in every passive orthogonal mode basis. Vacuum has the same property. In particular, the fresh state factors between C and the fresh directions entering the retained output.

To see that this proves more than product-input independence, write a completely general joint input as

\[
 \rho_{DMR}=\sum_{z,z'}|z\rangle\langle z'|\otimes\rho_{zz'}^{MR}.
\]

The off-diagonal blocks \(\rho_{zz'}\) need not be positive. Controlled displacements act only on the independent C modes. After tracing their output modes they produce the scalar

\[
 c_{zz'}=e^{i(\phi_z-\phi_{z'})}
 \operatorname{tr}\!\left[D(\xi_z)\sigma_C D(\xi_{z'})^\dagger\right].
\]

Every block of the retained output is therefore

\[
 \rho_{zz'}\longmapsto c_{zz'}(\mathcal E_{\mathrm{free},M}\otimes I_R)(\rho_{zz'}).
\]

Linearity on all blocks proves

\[
 \Lambda_{DM}=\Phi_D\otimes\mathcal E_{\mathrm{free},M}
\]

as a complete channel identity, including arbitrary external references. It does not assert that correlated inputs become product states. It asserts that the channel acts independently on their two subsystems.

For a thermal field of occupation n,

\[
 c_{zz'}=e^{i(\phi_z-\phi_{z'})}
 e^{i\operatorname{Im}\langle\xi_{z'},\xi_z\rangle}
 e^{-(n+1/2)\|\xi_z-\xi_{z'}\|^2}.
\]

The second phase must be retained for a complex, nonorthogonal radiation Gram matrix. It vanishes for the real orthogonal Gram matrix used in the nominal parity construction.

### Assumptions that cannot be silently weakened

- The fresh field is independent of the old apparatus, data, and reference. A colored or recirculating bath can violate this premise across successive windows.
- Homogeneous thermal/vacuum input is sufficient for the mode factorization. For a general Gaussian bath, orthogonality of mode vectors alone is insufficient; the controlled modes and retained-input modes must also have zero cross covariance, including anomalous covariance.
- Gate-radiation outputs are traced. Arbitrary later measurement of a mixture of controlled field modes and old-memory-carrying modes can produce a conditional instrument that does not factor.
- All old apparatus couplings omitted from the scalar oscillator equation must really be absent, or included in the scattering matrix and closure constraints. A nonzero converter coupling changes the retained-input mode geometry.

Multiple unobserved Markov loss ports can be reduced to the same one-mode Lindblad equation with total damping and weighted thermal occupation. Equality of the reduced generator justifies the reduced-channel statement. It does not automatically identify any port-resolved measurement instrument.

## 2. Incoming-only closure and the semicausal distinction

If only the incoming condition holds, the displacements still act exclusively on fresh input modes. Tracing **all** apparatus output gives

\[
 \operatorname{Tr}_{M'}\Lambda(\rho_{DM})
 =\Phi_D(\operatorname{Tr}_M\rho_{DM})
\]

for every correlated input. The gate can nevertheless transfer data information into the retained oscillator. Its next use is safe at the reduced-data level if that next use has the same uniform incoming property. Data-only measurements and feedforward then compose through this equality.

For a delivered instrument \(\{\Lambda_y\}\), the sufficient condition is instead

\[
 \operatorname{Tr}_{M'}\Lambda_y(\rho_{DM})
 =\Phi_y(\operatorname{Tr}_M\rho_{DM})\quad\text{for every }y.
\]

Equivalently, include the classical y register in the channel output before asserting semicausality. The outcome-summed equality does not imply this stronger statement.

A simple counterexample illustrates the issue. Identity on an entangled D,M state is semicausal. Measuring M in Z and retaining its outcome still has the same reduced-data **summed** channel, but its conditional data state depends on the initial D–M correlations. A Bell input and an uncorrelated input with the same data marginal yield different conditional data instruments. Thus apparatus postselection is safe only after proving the record-inclusive condition, or after restricting the postselection to data-side records already covered by the reduced channel.

## 3. Complete nominal parity instrument

Let \(P_s=(I+sZ_1Z_2)/2\), with \(s=+1\) even and \(s=-1\) odd. With an ancilla in \(|+\rangle\),

\[
 U=e^{i\pi Z_A(Z_1+Z_2)/4}
\]

has raw X-ancilla Kraus operators

\[
 K_{X+}=P_-,\qquad K_{X-}=iZ_1P_+.
\]

The declared outcome frame removes the extra Z1 on X−. The global i on the even branch is irrelevant because the ideal instrument projects parity.

For real x and imaginary y trajectories with \(\int xy=0\), the two fresh radiation modes are orthogonal. The data channel is collective dephasing in \(J=Z_1+Z_2\), independent of the ancilla Z channel. Restricting the data dephasing to parity gives

\[
 p_+=\frac{1-e^{-8(2n+1)G_x}}2,\qquad p_-=0,
 \qquad p_A=\frac{1-e^{-2(2n+1)G_y}}2.
\]

An explicit full CP instrument after frames is

\[
 \mathcal I_{\hat s}(\rho)=
 \sum_{s=\pm1}\sum_{a,d=0}^1
 \mathbf1\{\hat s=s(-1)^a\}
 w_A(a)w_s(d)
 Z_1^{a\oplus d}P_s\rho P_sZ_1^{a\oplus d},
\]

where \(w_A(1)=p_A\), \(w_s(1)=p_s\), and the zero-tag weights are their complements. Tensor this instrument with the actual free retained-apparatus channel.

This formula includes both sectors, arbitrary cross-sector input coherences, the report, the data frame, and the retained apparatus. Cross-sector coherences vanish because the nominal parity instrument is projective. The ancilla tag a both flips the report and adds Z1 after the declared frame; these are two consequences of one event, not two faults.

The hidden data-bad CP map has adjoint effect

\[
 B_D^*(I)=p_+P_++p_-P_-=p_+P_+\le p_+I.
\]

The ancilla-bad effect is \(B_A^*(I)=p_AI\). Their joint effect is \(p_Ap_+P_+\), as a consequence of the derived orthogonal thermal modes. These operator inequalities hold on every current state. Because future field windows are fresh, they can be iterated over arbitrary preceding physical records and arbitrary surviving mediator states.

The resulting guarantee is unnormalized: for specified operation locations, the joint probability of their bad tags is bounded by the product of the admitted bounds. Conditioning afterward on a rare accepted output history can divide by its probability. No such normalized-postselection bound should be asserted without that denominator.

## 4. Constant gains and the key-retirement caveat

Constant gains preserve both closure equations because those equations are linear in the waveform. The phase angles are

\[
 \theta_j=\frac\pi4\operatorname{Re}(g_j^*g_A).
\]

After the outcome frame, the **untwirled** Kraus operators, ignoring bath dephasing for this algebraic observation, are

\[
 K_{X+}=\cos(\theta_1+\theta_2)P_+
       +\cos(\theta_1-\theta_2)P_-,
\]

\[
 K_{X-}=i\left[\sin(\theta_1+\theta_2)P_+
       +\sin(\theta_1-\theta_2)P_-\right].
\]

They are indeed functions of the measured gauge P. On a definite parity input, wrong-report probabilities are \(\sin^2(\delta_1\pm\delta_2)\). On a coherent superposition of sectors, the delivered instrument also contains cross-sector terms linear in the angle errors. No exact projective good/bad CP decomposition with bad weight of that quadratic order follows merely from the sector probabilities.

### A concrete future-record counterexample

Represent P as gauge Z and prepare gauge \(|+X\rangle\). Choose \(\delta_1=\delta\), \(\delta_2=0\). Then

\[
 K_{\mathrm{odd}}=-\sin\delta\,P_++\cos\delta\,P_-.
\]

Follow the parity report by a measurement of the anticommuting gauge X. The joint probability of the history (odd report, X+) is

\[
 \frac{(\cos\delta-\sin\delta)^2}{4}
 =\frac{1-\sin2\delta}{4}.
\]

A sharp-P instrument followed by classical report flips of probability \(\sin^2\delta\) gives 1/4. The difference is linear in δ. Therefore the complete delivered record history is not the ordinary sharp-measurement-plus-quadratic-report-error instrument.

This counterexample does not rule out a **receiver-specific logical quotient theorem** that permits arbitrary gauge backaction. A complete layer of commuting gauges admits a useful partial result: its joint outcome probabilities can be evaluated in the common gauge eigenbasis. For an incoming definite center-stabilizer sector, a union bound on the individual quadratic report errors bounds an incorrect stabilizer product, uniformly over gauge coherence. But that observation has not yet handled coherent superpositions of correctable syndrome sectors, correction feedback, faults between gauges, overlapping recovery, or subsequent noncommuting gauge layers. It should not replace the bounded coherent default without that proof.

### Orientation averaging

At the nominal angle, \(U_-=-P U_+\). Applying the known P frame for negative orientation makes the two calibration perturbations opposite. Averaging a true fresh unbiased orientation removes the cross-sector terms and gives the stated projective instrument with quadratic report errors.

This result requires both the correct frame and orientation-covariant physical response: the same gain parameters multiply the waveform with either sign. If hardware errors depend on the random sign, freshness of the bit alone does not imply the cancellation. Those deviations require their own noise bound.

If the delivered instrument retains the orientation key, it is a direct sum of two coherent conditional instruments, not their average. The key must be operationally retired from the permitted future consumer, or a task-specific theorem must show why its continued availability is harmless. The source report correctly recommends the bounded coherent treatment as its default.

For unequal complex data gains, the cross-sector radiation Gram matrix can have imaginary components. Within each parity sector its channel is still the stated Z1 dephasing. The nominal-angle comparison instrument kills cross-sector terms; the difference from the actual unitary can still be bounded by the finite operator \(\delta_1Z_1Z_A+\delta_2Z_2Z_A\). This is a valid route to a bounded coherent perturbation independent of initial oscillator energy. It should not be described as an untwirled exact stochastic instrument.

## 5. The initial-memory term under pole/shape errors

If a perturbation creates a nonzero incoming coefficient \(\varepsilon\), the interaction-picture propagator contains a controlled displacement \(D(\varepsilon Z)\) of the **initial** oscillator. On an initial coherent amplitude α, this creates a data phase proportional to \(\operatorname{Im}(\varepsilon\alpha^*)\). For every nonzero ε, one can choose α large enough to make that phase order one.

Consequently a bound only on fresh noise, noise-added occupation, or deviations from a reference displacement is insufficient unless the argument explicitly cancels the initial-memory coefficient. A full physical perturbation theorem must do one of the following:

- retain an exact algebraic incoming null for those perturbations;
- restrict the initial state with a physically justified global moment/tail assumption;
- use an input-sensitive error statement that openly depends on its initial energy or characteristic function.

The exact nominal and static-gain theorems do not need such an initial-state restriction. This distinction preserves their value while preventing an overclaim for arbitrary physical shape/pole errors.

## 6. Consequence for the main result

The strongest defensible claim is: an ordinary damped geometric bus can be shaped to provide a full data–retained-apparatus product-channel interface, an exact two-sector parity CP error instrument, and joint bad-tag bounds under the specified fresh thermal input model. The same construction can be given to the ordinary comparator. It is stronger than an isolated coherence or mean-energy estimate.

The complete operational theorem still depends on the actual finite preparation/readout instrument, all-interval noise admission, and the inherited receiver's extended-rectangle invariant. The code-gauge support lemma from `single_fault_support.md` remains applicable, but it does not remove those rate and receiver obligations. Keep the bounded coherent treatment of gain mismatch unless the additional receiver-specific quadratic theorem is completed.
