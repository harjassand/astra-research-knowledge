## ASTRA — New construction: finite-time photon capture with order-one interaction strength

The strongest continuation is a change of mechanism. Instead of making a photon acquire a conditional phase through a very large memory-dependent resonance shift, we can capture the photon, apply a small local interaction, and release it coherently.

This removes the earlier \\(201B\\)–\\(400B\\) detuning requirement from the mathematical architecture.

### 1. A certified capture point in a positive, gapless lattice

Consider the semi-infinite Jacobi Hamiltonian

\\[ h=I+\sum\_{j\ge0}g_j(|j\rangle\langle j+1|+\mathrm{h.c.}), \\]

with boundary coupling \\(g_0=0.7B\\) and all subsequent couplings \\(g_j=0.5B\\), in units where \\(B=1\\).

I independently certified an exact zero of the boundary state's survival amplitude at a time within

\\[ \boxed{2.433886050\<t\_\*<2.433886053.} \\]

The certificate uses exact rational quantum-walk moments and a bounded Taylor remainder, rather than numerical root-finding alone.

At \\(t\_\*\\), a precisely shaped photon state initially supported entirely in the lead evolves into the localized boundary excitation with unit probability. The Hamiltonian remains nonnegative, with strict zero-energy Schur margin

\\[ \boxed{1-2g_0^2=0.02B.} \\]

The bath itself remains gapless.

This is faster than the previous \\(3.831706B^{-1}\\) capture construction, while retaining a positive stability margin.

### 2. A rigorous finite-support approximation

The exact incoming photon extends over the lead, but its distant-site amplitudes decrease factorially. If the source is restricted to the first \\(L\\) lead sites, the ideal conditional-sign error is bounded by

\\[ \epsilon_L\le 2\sum\_{n=L+1}^{\infty}\frac{t\_\*^n}{n!}. \\]

For \\(L=16\\), the executed rational-root and factorial-tail calculation gives

\\[ \boxed{\epsilon\_{16}<2.40\times10^{-8}.} \\]

The complete captured–held–released photon operation uses a local conditional energy shift of only \\(B\\), applied for time \\(\pi/B\\). Its ideal photon-operation duration is approximately \\(8.0094B^{-1}\\).

This is a finite-time coherent-state construction, not an asymptotic scattering approximation. It requires a specially prepared incoming photon and controllable boundary hopping.

## 3. A new local-current limit explains the remaining loss

The next calculation yields a more general result than the specific gate design.

For any number-conserving, single-photon Hamiltonian in which a localized emitter communicates with the rest of the system through one hopping edge bounded by \\(g\\), let \\(p(t)\\) be its occupation probability. Probability-current conservation gives

\\[ |\dot p(t)|\le2g\sqrt{p(t)(1-p(t))}. \\]

Consequently, moving a photon from zero emitter occupation to unit emitter occupation requires

\\[ \boxed{T\_{\rm capture}\ge\frac{\pi}{2g}.} \\]

It also requires an integrated emitter occupation of at least

\\[ \boxed{\int_0^{T\_{\rm capture}}p(t)\\,dt\ge\frac{\pi}{4g}.} \\]

These statements do not depend on the details of the bath spectrum or the shape of the incoming photon, provided the stated single-edge coupling constraint holds.

At \\(g=0.7B\\), the constructed Jacobi capture achieves:

| Quantity                | Universal lower bound | Construction     |
| ----------------------- | --------------------- | ---------------- |
| Capture duration        | \\(2.243995/B\\)      | \\(2.433886/B\\) |
| Emitter occupation-time | \\(1.121997/B\\)      | \\(1.150798/B\\) |

The capture is only 8.46% above the minimum time and 2.57% above the minimum radiative exposure allowed by that interface.

This changes the research direction: improving the incoming waveform alone cannot substantially reduce emission from the boundary site. A stronger architecture must alter where the photon is stored or change its coupling topology.

## 4. Constructive repair: transfer the photon into a protected storage mode

I tested a second architecture that removes the photon from the radiatively exposed emitter during the conditional hold.

After capture, a locally coupled storage oscillator receives the photon through an exact resonant swap. The conditional phase is applied to that storage mode; a second swap returns the photon for release.

The declared controls are

\\[ J=10B,\qquad U=B, \\]

with a maximum temporary on-site energy of \\(11B\\). The two-mode swap Hamiltonian remains positive, with eigenvalues \\(B\\) and \\(21B\\). The all-particle capacity lower bound is preserved.

The emitter occupation-time decreases from

\\[ 5.44319/B \quad\longrightarrow\quad 2.45868/B. \\]

This is a 54.8% reduction in exposure to independent emitter radiation.

Direct capture gate

# 1.043%

Full-state error at emitter loss \\(2\times10^{-5}B\\)

Protected-storage variant

# 0.724%

Same emitter loss; storage loss \\(10^{-6}B\\)

Both figures come from executed no-jump evolution with emitted radiation retained as orthogonal environmental states. Neither is a postselected fidelity.

The protected-storage variant therefore meets the 1% loss-only target in this effective open-system model, whereas the direct construction does not. It adds a controlled storage oscillator and stronger transient couplings, but no memory-capacity-dependent detuning range.

### Scientific assessment

The most useful conclusion is the new port-current/exposure principle. It explains why the original capture process is already almost optimal within its own microscopic interface and directs further invention toward topology changes instead of narrower parameter optimization.

The present construction gives an end-to-end ideal controlled-photon operation with explicit finite-time loading, coherent Boolean flags, stability, switching bounds and an independent-loss audit.

It does not yet acquire the photon source, the physical switching mechanism or a semibounded microscopic completion of the additional Markov radiation channel. Time-reversed absorption and passive photon transfer have relevant established precedents.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubs.acs.org\&sz=32)

ACS Publications

+2



## Preserved research

The proof and executable results are available:

- Complete mathematical derivation and scope
- Exact-rational capture proof and results
- Full coherent memory–reference–photon simulation and results
- Independent radiation audit, protected-storage construction, and local-current theorem audit

Next substantive physics obstruction: reduce radiative occupation during the capture and release themselves, ideally through a dark-state transfer interface derived from one positive, local Hamiltonian with a genuinely prepared traveling photon. The current local-current theorem establishes exactly which single-port architectures cannot achieve that reduction merely through waveform shaping.