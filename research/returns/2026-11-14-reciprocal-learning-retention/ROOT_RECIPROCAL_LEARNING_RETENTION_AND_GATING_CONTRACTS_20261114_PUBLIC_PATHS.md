RECIPROCAL LOCAL ADAPTATION: WRITING, BACKACTION AND RETENTION
Original restricted derivation,14 November2026 Brisbane. Not a universal
memory law, material fit, independent novelty claim or physical validation.

The question

An ideal local update such as xdot=c*p is not yet a thermodynamically closed
material model. Useful boundary behaviour might not require independent
control of every internal state, but the useful observable itself must survive
thermal fluctuations after teaching. Investigate this at a deliberately small
scope where the forces, rates, work and omitted operations are explicit.

Assumptions

Take boundary pressure forces p and internal state coordinates x, with flows
Q and xdot. The state coordinates have even time-reversal parity. There is one
isothermal bath at T, overdamped reciprocal purely dissipative coupling,
constant transport coefficients, and no uncounted magnetic/gyroscopic,
Hamiltonian, chemical-fuel or active-control channel. Let A=-grad_x F be the
state free-energy affinity. A near-equilibrium Onsager model is

  [ Q    ]   [ G   C ] [ p ]
  [ xdot ] = [ C^T M ] [ A ],             G=G^T positive definite.

The entropy-production power is T*sigma=p^T Q+A^T xdot. Requiring it
nonnegative for every p,A is equivalent to positive semidefiniteness of the
block matrix. Completing the square gives

  T*sigma=(p+G^-1 C A)^T G (p+G^-1 C A)
          +A^T (M-C^T G^-1 C) A.

Thus M >= C^T G^-1 C in positive-semidefinite order. The state noise covariance
required by fluctuation-dissipation is 2*k_B*T*M*dt. Reciprocal backaction
Q=G*p+C*A accompanies writing; it cannot generally be dropped while retaining
an arbitrary free-energy affinity and claiming closure.

For example, the declared noiseless one-way rule Q=p, xdot=p, with no affinity
backaction or state mobility, gives T*sigma=1-2=-1 at p=1,A=-2. This refutes
closure of THAT declared rule over unrestricted affinities. It does not rule
out active or nonlinear physical learning, or prove a mathematical update law
has no possible enlarged physical realization.

A bound on a useful observable, not necessarily on every state

Now make the ADDITIONAL assumptions that F is locally flat, y=a^T x is linear,
and the SAME constant G,C,M applies during writing and holding. There are no
barriers, confining boundaries, mode switches or subsequent feedback during
the hold. For a write of duration t_w, the mean change is

  Delta_y=integral_0^t_w a^T C^T p(t) dt.

Let theta=a^T C^T G^-1 C a and eta=a^T M a, so eta>=theta. With drive work
W_d=integral p(t)^T G p(t)dt, the Cauchy-Schwarz inequality in both channel
space and time gives Delta_y^2 <= theta*t_w*W_d. During a subsequent hold
t_h at p=A=0, the added variance is V_h=2*k_B*T*eta*t_h. Therefore

  W_d * V_h >= 2*k_B*T*Delta_y^2 * t_h/t_w.

This result already concerns the USEFUL observable. Merely allowing internal
states to remain unidentified does not remove this particular always-on
noise/write relation. It is not a global bound for arbitrary state-dependent
learning trajectories, and it does not justify imposing perfect state
identification or stabilization when only an observable matters.

For relative RMS retention error epsilon=sqrt(V_h)/abs(Delta_y), the same
model requires W_d>=2*k_B*T*t_h/(epsilon^2*t_w). For Gaussian endpoint error,
requiring99%probability inside +/-epsilon*abs(Delta_y) multiplies this necessary
work by z_.995^2, where z_.995=2.5758293. This is an endpoint criterion, NOT
continuous pathwise retention, device endurance or a measured error rate.

Introduced numerical examples

At the INTRODUCED reference T=298.15K, a1ms write and24h hold at relative
RMS error.001 give W_d>=7.11315e-7J in this model; the99%Gaussian ENDPOINT
criterion instead gives4.71950e-6J. A1s write/24hhold/.01RMS gives7.11315e-12J.
These are not a memory-product specification, experimental failure prediction
or universal lower bound; real protected nonlinear memories are outside this
constant always-on flat-free-energy model. Instruments, preparation, actual
mode transitions and other work reservoirs have not been supplied or priced.

The exact matrix diagnostic uses
  G=diag(2,3),
  C=[[1/5,1/10],[-1/10,3/10]],
  M_min=C^T G^-1 C=diag(7/300,7/200),
  M=M_min+[[1/100,3/1000],[3/1000,1/50]],
  a=(1,-1/2).
Then theta=77/2400, eta=529/12000, and optimal normalized constant pressure
p=(180/77,-200/77) writes unit mean change in unit time with W_d=2400/77.
The noise/work bound ratio is529/385>=1. All these matrix values are
INTRODUCED dimensionless examples. The completed-square identity is checked
exactly with rational arithmetic; the identity, not the finite force list,
governs positivity. No stochastic simulation is presented as physical data.

Why a gate or protected state changes the conclusion

The derivation compares writing and holding with the SAME M. A genuine
kinetic gate can instead use C_off=0 and M_off=rho*M_on while retaining
G_off>0 for useful reading. Both Onsager matrices can be positive semidefinite,
yet the hold variance is multiplied by rho. Ratios1e-3 and1e-6 are introduced
algebraic examples, not qualified gate states. Switching such a gate, changing
a barrier, cooling a material or preparing a metastable state has real
physics, work, time, stocks and possible effects on the learned function.
None is supplied by assigning a different mobility coefficient.

Fixed harmonic confinement, state-dependent barriers, nonlinear switching,
Casimir/reversible couplings, active fuel or time-dependent coefficients also
require a different calculation. A trap whose minimum follows an arbitrary
written value would itself contain the missing memory. No general obstruction
to such mechanisms is claimed. This diagnostic identifies what a physical
learning implementation must include; it does not invalidate earlier
conditional controllability calculations in their mathematical domains.

Primary-source boundaries and credit

Strukov2016, Endurance-write-speed tradeoffs in nonvolatile memories,
DOI10.1007/s00339-016-9841-0, exact
https://web.ece.ucsb.edu/~strukov/papers/2016/APAtradeoff2016.pdf
WHOLE4page TEXT0--291 read. It is a phenomenological thermally activated
switching/failure model with supplied activation-energy/temperature-voltage
assumptions; it is not a measured general memory law. Its discussion also
acknowledges a possible filamentary mechanism with the opposite stress/endurance
trend. Rendered equation glyphs have gaps; plotted curves were not visually
read and cited original experiments were not followed. No precise unavailable
formula or material point is reconstructed or imported here.

Goldt--Seifert1706.09713v1 metadata29June2017 verified BEFORE exact
https://arxiv.org/pdf/1706.09713v1 ; actual main0--448/pp0--4 read. It specifies
overdamped weight dynamics, harmonic confinement, a supplied learning force,
unit mobility/FDT, a teacher/sample model, and a reported information-cost
bound with its conditions. Later sharper bounds/appendix proofs, SI and code
were not read or executed. This is prior thermodynamics of abstract stochastic
learning; it does not furnish a boundary-only material, our pressure-state
Onsager realization, or a qualified memory gate.

Schur complements, Onsager reciprocity, fluctuation-dissipation and stochastic
learning cost relations are existing machinery. The present result is a
restricted implementation diagnostic, not a claim to have discovered those
principles. No biological material, organism engineering or experiment is used.

Executable binding

ROOT_RECIPROCAL_LEARNING_MOBILITY_AND_RETENTION_SCREEN_20261114.py
7316ASCII/SHA25686fdb4126a927dad920d28d8637dd7d546ec8e4478e42ddde357bbbbfcb84f6d
and its JSON5101ASCII/SHA256e586790b1dc079516693aab3a11ff1f7c2afda575b917759823e6441af9a3916
use standard-library rational algebra, Gaussian quantiles and explicit model
parameters. No producer code/data/archive or physical experiment is used.
