# Any classical channel: a qubit reference cannot exceed the ordinary coefficient

24 October 2026. Root sphere-integral construction, with independent verification of the load-bearing modified-prior step. No historical priority claim is made. This theorem concerns qubit reference dimension, not arbitrary-dimensional quantum references.

Let K be any finite classical channel. Let eta(K) be its global ordinary relative-entropy contraction coefficient, equivalently its global classical chi-square contraction coefficient. The equivalence can be obtained by the standard local-metric and line-segment integration characterization; the scalar proof below only requires an upper bound on all classical chi-square pair ratios.

For every cq ensemble with a qubit reference R and X→Y given by K,

I(Y:R)≤eta(K) I(X:R).                              (1)

In fact the supremum over such ensembles equals eta(K), because a classical binary reference already realizes the ordinary global coefficient as a rare-message limit.

## 1. Scalar reciprocal Jensen gaps are classical pair divergences

Fix a prior p_x and positive scalars u_x. Put u_bar=Σ_x p_xu_x and define a second probability distribution

q_x=p_xu_x/u_bar.

With classical chi-square convention chi²(p||q)=Σ_x p_x²/q_x−1,

chi²(p||q)=u_bar[Σ_x p_x/u_x−1/u_bar].            (2)

At the output, q_y=p_y E[u_X|Y=y]/u_bar, where p_y=(Kp)_y. Consequently

chi²(Kp||Kq)=u_bar[Σ_y p_y/E[u_X|Y=y]−1/u_bar].  (3)

Zero-probability symbols are omitted. Therefore every reciprocal Jensen-gap contraction is bounded by the global classical coefficient eta(K). The changed denominator distribution q is essential; no fixed-prior contraction identity is claimed.

For real z_x∈[−1,1] and 0<t<1, set u_x=1−tz_x. The identity

z²/(1−tz)=t^−2[(1−tz)^−1−1−tz]

shows that its Jensen gaps have the same bound, since affine terms cancel. The same holds for 1+tz. At t=0 the quadratic Jensen gap is a variance and is covered either directly or by continuity. Averaging the two signs proves the bound for

f_t(z)=z²/(1−t²z²).

Every f_t is convex, being the average of two convex scalar resolvents plus affine terms.

## 2. Exact sphere representation of qubit entropy

Define the entropy deficit

F(r)=((1+r)log(1+r)+(1−r)log(1−r))/2,

so a qubit with Bloch vector v has S=log 2−F(|v|). Put phi(z)=F(z)+zF'(z). For |z|<1,

phi(z)=Σ_{k≥1} [(2k+1)/(2k(2k−1))] z^{2k}
      =∫_0^1 (2−t) z²/(1−t²z²) dt.             (4)

The coefficient identity follows from integrating (2−t)t^{2k−2}. If n is uniform on the unit sphere in R³, then E[(n·v)^{2k}]=|v|^{2k}/(2k+1). Hence

F(|v|)=E_n phi(n·v).                              (5)

Both representations extend to |v|=1 by monotone convergence. Although phi itself diverges at z=±1, those endpoints occupy measure zero on the sphere; the integrated value F(1)=log 2 remains finite.

## 3. Apply the scalar inequality inside both positive integrals

Write v_x for the input conditional Bloch vectors and v_y=E[v_X|Y=y] for the output vectors. The average v_bar is unchanged. Then

I(X:R)=Σ_x p_xF(|v_x|)−F(|v_bar|)
      =E_n ∫_0^1 (2−t)[E_x f_t(n·v_x)−f_t(n·v_bar)]dt.

The analogous expression holds for I(Y:R), replacing v_x by v_y. Each bracket is a nonnegative scalar Jensen gap. Equations (2)–(3) bound the output bracket by eta(K) times the input bracket, for every direction and every t<1. Integrate to obtain (1).

For complete endpoint rigor, first integrate t over [0,1−δ], where every scalar resolvent is bounded. Then take δ down to zero. Tonelli and monotone convergence apply to the nonnegative Jensen-gap integrands. This avoids subtracting divergent endpoint integrals.

## 4. Matching lower bound and scope

Given any pair of classical input distributions r,s with finite positive D(r||s), let a binary variable U have probability ε of selecting r and probability 1−ε of selecting s. As ε decreases to zero,

I(U:X)=ε D(r||s)+o(ε),
I(U:Y)=ε D(Kr||Ks)+o(ε).

Encode U in the two orthogonal basis states of a reference qubit. Optimizing the input pair proves the matching supremum eta(K). Support issues can be handled by faithful classical regularization.

Thus arbitrary noncommuting qubit reference states offer no improvement over the global classical coefficient for any finite classical transmitted channel. This does not assert equality at each fixed input prior, and does not settle quantum references of dimension three or larger. In particular it does not conflict with a fixed-prior matrix-entropy comparison problem or with the previously proved complete/conditional advantages.

## 5. Arbitrarily many classical flags and at-most-qubit blocks

The same bound holds whenever the reference algebra is a direct sum of matrix blocks of dimension at most two. Write the reference as a classical block flag J and a conditional quantum system Q of dimension at most two. There may be arbitrarily many finite blocks, and the block probabilities may depend on X.

The chain rule gives

I(X:JQ)=I(X:J)+Σ_j p_j I(X:Q|J=j),
I(Y:JQ)=I(Y:J)+Σ_j p_j I(Y:Q|J=j).

The classical term contracts by eta(K). Conditional on each flag j, the transmitted channel is still K, with a possibly different input prior; the qubit result applies because its bound is global over priors. Applying it blockwise and summing proves the same eta(K) upper bound for the entire reference algebra.

Consequently, any single-ensemble quantum-reference MI advantage for a classical channel, if one exists, must use a reference state family whose generated algebra has an irreducible block of dimension at least three. This is not an existence assertion at dimension three and is separate from complete/conditional two-state advantages.

## 6. Fixed-prior warning

The scalar reciprocal reduction changes p to q_x=p_x(1−tz_x)/E_p(1−tz_X), depending on the ensemble, sphere direction, and integral parameter. Replacing the global eta(K) by a coefficient attached to the original prior p is therefore unsupported. The result does not resolve the fixed-source matrix t log t entropy separation question merely by specializing to a qubit reference.

## 7. Arbitrary positive 2-by-2 matrix test functions

There is also a direct normalization argument that does not add a third reference dimension. Let B_x≥0 be arbitrary 2-by-2 matrices, b_x=Tr B_x, b_bar=Σ_x p_x b_x>0, q_x=p_x b_x/b_bar, and rho_x=B_x/b_x on nonzero-trace symbols. The matrix t log t Jensen gap decomposes exactly as

Σ_x p_x Tr(B_x log B_x)−Tr(B_bar log B_bar)
=b_bar D(q||p)+b_bar χ(q,{rho_x}).

At the output the same decomposition has qK,pK and the posterior qubit states obtained from the prior q and channel K. The first term contracts by the global classical KL coefficient; the second contracts by the normalized-qubit theorem proved above. Thus every positive 2-by-2 matrix t log t test function also contracts by eta(K).

Symbols with b_x=0 have q_x=0 and are omitted from the normalized ensemble. Because q is supported on p, the classical divergence is well defined. This still does not justify using a fixed-original-prior scalar SDPI coefficient: q generally differs from p.
