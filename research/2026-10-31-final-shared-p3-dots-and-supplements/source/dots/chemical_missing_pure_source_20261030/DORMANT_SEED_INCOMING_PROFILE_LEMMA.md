# Incoming A profile through the non-small dormant Green
Status: personal local derivation, unreviewed. This is NOT the missing full exponential-residual interface.

On D=0 in the dormant test, the actual process until D seeding is the reference connector with killing/seed intensity k_seed(A)_m(B)_q. The seed output decreases A by1; connector clearing decreases A by m; immigration and activation increase A. The frozen reservoir C has no effect on these rates. Let f_s(A)=(1+A)^-s, s>0 fixed.

For large A, the only positive connector contribution to f_s is clearing, and

    f_s(A-m)-f_s(A)<=C_s f_s(A)/A.

Meanwhile seed output satisfies f_s(A-1)<=[1+C_s/A]f_s(A). For F=D_s f_s, the killed generator plus actual seed terminal reward obeys

    K F + k_seed(A)_m(B)_q f_s(A-1)
      <=(A)_m(B)_q f_s(A)
          [D_s k_D C_s/A-D_s k_seed+k_seed(1+C_s/A)].

Choose A_star sufficiently large (depending on the fixed rates and s), then D_s>=2. The bracket is negative on A>A_star. Immigration and activation only decrease F, so no competing contribution has been dropped with the wrong sign. The inequality also holds when B<q: clearing and seed are disabled, and the remaining F drift is nonpositive.

Stop at seeding or the first entrance into A<=A_star. Such an entrance by a clearing lies in a fixed finite band; enlarge D_s so F>=1 on that band. Any subsequent seed output has f_s<=1, irrespective of the now-observed low A or B. The exact product-form/marked-clearing comparator earns eventual seeding from each finite state, so this continuation is legitimate. Stopped Dynkin and the boundary reward comparison yield

    E[f_s(A_seed)]<=C_s f_s(A_initial)

uniformly in arbitrary initial A,B and frozen C. For initially A<=A_star the same estimate follows immediately from f_s(A_seed)<=1 and the positive lower bound on f_s(A_initial).

Thus a NON-small dormant return block can preserve an incoming reserve profile without fast mixing, a vanishing lifetime, or a vanishing bad-return mass. Its proof uses the seed/clearing shared monomial and a real low-A boundary value, not a fictitious pointwise drift sign at every state.

What remains: coupling this unweighted profile with the exponential residual tilt and its actual running cost, then coupling the outgoing seeded-face kernel to the opposite large-D face. Separate finiteness of all output moments and unweighted profile transport does not automatically give a uniform SAME-exponent weighted norm. That interface is not assumed here.
