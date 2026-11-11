# P2 available return — 12 November 2026 Brisbane

Source: https://chatgpt.com/c/6af4793b-ffe8-83ec-a7ab-863459a8d78d, Pro. Final 61dd49db-c8e2-56fd-9cf1-acd01b741f41, answering user 72d8891f-26a1-4548-8ded-b21e0c431095. Exact actual question is held at `P2_FULL_NATIVE_LOCAL_PROCESSOR_AFTER_NONLINEAR_PORT_KERNEL_PRO_20261112.txt` (posted with one approved terminal LF omitted).

## Available visible activity

Previously observed while generating, verbatim:

> A concrete transport improvement has emerged: adding a nominal viscous correction to the shear pulse removes the order-one endpoint residual identified in your premise. Unknown viscosity then leaves an error proportional to the fixed uncertainty width. I’m checking its scope in the coupled equations and whether it helps with recurrent cleanup.

> The conservation check exposes a limitation of the proposed renewal estimate: a uniform contraction of the complete physical error would have to damp arbitrarily long wavelength velocity perturbations in one fixed period. That conflicts with momentum conservation as the domain grows. It does not obstruct the processor itself, but it points toward treating slow flow separately from the code errors that need rapid correction.

Additional expanded activity and helper contents were not captured. Original archive availability and identity are unknown; none collected. No attachment was listed in the native thread.

## Full response copied from the UI

**I have not completed the full native architecture, and I have not found an obstruction covering every allowed architecture.** The accepted interfaces still do not justify an affirmative answer to your full question.

There is, however, a concrete physical advance beyond the auxiliary operators: **the corridor translation can be implemented by a fixed, finite, rational mechanical force in the coupled MHD equations, with an error bound in each cell that is uniform in capacity.** This gives a controlled transfer step for arbitrary material words. It does not yet give a restoring Boolean processor.

I also obtain two estimates for the actual nonlinear faulty evolution and a restriction on the proposed renewal strategy:

| Result | What it establishes | What remains outside its scope |
|---|---|---|
| Mechanically implemented neighbor transfer | A fixed force moves compact magnetic codelets between cells and returns velocity close to zero, under the admitted coefficient uncertainty | Recurrent computation, copying, restoration and recovery from large fault clusters |
| Nonlinear damage estimate over one fixed step | A bound on total field damage and damaged port decisions, covering every fault cluster and every energy weak realization | A spatial or causal joint-error law over repeated updates |
| Finite-horizon resource tail | A probability bound for energy excursions, dissipation and absolute kick work, including failed runs | Uniform-in-time energy density and the required absolute mechanical-work bound |
| Conservation restriction | Uniform strict contraction of the complete physical error cannot serve as a capacity-independent reset | It does not exclude correction of logical data while accommodating slow flow |

Below I give the constructions and estimates, including the points where they stop.

## 1. A mechanically implemented local transfer step

Write \(\sigma\) for the duration of this step, reserving \(T\) for the eventual architecture period. All parameters in this section are chosen once. None depends on the programme, capacity, runtime or requested reliability.

Fix a finite family of sufficiently regular, compactly supported, divergence-free magnetic codelets. Arrange their supports in transverse lanes so that a selected channel can move while idle channels remain in place. Choose coordinate directions \(j,l\) with
\[
l\ne j,\qquad l\ne1.
\]
The second restriction preserves the constant bias \(H_*=e_1\).

The result has the following form. For sufficiently small fixed parameters,
\[
\boxed{
\sup_i
\left\|
\left(
u(\sigma),\,
B(\sigma)-B_{\mathrm{shift}}
\right)
\right\|_{H^1(Q_i)}
\le
C\left(
E_{\mathrm{in}}+\zeta+
\delta_{\mathrm{spec}}+
\delta_{\mathrm{shape}}+\sigma
\right).
}
\tag{1}
\]
Here \(B_{\mathrm{shift}}\) is the neighboring-cell translation of the selected channel, with the other channels unchanged. The constant \(C\) is independent of \(M\), the material word and the actual coefficient histories.

This is a **fault-free reference-step theorem**. It does not assert that a cell follows this estimate whenever only its own clock is quiet. Faults elsewhere in the connected fluid must still be accounted for.

### 1.1 The rational force

Choose a fixed smooth, \(a\)-periodic scalar function \(v_0(x_l)\) satisfying:

- \(v_0=1\) on the transverse supports of the travelling codelets;
- \(v_0=0\) on the transverse supports of idle codelets;
- a negative part in empty lanes makes its spatial mean zero.

Such a profile can be specified by fixed rational piecewise-polynomial cutoffs at a sufficiently high regularity. Approximate it by a finite trigonometric polynomial \(v\) with rational Fourier amplitudes, zero mean, and
\[
\|v-v_0\|_{C^6}\le\delta_{\mathrm{shape}}.
\]
The approximation uses only fixed, explicitly described functions and derivative bounds.

Set
\[
V(x)=v(x_l)e_j,
\qquad
U(s)=6s(1-s).
\]
Thus
\[
U(0)=U(1)=0,\qquad \int_0^1U(s)\,ds=1.
\]

The intended velocity is
\[
w(t,x)=\frac a\sigma U(t/\sigma)V(x).
\tag{2}
\]
It is solenoidal, has zero mean, and satisfies
\[
(w\cdot\nabla)w=0.
\]

The nominal viscous correction is essential. Applying only \(w_t\) as force leaves the endpoint residual described in your premise. Instead, use
\[
f_\sigma(t,x)
=
\frac a{\sigma^2}U'(t/\sigma)V(x)
-
\frac a\sigma U(t/\sigma)D_V(x),
\tag{3}
\]
where \(D_V\) is a rational Fourier approximation to \(\Delta V\), on the same fixed Fourier support, with
\[
\|D_V-\Delta V\|_{H^1_{\mathrm{uloc}}}
+\|D_V-\Delta V\|_{C^1}
\le\delta_{\mathrm{spec}}.
\tag{4}
\]

This last approximation is necessary for the binary contract: the exact Laplacian multipliers contain \((2\pi n/a)^2\), so they cannot simply be entered as rational coefficients. There are only finitely many such known numbers, and fixed rational approximations suffice.

For rational \(a,\sigma\), every temporal coefficient in (3) is an ordinary rational polynomial. The force is solenoidal and \(a\)-periodic. Its catalogue is fixed.

The discrepancy between the prescribed force and the intended shear obeys
\[
w_t-\nu(t)\Delta w-f_\sigma
=
\frac a\sigma U(t/\sigma)
\bigl(D_V-\nu(t)\Delta V\bigr),
\]
hence
\[
\|w_t-\nu\Delta w-f_\sigma\|_{H^1_{\mathrm{uloc}}}
\le
C\frac{\zeta+\delta_{\mathrm{spec}}}{\sigma}.
\tag{5}
\]
Its time integral is \(O(\zeta+\delta_{\mathrm{spec}})\). Shortening the pulse therefore does not leave an order-one viscous residue.

The force can be large:
\[
\|f_\sigma\|_{W^{1,\infty}}
\le C(\sigma^{-2}+\sigma^{-1}).
\]
But \(\sigma\) is fixed at architecture design time, so this is a fixed physical cost, independent of device capacity.

### 1.2 The magnetic reference and the coupled residual

Let
\[
F(s)=\int_0^sU(r)\,dr.
\]
The flow of \(w\) is explicit:
\[
\Phi_t(x)
=
x+aF(t/\sigma)v(x_l)e_j,
\]
with
\[
D\Phi_t
=
I+aF(t/\sigma)v'(x_l)e_j\otimes e_l.
\tag{6}
\]
Since \(l\ne1\),
\[
D\Phi_t e_1=e_1.
\]

For an arbitrary material word \(\alpha\), define the ideal induction reference by
\[
C(t,\Phi_t(x))
=
D\Phi_t(x)B_\alpha(x).
\tag{7}
\]
It satisfies
\[
C_t+(w\cdot\nabla)C-(C\cdot\nabla)w=0.
\tag{8}
\]

For the exact plateau profile \(v_0\), travelling codelets translate by precisely \(ae_j\), without deformation; idle codelets stay fixed. The finite Fourier approximation gives
\[
\sup_i
\|C(\sigma)-B_{\mathrm{shift}}\|_{H^1(Q_i)}
\le C\delta_{\mathrm{shape}}.
\tag{9}
\]

This reference is used only in the proof. It is not an imposed velocity or magnetic control. Its residual in the full equations is
\[
r_u
=
\frac a\sigma U(t/\sigma)(D_V-\nu\Delta V)
-\mathbb P[(C\cdot\nabla)C],
\]
\[
r_B=-\rho\Delta C.
\tag{10}
\]
Consequently,
\[
\|(r_u,r_B)\|_{H^1_{\mathrm{uloc}}}
\le
C\left(
\frac{\zeta+\delta_{\mathrm{spec}}}{\sigma}+1
\right).
\tag{11}
\]

In particular, magnetic diffusion and Lorentz backreaction have both been retained. Their integrated contribution is \(O(\sigma)\), because the required fixed spatial norms of \(C\) remain bounded.

Those bounds hold for every material word. The shear has bounded displacement and bounded spatial derivatives independent of \(\sigma\), so a local region receives contributions from only a fixed number of initial cells. No periodic-cell or zero-Bloch-sector assumption enters.

### 1.3 Local stability without a capacity factor

Put
\[
e_u=u-w,\qquad e_B=B-C.
\]
Use fixed overlapping cutoffs \(\psi_i\), equal to one on \(Q_i\), supported in fixed cell enlargements. Let \(E_i\) denote the corresponding localized joint \(H^1\) error energy, and \(D_i\) its dissipation, including second spatial derivatives. Define
\[
\mathcal F(t)=\sup_i\sup_{s\le t}E_i(s),
\qquad
\mathcal D(t)=\sup_i\int_0^tD_i(s)\,ds.
\]

The pressure estimate must be included here. Its error stress consists of
\[
w\otimes e_u+e_u\otimes w+e_u\otimes e_u
-C\otimes e_B-e_B\otimes C-e_B\otimes e_B.
\]
The near part is bounded by local elliptic estimates. The far part uses the actual \(D^3G_L\) kernel and the summable \(r^{-4}\) tail.

When a differentiated momentum equation is tested against
\(\psi_i\partial_r e_u\), the pressure contribution becomes
\[
\int \partial_r\pi\,
\nabla\psi_i\cdot\partial_r e_u.
\tag{12}
\]
Thus it does not require a second derivative of the pressure. In particular, the large reference shear contributes a coefficient \(C/\sigma\), whose integral over the pulse is fixed, rather than a spurious \(C/\sigma^2\).

The nonlinear terms satisfy estimates of the form
\[
\text{local nonlinear terms}
\le
\varepsilon_0
\sum_{j\in\mathcal N(i)}D_j
+
C_{\varepsilon_0}(\mathcal F+\mathcal F^3),
\tag{13}
\]
where \(\mathcal N(i)\) has fixed cardinality. For example,
\[
\|\nabla e\|_3^3
\le
C\mathcal F^{3/4}
(D_{\mathrm{near}}+\mathcal F)^{3/4}
\]
is absorbed by local dissipation and \(C(\mathcal F+\mathcal F^3)\).

After integrating each local inequality, taking the supremum costs only the fixed overlap number:
\[
\varepsilon_0\sup_i
\sum_{j\in\mathcal N(i)}
\int_0^tD_j
\le
\varepsilon_0 C_{\mathrm{ov}}\mathcal D(t).
\]
Choosing \(\varepsilon_0\) first absorbs this term. No estimate of
\(\int_0^t\sup_iD_i(s)\,ds\) is needed.

The resulting inequality is
\[
\begin{aligned}
\mathcal F(t)+c\mathcal D(t)
\le {}&
C\mathcal F(0)
+
C\int_0^t
\bigl[(1+\sigma^{-1})\mathcal F(s)+\mathcal F(s)^3\bigr]\,ds\\
&+
C(\zeta+\delta_{\mathrm{spec}})^2t/\sigma
+C\sigma t.
\end{aligned}
\tag{14}
\]
For \(0\le t\le\sigma\), a fixed-radius bootstrap gives
\[
\mathcal F(t)
\le
C\left[
\mathcal F(0)+
(\zeta+\delta_{\mathrm{spec}})^2+\sigma^2
\right].
\tag{15}
\]
Together with \(w(\sigma)=0\) and (9), this proves (1).

For each finite torus, this estimate continues the strong solution from the actual incoming \(H^1\) state through the step. Weak–strong uniqueness then identifies every energy-admissible weak realization with it during that step. This does not require a general global regularity theorem.

### 1.4 Preparation and the actual clock

The literal cellwise \(H^1(Q_i)\) preparation condition may allow tangential jumps across cell faces. It still gives a uniformly local \(L^6\) bound.

A fixed rational unforced prefix of duration \(d_0>0\) handles that case. Periodized heat and differentiated Stokes kernels give the uniformly local estimate
\[
\|e^{A_\nu(t,s)\Delta}\mathbb P\operatorname{div}F\|_{L^6_{\mathrm{uloc}}}
\le
C(t-s)^{-3/4}\|F\|_{L^3_{\mathrm{uloc}}},
\]
where
\[
A_\nu(t,s)=\int_s^t\nu(r)\,dr.
\]
The coupled mild construction uses separate heat clocks for \(\nu\) and \(\rho\). At the end of the prefix,
\[
\sup_i
\|(u(d_0),B(d_0)-B_\alpha)\|_{H^1(Q_i)}
\le
C\left(\gamma d_0^{-1/2}+\sqrt{d_0}\right).
\tag{16}
\]

Choose \(d_0\) first, then choose the fixed preparation tolerance \(\gamma\). The complete step takes the actual time \(d_0+\sigma\). Nothing is removed from the physical clock.

Uniformly local mild-solution methods for viscous resistive MHD have a primary precedent in Kang–Lai–Lai–Tsai, Theorem 2.10. That theorem concerns the half space; the torus and coefficient-history estimates here use the displayed periodized kernels and actual heat clocks. It is not a native processor theorem. [arxiv.org](https://arxiv.org/html/2407.07001v1?utm_source=chatgpt.com)

### 1.5 Why this is still only a transfer primitive

The endpoint estimate is
\[
E_{\mathrm{out}}\le C E_{\mathrm{in}}+\delta_{\mathrm{fixed}}.
\]
It is not a restoring contraction.

Indeed, even in the linear Stokes sector, repeatedly applying nominally compensated pulses at \(\nu\ne1\) can accumulate endpoint velocity error to order \(\zeta/\sigma\). The one-step result therefore cannot be promoted silently to recurrent cleanup.

It establishes a physically implemented transfer operation and a controlled reference family. **COPY, Boolean evaluation, canonical reshaping and recurrent garbage removal remain unconstructed.**

## 2. Actual nonlinear damage over one fixed step

There is a useful estimate that does cover arbitrarily large fault clusters, without requiring the damaged path to remain strong.

Let \(z^*=(u^*,B^*)\) be a smooth reference on a fixed interval \([0,h]\), with the same force and actual coefficient histories. Assume capacity-independent bounds
\[
A=\sup_{t\le h}
\bigl(\|u^*(t)\|_\infty+\|B^*(t)\|_\infty\bigr),
\]
\[
\Gamma=\int_0^h
\bigl(\|\nabla u^*(t)\|_\infty+
      \|\nabla B^*(t)\|_\infty\bigr)\,dt.
\]
The transfer construction above supplies such reference bounds for exact smooth incoming codewords.

Let \(e=z-z^*\), and let \(K_h\) be the actual total number of clock rings in this interval, including rings with zero marks. Then
\[
\boxed{
\sup_{t\le h}\|e(t)\|_1
\le
C_h\left(
\|e(0)\|_1+\|e(0)\|_2^2+
K_h+K_h^2
\right).
}
\tag{17}
\]
The constant is independent of \(M\), the mark directions and the weak realization.

### 2.1 The differentiated Stokes kernel is integrable in space

On \(\mathbb R^3\), writing \(H_s\) for the heat kernel,
\[
\nabla e^{s\Delta}\mathbb P
=
\nabla H_s I+\int_s^\infty\nabla^3H_r\,dr
\]
with the corresponding tensor indices. Hence
\[
\|\nabla e^{s\Delta}\mathbb P\|_{L^1}
\le
Cs^{-1/2}
+
C\int_s^\infty r^{-3/2}\,dr
\le Cs^{-1/2}.
\tag{18}
\]
Periodization preserves this upper bound uniformly in torus size. Substituting the actual heat clocks gives the same estimate for the non-autonomous diffusion.

The difference of the MHD fluxes satisfies
\[
|R(z)-R(z^*)|
\le CA|e|+C|e|^2.
\]
The weak mild identity therefore yields
\[
\begin{aligned}
\|e(t)\|_1
\le {}&
\|e(0)\|_1+C_aK_0K_h\\
&+
C\int_0^t(t-s)^{-1/2}
\left(A\|e(s)\|_1+\|e(s)\|_2^2\right)\,ds.
\end{aligned}
\tag{19}
\]

This identity uses only the distributional equations, the global energy class and the explicitly declared jumps. It does not assume a local energy inequality for the damaged solution.

### 2.2 Relative energy closes the finite-step estimate

Global relative energy against the smooth reference, with the triangle inequality at each jump, gives
\[
\sup_{t\le h}\|e(t)\|_2
\le
e^{C\Gamma}
\left(\|e(0)\|_2+K_0K_h\right).
\tag{20}
\]
Applying the order-\(1/2\) Volterra Grönwall estimate to (19) proves (17).

All constants may be large for a fast reference pulse. They remain fixed architecture constants; there is no capacity factor hidden in them.

For fixed bounded local probes with bounded overlap,
\[
\sum_i|\langle e(t),\phi_i\rangle|
\le C_\phi\|e(t)\|_1.
\]
If a bad output decision requires a probe discrepancy at least \(\beta>0\), then, from clean initial data,
\[
\boxed{
\#\{\text{bad port decisions in this step}\}
\le C_{\beta,h}(K_h+K_h^2).
}
\tag{21}
\]

This is an actual nonlinear damage-count estimate. It includes every large cluster.

### 2.3 Centering gives an expected defect density

For clean initial data relative to the reference, conditional centering removes the relative-energy jump cross term. Thus
\[
\mathbb E\|e(t)\|_2^2
\le C_h(p/T)M^3t.
\]
Taking expectations in (19) gives, for fixed \(h/T\),
\[
\sup_{t\le h}\mathbb E\|e(t)\|_1
\le C_h pM^3.
\]
Consequently,
\[
\boxed{
\mathbb E\#\{\text{bad port decisions}\}
\le C_h pM^3.
}
\tag{22}
\]

This does **not** imply the joint-error condition required by a threshold theorem. An average defective fraction of order \(p\) is compatible, as a probability statement, with an event of probability \(p\) on which every site is defective. Equation (22) alone does not exclude such correlations.

Nor can (21) be inserted into the accepted weighted-count lemma: \(K_h\) counts rings throughout the whole device. Assigning unit weight to all those rings would violate the capacity-independent row-sum requirement.

This is also where the all-weak quantifier matters. For example, the weighted MHD weak–strong theorem of Fernández-Dalgo–Jarrín explicitly assumes suitable local energy relations with nonnegative defect measures. It cannot simply be applied to every globally energy-admissible weak realization in your contract. The argument above avoids that substitution. [arxiv.org](https://arxiv.org/pdf/2002.10531?utm_source=chatgpt.com)

## 3. A restriction on complete physical-error renewal

There is a genuine conservation obstruction to an especially strong implementation of premise 7.

Let \(L=aM\), \(V=L^3\), and consider a controlled smooth reference on a fixed interval \([0,h]\), with uniformly bounded energy density and integrated spatial gradients. Use the admitted zero-mark law.

Perturb only the initial velocity:
\[
e_u(0,x)=\delta\psi_L(x),
\qquad
e_B(0,x)=0,
\]
where
\[
\psi_L(x)=e_2\sin(2\pi x_3/L).
\tag{23}
\]
This perturbation is solenoidal, has zero mean and satisfies the local preparation condition for sufficiently small fixed \(\delta\).

Relative energy gives
\[
\sup_{t\le h}\|e(t)\|_2
\le C_h\delta\sqrt V.
\]
Test the difference momentum equation against \(\psi_L\). The common force cancels. The viscous term carries \(L^{-2}\); the stress term carries \(L^{-1}\). The constant magnetic bias has no linear contribution for this transverse test.

Since
\[
V^{-1}\|R(z)-R(z^*)\|_1\le C_h\delta,
\]
we obtain
\[
\frac1V
\left|
\langle e_u(h),\psi_L\rangle
-\langle e_u(0),\psi_L\rangle
\right|
\le C_h\frac{\delta}{L}.
\tag{24}
\]
But
\[
V^{-1}\langle e_u(0),\psi_L\rangle=\delta/2.
\]
Therefore
\[
\boxed{
\frac{\|e(h)\|_2}{\|e(0)\|_2}
\ge 1-\frac{C_h}{L}.
}
\tag{25}
\]

No fixed \(\lambda<1\) can consequently satisfy
\[
\|e(h)\|_2\le\lambda\|e(0)\|_2
\]
for complete physical error at every capacity.

A cellwise linear renewal map with both Schur sums bounded by \(\lambda<1\) would imply such a contraction in the corresponding summed \(L^2\) norm. Repeated contraction in a uniformly equivalent complete-error norm runs into the same obstruction.

There is also a direct physical-time version. For
\[
q(t)=V^{-1}\langle u(t),e_2\sin(kx_3)\rangle,
\qquad k=2\pi/L,
\]
the fixed \(a\)-periodic force has no coefficient at this frequency, and
\[
q'
=
-\nu(t)k^2q+
\frac{k}{V}
\int_{\Omega_M}(u_2u_3-b_2b_3)\cos(kx_3)\,dx.
\tag{26}
\]
A bounded energy density therefore limits the rate of change of this mode to \(O(k)\). Changing its amplitude by a fixed amount requires time of order \(L\). With the contract’s expected energy bound, the analogous statement applies to its expected amplitude.

**This is not an obstruction to the requested processor.** A processor may tolerate slow flow, include it in a family of references, or reserve a deterministic error floor. Logical correction need not erase every long wavelength velocity perturbation.

What it rules out is using uniform strict contraction as an indiscriminate reset of the entire physical state. A workable renewal theorem must account explicitly for the slow sector or otherwise avoid that stronger requirement.

## 4. A finite-horizon tail for the full resource ledger

The accepted expected-energy calculation can be strengthened to a tail estimate without assuming bounded local gradients or excluding clusters.

Use post-jump states at observations, and include all jumps with \(s\le t\). Set
\[
E(t)=\frac12\left(\|u(t)\|_2^2+\|B(t)-H_*\|_2^2\right),
\]
\[
D(t)=\nu(t)\|\nabla u(t)\|_2^2+
\rho(t)\|\nabla B(t)\|_2^2,
\qquad
\lambda=p/T.
\]
For this lemma, any fixed upper bound on \(p\), such as \(p\le1\), suffices. It does not construct a computational threshold.

There is a fixed computable constant \(C\) such that, for every \(t\ge0\) and \(0<\delta<1\),
\[
\boxed{
\begin{aligned}
\mathbb P\Bigg[
&\sup_{s\le t}
\left(E(s)+\frac12\int_0^sD(r)\,dr\right)
+W_{\mathrm{kick}}(t)\\
&\qquad >
C\left(V(1+t)+1+\log^2\frac{2}{\delta}\right)
\Bigg]
\le\delta.
\end{aligned}
}
\tag{27}
\]

This concerns the actual uninterrupted evolution, including failed computations. The stopping used below is only a proof device.

### 4.1 Quadratic variation is controlled by dissipation

Write \(b=B-H_*\), \(z=(u,b)\), and let
\[
J_s=\langle z(s-),\xi_s\rangle+
\frac12\|\xi_s\|_2^2
\]
be the energy increment at a fault.

Conditional centering gives
\[
\mathbb E[J_s\mid\mathcal F_{s-},i,s]
=
\frac12\mathbb E[\|\xi_s\|_2^2\mid\mathcal F_{s-},i,s]
\le K_0^2/2.
\]

Choose enlarged cubes \(D_i\) of side \(3a\). They have overlap at most \(27\), and local Poincaré can be used with constant \(3a\). Zero integral of each kick gives
\[
|\langle z,\xi_i\rangle|
\le
3aK_0
\left(
\|\nabla u\|_{L^2(D_i)}^2+
\|\nabla b\|_{L^2(D_i)}^2
\right)^{1/2}.
\]
Thus, with the fixed rational bound
\[
\kappa=\frac{243a^2K_0^2}{1-\zeta},
\]
\[
\sum_i
\mathbb E[\langle z,\xi_i\rangle^2\mid\mathcal F_{s-}]
\le\kappa D(s).
\tag{28}
\]

Let \(\mathscr M\) be the compensated martingale formed from the jumps \(J_s\). Its predictable quadratic variation satisfies
\[
d\langle\mathscr M\rangle_s
\le
\lambda\left(
2\kappa D(s)+\frac12M^3K_0^4
\right)\,ds.
\tag{29}
\]
There is no additional factor of volume multiplying \(D(s)\).

### 4.2 Stop a majorant whose jumps are explicit

From the fixed force catalogue, compute a rational \(C_f\) such that
\[
\langle f_*,u\rangle\le\frac12D+C_fV.
\]
Define
\[
Y_s=E(0)+C_fVs+\sum_{r\le s}J_r.
\]
The actual energy inequality gives
\[
E(s)+\frac12\int_0^sD(r)\,dr\le Y_s.
\tag{30}
\]
The process \(Y\) is explicitly right-continuous with left limits, even when no stronger energy continuity is assumed for the weak solution.

Put
\[
F_t=E(0)+
\left(C_fV+\frac12\lambda M^3K_0^2\right)t.
\]
Then \(Y_s\le F_t+\mathscr M_s\) for \(s\le t\).

Stop at the first time \(Y\) reaches a level \(B>F_t\). Before that time,
\[
E(s-)\le B,\qquad \int_0^sD(r)\,dr\le2B.
\]
The stopped martingale jumps are bounded by
\[
b_B=K_0\sqrt{2B}+\frac12K_0^2,
\]
and its quadratic variation is bounded by
\[
v_B(t)=4\lambda\kappa B+
\frac12\lambda M^3K_0^4t.
\]

The compensated-Poisson exponential estimate then gives
\[
\boxed{
\mathbb P\!\left[\sup_{s\le t}Y_s\ge B\right]
\le
\exp\!\left(
-\frac{(B-F_t)^2}
{2\left(v_B(t)+b_B(B-F_t)/3\right)}
\right).
}
\tag{31}
\]
The crossing jump is included in \(b_B\). Its overshoot does not add to the time-integrated dissipation appearing in \(v_B\).

For \(B\ge C V(1+t)+1\), the right side is at most
\[
e^{-c\sqrt B}
\]
with fixed computable constants.

### 4.3 Absolute kick work has the same tail scale

The absolute cost of a kick is
\[
A_i=
|\langle u,\xi_u\rangle|
+
|\langle b,\xi_B\rangle|
+
\frac12\|\xi\|_2^2.
\]
The bias contributes zero, so this equals the requested cost written with \(B\).

Its compensated martingale has the same stopped jump and quadratic-variation bounds. Its compensator rate is bounded by
\[
\lambda\sqrt{\kappa M^3}\sqrt D+
\frac12\lambda M^3K_0^2
\le
D+
\left(\frac{\lambda^2\kappa}{4}
+\frac{\lambda K_0^2}{2}\right)M^3.
\tag{32}
\]
On the event that \(Y\) has not crossed \(B\), this compensator integrates to \(CB\). A second exponential estimate and a union bound prove (27).

Every ring is counted. Neither adaptive mark directions nor rare high-count clusters are removed.

### 4.4 The remaining energy gap is unchanged

Equation (27) is a stronger finite-horizon certificate, but its energy allowance still grows with physical time. It cannot be used to choose a local gate envelope depending on \(J\), because that would violate the fixed-architecture requirement.

The missing estimate remains
\[
\sup_{t\ge0}\mathbb E E(t)\le CV.
\]
If that estimate were available, the absolute prescribed-drive work would follow:
\[
\begin{aligned}
\mathbb E\int_0^t\int|f_*\cdot u|
&\le
\int_0^t
\|f_*(s)\|_2
\bigl(\mathbb E\|u(s)\|_2^2\bigr)^{1/2}\,ds\\
&\le CVt.
\end{aligned}
\tag{33}
\]
The signed work estimate alone still does not prove (33).

## 5. What prevents these results from answering the full question

The remaining construction is now more specific, but it remains substantial.

First, a fixed mechanically driven module must **evaluate and restore local data**, including extraction, copying, Boolean operations, canonical reshaping and velocity/buffer renewal. The transfer step above does not implement those operations. The auxiliary scalar reshaper remains an auxiliary map.

Second, one needs a **spatial or causal nonlinear fault theorem over repeated updates**. The finite-step \(L^1\) estimate and the expected defect density do not provide it. References must be renewed relative to the actual incoming decoded word; otherwise a valid flipped bit would be counted as a defective update forever. Large damaged regions must be included without assuming that every damaged trajectory stays strong.

Third, the architecture needs a **bulk-energy mechanism** that controls failed runs uniformly in time. High-moment probes and logical correctness cannot substitute for that estimate. The conservation calculation also shows why a proof should not presume rapid contraction of every physical mode.

Classical reliable cellular computation can be used only after the physical error law is matched. For example, Gács–Reif give an explicit three-dimensional rule with repetition encoding, but their perturbation hypothesis bounds the probability that every update in an arbitrary prescribed set fails. An \(O(p)\) average defect density is insufficient. Their stated pointwise guarantee also must be connected carefully to the requested decoder and simultaneous correctness at all observation times. [cs-web.bu.edu](https://cs-web.bu.edu/faculty/gacs/papers/Gacs-Reif88.pdf?utm_source=chatgpt.com)

Accordingly, I cannot yet supply a justified fixed catalogue \(f_*\), native restoring alphabet and rule, encoder, decoder, positive computational threshold \(p_0\), and complete resource certificate satisfying your contract. Nor do the conservation and energy arguments above exclude all permitted architectures.

**The constructive advance is an actual coupled-MHD neighbor-transfer primitive with local, capacity-independent control. The unresolved work is native recurrent computation, nonlinear fault containment and uniform long-time bulk energy.**