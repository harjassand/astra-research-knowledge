# Actual protected erasure: the missing full-bath dephasing operation
2026-10-30. Binding construction for FULL_OUTCOME_CONDITIONED_INSTRUMENT.md.

## The rejected shortcut
Coherent copying |z>_O -> |z>_O|z>_G and retaining G does NOT dephase O+G. A coherent input remains a coherent joint superposition. Tracing G only in an analysis cannot prove a full retained-bath classical instrument. The main note's copy-and-discard instruction is sufficient for a terminal reduced instrument, but not for the stronger complete instrument. Replace it by the actual operation below.

## Reset resource and strict code margin
The already-received physical replacement primitive has exact target R_i(X)=|0><0|_i tensor Tr_i X, acting as identity on the modeled retained finite bath. Its physical finite-time generator approximates this target with residual delta_R already included in x_0. The irreversible Markov reset reservoir is NOT part of that retained bath. If instead the entire reservoir is retained as a closed unitary environment, this replacement resource is unavailable and the present classical full-bath theorem does not apply.

Choose the fixed polynomial computation code and admitted sparse-module budget with

    2 r_res + k_bad < d_code,                           (1)

where r_res bounds the number of exceptional children on each ket/bra of an incoming working-period module, k_bad bounds newly bad child erasures, and d_code is its quantum distance. Conservatively take r_res=k ell from actual gadget spread and choose d_code>2k ell+k with k>=1. This is a FIXED stricter parameter choice inside the received polynomial computation-code family, not a numerical threshold assertion. Do not assume a minimally margined previously chosen code satisfies (1); instantiate a sufficiently large fixed member, keeping its actual A,ell and thresholds.

## Forward physical erasure circuit and recursive proof
To erase an admitted level-j encoded block, apply one actual finite replacement reset to EVERY physical symbol in that block, in parallel. There are m^j symbols. No inverse encoder, syndrome measurement or classical decoder is used; no old logical value is first moved to retained work. All reset-time noise/idle locations belong to the module. Park the consumed block afterward as auxiliary. It need not be re-prepared as an encoded zero because it will never again carry a logical input.

Analysis hierarchy: a physical reset is bad if its target location is faulty. A level-j erasure is bad if more than k of its m child erasures are bad. This is a disjoint recursive partition of the physical reset locations, not j sequential reset passes. A GOOD erasure implements full trace of the old logical input into the inaccessible reset reservoir, tensored with some signed operation on the auxiliary/syndrome variables. It can leave arbitrary old SYNDROME information in retained systems, but no old logical information.

Proof by induction. On a nonexceptional incoming child, a good child erasure traces its child logical symbol, including correlations with every external reference; all retained output/auxiliary effects depend only on its lower-level syndrome variables. Do NOT invoke this claim on a malformed exceptional child. For each ket/bra coefficient let T be the union of incoming ket-exceptional children, incoming bra-exceptional children, and newly bad-erasure children. Thus |T|<=2r_res+k. Treat the entire operation and retained output on T as arbitrary, even where an exceptional child's erasure was classified good. Contract every other child by the induction trace identity. In the Heisenberg test of any retained output observable, the remaining dual operator A_T is arbitrary but supported only on T (with arbitrary auxiliary coefficients). Then

    V† A_T V = c_(A_T) I_L,                            (2)

because |T|<d_code. This local indistinguishability identity says that the FULL retained output has no dependence on the old upper logical density matrix beyond its trace, uniformly with references and auxiliary coefficients. It is not necessary to insert E_b† O_S E_a around a reset map whose trace identity might fail on malformed inputs. All malformed child outputs were included in T before the induction was applied. At level zero the exact good reset is literally R_i. This proves the full two-sided common-module erasure statement.

The incoming module's exceptional child words need not be valid codewords: count their whole child support in E_a/E_b. On nonexceptional children the lower-level admitted module supplies the induction hypothesis. No arbitrary-input refresh that might leak logical information to unreset workspace is inserted.

## Noise strength and actual logical dephasing
Let y_0=x_0 for the physical finite-reset target. The exact nested cardinality sieve gives

 y_(j+1)<=binom(m,k+1) y_j^(k+1) (1+y_j)^(m-k-1).        (3)

Choose the overall fixed threshold small enough for both this recursion and the ordinary computation recursion. The same doubly exponential bound applies with its own fixed y_*; physical resets are not charged only once per enormous block. Joint selected block bad laws follow from disjoint physical reset modules. The resource count is m^j actual finite resets per block; parallel duration is one reset interval, with declared simultaneous bounded-incidence resources. If routing/parking requires more locations, pad and count them rather than silently retaining this timing claim.

For each desired protected classical outcome: use ordinary FT to copy its logical value to a level-j ancillary block, then apply this actual erasure to the entire copied block. Declare a dephasing module bad if its protected copy circuit is bad OR its erasure is bad. In every GOOD full coefficient, erasure traces the copied logical system even when its value is entangled with the original output. Therefore the original output is REALLY dephased in the logical outcome basis, including the full modeled retained bath. The retained erased-block state may know syndromes; it does not retain the copied logical coherence or value except through pre-existing outcome-dependent auxiliary data elsewhere.

Include all copy rectangles and the exact OR majorant for all erased output blocks in b_comp (or write a separate b_erase and combine using the same full-circuit disjoint sieve). Choose j=O(log N) so polynomially many erasure blocks have total bad-map norm exp(-cN). There is no exposed physical-bit accuracy assumption and no ideal detector.

## Binding consequence
With this operation and strict fixed code margin, branch-off-diagonal terms in FULL_OUTCOME_CONDITIONED_INSTRUMENT.md really vanish on good histories. Its rank-one branch factorization and CP/TNI positive replacement then apply to the FULL retained finite-bath channel. Without this operation/resource/margin, only the reduced terminal measurement result is asserted. The raw-data discard is not used to erase the final outcome coherence in the full-channel proof; the actual protected erasure is.
