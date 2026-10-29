# A connected diffusion receiver and local factor programs

29 October 2026. Root consequence construction for the bounded stationary
change-of-measure theorem. This is a complete mathematical operation family,
not an acquired apparatus. Addressed diffusion, noninvasive sign sensing and
compatible switching are supplied model controls.

## 1. Native dynamics with changing and conserved hidden memory

Let physical coordinates x=(x_1,...,x_d) lie in[-1,1]^d, let z be an
unobserved shared coordinate on a compact connected torus, and let h be a
conserved hidden parameter. A smooth finite energy U_h(x,z) is invariant
under each separate sign change x_i -> -x_i. Define

    mu_h(dx,dz)=Z_h^(-1)exp[-U_h(x,z)]dx dz.

No numerical knowledge of U_h or Z_h is used by the controller. The sign
symmetries imply that Y_i=1_{x_i>0} has a uniform joint bit law under every
mu_h. Coordinate zero sets have measure zero. Arbitrary interactions among
magnitudes and z are allowed; sign symmetry does not make the sign process
Markovian or the hidden magnitudes independent.

For each addressed operation i, supply a smooth symmetric positive definite
matrix A_i(h,x,z) on the active coordinates(x_i,z), with reflecting x_i
boundaries and periodic z. All other x_j are physically fixed. Define

    L_i f=exp(U_h) div_(x_i,z)
                  [exp(-U_h) A_i grad_(x_i,z) f].             (1)

Assume the regularity and nonexplosion conditions defining this reflected
diffusion; smooth uniform ellipticity on each compact h-sector suffices.
There need not be a uniform lower mobility over h. The unknown A_i may
differ between operations and need not share the sign symmetry of U_h.
Integration by parts gives

    <f,L_i g>_(mu_h)
       =-integral (grad_i f)^T A_i grad_i g dmu_h
       =<L_i f,g>_(mu_h),        L_i1=0.                    (2)

Thus each actual fixed-time kernel P_i=exp(t_0 L_i) is reversible for the
same mu_h and leaves the other visible coordinates fixed. Shared hidden z
evolves through the whole program; h never mixes. Their rates are not learned.

In Itô form the active drift is div A_i-A_i grad_i U_h and the noise
covariance is2A_i. Dropping the divergence drift generally changes the
invariant law. This thermodynamic-consistency issue is established by Lau
and Lubensky (2007), https://arxiv.org/abs/0707.2234,
DOI10.1103/PhysRevE.76.011123. Equation(1) states an actual mathematical
operation; a baseline equilibrium histogram does not supply that dynamics.
Kinetic uncertainty preserving(1) differs from an energetic asymmetry that
changes the baseline sign weights.

## 2. Exact local target without a hidden predictive model

Let the desired finite factor law be

    pi(y) proportional to W(y)=product_a psi_a(y_a),          (3)

with positive rational factors. In an update of i, all other coordinates
and their labels are fixed. Compute only the two relative local weights

    w_i(b;c)=product_(a containing i) psi_a(b,c_a), b=0,1,

and clear their denominators. Apply the counter compiler to P_i using the
current bit and these weights. On every fixed inactive-coordinate slice,
(2) supplies conditional reversibility. Factors not containing i are
constant on that slice. The compiler's balance identity therefore gives
the full microscopic target

    nu_h(dx,dz)=W(Y(x))mu_h(dx,dz)/mu_h(W).                  (4)

Prescribed scans or independent state-independent random scans preserve(4).
Its visible marginal is(3) in every h-sector, because baseline signs are
uniform in each sector. Arbitrary conserved-sector weights therefore do not
alter the common visible limiting target if within-sector convergence is
independently supplied. Conditional initial states and convergence times
remain real premises; invariance is not a preparation theorem.

The compiled sign transitions may depend on hidden magnitudes, z, h and
the full history posterior. The invariant law remains exact without a
finite-state heat-bath description. An ordinary Monte Carlo or physical
inference consumer can use these actual endpoints at completion indices.

## 3. Consequence and resource scale

For integer-valued local factor energies E(y), choose W(y)=2^{-E(y)}.
The relative edge weight is r_i=2^{|Delta_i E|}. A local macro needs at most
r_i native calls and log2 r_i fair bits for the two-label residual selector.
With bounded incident factors and bounded local energy changes, those
resources are independent of d. All context reads, arithmetic, native time
and isolation still count. At target equilibrium, the conditional baseline
sign masses are equal, so the mean native calls in each context are
2r_i/(1+r_i)<2. This is a stationary mean, not an all-start preparation cost.

The family includes strong ferromagnetic interactions, frustrated energies
and bounded-degree constraint/factor models. For square-lattice weight
2^(sum_edges s_i s_j), local ratios are1,16,256. Its coupling log2 exceeds
the standard Ising critical coupling(1/2)log(1+sqrt2). The q=2 critical-point
relation is supported by Beffara and Duminil-Copin,
https://arxiv.org/abs/1006.5073; conversion from Potts indicators uses
1_{s_i=s_j}=(1+s_i s_j)/2. The invariant-law theorem extends beyond the
earlier contractive receiver, while slow mixing and phase barriers remain.

A global weight compiler can have exponentially large max W/min W. Local
composition avoids that global per-update cost but retains collective mixing
barriers. No efficient solution of hard factor models or rare-event speedup
is inferred.

## 4. The earlier smoothing obstruction and physical-time limit remain

On each connected active leaf, the elliptic diffusion has a smoothing,
injective self-adjoint finite-time semigroup. The preserved obstruction
rules out a finite invariant predictive feature space containing its sharp
nontrivial sign indicator. This construction does not claim such a space.
It stops at different actual endpoints according to label and counter. A
stopped endpoint density can be piecewise weighted even though each native
fixed-time semigroup smooths. The invariant-law objective is therefore
compatible with the earlier obstruction and the infinite predictive-rank
example.

Equation(1) does not build the selective actuator, sensor or boundary timing.
Finite-resolution sign errors near0 and uncontrolled asymmetry remain actual
implementation errors. No fabricated apparatus or precision budget has been
acquired. For one P repeated back-to-back, selected endpoints are tilted
but native-step occupation remains mu_h. Local scheduling changes actuation,
but its wall-time law is still separate. A real hold or direct bias actuator
is a legitimate stronger alternative when wall-time occupation is the goal.

The exact consequence is a bounded-call stopped-state program for continuous
hidden physical models. It can be consumed by conventional inference methods
without kinetic closure, while their preparation, mixing, sensing and
execution costs remain intact.

