# Constitutive scope: fixed Eulerian anisotropic conduction vs convected axes

## Direct answer

The layer equation in `ELASTIC_INTERFACE.txt`,

\[
k_n u''-k_tq^2u=0,
\]

is internally consistent if it is declared as a **current-configuration Eulerian Ohmic law**: in the instantaneous spatial coordinates \(x\) (tangent) and \(y\) (normal), set
\(\mathbf i=-\mathbf K_E\nabla\phi\), \(\mathbf K_E=\mathrm{diag}(k_t,k_n)\), with positive \(k_t,k_n\) fixed in the spatial basis and independent of strain, stress, concentration, and deformation. Quasistatic charge conservation \(\nabla\cdot\mathbf i=0\), linearized about a flat base \(\phi_0(y)\) and a Fourier perturbation \(\delta\phi=u(y)e^{iqx}\), gives the stated ODE. This is a valid phenomenological constitutive choice for the bulk operator; it does not remove moving-boundary corrections to interface conditions. It is not by itself a material-frame law for an anisotropic solid whose texture rotates with the body.

Let material principal axes rotate counter-clockwise by a small angle \(\theta\), with \(\mathbf K_E=\mathbf R(\theta)\mathrm{diag}(k_t,k_n)\mathbf R(\theta)^T\). Then

\[
\delta K_{xy}=\delta K_{yx}=(k_t-k_n)\theta,\qquad
\delta K_{xx}=\delta K_{yy}=0+O(\theta^2).
\]

For a small displacement field \(\mathbf w=(w_x,w_y)\), the convected in-plane rotation is \(\theta=(\partial_xw_y-\partial_yw_x)/2\).

\[
\nabla\cdot\bigl(\mathbf K_0\nabla\delta\phi+\delta\mathbf K\nabla\phi_0\bigr)=0.
\]

For \(\theta=\theta_q(y)e^{iqx}\) and a normal base field, the Fourier ODE therefore gains the first-order source

\[
k_nu''-k_tq^2u+iq(k_t-k_n)\theta_q(y)\phi'_0(y)=0.
\]

A strain-dependent normal conductivity adds \(\partial_y(\delta K_{yy}\phi'_0)\); concentration-, stress-, or porosity-dependent coefficients add their corresponding divergence terms. Pure rotation contributes the off-diagonal term above, not a first-order change to the principal eigenvalues.

Equivalently, if one starts from a fixed **referential** conductivity matrix \(\mathbf K_R\), rather than a fixed Eulerian tensor, the standard current/reference pullback gives \(\mathbf K_E=J^{-1}\mathbf F\mathbf K_R\mathbf F^T\). For \(\mathbf F=\mathbf I+\mathbf H\),

\[
\delta\mathbf K_E=\mathbf H\mathbf K_R+\mathbf K_R\mathbf H^T-(\mathrm{tr}\,\mathbf H)\mathbf K_R.
\]

Writing \(\mathbf H=\boldsymbol\epsilon+\boldsymbol\Omega\) separates rotation \(\boldsymbol\Omega\mathbf K_R-\mathbf K_R\boldsymbol\Omega\) from the first-order stretch/area terms \(\boldsymbol\epsilon\mathbf K_R+\mathbf K_R\boldsymbol\epsilon-(\mathrm{tr}\,\boldsymbol\epsilon)\mathbf K_R\). A reference-frame formulation therefore does not reduce to a fixed spatial diagonal tensor under arbitrary deformation. The fixed Eulerian model remains valid if this is the declared constitutive assumption and its axes are physically fixed or the model intentionally neglects their advection.

## Closest primary continuum precedent and its limit

Bistri & Di Leo, “A continuum electro-chemo-mechanical gradient theory coupled with damage: Application to Li-metal filament growth in all-solid-state batteries,” *Journal of the Mechanics and Physics of Solids* 174 (2023), 105252, DOI [10.1016/j.jmps.2023.105252](https://doi.org/10.1016/j.jmps.2023.105252); full primary text: [arXiv:2302.06462](https://arxiv.org/abs/2302.06462). The source formulates finite-strain kinematics and stress balance (\(\mathbf F=\mathbf F^e\mathbf F^c\), Eqs. 6.1 and 6.5), derives a free-energy electrochemical potential, and imposes ionic flux linear in its gradient through a positive-semidefinite mobility tensor (Eqs. 5.6–5.12). Its LLZO specialization uses isotropic concentration/phase-dependent mobility \(\mathbf j_R=-m(c,\bar\xi)\nabla\mu^e\) (Eq. 7.30); the stress term enters the deposition reaction driving force. The authors explicitly do not model stripping in that specialization (line 634). This is a primary continuum **model**, not a measurement of the Li3N film in the frozen interface proposal. It shows that strain, chemical potential, mobility, and reaction coupling are constitutive choices; it neither supplies nor experimentally validates the proposed fixed diagonal anisotropic Ohmic tensor.

The existing `ELASTIC_INTERFACE.txt` says no same-film in-plane conductivity tensor, Young modulus, or signed prestress for the Li3N film was acquired. I did not reopen the Li2018 paper in this bounded check; that same-film evidence gap remains as recorded. Likewise, the source above does not certify the film’s unstressed-isotropic plane-strain Airy solution. For that interface, the clean statement is: the ODE is exact under the declared Eulerian conductivity assumption, while material-convected anisotropy, stress-coupled electrochemical potentials, and finite-deformation geometry are separate corrections/gates, not algebraic contradictions of the stated model.
