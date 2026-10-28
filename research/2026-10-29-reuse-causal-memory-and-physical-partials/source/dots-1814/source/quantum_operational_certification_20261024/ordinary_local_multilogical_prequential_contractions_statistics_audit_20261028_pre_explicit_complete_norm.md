# Independent statistics audit of local simultaneous recovery with retained memory

28 October 2026. Reviewer `producer-workspace/audit_count_pilot_fresh`.

**PASS at the promised common-algebra, uniform-contrast, private-terminal scope.** Final source `ordinary_local_multilogical_prequential_contractions_20261028.md`, SHA-256 `bf75d786ce1a815cb122c78b39df85f84f32842319fe36bcf95edc7af1f14808`. The earlier `c1505e16aa6c4222826ac69ba9c7ad6825d191648c383d0d8d4792db2a924202` source is preserved; the final changes only specify finite rational bounds, canonical dyadic choices and the ancilla-basis control charge. This audit covers actual product-Pauli records, martingale localization, selected-patch online contraction learning, finite rational processing and complete statistical/resource accounting. It independently checks the new statistical composition and imports only the already received algebraic colored receiver and private-terminal channel principles. It does not import the old constructions' iid acquisition assumptions. No source calls, random draws, count acquisition, hardware experiment or generic optimization/Jacobi execution occurred. Deterministic exact checks enumerate finite Born laws; they do not sample them.

The theorem requires one fixed compatible hidden local logical algebra, a supplied uniform CP-order generator contrast after every allowed prior history, a fixed supplied encoder, private fresh current labels and a complete trusted-interface implementation budget. Comparison to the unrestricted joint recovery oracle additionally requires the separate global Pauli CP-dominance promise. These assumptions are not learned or certified by the records.

## 1 Actual correlated measurement laws

For any one-qubit operator T, direct summation over the three uniform Pauli bases and their Born outcomes gives the linear maps

`M(T)=T`, and `Phi(T)=T+2 Tr(T) I`,

where M and Phi are the first- and second-snapshot measurement-linear maps. For normalized states these are the corresponding expectations. Tensoring these linear maps is valid on an arbitrary entangled input operator, not only product states. Consequently, for the current normalized marginal rho_J,

`E Z_J=rho_J`,

`E Z_J^2=sum_(S subset J) 2^(|J|-|S|) rho_S tensor I_(J\S) <=3^|J| I`.

Each individual factor has eigenvalues 2 and -1; its squared Frobenius norm is 5. Thus every record has exactly the stated operator and Frobenius norms. Measuring other output sites and then averaging their current outcomes leaves the marginal law unchanged. Conditioning on those other current outcomes would in general change it and is not used.

The measured physical output can be correlated with the inaccessible source memory. At the complete prior classical history h it still has a well-defined conditional density matrix, to which the one-copy calculation applies. The next conditional state may change arbitrarily after the actual measurement backaction. Nothing in this argument asserts iid copies or reconstructs the memory.

Fresh independent logical signs and axes are averaged in the conditional expectation given h. In particular, averaging all other logical inputs makes them maximally mixed. For a fixed i and its own sign, the marginal is rho_h+s Delta_(i,j,h). Therefore the coarse signed matrix s_i Z_J has mean Delta_(i,X,h)^J. For fine acquisition,

`E[-1{j_i=j} s_i Z_(W_i) | h] = -Delta_(i,j,h)^(W_i)/2`.

The one-half is exactly the probability of the own input axis; it already matches the gradient of the declared loss. There is no missing importance factor. The conditional second moment of a fine gradient is actually (1/2)5^W in squared Frobenius norm, but the theorem safely uses the larger deterministic bound 5^W.

The same global record can be reused in classical computations for overlapping intervals. It is one compatible product measurement, not two incompatible quantum measurements or cloning. Different learners' records and gradients need not be independent. Our exact Bell-state example has covariance 1 between two local shadow estimates with zero individual means. A separate physical two-logical example shows that conditioning on the other learner's current input sign changes the claimed marginal signal. These witnesses are retained as checks against precisely the shortcuts the manuscript excludes.

## 2 Coarse martingale localization

For each fixed i,J, let Delta_t be the conditional signed mean and X_t=s_i Z_J-Delta_t. Even when Delta_t does not commute with individual snapshots,

`E[X_t^2 | past]=E[Z_J^2 | past]-Delta_t^2 <=3^w I`.

The cross terms collapse because E[s_i Z_J | past]=Delta_t. Also ||Delta_t||<=1, so ||X_t||<=d0+1<=2d0. Applying Matrix Freedman to both signs yields exactly the displayed two-sided bound. The inspected primary theorem is Tropp, *Freedman's Inequality for Matrix Martingales*, Theorem 1.2, printed page 264. Its hypotheses are martingale adaptedness, an almost-sure increment bound and predictable quadratic variation, not independent increments. [Primary paper](https://tropp.caltech.edu/papers/Tro11-Freedmans-Inequality.pdf). The separately saved primary-import note records the version and scope of the read.

With a=kappa/(8d0),

`2(3^w+2d0 a/3)<=4*3^w`.

Thus the exponent is at least `N0*kappa^2/(256*12^w)>=L0`. Since ceil(log2 x)>=ln x for x>=1, the union over qM0 martingales is at most beta0. Correlations among these processes do not change the union bound. Operator error a becomes trace-norm error at most d0 a=kappa/8.

The predictable means need not be constant in time. A true containing patch nevertheless has trace-norm average at least kappa because the SAME fixed true reflection pairs with every summand to give at least kappa. Cancellation of moving gauge states cannot remove this lower bound. A disjoint patch has zero mean at every history by conjugation with the complementary true logical reflection supported in the traced-out interval. This uses the common algebra and gauge commutation, not a generic locality heuristic.

The finite score error kappa/16 leaves containing scores at least 13kappa/16 and disjoint scores at most 3kappa/16. Hence selecting the first score at least kappa/2 guarantees overlap on the one simultaneous coarse good event. Boundary clipping and padding still contain the true width-at-most-w support. The received algebra-packing argument then validates the color guard. Passing the guard alone does not certify the model or the good event.

## 3 Adaptively selected envelopes and expected online regret

Condition first on an arbitrary complete good coarse history. Its selected envelopes are then fixed, the corresponding common true B_(i,j) is feasible, and the future uniform contrast promise holds for the resulting conditional quantum memory state. All future own/other labels remain fresh. This conditioning is not on future observations or future estimator success. The coarse event costs beta0 only once after averaging.

For Hermitian contraction A and reflection B, define P=I-(AB+BA)/2. Since ||AB||<=1, P is PSD. Cyclicity and [R,B]=0 give

`e=L(A)-L(B)=(1/2)Tr(RP) >=(kappa/2)Tr(rho P)`.

Also A^2<=I gives

`a=Tr rho(A-B)^2 <=2Tr(rho P) <=4e/kappa`.

No commutation of A with R or rho is assumed. The common B minimizes the loss pointwise, even if its raw loss is large. Thus this is an excess-risk mechanism, not a small-raw-noise claim.

The Frobenius radius from zero is sqrt(d)<=R0; the contraction domain diameter is 2sqrt(d). An exactly feasible next iterate within u of the true projection changes the usual comparator squared distance by at most 4sqrt(d)u+u^2. Consequently the manuscript's pathwise bound is

`d/(2eta)+(eta/2)N G0^2+N(4sqrt(d)u+u^2)/(2eta)`.

Substituting eta=R0/(G0 sqrt(N)) and u=1/(16R0 N), the first two terms sum to at most R0 G0 sqrt(N), while the final term is less than G0 sqrt(N)/(7R0). This is below 2R0 G0 sqrt(N). Taking the conditional expectation against the fixed true B turns the measured-gradient inner products into the declared losses. Correlated learners, time-varying conditional objectives and arbitrary measurement backaction remain allowed. Fine acquisition receives an expected-risk statement, not a simultaneous high-probability fitted-state guarantee.

## 4 Finite clipping and exact physical controls

The imported rational Jacobi primitive is restricted to known classical matrices. Scaling Y to Y/(4L)+I/4 puts its spectrum in [0,1/2]; L=2+R0 suffices because ||Y||<=1+eta*2^W<=1+R0. The primitive's Frobenius off-diagonal certificate zeta/4 becomes at most tau after multiplying back by 4L when zeta=tau/L. Clipping its diagonal labels gives a rational exact contraction, and nonexpansiveness of convex projection bounds its distance to the true clip by tau. No unknown eigenspaces, spectral gap or positive eigenvalue floor are supplied.

For the fixed entry grid, Hermitian rounding has Frobenius error at most 2dv<=t0/2. Dividing by 1+t0 gives exact contraction feasibility. Relative to the pre-rounded contraction its extra error is at most t0(sqrt(d)+1/2)<u/8. With tau=u/4, the total is safely below u. A fixed denominator for the repaired iterates prevents recursive precision growth. Choosing the largest admissible dyadic v gives a bit length O(log d+log R0+log N); source-independent known-matrix processing pays the polynomial dimension and precision costs.

For the physical reflection S, rational Q is exactly unitary and rational diagonal sign labels, including sign(0)=+1, give S^2=I exactly. Finite synthesis approximates this declared exact-reference control within the whole-process budget; floating eigenvectors are not declared physical. On each opposite-sign overlap between B and a C eigenvalue, |b-c|>=1. Using the joint eigenbasis of rho and B proves

`Tr rho(B-S)^2 <=4Tr rho(B-C)^2 <=8a+8b^2 <=32e/kappa+8b^2`.

The backward error is Frobenius at most b, so it is also operator at most b. Taking the largest admissible dyadic b guarantees a finite logarithmic precision cap without any source spectral premise. Our exact examples include a zero C label, noncommuting R and rho gauge factors and an extremely small occupied gauge eigenvalue.

The received colored-cone inequality applies to the constructed SINGLE joint unitary receiver with distinct mixed ancillas. The current source's retained quantum memory can be included in the gauge purifier. Ideal elementary prefixes preserve the logical-plus-ancilla maximally mixed marginal even when the gauge is correlated with retained memory. Thus this is an algebraic import at each conditional history, not an import of iid acquisition or a sequential deployment of independent fitted decoders.

## 5 Complete expected loss and finite call arithmetic

Combining the two per-axis regrets with the received weighted cone inequality gives

`average ell0 <=288AqR0G0/(kappa sqrt(N))+36Aq b^2`.

The stated N makes the first term at most epsilon/4. The b choice makes the second at most epsilon/8. Good coarse histories therefore contribute at most 3epsilon/8. Bad coarse histories and guard failures are retained in the protocol and cost at most beta0=epsilon/8, since Bell loss is at most 1 and the comparison loss is nonnegative. Their complete fixed schedule remains in the comparator definition and resource cap. A complete implementation discrepancy nu<=epsilon/4 leaves total excess at most 3epsilon/4, strictly inside the claimed epsilon allowance.

The ideal terminal time is uniform over all N potential fine calls and independent of source, payload and probe randomness. The unknown q-qubit payload and its complete reference are initially product with acquisition and are held isolated. Hence the existing private-terminal identity applies to one simultaneous q-qubit input: the averaged actual terminal channel is the mixture of conditional current source maps and the already frozen joint receivers. The all-probe extension is only an analysis construction. No hypothetical post-terminal queries are charged as if performed, and no future frozen-decoder service is inferred.

At each history the gauge Bell blocks give the upper comparison by ell0 without requiring global dominance. Under the separately supplied CP dominance, the same D_* is pointwise optimal over all joint CPTP decoders, hence also optimal among fixed decoders on this occupation. The comparator is the occupation of the declared ideal trusted-interface controller, not a counterfactual path generated by deploying the oracle and not the imperfect implementation's changed histories. A single complete-process allowance does not silently move that comparator.

N is a power of four, so sqrt(N), eta and the terminal sampler are exact finite numbers. Because the threshold exceeds 1,

`N <4[1152AqR0G0/(kappa epsilon)]^2`

`  <=32*1152^2 A^2 q^2 10^W/(kappa^2 epsilon^2)`.

Thus the stated fixed-width q^2, epsilon^(-2) call scale is sound. This is not an epsilon^(-1) small-loss theorem. The coarse term uses log(q(n-w+1)) but every call still prepares q actual inputs and measures n physical outputs; physical traffic and storage are not logarithmic in n.

## 6 Randomness and physical resource scope

Let Bcalls=N0+N and J_rng=n Bcalls. Each local-axis draw accepts three of four two-bit values, so exhausting R trials has probability 4^(-R). The declared R_rng gives J_rng*4^(-R_rng)<=nu_rng, conservatively. The ideal-process proof couples to this capped sampler until an exhaustion and debits the prescribed physical replacement inside the one operational budget. It does not condition the regression proof on an eventual no-abort event.

The cap

`log2 N+qN0+2qN+2nBcalls R_rng+q`

includes the exact private terminal draw, coarse signs, fine signs/axes, every physical output measurement-axis choice and the mixed-ancilla bits. Optional whole-input/output Pauli framing adds 2q bits and its gates. Fine output-axis choices and possible updates at the terminal slot are conservatively overcounted; they are not omitted from the worst-case cap. All numerical accuracy bounds are used through finite rational descriptions, with canonical dyadic choices where needed.

The learner stores local classical matrices and records, not a global 2^n source matrix or the source memory. Each possible fine slot pays local matrix updates and sign compilation before its current private inputs. The actual coherent receiver uses 3q known controlled reflections and 4q ancilla Hadamards for the two basis-conjugated C_Z gates per block, or includes those changes in direct C_Z synthesis without counting them twice. Distinct reset/mixed ancillas, reversible routing and isolation of all final outputs are paid. Dense local synthesis retains its exponential 4^W cost. Timing padding, calibration measurements, quantum storage and controls must jointly satisfy the stated complete-process interface; that physical accuracy is assumed, not established by our fixtures.

The optional private Pauli twirl is of the entire ideal averaged q-input/q-output channel. It converts its global Bell loss into half-diamond distance only after averaging the secret frame. The physical imperfect framed channel need not itself be Pauli; its separate complete-norm error is transferred by the triangle inequality. There is no untwirled or key-conditioned dimension-free diamond claim.

## 7 Independent evidence and limits

The source-disabled exact check enumerates 774 Born terms for nine correlated 1–3-qubit snapshot cases; 1,152 fine and 288 coarse input/output Born terms for two distinct conditional two-logical channels; eight conditional gradients; nine local/disjoint contrast cases; eight noncommuting-gauge excess/sign cases including tiny eigenweights; six finite clipping/repair cases; six deterministic pathwise OGD cases; and 36 complete integer confidence/source/randomness budgets. The same-output covariance witness is 1. These are finite law and arithmetic checks, not sampled acquisition, model verification or an executed generic diagonalization routine.

The first check run reached its final JSON serialization after all assertions passed, then stopped because a SymPy Boolean metadata value was not JSON serializable. Its original script is preserved. Converting only that metadata value to Python bool produced the passing result; no mathematical assertion or author source changed. The history file records this reporting-only repair. The passing pre-clarification script/result are also preserved; rebinding the final source changes only its hash guard and reported source hash, not the mathematical checks.

Three stable statistics receipts are imported only for their specified components: rational Jacobi processing, colored receiver algebra, and the private-terminal channel principle. Their 31 direct manifest entries were reverified. The current receipt does not import any forthcoming main receipt, avoiding a dependency cycle. The conventional same-information learner receives the same records, finite processing and controls; no superiority, practical small budget, hardware implementation or generic unknown-noise recovery is claimed.
