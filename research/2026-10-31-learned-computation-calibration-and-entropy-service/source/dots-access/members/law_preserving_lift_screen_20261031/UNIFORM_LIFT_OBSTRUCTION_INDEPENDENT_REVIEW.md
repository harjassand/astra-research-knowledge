# Independent review: known-uniform lift acquisition obstruction

## Verdict and binding

PASS for the exact rigidity identity, its stated approximate-reference extension, and the total-query acquisition obstruction. This is stronger than the earlier unknown-support Index Erasure example: full-support uniform pi and its pure preparation are free here, yet acquiring the specified coherent law-preserving interface can still require square-root-in-dimension oracle queries. It is not a lower bound on ordinary forward classical simulation, arbitrary inspectable programs, or online reuse after paid preprocessing.

I read the complete initial body and then the complete final version. Bound source: `UNIFORM_STATIONARY_LIFT_ORACLE_OBSTRUCTION.md`, 12,719 bytes, SHA-256 `0aa48e1df1ff88050b21c31e7c8fef896610fdc904a5382574c89551598d2739`. The earlier 10,967-byte source SHA `824e1973068b8663de8cc59578b1b11ac8547e1111add0d00f98ac328042e087` is not the final binding. Query accounting and the direct distributional reduction are explicitly included in the final source.

## 1. Rigidity for every eligible dilation

For fixed output y, the exact adjoint law for |y><y| says that the environmental column vectors v_yx have Gram matrix diag_x P(y|x). They are therefore pairwise orthogonal with squared lengths P(y|x). Pure fixedness of psi implies each Kraus operator sends psi to a scalar multiple of psi; the scalar vector c is normalized by trace preservation. The row identity sum_x sqrt(pi_x)v_yx=sqrt(pi_y)c then gives

<c,v_yx>=sqrt(pi_x/pi_y)P(y|x).

All factors and the orientation of the balanced matrix are correct. Thus A=D_pi^(-1/2) P D_pi^(1/2) is forced, not an optional feature of the author's inverse-fibre construction. This uses the full diagonal-adjoint law; agreement only on classical transition probabilities of diagonal input states would not force environmental orthogonality and would not suffice.

The identity holds for any Kraus/Stinespring representation satisfying the premises, with its actual c and phase. It supplies a necessary coherent block once the appropriate environment reference is prepared. It does not itself imply a return bound for the remaining environment/source dynamics.

## 2. Oracle family and exact inversion

P_f=(U_f+J)/2 has known strictly positive uniform stationary law. Forward sampling uses at most one classical evaluation query. Its supplied forward maps coalesce whenever a reset occurs, so failure after m steps is 2^-m. The stationary source state is the known n-qubit plus state. These conveniences do not supply evaluation of f^{-1} or an in-place permutation unitary.

The oracle model is the self-inverse XOR evaluation O_f, not the in-place map U_f. A reversible circuit for W can be reversed using the same number of XOR queries. The source correctly requires clean-ancilla reversible circuit access, rather than assuming that an irreversible channel box or an unknown consumed quantum program provides W^dagger.

One W application to plus followed by known source unpreparation prepares the actual environmental reference c. Applying W^dagger to c and y, and measuring the clean-input-ancilla flag, gives unnormalized source P_f^dagger|y>. Its inverse-label amplitude is 1/2+1/(2d). The probability of that label together with the clean flag is at least 1/4, without dividing by a postselection probability. One extra forward query verifies the candidate. Fixed-small synthesis errors can be budgeted at the amplitude level; a combined error at most 1/16 leaves at least 7/16 correct amplitude in the exact-reference reduction.

## 3. Robust approximate-reference calculation

For an exact isometry with exact diagonal law, let v=(I tensor <s|)W|s>. The best normalized product reference is c=v/||v|| and the minimum squared vector distance is 2-2||v||. Thus the assumed error epsilon implies ||v||>=1-epsilon^2/2. Measuring the known-source-plus flag prepares c with success at least (1-epsilon^2/2)^2. Failure is an ordinary failed attempt, not free normalization or an unbounded expected-time routine.

Writing r_y=sum_x v_yx-c gives sum_y||r_y||^2<=d epsilon^2. Orthogonality of the row vectors yields

sum_x |A_yx-P_f(y|x)|^2 <= max_x P_f(y|x) ||r_y||^2.

The sign of the row-error inner product is immaterial to its square. Summing proves ||A-P_f||_F^2<=d epsilon^2. Restricting to the correct inverse entry in each row and applying the normalized L2 triangle inequality gives average inverse-success probability at least (1/2-epsilon)^2 conditional on successful c preparation. Multiplying by its actual flag probability proves the stated positive constant for epsilon<=1/4.

This is an average-target amplitude statement, not a uniform row operator-norm statement. The source now receives exactly the needed distributional lower bound rather than silently strengthening the estimate. Approximate preservation of the diagonal process itself is not covered by this argument without an additional error hypothesis. Refinable implementation error can be separately made a sufficiently small constant.

## 4. Distributional reduction and total acquisition cost

For uniform oracle permutation f and independent uniform XOR shift z, f'=f xor z is uniform and independent of y'=y0 xor z: for each z the map f -> f xor z is a bijection of permutations. Moreover (f')^{-1}(y')=f^{-1}(y0). Each query to O_f' uses one O_f plus a known output XOR. This supplies the uniform-target input needed by the robust bound while reducing to a fixed-target inversion problem under a uniform permutation.

A verified inversion attempt of success probability s returns the correct inverse parity; on failure an independent fair guess has success one half. The resulting decision success is 1/2+s/2. No repetition is needed to obtain a constant distributional advantage. I inspected the primary [Nayak 2011 paper](https://www.math.uwaterloo.ca/~anayak/papers/Nayak11.pdf), especially Theorem 1.1 and Corollary 1.2: the latter gives the requisite square-root query lower bound for fixed-target inverse parity on uniform permutations in the value-query model. I also inspected the primary [Ambainis paper](https://arxiv.org/pdf/quant-ph/0002066), whose inversion lower bound provides the ordinary worst-case comparison. The distributional Nayak statement is sufficient for the present reduction; no unsupported replacement of inversion by unstructured search is used.

The charged attempt has q_acq queries for acquisition of the reusable classical circuit/advice, one q_use invocation to prepare c, one q_use invocation of the reversed circuit, and one verification query. Therefore q_acq+2 q_use+1=Omega(sqrt(d)) for the stated uniformly correct acquisition guarantee, with a constant set by the fixed success advantage. An acquisition routine with its own unbounded or unspecified failure probability is not covered by pretending it always outputs a valid lift; such a guarantee must be included if that variant is proposed.

The conclusion is about total acquisition plus the bounded number of uses. Learning and retaining a full permutation/inverse table can make later online calls cheap after expensive acquisition. Nothing in this receipt asserts an online-only Omega(sqrt(d)) lower bound with arbitrary free preprocessing or f-dependent advice. Likewise supplying in-place U_f and its reversible circuit changes the access model and can eliminate the obstruction.

## 5. Existence and return are distinct

The displayed channel Phi_f(rho)=U_f rho U_f^dagger/2+|s><s|Tr(rho)/2 genuinely exists, fixes s and has the desired diagonal law. Since U_f fixes s, its adjoint maps Q to Q/2. Four uses give the 1/16 return certificate. This demonstrates that neither existence nor a favorable abstract return horizon is the bottleneck; the missing resource is acquiring the coherent realization from forward XOR access.

The one-bit contrast is also correct. X-dephasing and immediate plus reset have identical classical J restriction, pure fixed plus state and forced overlap A=J, but the former preserves the minus state while the latter eliminates it. Thus balanced-kernel access is necessary for the eligible lift but not sufficient to earn purification. The environment/complement choice and its return certificate remain separate operations.

## 6. Decisive scope

This result establishes a concrete access-model barrier to automatically promoting a cheap forward coalescent sampler into a reusable pure-reference law-preserving quantum source. It no longer relies on an unknown stationary support. It does not establish that all explicit reversible programs are hard to analyze, that classical sampling is hard, that every downstream source-controlled observable is hard, or that quantum compilation is practically superior.

The organizing requirement is actual acquired reverse/balanced-kernel coherent access together with a separately proved purifying outlet/return certificate. An ordinary forward classical implementation already handles this example cheaply. The negative result narrows which future raw-program classes could add capability rather than merely assume a difficult interface. All primary lower-bound machinery is credited; no historical novelty claim or comprehensive literature exclusion is made.
