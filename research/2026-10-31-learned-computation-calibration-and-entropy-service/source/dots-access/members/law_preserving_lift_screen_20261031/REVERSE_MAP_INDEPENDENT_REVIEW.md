# Independent review: reverse-map lift and acquisition obstruction

## Verdict and binding

PASS for the explicit conditional lift, power-return certificate and scoped oracle acquisition obstruction. This principally identifies what a classical coupling certificate does not acquire; it is not a general efficient compiler or a newly acquired inverse-fibre operation.

I read the full original body and the final changed primary-range paragraph. Bound final source: `REVERSE_MAP_LIFT_AND_ACQUISITION_OBSTRUCTION.md`, 12,358 bytes, SHA-256 `994d0a262d788c7ebce8d28b45d326f06b4b639c299119d7e2686b6aa00e1b22`. Original submitted SHA `7cf45852121b458c02ebf24b3e3c45c4603f195b5067a997b27d3563e2faaa84` was clarified before this receipt. The mathematical formulas were unchanged.

## 1. TP, pure reference and correct classical direction

With the column-kernel convention, the maps represent the REVERSE kernel x conditional on y. Every row y of K_a has only input column f_a(y). Thus K_a^dagger K_a and K_a^dagger D K_a for diagonal D have no off-diagonal entries. Summing the diagonal entries uses pi_y P_rev(x|y)=pi_x P(y|x), giving both trace preservation and the original forward classical restriction. There is no accidental reversal of the consumer's label process.

Applying K_a to psi cancels the square-root stationary ratios and gives sqrt(w_a)psi with the stated positive phase. Hence the specified Stinespring isometry fixes psi with environment reference c. Coherent implementation of this phase convention is still an input operation, not implied by the formula alone.

Replacing diagonal scalars by arbitrary system/reference operators gives the same adjoint restriction. Source-diagonal Hamiltonians preserve this algebra. Prescribed instruments must have adjoints preserving the source-diagonal operator-valued algebra and the desired classical restriction, as the source explicitly states. Merely mapping diagonal input states to diagonal outputs would not be enough. No equality on arbitrary source-coherent operations or private Kraus-label disclosure follows.

## 2. Kraus word order and conditional return

For two steps, K_b K_a[y,x] requires the intermediate label f_b(y), followed by x=f_a(f_b(y)). Thus the source's order f_a1 composed with ... composed with f_am is correct for K_am ... K_a1. The stationary ratios telescope without additional branch weights. A constant composed map gives the rank-one output psi, so its Q-output contribution vanishes.

Each bad word still has at most one nonzero input column per row. Its trace effect is diagonal. The x diagonal of the sum of bad effects is exactly Pr(bad and f_word(Y)=x)/pi_x for an independent Y distributed as pi. Therefore (Phi^dagger)^m Q is bounded by rho_m I. Since it is positive and has zero expectation in psi, it annihilates psi and is supported in Q; compression then gives the sharper rho_m Q inequality. This step does not require the bad trace-effect matrix itself to annihilate psi.

The unconditional coalescence tail supplies only rho_m<=Pr(bad)/pi_min (and the trivial cap one). Uniform conditional root statements can improve that loss but require proof for the actual map representation and orientation. A classical coupling-time slogan alone does not provide the received power certificate. Failure of this particular certificate does not exclude a different faster lift.

As a numerical sanity check, I separately constructed three nonuniform examples d=2,3,4 from reverse constant/permutation maps. TP, the exact pure phase, forward diagonal restriction, two-word order and the rho_m Q bound all held to floating residual below 10^-15. Results are saved in `reverse_map_independent_checks.json`. These are diagnostics only, not a succinct implementation or the proof.

## 3. The actual missing operation

The displayed isometry maps a superposed input x to its normalized weighted inverse fibre in (a,y). Preparing independent a,Y and conditioning on f_a(Y)=x succeeds with probability pi_x. Simply normalizing that postselected state omits both its probability cost and the need for coherent uniform-in-x operation. Classical sampling of the maps or perfect stationary samples does not supply the required isometry, its inverse/controlled use, or a coherent psi preparation.

The alternative using a coherent forward transition and controlled reverse-conditional preparation is also mathematically correct. For each y, U_y maps the normalized reverse state phi_y to zero. For input psi the resulting environment is zero, while orthogonality of U_y|x> for fixed y gives the exact diagonal transition restriction. This proves another conditional construction, not automatic acquisition or fast attraction. The return premise still needs an independent argument.

Thus the sufficient inputs in Section 3 are meaningful, but a future compiler must actually obtain them, quantify their implementation errors/costs and handle physical support/register extensions. Strict positivity on an abstract support does not give efficient support membership or coherent indexing.

## 4. Primary Index Erasure check and limitations

I opened and inspected the primary [Ambainis–Magnin–Roetteler–Roland paper](https://arxiv.org/pdf/1012.2112), including Theorem 29, and [Lindzey–Rosmanis ITCS 2020](https://drops.dagstuhl.de/storage/00lipics/lipics-vol151-itcs2020/LIPIcs.ITCS.2020.59/LIPIcs.ITCS.2020.59.pdf), including Theorem 1. The former establishes the coherent-workspace square-root Index Erasure obstruction; the latter allows function-dependent ancillary garbage under its stated M>=N^(3 sqrt(N)) range condition. The source's final paragraph now uses both only in that sufficiently-large-range, fixed-small-error regime. This avoids an invalid all-M reading: at M=N the image is known and the desired uniform state needs zero queries.

An oracle reset sampler can generate f(Z) with one query and coalesce in one step, yet preparing the coherent uniform image state is Index Erasure. Discarding an entangled index register instead yields a mixed image distribution, not that state. The reduction therefore blocks a blanket cheap sampler-to-pure-preparation conversion in the stated oracle model.

This is NOT a lower bound for the strictly-positive known-coordinate input model in Sections 1-3: the oracle example has an unknown support and zeros on the ambient register. It is not an exponential-in-log M noncoherent lower bound under the quoted range condition, and it is not a lower bound for every inspectable explicit circuit family or for direct classical simulation. A theorem that supplies or pays for psi and conditional fibres is not contradicted. The source explicitly retains these limits.

## 5. Continuous edge lift and opportunity assessment

The complementary continuous-time formulas agree with the independently reviewed edge-local construction: the current Hamiltonian cancels dissipator off-diagonals, the pure vector is dark, and Q-loss is the stated positive weighted graph form. Complete refresh has exact edge-lift decay exp(-2t/d), whereas a coherent reset outlet gives exp(-t) with the same diagonal classical law. This is a realization penalty, not a universal impossibility. All stationary ratios, current Hamiltonian, preparation and return-gap acquisition costs remain paid.

The decisive consequence is a sharper acquisition target and two explicit warnings, not an already-opened general computational capability. A consequential new class would need an efficiently implemented inverse-fibre/nonlocal-outlet operation and a conditional return certificate, beyond what its ordinary retained classical program already gives. Without that acquisition, a new whole efficient-lift theorem is not earned. Ordinary conditional sampling, quantum state preparation, coupling and pure-state engineering should remain fully credited. No novelty or comprehensive priority conclusion follows from this bounded check.

Final status: accepted conditional mathematical lift and carefully qualified obstruction; no frozen-source edits by this reviewer, no general efficient compiler, no unsupported source-support or quantum-control extension.
