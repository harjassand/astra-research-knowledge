# Exact finite-block code obstruction: preserved partial result

Reviewer/constructor: `/root/stopping_converse`  
Date: 21 October 2026  
Scope: fixed nonzero coherent perturbation \(V_s=\alpha U+i\beta I\), with \(\alpha\beta\ne0\), on the unchanged infinite port-labelled tree. No asymptotic capacity conclusion is drawn from this finite-block investigation.

## Exact analytic result: no nontrivial two-slot universal subspace code

There is no \(K\ge2\) exact two-forward-slot quantum subspace code that works for every bath initializer with one decoder. The conclusion already holds for any fixed faithful vertex-diagonal initializer, including the prescribed stationary \(\tau_\pi\). Logical-independent bath evolution is allowed; bath return is not required by the obstruction.

For a faithful diagonal initializer, the physical block Kraus family contains
\(\sqrt{\pi(v)}A_{w,v}\), where

\[
A_{w,v}=\langle w|V_{s,2}V_{s,1}|v\rangle.
\]

Every weight \(\pi(v)>0\), so scalar weights do not change the Knill--Laflamme conditions. A universally correctable subspace must in particular correct this channel. If a Kraus error restricted to a known ambient input subspace has rank one, then any exact code of dimension \(K\ge2\) within that ambient space lies in its kernel: the compressed positive operator has rank at most one but must equal a scalar times the \(K\)-dimensional identity, so that scalar is zero.

First apply this observation to geodesic two-step bath endpoints. Such an endpoint is at graph distance two from \(v\); reaching it requires both interactions to use the \(\alpha U\) term. The unique path fixes the input word, and its Kraus operator is a nonzero rank-one map \(\alpha^2|y\rangle\langle x|\).

- For input \(x=00\), start at depth at least two. Both steps go to ancestors, giving a geodesic.
- For input \(x=0a\), \(a\in\{1,2\}\), start at a vertex whose parent-edge color is \(c\ne a\). Popping and then pushing color \(a\) goes to a sibling along a geodesic.
- For input \(x=ab\), \(a,b\in\{1,2\}\), both steps push and form a geodesic.

Thus any \(K\ge2\) exact code must be orthogonal to these seven computational basis words. Its input subspace must lie inside

\[
\mathcal H_0=\operatorname{span}\{|10\rangle,|20\rangle\}.
\]

Now fix an ordinary sufficiently deep vertex \(v\) and its child \(va\), \(a\in\{1,2\}\). Its distance is one, so in two slots the only histories reaching it use one \(U\) and one idle term; histories with zero or two moves have the wrong parity. On the remaining subspace,

\[
A_{va,v}|b0\rangle=i\alpha\beta\,\delta_{ab}|00\rangle.
\]

Indeed, moving on the first slot pushes \(b\), while moving on the second slot would pop and reach the parent of \(v\), not its child. Hence each of the two child endpoint errors restricts to a nonzero rank-one map on \(\mathcal H_0\). Their kernels intersect trivially. There can be no \(K\ge2\) exact code.

All vertices used above are actual vertices of the infinite tree, with enough depth to avoid the special root in the specified paths. No finite-tree boundary or approximation is involved. The proof excludes arbitrary subspace encoders and arbitrary recovery maps satisfying exact quantum correction, not just the original two-word Dyck encoder. It also excludes a universal exact operator identity with logical-independent bath evolution, since such an identity would be an exact code for the faithful diagonal initializer.

The endpoints are essential: at \(\beta=0\), the original two-dimensional Dyck code works; at \(\alpha=0\), the device is identity up to phase and full port-rate coding works.

## Computational structural probes, with precise limits

The tree is represented exactly as two rooted binary trees joined by their port-0 root edge. A vertex is `(side, word)`, with `side` in `{0,1}` and `word` a finite word in `{1,2}`. Inputs 1 or 2 append that symbol and output 0; input 0 pops a nonempty word and outputs the popped symbol, or flips the side and outputs 0 at an empty word. This is an exact relabelling of the original infinite device.

`exact_code_system_probe.py` constructs actual finite-horizon Kraus matrices for a finite list of actual initial vertices, without truncating the later bath dynamics. At the rational unitary point \(\alpha=3/5,\beta=4/5\), common denominators can be suppressed. A Gaussian elimination certificate modulo the prime 1009 proves that the two-slot Kraus-product operator system has full complex dimension \(9^2=81\). The reason a modular full-rank result is conclusive is that a nonzero minor modulo a prime certifies a nonzero Gaussian-integer minor before reduction. The saved file includes the selected independent product indices.

The stronger symbolic two-slot argument above does not depend on this numerical choice or certificate. Its purpose was to identify and then prove a structural obstruction.

Three-slot probes did **not** close a new theorem. For the tested families, modular product-system ranks were 626 out of the possible 729, at both `(alpha,beta,prime)=(3,4,1009)` and `(12,5,1013)`. This is a lower bound on the exact operator-system dimension, not an exact rank upper bound. It cannot be used to claim either a code or its absence. It also warns against assuming that full two-slot confusability automatically tensors through a persistent bath.

`exact_code_peeling.py` implements the rank-one-kernel argument using exact rational nullspaces and integer operators. At two slots it reduces possible ambient dimensions `9 -> 2 -> 0`, matching the symbolic proof. At three slots the tested necessary-condition procedure stops at `27 -> 12 -> 8`; this is an **inconclusive method**, not an eight-dimensional exact code. It examines actual Kraus errors, not all possible linear combinations of them.

Saved outputs:

- `exact_system_n2.json`: full two-slot operator-system certificate at the rational point; approximately 0.0291 s.
- `exact_system_n3.json`: three-slot modular lower rank 626; approximately 0.404 s.
- `exact_system_n3_second.json`: separate three-slot parameter/prime check, lower rank 626; approximately 0.359 s.
- `exact_peeling_n2.json`: exact two-slot kernel peeling; approximately 0.00592 s.
- `exact_peeling_n3.json`: inconclusive three-slot kernel peeling; approximately 0.226 s.

These are process-body timings, not all-in research costs. Python, NumPy, and standard-library exact fractions were used; no package installation, outside compute service, or outreach was needed. The finite findings are not a historical-priority claim.

## State on handoff

The two-slot exact obstruction is proved for all \(\alpha\beta\ne0\). The existence or impossibility of nontrivial universally exact codes at arbitrary larger finite block lengths remains unresolved here. No all-\(n\) full-operator-system claim has been established. In particular, this result does not show asymptotic zero quantum capacity; approximate long-block codes already have independent positive lower bounds near the unperturbed point.

This operation is paused at the parent's request to challenge the more consequential universal compression/capacity-floor construction. Its source and failed larger-block shortcuts are preserved rather than promoted to a completed general obstruction.
