# Acquired occupation tails and the competent tensor comparator

This gives ordinary comparators the same contraction and count information as the field sampler. Gaussian/Wick/resolvent and Gibbs-variational arguments are credited ordinary tools, not an asserted new generic principle.

## 1. Uniform physical grand moments

Use the EXACT balanced grand physical mixture, r<1 and T>=0. At a fixed imaginary-time cut the single-flavor history B is a contraction. With z=r exp(i phi), its absolutely convergent grand trace has covariance

`C_z=zB(I-zB)^(-1)`, `||C_z||<=c_r=r/(1-r)`.

The Gaussian trace identity is algebraic even for non-Hermitian B: insertion of the local falling factorial has conditional value `m! (C_z,ii)^m`. The second flavor has the conjugate covariance. The joint base-field/common-phase determinant weight is NONNEGATIVE. Its physical average after the phase projection is the balanced grand Gibbs mixture. Therefore, although a conditional inserted value can be complex,

`0<=E_bal binom(n_i,m)<=c_r^m`.

This holds at every finite symmetric slice count, because all cut factors are contractions and each physical finite-sector transfer is positive. For continuous Gibbs pass by finite-sector convergence and a dominated number sum: sector traces are bounded by D_n^2, and geometric fugacity tails dominate every fixed polynomial number moment. No unbounded-operator trace-norm Trotter assertion is needed.

For `t=1+1/(2c_r)>1`, Tonelli on the POSITIVE physical moments gives

`E_bal t^(n_i)=sum_m (t-1)^m E_bal binom(n_i,m)<=2`.

If a canonical balanced count K has acquired grand mass at least b, then

`E_can t^(n_i)<=2/b`, `P_can(n_i>H)<=2 t^(-H)/b`.

Across M sites and both flavors, the probability of exceeding the local cap is at most `4M t^(-H)/b`. This is a derived tail, not an altered Hamiltonian supplied at the start.

## 2. Replacing the Hamiltonian is payable too

Now use the exact finite K,K Gibbs state rho=exp(-beta H)/Z. Let Pi impose the per-site occupation cap, p=Tr rho(I-Pi), and rho' be its normalized projection. Projecting a purification proves `||rho-rho'||1<=delta=2sqrt(p)`.

Let H_cap=Pi H Pi restricted to Pi's subspace, with partition Z_cap. Rayleigh--Ritz gives Z_cap<=Z. Gibbs variational with witness rho', followed by finite-dimensional entropy continuity, gives for delta<=1

`0<=ln Z-ln Z_cap`

`<=beta ||H|| delta+(delta/2)ln(D_full-1)+h2(delta/2)`.

Here D_full=D_K^2, ln D_full=O(M) at fixed density, and `||H||<=2K||T||+2K^2 max U_i`. Choosing delta sufficiently inverse-polynomial in M,1/epsilon makes this log-partition debt at most epsilon. The tail in Section 1 then requires only a cap `O(log[M/(b epsilon)])` at fixed r,beta,density and interaction bounds: polynomial norm factors add logarithms. The witness rho' need not be constructed to prove this variational error bound.

For the embedded Gibbs state rho_cap of H_cap, `D(rho_cap||rho)=ln Z-ln Z_cap`. Quantum Pinsker therefore gives `||rho_cap-rho||1<=sqrt[2(ln Z-ln Z_cap)]`. This pays STATE replacement, not merely small original-state weight outside the cap.

The b here is for exact Gibbs. A finite-L count floor needs the continuum budget below before it is used as that b.

## 3. Grand normalization in the continuum is finite work

For all n,L, `Z_(L,n)<=D_n^2`, since physical transfer factors are contractions. For r'>r,

`sum_(n>J)r^(2n)Z_(L,n)<=(r/r')^(2J)(1-r')^(-2M)`

uniformly in L; the continuous trace has the same bound. Take J=O(M+log(1/eta)) to make both tails at most eta. On the finite n<=J sectors use `R_J=2J||T||+2J^2 max U_i`. The frozen Strang/principal-log estimate with L>=8 beta R_J bounds every log-partition error by `128 beta^3 R_J^3/L^2`. Make this at most eta. The finite sum then controls the exact balanced grand normalization, plus the two charged tails. Its vacuum contribution is one, so absolute tail errors also pay relative normalization errors.

This supplies a polynomial sufficient L, potentially enormous. The rejection/recursive-cut envelopes do not grow with L. The actual L16 receipts stay L16 predictions; they are not promoted to continuous Gibbs accuracy by this existence/cost argument.

## 4. Same-input tensor/MPO comparison

The ordinary baseline includes canonical AFQMC with correlated field updates, worldline/cluster methods where their sign conditions hold, and finite-temperature tensor/MPO algorithms. Full Hilbert-space enumeration is not the only comparator.

Kuwahara--Saito arXiv:1807.08424, Setup Eq.(1), explicitly takes a d-dimensional local Hilbert space and local operator norm at most one. Kuwahara--Alhambra--Anshu arXiv:2007.11174 gives stronger MPO constructions under its local bounded-norm setup. These are serious alternatives. The cap theorem above gives them a QUALIFIED local dimension (Hcap+1)^2, rather than a free fixed dimension. Direct bounded-spin normalization has onsite norm O(U Hcap^2) and hopping norm O(j Hcap).

Substituting growing norms into fixed-temperature constants does not automatically retain that theorem's polynomial bound. Conversely it is not an ordinary-method obstruction. Onsite-aware imaginary-time methods, bosonic moments, charge-resolved tensor contraction and model-specific compression may improve it. Exact canonical charge indices range only to K and should be granted to a competent tensor method, with actual approximation error and acquisition paid.

The present output is an explicit positive FIELD-law sampler and partition receiver. A tensor approximation to the quantum Gibbs state is a different, potentially stronger output. No practical speed advantage or new universal simulability boundary over those methods is established.
