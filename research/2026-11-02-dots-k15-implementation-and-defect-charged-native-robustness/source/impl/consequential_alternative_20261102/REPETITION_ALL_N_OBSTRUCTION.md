# An all-length obstruction for the conventional repetition comparator

Scope: equal mixture of the two repetition codewords |0>^n and |1>^n (equivalently the maximally mixed logical state of the GHZ± code basis), including any global Clifford-axis orientation. This is NOT an obstruction to arbitrary symmetric rank-two inputs, unequal logical mixtures, all codes, or the underlying bosonic channel. All flags are retained, with no postselection.

## Exact finite-flag formula

Write each conditional Pauli channel in [I,X,Y,Z] order as p_f, with independent receiver flag probability w_f. For computational Z-oriented repetition, define

 r_f0=p_I+p_Z, r_f1=p_X+p_Y,
 t_f0=(p_I-p_Z)/r_f0, t_f1=(p_X-p_Y)/r_f1,
 mu_fx=w_f r_fx, ell_fx=log(r_fx/r_f,1-x).

Draw n independent categories c=(f,x) from mu. Let T=product t_c and L=sum ell_c. Then the exact block coherent information is

 I_n = A_n - B_n,
 A_n = E[1-h2((1+T)/2)],
 B_n = E[h2(logistic(L))].

The finite sums are evaluated by multinomial count enumeration in flagged_repetition.py. A completely independent full-density-matrix calculation for n=1,2,3, two arbitrary flags, and logical mixture weights .1,.3,.5 agrees within 3.4e-16; see repetition_density_validation.json. Stable entropy-deficit and LLR evaluations avoid machine-epsilon false positives.

Define

 rho = sum_f w_f[(p_I-p_Z)^2/(p_I+p_Z)+(p_X-p_Y)^2/(p_X+p_Y)],
 b = sum_f w_f h2(p_X+p_Y).

### Theorem

For every integer n>=1,

  I_n <= rho^n - b^n.

Consequently rho<=b rules out strictly positive coherent information for this repetition-code input at EVERY block length.

### Proof

Set a(t)=1-h2((1+t)/2), for 0<=t<=1. Its positive power series is

 a(t)=sum_(k>=1) c_k t^(2k), c_k=1/[ln(2) 2k(2k-1)], sum_k c_k=1.

Since |t_c|<=1, E(t_c^(2k))<=E(t_c^2)=rho. Independence gives

 A_n=sum_k c_k [E(t_c^(2k))]^n <=rho^n.

For the bit ambiguity, B_n is the conditional entropy of a uniform input bit sent n times through the binary-input memoryless symmetric channel W with output (flag, corrupted bit); H(W)=b. For two BMS channels W,V, the standard binary polar entropy identity gives H(W-plus-V)+H(W-minus-V)=H(W)+H(V). This identity can also be obtained directly by the invertible change of variables U1=X1 xor X2, U2=X2 and the chain rule.

The minus channel has posterior reliability magnitude TU, where the individual reliability magnitudes T,U are independent. The positive series implies

 a(tu)>=a(t)a(u).

Indeed, the difference is the nonnegative covariance of the decreasing sequences t^(2k),u^(2k) under the probability weights c_k; explicitly it is half the sum over k,l of c_k c_l(t^(2k)-t^(2l))(u^(2k)-u^(2l)). Averaging therefore yields

 1-H(W-minus-V)>=(1-H(W))(1-H(V)).

Combining this with the chain-rule identity gives H(W-plus-V)>=H(W)H(V). By BMS output symmetry, the plus channel is equivalent to transmitting the same bit through W and V (the known xor bit can be absorbed into an output relabeling). Repeating the inequality proves B_n>=b^n. Subtraction completes the proof.

## A separate explicit eventual-negativity bound

If rho<b fails but rho<beta holds, define

 beta=sum_f 2w_f sqrt(r_f0 r_f1),
 q_fx=w_f sqrt(r_f0 r_f1)/beta,
 V=sum_fx q_fx ell_fx^2.

The tilted distribution q is symmetric under x->1-x, so its LLR has mean zero. Exact change of measure gives

 B_n=beta^n E_q[cosh(L/2) h2(logistic(L))].

Using h2(p)>=4p(1-p), sech(x)>=exp(-|x|), Jensen and Cauchy–Schwarz,

 B_n>=beta^n exp(-sqrt(n V)/2).

Therefore I_n<0 whenever n>V/[4 log(beta/rho)^2]. This is an explicit finite crossover bound, not merely an asymptotic slogan. The stronger rho<b criterion is sufficient for all of the selected high-noise coarse channels, so this crossover is not needed for their certificate.

## Diagnostic margins before exact-cell integration

For entropy-clustered v=.38,r=3,K=3 (256-node quadrature):

| Orientation | rho | b | b-rho |
|---|---:|---:|---:|
| X | .9572934528 | .9622141863 | .0049207335 |
| Y | .9583049959 | .9635641907 | .0052591948 |
| Z | .0517555459 | .0594738304 | .0077182845 |

Every tested v=.38/.4, r=1/2/3, total K=2/3 channel satisfies rho<b in all three orientations. These preliminary quadrature values alone are not certificates. The explicit 64x64 cell-quantizer interval calculation is in certified_repetition_quantizers.json and certify_repetition_quantizer.py.

## Resource and interpretation boundaries

The actual finite flag partition is a 64x64 lookup on absolute normalized GKP syndrome coordinates, hence 4096 classical cells and only three output flags. Its likelihoods are Gaussian-CDF sums, not a quadrature-generated artificial channel. Numerical integration subdivisions are certificate work, NOT extra receiver cells. The construction still presumes access to the GKP syndrome; it does not independently implement or price finite-energy GKP preparation and syndrome measurement. The result is a rigorous obstruction for the specified conventional input family, not a claim that the channel is antidegradable. The parent's separate PSD test found evidence against antidegradability; that is consistent with this restricted obstruction.
