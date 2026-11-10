ROOT MATHEMATICAL PREPARATION AFTER 9CE791
10 November2026 Brisbane. Two precise bridges; no global all-K gap or universal transition compiler is asserted.

Sources: complete P1_XI_9CE791_WF_RETURN.md21678UTF8/SHAfdad8f19257f10b43e572b556d0077945200ee4c5eba7c4c4fbada4a5f91ca08 and actual issued14386/269f1563, full answer/activity read. The actual full all-K/all-time/closed-simplex polynomial finite-bit question stays unchanged. Current2611.08623v1 Definition3.1/Proposition3.4/entrance Proposition3.6/Theorem4.1 reread: the gamma-count rates and representation are premises, not new discoveries or a finite-bit entrance sampler.

1. DISCRETE GIBBS GAP TRANSFERS TO THE PHYSICAL GAMMA-COUNT GAP
Use the accepted joint law nu(n,dx)=pi(n)Dir_(alpha+n)(dx), with marginal mu(dx) proportional to exp(sigma dot x)Dir_alpha(dx) and conditional n_i|x independent Pois(sigma_i x_i). The count Gibbs kernel G samples x conditional on n and then m conditional on x. It is reversible with invariant pi. For any form-domain count function F,
 E_G(F)=1/2 sum_n pi(n)G(n,m)(F(n)-F(m))^2
       =E_mu Var_(productPois(sigma_i x_i))(F).
The equality follows by conditioning two independent counts n,m on the common x. Product-Poisson Poincare gives Var(F)<=sum_i theta_i E[(F(n+e_i)-F(n))^2]. One self-contained derivation is to approximate each Pois(theta_i) by the sum of M independent Bernoulli(theta_i/M) variables and apply the product Efron-Stein inequality; finitely supported F passes to the limit, followed by form closure.
Conditional expectation of x_i given n is (alpha_i+n_i)/(alpha0+|n|). Therefore
 E_G(F)<=sum_n pi(n)sum_i sigma_i(alpha_i+n_i)/(alpha0+|n|)*(Delta_i F)^2
        <=(2/alpha0) E_D(F),
where E_D is the actual continuous-time gamma-count birth/death form, with birth sigma_i(alpha_i+n_i)/2. Thus an ACTUALLY PROVED discrete gap lambda_G>0 implies
 lambda_D>=alpha0*lambda_G/2.
Combining this with ROOT's already proved Dirichlet-fibre comparison yields
 Var_mu f<=[2/alpha0+2S/(alpha0*(alpha0+1)*lambda_G)] E_mu(f).
This is a genuine conversion between different count chains, not identification of G with the entrance dual. A global polynomial lambda_G, boundary-start TV and transient initialisation are not supplied. No reverse comparison or circular assumed WF gap closes the question.

2. THE GIBBS STEP ITSELF HAS A FINITE-BIT IMPLEMENTATION
For any rational alpha,sigma and integer input n, choose eta in(0,1). If S=0 output zero counts. Otherwise take M>=max(ceil S,ceil(4S^2/eta),1). Perform M exact rational Bernoulli(S/M) trials. At each success draw a proposal label by the Polya urn with initial weights alpha+n, updating the urn after EVERY proposal, accepted or rejected. Accept a proposal label i with exact rational probability sigma_i/S. Return the accepted counts. Conditional on one latent Dir(alpha+n), the proposal count would be Bin(M,S/M); replacing it by independent Pois(S) and then thinning gives exactly the desired product-Poisson conditional. Le Cam bounds the whole output-count error by2S^2/M<=eta/2. Rational urn choices/fair-bit rejection and all M trials have expected bit work/fair bits and peak space polynomial in complete input bits, K, numerical S and eta^-1; numeric |n| is not required as an iteration bound. Every integer has the bits of alpha,n,sigma plus O(log M) count growth. No actual Dirichlet, Poisson-real, normalising or integration oracle is used. This only implements G; its mixing and the original diffusion law are separate.

3. COVER THE REPLACEMENT EDGES OF THE EDIT METRIC
9CE791 proves W_edit(G(n),G(n+e_i))<=S/(alpha0+|n|+1). The max(additions,deletions) multiset metric also has distance-one REPLACEMENT edges, which do not follow with the same constant by a two-step deletion/addition path. Let n=l+e_i,m=l+e_j, |n|=|m|=N. Couple a common Z0~Dir(alpha+l) and U~Beta(1,alpha0+N-1), and set Z_n=(1-U)Z0+Ue_i, Z_m=(1-U)Z0+Ue_j. Common Pois(S) proposals and coupled thinning change at most one edit per replaced proposal. Hence
 W_edit(G(n),G(m))<=S/(alpha0+N).
This is also valid if some sigma vanish. The proof is a coupling identity; it is not an instruction to use a continuous sampler. Together with addition/deletion edges, shortest edit paths can be taken without dropping total count below min(|n|,|m|). Thus for |n|,|m|>=h>0,
 W_edit(G(n),G(m))<=S/(alpha0+h)*d_edit(n,m).
Outputs need not remain in this high-count region: E_G|n'|<=S. Therefore this is NOT global contraction and gives no high-region invariant set or global gap. Low-count expansion and its actual transition probabilities remain central.

4. COMING DOWN PLUS BINARY OR GIVES A ROW-UNIFORM MIXING BOUND
For the unpruned ASG, its first moment m(u) satisfies m'<=(S+1)m/2-m^2/2. Scalar comparison with the solution starting from infinity gives, for every finite initial r and u>0,
 E_r N_u <=(S+1)/(1-exp(-(S+1)u/2))<=S+1+2/u.
The finite-r comparison is elementary logistic ODE comparison, so no infinite-entrance sampler is assumed. In particular E_r N_1<=S+3 uniformly over r.
In the K=2 OR representation, the initial r output roots at backward time1 are constants or Boolean ORs of subsets of these N_1 unresolved variables. Couple the types of those N_1 variables using the accepted binary pruning process for a further t-1 units. Every variable fails to resolve by beneficial mutation with probability at most exp(-alpha_+(t-1)/2). Once all of them agree, all original root expressions agree, whatever their shared subsets. Conditioning on the first graph segment and taking expectation proves
 TV(O_(t,x)^r,O_infinity^r)<=min(1,(S+3)exp(-alpha_+(t-1)/2)), t>=1,
UNIFORMLY in r,x, including boundary starts. Unlike a union over the original r roots, the prefactor is polynomial in S and independent of row length.
The same bound holds for the latent simplex transition laws. To see this without presupposing a density, append an infinite conditionally IID categorical sequence to each latent point. TV of these infinite-sequence laws is the supremum of finite-prefix TV (conditional-expectation approximation of events). Empirical frequencies converge to the latent point almost surely; data processing recovers its law. The finite-prefix bound therefore passes to the latent law. This uses a proof-level infinite observation, not infinite work in a compiler.
This supplies a genuine two-type boundary-uniform TV interface for future perturbation arguments. It does not prove multi-type pruning for intermediate fitness, or remove the cost of a general all-K transient representation. The class-lifting theorem in9CE791 retains its all-positive-mutation/whole-row scope; time-changed internal compositions through vanishing class mass must retain the correct entrance interpretation rather than silently assuming all coordinates stay interior.

All prior ASG/positive-mixture/fibre constructions are inherited once. No historical novelty, result rating, model effect, new resource, held-source recovery or extra build/index/probe is claimed. All known/unknown access/transfer/resource holds persist.
