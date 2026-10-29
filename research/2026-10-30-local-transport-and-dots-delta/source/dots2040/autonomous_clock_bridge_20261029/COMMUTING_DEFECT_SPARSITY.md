# Commuting bad-box flags and uniform sparse defects

2026-10-29. Root proposed theorem, under independent review. This strengthens EXACT_DEFECT_DAMPING.md to simultaneous, physically meaningful defect probabilities. It does not prove a logical quantum-memory threshold.

## 1. Define a commuting local family

Use P_x,Q_x,V_x,G_x and the guarded clean Hamiltonian of GUARDED_CHANNEL_CLOCK.md. Define

    B_x = Q_x - V_x V_x* G_x.

V_x V_x* is a projector under Q_x, and G_x commutes with it. Thus B_x is a projector. It is local on box x and its neighboring auxiliaries.

All B_x commute. Proof: each preserves every auxiliary occupancy pattern. In a fixed occupancy sector, B_x=0 if x is ready; B_x=I on its active sector if an occupied neighbor exists; otherwise B_x is the complement of the Stinespring image on data box x. Two active isolated boxes have disjoint data supports. Therefore all nontrivial projector factors commute in every occupancy block.

Let P_good=product_x (I-B_x). It is exactly W W*: every active box must be isolated and in its Stinespring image. This criterion is equivalent to the independent-set encoded space, not an additional good-state assumption.

## 2. Clean product drift is uniformly negative

For S a set of boxes, define B_S=product_{x in S}B_x. Then

    [H,B_S]=0,
    L_clean*(B_S) <= -(sum_{x in S} kappa_x) B_S.

For H_x, B_x annihilates its ready/image transition. For a neighboring B_y, H_x either has y ready (B_y=0) or is blocked by y's occupancy. All nonneighbor terms commute. Thus [H,B_x]=0 individually.

A reset at x in S maps x to ready, so its gain term vanishes and its loss is exactly -kappa_x B_S. For a reset at y outside S, condition on all other auxiliary occupancy bits. The product B_S is independent of y's excited Kraus label and takes values C_0 when y is ready and C_1 when y is occupied. Clearing y can only turn a neighbor's bad identity projector into its smaller Stinespring-complement projector. The affected factors commute in each occupancy sector, hence 0<=C_0<=C_1. The reset contribution is kappa_y Q_y(C_0-C_1)<=0. This proves the product inequality, including overlapping S.

The argument retains noncommuting data operators by blockwise occupancy analysis; it does not incorrectly assume the earlier R_x projectors commute everywhere.

## 3. General bounded local generator perturbations

Allow perturbations N_e(t), each annihilating the identity in the adjoint and supported on a specified physical region, possibly jointly with an arbitrary bath. Let C_e be the boxes whose B_x support intersects that physical region. Suppose

    |C_e|<=b,
    sup_x sum_{e:x in C_e} ||N_e*(t)||_(infty->infty) <= lambda.

The total evolution must remain a legitimate quantum evolution. Individual N_e may be differences of calibrated local generators; complete positivity is not used for the following norm bound. Bath-only dynamics commutes with all B_S and contributes zero. For Hamiltonian bath terms a finite interaction norm is required; an unbounded unknown bath coupling is not covered.

Put m_S(t)=Tr[B_S rho(t)]. Write B_S=B_(S\C_e) B_(S intersect C_e). Locality yields

    N_e*(B_S)=B_(S\C_e) N_e*(B_(S intersect C_e))
              <= nu_e B_(S\C_e),

because the outside projector commutes with the local image and the latter Hermitian operator has norm at most nu_e. Therefore

    m'_S <= -kappa |S| m_S + sum_(e:C_e intersects S) nu_e m_(S\C_e),

where kappa=min_x kappa_x. If initial state is clean and 0<lambda<kappa, set

    a=(lambda/kappa)^(1/b).

Induction on |S| and comparison with the constant supersolution gives, for every finite S, all t>=0 and every volume,

    m_S(t) <= a^|S|.

Indeed lower moments are at most a^(|S|-|C_e|)<=a^(|S|-b), and sum touching rates is at most lambda |S|. The resulting stationary upper bound is a^|S|. For lambda=0 the moments remain zero. More generally an initial a0-sparse defect law remains max(a0,a)-sparse.

Because the B_x commute, m_S is the probability that a simultaneous measurement finds every box in S bad. The conclusion is a genuine joint equal-time sparse-defect bound, not a collection of marginal estimates. It requires no noise-model reconstruction, global mixing gap, or bath reset beyond the specified local auxiliary reset operations.

## 4. Sharper coherent-noise accounting

Separate stochastic/general-generator terms with budget lambda from bounded Hamiltonian terms h_e (possibly coupled to retained baths), with per-box sum norms <=h and support touching <=b flags. Cauchy–Schwarz gives

    |Tr rho i[h_e,B_S]| <=2||h_e|| sqrt(m_S m_(S\C_e)).

The same boundary comparison gives m_S<=a^|S| with

    a = [(h+sqrt(h²+kappa lambda))/kappa]^(2/b),

provided a<1. To check the invariant boundary m_S=a^|S|, use lower moments and obtain the factor

    -kappa a^b +2h a^(b/2)+lambda =0.

This charges coherent leakage quadratically in h/kappa at small h, while not asserting that logical DATA errors are quadratic. The norm budget covers only the declared bounded physical interactions.

## 5. What this enables, and the missing bridge

The exact finite-rate compiler does not rely on perfectly maintained auxiliary code spaces: bounded local noise produces a uniformly sparse distribution of explicit bad-box flags at every time, independent of total size and runtime. This is a constructive repair of an otherwise hidden perfect-controller premise.

It is NOT yet a space-time fault-path theorem. A rare long-lived defect can correlate errors at many update times. Nor does healing B_x repair data corrupted while it was bad. To obtain a scalable autonomous memory/computer, one must show the full asynchronous logical correction process tolerates the resulting time-correlated faults and clock scheduling, implement guarded couplings with actual two-body hardware, and supply the reset reservoirs and preparation/readout interface. These obligations are not assumed by this theorem.
