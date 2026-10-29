# The nonlinear particle-field attack: what closes and what does not

30 October 2026. Root construction, with a load-bearing unresolved receiver.
This is the attempted step beyond the exact Gaussian transport family. It is
not a completed nonlinear action or a new particle-field principle. The close
Maggs--Levrel predecessor below materially narrows the invention claim.

## 1. An actual local Markov operation

Let eta be exclusion occupancy on one ring, or two separate native rings, with
fixed particle numbers. On an active edge put delta_i=eta_i-eta_(i+1), equal to
+1 or -1. Fields q,p have energy (||q||^2+||p||^2)/2. A particle hop is the
joint local event

    eta -> eta^i,      q -> q+g delta_i e_i,     p unchanged. (1)

Use the actual rate

    c_i(eta,h) min{1,exp[-g delta_i q_i-g^2/2]},             (2)

where 0<c_i<=c_+, c_i(eta,h)=c_i(eta^i,h), and h is frozen hidden memory.
The prefactors may be unknown and state dependent within this reciprocal
bounded class. Equation (2) is a supplied joint operation. Static reweighting
does not establish an unmeasured intervention's kinetic interface.

Between events run

    dq=-a A^*p dt,
    dp=a A q dt-gamma AA^*p dt+sqrt(2gamma)A dV.             (3)

For one ring A=B_N; for two, A is the signed ladder in the root construction.
All native current is counted in (1). Equation (3) transports a separately
declared apparatus field, not native particles. There is no event-wide bit.
Particle rates are bounded; field frequencies have bounded local coefficients.
Gaussian amplitude and white bath force remain ideal specifications.

## 2. Exact statements without identifying hidden kinetics

At zero native force the actual invariant law is

    mu=uniform canonical eta x N(0,I)_q x N(0,I)_p.         (4)

The marked event (1) changes energy by Delta E=g delta_i q_i+g^2/2. In its
reverse, delta changes sign and q_i becomes q_i+g delta, giving increment
-Delta E. The shift has unit Jacobian. The reciprocal prefactor and Metropolis
identity therefore give exact detailed balance for each marked pair. The
lossless part of (3) is divergence free and energy preserving; its conservative
OU bath preserves the Gaussian p factor. Each part preserves (4).

Nonexplosion follows from the bounded particle rate and the linear SDE between
finitely many jumps. No hidden mixing, copying, or reset is used. For every
h_0 in ker A, actual paths satisfy

    h_0^*J(t)=[h_0^*q(t)-h_0^*q(0)]/g.                    (5)

This is a collective current counter with transported memory. It does not
establish availability of the desired nonflat density histories.

## 3. A non-Gaussian whole-horizon rare-current bound

For one ring S=sum_i q_i is Gaussian of variance N under (4). Suppose the
actual initial density relative to (4) is at most exp(CN), uniformly over
the retained old records and h to which the result is applied. A deterministic
particle configuration and independent thermal q,p satisfy this: its density
ceiling is at most the number of fixed-mass configurations, which is <=2^N.
An arbitrary hidden preparation does not automatically meet the condition.

Invariance and positivity of the adjoint Markov semigroup preserve the density
ceiling at every deterministic time. Gaussian tails and a union over integer
times up to N^2T give

    P(max_j |S(j)|>epsilon g N^2/4)
       <=C_T(1+N^2)exp[CN-c epsilon^2 g^2 N^3].             (6)

Between successive integers, S changes only at particle events, by at most g
per event. Their number is dominated by Poisson(c_+N), regardless of field or
unknown rates. The chance of epsilon N^2/4 events in a unit interval is at most
exp[-c_epsilon N^2 log N] for large N. Including the initial endpoint, (5)-(6)
therefore imply

    P(sup_(t<=N^2T)|J_tot(t)|>epsilon N^2)
      <=C_T(1+N^2)exp[CN-c epsilon^2 kappa_N N^3]
        +C_T(1+N^2)exp[-c_epsilon N^2 log N].               (7)

Thus kappa_N N^2->infinity yields superexponential disappearance at speed N.
The two-ring current difference has the same proof with different numerical
constants. This is a true non-Gaussian path bound, not a covariance-to-LDP
inference. The exp(CN) ceiling transfers this superexponential estimate, not
finite-action probabilities for free.

## 4. A protected force is stored, not freely converted

For a constant work vector f in ker A, replace the event increment in (2) by
Delta E-f_i delta_i. Marked balance gives the invariant law with q mean f/g,
because A(f/g)=0. Stationary native current is zero and the mean stored energy
is ||f||^2/(2kappa). Suppressing a current direction removes its DC conduction
under this actual reciprocal force port. Useful driven common-channel
conversion outside ker A is a separate nonlinear nonequilibrium receiver;
it is not supplied by this shifted-equilibrium argument.

## 5. The missing theory is specific

The intended stronger result would retain nonflat exclusion heat and prove
the projected nonlinear density/current action for (1)-(3). That is not
established. Canonical invariance and (7) are insufficient: the earlier elastic
memory preserved equilibrium and typical stationary fluctuations while freezing
large profiles.

The naive argument that rates approach native rates fails on time N^2, with
order N^3 events. Even a small per-event quadratic likelihood cost of order
kappa accumulates to order kappa N^3. Per speed N this is kappa N^2, precisely
what must diverge for (7). Full microscopic path equivalence is impossible
anyway: native circulating histories have finite action but (7) excludes them.
Only a selective density/current elimination could work.

Weak-coupling drift contains weighted terms of the form
g q_i(eta_i-eta_(i+1))^2. Fields and activity develop joint histories. The
static product law (4) does not permit replacing activity by its equilibrium
mean inside this product. A valid proof needs weighted replacement and field
averaging under the actual weakly tilted histories, including nonflat density
and rare small activity. The linear corrected-momentum identity does not
close this product, and the Gaussian theorem does not repair it.

The exploratory window N^-2<<kappa<<N^-1 keeps (7) while making a fixed-size
single-coordinate rate perturbation costly at speed N. That observation is
neither the required weighted replacement nor the full action. It is saved
as a possible further attack, without assuming its outcome.

## 6. Direct predecessor and transducer boundary

Levrel--Maggs, *Boundary conditions in local electrostatics algorithms*,
J.Chem.Phys.128,214103(2008), https://arxiv.org/pdf/0805.1869, couples particle
hops to local link-field updates and obtains a conserved relation between
uniform field and winding displacement (periodic-boundary section, equations
11-12). Independent field/worm updates change that sector. Maggs, *Dynamics
of a Local Algorithm for Simulating Coulomb Interactions*,
https://arxiv.org/pdf/cond-mat/0111272, already treats charged lattice gases
with local field dynamics. These preempt a broad invention claim for local
field counters or selecting winding through a field sector.

Maxwell transport uses curl C with BC=0 and preserves a Gauss-law sector.
Integrating field energy over that sector generally induces Coulomb particle
interactions. Scalar-wave A^* in (3) has different geometry and can preserve
the product marginal (4). Ordinary electromagnetism does not supply (1)-(3)
by analogy. A real transducer must provide the joint particle/memory event,
its energy-dependent rates and reciprocal scalar field, counting all native
motion. No fabricated transducer is claimed. The unresolved step is the
actual nonlinear trajectory receiver and its supplier, not another invariant
counter identity.
