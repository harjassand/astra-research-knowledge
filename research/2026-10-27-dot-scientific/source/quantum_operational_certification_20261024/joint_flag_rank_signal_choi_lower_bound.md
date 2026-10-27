# Joint mixed-flag rank and success-signal lower bound

2026-10-27. New corollary candidate, independent receipt requested. Access is IID full normalized Choi programs only; no quadratic arbitrary-adaptive-query lower bound is asserted.

## Family and claim

Choose integers1<=r<=D, p=r/D, and let P_r be a rank-r flag projector in C^D. Before an unknown Haar unitary U on B=C3 tensor CD, define

 E0(rho)=(1/D)rho tensor P_r
        +(1/D)Tr(rho) I3/3 tensor(I_D-P_r),
 E_U=Ad_U composed E0.

This has success probability p, a uniform mixed success flag of rank r, and reset orthogonal to the success sector. At r=D it is the reversible p=1 family. The receiver marginal is exactly I_(3D)/(3D). Its WH3 deficit is zero: the active flag blocks are scaled maximally entangled Choi states, the other blocks are scaled isotropic reset states, each with zero homogeneous deficit.

If a fixed processor using n independent normalized Choi copies and one independent datum approximates the COMPLETE target p identity+(1-p)erasure with unhalved diamond error at most nu p uniformly in U, where0<nu<=1/4, then

 n>=9D²/4096=(9/4096)r²/p².                         (1)

This is a uniform lower bound on this explicit integer-grid family p=r/D. It does not silently claim an all-real-p interpolation or an optimal numerical constant.

## 1. Centered Choi moment and concentration

The Choi state has form

 J_U=I/(9D)+A_U,
 A0=[(Phi_3-I_9/9) tensor P_r]/D,
 A_U=(I_A tensor U)A0(I_A tensor U*).

Direct calculation gives

 Tr A0²=8r/(9D²),
 Tr_A A_U²<=8I_(3D)/(27D²).

Let g(U)=9D Tr(J_I J_U)=1+9D Tr(A0 A_U). Its Haar mean is1. The Hilbert-Schmidt tangent derivative obeys

 |g'|<=18D ||A0||_2 ||(I_A tensor K)A_U||_2
       <=[16sqrt(r)/(sqrt3 D)]||K||_2.

The phase-invariant SU(3D) log-Sobolev/Herbst estimate, with the same explicitly normalized input as `mixed_flag_quadratic_choi_program_lower_bound.md`, therefore gives

 log E exp[t(g-1)]<=256r t²/(9D³).

For R_m=E J_U^tensor m and F_m=m log(9D)-S(R_m), pair purity and Renyi monotonicity give

 F_m<=256r m²/(9D³).

Exchangeability and strong subadditivity then imply, for n>=1,

 F_(n+1)-F_n<=F_(2n)/n<=1024r n/(9D³).               (2)

Measuring the reference qutrit of one further Choi state produces the uniform logical-label/data experiment. Since Tr_A J_U=I_(3D)/(3D) for every U, the same exact entropy-increment argument bounds its Holevo label information by(2).

The concentration input is the SU(N) inequality Ent(f²)<=(4/N)E||grad f||², as normalized in the Appendix of [Meckes and Meckes](https://arxiv.org/html/1210.2681). No singular inverse Haar Gram formula is continued past a support cutoff.

## 2. Accepted-label information is order p, without log(1/p)

Choose the true logical label A uniformly among three basis states, and measure the receiver's output as accepted logical label B or erasure. Let z be total acceptance probability and w the joint probability of acceptance with wrong B. Put delta=nu p<=p/4.

The complete error guarantee gives

 p-delta/2<=z<=p+delta/2,
 w<=delta/2,
 Pr(accept|A=a)<=p+delta/2 for each a.

Consequently

 z>=7p/8,
 Pr(wrong|accept)<=1/7,
 max_a Pr(A=a|accept)<=3/7.

The last inequality permits input-dependent acceptance; it is NOT replaced by an assumption of uniformly accepted labels. It yields H(A|accept)>=log(7/3). Conditional Fano gives

 I(A:B|accept)>=log(7/3)-h(1/7)-(log2)/7.

The acceptance flag itself can only add mutual information. Therefore

 I(A:complete classical output)
 >=(7p/8)[log(7/3)-h(1/7)-(log2)/7]
 = (p/8)log(32/3)>p/4.                              (3)

The final strict inequality is exact: e<3 implies e²<9<32/3.

All logarithms are natural. This avoids a continuity estimate whose error would unnecessarily contain log(1/p).

Combining data processing,(2),(3), and p=r/D proves(1). A zero-program processor has no Haar-averaged label information, so excluding n=0 from the entropy-increment division is harmless.

## Scope

The full-program model permits arbitrary collective processing of the mixed Choi copies and datum. It does not provide purified preparations, coherent flag indices, or a classical U description. Training and datum are independent conditionally on one fixed U.

This theorem simultaneously contains the p^-2 signal obstruction at fixed mixed rank and the r² mixed-rank obstruction at p=1, but only in the Choi-copy access model. The received physical-query collision lower bound is a separate theorem and must not be upgraded by implication.
