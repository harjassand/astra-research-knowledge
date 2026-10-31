# Query costs of exact global affine-law acquisition
31 October 2026. Candidate mathematical supplement. These are ordinary counting/testing reductions, not a new general learning lower-bound method.

## Task and access
An unknown classical kernel is x' = F x + beta + eta on GF(2)^n, with fresh independent eta uniform on a fixed unknown subspace. The learner may choose each classical input state and observe the complete next-state label. It must, with probability at least1-delta, output the exact global transition law (and admit the corresponding controllable input) for EVERY member of the admitted family. Rejecting a controllable model counts as failure for this completeness statement. The output must be a self-contained identified model; returning an unknown source-oracle handle for later calls is not identification. All acquisition calls, including preprocessing, count. The bound is on a worst-case number of classical transition queries, not on a coherent sampling-oracle model.

## 1. Worst-case linear register-size cost
Fix noise subspace span(b), b=e_0, and zero offset. Let S be the nilpotent forward shift S e_j=e_(j+1), S e_(n-1)=0. For each invertible binary matrix T with T e_0=b, set F_T=T S T^(-1). Every pair(F_T,b) is controllable, since b,F_T b,...,F_T^(n-1)b are exactly T's basis columns.

The maps T->F_T are distinct. If F_T=F_T', then R=T^(-1)T' commutes with S and fixes e_0. Since e_0 is cyclic, R fixes every S^j e_0, so R=I.

There are product_(j=1)^(n-1)(2^n-2^j) such T. This is at least2^(n(n-1)-2): factor out2^n from each term, and bound product_(k=1)^(n-1)(1-2^(-k))>=1/4 (the first factor is1/2, and the remaining product is at least1-sum_(k>=2)2^(-k)>=1/2).

Different F can still give the same kernel, because their difference may have image inside span(b). For any fixed F there are at most2^n such matrices F+b*l, where l is a binary row. Therefore this family contains at least

    K >= 2^(n^2-2n-2)

distinct observable transition laws. This deliberately loose count avoids assuming uniqueness of a feedback representation.

A depth-N classical-query learner has at most2^(nN) response leaves after its independent random coins are fixed. Each leaf can correctly identify at most one of the K different laws. Average over a uniform prior on those laws, then over the learner/source random coins: success probability is at most2^(nN)/K. Thus uniform success at least2/3 implies

    N >= (log2 K+log2(2/3))/n = Omega(n).

Equivalently this is the usual transcript information bound: each observed label contains at most n classical bits. Unlimited computation after receiving those labels does not remove the acquisition bound. The claim is asymptotic in n; it is not a nonzero bound for every trivial one-bit subfamily.

## 2. Confidence costs at least logarithmically many samples
For n>=2 compare two controllable kernels. P0 redraws all n output bits uniformly, independently of input. P1 redraws all bits except coordinate1 uniformly, and sets output coordinate1 equal to input coordinate0. P1 is affine with noise subspace span(e_0,e_2,...,e_(n-1)) and F e_0=e_1, all other columns zero. Its pair is controllable; P0 is also controllable.

At any chosen input, P1's output is uniform on one half of the possible P0 outputs. Thus on every adaptive transcript allowed by P1, its likelihood under P0 is exactly2^(-N) times its likelihood under P1. Adaptive query-choice and internal randomization factors cancel because their rules given the same previous transcript are identical. Pad a shorter protocol with unused queries if necessary to use a common worst-case N.

If the learner outputs the P1 law with probability at least1-delta under P1, it outputs that wrong law with probability at least2^(-N)(1-delta) under P0. Requiring failure probability at mostdelta under P0 gives

    N >= log2((1-delta)/delta)=Omega(log(1/delta)).

A confidence statement conditioned only on admission without any completeness requirement would not support this lower bound: an algorithm could reject everything. That is why the task above explicitly includes successful output on every controllable member.

## 3. Comparison with the acquisition procedure
For n sufficiently large and0<delta<=1/3, the two families imply a worst-case lower bound Omega(n+log(1/delta)), up to constant factors. The separately constructed procedure uses

    2n+ceil(log2(2/delta))+1

classical chosen-input samples and succeeds globally with failure at mostdelta/2 under its model promise. Thus its INITIAL TRANSITION-QUERY dependence has the right worst-case order in this access model.

This does not establish optimal bit-operation time, reset cost, source-code size, quantum gate complexity, model-misspecification robustness, or practical benefit. Strong ordinary active linear learners can attain the same order; they are not denied the observations or retained representation. The new simulation consumer and its real costs are separate from these ordinary acquisition lower bounds.
