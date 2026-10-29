# Ordinary comparison, exact admission, and surviving gate

The result is an explicit noisy asynchronous CLASSICAL register/copy
operation, with the strong offline fault-label quantifier and a multipoint
output guarantee. It is not claimed as a new generic majority mechanism.

## Strong conventional method, read before completing the construction

[Cruise--Ganesh, *Probabilistic consensus via polling and majority rules*](https://arxiv.org/html/1311.4805),
primary Sections1.1--3, already uses independent rate-one Poisson clocks,
samples with replacement, and explicitly includes majority of THREE polls.
Its main analysis is on the complete graph. Crucially, Section1.1 ALREADY
proposes implementing polls by random walks on an expander and charges
their mixing/communication cost. Thus neither asynchronous polling nor
the expander/random-walk combination is a new representation here. An
equally informed ordinary method receives our exact graph, error contract
and source bits, and can reproduce the scalar branching argument. We do
not withhold random-walk amplification, a stronger graph, or classical
birth/death exit analysis from it. No practical or asymptotic superiority
over that informed method is claimed.

[Doerr--Goldberg--Minder--Sauerwald--Scheideler, *Stabilizing Consensus With
the Power of Two Choices*](https://www.cs.ox.ac.uk/people/leslieann.goldberg/papers/SelfStabilizing.pdf),
primary Sections1.1--1.2 read, admits sustained adversarial state
corruption. Its stated model is synchronous rounds and complete contact
information, with up to sqrt(n) currently corrupt processes in its main
result. That is a strong incumbent, not an acquired Poisson threshold
for the native geometrically local quantum decoder. The tasks differ in
geometry, scheduling, corruption budget and initial-state contract.

The named ordinary Margulis--Gabber--Galil graph bound is imported through
the already frozen c_new_theory/SPECTRAL_SOURCE_BRIDGE.md. That packet
visually verified Gross--Eisert Section2.2's primary statement and the
integer reflection conjugacy for every modulus. Here we reuse exactly
that mathematical graph, not its former measurement implementation. No
old source menu is used as a current literature-completeness premise.

## What the asynchronous classical priors actually pay

[Gacs, *Reliable Cellular Automata with Self-Organization*, corrected
24 January2024 printing](https://cs-web.bu.edu/faculty/gacs/papers/long-ca-ms-24.pdf)
is an explicit strong conventional construction of noisy asynchronous
one-dimensional computation. The acquired primary Def2.20 (printed p19)
defines its continuous-time perturbation by FIXED small changes of the
transition-rate matrix. Cor7.21 (p75) invokes that CCA perturbation. These
two passages were checked visually as well as by extraction. They do not
by themselves state our supremum over labels chosen after the entire
nominal clock/coin schedule is revealed. The broader strong-medium
machinery might support another admission proof; it has NOT been declared
impossible or fully audited away. We simply do not import that stronger
quantifier as a free threshold. Our Section2 instead pays it directly by
monotonicity of the specific binary controller.

[Gharavi--Anantharam1992](https://content.wolfram.com/sites/13/2018/02/06-3-5.pdf),
primary Introduction and Sections2--3 read, studies SYNCHRONOUS computation
with bounded asynchronous communication delays. Its wording does not
grant Poisson update timing. [Gray1999's primary abstract](https://link.springer.com/chapter/10.1007/978-1-4612-2168-5_18)
warns that merely replacing a discrete update by continuous time does not
preserve stability. Its complete chapter was not acquired: a public archive
link was404 and Springer exposed a preview. No claim of absence of a
continuous-time Toom result follows from that access limit.

[Swart--Szabo--Toninelli, *Peierls bounds from Toom contours*](https://arxiv.org/html/2202.10999v2),
primary history/set-up and the older v1 Sections2.6/6 read, explicitly
distinguishes a random identity/no-update rule from a deterministic eroder.
Its v1 continuous-time contour calculation treats the stated cooperative
branching/contact model, not our quantum syndrome rule. The 2025 companion
[random-contour paper](https://arxiv.org/html/2501.09660) likewise shows why
intrinsic randomness is an actual theorem input. These readings prevented
using synchronous erosion or average update velocity as a Poisson memory
certificate. We do not issue a present-day world-open/closed classification
of the continuous-time NEC model from these scoped readings.

For the multipoint result we use the standard Finner/read-q inequality.
The exact nonnegative-function formulation is given in the acquired primary
[Gavinsky--Ito--Wang2013, Section3.3, Lemma3.3](https://eccc.weizmann.ac.il/report/2013/044/download/),
which credits Finner1992. Its printed page6 was visually checked. The
related primary [Gavinsky--Lovett--Saks--Srinivasan2012, Theorem1.2](https://arxiv.org/html/1205.1478)
gives the equal-marginal read-q product bound. This probability inequality
is an ordinary import, not a newly inferred independence assumption.

## Resources and real remaining operation

The register contains only noisy bits and performs measured Boolean
updates at constant per-bit Poisson rates, robust here to fixed rates in
[15/16,17/16]. No noiseless timing/program-state bit is introduced. The
error class covers arbitrary q-bit replacements at independently clocked
locations, even with future-dependent labels. It does not cover arbitrary
deletion of update clocks, permanent broken transition functions, or an
unwarranted physical bath. Each nominal channel has an explicitly finite
144-bit random draw, at most four-bit support and graph radius16
(radius17 for a copy between layers). Random-number generation and atomic
read/update access are part of the nominal model, not acquired apparatus.

Native three-dimensional geometry is not supplied by an expander. The
proof pays a specific obstruction to the proposed reversible-walk port:
on a bounded-range L^3 torus, constant spectral mixing requires Omega(L^2)
walk steps. Calling those reads atomic at rate1 would hide precisely the
unavailable communication resource. This does NOT rule out directional
Toom dynamics, a Gacs hierarchy, active fault tolerance, or another
nonreversible geometric eroder.

The buffered-copy theorem requires an unchanged retained source bit.
All-time local-stochastic correctness of many such independent pairs is
paid, but dynamic feedback changes the dependency graph behind that bound.
An actual syndrome controller must process changing syndrome streams,
distribute corrections at real local-bit rates, and restore its own
state. Terminal global mathematical majority is not a free noisy readout
or a data-Pauli feedback algorithm.

Accordingly this packet closes a restricted classical register/restoring-
copy operation at the stated graph access, while the programme's central
three-dimensional joint data/controller persistence estimate delta_cl
remains NOT_ACQUIRED. The ordinary core wins any generic novelty claim.
The enabling value retained is a paid, explicit, strong-quantifier
primitive and a precise geometry/dynamic-feedback boundary, not a claimed
autonomous quantum-memory threshold.
