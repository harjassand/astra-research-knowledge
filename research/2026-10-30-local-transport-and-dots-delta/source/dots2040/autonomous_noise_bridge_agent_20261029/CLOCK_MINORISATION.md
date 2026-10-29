# Uniform-volume local emission minorization for ideal hard-core clocks
Date: 2026-10-29. Proven for uniform g,κ, any bounded-degree conflict graph, any initial clock density operator supported on independent sets. Does not itself prove a joint local stochastic fault bound.

## Statement
Let maximum graph degree be D, ε=g/κ>0, ε²≤1/[100(D+1)]. For clock dynamics

L_c(ρ)=−i[gΣ_x(b_x+b_x†),ρ]+κΣ_x D[b_x](ρ),

put
T=[4 log(1/ε)+2 log 10+log 2+1]/κ,
α=ε²/2.

For every vertex x and every initial clock density matrix, the probability of at least one x-emission within [0,T] is ≥α. The bound is independent of graph volume. Because it holds for every initial state, it also holds conditional on any past monitored-emission record up to the start of the interval, provided the clock remains in the legal independent-set space. Thus

P(no x-emission by time mT | past)≤(1−α)^m.

This is a one-vertex delay tail, not an independence claim across vertices.

## Proof
On the independent-set Hilbert space, let n_x=b_x†b_x and A_x=Π_{y~x}(I−n_y). Exact operator relations imply, with p_x=Tr(n_xρ), c_x=Tr(b_xρ),

p'_x=−κp_x−2g Im c_x,
c'_x=−κc_x/2−ig Tr[(A_x−2n_x)ρ]+ig Σ_{y~x}Tr[b_y†b_xρ].

The damping terms of other vertices vanish in the second equation. For adjacent x,y, [b_x,b_y†]=−b_y†b_x and both n_y b_x and b_x n_y vanish. For nonadjacent vertices the relevant operators commute. The local equations were also checked as exact matrix identities on path graphs of lengths 1 through 7 by clock_minorization_check.py.

Cauchy–Schwarz gives |c_x|≤√p_x. Therefore

p'_x≤−κp_x+2g√p_x≤−κp_x/2+2g²/κ,
p_x(t)≤e^(−κt/2)+4ε².

For t≥t0=4 log(1/ε)/κ, every p_x≤5ε². Define
F_x=Tr[(A_x−2n_x)ρ]−Σ_{y~x}Tr[b_y†b_xρ].

Since I−A_x≤Σ_{y~x}n_y and |Tr[b_y†b_xρ]|≤√(p_yp_x),
Re F_x≥1−5Dε²−10ε²−5Dε²≥0.9.

Let y_x=−Im c_x. Then y'_x≥−κy_x/2+0.9g for t≥t0, and y_x(t0)≥−√5 ε. After t1=2 log10/κ,

y_x≥1.8ε−(1.8+√5)ε/10>ε,

and this lower bound persists. Consequently p'_x≥−κp_x+2κε². Starting from p≥0, after an additional t2=log2/κ we have p_x≥ε², and this persists.

In the final interval I=[t0+t1+t2,t0+t1+t2+1/κ], the expected number N_x of x-emissions is
E N_x=κ∫_I p_x(t)dt≥ε².

The counting-process intensity is at most κ, since n_x≤I. Let τ be its first event in I. Conditional on τ and the complete record then, expected additional events are at most κ|I|=1. Hence E N_x≤2P(N_x≥1). This proves P(N_x≥1)≥ε²/2, and therefore the claimed lower bound over the full interval. Iteration follows by conditioning at each block boundary and reapplying the bound to the resulting legal density operator.

## Scope and limits
The proof permits arbitrary coherent and entangled clock initial states on the legal subspace, not merely product states or stationary states. It does not require global mixing or a spectral gap uniform in volume. It uses small but fixed ε, so all constants remain independent of system size/runtime.

It is not valid as stated after a thermal upward jump creates an illegal occupied-neighbor pattern. It also does not imply that simultaneous delays at nearby vertices have product probabilities. To obtain a threshold, one must bound multi-vertex/time marked fault clusters, accounting for shared clock bottlenecks and quantum correlations; replacing this task by repeated marginal estimates would be unjustified.
