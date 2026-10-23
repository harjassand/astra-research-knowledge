# Independent challenge: correlated-block compression really gives a code

Author: `/root/correlated_capacity_challenge`, 22 October 2026.

## Scope and verdict

This is a focused review of the load-bearing passage from a **proved negative-drift depth kernel for the exact correlated two-call bath map** to quantum transmission above 3/2 qubits per counted forward call. It does not certify the two-call algebra or the entropy certificate; those are separate obligations being supplied by the owner and the algebra/entropy contributors.

**Conditional verdict: the coding implication is valid.** It uses the actual unchanged device over all 2m calls and the complete inherited finite-environment code construction, including expurgation, auxiliary normalization and its polar repair. The tensor factors in the spectral type construction are two-call input blocks, not independent physical memory channels. No bath reset, replacement initialization, postselection or inaccessible purification is introduced. In fact, radial closure need only hold along the auxiliary radial bath average used to choose the code. Full dual closure on arbitrary coherent initial baths is stronger than necessary.

Actual source read: `inherited_cycle2/Astra_Amplification_Cycle2_PRO1_20261022/COHERENT_CAPACITY_FLOOR.tex`, the finite-error-set code, joint averaged-overflow lemma, its proof and counterexamples, and the pointwise extension to every fixed normal initializer. The following proof gives the new receiving use of that inherited operation.

## Required exact hypotheses

Let the input block be a fixed density `varrho` on C^9, independent of the horizon. Let `Psi` be the bath channel obtained by putting this density through two successive copies of the actual fixed V, with both external outputs retained in the physical process and traced only in the bath average. Let `W_(2m)` be the complete unchanged sequential isometry over 2m calls.

The bath is the same two-seed binary Fock space, with depth L, level dimension 2^(ell+1), and coordinate cutoff

`P_a = 1_[0,a](L)`, `r_a = rank P_a = 2(2^(a+1)-1) < 2^(a+2)`.

For the theorem below it is enough that:

1. Every radial initial density remains radial under Psi, with an exact depth Markov kernel.
2. Depth jumps have magnitude at most 2.
3. At every depth ell >= 2, the increment law is the same fixed law p_j, j in {-2,-1,0,1,2}, and its mean is `sum j p_j = -mu < 0`.
4. The kernel at depths 0 and 1 is the actual root-retaining kernel. Finite propagation gives L' <= 3 there. It need not be a reflected copy of the bulk law.

Neither a cutoff stationary distribution nor a formal negative first moment in an arbitrary evolving coherent state supplies these hypotheses. The exact block-map proof must supply them. The proposed parameter choice is fixed at beta = 1/512, b = beta^2 = 2^-18, delta = b^2/512, q = 1/2-delta, x=q^2, y=q(1-q)/2, z=(1-q)^2/4 and c=-b/128. If the independently derived bulk formula is correct, then `mu=(1-b)b^2/128 > 0`. Entropy greater than three is a separate exact finite-dimensional proof obligation.

## Uniform exponential moment on the infinite bath

All exponentials in this subsection are natural. Put

`t = min{1, mu/(4 e^2)}`, `lambda = 1-mu*t/2`, `C = exp(3t)/(1-lambda)`.

The strict positivity of t follows from the fixed negative drift; it never depends on m. Since the jump magnitude is at most two, Taylor's formula gives

`sum_j p_j exp(tj) <= 1-mu*t+2 exp(2t)t^2 <= 1-mu*t/2 = lambda < 1`.

Here the pointwise remainder bound is `exp(tj)-1-tj <= (t^2 j^2/2)exp(2t)`. Also `mu <= 2`, so lambda is positive for the displayed t. For f(ell)=exp(t ell), the actual kernel therefore satisfies

`P f(ell) <= lambda f(ell) + exp(3t) 1_{ell<=1}`.

This is a positive function inequality on the actual infinite depth chain. Iteration, first on nonnegative functions by monotone convergence if desired, gives

`E exp(t L_m) <= lambda^m E exp(t L_0) + C(1-lambda^m)`.

For any radial initial density supported in P_a, in particular the auxiliary `P_a/r_a`,

`E exp(t L_m) <= exp(t a)+C`,

and hence, uniformly in the number of repeated blocks,

`Pr(L_m > h) <= exp(-th)(exp(ta)+C) <= (1+C)exp[-t(h-a)]`.

No invariant state or mixing theorem is needed. There is no reflecting numerical boundary. Constants may be extremely large because the proposed negative drift is tiny; this is an asymptotic existence result.

For the actual tau_pi the initial exponential moment is finite whenever t<ln 3, with value `(2/3)/(1-exp(t)/3)`. The displayed choice has t <= 1 < ln 3. Thus the actual bath has a uniform exponential moment, and therefore a uniform finite mean depth. Radiality then implies

`S(tau_m) = H(L_m)+1+E L_m <= 1+M+log_2[e(M+1)]`,

where M is any common upper bound for the mean. This establishes bounded bath entropy, not merely bounded mean drift, on the actual initial trajectory. The initial purification F has the unchanged finite entropy S(tau_pi), so `S(E_m F) <= S(E_m)+S(F)=O(1)`. This is an analytic entropy statement; F is not supplied to Alice or Bob.

## Spectral type: within-block entanglement is admissible

Diagonalize the one fixed 9-dimensional density as `varrho=sum_j lambda_j |e_j><e_j|`. The eigenvectors may be coherent or entangled across the two calls. Alice is allowed one block encoder before all forward interactions, so this is not an additional physical operation on the bath.

For each m, partition the spectral product basis into multinomial types. There are at most `(m+1)^9` types. Choose a type with largest probability p_m under varrho^tensor m, and let T_m project onto its span, with dimension D_m. Then

`p_m >= (m+1)^(-9)` and `T_m/D_m <= varrho^tensor m / p_m`.

The latter is an operator inequality because the density is a scalar on the type subspace. It does not require the type projection to be diagonal in the computational qutrit basis.

For completeness, `log_2 D_m/m -> S(varrho)`. If t_m is the empirical eigenvalue distribution of the selected type, the multinomial bound `D_m <= 2^(m H(t_m))` gives

`p_m = D_m product_j lambda_j^(m t_(m,j)) <= 2^[-m D_2(t_m||lambda)]`.

Thus `D_2(t_m||lambda) <= 9 log_2(m+1)/m -> 0`, and Pinsker (or finite-alphabet compactness and strict positivity of relative entropy) gives t_m -> lambda. The lower multinomial bound

`D_m >= (m+1)^(-9) 2^(m H(t_m))`

then proves the entropy-rate limit. Zero eigenvalues can simply be omitted; the proposed density is strictly positive.

Although the bath is correlated with earlier outputs, tracing those outputs shows that the final bath average under the input varrho^tensor m is exactly Psi^m. This uses independence between **input blocks** and the initial bath, not a memoryless-channel assumption. The one actual sequential unitary W_(2m) implements every interaction.

## A quantitative choice satisfying the inherited lemma

Set

`a_m=floor(log_2(m+1))`,

`h_m=a_m+ceil([20 ln(m+1)+ln(1+C)]/t)`,

`r_m=rank P_(a_m)`, `d_m=rank P_(h_m)`.

The auxiliary bath average `P_(a_m)/r_m` is radial. Positivity, spectral type domination and the previous overflow estimate give an average overflow on `T_m tensor P_(a_m)` at most

`epsilon_m = (m+1)^(-11)`.

Indeed the type probability loses at most `(m+1)^9`, while the selected h_m supplies `(m+1)^(-20)/(1+C)`. This is an average over the mathematical code-selection input and bath, not a physical measurement or heralded success probability.

Apply the inherited joint-compression lemma to W_(2m), input A=T_m, initial bath E_0=P_(a_m)E and final bath cutoff P_(h_m). It produces a physical isometric encoder and a deterministic recovery with

`K_m >= ceil(floor(D_m/2)/(r_m d_m)^4)`

and finite-initial-support full-diamond error at most `4 e_m`, where

`e_m = r_m sqrt(2 epsilon_m)+(1-2epsilon_m)^(-1/2)-1`.

Since `r_m < 4(m+1)`, the first term is bounded by `4 sqrt(2)(m+1)^(-9/2)` and the second tends to zero. Also

`log_2(r_m d_m) < a_m+h_m+4 = O(log m)`

for this one fixed channel and fixed t. The constant contains 1/t; no useful finite blocklength or efficient compiler follows. Therefore

`liminf_m log_2 K_m/(2m) >= S(varrho)/2`.

The factor two in the denominator counts both forward qutrit calls in every input block. All decoder syndromes can be retained in a dilation and then traced to define the logical marginal. No final bath-return requirement is imposed or inferred.

## Arbitrary references and actual initializer

The inherited lemma is stronger than average entanglement fidelity. After recovery, the true physical joint isometry on logical tensor E_0 differs by at most 2e_m in operator norm from `I_logical tensor Z_0`, with Z_0 an isometry. This statement includes arbitrary references. It gives full diamond error 4e_m, half-diamond error 2e_m.

The derivation needs all initial and final bath matrix indices. The auxiliary normalization J makes the projected Kraus family CPTP solely for code selection; the physical encoder is C, not JC. The polar replacement of Z by Z_0 is required because exact factorization of the normalized projected comparison map alone does not make Z isometric.

For every one fixed normal initializer tau, let `q_m=Tr(P_(a_m)tau)`. Then q_m -> 1. Its normalized projected comparison state has trace distance at most `2 sqrt(1-q_m)` from tau. The same physical process is CPTP in that initial state, so

`||Lambda_(m,tau)-id||_diamond <= min{2, 4e_m+2sqrt(1-q_m)} -> 0`.

The half-diamond bound is `2e_m+sqrt(1-q_m)`. The code sequence is independent of tau. This is pointwise in each fixed normal initializer, not convergence uniform over the set of all normal states at each horizon. In particular it applies to the unchanged actual tau_pi, without preparing its cutoff or a different stationary bath. The initial projection is taken only in a comparison proof outside the type-domination bound, so no uncontrolled actual tail is multiplied by 1/p_m.

If codes are required at odd forward blocklengths, append one data-independent forward input after the 2m-call code and discard that final output. A later interaction with the bath cannot alter Bob's earlier reduced output. The extra call counts and has no asymptotic effect.

## Decisive counterexamples to weakened interfaces

* An average overflow alone is not an arbitrary-reference error bound. On a D-dimensional input, the projector onto one basis vector has average 1/D and worst-case probability one. The inherited spectral expurgation is indispensable.
* Bath-average overflow alone is not uniform over coherent bath inputs. For a maximally entangled rank-one projection X on C^r tensor C^r, `(1/r)Tr_E X=I/r^2` but `||X||=1`. The inherited factor r^2 before taking the square root is necessary. The chosen epsilon_m pays for it.
* Positive input entropy does not imply capacity. The proof needs the exact all-time overflow for the unchanged block map, a spectral type domination, and the actual error-correcting code. A finite dark vector, a finite cutoff stationary state or a larger Kraus rank supplies none of these.
* A bath entropy estimate is not automatically an arbitrary-rank compression estimate in infinite dimension. This proof directly uses the exponential coordinate tail and finite level dimensions. It therefore avoids the small-mass/huge-entropy loophole exhibited in the inherited Cycle3 source.

## Remaining independent obligations and status

Before the owner claims strict gain, the exact root-retaining block map must prove radial invariance and the stated depth kernel; every transition probability and boundary must be valid, and the selected parameters must make the bulk drift negative. The finite density must have entropy strictly greater than three with a genuine analytic or certified arithmetic proof. These are not established by the conditional coding argument itself.

If those obligations pass, then the strict gain is a mathematically substantive change to the live capacity boundary: it uses repeated temporally correlated input blocks, which lie outside the closed single-site iid theorem. It does not change notation in that theorem, replace its optimizer by a weaker control, or presume independent uses of the physical channel. It does not determine the exact capacity, establish feedback equality, optimize the gain, prove efficient realization or claim a historical first.

## Observed resources

This contribution used direct reading of the inherited native LaTeX proof and analytic reconstruction of the new conditional coding argument. No numerical bath cutoff, external hardware, purchase, or external communication was used. No CPU benchmark was performed. The writer has not measured total discovery time, upstream costs or the resources required to compile the nonconstructive codes.

## Final source-specific challenge and acceptance

The owner subsequently supplied the complete `CORRELATED_CAPACITY_GAIN.tex` and `INHERITED_COMPRESSION.tex`, together with `contributions/two_call_algebra.md` and `contributions/two_call_entropy.md`. I read the actual native sources, including the complete moment, complementary-information, type, code-rate and initializer-extension proofs. This final review supersedes the conditional status above for those supplied obligations; it does not claim external certification or historical priority.

**Internal acceptance:** no load-bearing gap was found in the capacity implication as written. The exact algebra and entropy contributions now supply the hypotheses that were conditional in the first part of this review. The owner’s actual constants differ from the convenient constants used above and are valid:

* The fixed candidate has `kappa=(1-b)b^2/128 > 0` for every fixed `0<b<1`. With `t=kappa/32`, bounded jumps give `E exp(tJ) <= 1-kappa*t+16t^2 = 1-kappa^2/64`. The inequalities `e^2<8`, `0<kappa<=1/128` and `0<t<1` justify the remainder bound. Its finite boundary contribution is bounded by `exp(3t)`, producing `C0=64 exp(3t)/kappa^2`. This is a true half-line estimate, not a finite-chain computation or an exponentiation of an operator-order claim.
* The supplied block-map source establishes the stronger dual identity on all bounded functions of depth, for every normal bath density. Extending it to nonnegative unbounded `exp(tL)` by monotone convergence is legitimate. Finite propagation preserves each finite initial exponential moment at every finite horizon. The actual initial moment is finite since `t<ln 3`; no different invariant state is physically substituted.
* For the actual tau_pi trajectory, radiality is separately proved. The entropy formula `S(tau_m)=H(L_m)+1+E L_m` and the geometric maximum-entropy bound give a horizon-independent finite entropy bound. Subadditivity with the unchanged analytic purifier F bounds `S(E_(2m)F)`. The lower squeeze `mS(varrho)-2S(tau_m)<=Ic` and upper squeeze `Ic<=mS(varrho)` are correct and retain all output correlations. F is never treated as a controllable resource or as a return obligation.
* The maximum-probability spectral type proof does not rely on a memoryless physical channel or on a computationally diagonal two-call input. Its polynomial probability and the relative-entropy compactness argument yield `log2 D_m/m -> S(varrho)`. The operator domination transfers through the one actual sequential W_(2m). The bath average under independent input pairs is the exact repeated block bath map; independence of physical channel uses is neither used nor concluded.
* In the owner’s actual cutoffs, `h_m-a_m` is the ceiling of `[25 ln(m+1)+ln(1+C0)]/t`. After the at-most `(m+1)^9` spectral-type loss, the average overflow is at most `(m+1)^(-16)`. Since `r_m<4(m+1)`, the error contribution `r_m sqrt(2 epsilon_m)` is at most `4sqrt(2)(m+1)^(-7)`. Both the normalizer term and this contribution vanish. For each fixed beta, `log2(r_m d_m)=O(log m)`, despite the very large fixed coefficient. This suffices for the claimed rate with all 2m calls counted.
* The appended inherited proof retains the complete initial/final error-index family, its `r^2` positive-block bound, the auxiliary CPTP normalizer, the physical isometric encoder C and the isometric polar repair. Its full-diamond bound is therefore justified rather than inferred from average entanglement fidelity. The finite-support-to-normal-state comparison is applied to the actual normalized physical process outside type domination. The stated quantifier is correctly one code sequence for each fixed beta, working pointwise for every one fixed normal initializer; it is not an initializer-uniform convergence claim.
* The entropy certificate in the supplied contribution is analytic for all `0<b<=1`, not just a floating-point observation at the selected small angle. It proves `S(varrho)-3 >= (569/262144)b^2 > b^2/512`. Combining with the actual code theorem gives `Q>=S(varrho)/2>3/2+beta^4/1024` for every fixed `0<beta<1`. The endpoint beta=0 lacks negative drift and is correctly covered by the inherited result; beta=1 is separately the identity channel. Diverging constants as beta approaches either endpoint do not invalidate a theorem that fixes beta before taking the coding limit.

One minor cross-reference repair was sent to the owner: the optional Cesaro-invariant-state paragraph originally attributed tightness of the actual tau_pi orbit to equation (24), whose displayed hypothesis is a finite-support initializer. For the actual untruncated state the direct bound is `Tr[(I-P_h)tau_m] <= M_* exp(-th)`, from equations (23) and (26). Citing those equations, rather than (24), makes the premise explicit. The uniform moment bound already proves the statement, so this is not a theorem gap and is unnecessary to the coding conclusion.

The mathematical result resolves strict gain within the exact model. It does not determine the capacity value, establish feedback equality, promise bath return, quantify an efficient code compiler or establish useful finite physical performance. This review found no hidden reset, access to the bath or purifier, success-only credit, change of initializer, or horizon-dependent angle.

### Additional signed-coherence counterexample, equation (38)

The owner added a same-device counterexample after the main source review. I read and checked the new paragraph and equation (38), keeping the actual initializer and replacing only `c=-b/128` by `c=+b/128`. The eigenvalues `y+c` and `y-c` are exchanged, so the input entropy is unchanged. The exact bulk drift becomes `3kappa`, since `a(4delta+2bc)=3ab^2/128`; both root corrections are positive. Finite initial mean and finite propagation justify telescoping `Delta E L >= 3kappa m`.

The charge and entropy coefficients in (38) are correct. Global charge conservation over the whole 2m-call unitary gives `sum_j q'_j=2mq+Delta E L`, even though the input ports inside each pair are correlated. Output subadditivity therefore gives `S(B^(2m))<=m(3+2delta)-Delta E L`. Combining with total entropy `m(3+epsilon)+S(tau_pi)` yields

`S(E_(2m))>=S(tau_pi)+m(epsilon-2delta+3kappa)`.

The purifier F remains fixed with entropy S(tau_pi), so `S(EF)>=S(E)-S(F)` and consequently

`Ic<=2S(B^(2m))-mS(varrho)<=m(3-epsilon+4delta-6kappa)`.

For the stated interval `0<beta<=1/8`, both inequalities `3kappa>2delta` and `6kappa>4delta` hold (each is equivalent to `a>1/6`, which this interval satisfies). Thus the bath and purified complement have extensive entropy, and the per-call coherent-information upper bound is strictly below 3/2. This is a valid counterexample to dropping the sign-sensitive exact temporal interference from the receiving interface. It does not become a capacity converse for arbitrary inputs. The newly added separable-density decomposition is a distinct algebra obligation reviewed by the algebra contributor, not by this paragraph.
