# Independent review: isotropic dark-direction pollution under streaming growth

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`. **Accept the root's exact two-class recurrence, eventual absorption law and stated IID label-model scope.** This receipt does not review the separate channel-support impossibility argument in `GOVERNING_DRAFT.md`. The finite-cap computation below is an additional independent diagnostic, not a physical source-call theorem.

## Full subset CP derivation

Work in the unknown label state's eigenbasis only as an analysis coordinate system: label0 is c, others span W. Let |I> denote the normalized wedge of a sorted k-subset I. Fresh eigenlabel j has probability lambda_j. The physical controller is basis independent and is not given this eigenbasis.

If j belongs to I, antisymmetric growth fails certainly and discarding the fresh register preserves |I>. If j is outside I, put U=I union{j} and t_j=(-1)^{number of elements of I larger than j}. The wedge decomposition is

|U>=(1/sqrt(k+1)) sum_{l in U} t_l |U minus l> tensor |l>.

Thus successful projection has amplitude t_j/sqrt(k+1) onto |U>. On failure, tracing the final register produces Kraus amplitudes

K_{l,j}|I>=[1_{l=j}-t_j t_l/(k+1)] |U minus l>.

For l=j this is k/(k+1) on the old subset. For each l in I it is a signed1/(k+1) replacement of l by j. Together with input weight lambda_j, full subset transitions are:
- success I→I+j: lambda_j/(k+1);
- failure I→I: lambda_j k²/(k+1)²;
- failure I→I-l+j, each l in I: lambda_j/(k+1)².

These sum to lambda_j. For fixed fresh/discarded labels each Kraus matrix is partial monomial with distinct output rows for distinct input columns. Hence its K†K has no unchecked off-diagonal entries. The supplied independent code constructs all these matrices in sparse column form, verifies all4,509 old-subset/fresh-label column normalizations and630 Kraus injectivity checks for d=9,k=1,...,7, then builds their full population transitions. Diagonal old-subset mixtures remain diagonal; no unjustified coherence deletion is used.

## Two-class reduction and absorption

With lambda_0=x and other eigenvalues a=(1-x)/8, aggregate only after constructing the subset maps. When0 is absent, replacing any of k occupied bright labels by0 has total probability kx/(k+1)². When0 is present, replacing it by one of9-k absent bright labels has total probability(9-k)a/(k+1)². Success probabilities are precisely the displayed S matrix. The column sums of S+F equal one, and the two classes are strongly lumpable: every individual subset in a class has the same aggregate transition probabilities. The root's F matrix therefore tracks the actual CP instrument, not merely a heuristic occupation process.

At fixed k, the failed-repeat distribution is F^n v. Summing n>=0 gives (I-F)^-1v, so S(I-F)^-1v is the next successful-stage distribution. For0<x<1/9 (indeed for0<=x<1 while growth remains possible), finite dimension and positive remaining bright mass ensure eventual absorption. The expected records at that stage are1ᵀ(I-F)^-1v. The first record is separately counted.

I independently differentiated this fundamental-matrix recurrence at x=0, using n'=(I-F0)^-1(v'+F' n0), instead of copying the root's final rational expression. It gives final error derivative9218/315 and zero-pollution expected normalized-record count4609/35. Exact arithmetic at x=1/100 gives final error6356434794173146283/26029075009971200900=0.24420517408851938, matching the root. At k=8, a subset containing0 omits a bright direction, so Hodge output is orthogonal to c. Symmetry distributes this error uniformly over conjugate(W); final infidelity equals the class1 mass.

The one-shot comparison follows from the nine possible missing labels: good weight a^8 and bad total8xa^7, giving64x/(1+63x) and slope64. Repeated growth reduces this coefficient but does not remove contamination.

## Finite cap changes accepted-state accuracy

A cap N counts total normalized input records, including the first. Start with probabilities lambda_j on singletons, apply the full CP transition once per further record, and make size-eight subsets absorbing. Let p_N be total absorbed mass and e_N the absorbed mass containing0. Successful-output infidelity is e_N/p_N only when p_N>0; otherwise no normalized accuracy is asserted.

For x=.01, exact full-subset and independently lumped two-class finite-cap propagation agree through N=64. Exact rational two-class propagation continues to1024:

| Record cap | Readiness p_N | Conditional infidelity |
|---:|---:|---:|
|8|9.0555341070e-8|0.3926380368|
|16|0.0001940416|0.3742496350|
|32|0.0129234972|0.3463379499|
|64|0.1738211971|0.3078893115|
|128|0.6459161962|0.2679464497|
|256|0.9605051281|0.2469844931|
|512|0.9995761074|0.2442357704|
|1024|0.9999999514|0.2442051776|

Raw exact probabilities through64 are retained in `finite_cap_exact.json`; displayed decimals are rounded. A cap of8 permits only all-growth histories and recovers the one-shot conditional error, as a useful boundary check. Eventual error must not be assigned to finite-cap accepted outputs. These counts are NOT ordinary source calls: a physical minus-label acquisition probability, history dependence and source backaction need separate treatment.

## Accurate robustness and provenance scope

The result is an exactly solved IID isotropic LABEL model with ideal Lüders controls. It is not derived from arbitrary physical source depolarization, approximate common symmetry, control errors or correlated records. It cannot be transferred to those settings merely by matching one marginal eigenvalue. It also does not calculate errors after the nonlinear heralded spinor transducer or subsequent gate use.

The precise adverse conclusion is **error amplification rather than noise purification** near x=0, with a poor24.4% program error at1% label pollution. The finite slope also establishes local linear continuity within this restricted IID family. Thus an unqualified claim that no approximate robustness exists would be too strong; the root's values demonstrate a limitation, not a general robustness impossibility theorem.

Primary source checked directly2026-10-29: Bene Watts et al., *Anti-symmetrization is cheap and useful*, https://arxiv.org/abs/2610.06737 and https://arxiv.org/pdf/2610.06737, Algorithm1 failure equation25/26 and Algorithm2/Theorem5. The paper already supplies streaming growth with failed-new-record discard and exact complementary projector action on the old antisymmetric subspace. No new growth-algorithm or generic sample-complexity priority is claimed here. This receipt concerns the root's added pollution calculation and its independent verification.

Original root sources were not modified. `independent_subset_cp.py` and `independent_absorption_derivative.py` reproduce the checks with exact rational arithmetic. These are analytical/computational diagnostics, not Monte Carlo measurements or hardware data.
