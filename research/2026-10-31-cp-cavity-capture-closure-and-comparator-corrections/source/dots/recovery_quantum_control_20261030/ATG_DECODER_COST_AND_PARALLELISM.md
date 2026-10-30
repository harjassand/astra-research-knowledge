# Actual ATG frame-computation cost and the remaining physical runtime gap
30 October2026. Algorithmic refinement, not a noisy classical-controller theorem.

## Source statement and exact task
The already-read primary paper Bergamaschi–Liu, arXiv:2411.04405v1 §1.1, footnote4, states that dynamic programming permits decoding in T exp(n) time; its efficient-decoding theorem needs an additional decoding premise. The protocol does NOT inherently require brute force over all O(nT) record bits.

Source: https://arxiv.org/html/2411.04405v1

## Explicit dynamic program
Fix one syndrome sector H with n columns and m=O(n) actual check rows, including dependent rows if present. Its measured variables are data records d_j in F2^n and check records c_j in F2^m. Internal metasyndrome constraints have the form

 H d_j + c_j + c_(j+1) = y_j.

The two ATG sectors partition the measured vertices, so their Hamming-weight minimizations separate. For a chain of L check-record layers define

 V_1(c)=|c|,
 V_(j+1)(c')=|c'|+min_{c,d: c'=c+Hd+y_j}[V_j(c)+|d|].

Minimize over final c'. Store predecessors and use a fixed lexicographic tie rule depending ONLY on the metasyndrome y. The initial and terminal check records are free variables; this is bulk minimum-weight inference, not a decoded boundary condition. Boundary parity conventions only alter the number of layers by one.

For each c, enumerate all 2^n values d and update the uniquely determined c'. This costs

 time O(T * 2^(m+n) * poly(n)),
 traceback storage O(T * 2^m * poly(n)).

Since the LDPC row count m<=C_ell n, the exponent is O(n), not O(nT). Keeping redundant rows avoids assuming row reduction preserves physical locality; redundancy changes only the fixed exponential coefficient. The DP is an algorithm on the classical record, not a physical nonlocal decoder inserted into quantum dynamics.

After beta is found, evaluate the boundary-check and encoded-Bell sign parities of m+beta and solve their fixed binary symplectic equations for P(m). A precomputed right inverse makes this step polynomial in n,T. Its Pauli representative need NOT be minimum weight; the source certificate permits any fixed solution consistent with those signs. Frame delivery/application is a separate physical action.

## Runtime versus quantum lifetime
Write the serial time as poly(n,T) exp(c_dec n), and a proved quantum storage horizon as exp(c_mem n) up to prefactors. These constants are not interchangeable. Unless c_dec<c_mem, increasing n does not make serial decoding fit. In particular 'both are exponential' is not a receiving proof. Our source/capture composition grants no such comparison.

## Explicit parallel alternative and its limits
All transitions for each layer can be evaluated in parallel. For each next state c', reduce candidate costs with a balanced min/comparison tree, retaining a deterministic predecessor. Additions, comparisons, tie handling and input copies have bounded-fanin Boolean implementations. Sequentially process O(T) layers, or use a more parallel min-plus composition if desired. Conservative bounds suffice:

 circuit size exp(O(n))*poly(n,T),
 circuit depth poly(n,T),
 bounded fanout achieved with explicit copy trees of depth O(n+log T).

At n=Theta(log(L/epsilon)) and T=Theta(n), this is polynomial hardware in L/epsilon with polynomial-logarithmic ideal depth. It is a concrete noiseless circuit alternative to the bad serial-exponent comparison, not an exponentially fast black box.

Actual reliable evaluation on that large circuit, capture-port fanout/read noise, bounded-degree routing, scheduled/autonomous activation, and protected delivery of P(m') to quantum DATA remain unproved here. One cannot simply fan out a noisy physical root to exponentially many processors and call their inputs trustworthy. The final frame is still an analysis frame until those interfaces are built. Existing reliable-classical machinery may be a candidate implementation, but its actual resource and noise contract must be checked.
