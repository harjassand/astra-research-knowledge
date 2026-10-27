# Finite-inventory kinetic ion separation: constructed scope

This note investigates a restricted classical separation operation, not a device claim. Let L denote a slow valuable ion and N a faster competing ion. Both have the same equilibrium affinity in the proposed capture medium; their association and dissociation rates share fixed positive kinetic multipliers a_L < a_N. The illustrative multiplier ratio a_L/a_N = 1.03/1.33 is borrowed from the *bulk diffusion coefficients* used in Herman et al. (2023). Those coefficients do **not** establish capture/release rate ratios for a real material.

## 1. Saturation cannot enrich the complete released stream

For a constant-composition chemostatted feed, let the capture flux be

    b_i(t) = a_i c_i h(t),    h(t) >= 0,

where h may depend on arbitrary common gates, vacancy, finite capacity, and prior occupancy. Let S_i be bound inventory and d_i arbitrary nonnegative release flux, so dS_i/dt = b_i - d_i. On any closed bed cycle S_i(T)=S_i(0),

    D_i = integral d_i dt = a_i c_i integral h dt.

Consequently, collecting **all** release as product gives

    D_L/D_N = (a_L/a_N)(c_L/c_N).

This is an exact mass-balance statement. It permits nonlinear saturation and arbitrary timing. It does not apply when only selected release windows are product, feed composition changes, or capture has an ion-specific factor beyond a_i. Those changes must be modelled rather than presumed absent.

## 2. Sharp one-wash purity/recovery curve

Start with an equal-affinity equilibrium loading whose L/N inventory ratio is q. Wash without rebinding, with dissociation rates a_i k(t), and route release according to any species-blind time valve. In operational dose H = integral k(t)dt the release-time densities are

    f_i(H) = a_i exp(-a_i H).

The likelihood ratio f_L/f_N increases monotonically in H. Hence the Neyman-Pearson optimum at any specified recovery r **of the initially loaded L** is the late-release tail. This conditional recovery is not whole-source recovery unless loading all source L was separately supplied and charged. For rho=a_N/a_L>1 its recovery of initially loaded N is exactly r^rho. The best product purity is

    p(r) = q r / (q r + r^rho).

Equivalently,

    r <= [q(1-p)/p]^(1/(rho-1)).

An arbitrary common wash waveform only reparameterizes H and does not change this frontier. An eventual complete tail collection is an ideal limit; finite completion, dead volume, rebinding and elution losses can worsen it. The theorem concerns the specified initial loading, not a loading enriched by earlier uncharged cycles.

## 3. A nonlinear finite-source capture-turnover floor

Let a fixed-volume well-mixed source initially contain L_0,N_0 particles or moles. The bed initially and finally has zero inventory. Total bed occupancy is at most B. Every source-to-bed capture obeys

    b_L = a_L L h(t),    b_N = a_N N h(t),

with any nonnegative common h(t), including occupancy-dependent saturation. Releases can return to source or enter the product; grant even an ideal species-resolved product router. There are no other sources, sinks, inventories, reactions, or uncharged Na-discard operations.

Require final L recovery R in (0,1) and product L mole fraction at least p. Then product N inventory is at most

    P_N,max = R L_0 (1-p)/p.

Source N is always at least N_min = max(0,N_0-P_N,max-B). Write r_L(t) for release back to source. From dL/dt=-b_L+r_L,

    integral b_L/L dt = log(L_0/L_T) + integral r_L/L dt
                         >= log(1/(1-R)).

Therefore gross N captures A_N satisfy

    A_N = rho integral (N/L)b_L dt
        >= rho N_min log(1/(1-R)).

The bound charges gross turnover, **not joules**. It remains valid for arbitrary common waveforms, nonlinear vacancy, arbitrarily many retries and perfect final sorting. For dissociation flux at most a_N k_off,max S_N and a closed bed cycle,

    A_N <= a_N k_off,max integral S_N dt <= a_N k_off,max B T,

so

    T >= A_N/(a_N k_off,max B).

A numerical release-rate or capacity value must be physically acquired before converting this to a clock-time statement. Large B can make N_min=0; then this particular bound is silent, while storing nearly all source Na is itself a charged inventory. The result does not rule out an ion-specific capture material, a spatial ratchet, electrophoresis, selective precipitation, or separately costed source preprocessing.

## 4. Exact optimal ONE-SOURCE wash-and-recycle operation

We next enlarge the favourable idealization: infinitesimal capture cohorts, negligible loading time, no bed interference or rebinding during wash, all released wash ions recycled without loss into **one well-mixed source**, complete elution of the survivors as product, and free source/bed switching. There are no other source, enriched, or waste inventories. This is a restricted conventional kinetic-swing separation operation. No energy or hardware advantage is asserted. An ordinary countercurrent multistage cascade lies outside this class and can be far better; this section must never be presented as its lower bound.

Each cohort is washed to dose H. Set

    rho = a_N/a_L > 1,
    gamma = a_L/(a_N-a_L) = 1/(rho-1),
    u = exp[-(a_N-a_L)H] in (0,1].

Survival fractions are s_L=u^gamma and s_N=u^(gamma+1). For infinitesimal common capture exposure dz,

    dP_L = a_L L u^gamma dz,
    dP_N = a_N N u^(gamma+1) dz,
    dA_N = a_N N dz.

Define x=log(L_0/L), X=log(1/(1-R)), and v=log(N_0/N)/rho. Then

    dv/dx = u,    dA_N = rho N_0 exp(-rho v)u^(-gamma)dx.

For endpoint impurity P_N (positive and less than N_0), let

    V = log[N_0/(N_0-P_N)]/rho.

Changing variable to v and writing w=1/u>=1 gives the exact problem

    minimize rho N_0 integral_0^V exp(-rho v)w(v)^(gamma+1)dv
    subject to integral_0^V w(v)dv = X.

If the constraint w>=1 is inactive, strict convexity or Holder's inequality gives the global optimum

    I = integral_0^V exp(rho v/gamma)dv
      = (gamma/rho)[exp(rho V/gamma)-1],
    w_*(v) = (X/I) exp(rho v/gamma),
    A_N,min = rho N_0 X^(gamma+1)/I^gamma.

The inactive-condition check is X/I>=1. The optimal operation is attained as the infinitesimal-cohort limit by an ordinary adaptive **one-source** wash-and-recycle policy with H(v)=log(w_*(v))/(a_N-a_L). Thus programming the same wash differently does not create an additional operation beyond this restricted comparator. This says nothing against multistage fractionation: moving the wash and retained fractions between separate partially enriched inventories changes both the state and the endpoint contract.

For a fixed wash u=V/X, the exact cost is

    A_N,const = P_N (X/V)^(gamma+1).

The optimal use of an allowed impurity budget is its largest permitted P_N, provided feasibility and the inactive condition hold. In the dilute high-purity limit,

    A_N,min ~ rho^(gamma+1) N_0^(gamma+1) X^(gamma+1) / P_N^gamma.

The severe exponent comes from the specified small kinetic contrast and repeated single-wash retention. This is **not** a lower bound on all separation physics, all kinetic networks, or all selective materials.

It is also not a global optimal-control theorem for concurrent capture/rebinding or additional internal kinetic states, even if they share one source. The strong cost formula requires the sequential infinitesimal-cohort operation specified above. The weaker general floor in Section 3 has broader waveform scope under its own inventory/sink assumptions, but does not establish general impracticality.

Parent comparator challenge, 27 October 2026: a gambler's-ruin countercurrent cascade can choose wash fractions that give L a drift toward product and N a drift toward waste, with all intermediate inventories and beds charged. The parent is constructing that comparator independently. It is not included in the present numerical optimum, and its existence precludes reading a large one-source cost as a general separation obstruction. This correction changes the scope of comparator conclusions, not the restricted derivation.

## 5. What is and is not new here

Sections 1-4 are derivations constructed for this investigation. Their algebra and numerical consequences are to be checked; historical novelty is UNKNOWN. Kinetic fractionation, swing adsorption, time-dependent CDI, and diffusion-dependent ratchet sorting have clear predecessors. The derived operation is a scoped model comparison and obstruction to a proposed waveform-only rescue. It is not an enabled lithium-extraction technology or a civilization-scale result.
