# Beyen et al. scope check: fixed heterogeneous reactivities

## Finding

There is no contradiction with the proposed three-state, binary-port witness from a general positivity theorem in Beyen, Casini, and Maes. Their general slow-probe formula is Eq. (11),

\[
\nu(x)=-\lambda N\int_0^\infty d\tau\,
\left\langle \partial_x U(x,\sigma(\tau));\partial_x\log\rho_x(\sigma)\right\rangle_x^{\rm BO},
\]

but the positive result for probe-position-independent reactivities is obtained only after specializing the model and expanding at weak coupling.

## Exact scope in the primary source

Beyen et al. first define the general symmetric reactivity as \(\psi_x(\sigma,\sigma')=\sqrt{k_x(\sigma,\sigma')k_x(\sigma',\sigma)}\) (Eq. 2), then choose a **common edge baseline**
\[
\psi_x(\sigma,\sigma')=\psi_0[1+\lambda\Psi_x(\sigma,\sigma')]
\]
in Eq. (7). Their explicit negative-friction calculation then fixes a three-state model with \(U(x,\sigma)=\delta_{\sigma,0}\tilde U(x)\), only edge \((0,1)\) having \(\Psi_x=\tilde\Psi(x)\), and \(\Psi_x=0\) on the other two edges (Eq. 14); they retain leading order in \(\lambda\ll1\). In that specialization Eq. (20) gives a positive entropic term plus a frenetic term proportional to \(\tilde U'(x)\tilde\Psi'(x)\), and the paper says the latter vanishes, leaving positive friction, when the reactivities do not depend on \(x\) (Eqs. 20–21 and discussion immediately after Eq. 24).

That calculation does **not** cover order-one, edge-dependent but field-independent baseline values \(\psi_{01},\psi_{12},\psi_{20}\). In the proposal, the conservative field changes forward/reverse rate ratios while each \(\sqrt{q_{ij}(h)q_{ji}(h)}\) stays fixed; the unequal baseline prefactors are outside Eq. (7)'s common-\(\psi_0\), weak-coupling expansion. Eq. (11) remains relevant as a general response framework, but it does not imply positivity for this uncomputed heterogeneous case. Therefore: **not a contradiction, and not a literature proof that the proposed generator has negative friction.** Keep the candidate's direct finite-amplitude work calculation distinct from a claim of negative *linear* friction; the latter needs its own small-signal/low-frequency check.

## Closest cited construction

Lefebvre and Maes, [“Frenetic steering: nonequilibrium-enabled navigation,” *Chaos* 34, 063121 (2024), arXiv:2309.09227](https://arxiv.org/abs/2309.09227), Eq. (2), allow symmetric activities \(a(x,\{\eta,\eta'\})\) to depend on probe position and use that control to steer the induced **mean force** (three-state example, Eqs. (4)–(5), and trajectory steering in Sec. III). It is direct prior art for reactivity-controlled probe response, but it deliberately tunes activities; it neither proves a no-go for fixed heterogeneous activities nor supplies the proposed fixed-prefactor binary-port work witness.

## Source

Aaron Beyen, Francesco Casini, and Christian Maes, [“A Rayleigh criterion for mechanical instability: inducing activity by chemo-mechanical coupling,” arXiv:2605.06543v2 (2026)](https://arxiv.org/abs/2605.06543), DOI [10.1088/1742-5468/ae898f](https://doi.org/10.1088/1742-5468/ae898f). The exact assumptions and equations above are in Secs. II–III.3, especially Eqs. (2), (7), (11), (14), and (20)–(24).
