# Energy-constrained redundancy forces approximate classical reconstruction
2026-10-29. Initial independent foundational construction; receiving review and historical novelty assessment pending. Not an encoder/recovery optimization.

## Scientific question and result
When can a quantum system be copied approximately to many observers yet remain far from every classical measure-and-prepare description? Astra's copy ladders show that unrestricted dimension defeats naive assertions of objectivity. Here the available low-energy state count is an explicit physical resource: for a fixed polynomial density of states, binary broadcasting error b implies one common classical reconstruction error O(b log(1/b)) at fixed mean energy. Persistent nonclassical reconstruction error then requires energy exponential in 1/b, up to polynomial factors. This is an existence/resource theorem, not a cheap laboratory construction, orthogonal pointer-basis theorem, independent-clone theorem, or a claim that natural dynamics actually broadcasts.

## Contract
Let H>=0 be a known self-adjoint Hamiltonian on a separable Hilbert space, with a normalized zero-energy vector |0> and finite-rank spectral projectors P_R=1_[0,R](H), d(R)=rank P_R, for every finite R. Let E_family be any family of density operators with Tr(H rho)<=E uniformly. Let B be a normal CPTP map from one full input algebra to two copies, each marginal T_i satisfying sup_rho T(T_i rho,rho)<=b, where T=half trace norm and rho ranges over the family. No extra supplied copies, labels or purification are given. B is a full-domain channel, so it may be composed on outputs not in the promised family. B need not conserve energy and no intermediate energy budget is assumed.

Define e as the infimum over one common finite-outcome measure-and-prepare (entanglement-breaking) channel Lambda of sup_family T(Lambda rho,rho). The source state is unknown to Lambda. No efficiency or acquisition claim is made for the supplied B, H, or the resulting POVM.

## The explicit inequality
For any R>0 and integer ell>=0, let K=2^ell and delta_R=sqrt(E/R)+E/R (one may cap delta_R at one). Then

 e <= min{1, ell b + 2 delta_R + d(R)^2/2^ell}.                 (1)

Proof:
1. The known CPTP cutoff/reset map C_R(rho)=P_R rho P_R+Tr[(I-P_R)rho]|0><0| takes values in the d(R)-dimensional subspace. For p=Tr[(I-P_R)rho]<=E/R, the gentle projection inequality and reset trace cost give T(rho,C_R rho)<=sqrt(p)+p/2<=delta_R. This is coherent cutoff, not a destructive energy measurement within P_R.
2. Apply B in a balanced binary tree of depth ell. A leaf marginal is a composition of ell maps chosen from T_0,T_1. For each promised rho, contractivity and a telescoping argument give distance <=ell b from rho, even though intermediate states may lie outside the promised family. Averaging over all output permutations yields a symmetric K-output channel without changing this bound. Outputs can be arbitrarily correlated or entangled.
3. Restrict this tree's input to P_R and apply C_R to every output. The resulting finite-dimensional symmetric broadcast channel F_R has one-site marginal F_R^(1). For rho_R=C_R rho, contractivity yields T(F_R^(1)(rho_R),rho_R)<=ell b+delta_R. The delta term here is solely from replacing the original input by rho_R; no unproved energy bound on intermediate outputs is needed.
4. Chiribella, arXiv:1010.1875v4, Theorem5 with k=1, gives one common measure-and-prepare channel L_R from the d(R)-dimensional input to output with half-diamond distance at most d(R)^2/K from F_R^(1). It is a true trace-preserving channel, not merely a separable approximation with an incorrect Choi marginal. The theorem's known Stinespring/symmetric-lift/coherent-state-POVM construction supplies the channel mathematically. Its input dimension does not enter the bound. Finite-outcome replacement follows from finite-dimensional convexity of the EB Choi set; no efficient finite design is claimed.
5. Embed the output and set Lambda=L_R composed with C_R. It is finite-outcome EB on the full Hilbert space, since each finite-dimensional POVM effect pulls back through C_R to a bounded positive effect and the effects sum to I. The final distance to rho adds at most another delta_R. This proves (1).

The cited primary theorem states a full diamond bound 2 d^2 k/K; dividing by two is necessary in (1). Its proof uses a symmetric dilation, not a claim that permutation invariance alone makes the physical output lie in the bosonic subspace. A mathematical Stinespring dilation of B is not an experimentally acquired source inverse or coherent access to the inaccessible environment.

## Polynomial spectral growth and energy obstruction
Suppose E>0, 0<b<1. Choose R=16E/b^2 and ell=ceil(log2[d(R)^2/b]). Then 2delta_R<=5b/8 and d(R)^2/2^ell<=b. Thus

 e <= min{1,b[2 log2 d(16E/b^2)+log2(1/b)+21/8]}.             (2)

If d(R)<=A(1+R)^s for fixed A>=1,s>0, then

 e <= min{1,b[2log2 A+2s log2(1+16E/b^2)+log2(1/b)+21/8]}.    (3)

In particular fixed E,A,s imply e=O(b log(1/b)). For any epsilon with e>=epsilon, (3) requires

 E >= (b^2/16) [2^((epsilon/b-2log2 A-log2(1/b)-21/8)/(2s))-1],

with a negative right side interpreted as the trivial lower bound zero. This is a necessary resource condition under a FIXED spectral-growth envelope, not a universal energy law across arbitrary Hamiltonians. Adding arbitrarily large zero-energy degeneracy defeats any such energy-only conclusion. The total number of modes/particles, volume and spectral degeneracy cannot be silently varied while retaining fixed A,s.

For E=0 the family lies in the finite-dimensional ground sector and one uses (1) with its rank and delta=0 directly. For the infimum b_2 over broadcasters, apply the inequalities to every achievable b>b_2 and take arbitrarily small slack. At b_2=0, first fix R, send ell to infinity, then R to infinity to get infimum e=0; this does not assert an exactly attained finite-outcome zero-error map in infinite dimension.

## Physical and computational interfaces
The theorem uses one unknown input to the candidate EB map. The proof's K-leaf tree uses K-1 calls to the supplied broadcaster plus output symmetrization and an enormous collective measurement. The classical reconstruction can alternatively be specified by its finite-dimensional EB Choi matrix and finite convex decomposition, but computing it is not solved efficiently. There is no guarantee of an experimentally available B dilation, energy-cutoff device, exact spectral knowledge, cheap POVM compilation, short classical record, or bounded control work. The primary de Finetti theorem grants existence, not a black-box implementation from calls to opaque B alone. An EB map may prepare noncommuting output states; no common orthogonal pointer basis is implied.

## Executed load-bearing checks
check_construction.py constructs actual universal qubit 1-to-2 cloner Kraus maps, composes the full binary tree through depth3 (128 Kraus operators, eight outputs), and checks the leaf channel and telescoping inequality against its exact depolarizing law. Residual <=1.06e-15. The third-depth leaf is already EB in this example; no optimality conclusion is drawn. Fifty finite oscillator cutoff/reset density-matrix tests verify the coherent tail bound. Large one-oscillator resource rows are evaluations of (1), not simulations of gigantic trees: at E=1 and b=.001, the simple prescription gives a reconstruction bound .0593884 using K=2^58 in the proof. These huge resources explicitly exclude a practical implementation claim.

## Astra capital, freshness and prior science
Astra Research plugin search for sharp memory/predictive compression timed out (MCP request timed out); it was attempted first. GitHub fallback read 00_START_HERE and pinned revision d5366275f4886a027526b70997e75db2c19e4efa. Current packets N61,N69,N368,N422 and actual governing rendered sources were read selectively. Crucially, corrections to historical N69/N93 say bounded-Holevo classicality was ALREADY internally closed by N353; this construction does not claim to solve that old open wording. N368's linear-logarithmic capacity proof was read in full; its statement provides context, not a premise for (1). Its much weaker fixed-capacity modulus does not contradict the present stronger fixed-Hamiltonian spectral premise. N422's EB/nonorthogonal-output and HMM-memory limits are preserved.

Exact Astra source routes at that revision:
- web/pages/d-0d0b53ae371005dd.html (historical report with current corrections)
- web/pages/d-b4ddaa96b233287d.html (historical fixed-sandwich reduction audit)
- web/pages/d-37081fa55c670b9b.html (N368 governing full proof)

Primary import actually read: Giulio Chiribella, On quantum estimation, quantum cloning and finite quantum de Finetti theorems, arXiv:1010.1875v4, Section2.1, Theorems4–5 and proof, https://arxiv.org/pdf/1010.1875 . This gives the decisive channel-level d^2/K estimate. Christandl–Koenig–Mitchison–Renner quant-ph/0602130 SectionII.D is related, but is not needed to repair Choi marginals here. Infinite-dimensional quantum Darwinism and energy-constrained de Finetti have substantial prior literature; historical novelty of this binary-broadcast/resource formulation has NOT been established. The intended advance is a sharper physical-resource explanation and a path to testing sharpness, not an unsupported claim of solving the emergence of classical physics.
