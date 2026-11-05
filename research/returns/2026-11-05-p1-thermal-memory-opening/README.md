# Opening: efficient write, passive hold and read for a 3D thermal quantum memory

P1 selects reference-preserving access to a three-dimensional passive quantum memory as its full question. The supplied opening gives an exact syndrome-sampling/loading identity, a local decoder-history polymer compiler and a polynomial sampler under explicit hypotheses. Its application is conditional on the stated construction and lifetime theorem of the external random-embedding memory family. Strong existing Gibbs samplers may already provide the operation; that comparison remains unresolved. This is not an established new discovery or an implemented memory device.

Read the [selection report](package/thermal_memory_selection_20261105.pdf), [complete TeX](package/selection_brief.tex), [independent challenge notes](package/learning_challenge.md), [comparison and physical costs](comparators-and-resources.md), [source audit](package/source_audit.json), [complete captured return](P1_OPPORTUNITY_OPENING_20261105_RETURN.txt), [original ZIP](original/thermal_memory_selection_20261105_package.zip), and [provenance](SOURCES.json). The ZIP arrived after the capture's unavailable-at-download observation, which is retained.

## Consequence and source-conditional model

The target has an explicitly known bounded-range commuting stabilizer Hamiltonian in three dimensions,

```text
H_N=sum_a J_a(I-S_a)/2,
m=O(N),     0<J_min<=J_a<=J_max.
```

The opening uses the random-embedding family and decoder-defined thermal encoding from the cited Balasubramanian-Davydova-Lin preprint, not its separate explicit-embedding proposal. Its desired half-diamond write/hold/read guarantee is

```text
error <=epsilon_sample+epsilon_calibration+epsilon_control+epsilon_read
        +C Gamma N t exp(-c N^eta).
```

For fixed error this permits stretched-exponential passive holding, t=exp(c' N^eta) for c'<c, with polynomial active write/read. It preserves an arbitrary unknown input and reference. During holding there are no scheduled corrections, refresh gates or syndrome measurements. The specified Gibbs-stationary thermal dynamics, such as the stated bounded-rate Davies model, is a premise. A finite-coupling microscopic bath approximation valid uniformly over exponential time is not derived.

## Exact loading from the complete syndrome law

Choose ground encoder V0 and correction F_s in the same decoder frame as the protected logical observables; let V_s=F_s^dagger V0. Distinct syndrome sectors are orthogonal. For

```text
E_p(rho)=sum_s p(s)V_s rho V_s^dagger,
0.5 ||E_p-E_q||_diamond=TV(p,q).
```

Block-diagonal trace norms prove the equality even with an external reference. Classically sample s, encode the input, and apply F_s^dagger. The sample may be prepared before the unknown input arrives. Initial loading error is paid once by channel contractivity, without multiplying it by holding time. Errors continuously introduced during holding are separate.

An efficient full-Gibbs preparation algorithm is a valid competitor: measure its commuting stabilizers and inject a fresh unknown logical input using the sampled syndrome. Logical randomization of the sampler does not disqualify it.

## Retaining the decoder history exposes a positive polymer model

Retain intermediate syndromes h=(s_ell,...,s0), deterministic local correction/coarsening equations, and the complete fixed-base validity relation `s0 in image(delta0)`. Cochain identities lift base validity to physical validity at every level. Deterministic tie-breaking gives one accepted history per physical syndrome, avoiding a hidden Gibbs multiplicity.

Connect history variables sharing a constraint. Each connected nonzero component is valid alone, and compatible components recombine. Alternating contraction supplies `sum_i |s_i|<=4|s_ell|` componentwise, hence physical energy `E(gamma)>=J_min |gamma|/4`. Locality without this energy control would be insufficient. The full base-validity factor avoids imposing base syndrome zero and inheriting an excluded-probability preparation floor.

For M=poly(N) fixed-alphabet variables, fixed constraint degree D, and polymer energy at least a|gamma|, put `kappa=(q-1)max(2,D)^2`, `x=kappa exp(-beta a)`. If `x<=1/[8(D+1)]`, the proved finite-list construction samples to TV error epsilon in poly(N,1/epsilon) time. Polymers larger than L have probability at most `M x^(L+1)/(1-x)`, so L=O(log(M/epsilon)) permits polynomial enumeration. A weighted-Hamming heat-bath coupling contracts by at least `1-3/(4K)` per step for K listed polymers; finite arithmetic has its own error allocation. This is a conservative approximate polymer sampler, not exact unbounded perfect sampling.

The source reports exact enumeration of 65,536 leaf strings in a four-child hierarchy, finding 1,024 valid histories and 300 polymers. These test deletion/recombination and rational sampling identities, not the enormous physical memory family. Ordinary binary XOR supplies a failure case: two defective leaves create 2h nonzero history variables at energy 2J, defeating size-independent energy control.

The abstract sampler and compiler are proved in the brief. Independent in-session checks address representative choices, sparse locality and the weighted-coupling extension at their stated conditional scope. The complete external lifetime proof was not independently re-proved and the full family was not implemented. Capital ran no new scientific audit, code, numerical replay or heavy build. Generated current retrieval was not rebuilt.
