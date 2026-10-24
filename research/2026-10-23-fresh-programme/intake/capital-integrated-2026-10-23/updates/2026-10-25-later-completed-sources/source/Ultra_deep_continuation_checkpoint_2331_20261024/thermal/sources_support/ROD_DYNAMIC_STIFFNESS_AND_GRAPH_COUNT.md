# Uniform-rod dynamic stiffness and periodic-graph counting: primary-source check

## Exact two-end rod map

**Direct primary match.** Liu, Zhao, Zhou & Banerjee, “Dynamic stiffness method for exact longitudinal free vibration of rods and trusses using simple and advanced theories,” *Applied Mathematical Modelling* 104 (2022), 401–420, DOI [10.1016/j.apm.2021.11.023](https://doi.org/10.1016/j.apm.2021.11.023). I inspected the authors’ accepted manuscript in [City Research Online](https://openaccess.city.ac.uk/28102/1/Manuscript%20DSM%20of%20rods.pdf). Its classical-rod section gives the distributed equation (Eqs. 1–4, PDF pp. 4–5), harmonic solution and endpoint force convention (Eqs. 5–9, p. 5), and exact two-end dynamic-stiffness map (Eq. 10; repeated as matrix definition Eq. 12, p. 5). With α=ωL/c=kL, its Eq. 10 is

\[
\begin{pmatrix}F_1\\F_2\end{pmatrix}
=\frac{EA\alpha}{L}
\begin{pmatrix}\cot\alpha&-\csc\alpha\\-\csc\alpha&\cot\alpha\end{pmatrix}
\begin{pmatrix}U_1\\U_2\end{pmatrix}
=\frac{EAk}{\sin(kL)}
\begin{pmatrix}\cos(kL)&-1\\-1&\cos(kL)\end{pmatrix}
\begin{pmatrix}U_1\\U_2\end{pmatrix}.
\]

The manuscript sets `F(0) = -F₁` and `F(L) = F₂`, so these are outward nodal forces; its ordering and signs match the finite-rod note. The model is a uniform classical axial rod with linear elasticity, constant area, no damping, and no distributed forcing. Its wave speed is `c = √(E/ρ)`. Taking `ω → 0` in Eq. 10 gives the static axial spring matrix `(EA/L) [[1,-1],[-1,1]]`.

## Pole / internal-mode caveat

The same paper explicitly treats the rod-element poles: Eqs. 55–57 (PDF pp. 11–12) give the Wittrick–Williams assembled mode count `J = Σᵢ J₀ᵢ(ω) + s(K(ω))`, where `J₀ᵢ` counts each element’s fixed–fixed natural modes. For a classical uniform rod, the poles satisfy `sin(kL) = 0`; Eq. 57 gives `J₀(ω) = floor(ωL/(cπ))`, with the usual threshold convention at an exact pole. Thus `ωL/c = mπ` is not a harmless numerical singularity: it is an internal Dirichlet standing-wave frequency of the eliminated rod. The endpoint dynamic-stiffness Schur complement is undefined there. For exact global mode/transmission treatment at such values, keep the interior field or use the regular state transfer matrix and take the appropriate limit; do not interpret clearing denominators as automatically preserving the spectrum. Isolated compact modes carry no propagating lead flux, but they remain in the full spectral/mode count.

## What periodic metric-graph theory establishes

Exner, Kuchment & Winn, “On the location of spectral edges in \(\mathbb Z\)-periodic media,” *J. Phys. A: Math. Theor.* 43 (2010), 474022, [arXiv:1006.3001](https://arxiv.org/abs/1006.3001), directly treats edgewise −d²/dx² on periodic metric graphs with continuity and Kirchhoff vertex conditions (source lines 19–45). For each Bloch quasi-momentum `k ∈ [-π,π]`, the fiber has a discrete, multiplicity-counted sequence `λⱼ(k)`; Eq. (4) states

\[
\sigma(\mathcal H)=\bigcup_j\lambda_j([-\pi,\pi])
=\bigcup_{k\in[-\pi,\pi]}\sigma(\mathcal H(k)).
\]

This supports reducing the infinite periodic graph’s spectrum to its Bloch fibers and counting bands as ranges of fiber eigenvalue branches. It does **not** provide the finite “number of right-moving channels at a chosen ω” used by the rod calculation. The paper’s Theorem 3 also cautions that for a one-periodic chain with more than one connecting edge, band extrema need not occur only at `k = 0, π`; that warning is relevant to a multi-link cell. Its vertex law is Kirchhoff and its edge operator is an unweighted Laplacian, so applying it to rods with point masses, nonuniform parameters, or other joint laws requires the corresponding self-adjoint Bloch operator to be specified.

## Boundary of the current root-count claim

For the particular uniform-rod unit cell, the finite secular-polynomial degree in `x = cos q`, the count of simple real roots in `−1 < x < 1`, and the pairing `q = ± arccos(x)` are model-specific algebra/dispersion claims, not results supplied by either cited source. Generically away from band edges, degeneracies, and rod poles, reciprocity pairs the two q roots with opposite group-velocity signs, so one simple x-root contributes one right-moving channel. The source checks do not validate the polynomial clearing/pole cancellation or the numerical root-count implementation. Those need a separate symbolic/full-transfer verification against the uneliminated Bloch boundary-value problem, especially at coincident rod poles and flat/compact rod modes.
