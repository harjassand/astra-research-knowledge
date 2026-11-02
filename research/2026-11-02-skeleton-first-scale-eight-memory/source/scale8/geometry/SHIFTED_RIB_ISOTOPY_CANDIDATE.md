# Explicit globally compatible shifted-rib isotopy candidate

The two sheet restrictions differ: original compatible ribs are at coordinates4,5 modulo8, while copied-sheet preimages are at3,4. A globally compatible candidate is a periodic coordinate warp, rather than independently choosing edge-marker permutations.

On [0,8], let h be monotone piecewise-linear through

    (0,0), (2.5,2.5), (4,3), (5,4), (5.5,5.5), (8,8),

and extend h(t+8)=h(t)+8. Let H(x,y,z)=(h(x),h(y),h(z)).

Then:

* h fixes [0,2.5] and[5.5,8] modulo8, hence fixes coordinates0,±2 and the corresponding narrow normal neighborhoods;
* h(4)=3 and h(5)=4, so it has the required rib-marker action;
* slopes lie between1/3 and3, displacement is at most1 per coordinate;
* H_s=(1−s)id+sH is an ambient isotopy with the same uniform bi-Lipschitz bounds;
* all ordinary grid subdivision changes can be resolved by a common subdivision of uniformly bounded size.

This is not yet a proved automorphism/isotopy of the ACTUAL abstract refined complex. The precise missing geometric check is: each abstract page and its inherited sheaf incidences must be product-like in the open middle coordinate slabs(2.5,5.5), so the warp preserves that page while only moving its ordinary subdivision. The source's perturbation planes0,±2 and bounded boxed regions make this a plausible and finite gadget-atlas check. Plane support alone, without page-boundary/attachment invariance, is not logically sufficient.

If that check passes, the warp acts compatibly on shared old edges automatically, fixes the complicated narrow boundary features transversely, and provides the desired bounded common-subdivision chain map q and prism homotopy t satisfying

    r_b q + r_a = d_R t + t d_A.

The corrected diagonal lift is then J(x)=(x,qx,tx), not the unverified (x,x,0). This statement also requires that the warp be lifted on parent-ID abstract cells; ambient coordinate coincidence must not identify free-cross sheets.
