# Low-work and passive multipliers: a competing physical construction and its obstruction

Date: 28 October 2026. New exploratory derivations by the successor physical-mechanism agent. This document does not alter any accepted P2 theorem. Its exact statements, numerical diagnostics, and unconstructed interfaces are separated below.

## Scientific decision

Lowering the conversion pump below the source frequency removes the **first-order on-shell vacuum-to-source seed** which made the 5/7/16 GHz multiplier dangerous. A smooth positive envelope then gives a very small, full-spectrum **first Dyson coefficient** without any notch. This is a real alternative worth keeping, but it does not currently justify changing the selected architecture: unobserved soft photons reopen lower-order false-count channels, and the low output frequency creates a quantitatively serious thermal/reset obligation.

A passive source-to-three-photon converter has exact stationary-ground darkness at zero temperature and is already demonstrated physical prior art at its experimental scope. Its relevant unresolved bridge is a *switched, stored-source measurement instrument* with quiet loading/unloading, rather than invention of spontaneous tripling itself. The new full-channel computational instrument being developed by the root is directly useful for deciding between this route and the high-frequency notched route.

## 1. Change the work budget, not merely the detector filter

Consider the explicitly different Hamiltonian

\[
H(t)/\hbar=2\pi f_aN_a+H_B/\hbar+
A e(t)\cos(2\pi f_pt)\sin(\sqrt{x_a}q_a)\sin\Phi,
\]

where the bath has only positive frequencies, finite vacuum phase variance, and initially is in its stationary free vacuum. Here \(q_a=a+a^\dagger\), \(e\) is a real envelope, and \(A\) is in inverse ns. This is a declared model, not an inherited physical-bath certificate.

The source-one-to-bath-three resonance is possible both when

\[
f_a+f_p\simeq3f_b\quad\hbox{and}\quad f_a-f_p\simeq3f_b.
\]

The first case absorbs pump energy; the second returns energy to the classical drive. For example:

| Candidate | Source | Pump | Nominal three-photon output | First-order source-plus-positive-bath seed |
|---|---:|---:|---:|---|
| Previous active design | 5 GHz | 16 GHz | 7 GHz | On-shell at 11 GHz |
| Low pump, energy added | 5 GHz | 1 GHz | 2 GHz | No on-shell channel |
| Low pump, energy removed | 5 GHz | 0.5 GHz | 1.5 GHz | No on-shell channel |
| Passive tripler | 5 GHz | 0 | 5/3 GHz | No stationary vacuum emission |

The lack of a first-order channel follows because every nonzero matrix element of \(\sin(\sqrt{x_a}q_a)\) from the source vacuum has odd source occupation, hence energy at least \(hf_a\). Every emitted bath photon has positive energy. A single pump quantum below \(hf_a\) cannot supply the required energy. This uses the complete positive-frequency bath, not a local loss model.

This is a long-time energy-support assertion. A finite pulse has nonzero Fourier tails, and repeated interactions can absorb several pump quanta. Neither has been discarded.

## 2. A finite-pulse full-spectrum first-vertex bound

The absence of an on-shell first-order seed admits an elementary bound that does not depend on a selected single-photon weak channel.

Let

\[
e(t)=\sin^{2p}(\pi t/T),\quad 0\le t\le T,
\]

with zero envelope outside that interval, and define \(\widehat e(\nu)=\int_0^T e(t)e^{2\pi i\nu t}dt\). Integration by parts, or the finite Fourier expansion of \(\sin^{2p}\), gives for \(|\nu|T>p\)

\[
|\widehat e(\nu)|\le
\frac{(2p)!}{2^{2p}\pi|\nu|\prod_{j=1}^{p}[(\nu T)^2-j^2]}.
\tag{1}
\]

One derivation sets \(u=\pi t/T\), \(\mu=2\nu T\), and iterates

\[
I_p(\mu)=-\frac{2p(2p-1)}{\mu^2-4p^2}I_{p-1}(\mu),\qquad
I_0(\mu)=\frac{e^{i\pi\mu}-1}{i\mu}.
\]

The bound is monotone decreasing above \(p/T\). Put \(\Delta=f_a-f_p>p/T\). The first Dyson vector from complete vacuum is

\[
\psi_1=-\frac{iA}{2}\left[
\widehat e(H_0/(2\pi\hbar)+f_p)+
\widehat e(H_0/(2\pi\hbar)-f_p)
\right]W\Omega,
\]

where \(W=\sin(\sqrt{x_a}q_a)\sin\Phi\). The spectral support of \(W\Omega\) has total frequency at least \(f_a\). If \(v=\langle\Phi^2\rangle\),

\[
\|W\Omega\|^2=
\frac{(1-e^{-2x_a})(1-e^{-2v})}{4}\le\frac14.
\]

Consequently,

\[
\boxed{\|\psi_1\|^2\le
\frac{A^2}{4}
\left[
\frac{(2p)!}{2^{2p}\pi\Delta\prod_{j=1}^{p}[(\Delta T)^2-j^2]}
\right]^2.}
\tag{2}
\]

This includes every source odd level and every odd bath photon multiplicity, every bath frequency, and interference between the two pump harmonics at this order. It does not assume a small phase excursion or discard an ultraviolet tail.

For \(f_a=5\) GHz, \(f_p=0.5\) GHz, \(T=7\) ns, \(p=2\), and \(A\le6\) radians/ns, exact rational arithmetic using \(\pi>314159/100000\) gives

\[
\|\psi_1\|^2<1.056\times10^{-13}.
\]

The receipt contains the exact rational upper fraction and its strict comparison to the displayed decimal. **This is the squared norm of the first Dyson vector, not a device dark-count probability, an all-orders perturbative remainder, or a numerical-solver error.** Its smallness is a useful design principle; it cannot replace the strong calculation. The permitted action can still be substantial, so the ordinary norm Dyson remainder is not automatically useful.

The amplitude and frequencies above are hypothetical delivered-control parameters. No physical passive circuit or compatible thermal state is certified by this scalar inequality.

## 3. Multi-vertex and unobserved-photon challenge

For an exactly single-frequency drive with constant envelope in the scattering limit, a term containing \(k\) interaction vertices has net pump integer \(m\), with

\[
|m|\le k,\quad m\equiv k\pmod2.
\]

Since the source sine and bath sine each flip their respective total parity at each vertex,

\[
n_a\equiv r\equiv k\pmod2,
\qquad n_af_a+\sum_{j=1}^{r} f_j=mf_p.
\tag{3}
\]

These are necessary conditions, not sufficient nonzero-amplitude claims. Interference and oscillator matrix-element zeros can remove additional terms. They are perturbation-order statements and do not assert the drive is weak enough to truncate there.

For a bath confined strictly to a detection band \([f_-,f_+]\), an odd-order process requires total energy at least \(f_a+f_-\). An even-order process can leave the source empty and emit two photons, requiring at least \(2f_-\). But the real bath is not confined to the detected band. A second undetected soft photon can carry arbitrarily little energy. Then an even-order process with a click needs only energy above \(f_-\).

For a 5 GHz source, 0.5 GHz pump, and detected band 1.36–1.64 GHz, the exact rational screen gives:

| Event class | First allowed perturbation order |
|---|---:|
| One or more detected photons, with arbitrary positive-frequency unobserved photons retained | 4 |
| All emitted photons inside the detected band, source left empty | 6 |
| A source excitation plus any positive-frequency weak seed | 11 |
| A source excitation with all emitted photons in the detected band | 13 |

For the 5/2/1 GHz option, the first line is already order 2: two pump quanta can create one photon near the lower edge of the detected band plus an unobserved low-frequency photon. Looking only for a source seed would miss this channel. Gapless bath photons can be created in pairs already at second order even in the 0.5 GHz case; those pairs alone are below the detected band but remain physical bath excitations.

The script also distinguishes strict nonzero continuum phase space from equality at a hard band edge. Its all-in-band screen does not count a set in which every photon is forced exactly onto a band endpoint.

### Higher harmonics and finite switching

The integer bound \(|m|\le k\) presupposes an exactly sinusoidal delivered coefficient. If the SQUID coefficient is \(\sin[\delta\cos(2\pi f_pt)]\), its higher odd Bessel harmonics can supply many pump quanta at one vertex. For \(\ell\ge0\), a useful coefficient bound follows directly from the Bessel series:

\[
|J_\ell(\delta)|\le
\frac{(|\delta|/2)^\ell}{\ell!}
\exp\!\left(\frac{\delta^2}{4(\ell+1)}\right).
\]

The source/bath parity relation survives odd-only harmonics, but the perturbation-order table does not. Finite switching also broadens the energy constraint; equation (2) handles the first vertex for the stated smooth sinusoidal coefficient only. Neither qualification can be silently omitted from a complete readout calculation.

### Explicit virtual-source pair channel

The two-vertex source-vacuum correlator is known exactly without a source Fock cutoff:

\[
\langle0|\sin[\sqrt{x_a}q_a(t_2)]\sin[\sqrt{x_a}q_a(t_1)]|0\rangle
=e^{-x_a}\sinh\!\left[x_ae^{-i\omega_a(t_2-t_1)}\right],\qquad t_2>t_1.
\tag{4}
\]

To derive it, insert the source number basis; the vacuum-to-odd-\(m\) matrix-element squared is \(e^{-x_a}x_a^m/m!\), whose odd exponential series sums to the right-hand side. The bath vector \(\sin\Phi(t_2)\sin\Phi(t_1)\Omega_B\) is a sum of four exact coherent packets. Equations (4) and that four-packet identity give a small, full-oscillator benchmark for the more general complete-channel solver.

In the additional quasistatic limit in which the relevant bath and drive frequencies are small compared with \(\omega_a\), virtual-source elimination produces the diagnostic effective interaction

\[
H_{\rm eff}/\hbar\simeq-\lambda(t)^2 C_a\sin^2\Phi,
\qquad C_a=\frac{e^{-x_a}}{\omega_a}\operatorname{Shi}(x_a),
\quad\operatorname{Shi}(x)=\int_0^x\frac{\sinh u}{u}\,du.
\]

For \(x_a=2\) and \(f_a=5\) GHz, \(C_a\simeq0.0107764\) ns. The coefficient \(\lambda(t)^2=A^2e(t)^2\cos^2(\omega_pt)\) contains frequency \(2f_p\), and \(\sin^2\Phi=(1-\cos2\Phi)/2\) creates even photon numbers. This makes the omitted pair channel explicit. The effective Hamiltonian is a diagnostic approximation, not an accepted channel replacement; equation (4) is the exact alternative for calculating it.

For the 0.5 GHz candidate, two pump quanta are below the detected band in the infinite-time limit. Nevertheless, finite-pulse spectral tails of the two-vertex process can emit a detected photon plus a soft photon already at second order. Thus the order-4 long-time screen cannot be read as a rigorous finite-pulse lower bound on the first nonzero order.

## 4. Thermal detector and reset calculation changes the architecture decision

Lower output frequency reduces the vacuum work budget, but substantially increases thermal occupation. The attached calculation treats an *independent ideal direct detector* of a thermal traveling field with efficiency 0.9, rectangular bandwidth 0.28 GHz, and time window 7 ns. It is a competing-noise screen, not the total noisy multiplier channel.

For the input thermal covariance on the observation window,

\[
C(t,s)=\eta\int_{f_-}^{f_+}n_T(f)e^{2\pi if(t-s)}df,
\quad n_T(f)=[e^{hf/(k_BT)}-1]^{-1},
\]

let \(\lambda_j\) be its nonnegative eigenvalues. The exact Gaussian-field photon-count generating function is

\[
G(z)=\prod_j[1+(1-z)\lambda_j]^{-1}.
\]

Thus \(P_0=\prod_j(1+\lambda_j)^{-1}\), \(P_1=P_0\sum_jr_j\), and \(P_2=P_0[(\sum_jr_j)^2+\sum_jr_j^2]/2\), where \(r_j=\lambda_j/(1+\lambda_j)\). These formulas follow by diagonalizing the Gaussian covariance into independent thermal modes, rather than assuming independent Poisson arrivals. The code uses a weighted time/frequency Gauss–Legendre Gram matrix. Orders 48 and 96 agree to the recorded floating-point differences. This is numerical convergence, not interval certification.

At an assumed effective temperature of 20 mK:

| Center frequency | At least one thermal count | At least two | At least three | Equilibrium buffer nonvacuum probability |
|---|---:|---:|---:|---:|
| 1.5 GHz | 0.0488511 | 0.00169816 | 0.000051646 | 0.0273392 |
| 5/3 GHz | 0.0328122 | 0.000763808 | 0.0000155463 | 0.0183272 |
| 2 GHz | 0.0147773 | 0.000154397 | 0.00000140959 | 0.00823598 |
| 7 GHz | \(9.11256\times10^{-8}\) | \(5.85523\times10^{-15}\) | \(3.45\times10^{-22}\) | \(5.06995\times10^{-8}\) |

The very small third-count entries are vulnerable to floating cancellation and are diagnostic only. The first-count values, which drive the decision, are well resolved. Effective temperature here is an assumption about the traveling field and reservoir, not a claim that a dilution refrigerator or an integrated device attains those occupations.

Requiring two or three detected photons suppresses thermal background but costs genuine-triplet efficiency. For independent 0.9 per-photon efficiency, probabilities of detecting at least one, two, or three of a genuine triplet are 0.999, 0.972, and 0.729. These are detector-only factors; conversion, propagation and reset add their own losses. The previous two-port measurement statistics do not transfer without recomputing the actual thresholded port instruments.

The reset objection is separate. A harmonic buffer passively equilibrated to the same thermal bath has

\[
P(N_b\ge1)=e^{-hf_b/(k_BT)}.
\]

At 1.5 GHz and 20 mK this is 2.73%. Waiting longer cannot produce a vacuum-reset error below that equilibrium value. Active cooling, measurement-based reset, a colder effective reservoir, or a different frequency is needed. The previously accepted zero-temperature preparation and reset statements do not supply any of those resources.

## 5. Passive conversion and close prior art

For a time-independent full Hamiltonian bounded below, a stationary ground state cannot emit positive energy into a vacuum output while remaining below the ground energy. Thus a passive tripler has exact zero-temperature *stationary-ground* darkness. This is not a claim about a suddenly coupled bare vacuum, nor about a bare annihilation-operator Markov master equation in an ultrastrongly dressed circuit. A real photodetector responds to emitted physical output excitations; virtual bare-mode occupations in a ground state are not outgoing photons.

Fraudet and coauthors reported spontaneous one-to-three microwave conversion without a strong classical conversion pump, using a nonlinear Josephson boundary and high-impedance resonator. The source was read at arXiv:2405.00411v1, with the journal record Phys. Rev. Lett. 134, 013804 (2025). Their full text explicitly includes the nonlinear spectrum, large intrinsic/radiative losses and a fitted few-level fluorescence model; it does not establish a low-error switched detector for P2. The basic passive mechanism is therefore prior art and must be credited.

Primary sources:

- D. Fraudet et al., *Direct detection of down-converted photons spontaneously produced at a single Josephson junction*, arXiv:2405.00411v1, full text: https://arxiv.org/html/2405.00411v1 ; published DOI: https://doi.org/10.1103/PhysRevLett.134.013804 . Read the methods and discussion of non-parametric conversion, not just the abstract.
- R. Albert et al., *Microwave Photon-Number Amplification*, Phys. Rev. X 14, 011011 (2024), https://doi.org/10.1103/PhysRevX.14.011011 . Its corrected figure version is dated 6 March 2024. This is the active voltage-biased route already cited by the predecessor; spontaneous parasitic emission is explicitly relevant to the comparison.

## 6. Preparation, storage and control delivery are the missing bridge

The candidate is not yet a compatible computing operation. A complete construction would need all of the following interfaces in the same Hamiltonian:

1. While storing and gating, prevent the stored source photon from passively down-converting. Detuning, a controllable coupling, or irreversible transport into a separate consumed-source detector changes the idle circuit and must be included.
2. During readout, bring source and three-photon dressed energies into resonance. Bare \(f_a=3f_b\) alone is insufficient once nonlinear level shifts are appreciable.
3. Prepare a physical dressed dark state or bound the radiation caused by loading and unloading. The gapless output continuum rules out importing a simple gapped adiabatic theorem automatically.
4. Include single-photon leakage at the source frequency, lower-output-frequency thermal stimulation, intrinsic losses, detector thresholds and all unobserved photons.
5. Reset or dispose of every consumed mode and bound the effect on fresh data. Lower-frequency passive reset is subject to the thermal equilibrium floor above.

One potentially useful later target is to raise a **consumed** source oscillator from 5 GHz to about 21 GHz and then passively emit three 7 GHz photons. That would retain the higher-frequency thermal advantage without the 16 GHz multiplication pump. Smooth frequency transport can preserve harmonic vacuum and occupation at endpoints in an isolated model, but coupling, finite tuning range, nonlinear loading, and reset make this an unconstructed proposal. Adding an ordinary 16 GHz driven upconverter can reintroduce the same 5+11 seed and is not an automatic repair.

## 7. Decisive next calculation

Compare the high-frequency notch and the low-work/passive route using the same physical-bath solver, keeping the source, all strong output modes, unobserved channels and detector POVM. For the low-work route the first necessary calculation is the finite-pulse source-vacuum output instrument including the two-vertex detected-plus-soft-photon spectral tails, the fourth-order on-shell channel, and finite temperature. The computation should expose channel error, strong-dynamics solver error, and physical false-count probabilities separately. A low first-vertex coefficient alone cannot select the winner.

Review correction: the predecessor wording of this paragraph singled out the fourth-order channel. The root reviewer correctly required explicit inclusion of the finite-pulse two-vertex tails already derived in section 3; the current paragraph preserves that stronger requirement.

The current evidence favors building that reusable instrument before committing to low-frequency hardware. The alternative has removed one resonant seed for an identifiable physical reason, while the thermal calculation has exposed a competing cost of the same choice.

## Reproduction and provenance

Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python energy_order_screen.py` in this directory. The JSON receipt hashes the exact source. It preserves exact rational kinematic searches, the exact rational first-vertex scalar check, thermal parameters, quadrature orders and convergence differences. No predecessor file was modified. The present document has not been independently reviewed; its derivations are available for review.
