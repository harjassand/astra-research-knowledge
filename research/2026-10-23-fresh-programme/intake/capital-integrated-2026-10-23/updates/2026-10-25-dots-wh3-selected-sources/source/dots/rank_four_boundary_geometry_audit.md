# Independent audit of the rank-four kernel geometry

Let K be a complex linear subspace of C³⊗C^r and identify its vectors
with3×r coefficient matrices. Define S(K)=span{AM: A^T=−A, M in K}.
Assume dim S(K)<=4. Then at least one holds:
(i) dimK<=1;
(ii) every vector of K has a common physical support of dimension<=2;
(iii) K is contained in C³⊗v for one reference vector v.
The proof is algebraic over C; transpose is bilinear, not adjoint.

## Rank-three member
For rank>=2 matrix M, A↦AM is injective on3×3 skew matrices, so
S(M) has dimension3. If independent M,N inK both have rank3, then
S(M)∩S(N) has dimension>=2. Given a rank3 M and any independent N,
replace N by M+epsilon N at a generic nonzero epsilon to ensure rank3.
Use an invertible reference coordinate change to make M=[I3,0].
Two independent skew matrices B satisfy BN inS(M). Their kernels are
distinct lines, hence the columns of N outside M's reference support
vanish. Thus N=[T,0]. The intersection condition says BT=T^TB for
two independent skew B.

For one such B with kernel line span(u), T preserves that line and
induces a self-adjoint map for the nondegenerate alternating form on
C³/span(u). In dimension2 such a map is scalar, so T=λI+u v^T.
For the second B, T=μI+w z^T with independent u,w. If λ≠μ then the
rank3 matrix (λ−μ)I would equal a matrix of rank<=2, impossible.
Thus λ=μ and u v^T=w z^T. Distinct image lines imply both sides zero.
T is scalar, contradicting independence. Hence dimK>=2 excludes rank3.
No orthogonal normal form for complex isotropic kernel lines is used.

## Rank-two member
Normalize M to [[1,0],[0,1],[0,0]], with remaining reference columns zero.
Every independent N can again be replaced by M+epsilon N to have rank2.
The same two-kernel intersection argument removes its outside reference
columns. Write N=[[p,q],[r,s],[t,u]]. The condition AN inS(M) imposes
on the three skew coefficients the matrix
[[0,t,−r], [−u,0,q], [−t,u,p−s]].
Its kernel has dimension>=2, so its rank is<=1. If t≠0, rows1 and3
are independent. If u≠0, rows2 and3 are independent. Consequently
t=u=0. Undoing N↦M+epsilon N proves that every member of K shares
M's physical plane.

## Product-only subspace
If every nonzero member has matrix rank1, fix a⊗v. Every other product
vector b⊗w must share a or v, since otherwise their sum has rank2.
If one member has physical factor not proportional to a, every member
must have reference factor proportional to v; otherwise the sum of two
appropriately chosen members has rank2. If no such member exists, all
members share a. This proves alternatives(ii) or(iii).

## Coordinate changes are NOT entropy filters
Left multiplication by G transforms S(M) by G^{-T}, because AG=
G^{-T}(G^TAG); right multiplication is an ordinary reference coordinate
change. Hence the dimension/intersection reasoning is invariant under
the invertible normalizations used above. No entropy inequality is
transported through a nonunitary filter. The resulting support
classification is transformed back to the original Hilbert space before
applying the following entropy facts.

## Entropy consequences in the original coordinates
For F(ρ)=S(ρ)−2S((W3⊗id)ρ)+S(ρ_R):
- A pure line gives F=H(p)−2H((1−p)/2)<=−log3, where p are Schmidt
  probabilities, padded to3.
- On a physical plane, W3 is exactly a flagged half-erasure:
  output=(1/2)UρU† directsum (1/2)ρ_R. Thus F=−2log2 exactly,
  independently of reference dimension and mixedness.
- A common pure reference reduces to the ordinary qutrit entropy bound,
  again F<=−log3.

For completeness the scalar entropy bound follows without a source
assumption. Put g(x)=xlogx−(1−x)log(1−x). Then
2H((1−p)/2)−H(p)=2log2+Σg(p_i).
If every p_i<=1/2, g is convex on the relevant interval and Jensen
gives the minimum at uniform p. If p1>1/2, convexity on the remaining
two entries lets one replace them by (1−p1)/2. The derivative of the
resulting sum is log[4p1/(1+p1)]>0 for p1>=1/2, so it cannot beat the
already covered boundary p1=1/2. The minimum is log3.

For the intended boundary application, positivity of
W3(I−P)=Σ_i L_i(I−P)L_i† and L_i†=−L_i imply that every vector in
K=ker W3(I−P) has L_iψ in ranP. Hence S(K) is contained in ranP,
and rankP<=4 supplies the geometric premise. The entropy conclusion
applies to states supported on K. Any additional tightness/limit step
linking boundary Gibbs sequences to K remains a separate obligation.
