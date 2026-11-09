ROOT MATHEMATICAL CONSTRUCTION: A FINITE-BIT TILTED-DIRICHLET OBSERVATION COMPILER
10 November 2026 Brisbane. A complete stationary finite-observation algorithm at its stated mathematical scope. No new transition sampler, physical kinetic realization, uniform mixing theorem or historical novelty claim.

FULL CONTRACT OF THIS CONSTRUCTION. Input is K>=2, ordinary binary rational alpha_i>0 and arbitrary rational selection coefficients s_i, an integer r>=0 and rational0<epsilon<1. Set sigma_i=s_i-min_j s_j>=0 and s=max_i sigma_i. Let D_alpha be the Dirichlet law and
 mu(dx)=Z^-1 exp(sum_i sigma_i*x_i) D_alpha(dx)
on the simplex. The target is the ENTIRE ordered r-label observation law obtained by first drawing ONE X~mu and then r conditionally independent categorical draws with parameter X. Output an ordered row on[K] whose whole-law TV from that target is <=epsilon. The algorithm uses rational/integer arithmetic and fair bits only. It needs no continuous-real output, gamma or Dirichlet sampler, probability/integration oracle, unknown-law advice or sample oracle. This target is a known-parameter mixture-of-products, not fixed-unknown-Q product sampling as in P1.

The compiler has polynomial expected local bit work and memory in K, complete binary input length L, r and NUMERICAL ceil(s). Dependence on alpha is through its bit encoding, not a mandatory inverse-alpha physical clock. No deterministic cap on fair-bit rejection is imposed. It does not assert polynomial work in log(s) or a physical population/time acceleration. The target is the known tilted law, which is the genic-selection WF stationary law at positive mutation; no transient or finite-population identity follows.

POSITIVE MIXTURE FROM DIRECT EXPANSION. Put alpha0=sum alpha_i and use rising factorials (a)_k. The exponential Taylor series and Dirichlet monomial integration give
 Z=sum_(n in N^K) [(product_i(alpha_i)_(n_i)*sigma_i^n_i/n_i!)/(alpha0)_(|n|)].
Let g_i(k)=(alpha_i)_k*sigma_i^k/k!,
 F_j(m)=sum_(n1+...+nj=m) product_(i<=j)g_i(n_i),
 T_m=F_K(m)/(alpha0)_m.
A latent degree m has weight T_m; conditional on m, a vector n has weight product_i g_i(n_i) on |n|=m; conditional on n, X~Dir(alpha+n). This is the established positive-mixture representation, also obtained directly from the displayed expansion. Its scientific source is attributed below rather than claimed as a new Astra representation.

EXPLICIT UNIFORM TRUNCATION. Choose k as the least integer with 2^-k<=epsilon/4, using rational comparisons. If s=0 take M=0. Otherwise set M=ceil(8*(s+k+1)). Since sigma dot x<=s on the simplex, the omitted unnormalised Taylor mass is at most sum_(j>M)s^j/j!. The full normaliser Z>=1. For M+1>=8s, exponential Markov/Chernoff gives
 sum_(j>M)s^j/j! <= exp(s)*(e*s/(M+1))^(M+1)
 <=exp(s-(M+1))<=epsilon/4.
Here e^2<8, and k>=log(4/epsilon); the algorithm does not evaluate e or a real logarithm. The latent tail probability is no larger. Renormalising the latent law on |n|<=M changes its TV by exactly that tail; applying a common Dirichlet/observation kernel cannot increase TV. Therefore this SINGLE truncation controls the entire r-label law for EVERY r, not merely separate marginals or moments. M is O(s+log(1/epsilon)+1), independent of r and of tiny alpha_i.

COMPUTING THE FINITE MIXTURE. Compute F_0(0)=1,F_0(m>0)=0 and
 F_j(m)=sum_(u=0)^m F_(j-1)(m-u)*g_j(u), 0<=m<=M.
This takes O(K*(M+1)^2) arithmetic operations and avoids enumerating (M+1)^K count vectors. Select m in{0,...,M} with weights T_m. Then for j=K,...,1 and current remaining degree v, select n_j=u with weights g_j(u)*F_(j-1)(v-u) and subtract u. Zero weights are skipped; a selected state always has positive normalisation. These exact conditional selections produce the whole truncated latent law.

REMOVING CONTINUOUS SAMPLING EXACTLY. Given n, set b_i=alpha_i+n_i. Simulate the r observations by a Polya urn: after l observations with label counts c_i, choose next label i with probability
 (b_i+c_i)/(alpha0+m+l).
The joint probability of any ordered row z is product_i(b_i)_(count_i(z))/(alpha0+m)_r, which is exactly the Dirichlet integral of product_j X_(z_j). Thus no gamma/Dirichlet numerical approximation is used. The final row has the exact conditional law for the selected n; all approximation is the proved latent tail truncation. Counts alone may be returned by projection if that is the declared output.

EXPLICIT INTEGER REALISATION AND BIT LENGTHS. Write alpha_i=A_i/B_i>0 and sigma_i=C_i/D_i>=0 in ordinary positive-denominator integers. For 0<=u<=M, choose
 H_i=(B_i*D_i)^M*M!,
 h_i(u)=H_i*g_i(u)
       =[product_(l=0)^(u-1)(A_i+B_i*l)]*C_i^u*(B_i*D_i)^(M-u)*(M!/u!).
All h_i(u) are nonnegative integers, including sigma_i=0 with h_i(0)=H_i and h_i(u>0)=0. Compute integer prefix convolutions
 V_0(0)=1, V_j(m)=sum_(u<=m)V_(j-1)(m-u)*h_j(u).
Then V_j(m)=(product_(i<=j)H_i)*F_j(m). The backtracking weights h_j(u)*V_(j-1)(v-u) are integers with the correct probabilities.
Let B0=product_i B_i and A0=sum_i A_i*(B0/B_i). To sample total m, use the integer weights
 W_m=V_K(m)*B0^m*product_(l=m)^(M-1)(A0+B0*l).
They differ from T_m by the SAME positive factor (product_i H_i)*product_(l=0)^(M-1)(A0+B0*l). In particular W_0>0. No unknown normaliser is evaluated. The urn uses integer weights A_i*(B0/B_i)+B0*(n_i+c_i), with known total A0+B0*(m+l).

If L is the complete input bit length, an upper bound Bstar=C*(M+1)*(L+K*log2(M+r+2)+K+1) on every integer bit length follows by summing factor lengths in h_i, bounding the number of summands in V_j(m) by (M+1)^K and using the displayed products for W_m. C can be taken as a fixed implementation constant after ordinary schoolbook arithmetic is selected; no input-dependent search or real oracle is hidden. Prefix convolution uses at most K*(M+1)^2 products/additions up to a fixed constant; h_i/products/powers/urn preparation add polynomially many operations. Schoolbook arithmetic costs O(Bstar^2) per product/exact division; additions/comparisons are smaller. Conditional selections cost O(K*(M+1)+K*r) further integer operations. Space is O(K*(M+1)*Bstar+r*log2(K+1)) up to counter factors.
For a positive integer total W of bit length b, generate b fair bits, reject values>=W and repeat. Each round succeeds with probability>1/2 (use zero bits for W=1). This gives an exact uniform integer, expected <2 rounds. Cumulative integer weights then sample exactly. There are K+1+r such selections; their expected fair-bit/arithmetic work is explicitly bounded by the above polynomial. This proves a computably uniform expected finite-bit construction. No deterministic finite fair-bit cap or real-arithmetic exactness is claimed.

WHAT THE CONSTRUCTION DOES NOT PAY. It is a stationary observation-law sampler, not a mixing certificate for a physical chain or the WF transition at a specified t. It does not produce a point whose discrete distribution is TV-close to an unrounded continuous law. Selection s appears numerically in M; the bit-length bound does not make large numeric s free. Time-varying selection, diploid selection, zero-mutation absorbing components, likelihood normalisation over arbitrary observed paths and finite-population transitions are not included. The Polya urn creates the declared mixture-of-products, not conditionally exact unknown-law IID samples. It cannot be substituted for P1's actual sample-only original-row task or P3's same-species/same-state-graph physical kinetic realization.

SOURCE AND COMPOSITION BINDINGS. The tilted-Dirichlet/positive-degree mixture and stationary truncation are existing mathematics: Sant-Jenkins-Ruggiero https://arxiv.org/pdf/2611.08623v1, modelSection2 and Section4.3/Lemma4.3/Proposition4.4/Algorithm2 actually read. The direct expansion above reconstructs the required law and a maximum-selection tail bound; the new scope is the complete known-rational finite-observation integer/urn compiler with paid bit resources, not a priority claim for their representation. ROOT_DIRICHLET_FIBRE_COUPLING_AND_OBSERVATION_CONTRACT_20261110.txt7670/c1dac0b17638bd6f97c5ec1318486319137330e78191ec863fde5940f885b639 supplies the earlier observation-kernel contracts and deterministic-grid counterexample; it did not already provide this finite compiler. All known/unknown source/access/transfer/resource holds remain. No new scientist, external oracle, software installation, resource probe, physical experiment, source recovery or additional recurring task is requested.
