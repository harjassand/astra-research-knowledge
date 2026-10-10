# Native quantum simulation: mechanisms fixed before literature search

Date: 2026-10-10. This note records proposals before using web/literature tools. No claim of novelty or success is made.

## Exact capability sought
Input is a bounded-degree k-local Pauli Hamiltonian H = sum_j h_j P_j on n qubits, with fixed k, O(n) terms, rational coefficients of at most b bits and bounded local energy scale. The ambitious output is a relative-epsilon thermal partition-function estimate, or additive-epsilon bounded-support thermal expectation, at inverse temperature beta polynomial in n, using time polynomial in n, b, beta, and 1/epsilon for a natively recognizable interacting class outside known sign-free/free-particle/tensor-network/cluster-expansion regimes. General-H claims are prohibited by complexity obstructions. No decomposition, sampler, fast mixing, rank bound, or partition oracle can be part of the input.

## Mechanism A: phase-summed multiplicity cancellation (selected)
For each multiplicity vector c of local Hamiltonian terms in the power-series expansion, sum all operator orderings algebraically before taking any absolute values. Since Pauli products commute or anticommute, each ordering differs from a canonical word by a computable inversion sign. Define the signed shuffle integer S_G(c). The actual operation is to replace the whole ordering orbit by its exact aggregate S_G(c) times one canonical Pauli product. This potentially annihilates many histories without walker collisions or importance sampling. The consequential conjecture is that this aggregation admits a polynomial native recurrence on bounded-degree interaction graphs and leaves only polynomially many nonzero boundary classes in an interacting regime.

Decisive tests: derive the recurrence; check small exact expansions; exhibit or rule out exponential surviving sectors with order and coefficient bit lengths accounted for; compare any viable compression against fermionic Gaussian and tensor-network structures.

## Mechanism B: reflected imaginary-time block fusion
Pair a half-history with its conjugate, preserving exact local sums inside a block before sampling block boundaries. Trace exp(-beta H) = ||exp(-beta H/2)||_F^2 is positive. The proposed operation would fuse short reflection-related time blocks while carrying only positive local boundary kernels. The missing step is a bound that prevents boundary kernels from acquiring exponential rank or long-range dependence. A positive norm alone does not give conditional sampling; no such oracle may be assumed. Lower priority because this risk is already apparent from the construction.

## Mechanism C: adaptive local gauge elimination
Use coefficient-aware local diagonal phases to remove the most damaging cycles of off-diagonal signs, then exactly eliminate the remaining signed cells through local Schur complements. Try to produce a contractive positive effective process with a certified local error. The desired distinction from simple basis stoquasticization is exact elimination of sign frustration rather than mere gauge rotation. Risks: elimination fill-in and energy-dependent self-energies; exponential cost of evaluating the resulting resolvent. Lower priority because locality of the Schur complement is unsubstantiated.

Selection: A is the strongest candidate because it is an exact native operation computable directly from Pauli coefficients, and the source of cancellation is explicit and testable. B and C are not promoted to viable inventions.
