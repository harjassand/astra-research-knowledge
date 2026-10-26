# ASTRA — An embedded two-photon resonance and asymptotic controlled-phase operation

27 October 2026. Independent continuation of temporary foundational-physics research. Energy units set the strong SSH edge weight to 2, weak weight to 1 and \(\hbar=1\). This note distinguishes (i) exact operator identities, (ii) a small-coupling spectral scaling result, (iii) executable finite-\(g\) checks, and (iv) unacquired control and device resources. **No new fundamental interaction, experimentally acquired gate, or historical priority is claimed.**

## 1. Physical question and competing mechanism

Previous work constructed a two-hard-core-emitter quasimode near energy 6 inside the free two-photon continuum. It found a connected energy shift \(-g^4/12\), a residual of order \(g^4\), and a strictly positive fourth-order on-shell source. Its Duhamel norm estimate controlled time \(O(g^{-2})\) but not the \(O(g^{-4})\) duration needed for a nonlinear conditional phase. A plausible but unproved golden-rule estimate predicted radiative decay at order \(g^8\).

The main attack here replaces further finite-volume fitting by the **exact interacting two-particle Green function**. A hard-core constraint excludes only two harmonic two-particle vectors, making the resolvent a rank-two finite-rank restriction. Parity reduces that restriction to one scalar harmonic-mean formula. The alternative is a geometry engineered to cancel the fourth-order radiative shell; the prior positive shell estimate for all finite separation \(d\) rules out accomplishing this by separation alone in the same gradient-port family. We pursue the resolvent mechanism and retain that negative comparator.

## 2. Declared SSH Hamiltonian and stability

The bath is an infinite alternating weighted graph Laplacian with onsite energy 3, intra-cell hopping \(-2\), inter-cell hopping \(-1\), and Bloch energies

\[
 \lambda_\pm(k)=3\pm e(k),\qquad e(k)=\sqrt{5+4\cos k},\quad -\pi\le k<\pi.
\]

Its absolutely continuous bands are \([0,2]\cup[4,6]\), so it is **gapless at zero** and has a one-photon gap around energy 3. Two hard-core memories \(L,R\) couple to the adjacent normalized gradients \(v_j=(|A_j\rangle-|B_j\rangle)/\sqrt2\). The number-conserving Hamiltonian is

\[
 H_g=d\Gamma(h)+\left(3+\frac{g^2}{2}\right)(n_L+n_R)
 +g\sum_{j=L,R}\bigl(\sigma_j^+a(v_j)+a^*(v_j)\sigma_j^-\bigr).
 \tag{1}
\]

The earlier exact graph-form identity \(\langle v_j,h^{-1}v_k\rangle_{\rm form}=\delta_{jk}/4\) gives harmonic one-body Schur margin \(3+g^2/4\). Compressing its second quantization to hard-core memory occupations preserves nonnegativity in **every fixed particle sector**. This ensures that the proposed embedded resonance is not an instability below the ground state.

Denote the one-body harmonic Hamiltonian by \(h_1(g)\). Its exact parity states are \(e_\sigma=(e_L+\sigma e_R)/\sqrt2\), \(\sigma=\pm1\). Put \(\varepsilon_g=3+g^2/2\), and let \(\mu_\sigma\) be the **entire** spectral measure of \(e_\sigma\) for \(h_1(g)\): its in-gap atom, both positive continuum bands and the additional upper positive atom when present. In the two-boson harmonic sector define

\[
 L_\sigma(z)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(y)}{x+y-z},\qquad \operatorname{Im}z>0.
 \tag{2}
\]

## 3. Exact interacting Green function (all couplings)

In the harmonic two-particle space, let \(|2_L\rangle,|2_R\rangle\) be normalized double occupations of the two emitters. The physical hard-core two-particle Hamiltonian is precisely the compression of \(d\Gamma_2(h_1(g))\) to the orthogonal complement of these two vectors. The target \(p=|LR\rangle\) belongs to the allowed subspace.

With \(|2_\pm\rangle=(a_\pm^*)^2|0\rangle/\sqrt2\), one has

\[
 p=\frac{|2_+\rangle-|2_-\rangle}{\sqrt2},\qquad
 D=\frac{|2_+\rangle+|2_-\rangle}{\sqrt2}
   =\frac{|2_L\rangle+|2_R\rangle}{\sqrt2}.
\]

Parity separates the antisymmetric forbidden vector \((|2_L\rangle-|2_R\rangle)/\sqrt2\) from the symmetric target. The Schur/Kreĭn formula for compressing the harmonic resolvent away from \(D\) gives

\[
 \boxed{G_p(z):=\langle p,(H_{g,2}-z)^{-1}p\rangle
     =\frac{2L_+(z)L_-(z)}{L_+(z)+L_-(z)}.}
 \tag{3}
\]

Equivalently,

\[
 \boxed{D_g(z):=G_p(z)^{-1}=	frac12[L_+(z)^{-1}+L_-(z)^{-1}].}
 \tag{4}
\]

The derivation is exact for all nonreal \(z\); no continuum state is deleted and no phenomenological decay term is inserted. For orientation, if \(M=(L_++L_-)/2\) and \(N=(L_+-L_-)/2\), then \(G_p=M-N^2/M\).

An independently assembled 76-dimensional finite-hard-core Fock Hamiltonian with a 12-dimensional one-particle harmonic model reproduced (3) at four nonreal energies with errors between \(4.7\times10^{-16}\) and \(2.3\times10^{-12}\). These finite-matrix checks verify the identity, not the infinite-volume resonance limit.

## 4. Exact one-body parity resolvents

Write \(t=z-3\), \(a=t^2-5\), \(q=(t+1)(t+3)/4\), and take the analytic branch

\[
 I(t)=\frac{1}{\sqrt{a-4}\sqrt{a+4}}
\]

obtained from the resolvent in the upper half-plane and satisfying \(I(t)\sim t^{-2}\) at infinity. Direct Bloch integration gives

\[
 F_0(z)=qI(t)-\tfrac14,\qquad
 F_1(z)=q\bigl[\tfrac a4 I(t)-\tfrac14\bigr],\qquad
 F_\sigma(z)=F_0(z)+\sigma F_1(z).
 \tag{5}
\]

The one-particle emitter Green function is

\[
 G_\sigma^{(1)}(z)=[z-\varepsilon_g-g^2F_\sigma(z)]^{-1}.
\]

At the center of the one-particle gap,

\[
 F_+(3)=-\tfrac38,\quad F_-(3)=-\tfrac58,\quad
 F_+'(3)=-\tfrac16,\quad F_-'(3)=-\tfrac12.
\]

The in-gap atoms \(E_\sigma\), with residues \(p_\sigma\), therefore satisfy

\[
 \begin{aligned}
 E_+&=3+\frac{g^2}{8}-\frac{g^4}{48}+O(g^6),
 &p_+&=1-\frac{g^2}{6}+O(g^4),\\
 E_-&=3-\frac{g^2}{8}+\frac{g^4}{16}+O(g^6),
 &p_-&=1-\frac{g^2}{2}+O(g^4).
 \end{aligned}\tag{6}
\]

**Important positive spectral pole:** the \(+\) parity one-particle measure also contains an atom above the top bath band,

\[
 E_U=6+\frac{g^4}{3}+o(g^4),\qquad p_U=\frac{2g^4}{9}+o(g^4).
 \tag{7}
\]

This atom is retained in (2) and in the numerical integral. Its pairing with nonnegative continuum excitations starts *above* 6, so it adds no imaginary part at the pair resonance located slightly *below* 6. Dropping it from a finite-band normalization would be incorrect.

## 4A. A general generative law beyond the SSH lattice

The rank-two Green-function identity is not specific to alternating chains. Suppose a reflection-symmetric bath has two congruent ports, a memory transition \(\varepsilon\) in a **one-particle spectral gap**, and parity bath resolvents \(F_\pm(z)\) analytic near \(\varepsilon\). Both emitters have the same calibrated energy \(\varepsilon+g^2a\); the common diagonal retuning \(a\) is arbitrary. Define

\[
 \Delta F=F_+(\varepsilon)-F_-(\varepsilon),\qquad
 \Delta F'=F_+'(\varepsilon)-F_-'(\varepsilon).
\]

If \(\Delta F\ne0\), the parity double-bound poles are separated at order \(g^2\). Repeating the harmonic-mean calculation yields the **universal leading connected energy**

\[
 \boxed{\chi_g=-g^4\,\Delta F\,\Delta F'+o(g^4).}\tag{10a}
\]

The common retuning drops out. In real-space terms, with \(F_{LR}(z)=\langle v_L,(z-h)^{-1}v_R\rangle\), one has \(\Delta F=2F_{LR}\) and \(\Delta F'=2F'_{LR}\); hence \(\chi_g=-4g^4F_{LR}(\varepsilon)F'_{LR}(\varepsilon)+o(g^4)\). Its sign can be either positive or negative in a passive, gapped bath.

For a nonthreshold, open two-photon continuum define the nonnegative projected spectral convolution

\[
 c=\frac12\sum_{\sigma=\pm}\int \nu_\sigma(E)\nu_\sigma(2\varepsilon-E)\,dE,
 \qquad
 \nu_\sigma(E)=\frac{\langle v_\sigma,\delta(E-h)v_\sigma\rangle}{(E-\varepsilon)^2}.
\]

Assume this density exists, is continuous at \(2\varepsilon\), and that other discrete-plus-continuum channels do not introduce a stronger threshold singularity at the pair energy. The same proof gives the **radiative amplitude linewidth**

\[
 \boxed{\gamma_g=\pi (\Delta F)^2c\,g^8+o(g^8),\qquad
 \Gamma_g=2\gamma_g.}\tag{10b}
\]

If \(c>0\), the rescaled pair spectral measure has the Cauchy limit stated below, with \(\gamma=\pi (\Delta F)^2c\). If \(c=0\), the octic coefficient vanishes and a different, potentially higher-order analysis is necessary; no permanent bound state follows merely from this zero. The general law requires one-particle spectral separation and parity. It is not a theorem for arbitrary matter Hamiltonians.

**Independent sign test.** I also diagonalized full hard-core two-particle Hamiltonians for a parity-symmetric two-mode bath whose pair energy is separated from all bath pair energies. For two choices of port weights, the predicted \(\chi_g/g^4\) limits are \(+0.240077328\) and \(-0.130716626\). The independently computed finite-matrix coefficients at \(g=0.04\) are respectively \(+0.239555055\) and \(-0.130678080\). This demonstrates that the connected shift is not merely a repulsive hard-core penalty: its sign is set by the bath's off-diagonal spectral response and its energy derivative.

For the SSH example, \(\Delta F=1/4\), \(\Delta F'=1/3\), and \(c=43/(648\pi^2)\), reproducing both exact constants in the following sections.

## 5. Fourth-order center and eighth-order radiative width

Split each parity pair resolvent into its near-resonant double-bound atom and its regular remainder:

\[
 L_\sigma(z)=\frac{p_\sigma^2}{2E_\sigma-z}+R_\sigma(z).
 \tag{8}
\]

For \(z=6+O(g^4)\) with \(\operatorname{Im}z=O(g^8)\) and its real part slightly below 6, the explicit measures give \(R_\sigma=O(g^2)\). The largest real term comes from bound-plus-continuum configurations, whose energy ranges are separated from 6. The two-continuum contribution is \(O(g^4)\) in boundary value; it has nonzero imaginary part. The upper atom contributes only smaller regular terms on this side of its threshold. With \(u_\sigma=2E_\sigma-z\sim\sigma g^2/4\), inversion of (8) gives

\[
 L_\sigma^{-1}=\frac{u_\sigma}{p_\sigma^2}
 -\frac{u_\sigma^2}{p_\sigma^4}R_\sigma+O(g^8).
 \tag{9}
\]

(The final \(O(g^8)\) denotes the squared-remainder term for the stated spectral neighborhood; the real \(O(g^6)\) term from the first remainder must be retained when locating the finite-\(g\) center.)

Let \(z_*(g)\) be the unique real zero of \(\operatorname{Re}D_g(E+i0)\) in the small neighborhood of \(6-g^4/24\). The dominant derivative is \(-1+O(g^2)\), and (6)–(9) yield

\[
 \boxed{z_*(g)=6-\frac{g^4}{24}+O(g^6|\log g|).}
 \tag{10}
\]

Since \(E_++E_-=6+g^4/24+O(g^6)\), the *connected* energy difference is

\[
 \boxed{\chi_g=z_*(g)-(E_++E_-)=-\frac{g^4}{12}+o(g^4).}
 \tag{11}
\]

### The radiative coefficient with every continuum channel included

The bath's gradient polarization weights at \(3\pm e(k)\) are

\[
 w_\pm(k)=\frac{1\pm(2+\cos k)/e(k)}2,\qquad
 w_+(k)w_-(k)=\frac{\sin^2 k}{4e(k)^2}.
\]

In parity channel \(\sigma\), the continuum part of \(d\mu_\sigma\), parameterized by the bath wave number, is

\[
 d\mu_{\sigma,\pm}(k)=\frac{g^2}{\pi}(1+\sigma\cos k)
 w_\pm(k)|G_\sigma^{(1)}(3\pm e(k)+i0)|^2dk.
 \tag{12}
\]

At pair energy 6, only one photon in the lower band and one in the upper band are on shell. Coarea applied to their energies yields

\[
 \frac1{\pi g^4}\operatorname{Im}R_\sigma(6+i0)
 \longrightarrow c_\sigma
 =\frac{1}{4\pi^2}\int_0^\pi
 \frac{(1+\sigma\cos k)^2\sin k}{(5+4\cos k)^{5/2}}dk.
\]

The integrals evaluate **exactly** to

\[
 c_+=\frac{5}{648\pi^2},\qquad c_-=\frac1{8\pi^2},\qquad
 c:=\frac{c_++c_-}{2}=\frac{43}{648\pi^2}.
 \tag{13}
\]

This is also \(c=\rho_W(6)/4\), where the independently calculated fourth-order source had \(\rho_W(6)=43/(162\pi^2)\). It demonstrates agreement between the quasimode and Green-function channels without equating a finite-ring survival oscillation with physical irreversible radiation.

Inserting the imaginary parts into (9) gives, for the boundary value at \(z_*(g)\),

\[
 \operatorname{Im}D_g(z_*+i0)
 =-\gamma g^8+o(g^8),\qquad
 \boxed{\gamma=\frac{\pi c}{16}=\frac{43}{10368\pi}=0.00132015095543\ldots.}
 \tag{14}
\]

Hence the probability-width coefficient is \(2\gamma=43/(5184\pi)\). This *spectral linewidth* will be given a rigorous meaning by the scaling limit below; an isolated pole of an analytically continued resolvent is **not** needed or separately claimed.

## 6. Long-time spectral theorem: Cauchy/van-Hove limit

**Theorem (small-coupling spectral concentration).** Let \(\nu_g\) be the probability spectral measure of the *bare* two-memory state \(p=|LR;\mathrm{vac}\rangle\) under the **infinite** hard-core Hamiltonian \(H_{g,2}\), recentered at \(z_*(g)\) and rescaled by \(g^8\):

\[
 \nu_g(A)=\langle p,\mathbf1_{\{(H_{g,2}-z_*)/g^8\in A\}}p\rangle.
\]

Then \(\nu_g\) converges weakly as \(g\downarrow0\) to the Cauchy probability distribution

\[
 \boxed{d\nu(x)=\frac{\gamma}{\pi(x^2+\gamma^2)}dx.}
 \tag{15}
\]

Equivalently, for \(\operatorname{Im}w>0\),

\[
 \boxed{\lim_{g\downarrow0}g^8G_p(z_*(g)+g^8w)
 =-\frac1{w+i\gamma}.}
 \tag{16}
\]

**Argument and regularity scope.** The one-body Bloch formulas (5), (12) supply an exact real spectral representation with no missing poles. In the interval just below 6 containing \(z_*\), the bound–continuum denominators remain separated; the upper isolated pole plus soft lower continuum starts above 6. The lower/upper continuous convolution is locally continuous at 6, and its possible internal-band-edge derivative singularity is at worst logarithmic because the lower gradient spectral weight vanishes as \(\sqrt E\) while the upper endpoint has an integrable inverse-square-root singularity. More explicitly, throughout both bath bands the real part of the one-body Fano denominator stays separated from zero for small \(g\), since \(|E-3|\ge1\) and the real parts of the explicit Bloch functions (5) are bounded there. Thus the continuous one-body impurity densities are bounded by a fixed multiple of \(g^2\) times the unperturbed port spectral densities. At the only internal mixed-band threshold \(S=6\), these densities have worst-case endpoint weights \(x^{1/2}\) at the lower band's bottom and \(y^{-1/2}\) at the upper band's top. Their convolution is bounded by integrals of the form

\[
 Cg^4\int_{\max(0,S-6)}^2
 \frac{\sqrt{x}}{\sqrt{x+6-S}}dx,
\]

which remain finite as \(S\to6\) and change by at most a logarithmically corrected small power of \(|S-6|\). The g-dependent upper atom contributes \(O(g^6)\) to the regular part on the *left* side of its threshold, with energy derivative \(O(g^4)\) at \(z_*\); the one-bound-plus-continuum denominators are separated from 6 by order one. These estimates give \(R_\sigma=O(g^2)\), and its change across a \(g^8\) window is negligible at the order used in \(D_g\). The normalized two-continuum coarea density converges to (13) by dominated convergence, and its spectral convolution is continuous on the needed scale. Using (9) in (4) then yields

\[
 D_g(z_*+g^8w)=-g^8(w+i\gamma)+o(g^8).
\]

For \(\operatorname{Im}w>0\) this proves (16); positivity and normalization of the exact spectral measures, together with Stieltjes-transform uniqueness and tightness, give (15). The theorem is a real-axis spectral scaling statement, **not an assertion of a meromorphic second-sheet pole or a global exponential decay law at fixed \(g\)**. In particular, branch points approaching 6 with \(g\) do not need to be crossed by an analytic continuation.

For any fixed \(s\ge0\), a corollary of weak convergence is

\[
 \boxed{\lim_{g\downarrow0}e^{iz_*s/g^8}
 \langle p,e^{-iH_{g,2}s/g^8}p\rangle=e^{-\gamma s}.}
 \tag{17}
\]

At the *shorter* nonlinear phase duration \(t_g=C/g^4\), this implies the stronger **complete-state** conclusion

\[
 \boxed{\|e^{-iH_{g,2}t_g}p-e^{-iz_*t_g}p\|\longrightarrow0.}
 \tag{18}
\]

Indeed, the characteristic functions of the weakly convergent \(\nu_g\) converge uniformly on compact argument sets, so their value at \(s=Cg^4\to0\) tends to one. Unitarity converts survival amplitude tending to one into a norm statement retaining all photon branches. Equation (18) is **not** obtained from the earlier \(t\times O(g^4)\) Duhamel bound, which is insufficient at this duration.

## 7. An asymptotic coherent controlled-Z gate

Let \(Z_L=e^{i\pi n_L}\) be a local phase flip on the left hard-core memory (the photon bath is untouched). Let \(\bar E_g=(E_++E_-)/2\), and define, on the full Hilbert space,

\[
 \mathcal U_g=
 e^{i\bar E_g t_g(n_L+n_R)}
 Z_L e^{-iH_g t_g/2}Z_L e^{-iH_g t_g/2},
 \qquad t_g=\frac{12\pi}{g^4}.
 \tag{19}
\]

The two pulses are applied in physical time order from right to left; the last factor is a known one-memory dynamical phase calibration. The vacuum is fixed. In the single-excitation sector the only two midgap levels are \(E_\pm\), with bare-memory overlap approaching one. The \(Z_L\) pulses reverse the one-body \(\sigma_x\) exchange in the two-dimensional effective memory subspace, so the two halves cancel **at the exact one-body splitting**, with an \(O(g)\) dressed/bare mismatch that is uniform in time.

In the double-excitation sector, (18) applies to each half. Both \(Z_L\) pulses multiply the bare \(|11\rangle\) by \(-1\) and cancel one another. Its remaining conditional phase is

\[
 -\chi_gt_g=\left(\frac{g^4}{12}+o(g^4)\right)\frac{12\pi}{g^4}
 \longrightarrow\pi.
\]

Therefore, if \(P\) embeds the four two-qubit computational basis states with bath vacuum,

\[
 \boxed{\|\mathcal U_gP-P\,\mathrm{CZ}\|\longrightarrow0
 \quad(g\downarrow0).}
 \tag{20}
\]

This is an **inclusive coherent-isometry** statement, valid on arbitrary reference-entangled code inputs; it does not postselect on un-emitted photons. It assumes ideal local phase pulses and exact model parameters. Fixed-duration calibrated positive onsite pulses can approximate these in the weak-coupling limit, but their finite-amplitude implementation and independent noise must be costed separately.

**Timescale and resources.** The proof does **not** supply an effective practical finite-\(g\) error threshold. The interaction time scales as \(g^{-4}\), far longer than the one-excitation iSWAP \(g^{-2}\) scale. Independent memory decay at a fixed nonzero rate eventually overwhelms this weak-coupling asymptotic. **Equal-resource comparator:** the same hardware already supports an entangling iSWAP on the faster \(O(g^{-2})\) timescale; standard compositions of iSWAPs and local single-qubit gates can synthesize a controlled phase. Thus the long-time CZ construction establishes the coherence of an intrinsic fourth-order interaction, **not gate speed or superiority over the faster available control.** The formal golden-rule extrapolation gives \(\Gamma_g t_g\sim(43/432)g^4\), but (17)–(20) do **not** by themselves certify that finite-\(g\) coefficient as the actual loss probability at the shorter timescale.

## 8. Executed checks and decisive failures

The following scripts were executed during this continuation. Each prints or saves an ordinary JSON result; none replaces the infinite-volume proof.

1. `ssh_ranktwo_fock_identity_20261027.py`: directly constructs the physical hard-core two-particle Fock Hamiltonian and compares its resolvent to (3), with maximum observed discrepancy \(2.21\times10^{-12}\) over four complex energies.
2. `ssh_ranktwo_resonance_audit_20261027.py`: derives the exact parity Bloch functions, solves the in-gap one-body poles and evaluates the mixed-band coarea density. The coefficient approaches \(43/(648\pi^2)\).
3. `ssh_ranktwo_full_boundary_20261027.py`: evaluates the *full* one-body measures, including the positive upper pole, and assembles the pair Green function by one-dimensional Stieltjes integration. One-body measure masses differ from one by less than \(4\times10^{-11}\). The corrected amplitude linewidth coefficient approaches \(43/(10368\pi)\), and the connected energy-shift coefficient approaches \(-1/12\).
4. `ssh_cauchy_scaling_test_20261027.py`: independently evaluates the scaled exact interacting Green function at three points in the upper half-plane. The maximum relative deviation from (16) decreases from \(4.18\%\) at \(g=0.25\) to \(1.35\%\) at \(g=0.12\).
5. `generic_two_impurity_interaction_law_20261027.py`: an independent two-mode, parity-symmetric finite bath verifies the generalized connected-shift formula and produces both positive and negative signs.
6. `ssh_echo_onebody_audit_20261027.py`: checks the two-pulse refocusing directly in a full one-body SSH ring, at the much longer time \(12\pi/g^4\). Full-code operator errors for \(g=0.2,0.12,0.08,0.05\) are 0.2427, 0.1965, 0.1085 and 0.0617 respectively, consistent with an \(O(g)\) bare/dressed mismatch. This test is restricted to one excitation; the double-excitation control claim follows instead from the infinite-volume spectral argument.

Selected numerical convergence:

| \(g\) | \((z_*-(E_++E_-))/g^4\) | inferred \(\gamma_g\) | upper-half-plane scaling deviation |
|---:|---:|---:|---:|
| 0.25 | -0.0799730 | 0.00137918 | 4.18% |
| 0.18 | -0.0815638 | 0.00136248 | 2.62% |
| 0.12 | -0.0825394 | 0.00134345 | 1.35% |
| 0.08 | -0.0829790 | 0.00133174 | not tested |
| limit | **-0.0833333** | **0.00132015** | **0%** |

The finite-\(g\) linewidth estimate subtracts the regulator's contribution using the *actual* real slope of \(D_g\), not an assumed slope \(-1\); failing to correct this produces a spurious order-\(g^2\) width error. The original preliminary finite-ring two-photon dynamics at fixed ring size cannot test the \(g^{-8}\) continuum decay law because its discrete level spacing and recurrence time interfere. This failure mode is deliberately not used as supporting evidence.

The continuous density (13) is strictly positive, so a permanent pair state with nonzero overlap with \(p\) cannot be inferred. In the resonance neighborhood, positive continuum spectral weight prevents a real pole of the target Green function, although this does not classify all symmetry sectors or exclude states orthogonal to \(p\).

## 9. Equally informed alternative and next frontier

The strongest alternative is to engineer the emitter/source geometry so the fourth-order **entire on-shell vector** vanishes. For two gradient ports separated by any fixed finite \(d\), the earlier source calculation gives

\[
 \rho_W^{(d)}(6)=\frac1{\pi^2}\int_0^\pi\frac{\sin k[1+\cos^2(dk)]}{(5+4\cos k)^{5/2}}dk>0,
\]

so changing separation alone cannot eliminate the radiative channel. More emitters with independently weighted complex source profiles could alter the rank of the shell coupling; that is a genuinely different construction, not an extension of the two-emitter cancellation already ruled out.

The present route is stronger because it converts the open-channel obstruction into a calculable two-timescale effect: \(g^{-4}\) nonlinear phase and \(g^{-8}\) continuum-resonance broadening. The next substantive attack is either an explicit *finite-\(g\)* error certificate for the echo protocol (requiring uniform estimates stronger than weak convergence), or a radiation-shell rank condition allowing multi-emitter interference to suppress the \(g^8\) coefficient. A physically constrained source geometry and calibrated local pulses remain unacquired.

### External antecedents and novelty boundary

Methods based on few-photon Green functions, hard-core scattering \(T\)-matrices and Fermi-golden-rule spectral limits are established; relevant starting points include *Green's function approach to interacting lattice polaritons and optical nonlinearities in subwavelength arrays of quantum emitters*, Physical Review Research 6, 043264 (2024), and Faupin–Møller–Skibsted, *Second order perturbation theory for embedded eigenvalues* (arXiv:1006.5869). This note claims no external historical priority, no real device and no improvement over equally resourced experimental gates. The constructive value lies in the exact model-specific finite-rank reduction, coefficient calculation and coherent echo consequence.
