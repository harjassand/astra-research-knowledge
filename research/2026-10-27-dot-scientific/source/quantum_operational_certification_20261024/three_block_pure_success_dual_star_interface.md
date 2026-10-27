# Pure logical success and three rank-one reset blocks: exact dual-star interface

Actual source E(rho)=p rho tensor P_s+q Tr(rho)sum_i wi |i><i| tensor P_vi, with sum wi=1. Put ri=|<s,vi>|^2. No value theorem is claimed here beyond previously received subclasses.

A Stinespring isometry is

V|psi>=sqrt(p)|psi>|s>|0>_E
 +sqrt(q)sum_i sqrt(wi)|i>|vi> (|psi>_(Einput) tensor |i>_(Elabel)).

The complementary channel has a scalar flag block p Tr(rho), reversible blocks q wi rho, and coherent cross row sqrt(pqwi)<vi|s> sum_k rho_ik |0><k,i| plus adjoint. In the normalized complementary Choi state, define

|Omega_i>=|Phi3>_(A,Einput) tensor |i>_(Elabel),
|f_i>=|i>_A tensor |0>_E.

The six vectors are mutually orthonormal. After absorbing phases, the entire Choi state is the direct sum over i of the exact2x2 blocks

[[q wi, sqrt(pq wi ri/3)], [sqrt(pq wi ri/3), p/3]]

on span{Omega_i,f_i}. Each determinant is pqwi(1-ri)/3>=0. Its input marginal is exactly I3/3, since the Omega blocks contribute q I3/3, flag blocks contribute p I3/3, and cross terms vanish under environment trace. Thus this is an actual TP complementary channel, not an arbitrary PSD embedding.

WH3 preserves the deficit under purification duality. Explicitly, use the antisymmetric Stinespring isometry |i> ->sum_jk epsilon_ijk |j>|k>/sqrt2, whose two output channels coincide. For any purification of A_AR to ARE, the resulting pure BCRE has S(BR)=S(CE), S(AR)=S(E), and S(R)=S(AE). Therefore Delta(A_AR)=Delta(A_AE).

This gives a finite coherent-star receiver target for the pure-success three-block question. It is not the already received incoherent reversible-success plus pure-reset flag family: the cross terms are essential. It also does not automatically fit a single common-filter form. Factoring each block gives a main vector sqrt(qwi)Omega_i+sqrt(p ri/3)f_i and residual p(1-ri)f_i f_i*/3; the associated input filter is qwi I+p ri |i><i|, which varies with i. A common-filter theorem requires an actual matching argument, not just the shared flag.

The coordinate-overlap endpoint failure in three_block_pure_success_overlap_monotonicity_failure.md applies to this dual-star class as well by exact duality. A stronger stationary/anchor comparison would be needed to receive it.
