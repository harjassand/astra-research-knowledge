# Quantum proposal-interface verification

Pin: 3e8a972f2924272e1a89859d2f556b5b1f91d501.

## Verdict

The conditional operator theorem is valid: on one location schedule that is simultaneously correctable for every allowed Pauli support history, arbitrary bounded-patch CPTP faults coupled to a finite persistent bath give exactly Id_logical tensor a CPTP bath map after the fixed decoder. Coherent cross terms, degenerate syndromes, retained bath records and causal bath-conditioned amplitudes do not invalidate this conclusion. The independent-location assumption is used to import a classical good-event probability, not to make bath coefficients independent.

This result applies to CPTP-completed correction proposals. They are a genuinely different generator from the original seven active Lindblad jumps on syndrome coherences. No counterexample under the literal completed-proposal assumptions was found.

Sources: the original theorem, readout construction and persistent-bath theorem included in originals/, together with an earlier quantum review not redistributed here. The reasoning below reconstructs the algebra rather than accepting an audit verdict as a premise.

## 1. Completion, null events and no-jump evolution

Let the seven active local pattern projectors Pi_j be mutually orthogonal, Q_j the prescribed Pauli correction, A=sum_j Pi_j and Pi_0=I-A. Define K_j=Q_j Pi_j and K_0=Pi_0. Then sum_j K_j^dagger K_j + K_0^dagger K_0=A+Pi_0=I, so C(X)=sum_(j>=0) K_j X K_j^dagger is CPTP. Every syndrome orbit E V is an eigenspace for these projectors: exactly the appropriate active branch, or the inactive branch, survives.

For rate kappa,
kappa(C-Id)=kappa sum_(j active) D[Q_j Pi_j]+kappa D[Pi_0].
This follows directly because all Kraus adjoint products sum to I. In particular, adding the inactive Kraus is not just a relabeling of an original no-jump branch. For an operator X mapping an inactive syndrome space into an active one, the original local generator gives -kappa X/2, whereas the completed generator gives -kappa X. This provides an exact witness of the changed generator, not an instability counterexample.

Any generator gamma(F-Id) with F CPTP is represented by an independent rate-gamma Poisson stream applying F. The no-proposal interval contributes only a scalar survival factor; the corresponding jump representation has sum B_j^dagger B_j=I and scalar no-jump attenuation. Given proposal locations and times, all Kraus outcomes must still be summed: the conditional circuit is CPTP. Conditioning on a selected quantum outcome instead is generally trace-decreasing and cannot be substituted in the averaging argument.

For the original Pauli-noise theorem, no-jump attenuation is a stabilizer function, hence scalar on E V. Definite-syndrome orbit operators remain a closed family, and the extra D[Pi_0] vanishes on each such operator. This explains why the original Pauli-input trajectory reduction and the completed coherent-fault theorem can both be correct without identifying their full channels.

## 2. One fixed decoder corrects the whole Pauli span

Use full joint CSS syndrome projectors P_s and a deterministic recovery Pauli R_s made from the primal and dual component fillings. For every physical syndrome sector there is such a Pauli; its recovery maps that whole syndrome sector to the code. With V onto the entire toric code, define decoder Kraus D_s=V^dagger R_s P_s. Then sum_s D_s^dagger D_s=sum_s P_s=I. Dependent checks cause no issue: sum only nonzero joint syndrome projectors.

The original theorem covers all six toric logical qubits, so the full-code identification applies. If one instead encodes only a proper subspace, these Kraus operators alone are incomplete: extend the decoder on unused syndrome-sector subspaces. Such extra Kraus operators can annihilate all good encoded histories. The global Gaussian-elimination filling must be fixed for every feasible boundary syndrome; impossible stabilizer labels have zero projector and need no separate recovery. The fallback may act logically on bad histories without affecting the bound.

For any history Pauli E, P_s E V is zero unless s=s(E). On a good history, both residual CSS chains after R_s have zero homology. Each is a stabilizer boundary. Therefore R_s E V=omega_E V for a scalar Pauli phase omega_E, simultaneously on every logical state, not just one codeword. Hence
D_s E V=1_(s=s(E)) omega_E I_logical.

Different histories with the same syndrome may differ by stabilizers and phases, but have the same logical action. Their relative phases must be retained; they are harmless scalar coefficients. A trivial final syndrome alone would not give this result. The historical local-transition proof is what excludes a logical Pauli in the residual.

For a fault patch contained in an injective coordinate box of fixed side a, the local homology proof extends from a unit face to its entire Pauli 2-chain F: all affected pre-event components lie in that box enlarged by r=L/32 on each side. Its width is at most a+2r. Requiring a+2r<rho=L/8, i.e. L>16a, keeps all affected fillings in the same contractible box. No fictitious intermediate correction-clock order is needed. Both sector envelopes must infect every possible patch-Pauli syndrome at the proposal and remain small at every pre-event time. This is the bounded-patch version of the classical certificate; its probability estimate remains separate.

## 3. Persistent bath and coherent cross terms

Fix a finite location schedule h and the full CPTP circuit, including any retained classical records in the bath. Expand each fault Kraus F on A_i tensor B exactly in the local Pauli operator basis:
F=sum_P P tensor B_P.
The bath coefficients may be noncommuting, nonnormal, outcome-controlled and correlated across all times. No probabilistic interpretation is assigned to P.

Fix one complete Kraus record alpha, including the final decoder label. Multiply its factors and expand only the fault operators. At each correction projector, a term's current memory operator is E V; the projector either annihilates it or leaves it intact, on the full logical space. Every surviving memory factor is thus one legal support history. The same-decoder identity of Section 2 sends each to scalar I_logical. Keeping exact chronological bath multiplication and summing amplitudes gives
A_(h,alpha)=I_logical tensor B_(h,alpha).

This equality holds before forming a density operator. Thus cross terms between two different Pauli expansions remain explicitly as B_(h,alpha) X B_(h,alpha)^dagger, including their interference and phases; none are discarded or bounded by absolute amplitudes. Syndrome degeneracy merely puts more summands in that same bath operator.

The conditional full circuit is CPTP. Its Kraus completeness now implies sum_alpha B_(h,alpha)^dagger B_(h,alpha)=I_B. Therefore Gamma_h=Id_logical tensor Lambda_(B,h), with Lambda CPTP, on all joint input operators and with any untouched reference adjoined.

This also exposes the common-decoder necessity: inserting sum_s D_s^dagger D_s=I between any two history operators E,F gives V^dagger E^dagger F V=sum_s conjugate(c_(s,E)) c_(s,F) I. The coherent-span cross-error identities follow directly. Error-dependent inverse recoveries would not suffice.

## 4. Causal records and initial correlations

Bath-conditioned future fault amplitudes are ordinary CPTP maps on the scheduled patch tensor the bath record. Fixing a full classical record selects a branch in the Kraus expansion; its subsequent factors still have the same support and are expanded in the same way. If a correction outcome is retained for later feedforward, append its record isometry to the correction Kraus and treat it as another ordered bath factor. The memory projector selection remains unchanged. Postselection is not allowed in place of the complete channel.

Initial logical-bath entanglement is allowed: Id_logical tensor Lambda preserves the reduced logical-reference state after tracing out B, even though Lambda may act on bath information already correlated with it. This does not assert that a bath initially correlated with the logical state learns no pre-existing information.

A finite bath dimension is arbitrary. Uniform constants in the schedule bound need not depend on it. This verification makes no infinite-dimensional extension.

## 5. Schedule averaging and exact claim

Assume one input- and outcome-independent distribution mu(dh) of fresh proposal locations, with a single location-only Good_T that certifies every supported Pauli history. Future amplitudes may depend causally on past locations and retained bath records; they may not alter mu or hide unscheduled memory interactions. For each h, after averaging all quantum outcomes, Gamma_h is CPTP.

For good h, Tr_B Gamma_h=Tr_B. For bad h, both maps are CPTP and their diamond distance is at most 2. Integration and the triangle inequality give
||Tr_B integral Gamma_h mu(dh) - Tr_B||_diamond <= 2 mu(Good_T^c).
This diamond norm has joint logical-bath input. Equivalently every initially correlated rho_LBR has recovered LR trace-distance error at most 2 mu(Good_T^c). A conventional logical-only channel follows by composing with preparation of one fixed bath state independent of logical input/reference.

Fresh Poisson locations supply a suitable mu to the classical probability argument. They are not required for the deterministic factorization once h and its certificate are fixed. A separate good event chosen after seeing a particular Pauli history, or conditioning location law on quantum outcomes, does not establish the displayed bound.

Precision about independence: the schedule is exogenous, sampled without input/outcome-dependent feedback. Outcomes can naturally be statistically correlated with the schedule because the circuit depends on its locations. Literal statistical independence of the entire schedule and every generated outcome is neither required nor generally true. What the proof needs is the same input-independent mixing measure mu and a full CPTP circuit for each fixed h, rather than posterior outcome-conditioned sampling.

## Remaining boundary

The algebra closes the quantum transfer conditional on the universal support-history certificate. The unresolved probability constants and full microscopic envelope verification are unchanged. Arbitrary persistent bath amplitudes are permitted only through the scheduled bounded patches; uncontrolled continuous memory-bath interactions, modified proposal laws, leakage, nonideal initialization/readout, and uncompleted original dynamics under coherent faults are outside this proof.



