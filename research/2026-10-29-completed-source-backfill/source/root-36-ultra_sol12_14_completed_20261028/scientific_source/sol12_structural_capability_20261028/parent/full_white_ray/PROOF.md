# Entire white-noise curves for arbitrary coherent positive rays

Root construction, October28; independently challenged by the quantum lead.
Use qutrits A,B, logical dimension r, A0=P_Omega tensor C,
0<mI<=C<=MI, kappa=M/m, and arbitrary PSD density H on ABL.
Put ell=Tr[(I-P_Omega/3)H]>0 and

    ell0=min(ell,8/9), eps_max=m ell0^4/(2^44 kappa^3 r^5),
    a0=m ell0²/(2^18 r³).

For EVERY0<eps<=eps_max, X=A0+epsH has the ENTIRE curve

    h(a)=Delta(X+aI)>=0, every a>=0.

More quantitatively,

    h(a)>=(epsell+8ra)/2, 0<=a<=a0,
    h(a)>=(3/35)ar m²/(a+M)², a>=a0.                 (1)

## Small noise: use the actual normalized combined perturbation

K=epsH+aI has trace w=eps+9ra and normalized leakage
ell'=(epsell+8ra)/(eps+9ra)>=ell0. For a<=a0,

    eps<=mell0²/(2^18r²),
    w<=10mell0²/(2^18r²)<=mell0²/(2^14r²).

Apply the reviewed sol11 GENERAL_POSITIVE_RAY.md theorem to the ACTUAL
density K/w: Delta(A0+K)>=w ell'/2. This proves the first part(1).
No reset form, diagonalization of H or white-noise grid is assumed.

## Large noise: a finite derivative estimate

The inherited exact baseline is h0(a)=sum_j c_j g(a/c_j), where
g(s)=f(s+3)+9f(s+1/3)-6f(s+1)-4f(s), f(x)=xlogx.
The baseline proof, reproduced below, gives

    h0(a)>=(6/35)ar m²/(a+M)².                       (2)

Integrate entropy derivatives along A0+aI+tH, 0<=t<=eps. Input and E
logs are at least loga. NH is a density, so the N log is at most
log(a+M+eps). All constant derivative terms cancel, giving exactly

    h(a)>=h0(a)-2eps log[1+(M+eps)/a]
         >=h0(a)-2eps(M+eps)/a.                     (3)

For a>=a0, a/(a+M)>=ell0²/(2^19 kappa r³), while eps<=m implies
eps(M+eps)<=2kappa m eps. Divide the last negative term by(2), then use
eps_max: the ratio is at most35/96<1/2. Half of(2) survives, proving(1).

## What is newly received

The EXISTING source-pinned common-bath identity, with q(t)=Tr(tU-V)_+,
states for any base X and finite PSD bath U,V,

    Delta(X tensor U+I tensor V)
      =q'(0+)h(0)+integral_(0,infinity)h(t)dq'(t).

Its positive measure requires the WHOLE curve, not only h(0). Our finite
receiver acquires that premise for every coherent H at the stated radius.
Arbitrary noncommuting/singular U,V are then admitted. The bath identity
is inherited, not rediscovered. Governing source: Git
8d51d60762b3ee28c10aaaa56e1b92da119dc1cc,
white_noise_stability_operator_bath_lifting_theorem.md, cached in sol11.

## Baseline proof and costs

Direct spectra give h0; scale-log terms cancel. Differentiate to get
g''(s)=12(s-1)/[s(s+3)(3s+1)(s+1)]. Concavity on[0,1], g0=0 and
g1=4log(32/27)>=5/8 give g(s)>=5s/8 there. For s>=1, g,g' tend to0,
so g(s)=integral_s^infinity(t-s)g''(t)dt. Restrict to t>=2s, where
g''(t)>=16/(35t³), and integrate: g(s)>=6/(35s). Thus always
g(s)>=(6/35)s/(1+s)². Sum over m<=c_j<=M to prove(2).
This baseline was already used in the earlier reset-only bridge.

For rational inputs the scalar endpoint and a0 have polynomial bit length
in supplied m,M,ell and log r. The small radius explicitly pays
kappa³ r^5/ell0^4. Reading matrices and acquiring PSD/order certificates,
m,M,ell and bath inputs remain separate costs. No physical acquisition,
generic speed advantage or priority claim is made.
At ell=0 absorb the supported H into C and use the known pure-main family;
do not use the displayed radius as positive. Singular C with new leakage
is unpaid. Existing PPT/reduction-positive, low-Schmidt and all-projector
families remain comparators. No arbitrary-source iteration or unrestricted
entropy result follows. The original source, not whitened entropy, is used.

## Exact acquired bath source

compile.py uses r1,m=M=1,H_star=[I9+(E01+E10)tensor diag(1,-1,0)/4]/9.
It has ell=8/9, eps_max=1/28179280429056 and a0=1/331776. Let
U=(1/2)[[1,1],[1,1]], V=diag(1,0); both are PSD projectors and UV!=VU.
For Z=(P_Omega+epsH_star)tensor U+I9 tensor V, its physical marginal is
(4+eps/3)I3, trace12+eps and reference dimension6. It is already TP Choi
after scalar normalization; the antisymmetric extension has dimension54.

The exact bath density is q(t)=(t-1+sqrt(t²+1))/2, so q'(0+)=1/2 and
q''(t)=1/[2(1+t²)^(3/2)]>=1/30 on[1,2]. Since a0<1, (1) implies
h(t)>=3/[35(M+2)²] there. The positive atom and this interval alone give

    Delta(Z)>=epsell/4+1/[350(M+2)²],
    CMI-log3 >=14089640214878/532588400109159975.

This is approximately2.64550e-5 nats. Much of that margin is inherited
white-bath slack, not amplification of the tiny coherent perturbation.
The new admission is the coherent all-white seed and its actual lift.

The exact physical off-diagonal block of X has nonzero square; tensoring
with U preserves it, excluding the old square-zero reset/bath package.
Compression of Z to kerV=|1> gives X/2. On the maximally entangled ray,
X-3EX has positive expectation2-2eps/9, so Z also violates the accepted
reduction-positive premise. Neither exclusion classifies every other
known positive family. Source PSD, physical marginal, block square,
compression and rational receiver constants are checked exactly. The
standard-library acquisition took about.0027s after imports/startup;
the proof and inherited source acquisitions remain separate costs.
