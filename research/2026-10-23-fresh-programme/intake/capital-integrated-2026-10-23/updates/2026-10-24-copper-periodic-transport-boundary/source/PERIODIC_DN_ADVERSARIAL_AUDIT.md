# Adversarial audit of the periodic diffusion/DN checkpoint

## Verdict

The signs in the displaced-interface boundary condition and in the code's diffusion Dirichlet-to-Neumann maps are internally consistent. A global galvanostatic constraint does not suppress a nonzero transverse Fourier mode at first order: its spatial mean is zero, so it may redistribute local current while preserving total current. The checkpoint is nevertheless conditional on a strong reaction/electrical closure: $A=r/c_s$ is the derivative of the chosen first-order irreversible Tafel rate at fixed local overpotential, and the ionic-potential perturbation at $k\ne0$ is set to zero. A metal electrode's equipotential condition and global current control do not imply that liquid-side potential perturbation vanishes.

The finite-film periodic computation is a fixed-domain, small-Ω, slow-interface-per-cycle calculation. It is not a full moving-boundary Floquet result, an optimization over waveforms, or a prediction for the Schneider bath. The admissible promotion is the controlled mathematical statement and its numerical fixture signs only. The physical morphology, any useful-flux consequence, and a pulse advantage remain unestablished pending bath-matched measurements of Cu-specific flux, concentration, potential, flow, and geometry.

## Boundary signs and DN maps

Take $z$ positive from the metal into the liquid; $r>0$ means Cu deposition consumes dissolved Cu²⁺, and the flat base has $D C_z(0,t)=r(t)>0$. A positive graph displacement $h e^{ikx}$ moves the boundary into the liquid. To first order, the concentration sampled at the displaced boundary is

\[
\delta c_s=w(0,t)+C_z(0,t)h,
\]

and the normal concentration derivative is

\[
\delta(D\partial_n c)=D\bigl(w_z(0,t)+C_{zz}(0,t)h\bigr).
\]

There is no first-order slope term from the normal vector because the base has no lateral gradient. With $\delta r=A\delta c_s-Bk^2h$, $A>0,B\ge0$, this gives

\[
D(w_z+C_{zz}h)=A(w+C_zh)-Bk^2h.
\]

For a quasistatic mode $w_z=-kw$, $C_z=g$, and $q=C_{zz}$, algebra yields

\[
w(0)=-\frac{Ag-Bk^2-Dq}{A+Dk}h,
\qquad
\frac{\dot h}{h}=\Omega\frac{Dk(Ag-Bk^2)+ADq}{A+Dk}.
\]

Thus the $+ADq$ term in the numerator is the correct displaced-gradient contribution under this sign convention. For the frozen steady base $q=0$, replacing $Dk$ by the exponential-mode admittance $K(s)=D\sqrt{k^2+s/D}$ gives

\[
s=\Omega(Ag-Bk^2)\frac{K(s)}{A+K(s)}.
\]

For $d=Ag-Bk^2>0$, $s>0$. Since $d\le Ag$, $s\le\Omega gK(s)=(V/D)K(s)$, with $V=\Omega r=\Omega Dg$. Setting $x=s/(Dk^2)$ and $\Pi_k=V/(Dk)$ gives $x\le\Pi_k\sqrt{1+x}$, hence

\[
0\le x\le \frac{\Pi_k^2}{2}+\Pi_k\sqrt{1+\frac{\Pi_k^2}{4}}=:E,
\qquad
1\le\frac{s}{s_{\rm QS}}\le\sqrt{1+E}.
\]

This verifies the local frozen-eigenvalue bound. It says nothing comparable about arbitrary initial-condition gains, finite-time non-normal growth, a time-varying base stability problem, or a complete periodic Floquet exponent.

For the finite layer in `periodic_dn_check.py`, the top boundary is fixed Dirichlet data $w(L)=0$. With time harmonic $e^{im\omega t}$, the decaying/anchored vertical solution has $q_m=\sqrt{k^2+im\omega/D}$, and the positive admittance is

\[
K_m=Dq_m\coth(q_mL),
\qquad
Z_m=\frac{\tanh(q_mL)}{Dq_m}
\]

for the nonzero-mode lateral and $k=0$ base maps, respectively. The code uses $-Z_1\delta r$ for the base surface-concentration response, which is the correct sign for a consuming flux, and solves the periodic Robin equation with the full $K_m$, not $Dk$. With its held-fixed $h$, the mean displaced term contributes ⟨$C_{zz}h$⟩ $=0$ over a periodic cycle. Its mean reaction/mean DN-flux identity is therefore the right fixed-film identity. These checks do not certify spatially varying conductivity, liquid-side potential, or motion of the top boundary.

## Galvanostatic constraint and the potential closure

On a periodic lateral domain, a $k\ne0$ Fourier current perturbation has zero integral:

\[
\delta I_{\rm Cu}^{(1)}\propto\int_0^{L_x}\delta r_k e^{ikx}\,dx=0.
\]

So fixed total current permits a nonzero local $\delta r_k$; it constrains the $k=0$ component, not the amplitude of a zero-mean mode. At first order in height, a graph's area element is unchanged, so using projected area for the global constraint is consistent for a linear mode. A uniform metal-potential correction likewise lives in the $k=0$ sector at first order. At second order in height, local current redistribution and true area can change total current, and a globally galvanostatic experiment must adjust its uniform potential/base current. The leading linear mode calculation is not that finite-amplitude charge closure.

The missing liquid-potential perturbation is different. A general local kinetic law gives

\[
\delta r=A\,\delta c_s+G_\eta(\delta\phi_m-\delta\phi_s)-Bk^2h,
\qquad G_\eta=\left.\frac{\partial r}{\partial\eta}\right|_0.
\]

Even with an equipotential metal, $\delta\phi_m$ has no nonzero spatial Fourier component; conductivity/current conservation and the perturbed geometry can nevertheless produce $\delta\phi_s(k)\ne0$. The code drops that term. For its concentration contribution to dominate under Tafel kinetics, one needs a bound such as

\[
\frac{\alpha nF}{RT}c_s|\delta\phi_s|\ll|\delta c_s|,
\]

or a directly solved electrical subproblem showing that its induced δr is negligible relative to $A\delta c_s$ and $Bk^2h$. A highly conducting support may help, but neither global galvanostatic control nor metal equipotentiality supplies this bound by itself. In a CuSO₄/H₂SO₄ bath the Cu²⁺, H⁺ and sulfate transport and the solution potential are coupled; a bath-specific transport/electrical model or measurement is needed before interpreting the sign as a copper-deposit prediction.

The assumed $A=r/c_s$ follows exactly from the restricted closure $r=k_0c_s\exp(\alpha nF\eta/RT)$ when η is fixed and the reverse Butler–Volmer branch is negligible. It is not a generic derivative of Butler–Volmer kinetics. It also presumes first order in Cu²⁺ activity, no concentration-dependent transfer coefficient, no local pH/speciation or additive state, and a measured Cu partial flux (r), not merely total electrical current. The capillary coefficient $B=\alpha\Gamma_{\rm cap}r$ is consistent only if the equilibrium-potential shift is $\gamma\Omega\kappa/(nF)$, $\Gamma_{\rm cap}=\gamma\Omega/(RT)$, and curvature is the only additional interfacial-state term. Those choices are valid model assumptions, not bath-matched facts.

## Interface motion, area, and charge/mass order

The Taylor term $C_{zz}h$ correctly accounts for evaluating the diffusive flux on the displaced boundary to first order in $h$, while the code holds $h$ fixed during each fast period. It does **not** by itself impose the species jump condition for a moving Cu/solution boundary. If liquid solvent is stagnant in the laboratory frame, the Cu balance with metal molar density $c_M=1/\Omega$ is

\[
D\partial_n C=(c_M-c_s)v_n
=r(1-\Omega c_s),
\qquad v_n=\Omega r.
\]

The model instead uses $D\partial_n C=r$, which is a leading-order approximation in $\Omega c_s$ for stagnant solvent. With liquid normal velocity $u_n$, this jump convention gives $D\partial_n C=r+(u_n-v_n)c_s$; $u_n=v_n$ recovers the simpler relation. For the 0.1 M CuSO₄ bath mentioned in the construction, using $\Omega_{\rm Cu}\approx7.1\times10^{-6}$ m³ mol⁻¹ gives $\Omega c_{\infty}\approx7.1\times10^{-4}$; this is small, but it is not automatically below a predicted ε² waveform correction. It must be compared on the same dimensionless gain scale, especially for the long-mode fixtures with small correction. The finite-film spectral fixture is not calibrated to that bath, so this estimate is only an order check.

For a graph interface, $dA/dA_{\rm proj}=\sqrt{1+|\nabla h|^2}=1+O(|\nabla h|^2)$. Thus projected versus true area is harmless in the linear $h\to0$ mode calculation, but not in a finite roughness/charge comparison. Total Cu charge and mass must be computed on the actual surface:

\[
Q_{\rm Cu}=\int\!\int_{\Gamma(t)}j_{\rm Cu}\,dA\,dt,
\qquad
\Delta m_{\rm Cu}=\frac{M_{\rm Cu}}{2F}Q_{\rm Cu}.
\]

The imposed model waveform $r(t)$ is the Cu molar flux per projected area of the flat base. It is not automatically the measured total current divided by $2F$ in a rough experimental cell. A mass/charge claim additionally needs Cu Faradaic efficiency; an interface envelope $h(x,t)$ gives Cu volume only if density/porosity is established. The small-Ω calculation reports linear shape gain, not an equal-mass experiment.

"Leading Ω" and "fixed $h$ within a cycle" require slow shape evolution relative to the forcing, schematically μ/ω ≪ 1 for the mode growth rate μ. A full periodic Floquet problem would retain the evolving $h(t)$ in the boundary displacement, couple it to the base concentration and any uniform galvanostatic adjustment, and account for moving-domain transport. The current script deliberately does not do that. Its spectral convergence and small-modulation coefficient checks validate only the stated periodic, fixed-film linearized problem.

## Strongest physical obstruction and promotion boundary

The sharpest obstacle is not the algebra: it is that the control variable and kinetic/electrical closure are not identified for the physical bath. The model controls Cu molar flux directly, fixes liquid potential perturbations to zero, and gives Cu²⁺ a scalar Fickian diffusion field. A real CuSO₄/H₂SO₄ plating experiment controls total current; the Cu partial current, local solution-potential perturbation, multicomponent migration, convection, and local interfacial kinetics are not determined by that control alone. The source packet gives no measured Cu²⁺ field or Fourier-mode wavelength with which to calibrate $D$, $L$, $A$, $B$, or $\omega/(Dk^2)$. The selected liquid-cell morphology result also does not supply this missing parameter and observability map. Without those measurements, the computed negative long-mode and positive shorter-mode harmonic coefficients are signs of the reduced model only, not practical pulse benefit or a compact/protruding morphology prediction.

The statement that survives is: **within the specified fixed-film, diffusion-only, first-order irreversible-Tafel and zero-liquid-potential-perturbation model, with the interface frozen over each forcing cycle and $\Omega c_s\ll1$, the spectral equations have the reported periodic gain corrections; separately, the frozen steady exponential eigenvalue obeys the stated $\Pi_k$ bound.** No claim about full CuSO₄/H₂SO₄ dynamics or a useful-flux advantage can be promoted without bath-matched local potential/current/concentration/flow/morphology measurements and an area/mass balance.
