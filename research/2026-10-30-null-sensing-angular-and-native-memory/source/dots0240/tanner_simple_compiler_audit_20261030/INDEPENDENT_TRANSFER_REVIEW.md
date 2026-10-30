# Independent transfer receipt: Tanner energy to the finite-rate simple compiler

2026-10-30. Reviewed `LINEAR_EXPONENT_FINITE_CONTROLLER.md`, SHA-256 `262ad8345f510e45f761703e8cf5a1dc83d6b1bd9e331daf502344e0e56ab858`. The exact input is preserved in `reviewed_sources/`; governing receipt/source hashes are in `SOURCE_SHA256.txt`.

## Verdict

**PASS at the stated scope.** The new orbit-minimizing GPT rule, full RAW-syndrome completion, nonlinear unary-energy tokens, and actual dirty-reset updates satisfy the additional interfaces of the independently accepted full-Hilbert simple compiler. This is a finite-rate **bounded-body guarded Hamiltonian plus onsite auxiliary-reset** result, not merely the previously accepted ideal atomic Tanner correction theorem.

Under the already accepted Tanner confinement/active-density/code hypotheses, it yields constant encoding rate and

    ||Dec_frame E_t Enc-id_L||_diamond
        <= min{2, C N^(3/2) t exp(-cN)}

for sustained bounded-incidence local Hamiltonian/Lindblad/common-bath perturbations below a positive fixed joint-norm threshold. Exact encoded input, a fixed logical-independent bath state, all-ready auxiliaries, and ideal mathematical framed output remain part of the theorem.

No actual new bridge defect was found. Two important precision requirements are made explicit below: **the proof closes on the full raw-syndrome/label diagonal algebra, not the coarse energy-token algebra**, and the reset DATA support in the energy-token bound is the **gauged/expanded** support. These clarify the correct reading of the candidate; they require no new code or physical assumption.

Native two-site continuous-noise compilation, noisy preparation/retrieval, practical constants, passive equilibrium protection and fixed-dimensional Euclidean locality remain unproved. No governing foundation is re-certified by this transfer receipt.

## 1. Imported versus newly checked contracts

Imported, at their exact reviewed versions:

- Tanner local coset energy is a function of full raw stabilizer syndrome; each DATA qubit belongs to two energy views in one sector.
- The accepted active-hub density counts hubs admitting **some** improving subset of their fixed correction view, independently of the selected improving subset.
- Integer-energy unary tokens, the enlarged full-read component containers, linear confinement/distance cutoff, and canonical local-edge theorem satisfy the ideal weighted/killed-basin interface.
- The full-Hilbert simple-compiler theorem accepts idempotent deterministic syndrome-measure/Pauli-update channels, actual monomial onsite resets, strict auxiliary bad-token charge, and the stated local operator/noise hypotheses.

Newly checked here: idempotence of the changed local choice; preservation of the active set and strict bounded token progress; raw rather than token-only closure; the bounded-patch decrement estimates; full-space monomial completion on raw labels; actual dirty-reset token budget; raw-syndrome covariance/basin compatibility; and volume-independent resource/exponent transfer. The earlier transactional gate implementation is used only to identify the actual finite full-read table, not as the physical generator of this theorem.

## 2. Orbit minimization is a genuinely idempotent channel

For hub h, all possible corrections f belong to the binary vector group of subsets of Q(h). Let H_h be the complete concatenated raw check list over every energy view meeting Q(h). The affected energy is

    E_y(f)=sum_(v meeting Q(h)) t_v(y_v+H_v f).

All other energy terms are invariant. If y'=y+H_h f, then for every allowed f',

    E_(y')(f')=E_y(f+f').

The allowed set is closed under addition, so y and y' have exactly the same attainable minimum energy. A minimizing selected f therefore takes y to an orbit minimum. Choosing identity whenever f=0 is any minimizer, including ties, makes the next correction identity.

The first measurement/dephasing by Pi_y makes the output block diagonal in the newly reached raw records. A fixed Pauli takes each measured raw sector to one definite new raw sector, including degeneracy spaces. Hence repeating the channel changes neither its diagonal blocks nor surviving within-sector coherences:

    Phi_h^2=Phi_h

on all operators, including arbitrary DATA/reference/bath entanglement.

The rule is active exactly when E_y(0)>min_f E_y(f), equivalently when some permitted correction improves the energy. Thus the accepted active-hub density is unchanged. The earlier lex-first-improving dynamics is not silently reused, but the theorem's actual active-set contract does not require that selection rule.

Every nonidentity selected correction lowers total integer energy by at least one. With w=Delta^2, |f|<=w and the accepted Lipschitz identity gives

    |D_h|=sum_v |U_v(e+f)-U_v(e)|<=2|f|<=2w,
    removed(D_h)-added(D_h)>=1.

Therefore beta_data=1/(2w) is valid. The finite local truth table may be enormous, but it depends only on fixed local code/degree and the fixed read list, not on N, unknown noise or a global decoder.

## 3. Nonlinear energy does not close the coarse token algebra—and need not

Different raw records can have identical unary-energy tokens yet select different corrections. Consequently d_h=V-Phi_h*V need not be a function of tokens alone. Likewise a raw-sector-monomial reset can send two equal-token source sectors to different token outputs. It is incorrect to infer preservation of the coarse token-only algebra.

The sufficient statement, which the actual construction satisfies, is stronger in the relevant direction: the full raw-syndrome/auxiliary-label diagonal algebra is preserved by every gauged raw reset, and **each fixed raw source sector** has a definite target token pattern. Every token is a local commuting projector function of that raw syndrome. The per-move proof, raw bad charge, coverage and local-orbit inequalities can all be evaluated in that finer common diagonal algebra. They never require a Markovian dynamics on energy-token configurations alone.

This distinction is especially important for the overlap estimate. Fix h,j in the same CSS sector with overlapping full read supports. If j is inactive at a raw source y, the identity-on-minima rule makes its raw update exactly identity, not merely an energy-preserving relabeling. Thus Delta_j d_h(y)=0. If j is active, its actual token changed set D_j is nonempty and has the strict per-move animal charge.

Expand Delta_j d_h animal-by-animal into its four potential values at y, T_j y, T_h y and T_h T_j y. A nonzero summand has an animal meeting the fixed union of possible h/j changed-token footprints, even when j only changes the raw decision for h without changing that animal's source energy. All local token ratios along those bounded moves are uniformly bounded. Enlarge that union to a fixed connected patch containing D_j. Completing the source animal by the patch has bounded added size, bounded weight ratio and bounded preimage multiplicity. The completed animal is paid by the actual d_j charge. Thus

    |Delta_j d_h|<=C d_j.

Interchanging h,j gives the required upper bound Delta_h d_j<=C d_h (indeed its absolute version). Full-read adjacency is necessary here; energy-token changes alone would miss decision dependencies. For opposite-sector hubs, the actual GPT tables read only their own sector, so the other correction leaves the entire relevant raw record, the selected mask and d_h unchanged: Delta_j d_h=0 exactly. This avoids trying to pay an animal in one sector graph from a decrement in the other. Arbitrary cross-sector-dependent tie choices are not covered. Nonoverlapping full DATA/read channels commute on all operators, so the linked clean commutator still has exact distant cancellation. See the independent `nonlinear_overlap_review.md` for the explicit patch argument.

## 4. Explicit RAW-label completion and actual onsite resets

The excited label contains the complete raw read list, not a coarsened energy value. The XOR unitary

    sum_y Pi_y tensor X_label^y

is unitary on the entire DATA/excited-label space because the raw projectors are orthogonal and sum to identity. Incompatible records have zero projector. Multiplication by the label-controlled Pauli unitary remains unitary even on unused labels, where a fixed default Pauli is specified. On reference label zero it produces exactly sum_y F_hy Pi_y tensor |y>, the required isometry.

Both factors normalize the full global raw-syndrome/label diagonal algebra. Occupancy-guarded products have the same mutual-exclusion/disjoint-support commutation as in the accepted simple compiler. Their product is bounded depth, and the gauged Hamiltonian is exactly DATA-independent ready/reference drive on the full Hilbert space.

The physical jumps are still the actual onsite auxiliary resets sqrt(kappa)|ready><excited y| tensor I_DATA. Conjugation by the explicit frame makes them partial monomial operators on full raw sectors. No instantaneous ideal correction jump is inserted. Good sources realize the intended idempotent Phi_h; dirty sources are treated by their actual raw-sector transition.

The physical good-range projector remains syndrome/label diagonal because K_y K_z^dagger=0 for y!=z. Thus the combined flags have exactly the previously proved form and monotonicity, and in gauge coordinates

    C'_h=Q_h-G_h R_good,h.

This part uses the raw syndrome and Pauli nature of F_hy, not linearity of the energy tokens.

## 5. Dirty energy change and augmented coverage

A gauged reset has a fixed bounded DATA/controller support Z, after including the full frame light cone. On each fixed raw source sector its DATA action is a definite Pauli on that DATA support, with auxiliary-label changes. For a Pauli supported on Z_DATA, the entire local raw-syndrome orbit can vary at most 2|Z_DATA| unary energy tokens in one CSS sector. This follows from the width bound for each local distance function and does not require that the token itself be a stabilizer character.

The relevant support is the **gauged** support. An original physical onsite reset has no original DATA support, but it can change dressed DATA energy through the frame; using zero DATA support in that coordinate convention would be wrong. The candidate's explicit frame/support enlargement supplies the correct fixed k_reset.

Choose R>k_reset in each sector. A bad-source reset removes its own R repeated flag tokens, creates no new combined flags, and changes at most k_reset energy tokens. Its removal surplus is therefore strict. The same raw full-animal completion proof pays all dirty diagonal loss and local-surgery cross terms. Token copies remain combinatorial repetitions of one projector, not independent physical bits.

Enlarge the component graph before choosing constants to include full raw reads, gauge/reset/credit supports, token neighborhoods and permitted noise/loss supports. The accepted Tanner confinement/density theorem applies to every sufficiently small reduced error, so enlarging the graph only changes which reduced subsets are called components and the fixed container/incidence constants. It does not require a new graph-dependent expansion theorem.

The energy containers obey the accepted component partition property. Added flag tokens are arbitrary auxiliary defects and are handled by the sparse/flag-dense/energy-dense coverage split, never by Tanner confinement. Extra occupied flag tokens can only improve the one-component completion ratio. Sectorwise constructions add; an intended correction in one CSS sector leaves the opposite energy potential unchanged.

## 6. CP credit, local noise and basin symmetries survive the transfer

The geometric B_h is purely auxiliary and commutes all combined flags. Hence it commutes every raw energy animal, regardless of the nonlinear token map. The identities Z_h(V)=-B_h d_h and Phi_h*d_h=0, the signed clean service proof and the zero-drive diagonal/cross-mask argument apply in the full raw-syndrome algebra. The new bounded-patch constant from Section 3 is used when selecting geometric blocker decay and all later parameters.

For local noise or local HP remainders, each token is a commuting bounded-support positive-factor projector function. The full raw Pauli orbit is invariant under arbitrary local DATA/controller/bath operators. Its variable energy-token count is bounded as above, with fixed flag-token enlargement. Therefore the relative-orbit estimates and the exact Stinespring noise transfer are unchanged. There is no Pauli-probability or token-independence reduction.

The basin is selected by raw syndrome (through the fixed canonical DATA representatives and energy potential) and by bad flags. Each K_hy has a fixed stabilizer-conjugation character because F_hy is a fixed Pauli; the control projector Pi_y commutes all stabilizers. Thus the proof-only CP credit preserves the raw-syndrome-diagonal algebra, even though it need not preserve the token-only algebra. Exact mask preservation gives [P,F]=0. Basin preservation and the two-weight lower comparison consequently use precisely the accepted simple-compiler mechanism.

The accepted canonical local-edge theorem still uses physical DATA Pauli representatives; it has not been replaced by a token decoder. All retained local Hamiltonian, reset, noise and complete-loss blocks therefore have identity logical action in that gauge. The fixed common-bath initialization supplies the input-independent killed logical scalar exactly as before.

## 7. Linear exponent and honest resource count

Fix the admissible degree/local codes once and for all. The newly enlarged supports and local dimensions are finite functions of those fixed choices, hence independent of N. Choose ell=c_*N strictly below the accepted confinement, density and distance coefficients, and retune all animal/credit/noise constants after the geometry is fixed. The source boundary remains

    exp[log(1/theta) h_T ell/8]=exp(c_edge N)

with c_edge>0. The whole simple-compiler comparison yields the displayed C N^(3/2)t exp(-cN) bound. It gives exponential storage times after reducing the exponent constant as usual; no useful numerical threshold is asserted.

There are O(N) DATA qubits and O(N) hub auxiliaries. Every local dimension is bounded by a fixed, potentially enormous constant. Consequently total elementary Hilbert-space capacity n_phys=sum_i log2 d_i is Theta(N). Since the imported code has k>=r_code N, the ratio k/n_phys has a positive constant lower bound, albeit potentially tiny. Large label spaces, guarded interaction arity, graph connectivity and maintained reset capacity are explicitly charged—not erased by calling degree constant.

The accepted simple-compiler parameter order is compatible with the new constants: raw table/graph/R first; both animal exponents and theta next; the actual overlap bound and blocker profile next; then small fixed nu, credit duration and noise strength. No choice must shrink with N. The usual vacuum-in-basin and ell>=8s conditions hold for sufficiently large N; the elementary finite-size extension in the whole simple-compiler receipt remains available.

## 8. Independent nonlinear/full-space regression

`check_nonlinear_energy_compiler.py` uses a three-bit repetition-coset toy with two duplicate distance views. Its unary energy is a nonlinear OR function of the two raw syndrome bits. Equal-energy raw records select different local corrections, so the fixture exercises the exact new distinction rather than disguising energy as a linear syndrome bit.

It checks all 8*5^3=1,000 DATA/controller basis sectors and all 2,400 occupied resolved reset sources, including dark and illegal occupations. The explicit XOR/controlled-Pauli frame is a permutation; transformed flags match exactly; resets never create flags and always clear their own; good resets equal the selected Phi_h; with R=3 every bad reset has removal surplus at least one. All three full CPTP channel superoperators are exactly idempotent, including off-diagonal operators. The bounded-overlap ratio in this fixture is at most one.

These checks support the raw-algebra bridge only. They do not independently prove Tanner expansion, active density, general coverage or the memory lifetime. Those remain the stated governing theorem inputs plus the analytic transfer above.

## Final scope

The reviewed new composition establishes the finite-rate bounded-body-H / onsite-reset Tanner memory statement under the exact accepted hypotheses. It is distinct from both the ideal atomic route and the previously accepted native Poisson/Markov-cushion routes. Generic continuous/common-bath noise is covered here without importing a Poisson representation or adding a depolarizing cushion.

The result remains autonomous storage with ideal encoded initialization and ideal framed mathematical output, not a complete noisy quantum-memory preparation/retrieval device. Native two-site continuous-noise compilation and that end-to-end operational interface remain open. No external mutation, source edit, publication or priority claim was made.
