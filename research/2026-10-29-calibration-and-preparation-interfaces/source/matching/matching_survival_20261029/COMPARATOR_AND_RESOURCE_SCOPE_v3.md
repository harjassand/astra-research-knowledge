# Comparator and implementation scope supplement

2026-10-29. This is a governing scope supplement to PROOF_MATCHING_SURVIVAL_v1.md,
not a change to its numerical or theorem statements. Read alongside the primary
comparison note at ../matching_prior_art_20261029/PRIMARY_COMPARATOR_NOTE.md.

## Stronger cheap conventional comparison
Two mutually unbiased logical bases suffice for a channel-preservation test
with a dimension-independent coefficient 2. For k logical qubits these can
be the computational and Hadamard-product bases: one basis coin, k random bits,
and at most k Hadamards before the physical encoder and after the decoder.
A uniformly random full Clifford is NOT needed for this comparator. Both
bases still require the actual full physical encoder and decoder for each test.
See Zeng, Zhou and Liu, arXiv:1911.06855, equations (21)-(25), and the focused
primary-source note above. Complex projective 2-design tests have still better
statistical coefficient (K+1)/K, when their preparation/readout is available.

The matching test's possible benefit is its physical interface: no general
logical state has to be encoded or decoded on test rounds. It directly
prepares pair singlets and measures the same pairs. It does not newly establish
a generic constant-shot, no-tomography, or unknown-environment verification
principle. Historical priority of this exact ensemble/coefficient is unresolved.

For a proper logical subcode the proved matching coefficient is
C=(d/K)(n+2)/(n-1); the cheap two-basis comparator instead has C=2 on its
logical code without d/K overhead. Either can win in a concrete instance.
Comparison must use identical accepted-error target, the same code and source
history rules, and paid gate, routing, calibration, storage and randomness
resources. No finite implementation advantage is presently established.

## Direct-pair gate accounting
With arbitrary pair connectivity, one explicit preparation circuit per edge
starts from |00>, applies X to the second qubit, H to the first, CNOT(first,
second), and Z to the first. It produces the singlet. Each Bell readout uses
CNOT(first,second), H(first), and Z-basis measurement of both; singlet is the
outcome 11. Thus a test requires:
- n single-qubit initializations and n final single-qubit measurements;
- n CNOTs total, and 2n single-qubit gates total;
- uniform perfect-matching selection and classical pairing/readout bookkeeping.
Known local frame conjugations add their explicit rotations. Constants can be
reduced with native singlet initialization/readout; that is a different hardware
interface and must not be assumed for a generic gate comparison.

An arbitrary perfect matching on a linear nearest-neighbor chain requires
routing. Mapping chosen partners to adjacent positions costs at most n(n-1)/2
adjacent swaps per permutation. Restore original labelled positions before
applying the source, and route again for output measurement. A conservative
bound is O(n^2) swaps and O(n) parallel routing depth per test, using an odd-even
transposition sorting network; sorting decisions are classical once M is chosen.

Service calls still need the actual full singlet encoder/decoder (unless an
independently justified already-encoded storage interface is used). Replacing
validation circuits alone cannot justify a blanket polylogarithmic or
asymptotic total-execution improvement when service gates dominate.

No hardware calibration, fault-tolerant threshold, energy cost, or high-fidelity
native pair-router is supplied by the abstract test theorem.
