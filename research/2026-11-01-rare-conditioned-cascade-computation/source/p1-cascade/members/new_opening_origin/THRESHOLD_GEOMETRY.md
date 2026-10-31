# Cumulative-exposure cascades and the convex integration baseline

## Conclusion

Generic convex-volume or logconcave-density integration does not automatically supply the full proposed cascade operation. The success set can be nonconvex even for three sites, unit exposure rates, exponential thresholds, and moral treewidth two. A family with the same width and a single designated target requires exponentially many pieces in any exact convex cover. These are geometric obstructions to invoking particular existing algorithms, not lower bounds against every randomized integration method.

The convex subclass is a serious established baseline. For AND-precedence project networks, completion by T imposes linear inequalities on independent activity durations, one inequality per path. Their intersection is convex, with a membership oracle obtained from longest-path computation. For logconcave independent duration densities, conventional integration and sampling can already provide relative probabilities and conditioned drivers without imposing bounded treewidth, subject to their evaluation, initialization, rounding, and arithmetic conditions. The new candidate should not claim an advantage on this subclass merely because the target is rare.

## Primary sources and what they establish

* [Lovász and Vempala, Fast Algorithms for Logconcave Functions: Sampling, Rounding, Integration and Optimization](https://faculty.cc.gatech.edu/~vempala/papers/integration.pdf). Section 1.1 specifies density evaluation, spread/concentration, and starting-point conditions. Theorem 1.3 gives a relative integral approximation for a well-rounded logconcave function; the paper also provides sampling and rounding machinery. Its guarantee is not for arbitrary nonconvex supports.
* [Cousins and Vempala, Gaussian Cooling and O*(n³) Algorithms for Volume and Gaussian Volume](https://arxiv.org/abs/1409.6011). The stated volume algorithm concerns a well-rounded convex body given by a membership oracle. Its Gaussian integration result likewise restricts to convex sets. This provides a stronger conventional comparator where the geometry actually fits.
* [Bringmann and Friedrich, Approximating the volume of unions and intersections of high-dimensional geometric objects](https://people.mpi-inf.mpg.de/~kbringma/paper/2008ISAAC.pdf). A union-volume FPRAS is available for a supplied list of objects with membership, volume, and sampling oracles, even approximate ones. The number and representation of the objects are part of the input. Nonconvexity alone therefore does not rule out existing relative integration; a concise usable union representation must also be checked.
* [Streftaris and Gibson, Non-exponential tolerance to infection in epidemic systems—modeling, inference, and assessment, Biostatistics 13(4):580–593, 2012](https://academic.oup.com/biostatistics/article-abstract/13/4/580/241210). This paper explicitly generalizes exponential Sellke tolerance thresholds to Weibull thresholds and uses Bayesian MCMC inference. Weibull cumulative-exposure semantics is therefore established ancestry. The paper's stated operation is different from the proposed bounded-width, finite-error relative integration and conditional-path guarantee.
* [Chandrasekaran, Dadush, and Vempala, Thin Partitions: Isoperimetric Inequalities and a Sampling Algorithm for Star Shaped Bodies, SODA 2010](https://karthik.ise.illinois.edu/pubs/star-shaped.pdf). Sampling and volume estimation extend to star-shaped bodies, with inverse-polynomial dependence on the fraction of volume occupied by the visibility kernel, and additional geometric/oracle assumptions. The kernel fraction is not free for a downset.
* [Vempala and Wibisono, The Geometry of Efficient Nonconvex Sampling, COLT 2026](https://arxiv.org/html/2603.25622v2). Theorem 1 gives nonconvex uniform sampling under Poincaré and volume-growth conditions from an M-warm initial distribution. Its expected query bound is Õ(q C_PI α β² M n³ log⁴(1/ε)). These quantitative conditions are additional resources; merely being a downset or having fixed factor width does not supply them in the theorem.

The earlier `CASCADE_COMPARISON_AND_LIFT.md` records the especially close Ando deadline-shift/dilation algorithm and NPEDT event-time representation. Those comparisons remain relevant when exponential thresholds are replaced by Weibull thresholds.

## A three-site nonconvex success set

All sites start inactive. Site i activates once its accumulated exposure reaches a fixed realization e_i of its independent threshold. Let the exposure rates be

\[
a_1(x)=1,\qquad a_2(x)=1,\qquad
a_3(x)=\mathbf1\{x_1\lor x_2\}.
\]

These rates are monotone in active sites, finite, and locally depend on at most two parents. The first two activation times are e_1,e_2. Site 3 begins accumulating exposure at unit speed after the first parent activates, so

\[
\tau_3(e)=\min(e_1,e_2)+e_3.
\]

For target site 3 and T=1, the success region is

\[
\mathcal A=\{e>0:\min(e_1,e_2)+e_3\le1\}.
\]

It is a downset. But both

\[
u=(1/4,7/4,1/4),\qquad v=(7/4,1/4,1/4)
\]

succeed at time 1/2, whereas their midpoint (1,1,1/4) reaches the target only at 5/4. Hence the region is nonconvex. All inequalities are strict, so this is not a measure-zero boundary artifact.

To obtain a cyclic hazard graph, replace a_1 by 1+x_3. The new edge 3→1 creates the cycle 1→3→1. Before site 3 activates, its two parents retain the original rates, so the target time and the entire witness remain unchanged. The moral graph is the triangle {1,2,3}, of width two.

This geometric example does not depend on the threshold distribution. Weibull thresholds with any positive shape have positive density around the witness points. For shape k≥1, the Weibull density itself is logconcave:

\[
\log f_k(e)=\log k+(k-1)\log e-e^k,
\qquad
\frac{d^2}{de^2}\log f_k(e)
=-\frac{k-1}{e^2}-k(k-1)e^{k-2}\le0.
\]

Nevertheless the density multiplied by 1_A is not logconcave: it is positive at u,v and zero at their midpoint. Even unit exponential thresholds therefore defeat direct logconcave integration on the full success set. Shape k<1 does not restore the generic theorem; then the one-dimensional Weibull density is itself not logconcave.

## Uniformizing each threshold does not fix the example

For exponential thresholds, use independent uniform coordinates z_i=1−exp(−e_i). The target condition becomes

\[
\max(1-z_1,1-z_2)(1-z_3)\ge e^{-1}.
\]

The uniform-space points (0.1,0.99,0.5) and (0.99,0.1,0.5) satisfy this inequality because the product is 0.45. Their midpoint (0.545,0.545,0.5) fails because the product is 0.2275. Thus the routine coordinatewise probability integral transform does not turn the success region into a convex body either.

This does not rule out every nonlinear change of variables. It shows that such a change, together with a tractable transformed measure and oracles, would be an additional operation to earn.

## A width-two family requiring exponentially many convex pieces

Take m copies of the OR gadget above. First require success of every gadget's output. For each gadget choose either u or v from the witness pair. This gives 2^m successful threshold vectors. Any two distinct vectors differ in at least one gadget, and their midpoint fails that gadget. Therefore a convex subset of the full success region can contain at most one of these 2^m witnesses. Any exact union of convex subsets equal to the success region requires at least 2^m members.

This lower bound is about representation as an explicit convex union. It does not rule out a different succinct representation or an approximation that discards some portions of the region.

A single-target version keeps the same width. Let m=2^d and combine the gadget outputs through a complete binary AND tree. Each internal site has rate one once both parents activate and zero before that. For each witness vector, fix each internal threshold at h=1/(8 max(1,d)). Successful gadget outputs occur at time 1/2, so the root activates at 1/2+dh≤5/8. A midpoint of two distinct witness vectors has at least one gadget output at 5/4; AND precedence forces the root to activate after that and fail the deadline.

There are 4m−1 sites, indegree at most two, and a width-two moral decomposition: each OR or AND family is a bag containing its child and two parents; connect each tree-gate bag to the bags containing its two child outputs. The cyclic feedback factor is contained in its existing OR bag. Every node's bag occurrences are connected and every family scope lies in a bag.

Consequently even single-target, cyclic, width-two instances can require 2^m exact convex pieces. The generic explicit-union FPRAS cannot be applied by simply listing a polynomial number of convex pieces for every such instance.

`nonconvex_witness.py` implements a separate exact rational exposure simulator, constructs these instances and width certificates, and checks all witness pairs for m=1,2,4. The generated `nonconvex_witness_results.json` records target times and pair counts. It also checks the exponential-CDF uniformization example.

## The star-shaped kernel can occupy exponentially little volume

The same example permits an exact check of the older star-shaped sampling guarantee. In independent uniform coordinates after the exponential CDF transform, one OR gadget's body at deadline T is

\[
A_T=\{(u_1,u_2,z)\in[0,1]^3:0\le z\le1-e^{-T},\ \min(u_1,u_2)\le g_T(z)\},
\quad g_T(z)=1-\frac{e^{-T}}{1-z}.
\]

The function g_T is concave on its domain, so each of the two arms {u_i≤g_T(z)} is convex. Their intersection

\[
K_T=\{\max(u_1,u_2)\le g_T(z)\}
\]

is the body's visibility kernel. To prove the reverse containment, take a point of one arm outside the other. At the same height z, connect it to a point on the second arm's boundary whose first coordinate exceeds g_T(z). The segment eventually leaves the first arm while remaining outside the second until its endpoint. Such a point cannot be in the kernel.

Direct integration gives

\[
\operatorname{vol}(A_T)=(1-e^{-T})^2,\qquad
\operatorname{vol}(K_T)=1-2Te^{-T}-e^{-2T}.
\]

At T=1 the ratio is

\[
\eta=\frac{1-2e^{-1}-e^{-2}}{(1-e^{-1})^2}\approx0.3226.
\]

For m independent gadgets with the joint success query, the body is A_1^m and its kernel is K_1^m. The kernel fraction is η^m although the moral width remains two. Thus the inverse-kernel term in the 2010 theorem gives an exponential bound on this family. At small T, even one gadget has a kernel fraction asymptotic to 2T/3.

This does not prove that the 2026 nonconvex sampler is slow on the product family: Poincaré constants can behave well under products. It identifies the exact resource missing from the older theorem. A transfer of the newer theorem to the full cascade class would still have to establish suitable Poincaré and volume-growth bounds, construct a sufficiently warm start, and obtain the desired normalizing-constant guarantee. No such class-wide transfer was located in this search.

## Where the claimed extension should remain narrow

The credible distinction is a constructive guarantee for nonconvex success regions generated by monotone local exposure dynamics, when a small event-factor width has actually been acquired. Independent non-exponential threshold models, event-time encodings, generic rare-event MCMC, deadline dilation, and convex integration each have established precedents. The numerical and statistical contracts still need to account for unknown rates, known threshold-family parameters, zero support, factor arithmetic, and conditional sampling error.

The search did not locate a primary theorem already supplying that complete operation. It also did not establish that no such theorem exists. The nonconvex construction resolves one concrete potential shortcut and gives a useful family on which to compare the proposed method against conventional integration.
