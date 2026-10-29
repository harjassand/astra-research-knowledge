# Two receivers, arbitrary finite outputs, and actual-prior Holevo loss

2026-10-29. Corollary of the frozen slow-mode theorem; independent receiving review requested. This document does not change `GOVERNING.md` or claim historical novelty.

## Contract and result
Let A be one qubit. Let B:A -> B1 B2 be any full-domain CPTP channel, where B1 and B2 are arbitrary finite-dimensional quantum systems, and let Phi_i be its two marginal channels. They need not be equal. For a finite ensemble E={p_x,rho_x} on A, with its actual barycenter sigma, write

`delta_i = chi(E) - chi(Phi_i E)`.

There is one prior-adapted CPTP entanglement-breaking map F:A -> A, independent of x, such that

`sum_x p_x T(rho_x,F rho_x)
 <= min(1, 9600 [sqrt(delta_1)+sqrt(delta_2)])
 <= min(1,19200 sqrt((delta_1+delta_2)/2)).`

The same conclusion holds for ensembles on AR, for any finite-dimensional quantum reference R, provided their actual mean is the product `sigma_A tensor omega_R`. Then Phi_i acts on A alone, delta_i is the joint AR Holevo loss under Phi_i tensor id_R, and F tensor id_R is EB on A only. Individual letters can be entangled and can have different R marginals. The constants have no dependence on either receiver dimension or reference dimension. The input is still **one qubit**; this is not a many-input-qubit tensorization theorem.

## Proof
For faithful sigma, apply the accepted universal averaged rotated-Petz recovery separately to Phi_1 and Phi_2, with CPTP support completion as in the received actual-prior packets. Denote the recoveries R_i:B_i -> A and the recovered marginal channels Psi_i=R_i Phi_i. Both fix sigma. They obey

`sum_x p_x T(rho_x,(Psi_i tensor id_R)rho_x) <= sqrt(delta_i)`.

For no reference, omit R; for the product-barycenter reference case, the recovery factorization R_i tensor id_R is precisely the accepted condition. This step does not require sigma stationary for either original Phi_i.

Apply R_1 tensor R_2 to the joint output of B. This is a full-domain qubit-to-two-qubit channel with respective marginals Psi_1 and Psi_2. Randomly swap its two outputs with probability one half. The resulting channel is a symmetric extension of

`Psi=(Psi_1+Psi_2)/2`, with `Psi(sigma)=sigma`.

Trace-norm convexity and the two recovery estimates yield average residual at most `(sqrt(delta_1)+sqrt(delta_2))/2`. Apply the frozen uniform residual-to-EB theorem to Psi and sigma. The same constructed F works for every letter and every quantum reference. This proves the first inequality. Concavity of square root gives the second.

If sigma is pure, every positive-weight A letter equals sigma; with a product reference mean, every letter is sigma tensor its own R marginal. Local replacement by sigma then has zero error. Thus no singular Petz inverse is needed at this endpoint. Singular omega is treated on its support, as in the accepted recovery theorem.

## Direct approximate-broadcasting consequence
The structural theorem also strengthens the fixed-input-qubit trace-broadcasting baseline without using entropy. Suppose a full-domain broadcaster A -> A A has marginal channels T_1,T_2 satisfying

`T(rho,(T_i tensor id_R)rho) <= b_i`

for every rho in a specified family (a reference may be present and unchanged). Symmetrize to get self-compatible Psi=(T_1+T_2)/2. A stationary qubit state tau of Psi exists by finite-dimensional compactness; it need not be the family mean. Apply the structural theorem at tau. Its all-state deficit identity yields a single EB F with

`sup_family T(rho,(F tensor id_R)rho) <= min(1,9600(b_1+b_2)).`

Only the ORIGINAL family is tested; no invariance of that family under the broadcaster is required. This linear residual implication is the addition beyond the already-received binary-tree/de Finetti `b log(1/b)` baseline for fixed dimension. The previous energy-constrained tree packet and its Knott prior-art correction remain valid; they are not relabeled as new here.

## Approximate channel self-compatibility
If a qubit-output channel Phi has a full-domain joint extension with marginal channels Phi_1,Phi_2 satisfying half-diamond distances at most eta_i from Phi, the same argument can use the actual-prior recovery R for Phi and symmetrize `(R tensor R)B`. For epsilon=(eta_1+eta_2)/2, the resulting exact self-compatible recovered channel Psi_0 need not fix sigma, but has an ordinary stationary state tau and

`average T(rho,(Psi_0 tensor id_R)rho) <= sqrt(delta)+epsilon`.

The all-state structural theorem at tau gives an EB comparator with

`average error <= min(1,19200 [sqrt(delta)+epsilon])`.

This is a mathematically quantified channel-approximation premise, not an inferred guarantee from sample tests. The original support completion makes R a genuine full-domain channel, so the diamond comparison is legitimate.

## Scope and provenance
This bridge uses the accepted primary universal-recovery theorem of Junge–Renner–Sutter–Wilde–Winter, arXiv:1509.07127v3, and the newly submitted elementary slow-mode geometry theorem. It does not require equal receiver channels, qubit receiver systems before recovery, a positive EB CP component, entropy-loss iteration, or normalization of the invalid TNI left resolvent. No universal arbitrary-input-dimension theorem, correlated-barycenter local recovery theorem, practical acquisition procedure, efficient implementation, orthogonal pointer-basis theorem, or historical-priority claim is made. F may prepare noncommuting states.
