# Continuation after a strict coherent capacity gain

## Current owned result

The selected two-call family succeeds. For the same one fixed beta=1/512,
actual tau_pi, and device V=alpha U+i beta I, reliable deterministic unassisted
communication exceeds 3/2 qubits per forward call. The proven floor is strictly
above `3/2+2^-46`; the explicit spectral-entropy rate is approximately
`1.50000000000001817074461819...`. This is a foundational asymptotic theorem,
with no useful finite blocklength or efficient compiler claim.

The proof actually works for each fixed 0<beta<1 and every fixed normal
initializer, using one code sequence independent of the initializer. Its error
convergence is pointwise in the initializer. The given actual bath is not
replaced by a cutoff or stationary comparison state. Terminal bath return
remains outside the capacity contract.

## Exact mathematical capital

The entire bath is C^2_seed tensor F(C^2), with creation isometries S1,S2 and
vacuum exchange R. The device matrix and all root relations remain unchanged.
The pair family has weights x00, z on the four color/color words, and y/c
diagonal/exchange blocks on a0,0a. Let a=alpha^2,b=beta^2,q=x+2y,delta=.5-q.

The exact bath map is `x A^2+y(AB+BA)+z B^2+c Gamma`, including the full
imaginary root contribution in Gamma. Its dual closes on all bounded depth
functions for every normal initializer. Bulk jumps are -2 through2 with
probabilities (x a^2, 2ab(x+2y+c), b^2+4ya^2-6cab,
4ab(y+2z+c), 4za^2). Root and level-one rows are in the proof, not ordinary
bulk rows. Bulk drift is `d=a(4delta+2bc)`.

Fix `delta=b^2/512`, `c=-b/128`, `q=.5-delta`, and product diagonal weights
`x=q^2,y=q(1-q)/2,z=(1-q)^2/4`. Entropy exceeds `3+b^2/512` while
`d=-kappa=-a b^2/128`. The same density is explicitly separable across the
pair by an eight-product coherent phase average; it is not diagonal and not iid.

The exact infinite depth kernel gives a uniform exponential moment, bounded
actual bath and complementary entropy, and pair coherent-information limit
S(varrho)/2. Spectral type domination loses only a polynomial factor. The
inherited joint compression operation, with its r^2 positivity factor,
auxiliary normalizer and polar repair, yields actual deterministic codes.
The new code uses all 2m calls through one W_(2m); pair input factors do not
mean independent physical channels. The signed-coherence counterexample has
the same input entropy but positive drift and extensive bath entropy.

## Chosen next question

What is the small-angle order of the capacity gain above 3/2? The current
construction supplies a quartic-in-beta lower increment. Is that scaling forced
for every fixed finite temporal block, or can longer coherent correlations give
a quadratic increment or another larger scale? Exact capacity and feedback
equality are also open, but this is the selected next operation.

Start with a charge-preserving four-call perturbation around the critical
rho_c^tensor4 input, retaining coherent final-bath overlaps. Derive the exact
bulk depth functional and its first nonzero dependence on the perturbation,
together with the input entropy Hessian. Test whether an inward drift direction
costs less entropy than in the two-call mechanism. Include the actual boundary
remainders; if depth no longer closes, identify and prove the needed operator
or information control instead of assuming a scalar chain.

A candidate must produce controlled overflow on the actual fixed bath or the
uniform finite-coordinate comparison, then satisfy the inherited code interface.
Finite block rank, a dark state, input entropy, a reflecting stationary density
or a merely formal drift is insufficient. The next step is not to optimize the
present numerical constant. It concerns whether temporal extent changes the
order of the attainable capacity gain.

## Retired routes and scope

Do not reopen balanced-only rate gain, diagonal biased compression, exact
product stationarity, reflecting-cutoff stationarity, or the closed high-entropy
single-site iid stabilization operation. The exact iid information theorem
remains valid and stronger than a diagonal comparator. No source-summary
certification, physical reset or horizon-dependent angle is permitted.

Max integrates; the evaluator studies scientific transfer. The current proof
has internal owner and focused independent challenges, not external certification
or a historical-priority determination. Hidden entropy, N33, N557, IQM, halted
Morrey, R1 and closed material/guide variants retain their owners and boundaries.

Read the complete new proof and REVIEW_STATUS.md. The unchanged Cycle3 ZIP in
preserved/ retains every older owner source; local historical paths are not
evidence that separate chats share a filesystem. Newer owner-local results take
precedence over this dated checkpoint.
