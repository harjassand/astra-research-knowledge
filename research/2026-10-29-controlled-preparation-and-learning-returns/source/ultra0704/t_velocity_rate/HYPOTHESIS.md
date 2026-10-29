# Positive conserved-currency lineage for actual hard-sphere rates

29 October2026. The completed Maxwell/rotation packages remain frozen.

The new target is a normalized iid one-particle output for the homogeneous
hard-sphere Boltzmann model with rate |v-w| and uniform outgoing relative
direction. Maxwell moment closure and Gaussian-convolution commutation are
NOT assumed. Velocity/source/model and real-bit costs remain explicit.

The strongest first primary is Fournier,2019, DOI10.3934/krm.2019020,
arXiv:1703.10874v1. It already constructs an exact weighted recursive
output (M_t,V_t), E[M_t 1_(V_t in A)]=f_t(A), and a finite-horizon expected
work bound. It does not claim V_t itself has law f_t; its mass second moment
is not acquired. Recursive/time-relaxed/DSMC methods remain strong ordinary
alternatives. Generic exact recursion, energy tilting and null collisions
are prior, not inventions here.

Candidate missing interface: use the conserved positive quantity
h(v)=a+|v|^2, c=a+E|V_0|^2, and the law g_t=h f_t/c. A pair of iid g_t
velocities v,w is proposed at a local rate dominating c|v-w|/h(w).
On an accepted collision, choose v' or w' with probabilities proportional
to h(v'),h(w'). Pairwise h conservation and exchange symmetry appear to
turn the gain into a genuine Markov jump, without multiplying a mass M.
Finally accept a g_t velocity with probability a/h(v), whose mean is a/c.

The exact bilinear generator identity is derived next. It is only the
first constructive step until the recursive sampler's termination,+law identification and full expected costs are proved. No unbounded-rate
oracle, unknown g_t sampler, or uniform-in-time cost is granted.
