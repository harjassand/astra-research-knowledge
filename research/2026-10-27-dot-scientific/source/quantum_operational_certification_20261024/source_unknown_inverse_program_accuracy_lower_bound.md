# Accuracy-dependent lower bounds for the actual discarded-label inverse programs

Status: new self-contained lower bound, pending independent receipt. This is a stronger complementary result to `source_unknown_program_training_lower_bound.md`. It concerns approximate DETERMINISTIC received-system inversion from the specified IID T programs, not arbitrary labelled/adaptive training or only the channel-composed recovery error.

Let a processor consume n>=1 IID discarded-label program states T_U (plus any U-independent ancillas/omega programs) and then act on an independent data system. Suppose its complete output channel, including any erasure flag, is within unhalved diamond distance zeta of the deterministic inverse U*(.)U uniformly in U. Define
 C=4225/248832.

For the actual white-reset channel family E_U=pU(.)U*+(1-p)Tr(.)I3/3, its programs T_U=(p/4)Phi_U+(1-p/4)I9/9 necessarily satisfy

 zeta>=C min{1,1/(n p²)}.                               (1)

Thus for zeta<C, n>=C/(p² zeta). This matches the received QPE/nine-Bell construction's signal and accuracy powers up to logarithmic factors for THIS general program-learning task. It is not an optimality claim for an entropy-restricted recovery task: the white-reset hard family may lie outside a small-deficit promise.

A separate hard family with EXACT original Delta=0 gives

 zeta>=C min{1,1/(n p)}.                                (2)

It uses reference/output dimension4, a fixed3D code, V_U equal to U embedded in that code, and reset tau on its one-dimensional orthogonal complement. This distinguishes the rare clean-code-sample regime from the weak signal buried in full-rank white noise. No p^-2 lower bound is inferred for every zero-deficit family.

## 1. Approximate programming lemma, proved from the actual Choi state

Take two pure program purifications |P0>,|P1> with real overlap r>=0. A processor can ignore any purifying registers, so a lower bound proved after granting them is valid for the original mixed programs. Purify the fixed processor itself. Its two induced Stinespring isometries V_i on a qutrit data input satisfy EXACTLY
 V0*V1=r I3.
Suppose the output channels are within diamond distance zeta of U_i*(.)U_i. Feed a normalized maximally entangled qutrit data/reference state. Its actual pure global output |Omega_i> has reduced overlap at least1-zeta/2 with the ideal pure inverse Choi vector. Projecting onto that vector and normalizing produces an environment vector |e_i> with
 ||Omega_i-Phi_(U_i inverse) tensor e_i||<=sqrt(zeta).
Normalized vectorization then gives
 ||V_i-U_i* tensor e_i||_op<=sqrt(3zeta).
This argument uses the actual pure-output Choi fidelity; no generic continuity theorem or guessed diamond/infidelity conversion is needed.

For zeta<=1/3, expanding V0*V1 yields
 ||rI3-c U0 U1*||<=2sqrt(3zeta)+3zeta<=3sqrt(3zeta),
where c=<e0,e1>. Choose U0=I and U1=diag(exp(i theta),exp(-i theta),1), with0<theta<=1. For ANY complex c, the two opposite-phase entries give
 max(|r-c exp(i theta)|²,|r-c exp(-i theta)|²)
 >=r²+|c|²-2r Re(c)cos(theta)
 =|c-r cos(theta)|²+r²sin²(theta).
Consequently
 zeta>=r² sin²(theta)/27.                              (3)
If zeta>1/3 the final lower bounds(1)-(2) are automatically true since C<1/3.

## 2. Exact mixed-program overlap for white reset

Put a=p/4,b=(1-a)/9. The two Choi vectors have squared overlap
 t=[(1+2cos(theta))/3]².
On their two-dimensional span, T0=bI+aP0 and T1=bI+aP1. The trace of the square root of their positive product is obtained from its trace and determinant; outside the span there are seven common eigenvalues b. Their root fidelity is exactly
 r1=7b+sqrt[4b(a+b)+a²t]
   =7b+sqrt[(a+2b)²-a²(1-t)].
The polar factor of sqrt(T0)sqrt(T1) explicitly chooses program purifications with this overlap. For n independent copies their overlap is r=r1^n.

Since a+2b>=(2/9),
 1-r1=a²(1-t)/[a+2b+sqrt((a+2b)²-a²(1-t))]
       <=(9p²/32)(1-t).
Also for0<=theta<=1,
 1-t=(4/9)(1-cos(theta))(2+cos(theta))<=2theta²/3.
Therefore1-r1<=3p²theta²/16. Choose theta=min{1,1/(p sqrt n)}. Bernoulli's inequality gives r>=1-3np²theta²/16>=13/16. The elementary integral/Taylor bound sin(theta)>=theta-theta³/6>=5theta/6 and(3) now give
 zeta>=(13/16)²(5/6)² theta²/27
       =C min{1,1/(np²)},
proving(1).

## 3. Exact zero-deficit hard family

Let P be the fixed first-three-coordinate code in C4, V_U=[U;0], and tau=|3><3|. The original source has an orthogonal success/reset split, so its original deficit is exactly zero for every U and every p. The local marginal sigma=pP/3+q tau is independent of U.

Its labelled T program splits into orthogonal receiver sectors:
 T_U=p [Phi_U/4+I9/12] direct_sum q [I3/3 tensor tau].
The conditional code program is exactly the previous white-program expression at p=1, and the outside program is identical for both unitaries. Hence its one-copy root fidelity is r1_zero=q+p r1_code, so
 1-r1_zero<=3p theta²/16.
Choose theta=min{1,1/sqrt(np)}. The SAME pure-program argument, with the independent DATA restricted to the fixed code, gives r>=13/16 and then(2).

The ideal received-system inverse is deterministic on that fixed code; an outside erasure flag does not affect the proof. A guarantee only AFTER the unknown noisy channel is composed with the decoder is a weaker task and is not silently substituted for this received-system inverse guarantee.

## 4. Resource interpretation and remaining gap

The processor is otherwise arbitrary; it is not restricted to partial-SWAP simulation or phase estimation. It may jointly measure all its T copies, retain quantum memory, and use any U-independent processing. However the quantitative bounds rely on the precise discarded-label program states above. They do not exclude an improvement obtained by retaining labels, changing training probes, using adaptive channel queries, or accepting a much smaller explicitly charged inverse rate.

For the actual QPE full-Bell implementation, the number of informative T copies is half the total collision-program calls, and its dependence is O[p0^-2 log²(1/zeta)/zeta]. Thus the p^-2 and zeta^-1 powers are necessary in the general white-reset discarded-T deterministic-inverse task; logarithmic and constant improvements remain open. On the zero-deficit subfamily only the weaker p^-1 signal lower bound is acquired here, leaving room for a genuinely better promise-adapted learner. This is a resource obstacle, not evidence of a practical rate or a general impossibility of quantum recovery.

## 5. Stronger independent proof by repeated retrieval and relative entropy

Root supplied the following simpler independent argument, avoiding the Stinespring environment-vector lemma and improving the constant. For0<zeta<=1/16 it proves

 n>=49/[64 pi² p² zeta]  (white-reset discarded T programs),
 n>=49/[64 pi² p zeta]   (the EXACT Delta0 orthogonal-reset family).       (4)

Let L=floor[1/(8zeta)]>=2, theta=pi/(2L), U0=I and Utheta=diag(exp(i theta),exp(-i theta),1). Compose L copies of the learned inverse processor, using FRESH independent n-program batches. Only local operations are used during retrieval; the nL training programs may all be prepared before the data arrives. If the processor includes an erasure flag, apply a fixed local fallback mapping that flag to |0> before the next retrieval. This CPTP postprocessing leaves each channel within zeta of its ideal unitary inverse, so it resolves the composition-domain issue without granting an extra channel query.

On input(|0>+|1>)/sqrt2, the two ideal L-fold inverse outputs are orthogonal. Each actual L-fold channel differs from its ideal by at most Lzeta in unhalved diamond norm. Hence the HALF trace distance of the two actual output states is at least1-Lzeta>=7/8. Quantum Pinsker (natural logs), or measurement data processing followed by classical Pinsker, gives output relative entropy at least49/32.

For T_i=bI+aPhi_i, the spectral logarithm is log b I+log(1+a/b)Phi_i. Therefore its exact one-program relative entropy is
 D(T0||Ttheta)=a log(1+a/b)(1-t),
 t=|TrUtheta/3|²=[(1+2cos theta)/3]².
Here a=p/4, b>=(1/12), log(1+a/b)<=a/b<=3p, and1-t<=2theta²/3. Thus
 D(T0||Ttheta)<=p²theta²/2.
All omega programs are identical between the two hypotheses. Relative entropy additivity and data processing through the entire composed processor consequently give
 49/32<=nL D(T0||Ttheta)<=n p²pi²/(8L).
Thus n>=49L/(4pi²p²). Since floor[1/(8zeta)]>=1/(16zeta) for zeta<=1/16, the first bound(4) follows.

For the Delta0 family, the common orthogonal decomposition has identical weights p,q and identical outside state. Its relative entropy is EXACTLY p times that of the conditional p=1 code programs, hence at most p theta²/2. Repeating the same proof yields the second bound(4).

These bounds apply to a uniform single-retrieval guarantee and do not assume one can reuse its consumed program. Fresh programs are explicitly multiplied by L in the proof. They neither lower-bound arbitrary raw labelled/adaptive training nor imply p^-2 optimality within the exact-zero-deficit promise. The first Stinespring argument remains an independent corroborating route; the stronger numerical constants in(4) are the governing quantitative bounds for zeta<=1/16.
