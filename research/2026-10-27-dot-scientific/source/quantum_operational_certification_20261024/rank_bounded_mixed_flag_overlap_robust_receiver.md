# Explicit-overlap robustness of the rank-bounded mixed-flag receiver

2026-10-27. New corollary candidate, independent receipt requested. This uses a RESET OVERLAP promise, not a mixed-success entropy-deficit implication.

## Source and claim

Let E(rho)=pV(rho tensor sigma)V*+qTr(rho)tau, p>=p0, rank(sigma)<=r, with V isometric but tau now allowed to overlap the success code. Let Pcode project onto V(C3 tensor supp(sigma)), and define

 beta=q Tr(Pcode tau).

Run exactly the protocol and parameters of `rank_bounded_mixed_flag_exact_erasure_receiver.md` for0<nu<=1, including xi=nu/2 and Htot=sum pair_delta²<=xi/10^6. Then its COMPLETE error from p identity+(1-p)erasure is at most

 0.441nu p+3beta.                                   (1)

In particular beta<=nu p/6 is sufficient for complete error below nu p, with the same O(r²/(p0²nu³)) consumed-sample scaling up to logarithms. Constants are deliberately loose. No claim of optimal overlap tolerance is made.

The reset-cancelled Hamiltonian H=J-omega=4T-4omega is independent of tau, so its code Bell spectra and the low-flag-weight analysis are unchanged.

## 1. Pinched source

Let tau0=Pcode tau Pcode+(I-Pcode)tau(I-Pcode). Its inside-code reset mass is beta; charge its entire complete output by2beta. Its outside reset mass is at most1. The fresh program code weights are now p+beta, and the programs commute with the common code projector.

The received exact sector argument therefore bounds first-import accepted mass by32(p+beta)Htot. The no-import all-label tail remains at mostp xi/100 because the Hamiltonian and its outside zero spectrum are unchanged and uniform simulation bounds do not depend on the program code weight. The genuine good and low-weight success terms are unchanged.

Thus the pinched-source complete error is at most

 0.441nu p+(2+64Htot)beta.                           (2)

No common-sector argument is applied directly to the unpinched source.

## 2. Paired cancellation and full-circuit parity

Interpolate tau(z)=tau0+z tau_off for-1<=z<=1. This is a density operator throughout the interval. Both T(z) and omega(z) have the SAME program derivative

 delta_program=q I_A/3 tensor tau_off,
 d=||delta_program||1=q||tau_off||1,
 d²<=4beta.

The last inequality follows from positivity of tau and the two-block trace-norm bound ||tau_off||1<=2sqrt(a(1-a)), a=Tr(Pcode tau).

Each signed round uses equal/opposite angles h,-h with h=4 pair_delta. The independently received paired-derivative estimates from the earlier near-erasure receiver apply without a projector-rank assumption:

 ||K_z'||_diamond<=12h²d,
 ||K_z''||_diamond<=8h²d².

Let Hsum=sum h²=16Htot. Product differentiation gives processor derivatives

 ||R_z'||<=12Hsum d,
 ||R_z''||<=(8Hsum+144Hsum²)d².

The full composed source channel F(z)=R_z composed E_z also differentiates the original datum, giving

 ||F''(z)||<=(32Hsum+144Hsum²)d².

The unknown sign S=I-2Pcode conjugates tau(z) to tau(-z), while leaving the success channel invariant. Simultaneously conjugating the B parts of the DATA and ALL fresh programs commutes through controlled full-register SWAPs and all known A/control operations. Discarding the physical B registers removes that conjugation. Thus the COMPLETE accepted-logical/erased output obeys F(z)=F(-z), including all branches and external references.

Consequently F'(0)=0 and Taylor's integral remainder gives

 ||F(1)-F(0)||_diamond
 <=(16Hsum+72Hsum²)d²
 <=(64Hsum+288Hsum²)beta.                            (3)

This is a quadratic coherence charge, not a sum of first-order single-program errors.

## 3. Constants and limits

Since Htot<=xi/10^6 and Hsum<=16xi/10^6, with xi<=1/2, the extra beta coefficients in(2)-(3) sum to less than1. Therefore the loose coefficient3beta in(1) is valid.

The parity argument is rank independent because S acts as a scalar on the WHOLE success support, leaving V(rho tensor sigma)V* invariant even for mixed sigma. It uses neither a minimum flag eigenvalue nor a physical measurement of Pcode.

No bound on beta is inferred from Delta for mixed success. The earlier pure-success linear entropy-overlap theorem is not imported; it is known not to extend automatically to mixed main states. This remains a model-plus-explicit-overlap recovery theorem, not a proof for all zero/small-deficit channels.
