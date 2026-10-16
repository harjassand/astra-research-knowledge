# Native-boundary static-product obstruction

Let K={0,…,162}^8, B={0,…,15}^8, x0=(50,…,50), T=1. Birth and death rates at count n are b(n)=2.676 n(n−1)+108.102 and a(n)=.040 n(n−1)(n−2)+37.881 n; each directed grid edge transports at rate 8.2207 n_source. All decimal constants are exact rationals. A transition creating count 163 is killed.

Consider g(t,x)=exp(λ(1−t)+F(x)), F(x)=Σ_i φ_i(x_i), positive everywhere on K. Assume native g≥1 on B at every time and Q^kill exp(F)/exp(F)≤λ on K\B. Stopping at first target entry, overflow or deadline gives the standard upper bound g(0,x0) on pre-overflow first-hit probability.

If λ<0, replace λ by zero and F by F+λ. Initial value and generator ratio are unchanged; target feasibility follows from the original condition at time zero. Thus λ≥0 is without loss.

The certificate's coordinate ordering is column-wise: sites 0,1 in column 0; 2,3 in column 1; 4,5 in column 2; 6,7 in column 3. Map certificate indices to row-major physical indices by [0,4,1,5,2,6,3,7]. The two degree/orbit classes are corners and internal-column sites. Tensor contract files use row-major physical labels; these describe the same graph.

At a non-target state s, form q_s from every nonoverflow transition's change in additive log profiles, and let k_s be total overflow rate. By exp(z)≥1+z,

    Q^kill exp(F)(s)/exp(F(s)) ≥ q_s·φ − k_s.

The exact rational file has 324 positive weights π_s, mass m≈0.722505697953930<1 and killing charge δ≈2.667415387553021e−22<3e−22. With c selecting four copies of each orbit's count-50 coordinate, the complete 326-coordinate identity is

    c + Σ_s π_s q_s = 4 e_corner,15 + 4 e_inner,15.

For arbitrary site-specific profiles, average each weighted generator row over the four exact graph automorphisms (row swap and column reflection). The checker verifies directly the resulting 1,304-coordinate identity, whose surviving right side selects count 15 once at every site. Thus symmetry assumptions on the candidate, low-coordinate nonnegativity and a gauge choice are all unnecessary. Native target feasibility at time one gives F(all15)≥0. Summing the tangent inequalities therefore yields

    λ+F(x0) ≥ (1−m)λ+F(all15)−δ ≥ −δ.

Consequently g(0,x0)≥exp(−δ)>1−δ>1−3e−22. The strict elementary inequality uses δ>0. This is a lower bound on feasible upper envelopes, never on the actual first-hit probability.

Every certificate state is an actual non-target eight-site state; 15 rows have transitions into B and 2 have overflow. The exact checker reconstructs reaction/diffusion rows without importing discovery code, verifies all coordinates, rational positivity, mass and killing charge, and checks the certificate hash. Its standard-library arithmetic provides replay without numerical optimization tolerances.

A target-overwritten nonflat product changes the 15 target-entering rows. This theorem does not cover it. It also does not cover genuinely time-dependent profiles, pair-factor barriers or tensor states.
