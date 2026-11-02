# Root candidate: amplify a rare-workspace attack to constant logical error

1 November2026. For independent audit. This strengthens the polynomial-error construction; it is NOT implied by that lower bound alone.

## Preserved input class
Use inputs block diagonal in the actual reference syndrome sigma, with arbitrary quantum logical/reference state within each block. Thermal logical overwrite is in this class. All proposed attack gates are monomial in the reference syndrome, logical Pauli and bath energy basis: predicates depend only on syndrome/bath bits; code gates apply Pauli case-swaps; other gates act only on classical-energy bath/workspace registers. Choose exact permutation implementations (or inverse-corrected phases). With initially diagonal bath states, every attempt preserves syndrome block diagonality. No branch needs to create a syndrome superposition.

The memory receives no preparation noise in the cleanest counterexample; common noise acts on all resource species. A stronger all-carriers statement needs a separately admitted initial logical-error bound.

## A good attempt approximately dephases the logical qubit
Modify one work-buffer attack by adding a fresh zero-energy bit r initially maximally mixed, independent of its workspace. Condition the entire code-Pauli path AND its flag-reset operations on r=1. On r=0 leave the code unchanged. Buffer refill may still run; it does not act on logical information. Never reuse r or the attempt's old resource spins.

The designated clean workspace/unary-buffer branch has probability p_n=c(q)n^-C, independent of the memory/reference state. Conditional on this branch, buffer mixing and boundary bounds make the r=1 path implement the desired bare logical X with error at most delta_n uniformly over syndrome and logical input. The r=0 branch is identity. Thus the good-branch channel is within O(delta_n), on the preserved input class, of logical X-dephasing E=(id+Ad_X)/2 with syndrome unchanged.

A bare logical representative differs from decoded X by a syndrome-dependent phase. Because sigma is classical and unchanged by the complete path, that phase does not encode r in a coherent gauge register and disappears in conjugation. Logical X-dephasing is entanglement breaking for a logical qubit, INCLUDING conditional logical/reference states in each syndrome block. Consequently E maps the entire memory/reference state to a separable state across memory versus reference. Later fresh-resource CPTP maps cannot restore that entanglement.

## Correct error accounting for repetition
One actual attempt decomposes by its INITIAL thermal workspace label as
 Phi = p_n Phi_good + (1-p_n) Phi_bad.
Both conditional maps are CPTP and preserve the input class. This is a mathematical mixture, not physical postselection. Define
 Phi_ideal=p_n E+(1-p_n)Phi_bad.
Their restricted reference-safe distance is at most p_n O(delta_n), NOT O(delta_n). This factor is crucial.

Use M=ceil(log4/p_n) attempts with disjoint fresh initial bath/workspace banks. The composed actual channel differs from the ideal mixture composition by at most M p_n O(delta_n)=O(delta_n). In the ideal process, the probability no E ever occurs is (1-p_n)^M<=1/4. Every history containing E is separable across memory/reference at the end. Hence for a Bell input the final Bell fidelity is at most
 1/2 + (1/2)(1-p_n)^M + O(delta_n) <=5/8+O(delta_n).
This is a CONSTANT logical entanglement-infidelity lower bound after polynomial time. Any final decoder acting on memory alone cannot turn the separable branches into a Bell state.

No condition delta_n<p_n is needed. Thus the unfavorable comparison between thermal rare-branch probability and buffer boundary tail does not create a circular choice of buffer length. It suffices to choose delta_n→0, which the logarithmic buffer and polynomial refill achieve.

## Resources and scope
M is polynomial in n for each fixed q>0. Multiplying the already polynomial finite bath bank, routing and execution time by M remains polynomial. All primitive Hamiltonians still commute exactly with K and have the same fixed body/gap/range/strength bounds. Old resource/record spins are never recontacted, so no later step can coherently undo a successful dephasing by retrieving its record. The always-on drift is K; there is no unaccounted coupling to discarded records.

This would refute a fixed-error exponential-lifetime claim that is uniform over this broad DRIVEN reference-charge-conserving control class after small preparation noise. It does not refute the earlier STATIC-H equilibrium-initialized theorem, or a memory model excluding such controls/resources. No autonomous clock is supplied. Native energy-resolved bounded-many-body contacts are explicitly admitted; native two-body impossibility is not bypassed.

The key extra obligations for review are the preserved syndrome-diagonal class on BAD workspace branches, the uniform good-branch channel approximation, and physical isolation of used records. Without these, the original attack proves only polynomially small error and cannot be promoted to a fixed-error lifetime counterexample.
