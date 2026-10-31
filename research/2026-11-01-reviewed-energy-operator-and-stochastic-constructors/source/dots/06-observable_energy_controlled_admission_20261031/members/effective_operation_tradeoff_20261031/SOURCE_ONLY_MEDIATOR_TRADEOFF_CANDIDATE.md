# Source-only mediator: paid coherent drive and noise

Status: root candidate, not independently reviewed. This is ordinary elimination algebra used to choose a consequential next task, not a novelty claim or a finite-rate elimination theorem.

## Scope

Take a finite excited SOURCE space, positive D, Hermitian F, and N=F-iD. All these matrices act on source only, tensor identity on data. Source jumps return directly to a single dark state with sum L_j^dagger L_j=2D. The excitation coupling B maps data into source-excitation tensor data. Ground Hamiltonian is excluded from the mediated operation below and is charged separately. Use the standard leading effective operator equations of Reiter–Sorensen, https://arxiv.org/html/1112.2806v2 , equations (3)–(5). No finite-rate error follows from those equations alone.

Let X=N^{-1}B, E=sqrt(2D)X, and K=D^{-1/2} F D^{-1/2}. A source-only isometry of jump colors transforms E into the physical effective jump stack and does not change its dissipator. Suppose ||K||<=chi is actually acquired. Direct identities give

  S= -B^dagger Re(N^{-1})B = -X^dagger F X = -E^dagger K E/2,
  Q=E^dagger E,
  -chi Q/2 <= S <= chi Q/2.

The first equality uses Re(N^{-1})=N^{-dagger} F N^{-1}. This is an ACTIVITY comparison, not a noise lower bound.

## Scalar drive must be paid

For any scalar vector e, decompose E=e tensor I + A, set a=||e||^2 and delta=||A|| (stack operator norm). Let s=-e^dagger K e/2. Because K acts only on source,

  ||S-sI|| <= chi sqrt(a) delta + chi delta^2/2.

The dissipator obeys the exact gauge identity

  D[E]=D[A]-i[H_e,.],
  H_e=(i/2)(e^dagger A-A^dagger e),
  ||H_e||<=sqrt(a) delta.

Thus, for the actually mediated Hamiltonian G=S+H_e in this centered-jump representation,

  inf_s ||G-sI|| <= (chi+1)sqrt(a) delta + chi delta^2/2.   (1)

This includes the scalar-drive interference term; suppressing it would produce a false quadratic gate/noise claim. The scalar jump flux a, detuning chi, coupling needed to realize B, and actual elimination accuracy are all paid resources.

For d-dimensional data choose e_j=Tr(E_j)/d. Define the infinitesimal entanglement-infidelity rate

  nu=sum_j [Tr(E_j^dagger E_j)/d-|Tr(E_j)/d|^2]
     =||A||_HS^2/d.

This is exactly the derivative of 1 minus entanglement fidelity at t=0 for the effective generator, for normalized maximally entangled input. Hamiltonians have zero first derivative of this fidelity. Since delta<=sqrt(d nu), (1) implies, writing h=inf_s||G-sI||,

  h <= (chi+1)sqrt(a d nu) + chi d nu/2.                 (2)

For fixed a,chi,d and nonzero h this bounds nu away from zero. It does NOT prove a finite gate-error lower bound with adaptive correction, encode/decode, or varying parameters; nor does it turn a jump count into thermodynamic power.

## Essential counter-scope: data-dependent excited Hamiltonian

If F acts on data as well, the scalar term e^dagger K e need not be scalar on data. No version of (1) follows without paying that term as an independently supplied interaction. For example D=d0 I, F=Z_data in one excited source level, and B=(F-iD)v give X=vI. The effective jump is sqrt(2d0)v I, whose dissipator is zero, while S=-|v|^2 Z. This is a nontrivial noiseless LEADING effective Hamiltonian; its desired interaction is already present in F and in the engineered B. Finite-rate correctness and physical implementation are separate. It disproves a blanket claim that a lossy mediator must produce noise proportional to its gate strength.

## Interpretation

For source-only detuning and direct return, low logical noise can coexist with a useful coherent gate through increasing scalar drive, detuning or other charged resources. This is standard Raman/reservoir-engineering territory. A new capability needs either an actually better implementation of those resources, a useful receiver that exploits the emissions, or a construction outside this restricted mediator model. The earlier local all-selected amplitude admission remains a distinct finite-rate result and is neither implied nor invalidated by this algebra.
