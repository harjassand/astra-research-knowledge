# Reusable rare-throughput recovery from infidelity tomography

2026-10-27. Constructive proof candidate; independent receiving requested. This improves the generic reusable baseline without claiming an optimal reusable signal exponent.

## Promise and conclusion

Let E be a qutrit-input memoryless channel with known finite output dimension s. A known0<p<=1 is promised to admit some CPTP complete decoder D_* with

 D_* E = G_p,   G_p(X)=p X accepted +(1-p)Tr(X)|erase><erase|.

No source-dependent quantum program is retained at deployment. The construction below learns a classical description of a reusable complete decoder using collective normalized Choi-state tomography and a fidelity-maximization SDP.

For0<nu<=1 it achieves training-averaged unhalved diamond error at most nu p with source-copy cost

 O(s²/(nu²p)) times logarithmic dimension/accuracy/confidence factors.

If the true normalized Choi state has rank R, the tomography factor s² can be replaced by sR. This R is CHOI rank, not necessarily the success-flag rank. The normalized Choi copies are prepared by fresh maximally entangled qutrit/reference probes, one physical source call per copy.

For the canonical ambient3D rank-r/signal-p family, generic Choi rank is O(D), so this gives a one-off reusable O(D²/p)=O(r²/p³) fixed-relative-accuracy upper, up to logarithms. It improves the generic trace-tomography O(r²/p⁴) baseline. The received consumed-program construction and adaptive lower scale r²/p²; no matching reusable p² upper is asserted here.

## 1. Learn in infidelity, then optimize fidelity directly

Use root fidelity F(rho,sigma)=||sqrt(rho)sqrt(sigma)||1. Suppose tomography produces a density estimate J_tilde with

 1-F(J_tilde,J_E)<=delta.

The reference marginal of J_tilde need not be exactly I3/3. Choose a CPTP decoder D_hat maximizing

 F((id3 tensor D)(J_tilde), J_(G_p)),

to additive fidelity accuracy at most delta. Enforce an explicit classical accepted/erased flag by dephasing those two output sectors; this is a linear channel constraint, or can be applied after optimization. The target is invariant under this dephasing, so fidelity cannot decrease. The objective has the standard block-positive fidelity SDP, and its first argument is linear in the decoder Choi matrix. Explicitly, fidelity is the maximum of Re Tr X subject to the positive block matrix with diagonal blocks sigma and J_(G_p), so decoder CPTP constraints can be included in the same SDP. No nonconvex model fit or unstable channel inverse is used.

The true D_* achieves fidelity at least1-delta by monotonicity. Thus the optimized estimated output has fidelity at least1-2delta with the target. Bures distance b(rho,sigma)=sqrt(2-2F) obeys the triangle inequality and contracts under channels. Therefore the ACTUAL recovered Choi state R=(id tensor D_hat E)(Phi3) satisfies

 b(R,J_(G_p)) <=sqrt(2delta)+sqrt(4delta),
 1-F(R,J_(G_p)) <=(1+sqrt2)² delta <6delta.             (1)

With exact optimization the factor6 can be replaced by4, but that sharpening is unnecessary.

## 2. Rare accepted mass improves the fidelity-to-recovery conversion

Let any complete qutrit/erasure channel have normalized Choi state R and root infidelity epsilon to

 K_p=J_(G_p)=p Phi3 accepted +(1-p)I3/3 tensor|erase><erase|.

Take Uhlmann purifications |psi>,|phi> with squared vector distance2epsilon. Write e=sqrt(2epsilon), and project both onto the accepted output sector. The ideal accepted vector has norm sqrt(p), the actual accepted vector differs by at most e, and hence its norm is at most sqrt(p)+e. Partial trace and the rank-one operator triangle bound give

 ||R_acc-p Phi3||1 <=(2sqrt(p)+e)e.

Both channels are trace preserving, so their reference marginals are I3/3. Their erased-reference block difference is minus the logical-output partial trace of the accepted-block difference. Therefore its trace norm is at most the accepted-block trace norm. Consequently

 ||R-K_p||1 <=4sqrt(p)e+2e²
             =4sqrt(2p epsilon)+4epsilon.

For a qutrit input, the unhalved diamond norm is at most3 times normalized-Choi trace norm. Thus

 ||D_hat E-G_p||diamond
 <=12sqrt(2p epsilon)+12epsilon.                       (2)

This is a COMPLETE instrument estimate. Without trace preservation and an explicit classical erased output, the reject-block argument cannot simply be reused.

By(1),(2), on the tomography-good event the error is at most

 12sqrt(12p delta)+72delta.

Taking delta=nu²p/10000 makes this less than nu p/2 for0<nu<=1.

## 3. Sample cost and confidence

[Haah, Harrow, Ji, Wu and Yu, Sample-optimal tomography of quantum states, arXiv:1508.01797v2](https://arxiv.org/html/1508.01797) gives a collective-copy estimator in dimension d and rank at most R with infidelity accuracy delta using O(dR/delta) times logarithmic factors. Its Eq(14) explicitly bounds the bad-estimate probability by (n+1)^(3dR) exp(-2n delta), so choose n with2n delta>=3dR ln(n+1)+ln(1/beta). Its convention is the same root infidelity used above. Here d=3s; the generic R<=3s case gives the stated s² factor.

To obtain an unconditional training-averaged complete error at most nu p, choose tomography failure probability beta<=nu p/4. On failure any complete-channel difference is at most2, so

 averaged error <=nu p/2+2beta<=nu p.

The confidence dependence, including log(1/p), must be included in the sample count; constant failure probability would not be sufficient for rare-throughput unconditional error. Finite-precision SDP/implementation error is charged within the remaining slack or by making delta smaller by a fixed factor.

The theorem is a source-sample upper, not a cheap collective-measurement, memory, or classical-runtime claim. The learned description is reusable, but an M-datum joint-channel guarantee on the good event costs up to M times the per-datum error. The one-off bad-decoder event is accounted separately. No quantum training state is being recycled.

## Next unresolved comparison

The canonical model has only O(rD) nontrivial orientation parameters, suggesting that a STRUCTURED infidelity estimator might improve the one-off cost to O(D²) at fixed relative accuracy. This would require a received finite-sample model-estimation theorem or construction. Pairwise discrimination of a separated net alone does not justify a robust estimator for every source near that net. No such sharper upper is part of the present result.
