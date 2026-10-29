# A nominal thermal encoder without a free Gibbs-state oracle

29 October 2026. A fully specified ideal preparation contract. The theorem
does not assert robustness during noisy preparation or an efficient native
hardware initializer.

Let m be the number of supplied checks and r=n-1 their independent rank.
The admissible syndrome set Sigma is a binary linear space of size 2^r;
all its syndrome spaces have dimension two. Stabilizer linear algebra
constructs its linear membership constraints in polynomial time from the
known nominal check matrix, including any redundant-check relations.

For sigma in Sigma let C_sigma be the SAME source decoder's Pauli correction,
and let E0 be a Clifford ground-code isometry. Put E_sigma=C_sigma† E0. Then

    pi_beta(sigma)=exp(-beta|sigma|)/Z_syn,
    Enc0(omega)=sum_(sigma in Sigma) pi_beta(sigma)
                                  E_sigma omega E_sigma†.       (1)

This is exactly the corrected-logical product encoder omega tensor tau0.
It does not require preparing a coherent many-body Gibbs vector. Its decoder
measures the nominal syndrome, applies C_sigma, and decodes E0. Phase choices
between syndrome sectors have no effect on this mixed encoding, but one
common correction rule is essential.

For a concrete exact finite-bit contract choose beta=ln B with integer B>=2
above the primary counting threshold. All Gibbs weights and nominal thermal
rates are then rational. Such a choice is possible independently of k.
If desired choose B=B0^4: the sufficient primary counting inequality uses
e^(-beta/4)=1/B0 and is an exact rational/integer inequality after raising
to its fixed positive integer power. This avoids an unqualified real-coin
or exact transcendental comparison oracle.

An explicit sampler draws each supplied check bit independently with
probability p=1/(B+1), and rejects unless the vector is in Sigma. On the
accepted space its probability is precisely proportional to B^(-|sigma|).
The acceptance is

    a_acc=Z_syn/(1+B^(-1))^m >=(1+B^(-1))^(-m),
    expected proposals <=(1+B^(-1))^m <=exp(m/B).           (2)

There is no need to identify a microscopic state from data. One proposal
uses m rational Bernoulli coins and a linear membership test. A Bernoulli
1/(B+1) can use a fair-bit uniform integer with rejection, costing fewer than
2ceil(log2(B+1)) expected bits. Polynomial preprocessing/memory and the
exponential upper bound in (2) are charged; the bound is NOT claimed sharp.
For fixed finite beta this is not an efficient-in-n preparation guarantee.
An unqualified ideal independent thermal sampler is not being supplied.

To enforce a finite return contract with failure at most 2^(-ell_fail), cap
the number of proposals at

    ceil[(1+B^(-1))^m ell_fail].

The probability of no accepted vector is <=exp(-ell_fail)<=2^(-ell_fail).
Sampling the classical vector may occur before the unknown logical qubit
arrives. A flagged failure need not consume that qubit. If a channel must
always return, use the zero-syndrome encoding on failure; the implemented
channel is within diamond norm 2^(1-ell_fail) of (1), and the storage
overlap-infidelity bound acquires at most 2^(-ell_fail).

After accepting sigma, prepare the code isometry and apply C_sigma†. An
ordinary ideal Clifford circuit and the known classical decoder suffice.
Their gates, geometric routing, reset/readout, and the preparation of an
unknown input qubit are additional implementation resources; they are not
obtained merely from the Hamiltonian model. Unknown V/E acting during an
actual finite-duration preparation stage need fault-tolerant control or a
separate error budget. Only the selected ideal initial channel (1), followed
by storage under the specified errors, is established here.

Thus the nominal initializer is selected before V and is computationally
explicit, but neither efficient syndrome sampling nor native noisy thermal
initialization has been proved. A stronger sampler can replace (2) if
qualified; the full-sampler slow-mixing result does not itself lower-bound
this syndrome-only task.
