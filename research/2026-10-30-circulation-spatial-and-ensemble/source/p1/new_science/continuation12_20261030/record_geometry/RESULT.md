# Independent round-12 opening: sparse internal loads create native material

The completed construction is
SPARSE_INTERNAL_LOADS_PREPARE_NATIVE_PROFILES.md. It was selected and
developed independently before receiving a preferred root mechanism.
It changes the task: create a prescribed nonuniform native density,
rather than preserving all original native density histories.

## Working operation

In a no-passing hard-particle channel, choose R tagged particles by
their conserved material ranks. Specify the particle count between
successive tags. Opposed loads on those tags fix pressure differences.
Unknown reciprocal kinetic coefficients affect waiting time but cancel
from the exact loaded equilibrium.

For the finite-rate lattice model, gap variables have

\[
\pi(g)\propto\prod_i w_i^{g_i},\qquad
F_i=\log w_{i-1}-\log w_i.
\]

Set w=1-rho_j in each desired density block. For continuous unit rods,
set gap pressures p=rho_j/(1-rho_j), with tag force
F_i=p_i-p_(i-1). These are different equations of state, not
interchangeable formulas.

A smooth interior target is approximated using R=N^(1/3) tags,
maximum individual load O(N^(-1/3)), total absolute load O(1), and
vanishing tag-density contribution. The equilibrium profile error is
O(1/R+R/N), with an ordinary order-N concentration bound.

One anchor gives a laboratory-frame material. Without it, the profile
has a random common translation and must be described in its actual
retained material frame. An origin selected after seeing the outcome
is not an unconditioned nonflat laboratory mean.

## Genuine preparation and release

The bounded-rate gap chain is irreducible for every fixed hidden
kinetic class. A displayed canonical-path bound gives a finite
uniform waiting time; its conservative exponential dependence is
retained rather than replaced with an unproved diffusion estimate.

The continuous model is stronger. Its actual reciprocal mobility
generator on the convex ordered configuration domain C obeys

\[
L_\lambda=e^{\lambda E}\nabla\cdot
        (e^{-\lambda E}\mathsf M\nabla),\qquad
\mathsf M\succeq m_- I.
\]

Adding a diameter-scale quadratic to the linear pressure potential,
applying Brascamp--Lieb, and comparing densities gives

\[
\operatorname{gap}\ge 2m_-/(e\,\operatorname{diam}(C)^2).
\]

Since diam(C)^2=O(N^3) and the actual unloaded-to-loaded density
ceiling is exp(O(N)), a conservative warm-canonical preparation
time is O(N^4/m_-). No kinetic fitting or hidden-class mixing
is used.

This is an overdamped thermal model. Its finite-bandwidth inertial
replacement was not constructed. The force schedule itself can
have finite ramp duration. For a smooth sparse program,
sum_i F_i²=O(1/R). Keeping the actual mobility or jump prefactors
unchanged while turning off the force over fixed time tau gives
path relative entropy O(tau/R) against the loaded reference.
The final positional law therefore stays within O(sqrt(tau/R))
in total variation. No global position clamp is granted.

## Work and resource consequence

A complete load-and-release cycle has exact bookkeeping

\[
W_{\rm motion}=-\int\lambda\,dE
             =-\Delta(\lambda E)+\int E\,d\lambda.
\]

When lambda starts and finishes at zero, true net force work equals
the parameter-work ledger. The two are not added twice.

J equilibrated loading steps and a finite-duration release achieve

\[
EW=D(\pi_{\rm target}\|\pi_0)
   +O(N/J+N\delta+N\sqrt{\tau/R}).
\]

The final full positional-law error is at most
delta+C sqrt(tau/R). With R=N^(1/3), J=N^(1/6),
delta=N^(-1/6), tau=1, the conservative total preparation time is
O(N^(25/6)/m_-), the work excess is O(N^(5/6)), and the final
TV error is O(N^(-1/6)). These are concrete finite-tolerance
resources, not an acquired hardware precision budget.

For alternating densities 3/4 and 1/4 in four equal spatial bands,
the reversible lattice preparation cost is 0.1308120359 N.
The continuous hard-rod cost is (log 3)N/4=0.2746530722 N.
Keeping the loaded equilibrium has zero mean ongoing force work.
Its actual absolute thermal motion, force-source recovery, tag
travel, preparation, calibration and supporting hardware are still
paid. The released native gradient subsequently relaxes; it is
not an indefinitely stationary unloaded state.

## Strongest ordinary comparison and selection

Bénichou, Démery and Poncet's 2018 primary paper explicitly
supplies the single-file pressure-jump mechanism and several
driven probes. Evans's 1996 exact disordered exclusion solution
supplies product gap weights. The source record is SOURCE_SCOPE.md.

Static exterior pistons alone give uniform pressure in one
connected equilibrium chamber and cannot hold the four internal
bands. Sparse internal access therefore changes the reachable
class. But ordinary internal pistons or semipermeable partitions
with the identical ranks, force ports and counts implement exactly
this same operation. Position-clamped internal partitions can
even enforce a coarse profile before microscopic equilibration,
if their stronger actuation and confinement resources are supplied.

This is a useful working alternative, not a claimed new generic
thermodynamic principle or a unique advantage over ordinary
piston control. Its role in selection is concrete: bulk native
profiles can be programmed without hidden kinetic identification,
but only by changing the native density task and supplying
internal access, order-N preparation free energy and real time.

## Checks, records, and preservation

check_sparse_loads.py and SPARSE_LOADS_CHECK.json contain 33
finite population cases, 554 states and 2,038 marked transitions.
Detailed balance, stationarity and every marked mean current
vanish exactly in rational arithmetic, including unknown
state-dependent reciprocal conductances. The floating energy
identity residual is below 6.7e-16. Finite-step work bounds and
canonical three-band entropy convergence are also checked.
No mixing time, physical source, force accuracy or detector was
measured or inferred from those calculations.

Conditional old-record claims retain actual initial ceilings,
frozen kinetic classes and future thermal hypotheses. Force
calibration and cumulative force-error control remain necessary.
The full microscopic preparation error does not automatically
have a superexponential scale, and a newly exposed preparation
log is not automatically independent of the prepared state.

Only this fresh continuation12/record_geometry directory was
written. Previous continuation bytes, completed proofs and
reviews were not modified. No new worker, branch, model,
external message or transfer was used.
