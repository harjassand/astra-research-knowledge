# Known erasure-flag hard subclass: all-p classical compilation lower

2026-10-27. Separate source-unknown recovery theorem submitted for independent receiving. It does not modify the full-ambient-reset theorem or the frozen broad upper assembly.

Let s>=3r+1, integer r>=1, and0<p<=1. Fix a known one-dimensional physical erasure flag |e> and its known (s−1)-dimensional orthogonal complement K. Haar U in SU(s−1) embeds C^3 tensor C^r into K through an unknown isometry V_U. Define

 E_U(X)=p V_U(X tensor I_r/r)V_U*+(1−p)Tr(X)|e><e|.

The learner may know p,r,K and the erasure flag. It uses at most n physical source queries, with arbitrary coherent adaptive inputs/memory, all BEFORE an independent datum. It then retains only a classical decoder description, or at most m dimensions of source-dependent quantum deployment storage in addition to arbitrary classical description. Fresh source-independent ancillas are unrestricted. Suppose its uniform training-averaged unhalved complete recovery error against full-throughput G_p is at most p/4.

Then, with natural logarithms,

    n >= (s−1)r / [32 p ln(3(s−1)/r)]

for classical deployment, and

    nm >= (s−1)r / [64 p ln(3(s−1)/r)]

for bounded quantum deployment storage. This is a worst-case lower for the broader family of arbitrary unknown orthogonal resets, since the present easier, revealed-reset subclass belongs to that family. It is not a statement that every unknown-reset instance is hard.

## Exact physical-query information increment

Write M for retained calibration memory and Q for the next qutrit input. Conditional on U the output has an orthogonal success/reset decomposition with fixed probabilities p,1−p and identical memory marginal in both branches. Therefore

 S(B|M,U)=h(p)+p[ln r+S(Q|M,U)].

Because the erasure sector is FIXED and known, the unconditional output has the same fixed block decomposition. Hence

 S(B|M)=h(p)+p S(B_success|M) <= h(p)+p ln(s−1).

This is stronger than the crude ln s bound; there is no unknown-support entropy contribution from reset samples. Using the exact increment identity

 I(U:BM)−I(U:QM)=S(B|M)−S(B|M,U)−I(U:Q|M)

and S(Q|M,U)>=−ln3 gives an increment at most

    p ln(3(s−1)/r).

This remains valid for source-dependent entangled query inputs. Processing cannot increase information, so the total deployment information is at most n times that value. The heralding flag is not granted for free: it is part of each charged physical output.

## Required information for recovery

Let T_i be the decoder's accepted logical-label effects and Ttilde_i=T_i−T_total/3. The source's common reset term cancels pointwise. The centered score is

    f(U)=p/(3r) sum_i Tr[P_i(U) Ttilde_i].

Its Haar mean is zero on SU(s−1), since sum_i Ttilde_i=0. The already received rank/ambient gradient estimates apply on K with a factor p²: scalar Gamma<=2p²/r; with m-dimensional retained quantum deployment storage the complete bound is Gamma<=4mp²/r. Classical outcome labels form a direct-sum algebra and do not enter m.

Unhalved complete error p/4 gives correct-label probability>=7p/8 and total acceptance<=9p/8, so the centered witness is at least p/2. Received complete heat transport with entropy-decay rate s−1 bounds the witness by2sqrt(Gamma_bound I/(s−1)). Consequently I>=(s−1)r/32 in the classical case, or I>=(s−1)r/(64m) in the quantum-memory case. Combining with the exact query information increment proves the claims.

## Comparison and boundaries

For all0<p<=1 and s>=3r+1 this is Omega(sr/[p log(s/r)]) at fixed relative accuracy. Thus the independently constructed all-source reusable upper O(sr/p polylogs), when its separate assembly is received, has matching rank/ambient/signal exponents for this broad model's worst case. A lower bound on a revealed-reset subclass is logically enough; it does not receive or replace the distinct full-ambient unknown-reset information formula D_Ber(p||3r/s)+2p ln3.

At p=1 and minimal ambient s=3r (where this extra flag is unavailable), the already received rank/ambient compilation lower applies directly to the reversible source. For p<1 the present theorem is explicitly restricted to s>=3r+1. Fixed query caps, pre-datum calibration and explicit deployment-memory restrictions are essential. No online/interleaved or expected-query lower, no quantum-program reuse theorem, and no historical novelty claim is made.

Dependencies: joint_rank_ambient_signal_compilation_tradeoff.md (centered score, scalar/complete gradients and memory contract); complete_mlsi_direct_heatflow_transport_lemma.md. The fixed-known-sector entropy calculation above is new to this separate corollary.
