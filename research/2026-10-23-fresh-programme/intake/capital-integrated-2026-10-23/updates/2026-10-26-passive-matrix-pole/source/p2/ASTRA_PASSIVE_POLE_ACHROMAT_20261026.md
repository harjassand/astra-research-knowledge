# ASTRA foundational physics — passive spectral-response hierarchy and correlated-memory scattering

26 October 2026. Continuation of the bosonic impurity / coherent scattering route. This is a **mathematical construction in an explicitly declared finite-band Hamiltonian**, with exact algebraic proofs and separately executed interval / matrix checks. No original-physics priority, material platform, practical quantum advantage or experimental device is claimed. Every bandwidth is a stationary, asymptotic one-photon scattering bandwidth, not a finite-duration optical pulse protocol. Energies are in units of a fixed memory binding scale \(B=1\); \(\hbar=1\).

## Scope and comparison with the incumbent

The earlier incumbent proved a pair-to-all-particle spectral bound for an inverse-square continuum impurity and a separate three-particle first-forbidden-sector certificate. Its **homogeneous single-impurity capacity-two theorem remains open**. The later dark-port and pairwise-memory alternative trades a single highly nonlinear oscillator for \(m\) hard-core memory sites and a conditional Fano-emitter scattering resonance. An earlier two-output-port construction with 10% *constant spectral-intensity* imbalance and static complex hopping had a conservative, independently executed continuous error certificate below 1% on \([1.465,1.535]\), requiring off-target shift \(\chi=260\).

Two comparators were considered here: (A) continue with that fixed pair of hopping controls only, where the selected real detuning and unwanted output amplitude generally have quadratic errors; (B) introduce positive-energy auxiliary oscillators, recognizing both their causal Stieltjes dispersion and their occupation / detuning costs. Route B permits cubic-flattened selected response, and with one **shared rank-one auxiliary** permits cubic loss conversion as well. It is the stronger live construction, despite raising the required off-target emitter-frequency shift to \(1300\). These are model-specific tradeoffs, not proof of an engineering advantage.

## 1. Exact one-body source Hamiltonian and all-sector realization

Let \(m\) two-level memory sites have \(n_j\in\{0,1\}\) and total charge \(K=\sum_j n_j\). Two two-level signal emitters have a one-excitation internal space \(\mathbb C^2_e\). Add two independent **positive-energy bosonic side modes** at \(\Omega_s\), one per emitter, and one shared positive-energy bosonic side mode at \(\Omega_x\), with coupling vector \(g\in\mathbb C^2_e\). The two photon ports are independent \(L^2((0,2),d\omega)\) continua, both retained in the physical output state. Put

\[
U_\tau(\omega)=\frac1{\sqrt2}
\begin{pmatrix}1&1\\-e^{i\tau\omega}&e^{i\tau\omega}\end{pmatrix},\qquad
V(\omega)=\sqrt\gamma\,\omega U_\tau(\omega)
\begin{pmatrix}1&0\\0&\sqrt{1+\eta}\end{pmatrix}.
\]

A 10% intensity imbalance is \(\eta=0.1\). The first port is the intended incident photon, the second the unwanted-but-**included** output. A phase \(e^{i\tau\omega}\) can be identified with separation along ideal linearly dispersing chiral waveguides, but the exact two-port sign pattern, dispersion, independent controls and absence of additional channels remain **assumed physical interfaces**, not an acquired apparatus.

For frozen memory charge \(K=k\), with \(\Delta_k=\chi(m-k)I_2\), the one-excitation signal operator is the ordinary block Fano Hamiltonian on
\(\mathbb C_e^2\oplus\mathbb C_s^2\oplus\mathbb C_x\oplus L^2((0,2);\mathbb C^2)\):

\[
h_k=\begin{pmatrix}
\epsilon I_2+\gamma\eta\widetilde H+\Delta_k&\sqrt r I_2&g&V\\
\sqrt r I_2&\Omega_sI_2&0&0\\
g^\dagger&0&\Omega_x&0\\
V^\dagger&0&0&M_\omega
\end{pmatrix}.\tag{1}
\]

Here \(\widetilde H=\begin{psmallmatrix}c&x+iy\\x-iy&c\end{psmallmatrix}\). The full number-conserving signal Hamiltonian consists of free photon and auxiliary-boson energies, emitter number terms, rotating-wave couplings and the matrix-valued two-emitter coupling \(\gamma\eta\widetilde H\), with **hard-core emitter occupations**. It is precisely the compression of \(d\Gamma(h_k)\) to that emitter-hard-core Fock subspace; the auxiliary oscillators and photon ports are not truncated. In a one-excitation sector the compression is inactive, so (1) directly governs scattering.

A single controller shift \(\chi(m-K)I_2\) is compatible with *any* memory Hamiltonian commuting with total \(K\). Independent site-conditioned noncommuting shifts \(\sum_j(1-n_j)A_j\), \(A_j\succeq\chi I_2\), also work **when the site occupations are frozen**. They generally **do not commute** with an XY-interacting memory, and the two interfaces must not be conflated.

Let \(P_\ell(\omega)=|U_\tau(\omega)e_2\rangle\langle U_\tau(\omega)e_2|\), and define
\[
A(E)=2+2E+E^2\log\frac{2-E}{E},\quad a(E)=\pi\gamma E^2,
\quad \overline M(E)=\operatorname{PV}\int_0^2\frac{\omega^2P_\ell(\omega)}{\omega-E}\,d\omega.
\]

The *exact* limiting resolvent denominator after eliminating the baths and side modes is

\[
D_k(E)=\left[E-\epsilon+\gamma A(E)+\frac r{\Omega_s-E}+ia(E)\right]I_2
-\gamma\eta\widetilde H-\Delta_k
+\gamma\eta[\overline M(E)+i\pi E^2P_\ell(E)]
+\frac{gg^\dagger}{\Omega_x-E}.\tag{2}
\]

For \(E\in(0,2)\) away from the explicit auxiliary poles, the loss-inclusive one-photon scattering matrix is

\[
S_k(E)=I_2-2\pi iV(E)^\dagger D_k(E)^{-1}V(E).\tag{3}
\]

The imaginary part of \(D_k\) is exactly \(\pi V(E)V(E)^\dagger\succ0\), so (3) is unitary on both physical ports. No postselection is performed. Exact 5-by-5 internal-matrix inversion independently reproduced (3) through Schur elimination to better than \(1.4\times10^{-15}\) in the executed scan.

## 2. Stationary loss-conversion geometry

Write \(u(E)=U_\tau(E)e_1\), \(\ell(E)=U_\tau(E)e_2\). Two real functions expose the causal bath response:

\[
F(E)=\frac12\int_0^2\omega^2\frac{\sin[\tau(\omega-E)]}{\omega-E}\,d\omega,
\quad
J(E)=\frac12\int_0^2\omega^2\frac{1-\cos[\tau(\omega-E)]}{\omega-E}\,d\omega.\tag{4}
\]

These integrals have no singularity at \(\omega=E\); all apparent singularities are removable. Exactly, \(u^\dagger\overline Mu=J\), \(\ell^\dagger\overline Mu=iF\), \(u^\dagger H_{\rm off}u=-x\cos(\tau E)+y\sin(\tau E)\), and \(\ell^\dagger H_{\rm off}u=-i[x\sin(\tau E)+y\cos(\tau E)]\), for \(H_{\rm off}=\widetilde H-cI\).

Set \(E_0=3/2\), \(t=E-E_0\), \(\tau=37/10\), \(d_s=\Omega_s-E_0\), \(d_x=\Omega_x-E_0\). The shared side mode is chosen with

\[
g=\sqrt{\gamma\bar a}\,(1,e^{i\phi})^T,
\qquad \phi=\tau E_0-\frac\pi2,
\qquad \bar a=\eta\,[F''(E_0)+\tau^2F(E_0)]\,\frac{d_x^3}{2}.\tag{5}
\]

Its positive rank-one residue satisfies
\(\ell^\dagger gg^\dagger u=i\gamma\bar a\sin(\phi-\tau E)=-i\gamma\bar a\cos(\tau t)\), while \(u^\dagger gg^\dagger u=\gamma\bar a[1+\sin(\tau t)]\). Thus the real coefficient \(b(E)\) of the cross-port entry \(\ell^\dagger D_m u=i b(E)\) is

\[
b(E)=\gamma\left\{\eta[F(E)+x\sin(\tau E)+y\cos(\tau E)]-
\bar a\frac{\cos(\tau t)}{d_x-t}\right\}.\tag{6}
\]

Choose static hopping quadratures by solving two *exact* linear equations:

\[
\begin{aligned}
h_0&=-F(E_0)+\frac{\bar a}{\eta d_x},\qquad
h_1=-\frac{F'(E_0)}\tau+\frac{\bar a}{\eta\tau d_x^2},\\
x&=h_0\sin(\tau E_0)+h_1\cos(\tau E_0),\\
y&=h_0\cos(\tau E_0)-h_1\sin(\tau E_0).
\end{aligned}\tag{7}
\]

They imply \(b(E_0)=b'(E_0)=0\). Applying \((\partial_E^2+\tau^2)\) to (6) cancels both static sine/cosine terms. At the center, \(\sin(\phi-\tau E_0)=-1\) and \(\cos(\phi-\tau E_0)=0\), hence

\[
\frac{b''(E_0)+\tau^2b(E_0)}\gamma
=\eta[F''(E_0)+\tau^2F(E_0)]-\frac{2\bar a}{d_x^3}=0.
\]

**Exact result:** \(b(E_0)=b'(E_0)=b''(E_0)=0\). The **scalar** side oscillators could not have canceled this quadratic cross-port conversion, since they add only scalar functions to \(D_k\). A single positive, rank-one **non-scalar** auxiliary residue supplies the missing control direction. This is an algebraic result, not a three-frequency interpolation.

The earlier scalar-resonator-only case has a nonzero \(b''(E_0)=\gamma\eta [F''(E_0)+\tau^2F(E_0)]\), with bracket \(37.49741855\ldots>0\) at \(\tau=3.7\). Thus a new control *geometry*, not merely additional scalar poles, is necessary to eliminate the second-order port conversion in that fixed model.

## 3. Cubic-flat selected phase, with positive controls

Let \(H_{uu}(E)=-x\cos(\tau E)+y\sin(\tau E)\), set \(c=J(E_0)-H_{uu}(E_0)\), and define

\[
T(E)=J(E)-H_{uu}(E)-c,\qquad
P(E)=\frac{1+\sin[\tau(E-E_0)]}{d_x-(E-E_0)}.
\]

The target-port real diagonal is exactly

\[
q(E)=E-\epsilon+\gamma[A(E)+\eta T(E)+\bar aP(E)]
+\frac r{d_s-(E-E_0)}.\tag{8}
\]

Define \(L_1= [A+\eta T+\bar aP]'(E_0)\), \(L_2=[A+\eta T+\bar aP]''(E_0)\). Set

\[
\gamma=\frac1{-L_1+(d_s/2)L_2},\qquad
r=-\gamma\frac{L_2d_s^3}{2},\qquad
\epsilon=E_0+\gamma A(E_0)+r/d_s+\gamma\bar a/d_x.\tag{9}
\]

For \(d_s=d_x=7/20=0.35\), the denominators are positive and the physical residues \(\gamma,r,\gamma\bar a\) are all **strictly positive**. Equation (9) forces \(q(E_0)=q'(E_0)=q''(E_0)=0\) exactly. Combining with (6) establishes **cubic-order real resonance detuning and cubic-order unwanted-port amplitude**. It does *not* assert that the total scattering phase is perfectly constant on an arbitrarily wide band.

The evaluated dimensionless controls (digits are displays, not their defining values) are

| Control | Value |
|---|---:|
| spectral delay \(\tau\) | 3.7 |
| unwanted-port spectral intensity excess \(\eta\) | 0.1 |
| scalar and rank-one side-mode frequencies \(\Omega_s=\Omega_x\) | 1.85 |
| \(\gamma\) | 0.4230478082531 |
| scalar side-mode coupling squared \(r\) | 0.1809703562380 |
| rank-one side-mode coupling squared **per emitter** \(\gamma\bar a\) | 0.0340067365695 |
| emitter bare energy \(\epsilon\) | 3.1837368845374 |
| hopping \(x+iy\) | \(2.04547324979+0.00647256856i\) |
| diagonal hopping/bias addition \(c\) | 1.84789411307 |
| minimum omitted-memory occupation shift \(\chi\) | 1300 |

The strong \(\chi\) is a resource. For \(m\) memory sites the total global emitter bias span can grow as \(1300m\), as in the preceding pairwise frequency-selector architecture. Nothing here bounds a hardware's permissible frequency span or nonlinear dispersive shift.

## 4. Complete continuous-band wavepacket certificate

For any real \(E\in[1.4,1.6]\), put \(a(E)=\pi\gamma E^2\). In the **instantaneous port basis** the dissipative part of \(D_m\) is diagonal, \(a(E)\operatorname{diag}(1,1+\eta)\). Therefore \(\|D_m(E)^{-1}\|\le1/a(E)\). The exact resolvent identity gives

\[
\boxed{\|S_m(E)e_w+e_w\|\le
\frac{2\sqrt{1+\eta}\sqrt{q(E)^2+b(E)^2}}{\pi\gamma E^2}.}\tag{10}
\]

For any memory record with at least one unoccupied memory site, its positive, possibly noncommuting emitter shift obeys \(\Delta\succeq\chi I\). On the same band, the Hermitian real portion of the target denominator has norm below 3, giving

\[
\boxed{\|S_{\rm not-full}(E)-I_2\|
\le\frac{2\pi\gamma(1+\eta)E^2}{\chi-3}.}\tag{11}
\]

The interval proof does **not** simply sample 1,001 photon frequencies. All occurrences of \(F,J\) and their derivatives are evaluated through absolutely convergent, *rational* sine/cosine series integrated against polynomial moments \(\int_0^2\omega^2(\omega-E)^p d\omega\), which have explicit rational antiderivatives. The scalar \(A\) uses the rational artanh series

\[
\log\frac{2-E}{E}=2\sum_{j\ge0}\frac{(1-E)^{2j+1}}{2j+1}.
\]

All tails are enclosed by explicit positive geometric bounds. On the **whole** interval, elementary product/derivative inequalities prove \(|q^{(4)}|<7864\) and \(|b^{(4)}|<2127\). Exact rational enclosures of \(q'''\) and \(b'''\) at 201 rational centers spaced by 0.001, **plus** their fourth-derivative Lipschitz bounds over the half-spacing 0.0005, yield the interval-wide statements

\[
q'''(E)>7.28766,\qquad b'''(E)<-1.46894.
\]

Since both functions and their first two derivatives vanish at the center, \(q(E)\) is monotonically increasing through zero and \(b(E)\) monotonically decreasing through zero. On each of 40 rational subintervals, the maximum of \(\sqrt{q^2+b^2}\) is thus bounded by the endpoint farther from the center, and \(a(E)\) is bounded below by its left-endpoint value. All 40 rational inequalities are strictly below the error target; the highest proves

\[
\boxed{\sup_{E\in[1.4,1.6]}\|S_m(E)e_w+e_w\|<0.009884406.}\tag{12}
\]

With \(\chi=1300\), Eq. (11) also gives

\[
\boxed{\sup_{E\in[1.4,1.6]}\|S_{\rm not-full}(E)-I_2\|<0.005773469.}\tag{13}
\]

Consequently, the physical, **loss-inclusive** asymptotic scattering operation approximates a conditional photon sign in operator norm on *every normalized one-photon wavepacket whose spectral support lies in the stated interval*, including arbitrary untouched quantum references. No survival conditioning enters either bound. The sign acts on the photon channel when all memory sites are occupied and is approximately identity otherwise, relative to the free memory evolution. If a memory Hamiltonian exchanges sites without conserving each \(n_j\), the collective shift \(\chi(m-K)I\) must be used as explained in Section 6.

Independent matrix evaluation of the complete **5-by-5 internal resolvent** on 1,001 photon frequencies gives selected error 0.0093474812, unselected error 0.0052344342, unwanted-port amplitude at most 0.00069873 and scattering unitarity residual below \(4.7\times10^{-15}\). These independent grids are diagnostics, not substitutes for the interval certificate.

## 5. Actual all-particle bound survives the auxiliaries and both continua

Integrating the free field and **positive** bosonic side modes at energy zero yields the Schur complement of the full one-body energy form:

\[
C=\epsilon I+\gamma\eta\widetilde H+\Delta_k
-\int_0^2\frac{V(\omega)V(\omega)^\dagger}{\omega}\,d\omega
-\frac r{\Omega_s}I-\frac{gg^\dagger}{\Omega_x}.
\]

Since \(U(\omega)U(\omega)^\dagger=I\),
\(\int VV^\dagger/\omega=2\gamma I+\gamma\eta\int_0^2\omega P_\ell(\omega)d\omega\). Use \(\|\widetilde H\|<4\), \(\|\int\omega P_\ell\|\le2\), \(\|gg^\dagger\|=2\gamma\bar a\). The exact rational interval enclosures for the controls prove

\[
\boxed{C\succeq1.9492\,I_2>0\quad\text{for all}\ \Delta_k\succeq0.}\tag{14}
\]

This is a positive **Schur-complement/energy-form margin**, *not* a spectral gap above the global ground energy: the continuum is gapless. It proves \(h_k\ge0\), hence its second quantization is nonnegative in every boson number. Restricting the two emitter occupations to 0 or 1 cannot make a nonnegative form negative.

For independent memory qubits with \(H_{\rm mem}=-K\), this directly implies for every finite total excitation sector \(N\)

\[
\boxed{\inf\sigma(H_N)=-\min(N,m).}\tag{15}
\]

For \(N\le m\), fill any \(N\) memory qubits, leaving emitter, side modes and photon fields in vacuum: this is an exact eigenstate with energy \(-N\). For \(N>m\), fill all \(m\) memory qubits and add \(N-m\) arbitrarily soft photons. The expectation tends to \(-m\). This threshold is a dissociation threshold, not an additional many-particle bound eigenstate.

### Entangled interacting-memory extension with no hidden XY incompatibility

On any weighted graph of memory sites, define the strictly two-body, total-charge-conserving, positive exchange-Laplacian

\[
T=\sum_{\{i,j\}}J_{ij}
(|10\rangle-|01\rangle)_{ij}
(\langle10|-\langle01|)_{ij},\qquad J_{ij}\ge0,
\quad H_{\rm mem}=-K+T.\tag{16}
\]

\(T\ge0\) and \([T,K]=0\). In each charge sector \(k\), the equal-amplitude Dicke state \(|D_{m,k}\rangle\) is annihilated by *every* edge term, so its exact energy is \(-k\). For \(1\le k<m\), Dicke states on a connected graph are generally **entangled** (not product storage states). The emitter shift \(\chi(m-K)I\) commutes with all these interactions, so the complete photon scattering acts on the memory as \(\bigoplus_kS_k(E)\otimes I_{K=k}\) relative to its independent free evolution. Both (12)-(13) and (15) remain valid. The result does **not** justify arbitrary heterogeneous site-dependent \(A_j\) together with XY hopping; those usually fail the required commutation relation.

The accompanying exact spin-sector numerical audit covered 30 sectors for graphs with \(3\le m\le7\): the Dicke-null residual was at most \(2.50\times10^{-16}\). A six-site, three-excitation Dicke state had \(1.46899559\) bits of entanglement across a 3|3 partition. These finite audits illustrate the direct operator proof.

## 6. Two no-go results and why the rank-one auxiliary matters

### The lower-complexity scalar alternative

If only scalar passive side modes are allowed, write their energy corrections as \(\sum_j r_j/(\Omega_j-E)\) with \(r_j>0\), \(d_j=\Omega_j-E_0\ne0\). Once the static two-quadrature hopping has canceled cross-port conversion at the center and through first order, let \(L=A+\eta T\). At \(E_0\), its exact coefficients obey \(L_1=L'(E_0)\approx-6.512066\) and \(L_2=L''(E_0)\approx-26.132338\). For \(q'=q''=0\) the auxiliary moments must obey

\[
\sum_j\frac{r_j}{d_j^2}=\gamma|L_1|-1,\qquad
\sum_j\frac{r_j}{d_j^3}=\gamma|L_2|/2.\tag{17}
\]

**In-band-pole requirement.** If every side resonance lies outside \((E_0,2)\), then \(d_j<0\) or \(d_j\ge1/2\), and termwise \(d_j^{-2}\ge\tfrac12d_j^{-3}\). Equation (17) would require \(|L_1|>|L_2|/4\). Exact interval bounds instead give \(|L_1|<6.52<26.13/4<|L_2|/4\). Contradiction. Hence at least one passive scalar auxiliary resonance **must lie within the upper part of the photon band**, \(1.5<\Omega_j<2\), in this particular fixed-envelope / static-hop model.

**No fourth-order detuning flattening by positive scalar poles.** Cauchy–Schwarz implies
\(
(\sum_jr_j/d_j^3)^2\le(\sum_jr_j/d_j^2)(\sum_jr_j/d_j^4)
\). Using (17):

\[
q'''(E_0)\ge\gamma L'''(E_0)
+\frac{3\gamma^2L_2^2}{2(\gamma|L_1|-1)}
>\gamma\left[L'''(E_0)+\frac{3L_2^2}{2|L_1|}\right].\tag{18}
\]

Using the exact integral derivative bound \(|T'''|<249\), the rightmost bracket is \(>46.85\), so \(q'''(E_0)>0\) for *every* number of scalar positive-residue side modes. Thus those passive modes can make \(q,q',q''\) vanish, but cannot also make \(q'''\) vanish. The obstruction holds for this fixed spectral density, fixed phase frame and scalar auxiliary class; matrix-valued auxiliaries and other spectral densities are not excluded.

Even an infinite number of scalar side modes cannot cancel the unrelated \(b''(E_0)\ne0\), since they contribute only multiples of the identity in emitter space. The shared rank-one mode in Section 2 **does** add a cross-port self-energy, so this second limitation is evaded rather than contradicted. The new model's \(b''=0\) is not an all-band zero-loss theorem.

### An exact limitation that remains

The two-port baths already represent all radiation in the model. Additional independent emitter emission/dephasing or uncontrolled waveguide backscattering creates extra channels not present in (1). The prior single-resonance loss-rank obstruction gave full-state error \(2\sqrt\eta\) for an independently leaking port of branching fraction \(\eta\) at perfect resonance. Introducing positive passive auxiliaries does not remove that separate independent-channel risk. Hardware calibration, spontaneous emission, pulse injection and extraction, actuator slew, mode matching, realization of the signed/complex hopping, physical photon timing, and large \(m\chi\) emitter-bias range are not supplied. The earlier Jacobi endpoint-only interface is still a different and unacquired physical operation.

## 7. Reproducible executed evidence and assumptions

All files are in the current `/mnt/data` workspace. The following are ordinary executable source and result files, *not* externally verified publications:

- `astra_passive_pole_rational_certificate_20261026.py` / `.json`: independent two-scalar-auxiliary interval certificate, \(w=.08\), stationary 10%-imbalance loss conversion, all-N positivity, necessary in-band pole, impossibility of quartic selected detuning with scalar positive poles.
- `astra_passive_pole_full_hamiltonian_audit_20261026.py` / `.json`: direct 4-by-4 internal scattering matrix, independent analytic self-energy versus off-axis complex quadrature (residual \(1.14\times10^{-15}\)), positive finite-quadrature matrices, noncommuting site-conditioned shift probes, and side-mode frequency-drift scans.
- `astra_rankone_crosspole_cubic_20261026.py` / `.json`: physically positive shared cross-pole construction, exact algebraic zero jets, direct **5-by-5** one-photon matrix and positivity checks. Gridded maximum errors are explicitly noncertifying diagnostics.
- `astra_rankone_crosspole_interval_certificate_20261026.py` / `.json`: **full continuous-band rational** certificate for \(w=.10\), with 201 rational derivative centers and proved fourth-derivative variation envelopes, plus 40 exact subinterval operator-error inequalities. This is the governing proof for (12)-(14).
- `astra_charge_laplacian_entangled_memory_20261026.py` / `.json`: fixed-excitation graph-Laplacian verification with entangled Dicke null states. The all-\(N\) statement comes from the direct positive-form argument, not from sampling those finite matrices.

Important related prior work includes Shi, Wu, González-Tudela and Cirac, *Phys. Rev. X* **6**, 021027 (2016), DOI 10.1103/PhysRevX.6.021027 (few-body impurity interactions); Heeres et al., *Phys. Rev. Lett.* **115**, 137002 (2015), DOI 10.1103/PhysRevLett.115.137002 (number-selective phases); and modern frequency-dependent electromagnetic-reservoir cautions such as Gustin, Ren and Hughes, *Phys. Rev. Lett.* **134**, 123601 (2025), DOI 10.1103/PhysRevLett.134.123601. These antecedents mean the current construction should **not** be described as the invention of conditional quantum phases, Fano interference or positive second-quantized Hamiltonians. Historical novelty and experimental value remain unestablished.

## Scientific conclusion and strongest remaining attack

This continuation proves a coherent composition, in one actual declared Hamiltonian, of (i) gapless all-particle saturation with multiple interacting-memory states, (ii) pairwise memory-emitter selection, (iii) non-Markovian two-port radiation with 10% intensity imbalance, (iv) **passive auxiliary-resonator cancellation of phase and loss-conversion jets through second order**, and (v) a loss-inclusive wavepacket error below 1% across the certified \([1.4,1.6]\) interval, valid for any number of memory sites and arbitrary untouched references. The cost is a severe fixed per-missing-excitation frequency shift and more controllable resonators.

The strongest physically consequential next step is to derive an implementation of the frequency-delayed sign-pattern couplings, complex static hopping, one shared positive mode, and collective \(\chi(m-K)\) shift from **one** restricted microscopic platform; then include independently measured radiative channels and finite-time source/detection dynamics. The rank-one shared-mode control should be challenged against a realistic three-dimensional free-space waveguide or multi-directional waveguide model, where extra channels are expected and the exact two-port cancellation is not automatic. In parallel, the homogeneous Jacobi single-impurity capacity-two theorem remains open and should not be identified with the separate pairwise memory construction.

## 8. Continuation beyond the certificate: spatial-delay mismatch is a real resource

The specific frequency-dependent frame \(U_\tau(\omega)\) admits a microscopic *idealized chiral-waveguide* reading: emitter 1 couples at position 0 to two propagating ports; emitter 2 couples at the same distance \(L\) from emitter 1 on each, with relative opposite coupling sign, and \(\tau=L/v\) for linear dispersion. This converts an abstract frequency-domain unitary into a definite **spatial matching condition**. It still assumes equal port delays, prescribed spectral envelopes, chiral directionality, and no additional radiative modes.

Challenge this matching by making the second emitter's wanted and loss port delays \(\tau_w=\tau\), \(\tau_\ell=\tau+\delta\tau\), with all controls fixed at their original calibration. The *actual* form-factor matrix becomes

\[
V_{\delta\tau}(\omega)=\frac{\sqrt\gamma\,\omega}{\sqrt2}
\begin{pmatrix}1&\sqrt{1+\eta}\\
-e^{i\tau\omega}&\sqrt{1+\eta}\,e^{i(\tau+\delta\tau)\omega}
\end{pmatrix}.\tag{19}
\]

Its off-diagonal spectral density acquires the additional term

\[
(V_{\delta\tau}V_{\delta\tau}^\dagger)_{12}
=\frac{\gamma\omega^2e^{-i\tau\omega}}2
\left[-1+(1+\eta)e^{-i\delta\tau\omega}\right].\tag{20}
\]

It is no longer the originally calibrated spectral matrix. By uniqueness of the Stieltjes transform, no constant Hermitian hopping adjustment can make its **entire off-axis self-energy** equal to the old one (nor scalar across an open domain where the spectral density itself is non-scalar). A static counterterm may still repair an individual photon frequency, so this is *not* a universal no-go for frequency-local recalibration or additional active controls.

`astra_waveguide_delay_mismatch_20261026.py` evaluates the exact two-port on-shell self-energy using independent analytic sine/cosine-integral formulas for \(\tau_w\) and \(\tau_\ell\), and confirms the original 5-mode resolvent at \(\delta\tau=0\) through matrix identities. With **no retuning**, the selected full-output error maximum over a diagnostic 201-frequency grid changes from \(0.00934748\) to \(0.01014668\) at \(\delta\tau=0.0005\), \(0.0263222\) at \(\delta\tau=0.01\), and \(0.0956770\) at \(\delta\tau=0.05\) in inverse-binding-energy delay units. Every two-port scattering matrix remains unitary to \(5\times10^{-15}\). These are **numerical sensitivity diagnostics**, not rigorous uniform-in-frequency tolerances. They establish that the *specific unretuned* control settings can fail a 1% goal under small geometrical mismatch. They do not exclude compensated or reoptimized designs, nor do they show that an actual fabrication process could achieve the required matching.

This failure materially changes the next physical attack: the most relevant comparison is now with a **single local chiral-waveguide model including its actual spatial Green functions and independently leaking radiation channels**, rather than with a formal spectral-frame optimization that assumes perfectly matched delays. A next-stage mechanism would need an adjustable geometry or dynamical control able to recover the center and derivative conditions after independent delay/loss characterization, without expanding the already large frequency-shift budget beyond an achievable range.
