# Independent whole review of fixed-coupling initialized clock memory

29 October 2026. Reviewer C. **ACCEPTED at the parameter-qualified ideal
quantum-algorithm/specified-controller model scope.** This reviews the actual
composition, not merely the titles of its accepted components. One explicit
lower-window clarification was requested and has been incorporated: the
chosen fixed coupling must also satisfy beta/(4lambda^L)>=T0.

Governing input is root_clock_initializer/FIXED_COUPLING_COMPOSITION.md at
the hash pinned in RECEIPT.json. I whole-read that file, the actual full-
weight bridge, its independent full-trace acquisition/bit-operation
supplements, the conditional preparation chain, the source decoder definition
including its level-2 modification, and the specified clock storage corollary.
The previously accepted static/KT/cylinder/receiver modules remain admitted
at their actual scopes; I do not reopen their validation.

## 1. The exact module, with the logical multiplicity paid

Let Sigma be the actual admissible JOINT source syndrome set, including all
redundant-check relations. The one-logical-qubit source has a rank-two
projector P_s for every s in Sigma. Fix the SAME decoder Pauli C_s used
in the storage logicals and a known ground-code isometry E0. Put

    E_s=C_s† E0.

These are isometries onto orthogonal syndrome sectors. Therefore the map

    W(|psi>_L tensor |s> tensor |phi>_clock)
          =E_s|psi> tensor |phi>

is a unitary identification of the full source-clock Hilbert space with
logical-qubit tensor syndrome-clock environment. It is not an additional
coherent gate oracle required by the preparation algorithm.

In the exact prefix gauge, the Hamiltonian is

    H_gauge=sum_(s in Sigma) P_s tensor Delta H_s.

Thus for Z_s=Tr exp(-tH_s), t=beta Delta, its full Gibbs state is

    rho_gauge=[sum_s P_s tensor exp(-tH_s)]/[2 sum_s Z_s].

Define p_s=Z_s/sum Z and sigma_s=exp(-tH_s)/Z_s. The environment state is

    tau=sum_s p_s |s><s| tensor sigma_s,

and rho_gauge=W[(I_L/2) tensor tau]W†. The constant source-sector logical
multiplicity two cancels from the classical law. No sign assignment outside
Sigma is sampled and no additional degeneracy factor is missing.

The physical identification is W_phys=U†W for the SAME finite-depth prefix
gauge U. Its corrected Paulis W_phys(sigma_alpha tensor I)W_phys† are
precisely the shared decoder-defined full logical algebra used by storage.
They commute with the full physical Hamiltonian at every clock energy.
The environment is the real full Gibbs environment, not a ground-band one.

For an arbitrary unknown input and reference, the target encoder is exactly

    Enc(omega)=Ad_(U†) sum_s p_s [E_s omega E_s† tensor sigma_s].

The preparation branches on a CLASSICAL s and acts on clocks only in its
conditional Gibbs step. It never measures the logical state. Syndrome-
dependent global phases therefore cancel in the mixture. This does not
license replacing C_s by a different representative which differs by a
logical Pauli; the same chosen C_s is load-bearing.

## 2. There is no hidden exponential source encoder

The analytical W above need not be coherently synthesized. The actual
algorithm first samples s, then evaluates one C_s and applies one Pauli
after preparing E0. Stabilizer symplectic elimination supplies E0 as an
ordinary polynomial-size Clifford isometry aligned with the fixed bare
logical pair. Dependent supplied checks are handled by choosing an independent
generator basis; no enumeration of all 2^(n-1) sectors is involved.

I checked the actual primary decoder definition, 2605.10943v1 Section 4.1,
Eq(118)--(122), and its Section 5.1.1 modification. At every higher level,
the syndrome determines bounded-cell corrections and a coarse syndrome.
Local fill enumeration has a fixed finite cost because the primary-qualified
subdivision ell is fixed. The modified base decoder is a lookup on the
CONSTANT level-2 code, not a minimum-weight search on the level-2k code.
Its table can be selected once with the source's stated correction property;
it can be enormous but is independent of system size.

Lifted corrections can be accumulated recursively as

    g_i=f_i+F_(i-1) g_(i-1),

using the explicit sparse local cochain maps. Each replacement has constant
cell size at fixed ell, and sum_i n_i=O(n). This yields polynomial work,
including true bit/address costs, without separately lifting every term
through a dense exponentially large tensor space. The two CSS corrections
give an n-bit X/Z Pauli word, applied with O(n) ideal one-qubit Pauli gates.
Tie orders and the base table must be the same ones fixed in the storage
module. The auxiliary sampling history continued down to level zero is not
silently substituted for the level-2-modified memory decoder.

An ideal final logical decoder is also explicit: apply U, measure the
nominal syndrome, compute this same C_s, apply it, perform the Clifford
decoding, and discard clocks/ancillas. This equals logical partial trace in
W_phys coordinates even on arbitrary inter-syndrome-coherent inputs, because
the discarded syndrome environment removes those off-diagonal blocks. It
requires no clock diagonalization or clock-conditioned logical inverse.

These are ideal circuit resources. Finite-range routing and gate/reset/noise
qualification are not inferred from stabilizer linear algebra. Polynomial
abstract gate work is the claimed preparation contract.

## 3. The fixed-parameter intersection exists in the claimed order

The enlarged history graph includes the native clock-interaction edges, not
a new clique on every acquired long bond. Its degree is fixed independent
of the truncation cutoff and lambda. A bond's DECLARED native support is
connected in that graph. Thus the sampler temperature B0 may be chosen first.

Then beta=4ln B0 is fixed in defect-energy-one units, the weighted cylinder
slab constants are fixed, and lambda can be chosen smaller than all admitted
positive KT/Peierls, full-trace Gamma and cooling gates. For the conditional
cooler take a=L and B=beta/4. The additional lower endpoint

    t=beta/(4lambda^L)>=T0

is another fixed positive upper bound on lambda; it is now explicitly named.
Decreasing lambda further preserves the strengthened slab/Gamma conditions
once their fixed onset is imposed. No temperature/coupling parameter need
grow with n or target accuracy. The existence is effective using the component
finite-constant compilers, although those constants have NOT been evaluated
for the old literal lambda_T.

Delta, t, normal-form order, local catalogues and LR constants may be
catastrophically large fixed costs. "Fixed" is not a claim of practical
magnitude. The L=8 clock is one bounded-dimensional QUDIT; re-labeling it
with three bits does not make this a two-body-qubit Hamiltonian.

## 4. The correct marginal and a constructive positive circuit

The full-weight component supplies the actual p_s proportional to Z_s,
including all excited levels, through connected full-free-energy increments.
Its accepted finite local trace/inertia routine pays the coefficient input,
global truncation, unresolved-sign omissions and rational rounding. The
streamed positive history/bond chain pays internal activities, coin precision,
expected work and a single-run timeout fallback. This is not a ground-energy
marginal with an uncounted extensive excitation error.

Conditional on the sampled CLASSICAL s, the separately reviewed cooling
algorithm prepares the FULL sigma_s with uniform trace accuracy. Its native
term list, order-116 dressing compiler, flat filters, exact KMS heating,
total-number coherent cancellation and finite reset/LCU circuit costs remain
charged. A partition-function routine alone would not have supplied this
quantum state; the composition actually calls the distinct conditional
preparation operation. The inverse prefix gauge is then applied as a known
finite-depth quantum circuit.

The unknown logical input can be supplied after classical acquisition, so
the construction need not grant a protected quantum waiting register while
the classical law is compiled. Equally, an always-returning capped sampler
can use the valid zero syndrome on timeout and still encode the logical
qubit. No failed branch erases or postselects the unknown input.

## 5. Diamond error, without a hidden logical-dimension factor

For any purified logical input, disjoint source-sector isometries preserve
trace norm. A classical TV error delta therefore contributes at most 2delta
to the encoder diamond norm. A uniform clock-state error e contributes at
most e: the logical/reference density matrix is a trace-one tensor factor
in each branch, independent of the clock preparation. There is no factor
equal to source Hilbert dimension or number of syndromes.

The displayed TV epsilon/8 and conditional trace epsilon/4 consume epsilon/2
in total. A prefix-gauge channel budget epsilon/4 leaves margin below epsilon.
Clifford/Pauli operations may be exact in the ideal gate model; if approximated,
their channel error must consume that remaining margin. The global clock-state
error already includes its own dressing, Hamiltonian simulation, coefficient
and reset budgets. Unitary conjugation preserves these estimates.

The classical acquisition/sampling and conditional circuit bounds are uniform
in s. With the known fixed parameters they are polynomial in n,1/epsilon,
in expectation for the unbounded sampler, with its explicit bounded-work
single-cap alternative. This does not claim that exponentially small epsilon
has polynomial-in-n cost for the combined initializer. The chosen final
epsilon_n=n^-p is exactly what makes the full initialization polynomial.

## 6. The actual storage interface and composition

Preparation and storage use DIFFERENT algorithmic controllers. After preparing
Enc_hat, the model switches to the exact Gaussian CKG generator constructed
from this same Hsim and beta, with its whole coherent correction and constant
per-site seed rates. No natural bath or stationary state of an unknown perturbed
Hamiltonian is assumed. The source-clock Pauli module above is exactly the
one in b_conventional/clock_thermal/DYNAMICAL_COROLLARY.md.

Importing that accepted specified-controller theorem gives all-input storage
diamond error 2sqrt(2)exp(-b 2^(k/3)/4) over its stated interval. For the SAME
storage propagator S_t and CPTP decoder D,

    ||D S_t Enc_hat-id||_diamond
       <=||Enc_hat-Enc||_diamond+||D S_t Enc-id||_diamond.

Thus initialization error is added once and is NOT multiplied by storage
time. No generator-perturbation Duhamel estimate is being smuggled in here.
With epsilon_n=n^-p, total error vanishes, and that inverse-polynomial
preparation error generally dominates the exponentially smaller storage term.

The accepted source bound n_data<=5g^(2k) converts the storage interval to
exp(c n_data^alpha), alpha=ln2/(6ln g). Clock count is at most a constant
times data count, so using total simulator sites only changes fixed constants.
Fixed lambda also keeps the physical LR parameters independent of n; the
growing-penalty branch's logarithmic velocity debt is not imported.

## 7. Exact acceptance boundary

This composes a real model-wise constructive ideal quantum encoder with a
stretched-exponential specified-controller storage theorem at fixed couplings.
It does not establish a microscopic bath, fixed finite-radius controller,
unknown charged-error robustness, noisy/efficient native initialization,
useful constants, hardware fabrication, practical advantage or historical
novelty. The full native quantum initializer and its additional coupling
qualification have not been executed. No new native case or trajectory was
needed for this composition review.
