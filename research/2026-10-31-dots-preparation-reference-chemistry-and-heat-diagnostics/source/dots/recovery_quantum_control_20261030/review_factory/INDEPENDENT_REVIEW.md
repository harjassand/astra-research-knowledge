# Independent review: late factory frame interface

30 October 2026. Verdict: **SCOPED PASS after the correction-rule and native-failure qualifications**, with the syndrome-admissibility precision now explicit. This accepts an exact limited obstruction and an identified missing proof interface, not a general state-preparation impossibility.

## Input binding

The final reviewed manuscript SHA is recorded in INPUT_SHA256.txt; it includes the final admissibility/sanitization and decoder-versus-memory lifetime qualifications. The independently written check_signed_factory.py has SHA f6c8363f1d4f3c7e972034acfa55d24e8abb7975fd62c22ae6f012499efebaa0. The prior rail and coherent-cut reviews are unchanged.

## Signed Bell calculation and known-state quotient

For a real CSS sector projector, Alice's computational measurement gives Bob Pi_s|a>, up to the stated normalization. On any nonzero branch H_Z a=s_Z. Commuting X^a through the projector therefore clears Z-check signs while leaving X-check signs unchanged. Every chosen logical Z commutes the X checks and fixes |0^n>, so the resulting state has known logical-Z eigenvalues. A Z mask solving H_X z=s_X prepares the same known encoded state for every solution: the difference belongs to ker H_X, consisting of Z stabilizer/logical-Z operators that fix this state. It is correct not to reject a correction merely because its raw Hamming weight is extensive.

The residual-D statement assumes the reported sign string is admissible and the feedforward mask actually solves it. With redundant checks, invalid reported strings require an additional decoding/projection rule. The path example has surjective H_X, so this qualification does not weaken its obstruction.

Independent four-qubit CSS tests cover 32 nonzero signed-Bell branches, all with exact zero residual for the stated X-mask identity and known logical-Z condition. Every matching Z correction gives the same known state in these tests.

## Exact obstruction and its required restriction

For path-incidence H_X and empty H_Z, ker H_X consists of the zero and all-one strings. A central singleton syndrome has exactly two preimages, the prefix and complement, so the minimum weight even after quotienting the known state's logical Z is min(m,n-m). The known-|0> quotient does NOT remove this example.

The indistinguishability proof requires a correction selected only from the reported sign, with no extra quantum syndrome acquisition. Within the Z-Pauli correction class and exact noiseless correctness in every syndrome sector, every random or deterministic selected mask must have the reported syndrome. Thus a one-bit sign error leaves the central residual D with the claimed large minimum weight.

This is not a theorem about arbitrary CPTP correction algorithms: an operation can remeasure the quantum syndrome or reprepare a known state. The manuscript now excludes that overreach. Nor does this bad-distance path code disprove the desired property for the actual Tanner family. Independent enumeration verifies the two preimages and quotient weights for n=4,6,8,10,12.

## Existing native basin: missing theorem, not physical impossibility

The read native source explicitly bounds confinement/active density and its coverage drift only inside an admitted small radius. An arbitrary absolute factory sign need not lie there. Therefore those estimates cannot certify the proposed waiting interval without an additional reduction. During waiting, nominal corrections can also invalidate the originally computed final mask: if memory already applies z to Z_z|0_L>, later applying the old z restores the signed sector instead of the intended zero sector.

For a known target, however, global dissipative preparation may be possible without any protected initial baseline. Nothing here rules that out. One would need an all-sector convergence/noise/output proof for the actual generator, or another explicit preparation mechanism. The manuscript now correctly labels this as a failure to meet existing theorem hypotheses, not proof that the native memory cannot prepare known |0>. A general state-preparation route need not acquire absolute syndrome at all; the acquisition obstacle belongs to the stated feedforward construction.

## Primary comparator checked

I inspected the published ITCS page directly. Theorem 1 states CSS-LDPC preparation with O(nT) ancillas and the quoted success exponent. The construction has 2T+1 code layers, constant-depth graph preparation, measurements and Pauli feedforward. Footnote 1 explicitly assumes instantaneous classical processing. The decoding paragraph gives T exp(n) time; Theorem 2 requires a further efficient repeated-measurement decoder. These statements support the note's comparator, not a continuous retained-bath/native-controller theorem. [Bergamaschi and Liu, ITCS 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol325-itcs2025/html/LIPIcs.ITCS.2025.16/LIPIcs.ITCS.2025.16.html).

With linear distance, logarithmic n and T make the stated graph space polylogarithmic and exponential-in-n classical computation polynomial in L/epsilon. This arithmetic does not prove that decoder physical runtime fits the available memory lifetime, nor that the extensive pending frame is protected. Those rate/exponent and physical-interface checks remain required.

## Verdict boundaries

Accepted: signed-state algebra, known-state quotient, restricted sign-only Pauli obstruction, faithful ordinary comparator, and identification of an unproved native wait interface. Not accepted or claimed: a Tanner-family no-go, global known-state-memory impossibility, broad-noise preparation, a late-arrival protocol, or completed factory/memory composition.
