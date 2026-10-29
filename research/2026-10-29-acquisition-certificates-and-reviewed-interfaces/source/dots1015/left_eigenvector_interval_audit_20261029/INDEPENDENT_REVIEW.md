# Receiving review: certified left-eigenvector coordinate recovery

2026-10-29. Accepted at the executed exact-instance interval-certificate scope. This review covers the LEFT_INTERVAL addendum, not the earlier uncertified modular coordinate identities.

## Governing argument

Every center is an exact integer matrix divided by 2^512. Original rational entries are rounded with entrywise error less than 1/S, hence induced infinity error at most n/S. Multiplication, scaling and addition radii are valid by submultiplicativity and a new n/S rounding allowance. Python arbitrary-precision integer object arithmetic does not incur machine-integer overflow. The centers may be numerically proposed, but their accuracy is not trusted.

For E=I−C_Q Q with norm r_Q<1, Q^-1=(I−E)^-1 C_Q and its norm is at most ||C_Q||/(1−r_Q). Consequently the exact residual QZ−N/4 bounds ||M_lambda−Z||. Transposition increases the infinity norm by at most n; the added root interval and diagonal rounding radii are valid. Replacing the normalization row cannot enlarge its uncertainty.

For the normalized eigenvector system, ||I−C_A A(lambda)||<1 proves invertibility uniformly over the entire certified root interval. With c=C_A b, the exact solution has ||w−c||≤r_A||c||/(1−r_A). The accepted reduced primitive quotient supplies an evaluation vector at the unique least-value stationary point, whose constant entry is one and which solves every eigenvector row. It therefore solves the normalized system. Uniqueness identifies it with the certified solution. The omitted eigenvector row is thus justified by existence, not assumed away or checked only numerically.

The coordinate indices 3,2,1 agree with the received standard-monomial basis entries x,y,z. The refined interval is replayed exactly from the earlier certified least-root isolating interval; no new assumption about which root is least is introduced.

## Independent execution

The author verifier was copied and replayed on frozen finder output. An independently written implementation using nested Python integer lists (no NumPy matrix products) reconstructed Q,N, both inverse residuals, transpose uncertainty and vector bound. All four exact rational bounds match. The evaluation-vector error is 3.633330976290955e−11. The root refinement, rational unit candidate, exact original objective and perturbation-adjusted gap were also checked. High-precision finder plus verifier was separately replayed in a copy; no author bytes changed.

The final quaternion conversion uses binary64 normalization only to choose a dyadic stereographic grid point. It is a finder, not a certified proximity-preserving rounding map. The resulting quaternion formula, norm and objective evaluation are exact, and its independent global gap check succeeds. Therefore this implementation detail does not weaken the accepted feasibility or gap result, but no extra rounding-proximity theorem is claimed.

The exact original-objective gap is 1.190011164703136e−5, below 1e−4. No local optimizer or reconstructed coordinate-polynomial identity is used by this route.

## Scope

This closes the missing constructive candidate step on the retained instance. It is not a universal condition-number bound, automatic fixed-precision solver or practical worst-case runtime theorem. Other instances may require increased interval precision and new verified inverses. Generic degeneracy handling, physical source timing and quantum controls remain separate. Failed binary64 recovery and interrupted direct root counting remain useful preserved failures; accepted prior root isolation is reused rather than incorrectly claiming the interrupted calculation completed.
