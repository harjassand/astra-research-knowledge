# Extension: thermally admissible faults, and the exact local obstruction

2026-11-01. Focus: endpoint return after noisy local writing, not another ideal-circuit compilation. Uses the parent's actual RX/RZ exact-spin-environment theorem and its protected logical algebra. This is partial progress, not a completed loading theorem.

## Main useful results

1. There is a rigorous nonstationary admission principle for **locally correctable Gibbs-preserving channels**. An arbitrary number of such channels can generate extensive changes in the gauge state without an extensive collision-divergence penalty; their logical disturbance is charged by the equilibrium bad-syndrome probability and the number of steps.
2. This principle gives a genuinely local, tractable **commuting-H0 subcase**, using syndrome-conditioned Metropolis channels. It does not require assuming mixing. Clean/thermal ancillas and entropy export must be explicitly supplied for a physical dilation.
3. There is a precise obstruction to transferring the mechanism to the actual generic interacting Gibbs state: even an arbitrarily weak local spin-bath coupling can force every exactly Gibbs-preserving **single-memory-site** channel to be the identity. This holds with the actual code Hamiltonian H0, not only for a toy model.
4. These facts do not construct a noisy writer. Interleaved loading gates leave the protected region, and a demonstrated return mechanism preserving the input/reference remains missing.

## 1. Admission lemma and separate logical criterion

Let rho be the ACTUAL Gibbs state of H, let rho_bar be its logical twirl, let delta=||rho_bar-rho||_1, and let ideal overwritten input omega satisfy omega<=2 rho_bar on memory+bath. Let Phi_1,...,Phi_m be CPTP maps, each fixing rho exactly. Exact free evolution under H may occur between them. Any prefix Psi fixes rho and contracts trace distance, so

 Tr(P_bad Psi(omega)) <= 2 Tr(P_bad Psi(rho_bar)) <= 2p+delta,

where p=Tr(P_bad rho). This bound is uniform over the prefix length; it does not multiply delta by m merely to establish admission.

Gibbs preservation alone is NOT logical preservation. The map that resets everything to rho, or a logical depolarizer in a factorized case, is an immediate counterexample. Add the actual local-correctability requirement: for each channel and each decoded Pauli Q, D_Q=Phi* (Q)-Q is supported on P_bad on both sides. A sufficient Kraus condition is [Q,K_a] P_good=0 for every Kraus operator. Since D_Q is Hermitian and ||D_Q||<=2, the change in each decoded Pauli expectation is at most 2(2p+delta). With a reference, the same support argument bounds the trace norm of each reference-valued Pauli coefficient. A conservative qubit-reference channel error bound is therefore

 epsilon_channels <= 6m(2p+delta).

Add the existing exact-H continuous-time storage bound for the interspersed holds. This is a real positive mechanism for *post-write* noise under explicit conditions, with no Gibbs mixing premise.

## 2. Consequential commuting subcase on the actual stabilizer code

Set V=0 (or use a strictly symmetry-restricted model); this is not an open generic perturbation region. For a physical Pauli P_i, collect the bounded set of stabilizers it changes. Their local joint projectors are Pi_s. Let Delta_i(s) be the energy increment for flipping by P_i. Choose Metropolis acceptance a_s=min(1,exp[-beta Delta_i(s)]) or the heat-bath acceptance 1/(1+exp[beta Delta_i(s)]). The channel has local Kraus operators

 K_s,flip=sqrt(a_s) P_i Pi_s,
 K_s,stay=sqrt(1-a_s) Pi_s.

The measured syndrome dephasing does not disturb the commuting Gibbs state, and detailed balance between s and the flipped syndrome establishes Phi_i(rho_beta(H0))=rho_beta(H0). Expand the stable set to cover the bounded support of these Kraus operators. Then the local-correctability hypothesis above holds. For the commuting model, rho_bar=rho and the stepwise logical error is exponentially small in the memory parameter.

This proves admissibility of repeated local thermal channels **once a logical state has been loaded into the equilibrium-overwrite ensemble**. It is not a proof of rapid preparation from arbitrary locally noisy outputs. Indeed V=0 already makes decoded logical observables commute with H0, so the generic-coupling storage difficulty is absent.

Physical resource statement: each such finite-support channel has a finite-dimensional local unitary dilation. The ancillary states, controlled acceptance, and discarding/record storage are resources. A finite run can consume a finite ancilla supply instead of assuming infinitely reusable perfect reset, but the supply, its placement/transport, and initial entropy must be charged. Nothing in an arbitrary weak bounded-spin environment automatically furnishes these resources. The construction must not be advertised as an autonomous generic physical bath.

## 3. No nontrivial single-site exact Gibbs-preserving repair in an allowed interacting subcase

### Linear-algebra lemma
If rho_AB=sum_j A_j tensor B_j has linearly independent B_j and the A_j span all operators on A, then

 (Phi_A tensor id_B)(rho_AB)=rho_AB implies Phi_A=identity.

This follows by equating coefficients of the independent B_j. Complete positivity is not even needed for the implication.

A transparent example is a weak Heisenberg pair H=epsilon(XX+YY+ZZ). At finite beta and epsilon!=0 its Gibbs state is a I tensor I+b sum_j sigma_j tensor sigma_j with b!=0. It has full operator-Schmidt rank, hence no nontrivial channel on only one spin fixes it.

### Actual-code version
Let H0 be the actual finite stabilizer-code Hamiltonian, with a full-rank finite-temperature Gibbs state gamma. Pick one memory qubit A and add one zero-field local bath qubit B, with the allowed weak perturbation

 V=epsilon sum_{j=x,y,z} sigma_j^A tensor sigma_j^B.

At fixed finite beta, expanding the reduced Gibbs state gives

 rho_AB = gamma_A tensor I/2
          -(beta epsilon/2) sum_j T_A(sigma_j) tensor sigma_j +O(epsilon^2),

where

 T_A(O)=Tr_memory\A integral_0^1 gamma^s (O_A tensor I) gamma^(1-s) ds.

The first-order partition-function correction vanishes because every bath Pauli is traceless. T_A is strictly positive definite for the Hilbert-Schmidt inner product: for O!=0, the integral of Tr[gamma^s O† gamma^(1-s) O] is positive because gamma is full rank. Thus T_A is invertible and T_A(I)=gamma_A. The four coefficients gamma_A,T_A(X),T_A(Y),T_A(Z) are linearly independent. Their determinant has a nonzero leading epsilon^3 term, so rho_AB has full operator-Schmidt rank for sufficiently small nonzero epsilon.

Consequently, any A-only channel that fixes the **global actual interacting Gibbs state** must fix rho_AB and hence be identity. This is an allowed bounded-dimensional local spin environment with arbitrarily weak coupling. It rules out a universal sitewise exact-Gibbs-preserving reset/noise prescription across the desired perturbation class.

Scope: this is not a general no-go for larger-support channels, quasi-local channels, approximate Gibbs preservation, correlated sequences whose total action restores equilibrium, or memory loading itself. It identifies why the commuting Metropolis mechanism cannot simply be transferred unchanged. Approximate per-site preservation of order epsilon is not automatically adequate when applied at N sites; an extensive global bound reappears unless a structured cancellation/local theorem is earned.

## 4. What collision cost can and cannot tell us

An extensive collision/Renyi cost does not establish physical instability. Consider a logical subsystem that is exactly decoupled from N onsite thermal gauge spins. Independent gauge bit flips change a one-site Gibbs probability vector p to q, and the classical collision factor is

 K = [sum_x q(x)^2/p(x)]^N.

It grows exponentially whenever q!=p, yet every logical Pauli commutes with the full Hamiltonian and the logical lifetime is infinite. Therefore the parent's collision criterion is sufficient, not necessary. A failure of that criterion for noisy loading is not a no-go; exploiting spatial error-cluster structure may still give a stronger storage statement.

The actual missing step is temporal: a static joint contour estimate can show that a local-error-thickened Gibbs ensemble has the right logical value immediately after noise, but the perturbed ensemble is not stationary for H. Controlling its decoded value for exponentially long exact-H evolution cannot be inferred from that initial estimate alone.

## 5. Established routes that clarify, but do not close, this gap

- Bombin, Chhajlany, Horodecki, Martin-Delgado, *Self-Correcting Quantum Computers*, arXiv:0907.5228v2, https://arxiv.org/pdf/0907.5228 . Section VI.E handles sudden independent Pauli noise through joint thermal-syndrome/error estimates. Section VIII.A considers finite-temperature initialization by changing protecting terms/external fields or code deformation. These are substantial precedents, not a demonstrated RX/RZ noisy loader for generic exact spin-bath dynamics. In particular, sudden-noise overlap is not automatically a uniform long-time bound on the resulting nonstationary state.
- Bergamaschi, Gheissari, Liu, *Rapid mixing for Gibbs states within a logical sector*, https://arxiv.org/abs/2507.10976 . Establishes quasi-local sampler convergence within sectors from ground-state starts for an appropriate class of redundant-check lattice models, including a 4D toric application. It does not supply a general generic-interacting warm-start result for this RX/RZ family, nor a free finite-spin-bath realization. A warm-start, sector-preserving return theorem for the actual noisy-write output class would be a consequential next target.

## Access and status

The Nature page https://www.nature.com/articles/s41467-026-75465-z failed via non-retryable authorization redirect. It was not retried or bypassed, and no claim here relies on its full text. The arXiv sources above were accessible. No external contact/publication.

Status: positive post-write thermally admissible-noise lemma, explicit commuting local channel subcase, and actual-code single-site obstruction established by direct derivation. No end-to-end generic noisy local loading theorem is claimed. The coherent logical-SWAP derivation in the earlier note remains valid ideally.
