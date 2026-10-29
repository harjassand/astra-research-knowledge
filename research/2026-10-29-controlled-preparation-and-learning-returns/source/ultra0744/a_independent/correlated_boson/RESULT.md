# A correlated field operation beyond independent-phase overlap

29 October 2026. **Constructed; independent scientific review pending.** No generic many-body efficiency or historical priority claim.

The substantive new operation is recursive positive sampling of the auxiliary FIELD law for stable conjugate-flavor bosons with noncommuting, frustrated hopping. It replaces an exponential whole-system overlap envelope by a bound on the hopping introduced at each recursive cut. The main theorem is in `PROOF.md`; count and finite-bit interfaces are in `COUNT_AND_PRECISION.md` and `OCCUPATION_INTERFACE.md`.

## Mathematical output

For `H=b†Tb+c†conjugate(T)c+sum_i U_i(nb_i-nc_i)^2`, T>=0 and U_i>=0, use the actual uncut canonical K,K model. At finite L all one-particle histories are contractions. A trace-convergent common-phase determinant envelope supplies positive grand balance, with no finite-part continuation.

If a supplied balanced tree decomposes each parent hopping as child hopping plus PSD cut R, `Tr R<=b=O(1)`, determinant calculus gives the uniform pointwise merge ratio

`exp[-2r beta b/(1-r)] <= g_parent/(g_left g_right) <= exp[2r beta b/(1-r)]`.

Recursive rejection therefore samples the EXACT-REAL conditional-common-phase field law in expected polynomial work, independent of Hilbert-space occupation dimension and without an MCMC mixing promise. The fixed-parameter exponent can be poor. Bounded merge-acceptance estimates acquire every phase normalizer in polynomial randomized work; a log-Lipschitz positive phase grid then acquires the approximate full grand joint law. This phase-normalizer algorithm is proved, not implemented here.

A prescribed canonical count additionally costs its acquired balanced-grand mass pK. The low-whole-trace class `Tr T=O(log M)` pays that gate at homogeneous finite U and any fixed density via the explicit onsite saddle/Fourier count bound. For the extensive bounded-cut class, the proof supplies an alternative nonempty dense family: acquire and REPORT some K=Theta(M) whose count mass is Omega(1/M). That selection is not success on an arbitrary preassigned K.

The same positive grand representation gives uniform local factorial moments. Conditioning on a paid count mass yields exponential local occupation tails, and Gibbs variational/entropy continuity pay replacement by a logarithmically capped Hamiltonian. A competent ordinary tensor/MPO comparator receives that information. No occupation cutoff is inserted without qualification.

## Actual acquired canonical prediction

NEW M64/K64+64, U4,beta1,L16, nonuniform rank-one PSD frustrated hopping with trace1/4:

* Exact rational setup: base count mass about.03533764704; determinant envelope<=3.300705842; ideal final acceptance>=.006493570588, at most153.999 proposals in expectation. Setup.31148s after imports, reusing the frozen diagonal canonical interval rather than rerunning a diagonal DP.
* 32,768 fixed proposals produced222 histories in71.2267s after imports, with every rejected source draw counted. The finite-L CV partition ratio is.62518435, free-energy shift.46970871. Its ideal-iid95% empirical-Bernstein display is[.41559861,.52691506], intersectable with the physical upper.5. Actual floating/52-bit RNG errors are outside that confidence theorem.
* Same-T U0 canonical mechanism control gives.40171460. This is not an algorithmic advantage or a rejection of stronger correlated/atomic/RPA/tensor approximations.
* The actual64x64 history representation does not construct the approximately1.434e74-state canonical sector. Accepted histories are saved.

## Actual extensive conditional sampler

NEW M64 nearest+next-nearest triangular ladder, PSD bond strength.01,U4,beta1,L16: total TrT2.5, maximum cut trace.06. The recursive consumer produced32 histories at each of two fixed common phases in2.90068s, after.00301s matrix setup. It charged54,116 recursive calls and27,026 merge attempts. Every observed determinant ratio obeyed its declared envelope; numerical agreement is not the all-family theorem.

This run is CONDITIONAL-PHASE output. It does not execute the full phase-normalizer FPRAS, canonical count discovery, or continuum prediction for that extensive ladder. The source, code, output histories and primitive costs are saved. An initial slogdet-warning run is preserved alongside its stable Gram-Cholesky repair.

An independent36-state,729-history interacting control agreed on its finite-L partition within3.55e-15. Its continuous value differs, so it is not used to waive finite-slice error at M64.

## Remaining scientific boundary

The rigorous finite-bit operation is specified but not executed with interval arithmetic/fair bits. The conservative continuum log-error theorem demands672,071,920 slices for the actual low-trace M64 norm bound at tolerance1/100; only L16 was run. Better ordinary continuous-time or local error bounds may greatly improve that debt, but they have not been acquired here.

Canonical AFQMC already provides correlated importance/field MCMC, and one-dimensional worldline/tensor/cluster approaches are strong incumbents. This package proves a different positive FIELD-law operation under explicit contraction/cut/count conditions. It has not demonstrated practical advantage over them, a generic prescribed-density theorem, hardware performance, a new material phase, or completion of the civilisation-level mission. The missing global sign/variance problem has not been declared hard merely because an independent-phase route failed.
