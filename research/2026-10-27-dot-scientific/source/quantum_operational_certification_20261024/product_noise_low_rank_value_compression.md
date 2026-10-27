# Negative-value reference compression for low-rank perturbations of product noise

2026-10-25. Root construction; independent core check supplied by SIC worker, final receipt requested. Structured actual-value theorem, NOT an unrestricted WH3 dimension bound and NOT universal positivity of an individual top anchor.

Let N=W3 tensor id and E=I3/3 tensor Tr_phys. Set
Delta(A)=Tr A log A+Tr EA log EA-2Tr NA log NA.
Consider a normalized actual source
A=Y+X, Y=H tensor tau, X=UU*, rankX=k>=1,
H,tau>=0, TrH=1, TrA=1.
Zero product noise is the immediate rank-k source case and can be handled by its reference support of dimension<=3k. All channels below act only physically.

## Theorem

If Delta(A)<=-epsilon,0<epsilon<=1, another source of the SAME product-noise-plus-rank-k form exists with normalized deficit<=-epsilon/2 and reference dimension at most3k(floor(K/2)+1). A reference compression followed by normalization constructs it; no arbitrary reference-discard monotonicity is asserted.

Define the integer ell=1+ceil(log2(1024k/epsilon)),
eta=epsilon/(1024k ell), R=96/epsilon,
delta=epsilon/(256kR).
Any uniform degree-K resolvent approximation with error<=delta on[0,1] for every s>=eta suffices. One explicit choice satisfies
K+1>=eta^(-1/2)log(2/(eta delta)).
Thus reference dimension is O(k^(3/2)epsilon^(-1/2)log^(3/2)(k/epsilon)). Constants are conservative; this is not an economical numerical or experimental claim.

## 1. Paid product baseline and exact finite-rank perturbation identity

Product structure gives Delta(Y)=Trtau*Delta(H), since every log(tau) term cancels. The acquired reference-dimension-one theorem gives Delta(H)>=0. Therefore compressing tau to PtauP can only DECREASE this baseline.

For j=I,N,E write Y_j=Phi_j(Y)=H_j tensor tau and X_j=Phi_j(X)=U_jU_j*. Choose the fixed physical Kraus factors; U_j has at most k,3k,9k columns respectively, and every reference component lies in the span of the original3k reference components of U. All TrX_j=p=TrX<=1 and ||Y_j||<=1.

The matrix determinant lemma plus the trace-cancelled entropy integral gives
Delta(A)=Delta(Y)+integral_0^infinity [2d_N(s)-d_I(s)-d_E(s)]ds,
d_j(s)=logdet(I+U_j*(Y_j+sI)^(-1)U_j).
Linear trace terms cancel because the channels preserve trace. Singular Y and X cause no problem at s>0; the estimates below justify both endpoints.

## 2. Uniform tails

Near zero,0<=d_j(s)<=r_j log(1+1/s), r_j<=k,3k,9k. Hence the absolute integrand is at most16k log(1+1/s). For original and compressed sources together, the low interval costs at most
32k eta[1+log(1+1/eta)].

For large s, with M_j=U_j*(Y_j+sI)^(-1)U_j,
|TrM_j-p/s|<=p||Y_j||/s²<=1/s²,
0<=TrM_j-logdet(I+M_j)<=Tr(M_j²)/2<=p²/(2s²).
Thus |d_j-p/s|<=3/(2s²). Leading terms2p/s-p/s-p/s cancel, so the integrand is bounded by6/s². The two-source high tail is at most12/R. These bounds do not grow with the original auxiliary dimension.

## 3. Actual product-reference Krylov subspace

Write the3k physical-coordinate reference vectors of U as u_l. Let m=floor(K/2) and
S=span{tau^j u_l:0<=j<=m,1<=l<=3k}.
Then dimS<=3k(m+1). Let P project onto S and define
Y'=H tensor(PtauP), X'=X on C3 tensor S, A'=Y'+X'.
All source positivity and physical-channel identities are preserved. TrX'=p exactly, while TrY'<=TrY.

Moments <u_l,tau^n u_q> through n=2m+1 are preserved by the compressed tau: split even powers across an inner product; odd powers insert one middle compressed operator between vectors in S. Since Y_j^n=H_j^n tensor tau^n, this preserves ALL needed matrix polynomial moments for U_j, even though the channels have different physical Kraus factors. No extra reference seeds are needed.

For a scalar polynomial approximant with error delta, original and compressed weighted resolvent Grams differ by at most2delta in norm, since ||U_j||²<=p<=1. Positive logdet is trace-norm Lipschitz with constant1 on I+PSD. Therefore a conservative middle-integrand discrepancy is at most32kdelta, costing32kRdelta. (The Loewner bound by2delta U_j*U_j permits a sharper trace-dependent estimate, but is not needed.)

## 4. Actual negative VALUE receiving

The favorable baseline and paid integral errors give
Delta(A')<=Delta(A)+32k eta[1+log(1+1/eta)]+12/R+32kRdelta.
For T=1024k/epsilon and ell>=1+logT,
1+log(1+T ell)<=ell+logell+log2<=2ell.
Thus the chosen low term is<=epsilon/16; the tail and middle terms are each epsilon/8. Total error<=5epsilon/16<epsilon/2.

The compressed trace lies in(0,1], because a negative source must have p>0 and X is retained. Homogeneous Delta(A') is negative; dividing by its smaller trace can only strengthen the negative margin. This is a counterexample-preserving VALUE theorem in the stated structured family, not an anchor witness or a positivity proof.

## 5. Obtainable uniform resolvent polynomial

For r(s)=(sqrt(s+1)-sqrt(s))²,
1/(x+s)=[1/sqrt(s(s+1))][1+2 sum_(n>=1)(-r(s))^n T_n(2x-1)].
The degree-K tail is at most2r(s)^(K+1)/s. For0<eta<=1 and s>=eta,
r(s)<=exp(-sqrt(eta)); this follows from r(eta)=exp[-2asinh(sqrteta)] and2asinh(x)>=x on[0,1].
The displayed degree therefore gives error<=delta uniformly. Rational outward choices of eta and integer degree are obtainable; for example an integer binary-log upper bound and an integer upper bound on eta^(-1/2) give a fully finite prescription. The asymptotic degree follows from the explicit parameters above.

## Limits

General high-rank sources need not be bounded-rank perturbations of product noise. The rank k is a substantive input resource; it is not silently bounded by physical dimension. No unrestricted squashed-entanglement dimension theorem, general entropy closure, or practical runtime guarantee follows. The proof suggests a reusable principle: stable nonnegative product baselines plus finite-rank entropy perturbations admit paid finite-memory value witnesses.
