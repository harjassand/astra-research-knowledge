# Independent asynchronous parity investigation

Date: 2026-10-16. Worker: gd_async_genesis.

**The full asynchronous endpoint/Walsh product-Q question remains open in
this worker's investigation.** No legal counterexample and no universal
proof were obtained. The report does not upgrade the supplied synchronized
or one-unpinched-coordinate results to genuinely asynchronous schedules.

The main analytic result is an explicit finite absorbing-history lift.
Within the broad finite-dimensional parity uncertainty class, a legal
all-ever-mismatch counterexample can be converted into a terminal-flip
counterexample with the same bounded odd-interaction actions. New fixed
parities are the OR of the original wrong parity and coherent record bits.
The total physical Hamiltonian stays unchanged; its masked odd part and
sector-preserving baseline satisfy the required identities on the entire
enlarged Hilbert space. Predetermined sector-preserving copies at the nodes
retain the original record distribution. Therefore the universal endpoint
and all-ever product claims are equivalent in this broad class, with the
finite-control/padding qualifications in [PROOFS.md](PROOFS.md) §2.

That reduction does not retain the literal factorized virtual-seed form
automatically. A selected-sign term moved into the new baseline can fail
the required sign/path independence of the actual private-sign receiving
contract. The narrower Walsh theorem must still be addressed directly,
or proved by a valid broad upper theorem. No public access to latent
records or adaptive sign-dependent schedule has been introduced.

I also independently constructed a small exact function-only obstruction:

    F0 = 1-(1+cos x)cos²(y/2),
    F10 = sin x cos(y/2),
    F01 = (1+cos x)sin(y)/2,
    F11 = 0.

It is entire of type at most one per variable, norm one on the real plane,
reflection-equivariant and deletion-null in the specified components. At
sin t=3/5, cos t=4/5, its terminal-odd/OR weight is 1539/2500, exceeding
the putative two-own-gap Q=1476/2500 by 63/2500. It has an explicit
three-level rotation completion, but that completion uses the y interaction
both before and after x. It violates own-gap chronology and is **not** a
legal parity-process counterexample. This pinpoints a missing causal
premise in generic Bernstein tensorization; it does not refute the source
singleton or endpoint theorem. The complete derivation is in §3.

The exact finite checker verifies the history lift on a concrete
dimension-16 model. Original record-OR probability and lifted terminal
probability are both 1595838600000/23298085122481; the original terminal
probability is the different number 1476440100000/23298085122481. It also
checks the all-input commutation/anticommutation and norm certificates,
and the exact polynomial identity behind the function-only obstruction.

Four bounded diagnostic searches used own NumPy code and predeclared
fixed seeds. All actions in these asynchronous searches were A:[0.4,0.4],
B:[0.4,0.4], with A pinched after the second gate and B after the fourth
of six alternating gates. The target product was 0.07856617590691034.

| Control family | Bounded search | Largest objective |
| --- | --- | --- |
| No-bath controlled rotations, endpoint | 24 starts × 180 steps | 0.06620322854407507 |
| Nine-dimensional conditional sink rotations, endpoint | 256 tangent probes; 8 starts × 180 steps | 0.07856617590691037 |
| No-bath controlled rotations, all-ever record event | 32 starts × 180 steps | 0.0785661759069104 |
| Nine-dimensional sink plus sector-preserving real rotations, endpoint | 12 starts × 180 steps | 0.07856617590691037 |

The last three displayed equalities differ from the target only by floating
roundoff. Independent sink/qubit models attain the appropriate product
exactly within those families. These are lower witnesses and bounded
diagnostics, not a universal upper bound, a confidence estimate, or
evidence of independence of bath errors. No acquired optimizer or code
was executed. Search receipts retain their exact finite scope and runtime.

The source read was pinned at
2688d7a383502df4fc1e64001d04bb76e6ec05e5. I read the start instructions,
N890/N894 dossiers and their decisive finite-rate/fixed-grid proofs, then
the received original joint proof. I independently inspected the publisher
PDF of Redheffer's Theorem 11 (p. 832), the classical real-entire ingredient.
No historical-priority conclusion follows from this limited search.
Source paths/hashes and actual resources are in SOURCES.json and
RESOURCE_RECEIPT.json.

All authored files stay under this worker directory. W and originals were
read only. No branches, installs, subagents, or external-app messages were
used. Root task-steering messages were received and answered. No other
current worker artifact was read during the independent investigation.
After that phase, the root explicitly requested a cross-review of
gd_async_adversary/ANALYSIS.md. That separate review is saved in
CROSS_REVIEW_ANCHOR.md; the independent constructions above do not depend
on it. Same-team discussion and review are not external validation.

The cross-review accepts the new anchored asynchronous certificate under
the canonical ideal-pinch contract: for a synchronized anchor subset A,
the all-ever effect is bounded by product_(i in A)Q_i times
product_(j outside A)C_j, where C_j=min(1,sum_k s(a_jk)). For two arbitrary
schedules this gives min(Q_1 C_2,C_1 Q_2). The whole-real-axis anchor bound,
positive record union, clipping by dropping constraints before the proof,
and zero cases check out. This is a valid improvement over the incoming
product-C certificate, while full asynchronous product-Q remains open.

The remaining obligation is the central one: a genuine causal operator
argument preserving every own-gap survival discount for the joint endpoint
effect, or a fully legal fixed asynchronous finite model violating that
effect. Physical implementation of complete pinches, controller privacy,
wrappers, pulse support, reset, precision, energy and matched useful output
costs remain unqualified by this mathematical investigation.
