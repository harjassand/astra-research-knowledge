# Targeted comparison: thermal heat, native equilibrium models and memory

29 October 2026. Independent targeted primary reading by
producer-workspace/different_consequential_opening. This is a strength/subsumption check,
not a generic survey and not a historical-priority determination.

## Conclusion at the actual scope

No directly subsuming theorem for the combined target was identified in the
primary sections inspected in this pass. Substantial ingredients are explicitly
established in the literature, including the complete path-KL/force-matching
formula, weighted gradient projection, integrated-OU shear covariances,
nonequilibrium induced by a one-way equilibrium subsystem, and the exact
zero-entropy equilibrium characterization. Those ingredients must be credited.

The residual claim under consideration is this conjunction:

1. Fixed temperature, masses and friction; all momenta thermalized; applied
   position-only mechanical forcing; a sequence with physical entropy production
   tending to zero.
2. A positive full-path KL floor against **all smooth same-class Gibbs potential
   models**, and a positive uniform full-path TV floor against those whose forces
   obey a **fixed ceiling**. The current TV proof does not remove that ceiling.
3. For the autonomous equilibrium-driver source class, exact heat is a compressed
   position-resolvent quadratic form, whereas optimal native equilibrium KL rate
   is an ordinary force quadratic form. Their equivalence on a declared force
   family is exactly a coercivity condition, and the two forms admit a reusable
   lagged acquisition record.
4. A compact force class restores same-native-class full-path TV closure as
   physical entropy tends to zero.

This pass does not justify calling any item historically first. Absence from
selected readings is not absence from the literature.

Local comparison targets:

- GENERAL_THERMAL_MEMORY_METRICS.md, SHA256
  0d452d6a839b7609341ee73e825f550d95ac8ce2a1e7bd133a3d1f98727a8121.
- physical_frontier/NATIVE_EQUILIBRIUM_TOPOLOGY_OBSTRUCTION.md, SHA256
  b0318b8659d1acdff6887b1a5a58ec0c9f33661dd75ba845cb1bd573b468afa7.

## Strongest direct conventional overlap

**Harmandaris, Kalligiannaki, Katsoulakis and Plecháč, _Path-space variational
inference for non-equilibrium coarse-grained systems_, J. Comput. Phys. 314
(2016), 355–383.** [Primary manuscript](https://arxiv.org/html/1508.00289v2),
[DOI](https://doi.org/10.1016/j.jcp.2016.03.021).

Read §4.1, Theorem 4.1 and equations (25)–(29); Theorem 5.1; §6's kinetic
Langevin setup and stationary force-matching formulas, including the
noise-degenerate phase-space matrix. Theorem 4.1 directly gives finite-path KL
as initial KL plus one-half integrated squared noise-normalized drift difference.
Theorem 5.1 and §6 identify the resulting optimization with force matching,
without requiring equilibrium. With identity coarse map and fixed bath, this
directly supplies the ordinary force-square cost used by Astra. It is a stronger
equally informed route than fitting a generic reduced model. Astra's exact
periodic transverse geometry solves this established optimization and separates
its answer from physical heat; the general KL/force-matching principle is not an
addition.

**Zhao, Zhang and Li, _EPR-Net: constructing a non-equilibrium potential
landscape via a variational force projection formulation_, National Science
Review 11 (2024), nwae052.**
[Primary manuscript](https://arxiv.org/pdf/2301.01946),
[DOI](https://doi.org/10.1093/nsr/nwae052).

Read the nondegenerate overdamped setup, equations (1)–(6), and supplementary
§A's orthogonality/Pythagoras proof. They minimize stationary-density-weighted
squared force residual over gradient fields, with an exact orthogonal
decomposition. This directly precedes a broad claim that weighted force
projection or its quadratic Pythagoras is new. Their inspected result uses
overdamped variables with positive diffusion in every coordinate. It does not
supply the kinetic source's distinct heat resolvent, constrained same-bath
Gibbs comparison, or fixed-bath separation. The relevant addition must remain
attached to those restrictions and consequences.

## Known nearby mechanisms and the exact difference

**Hao Ge, _Time reversibility and nonequilibrium thermodynamics of second-order
stochastic processes_, Phys. Rev. E 89, 022127 (2014); manuscript v3 (2015).**
[Primary text](https://arxiv.org/pdf/1209.3081).

Read §§II–III, especially the velocity-feedback examples (12)–(15), and
§V.A–B, equation (18) and the beginning of the conditional entropy-current
decomposition. The distinction between statistical reversal symmetry and
thermodynamic Maxwell equilibrium is established. In the position-only-force
class, §V.A already proves the exact-zero condition: equilibrium requires a
potential force and spatially constant reservoir temperature. Its explicit
reversible/non-Maxwell examples use velocity-dependent feedback. These do not
directly subsume the small-positive-physical-entropy, fixed-bath, position-force
path-separation result. The exact-zero identification in the compactness repair
is an established antecedent.

**Boi, Mazzino and Muratore-Ginanneschi, _Eddy diffusivities of inertial
particles in random Gaussian flows_, Phys. Rev. Fluids 2, 014602 (2017).**
[Primary text](https://arxiv.org/pdf/1611.02747).

Read equations (1)–(10), including the explicit OU/shear solutions and Fourier
Gaussian-increment kernel. The integrated-OU factor
exp[-D0 |k|²(t−τ(1−exp(−t/τ)))] is already explicit. Under τ=1/γ and
D0=temperature/γ it is the kernel used in the shear calculation.
Their declared problem is inertial transport and eddy diffusivity in a carrier
flow. The covariance/filter calculation is therefore known; a same-looking
carrier-flow equation does not by itself acquire Astra's applied-force heat
interpretation. No same-bath-Gibbs path-distance theorem was identified in the
read material.

**Ding, Liu and Xing, _Unified theory of thermodynamics and stochastic
thermodynamics for nonlinear Langevin systems driven by non-conservative
forces_, Phys. Rev. Research 4, 043125 (2022).**
[Primary text](https://journals.aps.org/prresearch/pdf/10.1103/PhysRevResearch.4.043125).

Read the introductory near-zero-EP remark, §V.A equations (5.1)–(5.22), and
§VII.B–C equations (7.17)–(7.39). Their statement allowing very small EP in
nonequilibrium occurs in a broader entropy-pumping discussion. The explicit
position-independent force example has stationary EP f²/(γT); later examples
allow momentum-dependent forces, and the circular/shear sections use
overdamped reductions. Their shear discussion explicitly distinguishes
reversal/heat interpretations. None of these inspected examples is the target
fixed-bath rapidly varying position-force family with an optimization over all
same-bath Gibbs path models.

**Busiello, Ciarchi and Di Terlizzi, _Unraveling active baths through their hidden
degrees of freedom_, Phys. Rev. Research 6, 013190 (2024).**
[Primary manuscript v2](https://arxiv.org/pdf/2310.00620),
[published source](https://doi.org/10.1103/PhysRevResearch.6.013190).

Read the linear coupled setup (1), heat definition (2), reciprocal elimination
(3)–(6), and the discussion/example with A21=0 on manuscript page 4.
They explicitly consider an equilibrium OU hidden variable driving another
variable nonreciprocally; this already distinguishes hidden equilibrium from
equilibrium of the coupled system, and warns that eliminating dynamics can
change thermodynamic interpretation. The main setup inspected is overdamped
linear dynamics. It does not directly supply the new kinetic two-metric theorem
or the all-native-potential distance statement. Do not advertise one-way
equilibrium driving or hidden thermodynamic ambiguity itself as an addition.

**Loos and Klapp, _Irreversibility, heat and information flows induced by
non-reciprocal interactions_, New J. Phys. 22, 123051 (2020).**
[Primary manuscript v2](https://arxiv.org/pdf/2008.00894),
[DOI](https://doi.org/10.1088/1367-2630/abcc1e).

Read the setup/introduction and §VII's underdamped models and heat formulas
(44)–(51), together with its stated relation to the earlier temperature-rescaling
map. Nonreciprocal linear forces, memory, energy/information flows and inertia
are established mechanisms. The explicit underdamped heat example uses a
restricted coupled harmonic family and compares temperature-rescaled
representations. No full-path distance optimization against the fixed original
bath Gibbs family was identified in those sections. This is useful physical
background, not direct subsumption.

## Regularity and a recent spectral screen

**Cattiaux, Guillin, Monmarché and Zhang, _Entropic multipliers method for
Langevin diffusion and weighted log Sobolev inequalities_, J. Funct. Anal. 277
(2019), 108288.**
[Primary manuscript](https://arxiv.org/pdf/1708.01058),
[DOI](https://doi.org/10.1016/j.jfa.2019.108288).

Read abstract and setup in §1, including equation (1), the fixed conservative
potential and Gibbs law. This addresses entropic relaxation under a known
conservative Langevin dynamics, with improved potential regularity assumptions.
That is different from showing that a sequence of initially nonconservative
stationary dynamics approaches some conservative path model. The current pass
did not read its full proofs and makes no claim about every corollary.

Astra's qualitative repair is itself an application of a standard compactness
schema: on a compact model class, continuity of the path-law map in TV and
lower-semicontinuity of entropy, together with identification of the zero set,
force small-entropy models to approach that zero set. The work is in verifying
these properties for the stipulated kinetic interface, particularly initial
stationary-law TV via noise smoothing. It is not a new compactness or
hypocoercivity method, and it supplies no effective modulus. No directly
subsuming native-model-closure theorem was found in the targeted search.

**Sekizawa, Ito and Oizumi, _Koopman Mode Decomposition of Thermodynamic
Dissipation in Nonlinear Langevin Dynamics_, arXiv:2510.21340v2 (2025).**
[Primary manuscript](https://arxiv.org/html/2510.21340v2).

Read §§II and III's setup, virtual dynamics and main result (10)–(11).
Their mode decomposition uses a virtual deterministic housekeeping-current
dynamics for nondegenerate overdamped, all-even variables. The cost of a
virtual oscillatory mode is proportional to frequency squared times its
intensity. This is neither the compressed resolvent of an autonomous kinetic
equilibrium driver nor an optimization over native thermal Gibbs models. The
two results should not be conflated merely because both use spectral objects.

Da Costa and Pavliotis, [arXiv:2212.05125v3](https://arxiv.org/html/2212.05125v3),
was screened through its abstract/contents and the explicit scope cautions in
§§5.2/6.2. Its ordinary reversal convention, unless modified by a parity map,
can give infinite phase-space reversal divergence for equilibrium kinetic
Langevin dynamics. It is not a substitute for the physical parity/bath contract.

## Assessment and remaining boundary

The strongest equally informed conventional route can reproduce Astra's native
equilibrium optimization directly: use the known path-space force-matching
functional, exploit the source's exact position marginal, and integrate the
transverse potential derivative over its periodic coordinate. The orthogonality
then fixes the minimizer and its residual. Heat follows independently from
ordinary stationary linear filtering of the actual driver correlation.

The proposed scientific content is the **joint consequence** of those two
calculations: the same force has two inequivalent norms, which determine
different physical questions; unrestricted fine force structure separates
them; a declared structural restriction or acquired dynamical Gram record
reconnects them. Positive finite-dimensional coercivity and generalized
eigenvalue calculations are standard linear algebra once the forms are known.
The complete acquisition and physical interpretation are necessary for the
capability claim, but no algorithmic speedup has been established.

The targeted searches included fixed-bath small EP, high-frequency
underdamped forcing, force-matching relative entropy, entropy/resolvent norms,
compactness/Lipschitz repairs, and nonreciprocal hidden-driver examples.
Search results were used for navigation; only the primary portions described
above support this note. Harada–Sasa and standard Green–Kubo/linear-filter
antecedents remain acknowledged in physical_frontier/PRIMARY_SOURCE_COMPARISON.md;
this pass did not repeat their earlier read.

The remaining novelty uncertainty is precise: whether an earlier source proves
the fixed-bath/full-path native-Gibbs separation and/or the exact
compressed-resolvent-versus-native-cost assembly at this source-class scope.
This limited pass did not resolve historical priority. It found no reason to
withdraw the mathematical result, but it does require keeping the established
ingredients and the actual joint addition separate.

