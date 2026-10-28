# Independent root review: ordinary NPT filtered-seed front end

2026-10-28. Scoped PASS on the new front-end derivation; the downstream finite factory remains a separately reviewed dependency, not accepted by this receipt.

Reviewed frozen source: `ORDINARY_NPT_FILTERED_SEED_FRONTEND.md`, SHA256 `341ede005dbf3f6d5486311ddfdd3448aa779b4821d516dd9d8a24a42b3da9b7`. Reviewed governing accepted ten-anchor derivation: `../ordinary_generic_inverse_square_polynomial_baseline_20261028.md`. Read the full neighboring factory draft to check the intended interface, without replacing its independent composition review.

## Load-bearing checks

1. **Acquisition and interpolation.** The accepted fit supplies uniform trace error 28 delta_a. The reconstruction map `J=2 I_A tensor Tr_A(T)-3T` has trace-norm bound 7 on Hermitian perturbations: partial trace contracts the Hermitian trace norm, and the two-dimensional identity contributes factor 2. Thus 196 delta_a is valid. No efficient environment tomography or coherent source-input oracle is inferred. Partial transpose preserves Frobenius norm, so the spectral perturbation is bounded by this trace error without a k factor.

2. **Global search over the stated four-dimensional selector.** Fix a comparator negative vector and minimize its real quadratic in x. Its spectrum lies in [-1,1]; a chord-h grid near a least eigenvector loses at most 2h^2. The selected model Rayleigh value is compared with the gridded comparator and incurs the stated two model errors and mu/16 numerical error. The displayed constants are strictly below the mu/2 slack required in (3). This is polynomial only because selector dimension is fixed; it is not an efficient search over arbitrary encoder circuits.

3. **Ordinary certificate.** `Tr(T O_v)=Tr(J W_v)` follows by the adjoint of the same reconstruction map. `||O_v||<=5` is conservative. Hoeffding for range length 10 and tolerance mu/4 gives failure at most `2 exp(-n mu^2/800)`, exactly matched by n_v. The training event plus validation event ensures acceptance, while the validation event alone prevents accepting theta>-mu. No posterior normalization is used.

4. **Complex local filters.** The transpose placement is correct. With the source's Schmidt convention, `sqrt(2)(F_A^T tensor F_B^*) psi_-` is v up to a harmless global sign; its rank-one projector is exact. Transposing the reference subsystem yields the stated witness conjugation and `theta=a(1-2F)`. Contractions imply a<=1, while F<=1; theta<=-mu therefore yields both a>=mu and F>=1/2+mu/2. These are statements about fixed prepared resource pairs, not about a successful conditional channel on arbitrary input. The lower bound on the smaller Schmidt square follows from `s(1-s)>=mu^2` and is adequate for bounded numerical conditioning.

5. **Reservoir.** On each good warm branch, independent filtered trials have fixed acceptance a>=mu. The cap has mean at least 2(N_0+t_f). A multiplicative Chernoff bound costs at most exp(-(N_0+t_f)/4), which is bounded by the stated exp(-t_f/4). Keeping the first N_0 successes produces the tensor product of the same normalized accepted pair, conditional on coarse success flags, by the tensor instrument factorization. This relies on the accepted common-frame experiment and independently reset source; it must not be replaced by iid statements about averaged warm histories.

6. **Strictly broader fixture.** The amplitude-damping partial-transpose eigenpair and filter success/fidelity formulas are correct. For arbitrary CPTP qubit decoder the Bloch linear norm is <=1, since trace distance contracts on opposite Bloch inputs. The trace/nuclear norm bound therefore proves the full stated CPTP and unitary-encoder optimum, attained by the identity at r=1/16. The anti-degrading composition at survival r/(1-r) is also correct for r<=1/2. This illustrates a two-way-assisted resource promise beyond unfiltered CPTP Bell fraction >1/2, not positive unassisted capacity.

## Reproducible independent checks

`npt_frontend_root_checks.py` and `.json` check 480 randomly generated complex Schmidt bases and physical channels (receiver dimensions 2,3,5,8), including the full operator filter identity and the ordinary observable identity, plus five amplitude-damping examples. Largest residual <5e-16. These are numerical algebra checks, not acquisition trials or hardware measurements. They supplement the arguments above and do not establish historical novelty.

## Scope and remaining obligations

The front-end is accepted at its written finite-gap, fixed-selector, independently reset, trusted-control scope, conditional on the separately received factory and typed interface. No arbitrary NPT distillability decision, no growing-circuit encoder optimization, no efficient near-PPT rate and no practical hardware advantage are established. Standard filtering and recurrence remain prior art. The source records finite circuit errors under the common whole-process discrepancy budget; this receipt does not grant fault-tolerant local memory or communication for free.
