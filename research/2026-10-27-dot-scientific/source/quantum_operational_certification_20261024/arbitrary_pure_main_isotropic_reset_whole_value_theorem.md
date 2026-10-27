# Whole arbitrary-reference pure-main / isotropic-reset VALUE

26 October2026. Governing proof FROZEN, pending independent whole-chain receipt. Root proposed the e2 scalar clock; this worker independently acquired the arbitrary-main source formula, branch/measure/source limits, and exact corroborating source checks. No unrestricted mixed-input or charged-decoder theorem is claimed.

## Statement and exact scope

Let R be any finite-dimensional reference, let psi belong to C3 tensor R, and let Y>=0 on R. Put
X=|psi><psi|+I3 tensor Y,
N=W3 tensor id, W3(A)=(Tr(A)I3-A^T)/2,
f(A)=Tr A log A (0log0=0),
Delta(X)=f(X)+f(Tr_phys X)-2f(NX)-Tr(X)log3.

Then Delta(X)>=0.

The main vector is arbitrary, including deficient Schmidt rank; the reset may be arbitrary coherent PSD noise of any finite rank and reference dimension. This is a theorem only for the displayed pure-main/isotropic-reset source class, not arbitrary mixed bipartite X. A maximally entangled isometric main gives the actual TP isometry-plus-replacer channel after homogeneous normalization. A general nonmaximal main is not silently called TP. No original-main GLS payment, recovery rate, equality classification, or entropy monotonicity under a generic channel is asserted here.

The mathematical dependencies are the separately exact scalar pair-score inequality and the earlier pure-success physical-CQ VALUE theorem, not the new whole aligned-Schur or clean-kernel families. The proof is therefore not circular with those dependent coverage results.

## 1. Exact arbitrary-main entropy integral

Write psi=sum_i |i> tensor v_i and Psi=[v_0,v_1,v_2]:C3->R. Define
K(s)=Psi*(Y+sI)^(-1)Psi, H_infinity=Psi*Psi.
The acquired scalar spectral kernel is

F(K)=2 logdet[I+(TrK I-K)/2]-3 logdet(I+K/3)-log(1+TrK),
Delta(X)=integral_0^infinity F(K(s)) ds.             (1)

Here is a direct source derivation, including the main-dependent cutoff constant. Relative to the reset-only source, the input determinant ratio is1+TrK(s). The reference marginal is3Y+Psi Psi*, so its ratio is det(I+K(s/3)/3). The three antisymmetric WH Kraus vectors of psi have reset-resolvent Gram
[TrK(s) I-K(s)^T]/2;
thus the output ratio is det(I+[TrK I-K^T]/2). The transpose has no effect on this determinant, and is not omitted in acquiring the actual complex source.

For any finite-rank perturbation with added trace m=Tr H_infinity, the elementary cutoff entropy identity is
f(A)-f(A0)=lim_R [m(logR+1)-integral_0^R log(det(A+s)/det(A0+s))ds].
Correction recorded before independent promotion: an initial draft omitted the +m in this single-perturbation identity. The correct +m is essential for the standalone identity. Apply it to input, reference and output; BOTH the logarithmic m logR terms and the constant +m terms cancel with coefficients1+1-2. Rescaling the reference integration s=3t produces the extra tail
3 integral_(R/3)^R logdet(I+K(t)/3)dt ->m log3,
which cancels the explicit -m log3 in Delta. The reset-only source itself has zero deficit. This proves (1), including the homogeneous constants, for arbitrary Psi. Singular Y is harmless: finite-dimensional logarithmic endpoints are integrable, or can be acquired by Y+epsilon I and the same explicit integral bounds below.

## 2. Universal pair compensation

For positive eigenvalues(x,y,k), write T=x+y,P=xy and f_pair(T,P,k)=F(x,y,k). The exact derivatives are
f_P=2/[P+(2+k)T+(2+k)²]-3/[P+3T+9],
f_T=2/(2+T)+2(2+k)/[P+(2+k)T+(2+k)²]
    -9/[P+3T+9]-1/(1+T+k).
The separately certified inequality is

f_T-k f_P>0.                                      (2)

For completeness, multiply by the positive denominator(2+T)[P+(2+k)T+(2+k)²][P+3T+9](1+T+k). Its numerator equals
10(T²/4-P)+3k²T³
+[4Pk+6k³+18(k-1/6)²+9]T²+[(P-1)²+23]T
+[6Pk²+18Pk+3k⁴+24k³+36k²+6k]T
+2P²k+2Pk³+14Pk²+22Pk+6k⁴+30k³+30k²+24k.
It is strictly positive because0<=P<=T²/4 and T>0. The exact identity is checked in `aligned_rank_one_schur_pair_score_certificate.py`; it extends to zero active eigenvalues whenever the displayed denominators remain positive.

## 3. Full e2-balanced spectral lower bound

Let E=e2(K) be the sum of the three pairwise eigenvalue products. Balance any pair(x,y) while holding its spectator k and(k+x)(k+y) fixed. This preserves E=P+kT. Decreasing T to its equal-pair endpoint has dP/dT=-k, so(2) strictly lowers F unless the pair was already equal. Both changed eigenvalues stay between their original minimum and maximum.

Repeatedly balance the largest and smallest eigenvalues. For rank at least2, the first step makes all three positive if needed. Thereafter the eigenvalues stay in a fixed positive compact interval, and their sum decreases, bounded below by sqrt(3E). If their spread stayed bounded away from zero along any subsequence, continuity of the strictly positive trace drop on that compact set would force an impossible unbounded cumulative decrease. Hence they converge to the equal vector rI with
r=sqrt(E/3).
Continuity gives the universal pointwise comparison

F(K)>=F(sqrt(e2(K)/3) I3).                          (3)

It is strict for nonzero nonscalar K of rank at least2. For rank1, E0 and
F(x,0,0)=4log(1+x/2)-3log(1+x/3)-log(1+x),
whose derivative is2x/[(x+1)(x+2)(x+3)]>0. Thus F(K)>0 for any nonzero rank-one K, and(3) remains valid with r0. Rank0 is trivial. No Schur-convexity at fixed trace or generic matrix concavity is assumed.

## 4. The e2 mean of an actual inverse clock is a scalar Stieltjes clock

Assume Psi has rank r>=2 and restrict matrices to the fixed support of H_infinity, where H_infinity>0. The actual finite reset spectral decomposition gives
K(z)=sum_j M_j/(z+lambda_j), M_j>=0, sum M_j=H_infinity,
H(z)=zK(z)=sum_j M_j z/(z+lambda_j), 0<=lambda_j<=L=||Y||.
The nullspace removed in this restriction is common to every M_j, so no source information is lost.

For Imz>0,
Im H(z)=(Imz)sum_(lambda_j>0)lambda_j M_j/|z+lambda_j|²>=0.
If an eigenvector of H has a real eigenvalue, it lies in the kernel of this imaginary part, so every positive-lambda effect annihilates it and H acts on it as H_infinity. That real eigenvalue is therefore positive. In particular H is invertible and has no nonpositive-real eigenvalue in the upper half-plane.

For r3 define

g(z)=exp{[Tr Log H(z)+Log Tr(H(z)^(-1))-log3]/2}.       (4)

All logarithms use their analytic principal branches in the indicated half-plane. The inverse has nonpositive imaginary part; unless ImH is zero, Tr H^-1 has strictly negative imaginary part and cannot vanish. If ImH=0, H=H_infinity>0 and its inverse trace is positive. Thus the second logarithm in(4) is also analytic.

More precisely, every scalar z/(z+lambda_j) lies in the sector from0 toarg z. Positivity of the matrix effects puts the numerical range, hence every eigenvalue of H, in that same sector. Let their arguments be theta_i in[0,arg z], a subinterval of[0,pi). The reciprocal eigenvalues lie in a cone of angular width less than pi, so the argument of their sum TrH^-1 lies between -max theta_i and -min theta_i. Consequently the argument in the exponential(4) lies between half the sums of the two smallest and two largest theta_i, hence in[0,arg z] and in particular[0,pi). This proves Im g>=0 globally, not just a formal scalar square-root sign. On positive real s, the identity e2(H)=det(H)TrH^-1 gives

g(s)=sqrt(e2(H(s))/3)>0.

For r2, e2(H) is the determinant on its two-dimensional support. Define instead

g(z)=exp[Tr Log H_support(z)/2]/sqrt3.
The same eigenangle argument gives Im g>=0. No inverse of a singular3x3 matrix is used. In both cases set h(z)=g(z)/z; on positive s this is exactly sqrt(e2(K(s))/3), the scalar in(3).

## 5. Compact positive measure, including every zero endpoint

For real z<-L, each scalar z/(z+lambda_j)>=1, so H(z)>=H_infinity>0. The above branch is real positive and analytic across that interval. All possible zeros, poles and branch cuts of g therefore lie in[-L,0]. The rational e2(H) consists of2x2 minors of a matrix with only simple poles, hence its pole order is at most2; g has at worst integrable square-root singularities or isolated simple poles. At infinity,
g(z)=c+O(1/z), c=sqrt(e2(H_infinity)/3)>0,
h(z)=c/z+O(z^-2).

At0 write H(z)=M0+zA1+O(z²), with A1 positive on ker M0 within the fixed support. If rank M0>=2, g(0)>0 and h has a simple zero-atom pole. If rank M0=1, g(z)=O(sqrt(z)) and h(z)=O(z^-1/2), giving an integrable cut density. If M00, H=zA1+O(z²) with A1>0, so g=O(z) and h remains finite. These exhaust the endpoints; there is no unreceived singular positive-rate limit.

A Cauchy contour around the finite negative cuts and poles now gives

h(s)=integral_[0,L] nu(dt)/(s+t), nu>=0, nu([0,L])=c. (5)

On a cut at-t<0 the density is Im g(-t+i0)/(pi t)>=0. A simple pole of the Pick function g has nonpositive residue, which becomes a nonnegative residue of h after division by-t. The atom at0 is g(0)>=0 when present. The endpoint behavior just established makes all remaining densities locally integrable. Finally the coefficient c/z at infinity fixes the total measure mass. This is a direct finite-source contour receiving, not an appeal to unverified determinant monotonicity or arbitrary operator-mean closure.

If L0, the measure is simply c delta0. The rank-one-main case does not need(4)-(5): its pointwise kernel is already positive by section3.

## 6. Actual finite auxiliary sources and dimension-independent limit

Approximate nu by finite positive atomic measures nu_n of EXACT mass c on[0,L]. For atoms(t_j,m_j), choose a logical vector v_n with entries sqrt(m_j/c) and a bath T_n=diag(t_j). Use three physical reference-label copies of this logical space, with reset
Yaux=I3_label tensor T_n,
and pure main sqrt(c) sum_i |i>_physical tensor |i>_label tensor v_n.
This is an actual finite pure-success physical-CQ source. Its compressed main-resolvent matrix is
Kaux(s)=[sum_j m_j/(s+t_j)] I3=h_n(s)I3.
The earlier theorem `pure_success_arbitrary_cq_reset_bath_collapse_theorem.md` pays its entire homogeneous deficit. Its main mass is3c, generally DIFFERENT from the original Tr H_infinity. No same-main charged comparison or equality of normalized auxiliary/original channels is asserted or needed.

Auxiliary reset trace and dimension can grow, so we pass through the exact integral, not dimension-dependent entropy continuity. Put M=||H_infinity||. Then c<=M and original/auxiliary clocks satisfy0<=K<=MI3/s. Directly from F,
|F(K)|<=16log(1+3M/s),
|F(K)|<=8M²/s².
For the second bound the linear logarithmic terms cancel EXACTLY; the elementary remainder0<=t-log(1+t)<=t²/2 bounds the output, reference and scalar-input pieces by3M²/s²,M²/(2s²),9M²/(2s²). The minimum of the displayed bounds is integrable on(0,infinity), independently of all auxiliary dimensions and traces. Since h_n(s)->h(s) pointwise, dominated convergence gives

integral F(h(s)I3)ds=lim_n Delta(auxiliary_n)>=0.

Combine with(1) and(3) to conclude Delta(X)>=0. Rank0 main is directly the zero-deficit isotropic product. Rank1 was paid pointwise. Rank2 is directly covered by its support branch, although fixed-dimensional pure-main regularization would also receive nonnegativity.

## 7. Executed source and scope checks

`arbitrary_pure_main_e2_clock_source_check.py/.txt` acquires original complex input/reference/WH matrices, the exact F integral and the e2-balanced integral for full and rank-one/two mains in reference dimensions3,4,6, including singular and coherent resets. It also checks the actual matrix-log branch at upper-half-plane points. These replays corroborate the analytic source/branch proof, not replace it.

The earlier exact arbitrary-main same-main charged GLS failure, full-instrument entropy-monotonicity failure, orientation failures and full leaf-matrix convexity counterexample remain valid. The new statement is homogeneous VALUE for one pure main plus isotropic reset only. Neither a decoder on the original source nor a normalized auxiliary comparison is constructed. Arbitrary mixed-main or unrestricted WH3 entropy inequalities remain outside this theorem.
