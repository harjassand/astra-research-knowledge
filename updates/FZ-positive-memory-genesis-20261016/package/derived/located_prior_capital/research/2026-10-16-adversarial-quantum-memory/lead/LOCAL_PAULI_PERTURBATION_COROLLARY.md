# Local syndrome conditioned Pauli perturbations

Principal-investigator derivation, 16 October 2026. Status: corollary of the
reconstructed sweep theorem under the same named imports. Its added steps
survived separate direct extension audits in trajectory/ and envelope/.
Historical originality of this corollary is unestablished. It does not presume
that arbitrary small Lindblad perturbations admit Pauli trajectories.

## Statement

Retain the ideal sweep generator with attempt rate kappa. Fix a finite integer
q independently of L. Add local jumps

    K_(x,a) = Q_(x,a) f_(x,a)(S),

where Q_(x,a) is a Pauli string, f_(x,a) is a function of commuting stabilizers,
and the entire jump lies in the radius-q neighborhood of fine cell x. Let

    sum_a ||f_(x,a)||_infinity^2 <= nu

uniformly in x and L, with finitely many terms per cell. Types and rates may
vary spatially. The f may depend on both CSS syndromes. A single Q may toggle
many nearby qubits and both sectors simultaneously. Independent single-face
noise can be included among these terms and charged to the same budget.

For each fixed q, there is epsilon_q>0 such that nu<=epsilon_q*kappa implies
the same form of code-initial lifetime bound, with constants depending on q
and the budget but not L,T:

    || Dec_L exp(T L_total) Enc_L - Id ||_diamond
       <= min(2, A_q L^4 (1+kappa*T) exp(-c_q L)).

As in the original statement, L=b_q M is a compatible family, all six logical
qubits and arbitrary references are covered, and final recovery is ideal.

## Proof

The invariant-family identity in PRINCIPAL_RECONSTRUCTION.md applies to each
K: it induces the Pauli transition Q with rate |f(s)|^2. Uniformize using an
independent Poisson proposal stream at its maximum rate, accepting with
probability |f(s)|^2/||f||^2. These streams and independent uniform acceptance
marks construct the exact joint Pauli CTMC. There is no need for a sector
marginal to be a Markov process.

At each fine cell, superpose proposals and pad to a common rate nu with null
proposals. One can generate the type of each accepted proposal by local marked
thinning. In the analytical envelope, set EVERY vertex in a fixed radius-(q+2)
box occupied on EVERY rate-nu proposal at that cell. The box contains both
sector boundaries of all possible Q at that anchor, with harmless extra dual
lattice rounding. These conservative births are homogeneous independent
Poisson events, irrespective of the state-dependent acceptances or spatially
varying jump types.

The original sweep maps dominate each actual correction exactly as before.
Each Pauli proposal changes syndrome only inside its prescribed box, so its
conservative envelope birth dominates either its accepted action or a null
proposal. This proves joint pathwise support inclusion.

Enlarge the primitive birth guard to count every anchor whose radius-(q+2)
box meets the original guard. Keep the original slow and fast flags. No fault
proposal in this enlarged guard implies that the microscopic envelope within
the relevant region has exactly the original correction dynamics. An outside
birth reaching a target still requires the excluded ordered clock chain.
Thus the same uniform forcing and whole-slab proofs apply. A safe birth term is

    delta_noise <= nu * ((2R+5)b + 2(q+3))^4 * Delta.

The extra coarse primitive radius can be bounded by R+q+6 for b>=1, hence is
fixed before b increases. Fix q,C,R and the resulting dependence/connectivity
radii first; take p_* from HT and delta_* from LSS; increase fixed b to suppress
the unchanged clock terms; finally choose nu/kappa small enough for the displayed
birth term. This preserves the required noncircular order of constants.

The larger q does not require increasing the whole-slab representative radius:
any proposal directly relevant to a good target is excluded; a bad target is
already represented by a forced zero at the next layer. It does enlarge the
primitive patch used by stopped replay. Take M sufficiently large for that
fixed enlargement.

A fault event's 2-chain support now has bounded diameter a_q rather than one.
The decoder transition box has side at most 2r+a_q, which remains below
rho=L/8 for r=L/32 and sufficiently large L. Hence all accumulated homology
and quantum-channel arguments are unchanged. This proves the corollary under
the same published imports and the original deterministic bridge.

## Restricted correction calibration errors

The statement can handle some imperfect intended dissipators without assuming
that their full generators split into independent errors on arbitrary inputs.
For every intended jump Q Pi, suppose the implemented jump is

    J_tilde = sqrt(kappa) Q f(S),   ||f(S)-Pi|| <= delta < 1,

with f a local function of the commuting stabilizers and the SAME Pauli Q.
Set kappa_minus=kappa*(1-delta)^2. On every definite syndrome, the exact rate
splits into a base ideal rate kappa_minus*Pi and a nonnegative residual:

    r_residual(s)=kappa*|f(s)|^2-kappa_minus*Pi(s) >= 0.

On active syndromes the residual is <=4*kappa*delta; on inactive syndromes it
is <=kappa*delta^2, also <=4*kappa*delta. Fourteen intended terms per cell
therefore contribute at most 56*kappa*delta to a dominating proposal budget.
Their residual jumps can be written Q sqrt(r_residual(S)). Apply the corollary
with base correction rate kappa_minus and the total residual-plus-data budget.
For sufficiently small positive delta and data noise, the exponential form
survives. This is equality of rates and of the evolution on the invariant
Pauli family, not equality of the full quantum generators on syndrome-coherent
inputs.

This class includes false activations, suppressed intended activations, nearby
correlated Pauli faults, and cross-sector syndrome dependence. It retains exact
commuting stabilizer functions and one Pauli string per jump. A coherent sum
of different Pauli actions, noncommuting projector errors, amplitude damping,
or leakage need not preserve the invariant family and is not covered.

## Scientific scope

This is a structural robustness corollary with a qualitative positive threshold.
It is not a useful numerical threshold, fabricated imperfect reservoir, generic
coherent-noise theorem, or general conversion of every classical eroder to a
quantum memory. The quantum/classical lifting idea has predecessors; the new
review target is the preservation of the specific forcing and homology bridge
under this larger proposal class. Priority requires separate checking.
