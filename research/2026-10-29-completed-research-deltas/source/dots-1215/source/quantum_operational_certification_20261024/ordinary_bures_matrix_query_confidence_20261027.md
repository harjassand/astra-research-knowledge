# An acquired ordinary matrix query with a convex Bures confidence update

27 October 2026. A paid positive subroutine for the genuinely unflagged problem. This supplies each encoder-local matrix observation and its polynomial confidence update. It does NOT bound how many active encoder queries are needed for generic global discovery.

Imports: the received explicit online common-frame compiler; Section5 of `direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md`; the positive lift in `ordinary_convex_matrix_confidence_update_20261027.md`. Unlike a proposed relative-Keyl route, this uses the already compiled Bures estimator, not an unreceived efficient covariant-Keyl measurement.

## 1. Actual ordinary preparation of the loss density

Suppose all outputs of the supplied quaternion family share a physical support of dimension at most k. The uniform encoded Choi-rank bound R implies k<=min(s,8R) by spanning the four basis-encoder output supports; no support basis is supplied for free. The received online processor supplies one common k-output frame over a prescribed finite horizon.

At a chosen ordinary encoder x, independently choose one of the six Pauli eigenstates P_l, send it through the actual encoded source, feed the output through the SAME online frame, and prepare the receiver-local qubit state `(I-P_l)^T`. Discard the classical Pauli label after that preparation. The emitted pair has density

`T_U(x)=(1/6)sum_l E_(U,x)(P_l) tensor (I-P_l)^T`.

No reference or selector is retained coherently through the unknown source. One copy of T_U(x) costs ONE ordinary source call. Its dimension is d=2k. An exact identity improves the elementary six-mixture rank bound. In output-B/reference-A order, let J_x be the normalized source Choi matrix and rho_bar=E_x(I_2/2). Then

`T(x)=[2 rho_bar tensor I_A-J_x]/3`.

The six-state2-design identity gives this formula directly. Equivalently T is the normalized Choi state of E_x composed BEFORE the source with the qubit universal-NOT channel N(rho)=(2I_2-rho)/3, with tensor factors swapped. N has Kraus X/sqrt3,Y/sqrt3,Z/sqrt3. Hence

`rank T(x)<=3 rank J_x<=3R`,

and use `r=min(d,3R)` below. The Choi identity is a mathematical representation, NOT a replacement of the actual ordinary preparation by an entangled sender input. A homogeneous batch at fixed x is iid conditional on the common mathematical frame U and all PREVIOUS query records. It is important not to condition later analysis on undiscarded per-copy Pauli labels.

The processor may carry quantum memory from earlier queries. The causal arbitrary-operator common-frame identity, not an assumption that its physical memory resets, justifies this conditional iid description. All later queries retain and update that same frame.

## 2. Deterministic copy cap and actual estimator

For rational 0<m<=1/16, 0<beta<1, set

`D=2^ceil(log_2(dr))`,

`n(m,beta)=ceil[(80D/m) log(12D/beta)]`.                     (1)

Use the received random-purification channel on n copies of T_U(x), followed by its finite-Clifford pure-state tomography, a certified near-top eigenvector, and partial trace of the known purification register. The result is a genuine normalized density tau. Use the received eigen/backward error allocation `a<=sqrt(m)/4`.

The operator Bernstein and eigenvector argument in that receipt gives

`Pr[1-f(T_U(x),tau)>m | U,previous history] <= beta`,         (2)

where f is ROOT fidelity. The larger logarithm12D is conservative for this single bank. Since D<2dr<=12kR<=96R^2,

`n=O(R^2 log(R/beta)/m)`.

The source cap counts all n copies and all measurement branches. Known gates/arithmetic are polynomial in n,R,log s and the paid precision by the separately received frame and Bures primitives. This is not a claim of practical constants or low quantum memory.

For any deterministic finite query cap Q, encoder choices x_j may depend on earlier records. Allocate beta_j with sum beta_j<=beta_total and prescribe deterministic tolerances/copy caps. Conditional first-failure reasoning gives simultaneous events (2) with probability at least1-beta_total in the ideal common-frame description, and total calls exactly sum_j n(m_j,beta_j). A new fast Q bound is not inferred.

## 3. The confidence update is a literal SDP

Use the outer positive lift H from the companion note: H>=0, trace H=4, and its real-control contractions J_x(H) are TP qubit-channel Choi states. Let T_x(H) be its six-state loss density. This is a known linear map of H.

Regularize the acquired state by a PAID known amount

`tau_+=(1-m/64)tau+(m/64)I_d/d`.

The density is now strictly positive with minimum eigenvalue at least m/(64d). Because f(tau,tau_+)>=sqrt(1-m/64) and Bures distance obeys the triangle inequality, on (2)

`1-f(T_U(x),tau_+) <= (sqrt(m)+sqrt(m/64))^2
                       =81m/64 <2m`.                     (3)

Append the confidence constraint

`f(T_x(H),tau_+) >=1-4m`.                                  (4)

It contains the true H with strict slack. It has the exact finite-dimensional SDP representation: introduce a complex d-by-d matrix Z and require

`[[T_x(H),Z],[Z^*,tau_+]] >=0`,

`Re Tr Z >=1-4m`.                                          (5)

Indeed the maximum of ReTrZ under the block PSD condition is root fidelity. No signed reconstruction coefficient is declared a state, and no exponential decoder menu or hidden continuum-positivity oracle is present.

### Explicit strict-feasibility margin

For finitely many such cuts let m_min=min_j m_j and lambda=m_min/4. The known center H_c=I_(8k)/(2k) predicts T_x(H_c)=I_d/d. On the simultaneous good event, set H_mix=(1-lambda)H_true+lambda H_c as a PROOF point. It has minimum eigenvalue at least m_min/(8k), and every predicted T_x(H_mix)>=lambda I_d/d.

Joint concavity of root fidelity gives for cut j

`f(T_(x_j)(H_mix),tau_(j,+)) >=1-81m_j/64-lambda`.

Choose a maximizing block variable Z_j and scale it by1-lambda. This loses at most another lambda in its real trace. Since 2lambda<=m_j/2, its trace is at least1-113m_j/64, strictly larger than1-4m_j. Write the scaled block matrix by congruence from `[[I,(1-lambda)K],[(1-lambda)K^*,I]]`, where ||K||<=1. Its minimum eigenvalue is at least

`lambda min{lambda_min(T_(x_j)(H_mix)),lambda_min(tau_(j,+))}
 >=m_min^2/(256d)`.                                       (6)

Thus the augmented SDP has a known polynomial-bit Slater/inner-radius bound in its affine space. The trace bound on H and ||Z_j||_F<=1 bound the outer radius. Finite coefficient/arithmetic slack can be chosen smaller than explicit fractions of (6) and the trace margins. Polynomial weak SDP feasibility/optimization is consequently paid under this contract, not assumed for an arbitrary boundary-degenerate problem.

The proof point H_true is never supplied to the algorithm. Its existence establishes conditioning; the actual feasible/central model is found by the stated known-coefficient SDP. If the statistical event fails the routine may return INCONCLUSIVE, which is charged to its failure budget.

## 4. All decoder policies are constrained simultaneously

For the unnormalized full-CPTP decoder Choi C, Tr C=k but the useful OPERATOR bound is ||C||<=2, independent of k. To prove it, let lambda be its largest eigenvalue with normalized eigenvector v. Partial tracing C>=lambda|v><v| gives I_k>=lambda rho_v; rho_v has trace one and Schmidt rank at most two, hence lambda_max(rho_v)>=1/2 and lambda<=2. Using the loose trace bound kI here would incorrectly lose a dimension factor. Its loss is

`ell_C(x)=(3/2)Tr[C^T T(x)]`.

For any two states A,B, Uhlmann's theorem and the reverse triangle inequality give

`|sqrt((3/2)Tr[C^T A])-sqrt((3/2)Tr[C^T B])|
 <=sqrt(6[1-f(A,B)])`.                                    (7)

Hence the acquired density tau alone already gives root-risk radius sqrt(6m) for EVERY decoder at the queried encoder. More strongly, for EVERY H satisfying the confidence cut (4), combine (3),(4) and the Bures triangle inequality to get

`1-f(T_x(H),T_U(x)) <= (2+9/8)^2 m=625m/64<10m`.

Therefore

`sup_C |sqrt(ell_(H,C)(x))-sqrt(ell_(true,C)(x))|<sqrt(60m)`. (8)

For desired root-risk radius eta, choose m<=eta^2/64 (and m<=1/16). Equation(1) then costs O_tilde(R^2/eta^2) actual ordinary calls and supplies a whole-decoder confidence cut, with polynomial processing. Taking eta^2 of order gamma epsilon gives the requested rank-squared scale for ONE matrix query.

## 5. Finite implementation and honest missing global step

For final query-event failure beta, one may run the ideal inner tomography at beta/2 and budget its record-channel discrepancy at unhalved diamond <=beta; the extra total variation is at most beta/2. Finite preparation, random-seed generation, tomography and coefficient arithmetic must be included. The online frame's whole-process approximation can instead be transferred at the final averaged operational-channel level; it does not create an observable latent U or a quality guarantee for every exposed record. Specify a deterministic total horizon, quantum memory lifetime, compiled operation cap and total error budget before deployment.

The rank-squared COPY AND POLYNOMIAL-PROCESSING interface in this note is thus received-primitives composition, not the uncompiled Keyl variant. Local receiver ancillas, ordinary input controls, all flags, failed/unused records, growing frame memories and full-CPTP decoder synthesis remain charged.

What remains OPEN is a global adaptive encoder exploration theorem. Repeating (1) at every epsilon^-3/2 grid point restores the unwanted physical grid factor. The confidence SDP can retain all matrix cuts, and the known-model root-risk separation routine can compare two fitted models, but neither proves a cheap choice of informative models/encoders or a bound on sum_j 1/m_j. An acquisition proof must establish that cumulative cost, not merely provide a matrix estimator at a selected encoder. No generic ordinary-versus-coherent mission lower bound or completed rank-squared global learner is asserted here.
