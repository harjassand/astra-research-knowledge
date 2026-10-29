# A direct finite certificate for definite free linear containment

30 October 2026. Root construction contributing to C's general Fisher-unit-
ball synthesis. This is standard free linear Farkas/CP machinery with a
self-contained proof, not a historical novelty claim. It does not assume a
bounded source domain. C independently invented the Fisher reformulation;
the following duality proof and its consequence were developed by root.
Substantive independent challenge is pending.

Let A(x)=A0+sum_(j=1)^g Aj xj be an a-by-a Hermitian linear pencil with
A0>0, and let B(x)=B0+sum Bj xj be a b-by-b Hermitian pencil. Free variables
xj range over Hermitian matrices of ANY finite size, evaluated by tensor
products. The following are equivalent:

 (i) A(X)>=0 implies B(X)>=0 at every finite matrix size.
 (ii) There is a completely positive map Phi:M_a(C)->M_b(C) and R>=0 with
      B0=R+Phi(A0), Bj=Phi(Aj) for j>=1.

In particular this is a finite SDP with one PSD Choi matrix of order ab,
one PSD residual of order b and affine coefficient equalities. Failure has
a source-feasible matrix witness of size b; it is not merely a hierarchy
with an unknown cutoff. Definite A0 and the residual R are substantive.

## 1. Closedness of the certificate cone

Use the Choi convention J=sum_pq E_pq tensor Phi(E_pq)>=0, so
Phi(A)=Tr_a[(A^T tensor I)J] and TrJ=TrPhi(I). The set of target coefficient
tuples representable by(ii) is a convex cone. It is CLOSED: along a convergent
sequence of target tuples, constant matching gives

 TrR<=TrB0,
 lambda_min(A0) TrJ<=TrPhi(A0)<=TrB0.

Thus both PSD variables are bounded and have convergent subsequences;
their limits retain every coefficient equality and positivity. No bound
on the free variables X, nor trace condition on Aj, is used here.

## 2. Separator produces an actual finite free point

If B is outside this closed cone, finite-dimensional separation supplies
Hermitian Y0,...,Yg with

 ell(B)=sum_j Tr(Yj Bj)<0,
 Y0>=0, W=sum_j Aj^T tensor Yj>=0.

The latter two facts follow by testing the residual and Choi PSD cones.
For sufficiently small epsilon>0 put Y0e=Y0+epsilon I_b. The separating
value remains negative, while

 We=W+epsilon A0^T tensor I_b>0.

Set S=(Y0e^T)^(1/2), Xj=S^-1 Yj^T S^-1. Full transpose of We followed
by congruence with I_a tensor S^-1 gives A(X)>=0. This is an ACTUAL free
point of size b, including complex Hermitian coefficients and variables;
partial transpose alone would not be legitimate.

Let Omega=sum_k e_k tensor e_k and v=(I_b tensor S)Omega. The vectorization
identity Omega^*(C tensor D)Omega=Tr(C^T D) gives

 v^* B(X) v=Tr(Y0e B0)+sum_(j>=1)Tr(Yj Bj)<0.

Hence B(X) is not PSD, contradicting(i). This proves necessity. Sufficiency
is immediate by applying the amplification Phi tensor id to A(X), then
adding R tensor I. All steps are finite-dimensional. The proof gives an
existence/SDP certificate and a finite counterexample bound; it does not
make a floating solver's status an exact certificate.

## 3. Why the special Fisher pencil pays strict optimization margins

C's source has blocks diag(Q_i) and [[diag(LQ),LU],[(LU)^*,I]], with
sum Qi=I and sum Ui=0. Write independent Ui as real-Hermitian plus i times
Hermitian variables, and eliminate the last Q/U. At Qi=I/n,Ui=0 the source
constant A0 is positive for any strictly positive rectangular stochastic L.
Its trace is3; every nonconstant coefficient has trace0. Here a=n+ell+1
when L has ell outputs. The target order is b=m+1.

A constant release K_yi=1/m has KU=0 and target B0=diag(I_m/m,c0), Bj=0.
Choose any rational c0>0 inside the budget box and
epsilon=min(1/m,c0)/6. Then

 J=epsilon I_(ab)>0,
 R=diag(I_m/m,c0)-3epsilon I_b>0

is an EXACT strict certificate. Positive entry floors below1/m are also
strict there. For all feasible stochastic K and0<=c<=cmax, constant matching
instead bounds TrR<=1+cmax and TrJ<=(1+cmax)/lambda_min(A0). These explicit
rational bounds provide the input for weak-SDP bit complexity after the
linear equalities are parametrized. Poor row probabilities remain a paid
conditioning/bit resource. This paragraph does not substitute for C's full
Fisher equivalence, actual rational optimization receiver or complexity
radius derivation.

No physical channel calibration, private-bit acquisition, coherent-input
quantum channel, guessing/differential-privacy semantics, correlated-block
budget, historical priority or practical scientific advantage is established
by this lemma. The complete new design operation must retain those boundaries.
