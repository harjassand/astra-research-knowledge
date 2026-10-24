# Static thermal passband versus a finite gated bosonic swap

Bounded model comparison, 24 October 2026. The calculations below establish an
ideal-model distinction, not an acquired interface or a device advantage.

## 1. Define the signal and the static heat floor

Take one matched bosonic transmission channel with power transmission
\(\mathcal T(f)\), and define the required band
\(B=[5.9,6.1]\,\mathrm{GHz}\). A static passband guarantee must specify a
threshold: assume \(\mathcal T(f)\ge\tau_{\min}\) for every \(f\in B\). If the
signal is a wavepacket, define its spectral mode by a normalized envelope
\(F\), \(\int |F(f)|^2df=1\), and input
\(A_F^\dagger|0\rangle=\int F(f)a_{L,\mathrm{in}}^\dagger(f)|0\rangle\).
Exact spectral support in \(B\) is an infinite-duration idealization. For a
finite pulse, use \(\int_B|F|^2df\ge1-\epsilon\); the bandpass guarantee then
implies at least \((1-\epsilon)\tau_{\min}\) total transmitted signal energy.
It says nothing about the part of the spectrum outside \(B\).

For thermal reservoirs at \(T_h>T_c\), the one-channel Landauer current and
small-bias conductance are
\[
 \dot Q=\int_0^\infty df\,h f\,\mathcal T(f)[n(f,T_h)-n(f,T_c)],\qquad
 G=\int_0^\infty df\,h f\,\mathcal T(f)\partial_Tn(f,T),
 \quad n=(e^{hf/k_BT}-1)^{-1}.
\]
Thus the static passband alone enforces
\[
 G\ge \tau_{\min}{k_B^2T\over h}
 \int_{hf_1/k_BT}^{hf_2/k_BT}{x^2e^x\over(e^x-1)^2}\,dx.
\]
At \(T=100\,\mathrm{mK}\), for \(\tau_{\min}=1\), this is
\(1.4434599\times10^{-15}\,\mathrm{W/K}\) per channel, or 1.52516% of the
single-channel quantum \(\pi k_B^2T/(6\hbar)=9.46431\times10^{-14}\,\mathrm{W/K}\).
For a 105mK/95mK reservoir pair the band current is
\(1.44232\times10^{-17}\,\mathrm W\). A different transmission threshold scales
the guaranteed bound by \(\tau_{\min}\). Equal-temperature reservoirs have
zero *net* current; the quoted floor is a conductance (or a hot-to-cold current
under a temperature bias), not spontaneous net heat at equilibrium.

The power-passband condition is not a coherent-mode fidelity condition. It
bounds energy transmission for an input spectrum in the band. For a one-photon
mode the transmitted spectral amplitude is \(S_{21}(f)F(f)\); phase/group-delay
dispersion can make its overlap with a chosen output mode small even when
\(|S_{21}|^2=1\) throughout the band. A known phase filter may be compensated,
but that is an additional operation. Loss and a thermal environment also turn
the port into a noisy channel; \(\mathcal T\) alone does not specify its added
noise or reference entanglement fidelity. The passband constraint is therefore
a valid idle-heat floor for a continuously connected static channel, not a
claim about every packet's fidelity or the cost of a switched channel.

## 2. Exact finite-time gated swap model

Consider two actual resonant modes \(a,b\), an arbitrary signal-reference state
\(\rho_{aR}\), and an initially independent thermal state \(\tau_b(\bar n_b)\):
\[
 H(t)=\hbar\omega(a^\dagger a+b^\dagger b)
       +\hbar g(t)(a^\dagger b+ab^\dagger),\qquad g(t)\in\mathbb R.
\]
Here the Hermitian beam-splitter term is \(a^\dagger b+ab^\dagger\); if the prompt intended \(ab\) literally, that term is not Hermitian and is not a beam-splitter Hamiltonian. This is explicitly the number-conserving rotating-wave model; it assumes resonance, a prescribed classical control, and negligible counter-rotating terms. In the interaction picture, \([H_0,H_I(t)]=0\), so
\[
 U_I(T)=e^{-i\Theta(a^\dagger b+ab^\dagger)},\qquad \Theta=\int_0^Tg(t)dt,
\]
\[
 U_I^\dagger aU_I=a\cos\Theta-i b\sin\Theta,\qquad
 U_I^\dagger bU_I=b\cos\Theta-i a\sin\Theta.
\]
At \(\Theta=\pi/2\), this is a mode swap up to known local phases. After
correcting the phase, the output \(bR\) state is exactly the input \(aR\)
state: the thermal state initially in \(b\) is moved to \(a\), so it adds no
noise to the ideal full-swap output. At incomplete angle, output \(b\) contains
signal power fraction \(\sin^2\Theta\) and thermal contamination
\(\bar n_b\cos^2\Theta\). The ideal full swap thus gives unit channel fidelity
for arbitrary input/reference states in the stipulated two-mode model.

A finite smooth pulse is, for example,
\(g(t)=g_{\max}\sin^2(\pi t/T)\) on \([0,T]\), zero outside. It has
\(\Theta=g_{\max}T/2\), so choose \(T=\pi/g_{\max}\). The speed limit for any
pulse with \(|g(t)|\le g_{\max}\) is \(T\ge\pi/(2g_{\max})\). For
\(\omega/(2\pi)=6\,\mathrm{GHz}\), \(g_{\max}/(2\pi)=10\,\mathrm{MHz}\) gives
this smooth full-swap time \(T=50\,\mathrm{ns}\), with \(g_{\max}/\omega=1/600\).
A 200MHz static passband does not follow from this oscillator swap: the input
must first be captured into a suitable mode, and loading bandwidth, finite
pulse matching, and control timing remain separate costs.

In the closed prescribed-control model the instantaneous control power is
\(\hbar\dot g(t)\langle a^\dagger b+ab^\dagger\rangle_t\). Its net work over a pulse
with \(g(0)=g(T)=0\) is exactly zero for every finite-energy initial state:
\(W=\Delta\langle H\rangle=0\), since total occupation is conserved and the
initial/final Hamiltonian is \(H_0\). This means that ideal interaction energy
can be returned to an ideal control source; it does not account for the source,
its switching losses, noise, latency, or energy needed to establish and stabilize
\(g(t)\). Those are absent from the Hamiltonian, not proven free.

For a concrete finite-noise ledger, couple both modes symmetrically to Markov
thermal baths of occupation \(n_T\) and energy-decay rate \(\kappa\) during the
pulse. At full swap, the signal transmissivity is
\(\eta=e^{-\kappa T}\), and the output has thermal added occupation
\((1-\eta)n_T\). In the zero-temperature single-photon example, ideal-mode
fidelity is \(\eta\); at nonzero temperature it is state-dependent and further
reduced by thermal noise. With the 50ns example, \(\kappa T\) is the explicit
loss parameter; no lossless-fidelity conclusion survives without bounding it.

## 3. Discriminator

A permanently open static link required to pass this band has the above idle
conductance lower bound. A pulse-gated link can have zero inter-mode thermal
conduction while its coupling is off, but only for known/captured events and
only in the ideal isolation limit. The Hamiltonian proves a finite coherent
swap under an externally prescribed switch; it does not show that its switch
beats an ordinary switched heat valve, because both may be assigned the same
perfect switch for free. A meaningful comparison must include switch leakage,
control work and noise, capture/release, bath coupling during the gate, and the
same signal/fidelity requirement. No advantage claim is made without that
matched hardware ledger.
