# A feasible noncommuting binary-POVM coherent-branch rounding

28 October 2026. Author proof and finite checks; independent receiving pending. This is an actual positive-cost rounding for the off-diagonal branch of a binary POVM. It is NOT a complete binary-POVM oracle, a full-CPTP decoder oracle, or an improved physical acquisition theorem. The one-sided diagonal-effect branches remain open.

## 1. The cost decomposition and an exact rational effect completion

Let the known Hilbert space be H_- direct-sum H_+, of dimensions a,b>=1 and d=a+b. Write a binary effect and its positive affine cost as

    0<=E<=I,  E=[[I-A,B],[B*,D]],
    u(E)=m+Tr(W_- A)+Tr(W_+ D),
    m>0, W_->=0, W_+>=0.                                (1)

Here W_- and W_+ act on their respective subspaces. This includes the positive/negative spectral split of an arbitrary known affine cost around its minimizing projector E0=I_- direct-sum0. The split itself must be known/paid; no unknown source-dependent projector is supplied by this theorem.

Let N(E)=||c+L(E)||^2 be a known PSD affine-quadratic numerator on Hermitian matrices. Define

    L_cross(B)=L([[0,B],[B*,0]]),
    n(B)=||L_cross(B)||^2,
    q(B)=Tr(W_- BB*)+Tr(W_+ B*B).                         (2)

Since E-E^2>=0, its diagonal blocks show

    BB*<=A-A^2<=A,  B*B<=D-D^2<=D,  ||B||op<=1/2.        (3)

Conversely, ANY B with ||B||op<=1/2 has the rational polynomial completion

    E_B=[[I-2BB*,B],[B*,2B*B]].                           (4)

This is an effect, not generally a projector. Indeed

    E_B-E_B^2=diag(BB* -4(BB*)^2, B*B-4(B*B)^2)>=0,

so every eigenvalue of E_B lies in[0,1]. Its cost is EXACTLY

    u(E_B)=m+2q(B).                                      (5)

The two completions E_B and E_-B have identical cost. Their diagonal terms coincide and their off-diagonal terms have opposite sign. The parallelogram identity therefore gives

    max{N(E_B),N(E_-B)}>=n(B).                            (6)

There is no assumption that the affine numerator or the diagonal completion has a favorable sign. All rational B produce rational effects by(4), with no spectral square root or positive-completion oracle.

## 2. A finite SDP relaxation for the coherent branch

Realify the complex a by b matrix B in a real Hilbert-Schmidt orthonormal coordinate basis, of dimension h=2ab. Write n(B)=v^T H v and q(B)=v^T K v, with known real H,K>=0. A covariance matrix X>=0 defines a centered real Gaussian matrix G and linear moment maps

    R(X)=E GG*,  C(X)=E G*G.

Consider the feasible covariance body

    X>=0, R(X)<=I_a/4, C(X)<=I_b/4.                       (7)

Every deterministic contraction B with ||B||<=1/2 gives a feasible rank-one X=vv^T. Thus the fractional SDP objective

    F_X=S/(m+q), S=Tr(H X), q=Tr(K X)                     (8)

upper-bounds the coherent optimum when optimized. The statement below rounds ANY supplied rational feasible X; no exact SDP optimum is presumed. The usual perspective transform makes(8) an SDP. The body is bounded, Tr X<=min(a,b)/4, and a small positive multiple of the real coordinate identity is a strict feasible point. Certified finite SDP optimization and inward scaling can therefore be paid with polynomial bit complexity. Numerical source information does not enter this optimization subroutine.

If S=0, the supplied covariance certifies no positive coherent objective and may simply be skipped. Assume S>0 henceforth.

## 3. Joint good event: numerator, cost and operator norm

Choose an integer

    R=2 ceil(sqrt(ceil(log_2(48d)))).                       (9)

This is computed from integer bit lengths and integer square roots; R>=sqrt(2 log(48d)) and R^2=O(log d). For the ideal Gaussian G with covariance X,

    E n(G)=S,  E n(G)^2<=3S^2,  E q(G)=q.

Paley-Zygmund gives Pr[n(G)>=S/2]>=1/12. Markov gives Pr[q(G)>48q]<=1/48 when q>0; if q=0 then q(G)=0 almost surely. The rectangular matrix-Gaussian bound with variance parameter max(||R(X)||,||C(X)||)<=1/4 gives

    Pr[||G||op>R/2] <=d exp(-R^2/2)<=1/48.               (10)

The concentration statement is the established rectangular Gaussian-series inequality in Tropp, *User-Friendly Tail Bounds for Sums of Random Matrices*, Corollary4.2; it is not a new concentration theorem: https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf .

A union bound, NOT an independence assumption, now gives probability at least1/24 for ALL THREE conditions

    n(G)>=S/2, q(G)<=48q, ||G||<=R/2.                    (11)

On that event put B=G/(2R). Then ||B||<=1/4, n(B)>=S/(8R^2), q(B)<=12q/R^2. Equations(5)-(6) show that one actual completed effect has

    N(E_±B)/u(E_±B)
      >=S/[8R^2 m+192q]
      >=F_X/max(8R^2,192).                               (12)

The Gaussian round simultaneously preserves the relevant positive quadratic cost and provides a useful numerator. It does not separately round a numerator and hope that an unrelated affine cost remains small.

## 4. Exact feasible rational output and a fixed bit-polynomial cap

The ideal Gaussian is only a proof device. Take known rational bounds Hbar>=max(1,||H||op), Kbar>=max(1,||K||op), and a positive rational precision delta satisfying

    delta<=min{1/8, S/[16(1+S)Hbar],
                         m/[16(1+m)Kbar]}.               (13)

These quantities have polynomial bit length in the supplied rational instance. They imply delta sqrt(Hbar)<=sqrt(S)/4 and delta sqrt(Kbar)<=sqrt(m)/4. Produce a rational matrix Gtilde coupled to G with

    Pr[||Gtilde-G||F>delta]<=1/96.                        (14)

This is bit-polynomial even when delta is exponentially small in its bit length: approximate a covariance square root to polynomially many BITS, truncate the standard Gaussian at a polynomial-dimensional norm bound, and generate high-precision coordinates by bounded inverse-CDF bisection from dyadic uniform random bits. Do NOT enumerate all cells of a delta-mesh.

More explicitly, a rational factor error delta/(8Q), with Q^2>=192h, costs failure at most1/192 by E||g||^2=h. For the finite standard-normal coordinate generator, couple dyadic uniform variates to ideal uniforms. Exclude tails of total probability at most1/192; on the remaining interval the inverse Gaussian CDF has polynomial-in-h derivative. Bisection/CDF approximation to O(log(1/delta)+polylog(h)) bits gives the desired Euclidean coupling. The normal CDF on the bounded interval can be evaluated by a convergent power-series/integration algorithm with polynomial precision cost. The factor norm is bounded from Tr X, and all resulting matrix entries are finite rational numbers. The allocations can be tightened to make the total vector discrepancy at most delta. No TV approximation between a discrete vector and a continuous Gaussian is asserted.

On the joint event(11),(14), the elementary root-norm triangle bounds imply

    n(Gtilde)>=S/8,
    q(Gtilde)<=96q+m/8,
    ||Gtilde||<=R/2+delta<3R/4.                          (15)

Set B=Gtilde/(2R), and certify ||B||<=1/2 by the rational PSD condition I-4BB*>=0. If certification fails, return E0 on that trial. Successful joint-event trials have strict norm slack, so they pass. The output completion(4) is exactly rational and exactly feasible on every accepted history. Evaluate both N(E_B)/u(E_B) and N(E_-B)/u(E_-B), include E0, and retain the best ACTUALLY evaluated ratio.

Equations(15) give on that joint event

    max_± N(E_±B)/u(E_±B)
      >=S/[64R^2 m+1536q]
      >=F_X/K_d,
    K_d=max(64R^2,1536)=O(log d).                         (16)

The joint event has probability at least1/24-1/96=1/32. Therefore a predeclared cap

    ceil[32 log(1/beta)]                                 (17)

of independent finite rounds succeeds except probability beta. No rare-sector expected-stopping refund, reciprocal m repeat count, or coefficient-magnitude sampling cap occurs. The SMALL known m and S affect arithmetic bits only. Rational objective evaluation and rational PSD certification are charged polynomial-time operations. This is a mathematical finite algorithm and proof, not a production SDP/Gaussian compiler or hardware execution.

## 5. How this fits, and does not solve, the full binary-POVM task

For a general candidate effect, expand

    c+L(E)=c+L(E0)-L(diag(A,0))+L(diag(0,D))+L_cross(B).

Four-term Cauchy bounds its squared norm by four times the sum of the four component squared norms. If the coherent term contributes at least one-sixteenth of N(E), then(3) gives q(B)<=u(E)-m; the coherent SDP and(16) therefore produce an actual effect within a factor16K_d of that candidate's ratio. This is a genuinely noncommuting branch, not a classical diagonal surrogate.

But the remaining one-sided effect optimizations are still unproved here:

    maximize ||L_A(A)||^2/[m+Tr(W_- A)], 0<=A<=I,
    maximize ||L_D(D)||^2/[m+Tr(W_+ D)], 0<=D<=I.          (18)

Spectral grouping of a first-moment matrix creates off-diagonal operator blocks; they cannot be discarded as if they were independent cube coordinates. Neither the received binary-cube gate lemma nor the coherent completion above supplies a free positive-cost rounding for(18). No full binary-POVM guarantee follows until these branches are controlled.

Full-CPTP Choi feasibility has the additional coupled partial-trace constraint, which(4) does not address. No generic decoder acquisition exponent is changed. The strongest equally informed conventional learner has the same optimization and receiver controls.
