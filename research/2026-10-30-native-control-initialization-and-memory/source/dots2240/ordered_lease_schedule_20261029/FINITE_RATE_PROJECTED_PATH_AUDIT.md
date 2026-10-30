# Independent audit: finite-rate projected-path completion mechanism

Audited FINITE_RATE_PROJECTED_PATH.md against coherent backtracking, outside dynamics, adaptive records, and Poisson timing.

## Verdict

The construction appears valid AS A THEOREM FOR THE EXPLICITLY DEPHASING-AUGMENTED GENERATOR under its stated structural assumptions. It is not a theorem for the original unmonitored scheduler and not a remedy for arbitrary malformed ownership/counter sectors. I found no hidden classical-feedback operation and no need for global color order in this argument.

The qualifications below should be made explicit in the proof rather than left implicit.

## 1. Rollback and bounded region

The set A must contain every hub that can own a target resource; its bound M<=kq is safe. Gamma must contain all physical hub and resource sites needed for their complete reversible programs and cleanup paths. If a program uses additional local work/ancilla sites, include them, changing n and B by a fixed factor. Gamma cannot mean only the clock tensor factors while the desired gate acts on data assigned to the 'environment'.

Reverse acquisition requires no FREE resource: it only removes a current matching owned lock. Reverse program gates must be genuinely unitary/isometric on the whole eligible clean workspace sector. Under these assumptions, rolling back the A hubs cannot be blocked by outside resource owners. Old/Z target locks are then cleared. Since all target competitors are in A, the final acquisition/program/completion path is enabled at the selected intermediate records.

The selected path may depend on the first Gamma record. No actual feedback is needed: this is a disjoint selection of trajectory cylinders of one fixed generator. Outside hubs can acquire freed non-target resources during the total protocol; that does not affect eligibility of the selected path, and unwanted changes during a short step belong to the bounded Dyson remainder.

## 2. Environment interaction picture

Define B using every Hamiltonian/repair term touching the FULL physical Gamma region and half the norm of the summed monitored local jump losses. Outside-only Hamiltonian and reset dynamics are unrestricted. Dilate their CPTP evolution to a unitary on the outside system plus fresh baths. This unitary commutes with Gamma projectors and with the desired Gamma-supported gate. Conjugating a boundary term by this unitary preserves its operator norm; it need not preserve its outside support, which is harmless.

Thus the local conditioned propagator has a Dyson series with bounded interaction norm B even if the outside total generator norm grows with volume. No global generator norm is used. If the desired operation has any support outside Gamma, this commutation argument fails and Gamma must be enlarged.

For a selected coherent step, uniqueness of its a-to-b clock block is essential. It is not enough that one intended term has amplitude g: another term with the same block could cancel it. The stated uniqueness assumption excludes this. With that assumption, the leading block is -ig delta times an isometry, and the displayed remainder bound and p_H are safe.

## 3. Reset step bound

The reset estimate should be stated for the bundled Kraus insertion. At zero local evolution, the vector of Kraus amplitudes is an isometry times sqrt(kappa_h), by the assumed terminal completeness. Before and after the selected jump, bounded interaction-picture evolution changes this vector by relative O(B delta), uniformly in jump time. The single-jump Dyson integral over its time therefore has probability at least kappa_h delta/4 for the stated B delta<=1/16. This avoids subtracting a generic O(B delta) PROBABILITY error from the small probability kappa_h delta.

No other monitored local reset is allowed in this selected record. Outside resets remain in the dilation. The same argument gives a constant positive bound for idle padding.

## 4. Finite measurement windows: use the WHOLE instrument

For a prescribed dephasing schedule, replace each projective event by its record isometry W= sum_c |c>_record tensor P_c. This has norm one. The product of these record isometries and bounded local evolutions differs from the zero-local-evolution product by at most O(B epsilon) in dilation-operator norm, because the sum of all intervening interval lengths is epsilon. Passing to channels gives the stated <=4B epsilon diamond bound for small B epsilon.

This argument treats the COMPLETE recorded instrument, summing all clock outcomes coherently into the record register. A per-outcome bound would not suffice without an outcome-count factor. The record-isometry proof supplies the required bound without such a factor.

Adaptive filtering on the classical record and all later physical evolution are completely positive trace-nonincreasing maps, so telescope errors remain bounded by 4B(L+1)epsilon. This justifies subtraction from the TOTAL selected-path success probability p_0^L, including paths chosen from the initial record.

## 5. Poisson factors and constants

For n independent rate-gamma attempt processes, exactly n events in epsilon with one prescribed ordered site list has probability

 exp(-n gamma epsilon) (gamma epsilon)^n/n!.

This is correct. The event labels/outcomes need not be fixed in advance. Total dephasing intensity at each site is gamma I, so attempt schedules are state-independent even in the presence of the coherent dynamics. Factoring their probability is legitimate. Excluding attempts during L transition windows contributes exp(-n gamma L delta).

With epsilon<=p_0^L/[8B(L+1)], the full-instrument perturbation error is <=p_0^L/2. The stated c_path is therefore a valid conservative lower bound, provided B includes the full physical interaction set as above. All parameters remain finite and independent of system size.

## 6. Scope that must not be enlarged

- The matching-epoch counter-reset self-stall remains outside the clean-sector theorem. Dephasing alone cannot release that exact dark configuration.
- The clean monitor projectors must ignore syndrome/Kraus workspace and commute with the history encoding; otherwise completed-channel semantics can change.
- Arbitrary history conditioning is allowed only when the conditional state remains in the clean legal span.
- A joint fault law still needs a locality/positive-Lyapunov construction on the applicable state space. The present local minorization cannot silently be promoted to a full-Hilbert-space inequality.
- This proof prices a finite one-site dephasing mechanism. It does not establish the same rate for a scheduler without that extra channel.

## Addendum: cleaner CP-Dyson proof supplied by parent

The environment dilation can be avoided. Expand the no-local-jump completely positive dynamics about the outside-only CPTP semigroup, using a bounded local perturbation V with diamond norm <=2B. For initial clock block a and final b!=a, the zeroth and first terms have zero transition probability. If the selected Hamiltonian block is uniquely gU AND the summed local no-jump loss has zero a-to-b block, the second-order transition probability is exactly g^2 delta^2. The outside semigroup commutes with the desired Gamma-supported operation. The remainder in trace is <=(2B delta)^3 exp(2B delta)/6. A conservative delta<=min{1/(16B),g_min^2/(16B^3)} gives the stated p_H lower bound.

The no-jump-loss condition should be explicit. It holds when local reset losses are diagonal clock projectors, as in terminal/Z resets. Without it, off-diagonal loss amplitudes can enter the selected transition block; uniqueness of the Hamiltonian block alone does not establish the leading coefficient. This is a documentation requirement for the displayed ingredients, not a found counterexample to them.

The complete-record instrument telescoping proof likewise follows directly from CPTP contraction and a 2B epsilon exp(2B epsilon) diamond bound, without outcome amplification.
