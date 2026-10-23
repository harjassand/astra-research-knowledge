# Independent review: tree-walk Kraus rank and exact-capacity converse

Reviewer: `recurrent_bath_rank`. Date: 21 October 2026.

## Verdict and scope

**The tree-walk Kraus-rank converse is correct.** For the directed-edge-reversal unitary on the rooted d-regular tree, d>=3, write

    a = 2 sqrt(d-1).

With any diagonal normal initial bath state and any ordinary unassisted n-slot code of dimension K, arbitrary CPTP encoding and decoding satisfy

    f_e <= min{1, floor(a^n)/K}.                            (1)

The same capacity threshold and strong converse hold for every normal initial bath state, including coherent states, by finite vertex-support approximation. The exact bound (1) is retained for the diagonal case; it is not asserted unchanged for coherent initial states.

Together with the root investigator's colored-Dyck noiseless codes, whose needed operator identity is checked below, this gives exact unassisted quantum capacity

    Q = log_2(2 sqrt(d-1))                                  (2)

qubits per slot for every normal initial bath state. The rate is strictly below log_2 d when d>=3. This argument is separate from the earlier standard-Choi spectral bound and does not use it.

## Model and communication contract

Let T_d be the infinite rooted d-regular tree. The root has d children; each other vertex has one parent and d-1 children. At every nonroot vertex the parent edge has input port 0 and the child edges have ports 1,...,d-1. At the root its d child edges have ports 0,...,d-1.

The reservoir Hilbert space is E=ell^2(V(T_d)). The slot system S has dimension d. If port x at vertex v points to w and the reverse edge at w has port y, define

    U|x,v> = |y,w>.

Directed-edge reversal is an involution of the complete basis, so U is a unitary permutation. Let W_n=U_(S_n E)...U_(S_1 E), with all completed outputs retained. Its n-slot block channel from S^(tensor n) to S^(tensor n), initialized in tau, is denoted M_n^tau.

An ordinary unassisted code consists of CPTP maps

    Enc : B(C^K) -> B(S^(tensor n)),
    Dec : B(S^(tensor n)) -> B(C^K).

The bath starts independently of the message and reference, and neither encoder nor decoder accesses the bath. Entanglement fidelity f_e is the overlap of the decoded normalized maximally entangled state with |Phi_K>. There is no output-to-encoder feedback or additional communication side channel in this coding contract.

## 1. Exact rank of each pure-vertex Kraus operator

Fix an initial vertex v. Every length-n input basis word x=(x_1,...,x_n) specifies exactly one length-n tree walk, because the ports are a bijection with the d incident edges at every visited vertex. Write

    W_n |x,v> = |y(x,v), w(x,v)>.

The global map (x,v) -> (y,w) is a basis permutation. For a fixed terminal vertex w, define the D-by-D matrix, D=d^n,

    A_(w,v) = <w|W_n|v>.

Each input column is either zero, when w(x,v) differs from w, or has a single entry equal to one at output word y(x,v). Two nonzero columns cannot occupy the same row: that would give two distinct global input basis vectors with the same output word and terminal vertex, contradicting injectivity of W_n.

Consequently A_(w,v) is a partial permutation, with mutually orthogonal nonzero columns. Its rank is exactly

    rank A_(w,v)
      = #{length-n walks from v to w}
      = <delta_w, H^n delta_v>,                             (3)

where H is the adjacency operator of T_d. Distinct walks ending at the same w are not being assumed to have different outputs without justification: their output distinction follows specifically from global unitary injectivity.

For fixed v the nonzero column sets over w partition the input-word basis, so

    sum_w A_(w,v)* A_(w,v) = I_D.                           (4)

Only finitely many w contribute for a fixed v and n.

## 2. Uniform walk-count bound

For completeness, the needed adjacency bound can be proved directly. Put b=d-1 and h(v)=b^(-depth(v)/2). For a nonroot vertex,

    sum_(w~v) h(w)/h(v) = sqrt(b)+b/sqrt(b)=2sqrt(b).

At the root the sum is d/sqrt(b)<=2sqrt(b), since d>=2. For finitely supported complex f, sum the edgewise inequalities

    2|f(v)f(w)|
       <= [h(w)/h(v)]|f(v)|^2 + [h(v)/h(w)]|f(w)|^2.

They imply |<f,Hf>|<=2sqrt(b)||f||_2^2. The adjacency operator is bounded and self-adjoint, so density gives

    ||H||_(2->2) <= 2sqrt(b)=a.

It follows that

    #{length-n walks v->w}
       = <delta_w,H^n delta_v>
       <= ||H||^n
       <= a^n.                                             (5)

Equivalently, with P=H/d, the count is d^n P^n(v,w) and ||P||<=a/d. Since (3) is an integer,

    rank A_(w,v) <= M_n := floor(a^n).                      (6)

Only the upper operator-norm estimate is needed; no unproved equality for the spectral radius or heat-kernel asymptotic is required.

## 3. Diagonal initial mixtures and countable Kraus sums

For a diagonal normal bath state

    tau = sum_v pi_v |v><v|,
    pi_v>=0, sum_v pi_v=1,

the block channel has Kraus operators

    B_(v,w)=sqrt(pi_v) A_(w,v).                             (7)

Equations (4) and (7) give

    sum_(v,w) B_(v,w)* B_(v,w)=I_D.

The family is countable, but there is no convergence gap. The input and output matrix spaces are finite-dimensional. Positive partial sums of the completeness relation have bounded trace and converge in trace norm, hence in operator norm. Channel action on positive matrices converges in trace norm; linearity then gives the full channel. Equivalently, (7) is the direct partial-trace expansion of the well-defined normal initial mixture.

Every B_(v,w) has rank at most M_n. The bound is uniform over v,w and does not depend on the stationary distribution, the bias in the reference input, or the entropy of tau.

## 4. Arbitrary encoding and decoding do not increase Kraus ranks

Choose finite Kraus families E_alpha for Enc and R_beta for Dec. The complete code channel has the countable Kraus family

    F_(beta,v,w,alpha) = R_beta B_(v,w) E_alpha.              (8)

Matrix multiplication cannot increase rank, so every F_i in this family has rank at most M_n. Completeness gives sum_i F_i*F_i=I_K.

For the normalized maximally entangled state, the exact fidelity formula is

    f_e = (1/K^2) sum_i |Tr F_i|^2.                         (9)

The summands are nonnegative, so the countable family poses no interchange issue. For any square matrix F of rank at most M_n, the singular-value inequalities give

    |Tr F|^2 <= ||F||_1^2
                <= rank(F) ||F||_2^2
                <= M_n Tr(F*F).                            (10)

Summing (10) in (9) yields

    f_e <= (M_n/K^2) sum_i Tr(F_i*F_i)
         = M_n/K.                                         (11)

This proves (1) for arbitrary CPTP encoders, with no isometric-encoder reduction or asymptotic coding theorem.

The equivalent Schmidt-rank proof is also valid: the unnormalized vectors (F_i tensor I)|Phi_K> each have Schmidt rank at most M_n, and their normalized overlaps with |Phi_K> are at most M_n/K. Their squared norms sum to one. They need not be mutually orthogonal. The resulting mixed state may have large ordinary matrix rank; the property used is its decomposition into bounded-Schmidt-rank vectors, not a bound on its ordinary rank.

## 5. Strong converse for the diagonal case

Let R_n=(log_2 K_n)/n. Equation (11) gives

    f_(e,n) <= min{1, 2^[-n(R_n-log_2 a)]}.                 (12)

At any rate at least log_2 a+alpha eventually, with alpha>0,

    f_(e,n) <= 2^(-alpha n).

This is an exponential strong converse in entanglement fidelity for every diagonal normal bath initializer. The decoded Choi state's half trace distance from the pure ideal state is at least 1-f_(e,n), so this half distance tends to one above threshold. Full trace distance tends to two.

## 6. Extension to every normal bath state

The exact diagonal Kraus representation (7) is not available for a coherent initial tau. A direct coherent sum of the A_(w,v) can have larger rank. This changes the finite-block bound but does not change the asymptotic threshold.

Choose a finite vertex set F and its coordinate projection P_F, with r=|F| and

    q=Tr(P_F tau)>0,
    tau_F=P_F tau P_F/q.

Such finite sets can make q arbitrarily close to one because tau is a normal trace-class density on the countable vertex Hilbert space. Purify tau to |psi_tau> and project that purification by P_F tensor I, then normalize. The overlap of the original and projected pure states is sqrt(q). Their half trace distance is sqrt(1-q), and partial-trace contractivity gives

    D(tau,tau_F):=(1/2)||tau-tau_F||_1 <= sqrt(1-q).          (13)

Diagonalize tau_F into at most r pure eigenvectors psi_l supported in F. For each such eigenvector and terminal vertex w, the corresponding channel Kraus matrix is proportional to

    <w|W_n|psi_l> = sum_(v in F) psi_l(v) A_(w,v).

Rank subadditivity and (6) imply that every matrix in this Kraus representation has rank at most r M_n. The preceding code argument therefore gives, for every encoder and decoder,

    f_(e,n)(tau_F) <= min{1, r M_n/K_n}.                    (14)

For the same code, taking the initial bath state to its final decoded Choi state is a CPTP map. Entanglement fidelity is the expectation of a projection. Consequently (13) implies uniformly in n and in the chosen code

    |f_(e,n)(tau)-f_(e,n)(tau_F)| <= sqrt(1-q).

Combining this with (14),

    f_(e,n)(tau) <= min{1, sqrt(1-q)+r a^n/K_n}.             (15)

For rates strictly above log_2 a, fix F first. The second term in (15) tends to zero. Thus limsup_n f_(e,n)(tau)<=sqrt(1-q). Now enlarge F so q tends to one. This proves

    f_(e,n)(tau) -> 0                                      (16)

above threshold for every normal tau, including states with coherences or infinite entropy.

The order of limits is essential: F and r are fixed before n tends to infinity. No finite reservoir-support hypothesis is introduced into the physical model. For arbitrary infinite tails, this proof does not supply the same uniform exponential convergence rate as (12). It does supply the strong converse and therefore the same capacity upper bound.

## 7. Compatibility with the colored-Dyck lower bound

The root investigator's matching lower bound uses input basis words of even length 2m. Each nonzero symbol a in {1,...,d-1} is a colored push; each zero is a pop. The push/pop pattern is a Dyck word: all prefix heights are nonnegative and the final height is zero. There are

    K_m = Catalan_m (d-1)^m                                (17)

such colored words.

For any starting vertex v, every push goes to a child and emits output 0. Every pop occurs at positive height above v, so it traverses the inverse of the most recent unmatched pushed edge, emitting that push's color. It never takes a parent edge from the starting vertex. Thus the special port-zero convention at the root causes no exception.

At the end the bath is exactly back at v. The output word is independent of v. It also determines the entire input word: its zeros mark pushes, its nonzero symbols mark pops and reveal the color of the matching push. Consequently the input-to-output map is injective.

If C_m is the span of these input words, there is a fixed isometry V_m on C_m such that

    W_(2m)(|phi> tensor |v>) = V_m|phi> tensor |v>

for every phi in C_m and every vertex v. By linearity and continuity this holds with an arbitrary bath state, including coherences, arbitrary normal mixtures, purifications, and external reference entanglement. A decoder inverts V_m on its range. Hence these are exact noiseless codes with exact bath return under the unchanged device.

Using Catalan_m=(1/(m+1)) binom(2m,m) and its elementary Stirling asymptotic,

    (log_2 K_m)/(2m)
       -> 1+(1/2)log_2(d-1)
       = log_2(2sqrt(d-1)).                                (18)

Odd horizons can use the largest preceding even block and one extra fixed input whose output is discarded; the completed code output is already decoupled from the bath. Thus parity does not affect the asymptotic achievable rate.

Equations (16) and (18) establish the exact capacity (2) for every normal bath initializer under the stated unassisted coding contract. The lower proof is a direct check of the root's supplied construction, not a separately invented replacement construction.

## Limits and provenance of this review

- The sharp exponential finite-block fidelity bound (1) is proved for diagonal normal tau. For general normal tau the verified finite-block replacement is (15), followed by an asymptotic strong converse.
- The initial bath is independent of the encoded message. Encoders and decoders do not access the bath or communicate through a side channel.
- The proof allows all output correlations and arbitrary CPTP block encoders and decoders. It does not assume independent channel uses.
- The result relies on the specific tree-edge permutation. It is not a capacity conclusion from recurrence alone, or from a generic entropy statement.
- No efficiency of optimal encoder/decoder synthesis is asserted beyond the explicit Dyck basis mapping. The converse concerns attainable information rate and fidelity under unrestricted finite block operations.
- The exact-capacity argument does not depend on the earlier Choi min-entropy estimate or on the biased-reference stationary distribution. Those remain separate properties of the same construction.
- The adjacency estimate, rank argument, fidelity inequality, and cutoff extension are proved here. This is an internal mathematical review, not an external certification or a historical-priority determination.
