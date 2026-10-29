# Independent review: elementary inverse-error expected-cost lemma

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`. **Accepted with the frozen target-boundary erratum**, for the expected-cost lemma only. This does not accept all claims in the older purification manuscript or duplicate the separately assigned history-uniform/cap theorem review.

For isotropic9-dimensional state tau_v, the successful symmetric-SWAP retained state is(tau_v+tau_v²)/2. Its trace is D(v)/2, D(v)=2-2v+9v²/8, and its normalized error is v'=v(1+v/8)/D(v). For independent fresh restart batches, a successful next-level preparation costs C'=2C/(D/2)=4C/D in expected base programs. Independence of a trial's cost from its own success is NOT needed: the renewal equation is E(total cost)=E(first-trial cost)+Pr(first failure)E(fresh future cost). Fresh identical restart distributions and finite preceding-level expectation are needed. Source-memory-correlated trials do not inherit this equality.

Put r(v)=(1+v/8)/D(v). On0<v<8/9,
- 1-r(v)=(v-1)(9v-8)/(9v²-16v+16)>0;
- r'(v)D(v)²=-9(v²+16v-16)/64>0;
- (r(v)-1/2)D(v)=9v(2-v)/16>=0.

The derivative numerator decreases with v, and is still positive at8/9. Hence with kappa=r(v0)<1, v_j<=v0 kappa^j and v_(j+1)>=v_j/2. Every positive error target below v0 is reached at finite depth, but exact purity is not reached at finite depth when v0>0.

The product recurrence is

C_(j+1)v_(j+1)/(C_j v_j)=4(1+v_j/8)/D(v_j)² <=(1+v_j/8)/(1-v_j)².

Taking logarithms and using log(1+t)<=t and -log(1-v)<=v/(1-v0) for0<=v<=v0 gives log(product increment)<=K v_j, with K=1/8+2/(1-v0). Summing the geometric bound gives

C_j v_j <= v0 exp[K v0/(1-kappa)].

At the first j reaching0<epsilon<v0, one has j>=1 and v_j>=v_(j-1)/2>epsilon/2. Dividing yields the claimed C_j<2v0 exp[Kv0/(1-kappa)]/epsilon. This proves O(1/epsilon) expected base programs for FIXED v0<8/9. The constant is not uniform as v0 approaches the maximally mixed threshold, and the bound is intentionally conservative.

The original displayed all-target statement needed a boundary qualification: if epsilon>=v0, j=0 and C0=1; the displayed expression can otherwise fall below1. `COST_BOUND_ERRATUM.md`, hash-bound below, fixes this by restricting the derivation to0<epsilon<v0 and using max{1,bound} globally. If v0=0, no purification is needed. This correction leaves the inverse-error asymptotic and stated small-target numerical examples unchanged.

Independent checks symbolically verify the three ratio identities and test28 exact rational recurrence cases including initial errors near zero and just below8/9. The proof, not these finite checks, establishes the asymptotic. The receipt does not verify the older manuscript's finite-cap trace-distance correction, robust transducer bound, physical source identification, or all decimal runtime/call estimates.

Primary source checked2026-10-29: Childs et al., *Streaming quantum state purification*, https://arxiv.org/abs/2309.16387. The current final version is v4, January2025, nearly identical to v3 according to its record; it explicitly treats recursive SWAP purification with dimension and initial noise fixed and optimal final-error scaling. The mechanism and inverse-error scaling are established prior work, not a novelty claim. The present review independently verifies the elementary nine-dimensional bound used as a dependency by Astra.
