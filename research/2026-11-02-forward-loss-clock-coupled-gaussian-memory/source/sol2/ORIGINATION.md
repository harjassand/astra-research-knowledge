# Stage 2 independent mechanism, before new primary retrieval

2026-11-01. Same sole Sol worker. First-stage files and coordinator-frozen first return are unchanged.

Target: remove auxiliary stiffness from the complete noncommuting system/coupled-passive-boson simulation, rather than improve the rational hierarchy.

Rejected route: a free Gaussian channel dilation for each coherently chosen interval does not automatically preserve emitted-field overlaps across different time partitions. A dissipative inverse interaction picture is nonpositive. Keeping an entire unitary continuum environment can reintroduce time-bandwidth storage. History-dependent Gram-Schmidt bases do not preserve cross-history overlaps if histories are uncomputed.

Positive mechanism: use the quantum-jump unraveling on the retained modes. All INNER free propagators are the no-jump contraction B(t)=Gamma(exp(At)), never discarded loss channels. Only the actual OUTER first-event record is retained as an orthogonal field time/color, and it is kept through complete-isometry amplification. Actual losses are not confused with virtual no-jump block failures.

Let A=-iH-BB^dagger/2 for an M-mode passive network, with jumps L_mu=B_mu^dagger b. On total occupation <=K,

    J_free(t)=[L_mu Gamma(F(t))]_mu,
    ||J_free(t)||<=sqrt(K) f(t),
    f(t)^2=||B^dagger exp(At)||_F^2,
    J(t)=int_0^t f(s)^2 ds=tr[I-F(t)^dagger F(t)]<=M.

The oscillator loss identity a(v)Gamma(F)=Gamma(F)a(vF) explicitly implements the normalized free-jump block. The scalar cumulative mass J is computable from M-by-M matrices.

Let full no-jump K0(t)=exp[(dGamma(A)+W)t], with bounded W=-i(H_S+V), ||W||<=v. Forward Dyson products of Gamma(F) contractions block-encode K0(t)/4 for t<=tau<=1/v, with truncation and coherent time precision paid. No inverse free channel is used.

Duhamel gives J K0(t)=J_free(t)+int_0^t J_free(s) W K0(t-s) ds. Cross row/column time sources (left density f^2/J(t), right uniform) normalize the convolution by 4v sqrt[K t J(t)]<=4v sqrt(KMt), instead of a stiffness-dependent L1 norm.

Consequently w(t)^2=2K f(t)^2+32K v^2 M t is an implementable enclosing first-jump source; int_0^tau w^2<=18KM. The whole first-event isometry (no jump K0(tau), all actual J_mu K0(t) sqrt(dt)) has source normalization A0^2<=constant*(1+KM), independent of auxiliary rates. Its ideal Kraus completeness earns complete-isometry amplification, rather than amplifying a no-jump contraction as an isometry.

Hard source operation to earn: coherent finite time-state preparation from interval masses J(b)-J(a), normalized vector annihilation and Gamma(F) blocks, with no enumeration of time cells or joint Fock states. Each source is given an explicit finite-matrix/arithmetic route, not assumed. Small-mass/clock-boundary cuts must be paid.

Global event cap candidate: on the exact counted process, N+C (retained particles plus actual emitted count) is conserved by free passive evolution and jumps. Bounded linear system drive yields E[(N+C)_k]<=(aT)^(2k), with a=sum_j ||Q_j||||c_j||. Thus actual jump count has a Poisson-type tail with lambda=(aT)^2, independent of damping/frequency. Compare to that exact capped process; do not assume a tail for the approximate implementation.

This could yield a broadly reusable stiffness-independent-in-the-exponent compiler with polynomial dependence on M,K,aT,hT and logarithmic dependence on ||A||T and inverse error, assuming actual paid system encodings. Literature priority and the complete finite-bit conjunction remain to be tested.
