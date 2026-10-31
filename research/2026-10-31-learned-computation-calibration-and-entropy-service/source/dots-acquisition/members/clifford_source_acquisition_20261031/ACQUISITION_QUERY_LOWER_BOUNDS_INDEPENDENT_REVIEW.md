# Independent review: exact affine-law acquisition query lower bounds

31 October 2026.

## Verdict and frozen source

**PASS at the stated classical worst-case transition-query scope.** I read the complete 5,015-byte `ACQUISITION_QUERY_LOWER_BOUNDS_CANDIDATE.md`, SHA256 `23558d71486fd21eb17ca1dc8dc6e9f60099aae2ee247d508cf00dad534e3978`, and independently checked both reductions and their conjunction. No source correction is needed. The probability argument below explicitly integrates source randomness rather than assuming that noisy transcripts are deterministic.

The accepted task requires a self-contained exact global transition-law output with uniform success at least 1-delta on every admitted controllable input. Rejecting such an input is a failure. The model is classical chosen-state one-step queries, fully observed n-bit outputs and fresh source randomness. A worst-case query cap N is being bounded. The statement is not an expected-query lower bound, a coherent-oracle lower bound, or a constraint on a learner permitted to return an unresolved source handle for later calls.

## 1. Controllable family and quotient count

Fix b=e_0 and noise uniform on span(b), with offset zero. Let S e_j=e_(j+1) for j<n-1 and S e_(n-1)=0. Each invertible T with first column b gives F_T=T S T^(-1). Its controllability matrix from b is exactly T, so every member is admitted.

If F_T=F_T', the matrix T^(-1)T' commutes with S and fixes e_0. Commutation then makes it fix every S^j e_0, which is a basis. Thus T=T'. This proves injectivity without identifying any hidden random coins.

The number of choices is

    |T| = product_(j=1)^(n-1) (2^n-2^j)
        = 2^[n(n-1)] product_(k=1)^(n-1)(1-2^(-k))
        >= 2^[n(n-1)-2].

For the last inequality, the first factor is 1/2 and the remaining finite product is at least 1 minus the corresponding sum, hence at least 1/2. The empty product at n=1 also satisfies this deliberately loose bound.

Distinct F values are not silently counted as distinct laws. For this fixed noise subspace and offset, equality of global kernels is equivalent to

    (F'-F)x in span(b) for every x,

which is equivalent to F'-F=b ell for one binary row ell. Each law therefore has at most 2^n representatives among the selected matrices. It follows that the number K of distinct observable laws obeys

    K >= 2^(n^2-2n-2).

This quotient bound is sufficient even if it is loose in the particular nilpotent subfamily. It neither demands recovery of F itself nor distinguishes physically invisible random-tape parameterizations.

## 2. Randomized adaptive transcript counting

Fix all learner random coins, including any final output randomization, but do NOT fix or remove source randomness. Pad a stopping procedure to N queries with ignored extra queries if necessary. The adaptive decision tree has at most 2^(nN) possible response leaves. Query choices are determined by the fixed coins and prior responses, so they do not contribute an additional alphabet.

Let J be the true law, uniformly selected from the K distinct laws. At a leaf h, the fixed learner's self-contained output can equal at most one of them, denoted J(h) when it does. Therefore its average success is

    (1/K) sum_J sum_h 1{output(h)=J} Pr_J(h)
       <= (1/K) sum_h 1
       <= 2^(nN)/K.

Each probability Pr_J(h) includes the source's actual fresh random choices. Averaging this bound over the learner's random coins preserves it. This establishes the candidate's success-counting statement even for randomized adaptive queries and arbitrary classical postprocessing. It is stronger justification than simply saying each label carries n bits, because exact semantic-law outputs and noisy leaves are handled explicitly.

For delta<=1/3, uniform success implies average success at least 2/3, so

    N >= n-2-[2+log2(3/2)]/n.

In particular N>=n/2 for every n>=6. No positive n-dependent assertion is inferred from the deliberately negative small-n exponent in the loose K bound.

## 3. Confidence lower bound and source randomness

For n>=2, P0 redraws all n bits uniformly. P1 sets output coordinate 1 to input coordinate 0 and redraws every other coordinate uniformly. It has F e_0=e_1, other F columns zero, and noise span(e_0,e_2,...,e_(n-1)). This pair is controllable: the noise already spans every coordinate except e_1, and F e_0 supplies e_1. P0 with full noise is also controllable. Their global laws are distinct.

For any input, a P1-supported output has probability 2^(-(n-1)) under P1 and 2^(-n) under P0. Fix learner coins and follow an adaptive length-N transcript. Its query choices agree under the two hypotheses whenever its response history agrees. Thus every P1-supported full transcript has likelihood ratio

    Pr_P0(h)/Pr_P1(h) = 2^(-N).

Padding earlier stops with ignored queries preserves the algorithm's output event and allows this same calculation. Let E1 be the event that the semantic output law is exactly P1. Summing over P1-supported transcripts and integrating the identical learner coin distribution gives

    Pr_P0(E1) >= 2^(-N) Pr_P1(E1).

The inequality permits additional P0-only transcripts. Completeness gives Pr_P1(E1)>=1-delta; soundness under P0 requires Pr_P0(E1)<=delta because outputting P1 is wrong there. Therefore

    N >= log2((1-delta)/delta).

No assumption is made that the source has the same number of random bits under P0 and P1. Their OUTPUT probabilities, not private coin counts, determine the likelihood ratio. The proof concerns classical reset queries, not coherent superpositions of inputs or environment observations.

## 4. Conjunction and exact qualifications

For n>=6 and 0<delta<=1/3, both families lie in the admitted n-bit class, so a uniform learner must satisfy both bounds. Since (1-delta)^2>=delta in this range,

    log2((1-delta)/delta) >= (1/2) log2(1/delta).

Consequently the explicit conservative bound

    N >= (1/4)[n+log2(1/delta)]

holds for the worst-case query cap. The separately constructed learner's count 2n+ceil(log2(2/delta))+1 therefore has matching worst-case order. This does not certify an optimal leading constant.

The lower bound needs actual successful output on all controllable members. A promise only about correctness conditional on admission would permit reject-all and is insufficient. Nor is it a posterior confidence statement for each realized transcript. If the allowed output is merely a handle that continues querying the original unknown process, those future acquisition queries must be counted; otherwise the self-contained identification task has been changed.

The argument does not establish bit-time, reset-cost, circuit-size, gate-count, robustness, practical, or distribution-free optimality. It does not separate the proposed learner from strong ordinary active learners with the same data and retained representation. It does not prove novelty for counting or binary hypothesis testing. Quantum source synthesis and the downstream controlled simulation remain separate received capabilities with their own access and operation costs.

## 5. Independent finite diagnostic

I also executed the separate exact-integer diagnostic `test_query_lower_bound_count.py`. It enumerates every invertible T with first column e_0 for n=1,2,3,4, computes each F_T, and compares the laws by deleting the noisy output coordinate from every column. Results were respectively:

    n       T count       distinct F       distinct laws
    1          1               1                 1
    2          2               2                 2
    3         24              24                24
    4       1344            1344              1344

These small cases confirm the count/injectivity/quotient implementation independently but do not replace the all-n proof above. No stronger all-n no-duplication claim is inferred from them. The diagnostic is not a lower-bound proof by experiment and is not an implementation of the learner or quantum simulator.
