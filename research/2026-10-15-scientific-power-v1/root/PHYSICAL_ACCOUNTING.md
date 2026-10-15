# Physical accounting before controller certification

Root working derivation, 15 October 2026. Internal reasoning; novelty and external validation UNKNOWN.

The promising guard construction must bound the amount of electronically conducting material beyond a physically complete cutset, not merely the electrical charge supplied by a charger. Let Omega be the region between that guard and the other electrode, with minimum slab separation d. If its Ohmic metal has scalar conductivity at most sigma_max, a Dirichlet trial potential z/d gives

    G_metal <= sigma_max V_metal / d^2.

The decision-control lead independently supplied this conductance inequality. The root's contribution below concerns what its physical accounting can and cannot imply.

## Exact local cancellation countermodel

Two surface patches have signed Faradaic currents +I and -I. The first deposits a conducting tip toward the far electrode; the second dissolves an equal volume of remote metal. The aggregate current and aggregate metal-volume derivative are both zero. The tip still advances. Spatially distinct electrochemical equilibrium potentials can support opposite current signs on an equipotential conductor. This is a countermodel to a net-current-only morphology or safety inference, not to an assay that independently resolves every patch or directly detects bridging.

Let a cylindrical tip have area A, density rho and molar mass M. If its deposition current is I and the reservoir contains enough metal, its advance is

    dx/dt = M I / (F rho A).

Equal remote dissolution holds total metal fixed while x reaches d in finite time. Metal already beyond the guard, mechanical transport of existing metal across it, chemical reduction and internally supplied electrochemical current are therefore separate terms in any downstream bound. A useful control volume ledger is

    V(t) = V(0) + V_advected(t) + V_chemically_formed(t)
           + (M/(F rho)) Q_net_electrochemical(t),

with sign conventions and losses stated. If one uses gross positive sources to obtain an upper bound, the bound can be conservative but cannot omit a source because it is unmeasured. Guard charge alone does not establish that ledger.

## Consequence of an actual conductance certificate

An ideal Thevenin source with voltage U and series resistance R feeding a metallic short of conductance G has

    I = U G/(1+R G),
    P_short = U^2 G/(1+R G)^2,
    P_total = U^2 G/(1+R G).

P_total is increasing in G, while P_short peaks at G=1/R. A low-resistance bridge can shift heating into the cell. Bounding bridge heating alone does not bound total heat. With justified bounds U<=Umax and G<=g throughout an interval T, the conservative total electrical heating bound is Umax^2 g T (or Umax^2 g T/(1+Rmin g) with a justified R>=Rmin). This does not bound heat from a chemically exothermic instability or a geometry-changing fracture.

These statements do not show the guard operation is feasible, useful or novel. In particular, a tiny sufficient residual-charge budget is not an impossibility theorem for every architecture. The guard lead and independent adversaries are checking physical scales, existing devices and all source terms.
