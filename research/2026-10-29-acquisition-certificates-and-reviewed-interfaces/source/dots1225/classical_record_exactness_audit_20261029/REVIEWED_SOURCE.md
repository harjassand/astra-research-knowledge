# Exact continuous-frame operations require a retained quantum resource

2026-10-29. Root derivation, independent review pending. This is a scoped comparison with classicalized acquisition, not a general quantum speedup or historical-priority claim.

## Contract
A finite-dimensional unknown source channel N_theta is queried during acquisition. Afterwards the learner retains ONLY a classical record (arbitrary standard measurable outcome space is allowed) and source-independent trusted resources. A new unknown payload arrives after acquisition and no more source calls are permitted. The execution processor uses the record to choose a known quantum operation, possibly heralded. The target is one exact unitary U_theta from an uncountable set of distinct unitary CHANNELS. Overall acquisition/execution may stop after a random but finite number of source calls.

## Theorem
Such a classical-record strategy can have positive-probability exact success for at most countably many distinct target unitary channels. In particular it cannot give positive exact success for every unknown relative frame R in SO(3).

## Proof
Let the source input/output dimensions be d_in,d_out and let D be the completely depolarizing replacement channel. Every source Choi matrix has trace d_in and hence operator norm at most d_in. Since J(D)=I/d_out,
 N_theta <=CP d_in d_out D.
For any fixed finite N-slot adaptive acquisition strategy, positivity and multilinearity imply domination of its classical record subprobability measures, including the event of stopping at N:
 mu_theta,N <= (d_in d_out)^N mu_D,N.
This statement remains true with arbitrary finite trusted coherent workspace DURING acquisition, intermediate measurements, feed-forward and continuous classical outcomes. The workspace is fully classicalized/discarded before payload execution.

For each record r, the later successful known operation has a positive Choi matrix J_r, independent of theta except through r. Any later internal randomness can be incorporated into r or its fixed operation. If the aggregate successful operation for theta equals p_theta |U_theta>><<U_theta| with p_theta>0, positivity/rank-one extremality implies that almost every record contributing nonzero success has J_r supported on precisely that unitary ray. Distinct unitary rays therefore have disjoint measurable record fibers F_U (records with zero operation contribute nothing). Positive exact success at some finite stopping depth N implies mu_theta,N(F_U)>0 and hence mu_D,N(F_U)>0 by domination. A finite measure has at most countably many disjoint positive-measure sets. Taking the countable union over finite stopping depths proves the claim.

The argument does not rely on finite classical precision, a finite outcome alphabet or deterministic execution. It does require that the source-dependent quantum resource be gone before the later payload arrives. If that resource is retained, the known processor's operation depends on its quantum state and the disjoint classical-fiber argument no longer applies.

## Relation to the acquired program construction
At eta=0 in the specified informative common-frame source family, the accepted commutator-label/exterior/program-transduction pipeline has finite-cap positive success uniformly over every unknown R and can apply an exact frame gate to a later payload. That is a quantum-resource versus classical-record exactness separation under the stated access contract. The source does not provide a direct U_R query. It does provide a rank-deficient channel from which a pure coherent program can be acquired using protected controls/storage.

At every positive depolarizing admixture, the separate full-rank CP-order theorem prohibits exact variable-frame gates even when quantum memory is retained. Thus this exactness distinction is fragile under general full-rank noise. The approximate noisy program architecture and the reusable classical9-dimensional frame estimator must be compared separately; no practical or asymptotic quantum advantage has been established there.

Sources: standard probabilistic quantum programming and storage/retrieval precedents already cited in the acquisition/transducer dossiers. This elementary specialization is presented to state the actual change in capability, not to claim a new universal no-programming theorem.
