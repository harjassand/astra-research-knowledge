# Native dynamic-flux influence: concrete bridge from clock rods to data excursions

2026-11-02. **Candidate lemma with derivation and exact remaining gates**, not certified as a proved native generic-perturbation theorem.

## New target using actual supplied clock algebra

The existing clock result controls F_beta(s) only for syndrome constant in imaginary time. A data Pauli insertion changes s, so a beta-uniform expansion needs an influence functional for piecewise constant s_a(tau). Let D_a={tau:s_a(tau)=-1}, let L_D=sum_a |D_a|, and let N_jump count syndrome-bit jumps (bounded by a constant times number of local data Pauli vertices). Seek

  log |Z_clock[s]/Z_clock[+]| <= -2 J_eff L_D + C_end N_jump,
  J_eff >= (1-delta)J0 > 0,

uniformly in beta, volume, and the piecewise constant history. The crucial endpoint coefficient C_end should be O(clock occupied-fraction moments), NOT beta J0. A matching lower bound or controlled complex log is useful for normalized expansions. This is a statement about a scalar clock trace with prescribed syndrome history, before generic clock/bath matrix insertions.

## Why supplied rod moments are exactly relevant

In the prefix-gauged clock, the closing clock link carries S_a. For a first-return ordinary rod from vacuum, a winding excursion carries one factor s_a at its closing-link endpoint. A nonwinding excursion using that link at both ends carries s_a(t_start)s_a(t_end). With constant s the latter is one, but with dynamic s it changes sign only if the rod straddles a syndrome jump. This endpoint factor must not be omitted.

For the singleton winding contribution, integrate the start time around the circle. Time translation makes the negative flux contribution exactly proportional to |D_a|: each marked endpoint spends fraction |D_a|/beta in D_a. The infinite-time coefficient is J0; the finite-beta missing-tail correction is already bounded in resonant_rod_bound.md.

For every nonwinding rod of length ell, the set of start times for which its endpoints straddle at least one jump has measure at most ell times N_jump,a (union bound on the circle). Therefore the integrated absolute change of its singleton activity is at most

  2 N_jump,a integral ell rho_a(ell) d ell = 2 M1,a N_jump,a.

After the existing KP length tilt, replace M1,a by M1,a(b) exp(a0). For resonant heterogeneous clocks this is at most a constant times eta^2/M per syndrome-bit endpoint. This is beta independent and dimensionless. Full-circle wraps can be charged separately by their exponentially small activity; their endpoint dependence must be written explicitly.

Connected-cluster corrections can be split by marking either (i) a winding rod whose endpoint lies in D, or (ii) a nonwinding rod whose endpoints straddle a jump. Case (i) gives the same relative marked-winding correction delta J0 L_D as in the static theorem. Case (ii) gives a rooted tilted first-moment bound C M1 N_jump. Since all flux factors have modulus one, the same absolute KP majorant applies for every prescribed history.

This suggests a concrete generalization of the existing marked-winding proof, rather than rebuilding the clock compiler.

## Cautions that prevent declaring the lemma earned yet

1. The precise native pair-sign formula must remain flux-independent for time-dependent s after all chronological data Paulis are moved out. Static flux independence alone is not the full assertion. Data Paulis may introduce extra endpoint phases; these should be local and chargeable, but must be derived.
2. A prescribed time-ordered product of positive operators need not automatically define a positive scalar trace in a signful multi-clock model. KP supplies a nonzero complex partition function and control of a chosen logarithm, not positivity of every conditional history weight. The data path expansion is generally signed.
3. The cluster marking argument must avoid attributing a static bulk sign to a backtracking rod with time-separated endpoints. Its entire contribution belongs to the endpoint term, as above.
4. Nonzero-clock-at-origin wrapping trajectories may touch the closing link differently; their exact temporal flux dependence must be included, not discarded.
5. Generic native perturbations include arbitrary clock and bath matrix units, not only data Pauli vertices. Those are actual local time pins. Their costs should be bounded via local clock propagator kernels/resolvents relative to the existing background, rather than assigning full beta columns.
6. Even if the stated influence bound holds, the remaining data-syndrome spacetime gas must be constructed and normalized. A raw absolute worldline expansion still loses an extensive vacuum factor. Zero-energy stabilizer/logical excursions and logical matrix normalization remain separate issues.

## Why this would be substantive progress

Given this influence estimate, a syndrome interval of duration ell pays exp(-2J_eff ell) and each jump vertex gets only an O(1) endpoint renormalization of v. Resolvent integration therefore produces v/J_eff, not beta v exp(C beta J_eff). A pinned virtual pair has two resolvent integrations and weight O((v/J_eff)^2). This is the native mechanism needed by the full-Gibbs endpoint-pinned contour framework. The clock's small gap mu and induced check energy J0 must remain distinguished: mu controls clock endpoint dressing; J0 controls data-defect excursion lengths.
