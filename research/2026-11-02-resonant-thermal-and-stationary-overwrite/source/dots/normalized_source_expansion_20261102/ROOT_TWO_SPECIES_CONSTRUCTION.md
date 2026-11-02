# Root construction: normalize singleton pressure before source expansion

2026-11-02. Constructive proof candidate for independent review. This is a scalar projected-Gibbs expansion, NOT a uniform operator-log theorem.

## 1. Change the exact source dictionary, not the physical Hamiltonian
Use the earned generic-V full-column history dictionary. For each elementary V label let R_lambda contain its clock matrix-unit supports and all checks meeting its data support; include actual data/bath support as before. Define the CLOCK CONTACT set T_lambda=N1(R_lambda) in the clock overlap graph. Group USED labels into components whenever their contact sets or actual data/bath supports overlap. The source Gamma owns C_Gamma=union R_lambda and has contact set T_Gamma=N1(C_Gamma). Its owned columns may be disconnected; this is harmless because all their complete trajectories are retained in that one source.

Crucially, source compatibility forbids the SAME enlarged contact overlap used to form components. Distinct compatible sources have disjoint T sets. Thus every individual background rod can interact with at most ONE source. Syndrome closure, commuting data words across sources and scalar reduction below distance remain valid, because this grouping only merges the old components and never separates affected-check supports.

## 2. Exact singleton resummation
For fixed syndrome s, write the convergent background log partition function as

 log Xi(s)=sum_T nu_s(T),

where T is a connected Mayer cluster of clock rods. Its one-rod clusters are ordinary nonwinding rods, ordinary winding rods and thermal wraps. A source pins a background rod by B_Gamma(rod) in {0,+1,-1}; a rod on an owned clock has factor0. For a cluster T put B_Gamma(T)=product_(rod in T)B_Gamma(rod).

For fixed source histories the exact normalized background response is

 exp{sum_T nu_s(T)[product_Gamma B_Gamma(T)-1]}.

For a singleton rod, disjoint contact sets imply

 product_Gamma B_Gamma(rod)-1=sum_Gamma[B_Gamma(rod)-1].

Therefore absorb ALL singleton responses into each source activity z_Gamma. No one-rod bridge remains between distinct sources. This is the place where the enlarged contact dictionary is essential; grouping only overlapping owned columns would not suffice.

For the resonant path let M0=2g^2/t=KJ0, J0=2g^2/(tK), and h_nv=M0-J0. Let h_nv^beta be the finite-time nonwinding integral and delta_nv=h_nv-h_nv^beta. Then

 0<=delta_nv<=(4/3) KJ0 exp(-beta t/K^2).

Owned-clock singleton deletion contributes at most exp[-beta h_nv^beta+beta J0] per clock. Exterior NONWINDING and WRAP singleton responses have modulus at most1 because their measures are positive and B-1<=0. Exterior winding singleton responses cost at most exp(2beta J0) per affected contact clock. Combined with the full-column raw bound K^|C|exp(beta M0|C|), this gives

 |z_Gamma| integrated over a fixed m-label source
 <= [K^b_c d_B^b_B exp(2beta J0 d_c+beta delta_nv b_c)
      (exp(beta v_dict)-1)]^m = q0(v)^m,

where |C_Gamma|<=b_c m, |T_Gamma|<=d_c m and the Pauli/matrix-unit dictionary norm overhead is explicit. The KJ0 scalar self-energy has canceled BEFORE absolute source majorants. This does not remove the physical growth of b_c, d_c or dictionary size when K is varied.

## 3. Remaining clusters are an ordinary second polymer species
Let the EVENT species consist of all background connected clusters T with n(T)>=2 rods. Give an event its original complex activity nu_s(T), with event-event pair factor1. Give a source-event pair factor B_Gamma(T), still in {0,+1,-1}. Source-source factors are the enlarged contact/data/bath hard cores.

The event-only partition function is exp(sum_(n>=2)nu_s(T)). Summing independent event multisets in the joint source/event gas and dividing by this event-only factor gives EXACTLY

 sum_(compatible sources) product z_Gamma
   exp{sum_(n(T)>=2)nu_s(T)[product_Gamma B_Gamma(T)-1]},

which is the remaining normalized projected-Gibbs expansion. This is not an assumed forest bound or a product of independently normalized actual singleton source weights. Complex event activities are allowed by the same |pair factor|<=1 continuum cluster theorem. Overlapping event clusters are allowed: these events encode the exponential of the log series, not physical disjoint rod configurations.

## 4. Explicit second-level KP target
At fixed gamma>0 define the weighted residual row mass

 E_gamma=sup_clock a integral_(T:n>=2,a in support T)|d nu_s(T)| exp(gamma n(T)).

Inflating EVERY native rod activity by exp(gamma) and using the strict original KP bound gives, schematically and with the explicit tilted charges,

 E_gamma <= exp(gamma){beta[exp(a0_gamma)M0(b_gamma)-M0]
                       +exp(a0_gamma)W(b_gamma)}.

The subtraction is INSIDE exp(gamma). Thus E_gamma=O(exp(2gamma) beta D eta^2 J0)+thermal wrap,
not O(beta M0). Admission must use the inflated-activity rod inequalities; it cannot reuse an unweighted margin without checking it.

Let C_an count connected used-label animals in the enlarged contact graph, B_r bound elementary labels contacting a fixed clock, and B_s m bound hard-core source roots near an m-label source. Set a_source=A m and a_event=gamma n, and define

 G(q)=q exp(A)/(1-C_an q exp(A)).

For an event root T, source contributions are at most 2 B_r n(T)G(q). For a source root Gamma, hard-core source contributions are at most B_s m G(q), and event contributions at most2 d_c m E_gamma. Choose

 A>=4d_c E_gamma+4,
 2B_r G(q)<=gamma/2,
 B_s G(q)<=A/4.

These are ordinary two-species KP inequalities with slack. There is no unbounded hyperedge-arity combinatorics or exp(beta M0) bridge factor. Gamma can be a fixed number; all graph/source constants remain charged.

## 5. Local influence and exceptional logical sources
Singleton-dressed source activities are generally bounded FUNCTIONS of syndrome bits, not individual monomials. Their dependence footprint is the original polynomial stabilizer filling plus the contact set T_Gamma. Uniform envelope bounds and |z(s)-z(s')|<=2 envelope suffice when a changed source footprint is marked. No Fourier truth table on a polynomial-size filling neighborhood is needed.

Event activities retain the background cluster's winding-character dependence and exponentially charged rod count. After subtracting the event-only logarithm, every remaining connected second-level cluster contains a source. Scaling V from an admissible v0 to v multiplies every concrete history by (v/v0)^{number of V events}; hence all such terms gain at least v/v0. The existing marked-source/marked-winding influence argument can then be rerun with EVENT roots, paying E_gamma and the source footprint count.

All large memory-touching sources remain exceptional regardless of accidental scalarity; bath-only sources stay in the scalar background. A fixed exceptional source acts as a modulus-at-most-one pin on the second gas (hard cores on other sources, B_Gamma on events). Its singleton dressing has already been included in its own norm envelope. Second-level pin ratios then give the same n-anchored relative matrix remainder with q0(v), not the old raw source fugacity.

These last analytic consumers must be checked with the exact source dictionary and actual norm budgets before claiming improved robustness. The fixed-K thermal compiler and fixed-source bounds are already separate retained results.

## Scope
The intended gain is removal of an unnecessary scalar bandwidth/self-energy charge, not removal of physical clock dimension, correlated-hook support, control noise, thermal winding cost or preparation assumptions. At fixed b_c,d_c,D,bath dimension and beta J0, the new source envelope is polynomial in K rather than exp(beta J0 K); if those support constants grow with K, their growth must be substituted explicitly.
