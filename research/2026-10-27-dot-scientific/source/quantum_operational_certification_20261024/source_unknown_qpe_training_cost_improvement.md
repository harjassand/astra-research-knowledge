# Explicit coherent-phase improvement of the quantum-training sample budget

Status: separate finite-resource improvement, pending independent receipt. The source/access/entropy theorem is `source_unknown_classically_labelled_training_recovery_corollary.md`; no conclusion of that already frozen construction depends on this improvement.

Use the SAME ordinary labelled-training programs T,omega, A=4(T-omega), supplied p>=p0>0, and erased spectral projector target. Labels/randomness are discarded and the data/reference is independent of their preparation. The source model and entropy promise remain assumed. Controlled output-register SWAPs and coherent ancilla gates remain required.

For0<zeta<=1 put eta=(zeta/16)^2. Let M=2^m be the least power of two satisfying M>=144/p0, and r=ceil log2(1/eta). Define
 S=r pi(M-1).
For each of the r repetitions and each j=0,...,m-1, the needed controlled A-evolution time is t_j=pi 2^j. Simulate it with
 N_j=ceil[512 t_j S/zeta]
signed collision rounds using T and omega. This consumes exactly
 N_train=2r sum_(j=0)^(m-1) N_j
training channel calls, plus ONE data call per decoding attempt. In particular
 N_train<=1024 S^2/zeta+2rm
 =O[p0^-2 log^2(1/zeta)/zeta]+O[log(1/zeta)log(1/p0)].        (1)
This is a potentially large non-practical upper bound, but improves the first Hadamard construction's p0^-4 dependence. Quantum phase estimation uses m coherent ancillas per repetition; they can be reused between repetitions. Gate width/storage still depend on the actual output dimension. No reusable/amortized classical decoder is claimed.

## 1. A wrap-safe spectral test

Apply standard finite quantum phase estimation with M grid points to
 U=exp[i pi(A+I/9)].
The scalar I/9 phase is known and needs no channel samples. If A has eigenvalue a, its phase is phi=(a+1/9)/2 mod1. The positive Phi_V phase is
 phi_plus=(8p+1)/18 in[1/18+4p0/9,1/2],
whereas all remaining phases lie in[0,1/18]. Accept a phase estimate exactly when it belongs to
 [theta,3/4), theta=1/18+2p0/9.
Let delta=2p0/9<=2/9. Any estimate with circular distance LESS than delta from the true phase is classified correctly. The upper rejection interval handles phase wrap near zero: an estimate wrapping to near1 is above3/4 since1-delta>=7/9. Positive phases have upper margin at least1/4>delta.

## 2. Explicit finite QPE tail

The exact probability of grid outcome l on an eigenphase phi is
 sin^2(pi M phi)/[M^2 sin^2(pi(phi-l/M))],
with the usual removable value at exact grid points. Since sin(pi x)>=2x for0<=x<=1/2, this is at most1/[4M^2 dist_circle(phi,l/M)^2]. Indexing grid outcomes from a nearest grid point, whose distance is at most1/(2M), the two tails beyond circular error delta are bounded by
 (1/2) sum_(j>=ceil(M delta-1/2)) (j-1/2)^-2
 <=1/[2(M delta-2)].
The last inequality follows by the integral bound for the decreasing function(t-1/2)^-2; we use M delta>=32. Thus each spectral test has error at most1/60<1/16 on EVERY eigenspace. No numerical phase scan is used.

Repeat r times and take the majority classification (ties may be assigned either way). Conditioned on an eigenspace the repetitions are independent. A union bound over at most2^r subsets of at least r/2 errors gives failure probability at most
 2^r(1/16)^(r/2)=2^-r<=eta.
The rank-one positive-space accepted-coherence argument from the core theorem now gives full success-plus-erased-failure instrument error at most8sqrt(eta)=zeta/2. We do not infer quantum instrument accuracy from classical misclassification alone.

## 3. Charged sample simulation and composition

For labelled programs A=4(T-omega), a controlled evolution for A-time t_j uses signed collision time4t_j. The core elementary simulation bound is256 t_j^2/N_j. With the allocated N_j this is at most zeta t_j/(2S). Summing over all r repetitions and m controlled powers gives at most zeta/2, because their total A-time is S. Ancilla processing, phase measurement, majority classification and failure erasure are CPTP postprocessings, so the diamond errors telescope without extra factors.

Together with section2 the acquired projector instrument has error at most zeta. Appending the known local Bell ancilla and actual V*/3 projector contraction yields exactly the SAME complete original-source guarantee
 distance <=zeta+2epsilon/(3p)
from(p/9 id,(1-p/9)erasure), epsilon=sqrt[5(p+3q)Delta]. Every rate per original channel use must divide by N_train+1. Neither p nor V nor tau is required to run the procedure; p0, zeta, output-register access and known training labels suffice.
