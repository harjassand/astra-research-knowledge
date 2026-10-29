# Independent product-block baseline review
2026-10-29. Accepted at the fixed-product-code, common-channel and ideal/private-control scope below. This strengthens the equal-resource conventional comparison; it does not discover a useful code from unknown noise.

## Tensor-frame argument
For a four-spin singlet block in the specified real basis, exact symbolic evaluation of the three matching projectors gives frame eigenvalues 1/2 on I, 1/4 on X and Z, and zero on Y. The six-state ensemble gives 1/2 on I and 1/6 on every traceless Pauli. For independently chosen product states on h blocks, the frame is the tensor product, up to vectorization order. The identity eigenvalue is 1/d, d=2^h; the largest orthogonal eigenvalue is (1/2)/d for matching or (1/3)/d for six-state. This is attained by a single nonidentity factor; additional factors can only decrease it.

For each compressed channel Kraus A=aI+A0, identity/traceless frame sectors have no cross term. Summing and using sum A†A<=I yields ppass<=Fraw+r(1-Fraw), with no product-channel, unitality, no-leakage or independent-memory assumption. Hence Hbad<=2 Fmatching or <=3/2 Fsix on memory after evaluation on all input memory densities. Saturation follows from a one-factor tested-plane Pauli for matching, or any one-factor nonidentity Pauli for six-state. The bound is a genuine operator inequality, not merely a scalar average for the carried bath.

CRUCIAL: the test pass is JOINT survival of the entire product state—all blocks pass. q is the probability that at least one block fails. It is not the mean fraction of failed local blocks. For the latter statistic, a one-factor Pauli introduces a factor h and disproves the stated h-independent coefficient. Both supplied programs use the correct joint-pass event. A set of local preparation/readout operations can implement this event without global entangling controls.

## Twirl interfaces and completion
The product S4^h representation on P4^tensor h is irreducible and occurs once in the full physical output, because each factor's spin-zero S4 irrep occurs once. The previously reviewed unique-intertwiner proof therefore gives an exact scalar-good/CP-bad split under independent physical permutations. Raw physical survival bounds this raw bad effect, including leakage as failure.

For the completed logical CPTP channel, independent logical Pauli conjugation is an irreducible one-design. The same scalar-good/residual decomposition applies after key retirement, with bad effect I_Q tensor Hcompleted. Cheap endpoint Paulis suffice: no full logical Clifford or encoded physical Pauli compiler is needed.

Canonical reset has a Kraus representation whose first operator is V†. Completing each raw source Kraus therefore retains its original compressed Kraus and adds reset Kraus. The scalar-good contribution from each added Kraus is B†B>=0 on memory. Consequently Hcompleted<=Hraw<=2 Fmatching. This remains true for a tensor product of block reset channels: the all-code branch is V† and every other branch contributes positively. Thus matching can also use the cheap completed logical Pauli service twirl; physical permutation overhead is optional, not a necessary comparison penalty.

The opposite interface substitution is invalid: completed six-state failures do not bound raw physical bad mass. Entire-code leakage followed by reset gives, at d=2, raw Hbad=1 but completed six-state q=1/2, so (3/2)q=3/4<1. The completed bad mass is instead 3/4, as required. Decoder reset and leakage accounting cannot be silently changed between tests and services.

## Retained-memory and secrecy scope
Memory may be quantum, correlated, and change dimension. The twirled CP split—not treating memory as a classical hidden parameter—supplies the valid payload-independent branch effect. The earlier memory-closure argument still requires retired private keys and retired decoder syndrome/trash for its same-source-memory-filter claim. If new records are retained as outputs, use the appropriate enlarged-interface or simulator statement instead.

The current test/service role, random test state and twirl keys must not be available to the source during interaction. Every test ensemble must probe the same conditional source channel with the declared physical interface. A source allowed to condition on the setting can invalidate an ensemble average bound. Uniform product matching and uniform product six-state ensembles have the same maximally mixed average on the fixed product code; private service product-Pauli padding supplies the corresponding logical randomization. This does not by itself certify timing, control side channels or imperfect endpoint calibration.

## Frozen learned fixture and gauge correction
The actual fixture has E=Vhat E_Bell R with R numerically equal to -X. Independent residuals are ||R+X||≈8.1e-16, encoder reconstruction≈2.5e-15 and good decoder branch≈2.5e-15. These are floating fixture consistency observations, not exact claims about stored rounded arrays.

To preserve its COMPLETE decoder, apply R† after the Bell inverse but BEFORE the final conditional leakage reset. Applying X after an already completed reset changes leakage output from |0> to |1>; the discrepancy is trace distance one on an entirely leaked input. This load-bearing order was identified during review and is now explicitly corrected in the author README. An equivalent implementation may apply R† only on the code branch and reset the leakage branch directly. The one-logical-X cost per endpoint is unchanged; the full physical source-memory maps must not be silently relabelled.

For h2, the supplied source acts successively on the two blocks sharing a bath without reset. Completed decoder operations on one block commute with the later source action on the other block and bath, so their sequential 225-Kraus representation is valid. The raw all-pass amplitude is the ordered product of the two bath survival operators; this is not an independent-noise approximation. The programs preserve the frozen source matrices and learned E rather than regenerating a different favourable fixture.

## Independent evidence
- Exact symbolic single-block matching Pauli-frame eigenvalues; tensor proof above governs every h.
- Nine independent random correlated multi-Kraus channels at h1,2,3, with input memory dimension2, output memory3 and two true leakage dimensions. The tests verify Hraw-Hcompleted equals the positive reset scalar contribution, both matching inequalities, and the completed six-state inequality.
- Full separate replay of the author's frame/24-and-576 permutation/memory tests and learned h1/h2 fixtures. Deterministic numerical outputs match to floating tolerance; these are not rigorous interval certificates.
- Actual learned gauge reconstruction and an explicit wrong-reset-order diagnostic.

## Resource and interpretation boundary
The accepted eight-CNOT encoder applies to all controllers using this code. Completed six-state testing costs16h encoder/decoder CNOTs, whereas raw matching pair preparation plus inverse Bell measurement costs4h CNOTs under suitable within-block connectivity. Both may use the same cheap service logical Pauli controls. Local frame gates, logical gauge, preparation/readout, conditional resets, routing, source calls, backaction, storage and outer-code costs must be charged. Physical S4^h service twirling is a valid optional alternative, at the separately stated conservative SWAP cost.

A smaller scalar constant and a smaller raw gate count are different resources; neither alone proves a yield or practical advantage. Product six-state has the better uniform constant (3/2 versus2), while raw matching has the cheaper stated test CNOT count. This result needs an already chosen good product code. It neither acquires such a code nor proves arbitrary broad noise has one. Tensor frames, Pauli twirls and standard control circuits are established machinery; no historical novelty is accepted.
