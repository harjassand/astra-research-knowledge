# Scope, ordinary methods and costs

29 October 2026. This wave constructs the full finite-temperature bridge
for the native Pauli-clock Hamiltonian form. No Hamiltonian fixture,
trajectory, finite code level, source complex or old compiler is rerun.

**What the strongest ordinary route already supplies.** The fixed transfer
slab, quantum contour representation, and scalar low-temperature polymer
expansion are established. Governing primary readings are BKU1996
(Microsoft Research public PDF, Sections3--5), Helmuth--Mann2201.06533v2,
and scalar KP/Ueltschi0304003v3. The direct construction in PROOF.md pays
the inhomogeneous graph, arbitrary formal sign assignments, operator-to-
scalar reduction, actual primitive dimension cost, connected logarithmic
multi-polymer lifting and local marked-check tail. It does not claim the
general contour mechanism invented, nor historical priority for this
composition. Priority is UNKNOWN.

The newer Mann--Waite2601.21140v2 FPTAS is also retained as an informed
comparator. Its 'arbitrary temperature' theorem has a sufficient lambda
window exp(-2qt)/(e^4 t d binom(q,2)); it does not by that statement supply
a temperature-uniform window at our t=beta Delta. The low-T slab method
does, at the price of an extremely small additional fixed coupling.

**The mathematical operation.**

    log Tr_clock exp[-beta Delta H'(lambda;S)]
      =-beta Delta E(S)+Theta(S),
    sup_c sum_(X containing c)|Theta_X|
      <=2M B0 exp(-M/2), M=floor(beta Delta/delta0).

The count is per supplied check, not all clock sites. It is before physical
symbol relations, includes the complete Gibbs trace, and is uniform in
code size. Peierls witness deletion has dimensionless cost at least
(3beta/4-4M B0 exp(-M/2)) per deleted check. This supplies the actual
static input for the native-clock endpoint, rather than borrowing its
ground-band gap or a global N exp(-beta Delta gap) bound.

**Actual executed primitive.** `compile_thermal_constants.py` is a general
stdlib exact-integer/Fraction gate compiler. It consumed only the admitted
uniform bounds q=43,d=344,L=8, not an instance Hamiltonian or ground-state
table. `THERMAL_CONSTANTS.json` records 0.007957834s for the compiler function
after imports (imports and JSON I/O are unmeasured), delta0=393,
lambda_T denominator bits=152079, chosen Delta integer bits=1216625,
Delta*lambda bits=1064546, Bstar=1/28903, and Mcrit=2433258. Exact integer
comparisons show beta>=1 pays the cylinder-height condition; additionally
beta>2beta_c pays the supplied source counting threshold. beta_c and the
source geometric admission remain their accepted input, not new numerical
measurements. No giant decimal output or underflow approximation is used.

These penalty magnitudes are physically prohibitive sufficient bounds,
not a practical prescription or a lower bound on the resources needed by
better analysis. The old literal lambda_* denominator has only1195bits
and has NOT been qualified by this thermal gate. If one also wants the
separate zero-T physical-perturbation theorem, take lambda below its
additional unevaluated lambda_FF gate as well. All penalties remain
constant in system size once chosen.

**Dynamic operation actually specified.** The composition uses the
established exact Gaussian CKG generator for this SAME Hsim, including
its coherent correction, frequency weights and whole-jump cross terms.
It has a constant number of data and clock seed operators per site;
the root's admitted LR/tail receiver is applied at the actual Hsim scales.
Both corrected logical Paulis commute exactly with Hsim, so no classical-
bit substitution or logical-twirl approximation is needed. The resulting
full-qubit storage interval is a model-wise theorem for that exactly
stationary quasilocal algorithmic thermal dynamics.

The complete logical thermal environment tau_beta is needed by the CPTP
encoder. Its physical initialization is UNACQUIRED; the slow Gibbs sampler
does not make it a free reset. Native finite-coupling/Davies bath access,
fixed finite-range controller, implementation errors, practical tolerance,
efficient encoder/readout and hardware memory are UNACQUIRED. Arbitrary
physical Hamiltonian errors are NOT included in the finite-T theorem.

No physical action or external write occurred. No comparative computational
or hardware advantage is asserted over an equally informed contour/CKG
construction using these same inputs.
