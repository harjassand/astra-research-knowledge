# A local criterion for reference-uniform channel order

## 1. Inputs and consequence

Let P and Q be finite classical channels on the same n-letter input. We use output-by-input matrices: entries are nonnegative and every column sums to one. Remove identically zero output rows. Assume every remaining output row of BOTH channels has at most two positive entries. The input alphabet, output counts, support graph, and number of overlapping cycles are unrestricted.

For an unordered pair e={i,j}, oriented by i<j, an output row supported exactly on e has coefficients (a,b)>0. Define

    k_e(t) = sum_(Q rows on e) ab/(a+bt)
             - sum_(P rows on e) ab/(a+bt),      t>0.                 (1)

An empty sum is zero. Singleton rows do not enter (1).

**Theorem 1.** The following statements are equivalent:

1. Every k_e is nonnegative on (0,infinity).
2. For every finite real or complex Hilbert space, every positive definite selfadjoint operator A_i on that space, and every vector x_i,

       sum_y <sum_i P_yi x_i, (sum_i P_yi A_i)^-1 sum_i P_yi x_i>
       >= the corresponding sum for Q.                              (2)

3. P dominates Q in ordinary classical less-noisy / relative-entropy order.
4. P dominates Q in complete SLD order, allowing every finite untouched quantum reference, every faithful baseline, and every traceless Hermitian tangent.
5. P dominates Q in unrestricted complete Umegaki relative-entropy order: all finite references and all input-state pairs, with NO equal-reference-marginal restriction.

In fact (1) also implies comparison of every operator-convex Petz f-divergence and the associated resolvent quadratic forms after every finite reference. No stochastic postprocessing map is asserted.

The equivalence of 4 and 5 for arbitrary channels is an accepted programme input, N675 Theorem 1.2(2), source lines101–125 and172 onward. We prove the structured reduction, including the stronger operator statement (2), rather than re-auditing N675. The source snapshot is pinned at ad7ff1b9d15a774d4b4d8362314c7070cac030e5 / input5788b347..., subsequently historical after a later refresh failed. The packet's explicit human programme-acceptance notice governs its older source-history labels.

This theorem supplies an exact finite operation on a class with unbounded input dimension and outcome counts. It does not provide a reference cutoff or an algorithm for generic inputs covered by N675.

## 2. The two-operator identity

For A,B>0, vectors x,y, and scalars a,b>0, set

    L_ab = a<x,A^-1x> + b<y,B^-1y>
           - <ax+by,(aA+bB)^-1(ax+by)>.

Whiten A: T=A^-1/2 B A^-1/2, u=A^-1/2x, v=A^-1/2y. The spectral theorem applies to the SINGLE positive operator T; no simultaneous diagonalization of A and B is used. On a spectral subspace with eigenvalue t>0,

    L_ab = ab/(a+bt) * |sqrt(t) u - v/sqrt(t)|^2.       (3)

Equivalently, its 2-by-2 matrix is ab/(a+bt) times [[t,-1],[-1,1/t]]. Expanding both sides proves (3). The same identity holds for spectral integrals on an infinite-dimensional space if the inverses are bounded, although Theorem1 only needs finite spaces.

Column stochasticity gives the exact row-loss decomposition

    sum_i <x_i,A_i^-1x_i> - output_quadratic(P)
      = sum_(pair rows of P) L_ab(A_i,A_j;x_i,x_j).       (4)

A singleton row contributes zero. Subtract (4) for P and Q and apply (3) separately to every input pair. Nonnegativity of k_e at every spectral value proves 1=>2. This permits arbitrary overlap of the pairs.

## 3. Classical necessity isolates one pair

Take scalar A_i=p_i>0 and x_i=h_i=p_i f_i. The loss contributed by a pair row is

    ab p_i p_j/(a p_i+b p_j) * (f_i-f_j)^2.             (5)

Suppose k_{ij}(t)<0 at some t>0. Before normalization, take input masses p_i=1, p_j=t, and p_l=epsilon for all other letters. Choose f_i=1 and every other f_l=0. Divide p by Z=1+t+(n-2)epsilon, subtract the p-weighted mean from f, and let h_l=p_l f_l. Then sum_l h_l=0; centering f changes no pair differences.

By (5), as epsilon decreases to zero the gap g_P-g_Q tends to

    t/(1+t) * k_{ij}(t) < 0.                          (6)

Every other incident-edge contribution is O(epsilon), and nonincident ones vanish for this f. Thus a faithful classical finite witness exists. If the channel entries and t are rational, taking epsilon=2^-r and evaluating the gap exactly eventually returns a rational witness. A negative value at any real t has a negative rational neighbour by continuity.

Consequently ordinary Fisher comparison implies1. Ordinary less-noisy comparison implies Fisher comparison by the local relative-entropy expansion. Conversely the ordinary Fisher matrices compare under1 by (2), so ordinary less-noisy order follows, for example from Makur–Polyanskiy Theorem1/Proposition8 (or integration along a line segment). This is 1<=>3. Classical witnesses also prove2=>1 and4=>1.

## 4. Quantum references and divergence scope

A classical channel acts after dephasing its input alphabet. For an arbitrary reference R and a faithful input state rho, write S_i=rho_ii>0 for its diagonal reference blocks and X_i=H_ii for tangent blocks. Off-diagonal input blocks never enter either output. On the real Hilbert space of Hermitian reference operators let A_i=J_{S_i}, J_S(X)=(SX+XS)/2. Each A_i is positive definite and linear in S_i. The complete SLD output is exactly the quadratic in (2), with x_i=X_i. Therefore1=>4 without a restriction on dimR, trace of individual X_i, or equality of reference marginals. The accepted N675 equivalence gives4<=>5. The reference-free special case gives5=>3.

There is also a direct resolvent formulation. For positive definite reference-block pairs rho_i,sigma_i and s>0, put A_i=L_{rho_i}+s R_{sigma_i} on complex Hilbert–Schmidt space and x_i=rho_i-sigma_i. These are arbitrary positive operators of the form allowed by (2), and the output quadratic is the Petz divergence for f_s(z)=(z-1)^2/(z+s). Positive integral representations, their quadratic endpoint, and common faithful regularization give the stated operator-convex Petz comparisons, including Umegaki. The affine parts cancel for states. This is not a claim for arbitrary scalar convex f.

## 5. Exact finite compiler and failure receiver

For rational input, aggregate terms with the same positive pole r=a/b:

    ab/(a+bt) = a/(t+r).

For each pair e, clear the product of its distinct (t+r) denominators, which is strictly positive on t>0. The criterion becomes nonnegativity of one rational polynomial p_e. Cancel common factors if desired. An identically zero p_e passes. Otherwise divide off a power of t and inspect its first nonzero coefficient: this is the sign near0. Square-free factorization over Q and Sturm variation counts decide whether any positive root has odd multiplicity. A polynomial is nonnegative on (0,infinity) exactly when its sign near0 is positive and all positive roots have even multiplicity.

Thus there is a terminating exact decision algorithm with no reference-dimension search or SDP hierarchy. Degree is at most the number of distinct pair-row poles minus1. Ordinary rational polynomial arithmetic, gcd, and univariate root isolation are charged; standard polynomial-time bit algorithms can implement these operations. The delivered SymPy-based implementation records exact square-free factors/Sturm sequences and measured costs; no optimized asymptotic implementation or universal numerical conditioning claim is made.

If a polynomial fails, rational isolating intervals supply a negative rational t, followed by the dyadic-epsilon witness of Section3. Its witness bit length depends on the actual negative margin and other row coefficients. The implementation does not claim a uniform small classical witness beyond this constructive termination argument.

The compiler needs the actual rational row coefficients and their exact pair supports. Inferring those from noisy observations, discovering a latent primitive measurement, robust leakage outside the support model, and physical controls are separate unpaid inputs.

## 6. Synthesis on every finite support graph

There is a broader exact LOCAL-EDIT version. Rows proportional to the same nonnegative input vector can first be merged, since the quadratic perspective and quantum divergences are positively homogeneous. Cancel any equal row-ray mass between P and Q. Arbitrarily dense common rows are allowed. If every uncancelled row has support at most two, Theorem1 still applies and is exact: the residual channels have equal (possibly subunit) column masses, so those weighted input terms cancel in (4); common rows cancel directly in (2). The necessity argument is unchanged. Thus a supplied arbitrary readout can retain its dense background while undergoing a pair-local edit. Unmatched higher-arity rows return OUTSIDE_CLASS rather than a guessed order. Discovering such an exact decomposition from imprecise data remains unpaid.

Let G be ANY finite simple graph. Assign each edge a positive rational weight w_e with sum_(e incident i)w_e<=1 for every vertex i. On each edge, define a flagged BEC fragment P with erasure e_e and a flagged BSC fragment Q with crossover d_e:

    P rows: w_e(1-e_e)(1,0), w_e(1-e_e)(0,1), w_e e_e(1,1);
    Q rows: w_e(1-d_e,d_e), w_e(d_e,1-d_e).

Add the same singleton filler 1-sum_incident w_e to both channels. Zero filler rows are discarded. For 0<d<1/2, direct algebra gives

    k_e(t)/w_e
      = [4d(1-d)-e]/(1+t)
        + d(1-d)(1-2d)^2(t-1)^2 /
          [(1+t)(1-d+dt)(d+(1-d)t)].                   (7)

Therefore complete order holds exactly when e_e<=4d_e(1-d_e) on every edge. Necessity is evaluation at t=1. The criterion is edge-local even though incident edges share input symbols.

For ANY edge with e_e>2d_e, Q cannot be a stochastic postprocessing of P. Its P-erasure row has mass w_e e_e on both endpoints. Because all entries are nonnegative, it can only be routed to Q rows containing BOTH endpoints. These are exactly the two Q rows on that edge. Their total common endpoint capacity is sum_y min(Q_yi,Q_yj)=2w_e d_e. Column stochasticity of a proposed postprocessor would require w_e e_e<=2w_e d_e, a contradiction. Extra edges and singleton fillers do not repair it.

Thus the open parameter region 2d_e<e_e<4d_e(1-d_e) synthesizes all-reference entropy-dominating channels without a postprocessor on every nonempty graph. The BEC/BSC binary order and its separation from degradation are established ordinary ingredients; the claimed reusable result here is the support-localization theorem, whose worldwide priority remains UNKNOWN.

## 7. Strictly positive noncommuting quantum measurements

Let M_i be any common POVM. Define E_y=sum_i P_yi M_i and F_z=sum_i Q_zi M_i. Precomposition of both ordered channels with M preserves complete SLD and relative-entropy order, by their definitions. If all M_i>0, every nonzero row gives a strictly positive effect. If the M_i are linearly independent, an identity F=T E with stochastic T would imply Q=T P coefficientwise, so the nondegradation witness survives.

For the executed four-letter path use edge weights1/4, e=3/10, d=1/10. Let sigma=(sigma_x,sigma_y,sigma_z), and let s_0=(1,1,1), s_1=(1,-1,-1), s_2=(-1,1,-1), s_3=(-1,-1,1). Set

    M_i=I/4+(s_i dot sigma)/16.

These four rational-complex Hermitian effects sum to I, are linearly independent, and each has minimum eigenvalue (4-sqrt3)/16>1/8. They do not commute. The synthesized P has13 outputs and Q10; E and F are strictly positive rational-complex POVMs. Their complete order follows from (7), and no classical output postprocessing exists. A quantum channel on classical measurement outputs is a stochastic postprocessor for these purposes, so allowing a general CPTP map does not repair simulation.

The output SLD/relative-entropy order is an information order, NOT universal predictive utility. This distinction is executable on the SAME qubit source. Put Delta=(sigma_y+sigma_z)/4 and rho_+=I/2+Delta, rho_-=I/2-Delta, each with prior1/2. Both states are faithful. Their primitive signed probabilities are (1,-1,0,0)/16. Exact optimal binary guessing succeeds with probabilities357/640 under E and179/320 under F; F is better by1/640 despite E's complete relative-entropy dominance. The receiver computes these probabilities by absolute values of exact rational measurement scores, with no optimization oracle. This is an explicit instance of the established Blackwell/less-noisy distinction, not a new decision-order theorem.

## 8. What survives the universal boundary

The positive construction is a dimension-uniform STRUCTURAL reduction and synthesis rule. It turns an arbitrary overlapping pair-support graph into finitely many scalar rational inequalities and exports them through a supplied noncommuting primitive measurement. The ordinary same-information comparator can reproduce the classical half using Makur–Polyanskiy's Hessian criterion and can reproduce the binary spectral step using established positive-pencil calculus. A generic bounded-reference numerical search is therefore not the strongest comparator. No overall speed superiority over a source-aware implementation of those methods has been established.

The structure is load-bearing. Comparing a general n-letter channel with an erasure channel introduces a GLOBAL row supported on all n inputs; for n>=3 that falls outside the pair-support theorem. In particular the theorem does not contradict known quantum-reference activation of contraction coefficients for classical channels whose own rows are pair-supported. Nor does a common POVM decomposition automatically exist or become efficiently discoverable from an arbitrary strictly positive pair.

The exact guessing reversal is also a capability boundary: complete entropy order alone cannot supply an all-loss decision replacement. An operational use must specify its objective (relative-entropy distinguishability, a stated capacity consequence, or a decision loss). Substantial physical/economic reach and historical novelty are not established by this theorem or its finite example.
