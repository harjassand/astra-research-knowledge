# Independent whole review: contrastive partition discovery

## Verdict and binding

**PASS as a class-specific mathematical success theorem with a finite-bit deterministic prototype.** No sampled acquisition experiment or complete discovery-plus-reuse implementation is accepted. No source correction was required.

I read all seven frozen files, checked the proof and actual frontends/filter/greedy/refinement code, executed the nonmutating author harness, and added independent exact tests. Freeze `REVIEW_FREEZE_MANIFEST_20261031_2143UTC.json`, SHA-256 `3d097b5aa700148acc2534a492a66608e0d46c67f10848be1d7c7c7f39855734`.

Principal sources:
- `PROOF.md`: `377a806e5c81946e9fafe91af545769adfe39b213cab2d4c66b746b98e001fc0`.
- `construct.py`: `03215a65c21cc8c61bb56073ffa96535b1dded0a56d2538d809274b55c50ef77`.
- `check_construct.py`: `56a961c0826f65b81e483b03a59a19da6b69392fd16a08ecbe13674c589dfec7`.
- `construct_checks.json`: `f9d96efbd5216795d9a900b55e26659c5755423877c8ad33633564829b1ec62b`.
- `QUESTION_AND_FIRST_CONSTRUCTION.md`: `c5acff07256d76cdf1a0d700409f41f3d20ddf3f929b34cea6c534a82c629df0`.
- `PRIOR_AND_SCOPE.md`: `09e1de073341589ceba9b4366a65f3bbd1c953059bfbf2f4762ed9a15e7d21c1`.
- `README.md`: `9cc5066c5eda63a0077d9daaecf8b866b4a81b35486578065fa0451634d0ba82`.

The initial-question document is historical scaffolding; its preliminary implementation language does not override the complete proof or the explicit current README limitations. Previous archives and the new resolvent-control branch are not part of this receipt.

## 1. Unknown-class assumptions and observation acquisition

Balanced blocks imply Z/sqrt(k) is an isometry. Thus C*=ZDW has D's nonzero singular values, and its left range plus the constant vector is precisely the true block subspace. Both row and column centering of D are important: J C* J=C*, and the added constant direction is orthogonal to the resolved left singular space. D need not be symmetric or positive. No true rank, basis or prototype is passed to the frontends.

The quantitative gap and per-row contrast residual conditions are SUCCESS-CLASS hypotheses, not empirically verified conclusions. A common arbitrary background cancels from action contrasts in expectation only. Independent observation errors from both actions remain and are charged. Outside the success class the output is only a proposal and may refuse or be wrong; no false guarantee of structural identification is attached to an apparent rank.

The column-count certificate has the correct direction: if q_j exceeds (2X_j+8K)/N_c, then X_j<N_c q_j/2 and N_c q_j>8K, an exponentially unlikely Chernoff event. Union over both actions' n columns gives the specified confidence. Clipping B at n is safe for stochastic matrices; forcing B>=1 is conservative. An arbitrary source may require B of order n, so there is no universal favorable sample bill.

For each row sample the centered empirical matrix summand has norm at most 2/N. Its left variance accumulates to at most I/N, and the right variance is bounded by diag(column sums)/N<=B I/N. Rectangular Bernstein via a 2n-dimensional dilation and a union over two actions yields the displayed radius with K>=ln(4n/delta_s). The linear term 4K/(3N) is conservative for summand bound 2/N. On the column event, taking fresh fixed-design row samples conditional on that acquired cap is legitimate. The two action errors plus the class perturbation give ||C-C*||<=2tau+beta/2<=beta.

The code's ceil-log2 bounds dominate natural logarithms. Its sufficient N leaves real slack for outward root rounding: each analytic radius term is at most beta/16 and the dyadic root error at most beta/64. Consequently the frontend's actual check 2tau<=beta/2 is not based on a rounded equality. Source-count bit lengths and preliminary column observations remain paid. A total success probability must union the column, spectral, fresh-cleanup and later validation failures, plus any resolution-search attempts; the source does not get free unbudgeted searches.

## 2. Actual matrix-sign operation and rank

S=C C^T is positive semidefinite even for nonsymmetric/signed contrast. With R=||C||_F^2+4beta^2, X0=(S-4beta^2 I)/R has spectrum in [-1,1]. Unwanted singular values<=beta place their eigenvalues at most -3beta^2/R; wanted singular values>=Delta-beta>=3beta place them at least5beta^2/R. The smaller declared a is therefore valid under the success hypotheses.

The cubic p(x)=(3x-x^3)/2 preserves [-1,1], is odd, expands magnitudes below 1/2 by at least 11/8, and obeys 1-p(x)<=3(1-x)^2/2 above 1/2. The code first counts enough expansion rounds, then iterates the upper scaled error q from 3/4 by squaring until (2/3)q<=nu/8. It uses only rational bounds, not a queried singular gap/eigensolver. The number of rounds has the claimed logarithmic dependence.

Entrywise floor rounding preserves symmetry because opposite entries are exactly equal before rounding. For matrices within nu/8 of a norm-one ideal iterate, expanding the cubic gives the conservative operator Lipschitz constant 4. The declared n*2^(-b)*4^(T+1)<=nu/8 dominates the entire geometric sum of initial and per-round errors and also maintains the small-error premise inductively. This is an operator-norm argument, not an entrywise-to-spectral assumption without the n factor.

Adding the constant projector to (I+Y_T)/2 gives the promised approximation to the resolved projector plus the constant direction. Trace error is at most n*nu<1/2; nearest-integer rank therefore recovers r under the class assumptions. The output's rational numerator/denominator implement that same formula. Divisor/range/trace checks are receiving sanity checks, not tests that the unknown class hypotheses are true. Zero contrast legitimately produces a rank-one constant proposal outside the claimed r>=2 success class.

The backend really performs dense matrix products with object integers and fixed dyadic rounding. Its O(T n^3) arithmetic and O(n^2) matrix storage are paid, along with formation of C,S, common denominators and input reading. Cubic intermediate bits grow by constant multiples of b plus log n, not an unbounded exact iteration denominator cascade. This does not make the backend competitive with a good ordinary SVD.

## 3. Coarse clustering and exact fresh cleanup

The elementary singular-subspace identity bounds the component of each resolved left singular vector outside the true block space. Summing and using equality of subspace ranks gives the stated Frobenius projector bound. Adding numerical error with the factor-two squared-norm inequality yields equation(4). Dividing by (s0/16)^2 gives exactly the bad-row bound in(5). Delta>=256sqrt(r)beta and nu=1/(1024n) make it strictly less than k/16.

The greedy proof does not assume known good rows. Before each round at least one remaining true block has all its good rows available. Its good rows lie within s0/8 of each other, so some radius-s0/4 ball contains at least k-b_bad points. That number exceeds the total bad count, ensuring the selected ball has a good point. All its good points belong to one block since different good blocks are separated by at least 7s0/8. The selected center is consequently within 5s0/16 of that block's true projector row. Enlargement to s0/2 includes every good row of that block and excludes every other good block. Removal can only harm bad rows. After r rounds, arbitrary leftover assignment still confines all misclassification to the original bad set.

The code's squared thresholds r/(8n) and r/(2n) are precisely (s0/4)^2 and (s0/2)^2. It pays all pairwise row distances and selection work, without a k-means optimizer. After analytic label alignment, both row and column sums of |T-I| are bounded by 2b_bad/k: each lost or gained wrong label belongs to the same global bad set. Hence ||T-I||_2<1/8, despite potentially unequal PROPOSAL cluster sizes.

Fresh cleanup uses indicator lifting by proposal blocks, not a uniform-within-proposal averaging that would introduce a wrong normalization. Its expectation is D[g,:]T plus residual of L1 norm at most beta/32. Since e_g-e_h is centered, the least nonzero singular value gives row-prototype separation sqrt(2)Delta, reduced by at most the factor7/8 under T. Two actions' coordinate Hoeffding errors contribute at most beta/32 in L2; adding the structural residual places every feature within beta/16 of its correct prototype. Thus within-block distances<=beta/8 and cross-block distances>beta/4. The exact representative scan is valid in this regime, not an assertion that arbitrary threshold graphs can be solved by that scan.

The required fresh count N_f>=2048r ln(4nr/delta_f)/beta^2 correctly unions two-sided coordinate errors over two actions, n rows and r proposal blocks. The proposal is frozen before those samples. The frontend builds features from complete equal row totals and binds the caller's old-proposal hash; it does not receive oracle prototypes. Final balanced-size/rank checks may refuse elsewhere. Authentic freshness is still external, not established by count arrays.

## 4. Precise join to the existing reuse certificate

The c/e notation in Section 6 matches the norm-free full-record receiver and must be interpreted as follows:

    c = max_(a,i in g) TV((A_a Z)[i,:], (W A_a Z)[g,:]);
    e = max_(a,g) ||(W A_a Q)[g,:]||_(H^-1), H=I/n;
    d = max_(a,g) ||(W A_a Z)[g,:] - B_a[g,:]||_1.

When K reduces P and the macro term is Z C_a W, both are closed under the relevant projection, so these two leakages arise solely from R_a. If every row of R has L1 norm<=eta, the row difference R_i Z minus its true-block average has L1 norm <=2eta, hence c<=eta. For e, the averaging row has Euclidean norm1/sqrt(k); multiplying by RQ gives at most rho/sqrt(k), and H-dual normalization multiplies by sqrt(n). Thus e<=sqrt(r)rho. These are correctly different norms; no c/e interchange or dimension-free outgoing claim occurs.

The fine stochastic model error d, actual initial law, task/control language, sampling confidence and finite-bit validation still have to be acquired separately. Discovery frontends do NOT execute this receiver. Reducing K alone is not a license to assume d or a small full-record E_L. Small residual bounds are an existence/success-family observation, not a supplied empirical certificate.

The explicit nonreducing-background example correctly has exact action contrast (P-J)/10 and exact recovered partition, yet true two-step value 91/100 versus projected value 101/200, difference 81/200. Thus even perfect recovery of action-effect classes is not dynamic sufficiency. This is a substantive limitation, not an artifact to remove by relabeling the output as a model.

## 5. Executed evidence, task binding and limitations

All seven frozen files/hash sizes verified and originals left unchanged. The author harness reran nonmutating: 37 exact checks and 5 refusals, including corrupted initial-label cleanup, full-rank centered perturbations, zero contrast and the 81/200 failure.

Additional reviewer tests in `reviewer_2149/extra_checks.py` passed 68 exact checks and 5 additional refusals. They cover genuinely nonsymmetric cyclic macro contrasts of both signs, numerical projector/rank/clustering bounds, and explicit c/e receiving inequalities for small stochastic perturbations of a reducing background. Wrong proposal hashes, boolean resolution and invalid count totals reject. Reviewer files are separate and contain no new observations.

The successful huge-count frontend unit arrays are explicitly FABRICATED deterministic fixtures. Zero source observations were executed. The sufficient schedules near 10^12--10^14 calls are neither executed datasets nor sample lower bounds. Column-cap acquisition, failed search rounds, cleanup and independent reuse validation all remain separate paid operations. The schema is a typed scientific prototype with assertions enabled, not a proof of sampling provenance or a hostile arbitrary-record security service. Caller-supplied expected resolution/confidence and proposal identity do not certify unknown class membership.

I freshly opened the primary cPCA paper https://arxiv.org/pdf/1709.06716 and Lei--Zhu https://www3.stat.sinica.edu.tw/sstest/oldpdf/A27n413.pdf. They establish close ordinary precedents for background contrast and sample-split approximate-to-exact community cleanup, respectively. Their covariance/graph observation models are not identical to this two-action row-sampling model, but that distinction alone proves no novelty. Matrix Bernstein, spectral subspaces, polynomial sign iteration and deterministic clustering are also ordinary components. Every strong spectral/multiview method receives the same observations and legitimate row metadata and can use the same later validation.

The accepted result is the particular class-specific finite-bit discovery construction and its honest boundary with reuse, not demonstrated comparative superiority, an empirical learning success, a complete simulator/planner, or a consequential new application. The pending resolvent-control foothold and all old/new physics or capacity constructions remain outside this receipt.
