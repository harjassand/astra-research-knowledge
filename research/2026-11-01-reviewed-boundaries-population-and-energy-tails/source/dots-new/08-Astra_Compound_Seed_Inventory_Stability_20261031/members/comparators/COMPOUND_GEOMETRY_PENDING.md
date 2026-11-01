# Pending mechanism check: complete-bipartite compound inventory

This is an independent algebra check only, **not** acceptance of the parent's new Lyapunov theorem or raw-list finder. The earlier source/no-go note remains unchanged.

Let the A-free hub graph be a disjoint union of complete bipartite components with sides L_s,D_s, using the same symbols for summed counts. Let z=Σ_s min(L_s,D_s), R=A+z, and N be total count. Species not in any hub component are permitted as arm species. Each hub edge is reversible with 2A; arm edges are reversible between a hub and A+X. Each X has total forward capture constant k_X, with k_min>0 and k_max=max k_X.

For an arm capture A+X→hub, deleting X before adding one particle to each side of the destination component shows ΔR is 0 or -1. It is 0 whenever X lies on a strictly larger side of its component, or outside all hub components. Thus the total count of definitely neutral arm species is at least

    N-A-2z = N-2R+A.

Indeed each larger-side total dominates the absolute side difference. At equal sides neither side is guaranteed neutral and their total is exactly twice the minimum. The bad-capture species mass is at most 2z. Hence

    neutral_capture_rate >= k_min A(N-2R+A),
    bad_capture_rate <= 2 k_max A z.

Adding all 2A→hub rates bounds the total R-decreasing forward rate by

    [Σ_h a_h + 2 k_max] A R.

At R=1, a hub capture cannot decrease R: A=1 and every side minimum is zero, so an enabled consumed satellite cannot be on a positive smaller side. The 2A channel requires R>=2. Thus internal dynamics preserve positivity of R, and R=0 disables every internal source.

Completeness, not merely bipartiteness, yields the exact source-rate identity

    Σ_hub_edges x_i x_j = Σ_s L_s D_s
                              >= Σ_s min(L_s,D_s)^2
                              >= z^2/k.

Consequently hub→2A rates are at least b_min z²/k. Removing an edge from a component destroys the first equality and may allow both side totals positive with no active hub source; completeness is a substantive guard.

For f=A/(R+1)^2, a neutral forward arm jump has exactly Δf=-1/(R+1)^2. Every internal jump has |ΔA|<=2 and |ΔR|<=1; if R decreases it starts at R>=2. These facts imply the deliberately loose bound

    |Δf| <= 11/(R+1)^2.

Reverse-neutral arm jumps can have positive Δf while their g(R) increment is zero. They therefore cannot be dropped or paid by their own g-drift. They can be compared source-by-source with the hub→2A rate from the identical hub complex, so reserving part of that negative g-drift may pay them when N is large. The constants and all regime joins in that argument remain for the full theorem audit.

The accompanying finite tests inspect two specified geometries only (a K2,2 component with an outside satellite, and two disjoint K1,1 components with an outside satellite). Supplying these partitions to a geometry test is not a replacement for acquisition by the candidate raw-list receiver, which remains unaudited.
