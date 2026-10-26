# Astra foundational physics continuation — finite-time Jacobi capture, an exactly local Boolean phase gate, and a loss-exposure frontier

26 October 2026. Independent continuation from `ASTRA_LOCAL_BOOLEAN_SPECTRAL_COMPILATION_20261026.md` and `astra_flag_exact_continuation/`. This record contains new exact-rational capture certificates and fresh executed calculations. Its claims are mathematical for declared Hamiltonians; no historical novelty, actual source apparatus, or experimental advantage is established.

## 1. Scientific decision: substitute time-domain capture for large stationary detuning

The prior lossless broadband stationary Fano gate had a conservative full-wavepacket certificate but required root-controlled emitter shifts of order 201–400 times the binding-energy unit. Its four-pulse Boolean flag compiler was already verified, and a first-J1-zero boundary-photon input was found but had not been integrated with a faster strictly positive boundary choice, full flag/reference propagation, finite switch errors, and independent radiative loss. I pursued those missing physical interfaces. A Markov chiral perfect-loading alternative has a different difficulty: with a bounded coupling rate, a finite-start strictly causal incoming waveform cannot be captured with exactly zero early reflection (the loading rate Gamma(t)=F'(t)/F(t) would diverge at the initial support edge). This is not a universal obstruction to non-Markov structured waveguides.

## 2. General spectral orthogonality principle

Let `h` be a positive self-adjoint, number-conserving one-particle Hamiltonian, and `|e>` the normalized localized capture state. Let `P=I-|e><e|` project onto all other sites/modes. Starting from *any* normalized photon supported in `Ran P`, the maximum occupation of `|e>` after time `T` is exactly

\[ P_{\rm capture}^{\rm max}(T)=\|P e^{+ihT}|e\rangle\|^2=1-|a(T)|^2,\qquad a(T)=\langle e|e^{-ihT}|e\rangle. \]

Proof: maximize `|<e|e^{-ihT}|psi>|^2=|<Pe^{ihT}e|psi>|^2` by Cauchy–Schwarz. The optimum is the normalized backward-evolved state projected into the external modes. **Perfect finite-time capture is possible iff the localized spectral measure's characteristic function `a(T)` has a real zero.** This is an exact criterion, not an assumption of adiabatic loading.

If `spec(h)` is contained in an interval of width `W`, then, for `WT<=pi`, centering the spectral interval and taking the real part of the Fourier integral gives `|a(T)|>=cos(WT/2)`. Thus

\[ P_{\rm capture}^{\rm max}(T)\le\sin^2(WT/2),\quad T\le\pi/W; \qquad T_{\rm perfect}\ge\pi/W. \]

This is a finite-band speed–fidelity lower bound. An exponential Markov survival amplitude has no finite real zeros; conversely, spectral interference in a bounded-band Jacobi lattice can create such zeros.

## 3. Strictly stable gapless Jacobi construction

In units `B=1`, on sites `0,1,...`, let

\[h=I+A_g,\quad (A_g)_{0,1}=g=7/10,\quad (A_g)_{j,j+1}=1/2\ (j\ge1).\]

The lead without site 0 has positive spectrum `[0,2]` and the zero-energy endpoint inverse boundary value `2`. The Schur margin of the boundary state is

\[1-2g^2=1/50>0.\]

Equivalently, `h` is positive and, by the alternating-site symmetry `S A_g S=-A_g`, `||A_g||<=1`. The essential spectrum is gapless `[0,2]`. The boundary occupation survival amplitude is real up to the trivial phase `e^{-iT}`:

\[a(T)=e^{-iT}\sum_{k=0}^\infty\frac{(-1)^kT^{2k}}{(2k)!}\mu_{2k},\qquad\mu_{2k}=\|A_g^k|0\rangle\|^2.\]

For rational `g=7/10`, all coefficients `mu_{2k}` are exact rationals from finite-length walks. `capture_orthogonality_certificate.py` evaluates terms through `k=26` **using exact fractions** and bounds the omitted alternating remainder by the positive absolute tail using `||A_g||<=1`. It gives opposite certified signs at rational time endpoints:

\[a(2.433886050)e^{iT}>+6.2649\times10^{-10},\quad a(2.433886053)e^{iT}<-9.0308\times10^{-10}.\]

Continuity proves a perfect capture time `T_*` in that interval. Independent diagonalization gives `T_*=2.43388605122875...`, *only as a diagnostic*. The general band-speed lower bound here is `pi/2=1.570796...`. The previously reported `g=1/2` Bessel `J1` construction takes `3.83170597...`; the new strictly positive `g=0.7` shortens it by 36.5%.

Set `phi=e^{ihT_*}|e>`; the equality `a(T_*)=0` ensures that `phi` has **zero emitter amplitude**. Normalize its projection `phi_L` onto lead sites 1 through `L`. Exact unitarity gives `|<e|e^{-ihT_*}|phi_L>|^2=1-delta_L^2`, with

\[\delta_L=\|P_{>L}\phi\|\le\sum_{n=L+1}^\infty\frac{T_*^n}{n!}.\]

Indeed, the first `L` Taylor powers of the nearest-neighbour operator cannot reach a site past `L`. For `L=16`, the new independently executed conservative bound is `2 delta_L < 2.39970522e-8`. Direct matrix propagation finds `delta_L≈1.02e-13`, but that much smaller value is not the claimed certified precision. This declaration preserves photon source preparation as an input resource.

## 4. Exact dynamic conditional phase with unit-scale control

During transfer, take root–photon coupling **OFF**, and evolve with `h_g`. Upon capture, turn the boundary hopping off, so the emitter separates from the positive lead. On the hold interval of length `tau=pi/U`, use the one-body emitter term `(1+U r)|e><e|`, where root flag `r=0` or `1`. The root-dependent interaction is the two-local cross-Kerr `U r n_e`. Choose `U=1`. After holding, remove the root interaction, restore the boundary hopping and release under the **same** `h_g` for `T_*`. All controls are ordinary positive self-adjoint Hamiltonians on every finite photon sector. The root=1 and root=0 emitter hold phases differ by `-1`, while every lead leakage branch acquires precisely the same physical evolution. Thus if `U_r` is the complete capture/hold/release propagator, for any incident `psi`,

\[ \|(U_1+U_0)\psi\|=2\|P_{\rm lead}U_{\rm capture}\psi\|.\]

For `phi_L`, this is **exactly** `2 delta_L`. This is a norm claim about the complete non-postselected photon, and its common outgoing waveform is the actual `U_0 phi_L`, not an assumed freely propagating original input.

No photon-emitter coupling of strength `201` or `400` is necessary. Peak required phase interaction is `U=1`, and the ideal photon transfer/hold/release time is `2T_*+pi≈8.00936476` binding-energy inverse units. The additional control interface is timed modulation of the emitter–lead edge and production of a special incoming lead state.

### Timing and finite switch bound

If the capture instant has error `Delta`, then the leaking lead amplitude of an initially localized emitter obeys `||P_lead e^{-ih_g Delta}|e>||<=g|Delta|` by Duhamel against the isolated emitter. If the emitter–lead hopping is then switched off with a nonnegative envelope `g_off(t)` (root interaction held off during the switch), the additional lead leakage is at most `int |g_off(t)|dt`. A source preparation error `epsilon_src` contributes additively. Consequently the full conditional photon-state error obeys

\[\boxed{\epsilon_{\rm conditional}\le 2\left(\delta_L+\epsilon_{\rm src}+g|\Delta|+\int_{\rm off\ ramp}|g_{\rm off}(t)|dt\right).}\]

This estimate is **independent of the subsequent root-blind release ramp**, when the reference photon waveform is defined by the actual root=0 release. A linear off ramp of duration `s` contributes `g s/2`; therefore with `g=.7`, `Delta=.001` and `s=.002`, the bound is `<.002800025` for the certified 16-site source (assuming no extra source error). An independent time-dependent Schrödinger integration gave `.002799999` under those conditions. A target requirement for the absolute *shape* of the outgoing photon would also require a release-ramp bound; the above theorem is a relative conditional phase certificate.

## 5. Exact Boolean encoding and whole-memory/reference composition

Use the earlier four-pulse `a,b`-controlled single-flag gadget, with generators `b(I-X_c)`, `a(I-Z_c)`, `b(I+X_c)`, `a(I-Z_c)` and times `(pi/4,pi/2,pi/4,pi/2)`. These are each positive-semidefinite, at most two-local, and preserve the two input bits. Its computational action on a newly zero target is `00 -> |0>`, `10 -> |0>`, `01 -> -i|0>`, `11 -> |1>`. It is **not exactly a Toffoli as a standalone all-branch unitary**; the branch phases cancel when the physically implemented encoder is reversed after the diagonal phase interaction.

Arrange the gadgets into a balanced tree with `m-1` neutral ancilla spins and depth `d=ceil(log2 m)`. The encoder `W` satisfies

\[W|x,0^{m-1}\rangle=e^{i\theta(x)}|x,F(x)\rangle,\quad r(F(x))=\prod_{j=1}^m x_j.\]

The composite `W^dagger` – photon hold/release – `W` yields the conditional phase `Z_AND|x>=(-1)^{prod x_j}|x>`, with complete memory/reference operator-norm error <= `2 delta_L` in the ideal control model. The full photon+memory Hamiltonian conserves `N=K+N_boson` where `K=sum x_j`; neutral ancilla operations have no photon U(1) charge. Because every active photon Hamiltonian and every two-local control pulse Hamiltonian is positive, `H_N(t)>=-min(N,m)` **at every instant** for every finite sector. This is not a claim that the photon is generated freely or that its external source obeys the same energy budget.

When the root–photon coupling is off, flag pulses and photon transport commute exactly, so **flag computation may overlap capture** and uncomputation may overlap release. With an available, appropriately timed prepared input photon, the ideal operation clock from first flag pulse to final uncomputation is

\[ T_{\rm logical}=2\max(3\pi d/2,T_*)+\pi=3\pi d+\pi\qquad(m\ge2).\]

This does not count external production and injection of the matched photon. In particular for `m=4`, the clock is `7pi=21.99114858`; there is no need for an extra wait to put the photon far away during the entire flag sequence.

If an imperfect physical encoder `W_actual` preserves memory words and the decoder is exactly its adjoint, define `q_x` as its probability of outputting an incorrect root flag on memory word `x`, and `q_max=max_x q_x`. An exact projection calculation gives, for an ideally captured photon, the root-controlled sign error `2sqrt(q_max)` in worst-case reference norm. With a finite captured-photon error `eps_ph`, the complete error is at most

\[\boxed{\epsilon_{\rm total}\le \epsilon_{\rm ph}+2\sqrt{q_{\max}}.}\]

If each fresh-node gadget has conditional wrong-target probability `p_max`, a union argument (each target is written once, no controls are flipped) gives `q_max<=(m-1)p_max`. This yields **square-root rather than linear amplification** of small coherent control overrotations for this specific compute–diagonal–uncompute contract. Arbitrary crosstalk or a non-matched decoder is not covered.

`coherent_flag_capture_fulltest.py` directly propagated all `2^7` registers, a three-dimensional untouched reference and a 100-mode full one-photon lattice for `m=4`. For an exactly calibrated encoder, the norm residual was `5.78e-14`; for relative common pulse overrotation `1e-4`, `3e-4`, and `1e-3`, measured full-state errors were `0.00021814`, `0.00065441`, and `0.00218137`, respectively. All were below the independently calculated compositional upper bounds. These finite matrices and the analytic infinite-lattice moment proof are separate checks.

## 6. Independent-radiation obstruction (the decisive physical resource)

Include an *additional*, unobserved Markov emission channel of rate `kappa` from the boundary emitter. This effective open-system augmentation **does not** by itself prove a positive-frequency microscopic model for that extra radiation continuum. On a perfectly parked emitter, the conditional hold lasts `pi/U`. Including the emitted environment orthogonally, even with otherwise perfect transfers the hold stage imposes a full pure-state error

\[\epsilon_{\rm hold}=\sqrt{2\left(1-e^{-\kappa\pi/(2U)}\right)}.\]

A 1% full-state target requires the necessary condition

\[\boxed{\kappa/U\le -\frac2\pi\log(1-10^{-4}/2)=3.18317844\times10^{-5}.}\]

This is an independent-loss ceiling, not a failure branch that may be postselected away.

Capture and release add significant exposure. For the exact `g=.7` input, the emitter occupancy during either ideal photon transfer is `|a(t)|^2`. The integral is `I_cap=1.15079830299772`, so the complete lossless emitter occupation-time is

\[\boxed{I_e^{\rm direct}=2 I_{\rm cap}+\pi=5.44318925958524.}\]

A Duhamel expansion of the no-jump propagator gives the rigorous leading term `epsilon_full^2=kappa I_e+O(kappa^2)` as `kappa->0`. In independently executed non-Hermitian full-Fock-one-photon + orthogonal jump-environment simulations, `kappa=2e-5` produced a full-state error of `0.01043363` (1.043%) even for otherwise perfectly programmed controls. Hence the improved gate fails a 1% end-to-end target at that radiation rate.

## 7. Executed constructive repair: a protected storage orbital

Add one local dark-storage bosonic mode `d`, decoupled from the radiative port except during two controlled swaps. At capture completion turn off the boundary-to-lead edge and turn on the positive two-mode Hamiltonian

\[ H_{\rm swap}= (J+1)(n_e+n_d)+J(e^* d+d^* e),\qquad J=10.\]

Its one-particle eigenvalues are `1` and `21`, and a duration `pi/(2J)` transfers `|e>` to `|d>` exactly up to a known common phase. Apply the root-dependent `U r n_d` only while the photon is held on `d`; perform the inverse swap, and release to the lead. All constituent one-body Hamiltonians remain positive, all rooted controls stay two-local, and no higher bosonic sector can acquire an energy below `-min(N,m)` from the signal subsystem.

In the *lossless* model the conditional phase remains exact, with the same finite-source error `2 delta_L`. The new cost is a transient on-site energy `J+1=11B` and active emitter–storage hopping `J=10B`. The strict distinction is that `J` does not scale with the memory capacity `m`.

The integrated lossless occupations now are

\[\boxed{I_e^{\rm store}=2 I_{\rm cap}+\frac\pi{2J}=2.45867623867494,\quad
 I_d^{\rm store}=\frac\pi U+\frac\pi{2J}=3.29867228626928.}\]

The emitter's radiative exposure decreases by `54.8%`; the price is time on the auxiliary storage oscillator, requiring small `kappa_d`. Exact no-jump propagation plus orthogonal environment emission gives, at `kappa_e=2e-5`, `kappa_d=1e-6`, a full-state error **0.00724371** (0.724%). At `kappa_e=2e-5`, `kappa_d=1e-5`, the error is 0.9064%. Thus the modified architecture crosses the prior 1% failure threshold in this declared Markov loss model.

When memory-tree computation time per pass exceeds the transfer-plus-swap duration (true for `m>=2` with the stated `J`), both swaps can be overlapped with compute and uncompute. They add controls and transient energy resources, but no necessary increase in the ideal Boolean-oracle clock `3pi ceil(log2 m)+pi`. The photon must be delivered in time, and the root interaction must remain off outside the hold.

## 8. Limits and future attack

1. **The input photon is specified, not sourced.** It is the (truncated) time-reversed boundary-emission state across 16 lead sites. An actual high-fidelity source, physical injection, and dispersion-preserving transport have not been supplied. Source availability `p` requires inverse-availability resource accounting.
2. **Switching is a resource.** The emitter–lead edge must be gated while retaining the calibrated photon mode. The local storage repair requires another independently switchable edge and an on-site energy of `11B` during swaps. The common outgoing photon waveform may be distorted by the root-blind release ramp; only the *relative* controlled phase enjoys ramp independence.
3. **Independent radiation is not cancelled.** Moving the photon to the storage orbital shortens its exposure to the original lossy emitter, but does not repair radiation emitted during capture or release. The loss simulations use Markov baths; an inclusive finite-band radiation Hamiltonian remains to be acquired.
4. **No general physical novelty claim.** Time-reversed absorption, coherent photon storage and ancilla logic have prior art. The new scoped mathematical result is a strictly positive, gapless local-lattice finite-time gate with certified capture zero, finite-source and switch bounds, a compositional Boolean reference norm, and an exact loss-exposure comparison.
5. **Strongest prospective alternative.** A genuinely dark adiabatic transport network that avoids populating the radiative boundary during capture/release could further reduce `2I_cap`; it must obey photon-current speed bounds and must not silently replace the source/lead interface. A positive passive Fano measurement remains an equally informed comparator for a real platform.

## 9. Executable preservation

- `astra_physics_finite_capture/capture_orthogonality_certificate.py` and `capture_orthogonality_results.json`: exact-fraction 52nd-order moment sign certificate, spectral stability, finite-source tail, numerical independent wavefunction diagnostic.
- `astra_physics_finite_capture/coherent_flag_capture_fulltest.py` and `coherent_flag_capture_fulltest_results.json`: full register/reference/photon propagation, imperfect encoder with exactly reversed decoder, timing jitter and linear off-ramp evolution.
- `astra_physics_finite_capture/capture_independent_loss_audit.py` and `capture_independent_loss_results.json`: radiation-environment inclusive norm and occupation-time costs, not survival-conditioned fidelity.
- `astra_physics_finite_capture/dark_storage_loss_comparison.py` and `dark_storage_loss_results.json`: positive two-mode storage-swap Hamiltonian, independent radiation from two local modes, and full unconditional state-vector norm.

Representative prior physics: *Deterministic Loading of Microwaves onto an Artificial Atom Using a Time-Reversed Waveform* (Nano Lett., 2022); *Passive Quantum State Transfer in a Dispersion-Engineered Waveguide* (PRL 137, 103605, 2026); *Enabling Deterministic Passive Quantum State Transfer with Giant Atoms* (PRX Quantum, October 2026). These address source/transfer physics; they do not certify this particular Boolean composite or its local control hardware.

## 10. New sharp local-current and loss-exposure theorem (strongest subsequent attack)

The particular capture came unexpectedly close to a universal bottleneck. This theorem **does not require** a Jacobi chain or any assumption on the unobserved bath Hamiltonian.

Let a normalized one-photon wavefunction be `(a(t),b(t))` in `C|e> ⊕ H_external`, with an arbitrary time-dependent self-adjoint Hamiltonian of block form

\[ h(t)=\begin{pmatrix}\omega(t)&v(t)^*\\v(t)&L(t)\end{pmatrix},\qquad\|v(t)\|\le G. \]

Here `G` is the *total* coupling-vector norm through the port, not a bound on each of many independent edges. Put `p(t)=|a(t)|^2`. The Schrödinger equation gives

\[|\dot p(t)|=2|\operatorname{Im}(\overline a\langle v,b\rangle)|\le2G\sqrt{p(t)(1-p(t))}.\]

Consequently `theta(t)=arcsin sqrt(p(t))` is `G`-Lipschitz (extend continuously at `p=0,1`). If `p(0)=0` and `p(T)=1`,

\[T\ge\frac\pi{2G}.\]

More generally, using the final value `theta(T)=pi/2`, we obtain `theta(t)>=max(0,pi/2-G(T-t))` and hence

\[\boxed{\int_0^T p(t)\,dt\ge\frac\pi{4G}.}\]

Both constants are sharp, attained simultaneously by a two-site resonant Rabi transfer at coupling `G`. The time-dependent `L(t)` can contain any interacting *one-particle* bath network, with or without continuum. External drives that inject photons directly into the protected site, or routes that bypass that site, violate the theorem's port assumption and can evade this bound.

For `G=.7`, the exact Jacobi capture takes only `1.08462199` times the minimum time and exposes the emitter for only `1.02566934` times the minimal occupation integral. In a staged single-site capture/hold/release oracle, with emitter-local phase strength `U=1`, the two full transfers plus hold must expose that same emitter for at least

\[\frac\pi{2G}+\frac\pi U=5.385587406...,\]

whereas the construction takes `5.443189259...`, **only 1.07% above this universal staged-architecture lower bound**. The dark-storage construction exposes the emitter for `2.458676238...` compared with the staged capture/release and bounded-swap lower bound `pi/(2G)+pi/(2J)=2.401074385...`, only 2.40% higher.

Thus, within the original one-port topology and at fixed hopping/interaction strengths, optimizing the photon waveform further can reduce the weak-Markov-loss coefficient by barely 1%. The scientifically substantive way forward is **topology change or transferring the interaction to a protected degree of freedom**, not more numerical waveform fitting.

At small independent loss rate `kappa`, `epsilon_full^2=kappa I+O(kappa^2)` yields an unavoidable weak-loss coefficient `I>=5.385587406` for direct capture–hold–release. The necessary corresponding 1% rate scale is `kappa≈1.86e-5 B` to leading order, whereas the achieved full loss calculation crosses 1% near `1.84e-5 B`. These are not global device-noise thresholds and are *not* exact finite-kappa inequalities without the preceding Markov/no-jump model.

Executed independent audit: `astra_physics_finite_capture/local_current_speed_and_exposure.py` and `local_current_speed_exposure_results.json`. It also numerically checks the port-current inequality on 15 random eight-mode Hermitian Hamiltonians with 101 times each; the analytic derivation, not those samples, proves the theorem.
