# Root join: noisy autonomous memory with small-qubit syndrome acquisition

2026-11-01. Proposed joined theorem for independent review. The previously delivered Tanner/witness theorem remains unchanged. This construction removes its native syndrome-input primitive at a specified bounded-arity GKSL level; it does not establish a useful hardware regime or microscopic two-body realization.

## 1. Governing components and actual operations

Use the previously audited Tanner witness controller and its protected low-W component, not an arbitrary LDPC code. Keep its explicit code-family, tensor-robustness, finite-degree and initial/readout assumptions. Let true improving move count satisfy N_down>=c0 W inside that component, and let each selected move have bounded witness support and bounded W change.

Implement each witness mask virtually: y=a XOR sum_j b_j x_j, with a physical flag b_j per candidate. A flag flip applies the mask in this representation. A finite-fanin Boolean DAG computes the move predicate from actual syndrome caches and virtual witness bits. Its physical wires are overwritten asynchronously by TP Boolean repair channels. All flags/wires/cache bits are noisy physical registers; no perfect metadata or classical controller is supplied. Include the entire finite but potentially huge truth-table/DAG/flag count in local constants and hardware cost.

Replace each true-check cache input by a private probe and actual qubit clock. For weight w, take M=w+2 forward operations: imperfect preparation, w controlled single-data-Pauli factors, X readout/cache overwrite. The clock comprises M qubits plus a mode bit. Its local 100 wall predicates and endpoint mode flips give 2M+2 legal phases, of which D=2M+1 have fast rate k; only initial preparation departure has slow rate r. Readout is before the return leg. All instrument outcomes advance. Every readout is accepted, including incorrect ones. No collision flag or external clock is used.

The largest native jump uses at most four clock qubits plus two probe/data/cache qubits: six physical qubits. Boolean repairs use at most three for fanin two, flag actuators at most two, inversion sorting at most three. Mode degree O(M), apparatus count, reset impurity, detector error, channel rates and physical wiring are charged. These are engineered GKSL primitives, not assumed consequences of elementary two-body Hamiltonians.

## 2. Exact finite prices and global mean inequality

Use the complete formulas in independent_native_protection/07_dilute_sensor_closed_join.md, and the source and clock receipts. Denote actuator rate a, fast sensor rate k, slow start r, Boolean weight epsilon=a/k (not preparation impurity), and source reward A_s=a[(1+D_W)R_s+1]. Each source has

  tau=1/r+D/k,
  t_post=A_s tau+epsilon B_s,
  xi_s=A_s tau+2epsilon B_s.

The own-clock t table retains return phases. The positive price t e_s+xi_s r_s pays both cache mismatch and probe readiness; readiness is zero after readout. Its negative h(e_s+r_s), h=epsilon B_s k at readout, cancels the Boolean inconsistency increase caused by cache overwrite.

For each ordered overlapping pair, actual quantum interference contributes at most 2k xi_s I_busy,busy in operator order. Let H_pair>=0 solve the actual product-clock equation

  Q_pair H_pair=-I_busy,busy+f^2, f=Dr/(k+Dr).

Adding 2k xi_s H_pair cancels that contribution pointwise and leaves floor 2k xi_s f^2. No independence of quantum errors, transient clock states or reports is assumed: the classical adjoint law follows exactly from TP instruments. For r<=k/(4D), the explicit bound H_pair<=8D/k is available. Preparation impurity p_s adds at most p_s r xi_s. Independent readout confusion eta_s can be paid with its own occupation price; general detector faults are admitted as actual local perturbations.

Extend every source coefficient, Pauli prefix and pair price to arbitrary clock strings through decoded (mode,rank). Adjacent 01->10 sorting preserves all these quantities. The physical-minus-decoded reference generator is supported on malformed clocks. The reference is proof-only, with source-labelled Kraus maps to canonical decoded successors, not physical high-arity control. All omitted reference and wrong actual moves are counted. For each clock g, if B_g bounds affected-term change and C_M=floor(M^2/4), choose positive a_clk and

  nu a_clk/C_M >= (M+2)k B_g+a_clk(M+1)k Delta_M+margin,
  Delta_M=max(M-1,floor(M^2/4)).

Then sorting pays the entire malformed-state contribution, including premature resets/readouts and base-W changes. Legal-to-legal clock errors that skip a gate remain physical perturbations; sorting does not detect them. The exact native guard construction and all-string checks are in SMALL_QUBIT_SENSOR_CLOCK_RECEIPT.md.

Combining source, verifier, flag and sorting operations yields, on the protected component and every apparatus state,

  L_ideal* V <= -c W+b_ideal n I,
  V=W+Z, 0<=Z<=z n I, c=a c0/2.

Here Z contains all Boolean, source, pair, optional detector and clock-inversion prices. It is local with bounded norm/incidence independent of n, although its constants may be very large. The displayed inequality is a join to be independently checked, not inferred from completion probabilities.

## 3. A nonempty intensive admission region, not a practical threshold

The weighted source construction gives explicit finite constants C_z,C_p,C_col and

  z<=C_z a/r+z_clk,
  b_ideal/a<=C_p(p+eta)+C_col r/k.

Include every actual local Hamiltonian/bath/jump perturbation, on data AND apparatus. Let its actual operator bound on V be L_noise*V<=nu_V n I. This can be bounded by sums of affected local-term norms: a Hamiltonian term H contributes <=2||H|| sum_near||v_X||; a dissipator J contributes <=2||J||^2 sum_near||v_X||. These are upper bounds, not automatically small. Calibration differences of an intended jump can be bounded using their actual cross terms or the difference of dissipators; do not treat them as necessarily positive extra Lindblad terms.

Thus L*V<=-cV+[b_ideal+nu_V+c z]n I. For a chosen strict theta below the logical barrier beta, choose the explicit inequalities of section6 of the weighted join with slack:

  C_z a/r, z_clk, (2/c0)C_p(p+eta),
  (2/c0)C_col r/k, (2/c0)nu_V/a

all small enough that their sum is <theta. Fix k; choose r/k small; choose a/r small; choose clock penalty height small and then sorting rate nu large enough; evaluate actual hardware noise AFTER selecting those rates and all apparatus constants. All parameters are fixed independently of n. A positive sufficiently small perturbation neighborhood exists for each finite hierarchy. There is no claim that a specified laboratory error-per-operation satisfies it, or that increasing nu leaves sorter noise fixed.

## 4. Protected component and logical interface

Work in the exact dressed frame. A fixed coloring orders the bounded-overlap controlled-Pauli prefix gates. Their clock-controlled product U_probe has finite depth and finite support light cones, independent of n. On each clock block it sends every complete stabilizer S_s to

  Sbar_s=S_s product_p Z_p^[omega(prefix_p,S_s)].

This formula follows because the extra probe-Z factors commute with subsequent controlled-Pauli gates. Apply also the previously defined witness and flag-frame unitaries. In that frame W is the old Tanner witness potential tensored with unused apparatus. The auxiliary quantum state is not declared classical or pure.

Let P be the transported old good low-W component, with identity on free apparatus. Every readiness term commutes each dressed stabilizer and each witness/flag Z label by the two-sign cancellation. All remaining Z terms are functions of these labels, caches/wires and clock-diagonal coefficients. Consequently [P,V]=[W,V]=0, and V>=W. This preserves the actual component labels, not merely the scalar W eigenvalue.

Every actual native local H,J and J†J, conjugated by the finite-depth dressing, has support in a fixed expanded neighborhood. Expand its data/witness part in bounded-support Paulis and leave arbitrary apparatus coefficients. The old canonical-representative argument then gives protected factorization for PHP, PJP AND PJ†JP when n is sufficiently large for R/2+w_expanded<d_old. A finite W bandwidth b_W is bounded from this expanded support and the affected commuting W terms. One- and two-step shell identities must use this actual b_W. Multi-Pauli local terms cannot be assigned a one-step anticommutator shell without justification.

These local-light-cone and component claims are explicit proof obligations of this join. They do not assert the non-Clifford dressed code is a new Pauli stabilizer code, nor infer distance from unitarity alone.

## 5. Exponential lift and actual-output comparison

The exact local noncommuting expansion applies to the full actual generator:

  e^(-alpha V/2) L*(e^(alpha V)) e^(-alpha V/2)
     =alpha L*V+R_alpha,
  ||R_alpha||<=C2 alpha^2 n.

Choose alpha>0 fixed so the actual mean floor/c plus C2 alpha/c is strictly below theta<beta. The killed-subchannel compression retains this exponential Foster inequality. It does not require every ideal operation to be downhill. Its small boundary mass follows from [V,W]=0, V>=W, and the gap beta-theta.

For an initial state supported in W=0, the uniform Z bound gives Tr(e^(alpha V)rho0)<=exp(alpha z n), so z<theta pays even arbitrary free-apparatus states in this ENCODED subspace. This is an ideal encoding interface, not a claim that an arbitrary unencoded hot apparatus can be attached to stored data for free. A physically prepared alternative needs its actual initial moment/tail. Terminal decoding remains the accepted ideal witness-frame plus Tanner decoder, after undoing the probe/flag frame; noisy terminal encoding/readout are not earned here.

With all native ideal AND noise terms counted, the independent killed-channel theorem yields a bound of the form

  logical output error <= C n T exp[-alpha(beta-theta)n/2],

where C includes the two-step-shell factor, total local Hamiltonian/jump norm densities and the moment prefactor. Full constants are in NONCOMMUTING_SENSOR_CONDITIONAL_THEOREM.md. For T exponential in n below this exponent, error is exponentially small. Initial truncation/preparation and terminal-readout errors are added separately. Fixed-bath-input channel and correlated-bath pointwise qualifications remain as in the original theorem.

## 6. Consequence and unearned steps

If the join is accepted, the new operation is autonomous syndrome acquisition and classical correction with physical faulty clocks, probes and wires, including coherent local perturbations, without trusted timing or a full-check input-repair primitive. It banks an essential implementation step on the reliable-quantum-technology route.

It does not establish economical code size, competitive error rates, local Euclidean routing, a microscopic two-body implementation, or an advantage over active extraction given the same apparatus. The strongest active Tanner and synchronous-QCA results remain competitors. Formal fixed-parameter existence and useful performance are different claims. Do not call this a civilisation-level breakthrough.

## 7. Concrete conservative parameter witness (added for review)

To remove any ambiguity about the existence order, assume positive finite constants in the component receipts and set k=1 by time units. Choose

  0<r<=min{1/(8D), beta c0/(80 C_col)},
  0<a<=min{r beta/(40 C_z), 1/(4 B_act)},
  z_clk<=beta/40,
  p+eta<=beta c0/(80 C_p),
  nu_V/a<=beta c0/80.

Zero denominators for absent mechanisms are omitted rather than divided by zero. Then each of the five terms in the mean-floor budget is at most beta/40, so z+(b_ideal+nu_V)/c<=beta/8. Choose the per-clock inversion coefficient small enough that the sum of its maxima is at most beta n/40, then select sorting rate from its explicit finite domination bound. The noise inequality is imposed AFTER this choice; it is not an assertion that every error-per-sort meets it.

Set alpha small enough for the local expansion and C2 alpha/c<=beta/8. Taking theta=beta/2 yields f(alpha)<=beta/4, initial density z<=beta/20, and moment prefactor at most3. The resulting explicit bound is

  logical error <=2 sqrt(3) n (2h_all+3Gamma_all) T
                    exp(alpha b_W) exp[-alpha beta n/4].

Here h_all and Gamma_all include every actual ideal and faulty operation's norm density, after the selected hierarchy; the b_W shell and factorization assumptions are as in section4. This is a fixed-positive formal threshold witness, not an engineering threshold estimate.
