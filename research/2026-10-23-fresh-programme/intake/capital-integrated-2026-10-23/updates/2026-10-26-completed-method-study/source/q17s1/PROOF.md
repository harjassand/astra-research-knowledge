# A sharp heat-capacity/temporal-spread law for reciprocal thermal trees

This is a self-contained proposed theorem and construction. Correctness at the stated mathematical scope is argued below and checked independently in code. Priority/novelty has not been established. The model is ordinary linear lumped Fourier conduction; it is not a new heat-transport mechanism or a fabricated device.

## 1. Operation and hypotheses

There are N finite isothermal lumps, with C_i>0, and one fixed-temperature bath b. The positive, time-independent, reciprocal conductances form a tree on these nodes and b. Write all temperatures relative to the bath. At t=0 a finite energy E is deposited at one source lump s: T_s(0)=E/C_s and all other T_i(0)=0. No further input, switching, advection, other storage degree of freedom, or feedback occurs. The source-connected component after deleting the bath contains every relevant node; any other nodes are wasted capacity and can only weaken the bound stated with totals.

Let L be the Dirichlet weighted Laplacian with the bath deleted and C=diag(C_i). Then

    C dT/dt = -L T.

The normalized energy flux into the bath is f(t)=sum_i g_ib T_i(t)/E. Positivity, stability, and energy conservation imply f>=0 and integral f=1. Define

    tau = integral t f(t) dt,
    sigma^2 = integral (t-tau)^2 f(t) dt,
    R = (sum_i C_i)/C_s.

The coefficient sigma/tau is the width of the deterministic release waveform. It is not an assertion about stochastic experimental timing noise. The absorption-time representation is a mathematical tool: normalized node energies p_i=C_i*T_i/E obey a killed reversible continuous-time Markov equation.

## 2. Theorem

For N>=2 and R>1,

    sigma^2/tau^2 >= B_N(R)
      := 1/[1+(N-1)tanh(log(R)/(2(N-1)))].                 (1)

This is the exact minimum over all such trees with N lumps, prescribed C_s, total capacity R*C_s, and any prescribed tau>0. Equality is attained by the positive ladder below. Thus neither branching nor arbitrary positive optimization of heat capacities and conductances can improve (1) in this class.

At fixed R, even arbitrarily many lumps obey

    sigma^2/tau^2 >= 1/[1+log(R)/2].                       (2)

For a target relative width epsilon<1, a necessary condition is

    R >= exp[2(epsilon^(-2)-1)].                          (3)

The exact finite-N feasibility condition is sharper. A finite R is possible only if epsilon^2>1/N. In that case the sharp necessary and sufficient capacity requirement in this ideal class is

    log R >= 2(N-1)*atanh[(epsilon^(-2)-1)/(N-1)].

Sufficiency follows from the attaining design and continuity/monotonicity of B_N(R). Equality epsilon^2=1/N requires R to diverge.

If the initially heated lump has maximum admissible rise DeltaT and energy E, then C_s>=E/DeltaT, so R<=C_total*DeltaT/E. Substitution into (2) yields the corresponding energy/temperature/capacity resource bound, provided R>=1.

The degenerate N=1 case has an exponential release and sigma^2/tau^2=1. Positive extra capacities require R>1 when N>=2.

## 3. Exact ladder moment formula

Number ladder nodes 1=s,...,n, with resistances r_k>0 from k to k+1 (k<n), and r_n>0 from n to bath. Put

    S_k=sum_{i<=k} C_i,    a_k=r_k S_k.

The Laplace transform of normalized output flux is

    F(z) = (product_k 1/r_k)/det(L+z C)
         = det(L)/det(L+z C).

The first equality follows by the (n,1) cofactor of the tridiagonal matrix; det(L)=product_k 1/r_k. Since C^(-1/2)L C^(-1/2) is positive definite, its eigenvalues lambda_j are positive, and

    F(z)=product_j lambda_j/(lambda_j+z).

Consequently tau=tr(L^(-1)C) and sigma^2=tr[(L^(-1)C)^2]. This spectral argument identifies a convolution of exponentials, without assuming any directed thermal link.

The ladder inverse has entries

    G_ij=(L^(-1))_ij=sum_{k>=max(i,j)} r_k.

Expanding the two traces gives

    tau=sum_k a_k,
    sigma^2=sum_{k,l} r_k r_l S_min(k,l)^2
           =a^T K a,
    K_kl=S_min(k,l)/S_max(k,l).

These are independently checked against the backward moment equations L h=C*1 and L h2=2 C h in explore.py. The latter equations do not use the trace/kernel formula to evaluate the designs.

## 4. Optimize all positive resistances and capacities

Set x_k=log S_k. Then K_kl=exp(-|x_k-x_l|), a positive definite exponential covariance kernel. For fixed S and sum a=tau, matrix Cauchy--Schwarz gives

    a^T K a >= tau^2/(1^T K^(-1)1),

with equality at a=tau K^(-1)1/(1^T K^(-1)1).

For rho_k=exp[-(x_{k+1}-x_k)] in (0,1), the inverse quadratic form is

    u^T K^(-1)u = u_1^2
         +sum_{k=1}^{n-1} (u_{k+1}-rho_k*u_k)^2/(1-rho_k^2).

This follows either by multiplying the resulting tridiagonal inverse by K, or by expanding this expression. Therefore

    1^T K^(-1)1
      =1+sum_k (1-rho_k)/(1+rho_k)
      =1+sum_k tanh[(x_{k+1}-x_k)/2].                     (4)

The equality weights are strictly positive. The endpoint components of K^(-1)1 are 1/(1+rho_1) and 1/(1+rho_{n-1}); an interior component is

    1/(1+rho_{k-1}) - rho_k/(1+rho_k)>0.

Thus optimizing over unconstrained a did not accidentally require a negative thermal resistance. Since the n-1 positive increments x_{k+1}-x_k sum to log R, strict concavity of tanh on (0,infinity) gives

    sum_k tanh[(x_{k+1}-x_k)/2]
      <=(n-1)tanh[log R/(2(n-1))].                       (5)

Equality holds exactly when all log increments are equal. Combining (4),(5) proves the ladder case of (1).

## 5. Explicit attaining construction

Given n>=2, C_s>0, R>1, and tau>0, let

    q=R^(1/(n-1)),     rho=1/q,
    S_k=C_s*q^(k-1),
    C_1=C_s,           C_k=S_k-S_{k-1} (k>=2),
    Z=1+(n-1)*(1-rho)/(1+rho).

For n=2 set w_1=w_2=1/(1+rho). For n>2 use the same endpoint weights and w_k=(1-rho)/(1+rho) for 2<=k<=n-1. Set

    a_k=tau*w_k/Z,     r_k=a_k/S_k.

Every component is positive, the capacities sum to R*C_s, and the mean is tau. The achieved normalized variance is exactly 1/Z=B_n(R). Overall resistance scaling changes tau without changing relative width or the heat-capacity ratio. This freedom is a timescale rescaling, not a precision improvement.

## 6. Extension to every tree

Root the tree at the bath. Let v_1=s,...,v_m be the unique source--bath path, excluding the bath, with path resistances r_1,...,r_m and tails R_k=sum_{ell>=k} r_ell. Partition the relevant lumps into B_k: the path node v_k and its off-path branches. Put D_k=sum_{i in B_k}C_i.

For any rooted resistive tree, G_ij=(L^(-1))_ij is the resistance shared by the paths from i and j to the bath. In particular, for i in B_k,

    G_si=R_k.

For i in B_k, j in B_l,

    G_ij=R_max(k,l)+1_{k=l} H_ij,

where H_ij>=0 is the shared off-path resistance. If i or j is the attachment node, H_ij=0.

The general backward equations give

    tau=sum_i G_si C_i,
    E[T^2]=2 sum_{i,j} G_si C_i G_ij C_j.

Collapse B_k into a single lump D_k at v_k. The mean is unchanged. Its second raw moment is smaller by exactly

    2 sum_k R_k sum_{i,j in B_k} C_i C_j H_ij >=0.          (6)

Because the means agree, (6) is also the variance difference. The collapsed path has m<=N nodes, initial lump D_1>=C_s, and relevant total capacity no larger than the original total. Its capacity ratio R'<=R. The ladder bound thus applies to the collapsed path.

Finally, Z_n(R)=1+(n-1)tanh(log R/[2(n-1)]) increases with R and with n. For the latter, set x=log R/[2(n-1)]; the derivative of k*tanh(log R/[2k]) is tanh x-x*sech^2 x>0 for x>0. Hence B_m(R')>=B_N(R). This proves (1) for the original tree. A pure n-node path from Section 5 attains equality, so the bound is globally sharp over the full tree class.

## 7. Limits and reach

As n tends to infinity, k*tanh(log R/(2k)) tends to log R/2, proving (2). Positive finite ladders approach this infimum. At fixed n, R tends to infinity gives B_n(R)->1/n, agreeing with the established unrestricted phase-type optimum. Achieving that directed-cascade precision with reciprocal heat links consumes an unbounded capacity ratio.

The theorem extends by an appropriate convergent RC discretization to one-dimensional linear Fourier conduction joined to a finite source reservoir, with insulated sides and a terminal bath. The exact finite-tree theorem above does not require this continuum claim; see CONTINUUM.md for the explicit limiting shape and its assumptions.

## 8. Boundaries deliberately retained

No generalization of the heat-capacity bound to looped graphs is proved here. graph_explore.py performs exploratory optimization on complete reciprocal graphs but cannot rule out a counterexample. There is a separate established resistance/terminal-conductance bound for reversible Markov chains (Chiclana 2026, Appendix A); our capacity optimization must not be mislabeled as that prior theorem or vice versa.

A lower bound on RMS width alone does not rule out a high fraction of output energy in a narrow time window accompanied by a very small, long tail. No concentration-in-probability or pointwise pulse-height theorem is asserted here. All quoted precision consequences use the specified RMS metric.

Time-dependent or temperature-dependent conductance, latent heat, moving fluid, mechanical energy storage, actively controlled switches, nonlinear material transitions, and multiple initially excited nodes are outside (1). Actual passive nonlinear switches are already demonstrated. The theorem is therefore a decisive restriction on the fixed linear-tree construction, not a no-go theorem for all passive thermal devices.
