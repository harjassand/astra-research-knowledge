# Active zero-risk support: bounded audit

## Verdict

The support argument is correct for the stated finite-dimensional,
time-varying coherent-controller class, provided “zero actual death” means
zero accumulated jump probability on the whole interval and the dead sector
is invariant under the Hamiltonian, as assumed in the opening. A unilateral
zero-risk trajectory at one $g>0$ then has no $e$- or $a$-support and is also
a solution for every other $g$, under the same initial state and common
control. This is an exact-face statement; it gives no uniform bound at small
positive risk.

## Block and carré-du-champ checks

Since $\gamma>0$, the increase in dead population is
\[
  p_D(T)-p_D(0)=\gamma\int_0^T \operatorname{Tr}(P_e\rho_t)\,dt.
\]
For a dead-free initial state, zero accumulated death makes this integral
zero. Continuity and positivity imply $P_e\rho_t=\rho_tP_e=0$ at every time.
The same conclusion follows if zero death is defined to include any initial
dead population, since then $p_D(0)=0$ as well.

Let $Q=I-P_e-P_D$, $H_g(t)=gV+H_c(t)$, and
\[
 K=P_eH_gQ,\qquad A=K^\dagger K.
\]
The $e,Q$ block of $\dot\rho$ is zero. With the dead sector invariant, all
terms in that block vanish except the Hamiltonian $e,Q$ coupling, so
$K(Q\rho Q)=0$. As $A$ is supported on $Q$, this gives
$f_0=\operatorname{Tr}(A\rho)=0$. Positivity strengthens this to
$K\sqrt\rho=0$, hence $K\rho=\rho K^\dagger=0$.

For any differentiable $K(t)$, differentiating $f_0$ has no surviving
$\dot K$ term: each such trace contains either $K\rho$ or
$\rho K^\dagger$. The Hamiltonian contribution is zero because
$A\rho=\rho A=0$. The loss dissipator is zero on a state with zero
$e$-row and column. Finally, for
$\mathcal D[Z](\rho)=Z\rho Z-\tfrac12\{Z^2,\rho\}$, the anticommutator traces
vanish for the same support reason. Thus the coefficient and sign are
exactly
\[
 f_0'=\kappa\operatorname{Tr}(K^\dagger K Z\rho Z)
      =\kappa\|KZ\sqrt\rho\|_{HS}^2\ge 0.
\]
Since $f_0\equiv0$, $KZ\sqrt\rho=0$. Put $K_1=KZ$ and
$A_1=K_1^\dagger K_1$. Then $f_1=\operatorname{Tr}(A_1\rho)=0$
identically. Repeating the same calculation is valid: $\dot K_1=\dot KZ$
terms vanish using $KZ\rho=\rho ZK^\dagger=0$; the Hamiltonian and loss
terms vanish; and the dephasing carré du champ yields
\[
 f_1'=\kappa\operatorname{Tr}((KZ^2)^\dagger KZ^2\rho)
      =\kappa\|KZ^2\sqrt\rho\|_{HS}^2.
\]
So $KZ^2\sqrt\rho=0$. No assumption that $K$ is constant or that $H_c$
commutes with $Z$ is used.

On the sample sectors, $Z=P_a-P_b$ and $Z^2=P_a+P_b$, including the
identity on the controller. Therefore
\[
 KP_a\sqrt\rho=\tfrac12(KZ^2+KZ)\sqrt\rho=0.
\]
The control-block promise gives
$KP_a=P_e(gV+H_c)P_a=g|e\rangle\langle a|\otimes I$. Since $g>0$, this is
injective on the $a$-sector, and $P_a\rho=\rho P_a=0$.

## Consequence and boundary

With both $P_a\rho=0$ and $P_e\rho=0$, the signal $V$ annihilates $\rho$ on
both sides, so $-i[gV,\rho]$ is zero along the trajectory. The same state
path solves the common finite-dimensional ODE for every coupling $g'$;
uniqueness makes the joint trajectory and any output derived from it
$g'$-independent. Coherent storage of records does not alter this argument
when included in the fixed finite controller and when $P_eH_cP_a=0$ holds on
the joint space.

The exact closure uses all of the stated gates: $\kappa>0$, a fixed
Hermitian dephasing observable with $Z^2=P_a+P_b$, zero death on the whole
interval, no Hamiltonian coupling through the absorbing dead sector, a
common differentiable coherent control, and no control $a$-to-$e$ block.
An added dissipative control can add terms to the expectation derivatives;
the proof does not cover it. Nor does it imply an approximate support bound,
a positive risk floor, or a duration-independent information bound.
