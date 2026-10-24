# Ensemble and free-energy audit of Mondal et al. (2026)

## Exact conserved quantity in the undriven model

The paper's Eq. (1) is the rotating-wave Tavis–Cummings Hamiltonian
\[
H_{TC}=\hbar\omega_c a^\dagger a+\sum_n\hbar\omega_n\sigma_n^+\sigma_n^-
+\sum_n\hbar g_n(\sigma_n^+a+a^\dagger\sigma_n^-).
\]
Its conserved excitation is
\[
Q=a^\dagger a+N_m,\qquad N_m=\sum_n\sigma_n^+\sigma_n^- ,
\]
with \([H_{TC},Q]=0\). For nonzero coupling, \([H_{TC},N_m]\ne0\): the interaction converts a molecular excitation to a photon and back. Thus molecule-only excitation is not an independent conserved charge of the full undriven model.

The corresponding equilibrium choices are unambiguous:

- An isolated system with fixed total excitation \(Q=q\) has the canonical-sector state \(\rho_q=P_q e^{-\beta H_{TC}}P_q/Z_q\). The molecular mean is determined by this state; it is not separately fixed to the uncoupled Boltzmann value.
- A system in contact with an excitation reservoir has \(\rho\propto e^{-\beta(H_{TC}-\mu_Q Q)}\). With an ordinary zero-chemical-potential photon/thermal bath, \(\mu_Q=0\), giving the Gibbs state \(e^{-\beta H_{TC}}/Z\).
- A nonzero chemical potential coupled only to \(N_m\) is not an equilibrium chemical potential for the full TC Hamiltonian: \(e^{-\beta(H_{TC}-\mu_mN_m)}\) does not commute with \(H_{TC}\) for generic \(g_n\ne0,\mu_m\ne0\). It requires a separate constraint, reservoir, or driven preparation.

## What Eqs. (33)–(40), (56)–(60) actually compare

After a second-order Schrieffer–Wolff elimination, Eq. (14) is a matter-only XY Hamiltonian. It conserves \(N_m\) within that effective model, unlike the original TC Hamiltonian. Methods Eqs. (56)–(60) then impose
\[
\langle N_m\rangle=\sum_n |v_n|^2
=\sum_n\frac{e^{-\beta\hbar\tilde\omega_n}}{1+e^{-\beta\hbar\tilde\omega_n}}
\simeq N e^{-\beta\hbar\omega_0}
\]
using \(\mu\) as a Lagrange multiplier, and vary the pure product ansatz \(\prod_n(u_n+v_n\sigma_n^+) |0\rangle\). This licenses a mean-number-constrained variational calculation for the effective matter Hamiltonian. It does **not** by itself license the \(\mu_Q=0\) Gibbs ensemble of the full TC system, nor a fixed-total-\(Q\) ensemble.

The ansatz is not number projected. For its product form,
\[
\operatorname{Var}(N_m)=\sum_n |u_n|^2|v_n|^2,
\]
which is positive at finite filling; with no photon degree of freedom in the ansatz, it therefore superposes distinct total-excitation sectors. Calling \(\mu\) a Lagrange multiplier is mathematically fine for the constrained minimization, but it does not establish that an undriven cavity supplies or fixes that molecular-only mean.

Equations (33)–(38) compare the energy of this single pure trial state (zero von Neumann entropy, so its assigned free energy is its energy) with the free energy of an approximate independent-molecule normal thermal manifold. A lower trial value can challenge that particular normal reference within a common constrained effective model. To establish an equilibrium transition in the full undriven TC model, the comparison must use the same physical ensemble and Hamiltonian on both sides, including the total-excitation sector or the \(\mu_Q=0\) Gibbs weights, photon contributions, and the relevant competing thermal states. The paper's calculation does not supply that identification.

## Vacuum-ground argument and the precise escape

Vacuum being the ground state only settles the zero-temperature, unconstrained-charge ground-state question. It is not a finite-temperature no-go: entropy contributes \(-TS\), and the paper's own normal reference has \(F_0=-Nk_BT\ln(1+e^{-\beta\hbar\omega_0})<0\) for every \(T>0\), despite the vacuum energy being zero. Finite-system U(1)-invariant Gibbs states have zero one-point order parameter, but that fact alone also does not rule out symmetry breaking in a thermodynamic limit. A finite-temperature claim must be tested by the appropriate equilibrium free-energy density/susceptibility, not by ground-state positivity alone.

There is a concrete escape from the ensemble mismatch: specify an isolated preparation with fixed extensive total excitation density \(q/N\), project the BCS-like ansatz into the corresponding total-\(Q\) sector (including the SW dressing), and compare canonical free energies in that sector. In a suitable thermodynamic scaling, number projection may preserve leading mean-field energy and long-range correlations, but that is an additional derivation, not what Eqs. (56)–(60) calculate. Alternatively, demonstrate the transition directly in the full \(\mu_Q=0\) Gibbs ensemble. Either route could support a finite-temperature phase; the present constrained mean-molecule calculation alone does not establish one for an undriven TC cavity.

**Scope:** This is an ensemble/variational audit of the cited paper's stated equations, not a claim that finite-temperature ordering is impossible or that the effective XY model cannot order.
