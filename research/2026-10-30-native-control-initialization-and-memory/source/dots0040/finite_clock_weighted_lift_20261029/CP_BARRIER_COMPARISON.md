# Per-animal barrier comparison under the finite-depth CP dressing

Let T be the fixed-depth circuit in the geometric-blocker construction. For a partial circuit S, the local Stinespring orbit lemma gives, for every local HP identity-annihilating generator M_Z,
±M_Z S(f_A)<=C ||M_Z||_cb S(f_A)
when its causal cone meets A, and zero otherwise. Constants are uniform over partial gate times in a compact bounded interval: support/depth and local dimensions are fixed, and Stinespring dilations stay local.

Turn on one layer continuously, keeping earlier layers fixed. If its generator is sum over disjoint local Z_h, only C'|A| causal cones contribute. The evolving positive animal F_A(s) obeys
-C''|A| F_A(s)<=dF_A(s)/ds<=C''|A|F_A(s).
Ordinary operator-order Gronwall (integrating the rescaled derivative) yields e^{-C''t|A|} bounds for that layer. Iterate over the fixed number of layers:
e^{-C_T t|A|} f_A<=T(f_A)<=e^{C_T t|A|} f_A.
No CP ordering T>=c Id is asserted.

Hence T(V_a)>=V_{a-C_T t} and T(V_a)<=V_{a+C_T t}, with the same theta. Pick t additionally small enough that shifted exponent a-C_Tt retains the established dense-boundary margin and a+C_Tt retains whatever summability margin is needed. This is compatible with the previous choices because t can be arbitrarily small but fixed.

Use a raw SYNDROME-diagonal low-potential basin, not a spectral cutoff of noncommuting T(V). Each SSF channel only decreases the raw potential, and clock factors do not change data. Thus every CP circuit factor preserves that basin in the Schrodinger picture. Moreover T(V) remains data-syndrome-diagonal (with operator-valued clock coefficients), so its barrier projector commutes with it when the projector is a function of the raw syndrome. This permits the original killed-basin argument without introducing nonlocal spectral projectors of the dressed clock/data observable.
