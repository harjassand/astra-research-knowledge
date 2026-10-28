# Entropy-to-reusable recovery for arbitrary overlapping rank-two reset

27 October2026. Source-unknown recovery construction submitted for independent receiving. This is a separately scoped robust extension, not a mutation of the received exact-erasure theorem.

## Physical promise and normalization

Let E(rho)=p V(rho tensor sigma)V*+q Tr(rho)tau, q=1−p, with arbitrary unknown sigma and tau, rank sigma<=r, rank tau<=2, and unknown isometry V into known finite ambient dimension s. Orthogonality of tau and the code is NOT assumed. Supply p0<=p, r, and0<nu<=1. All source access is the received ordinary-labelled mixed-state preparation; all acquired decoding storage is classical.

Use normalized Choi J. With UNNORMALIZED Omega=sum_i|ii>, write

 J=(I tensor V)(P_Omega tensor C)(I tensor V*)+I_3 tensor Y,
 C=p sigma/3, Y=q tau/3,
 A_phys=V(I_3 tensor C)V*=p V(I_3/3 tensor sigma)V*.

Thus Tr A_phys=p and TrY=q/3. Let Delta(J) mean EXACTLY the original homogeneous entropy deficit in low_rank_reset_dimension_free_discrimination_bound_child_proof.md evaluated on THIS J. No other entropy normalization is silently identified with it. Define

 e=(Tr A_phys+TrY−||A_phys−Y||_1)/2.

The separately received rank-two stability theorem gives

    e² <=1944 TrY Delta(J)=648q Delta(J).              (1)

This is the sole entropy import. For q=0 take e=0.

## Analytic comparator, not an oracle

Let B_phys=q tau. Choose an orthogonal projection Q deciding A_phys in the Helstrom problem A_phys versus B_phys, and set

 a_Q=Tr A_phys(I−Q), b_Q=Tr B_phys Q, m=a_Q+b_Q.

Using the optimal test for A_phys versus Y as a candidate for A_phys versus3Y shows m<=3e. Q is used ONLY to prove existence of a comparator; the acquisition/SDP algorithm never receives or implements this unknown test.

Let Pi be the support projector of the genuine normalized Bell Choi block S=p J_success. Its rank is rank sigma<=r. Let P_code be V(I_3 tensor supp sigma)V*. Then Tr_A Pi=P_code/3. Define the accepted comparator decoder

    D_Q,acc(X)=Tr_flag[V* Q X Q V],

restricting the V* output to the actual flag support supp sigma before tracing. Its normalized adjoint Choi effect is

    F_Q=(I_A tensor Q) Pi (I_A tensor Q).

Therefore F_Q>=0, Tr_A F_Q=Q P_code Q/3<=I/3, and TrF_Q<=TrPi<=r. This is feasible for the frozen low-trace decoder decision set, without enlarging its trace budget to3r. Its missing trace is completed by classical erasure.

Write R=I_A tensor Q. Since S is supported on Pi,

 p−Tr(S R Pi R)
 =Tr S(I−R)+Tr S R(I−Pi)R
 <=2 Tr S(I−R)=2a_Q.                                (2)

The inequality follows (I−Pi)R Pi=−(I−Pi)(I−R)Pi and the projector norm bound; it is valid for mixed S with no least-eigenvalue assumption. Hence comparator genuine entanglement weight f_s>=p−2a_Q. Its genuine acceptance a_s<=p. Reset acceptance satisfies a_n=Tr B_phys Q P_code Q<=b_Q.

For H=J−3omega and utility loss L=2p/3−TrHF, the exact reset identity f_n=a_n/9 yields

 L=(2/3)(p−a_s)+(a_s−f_s)+(2/9)a_n.

In particular, using a_s<=p and(2),

    L_Q<= (p−f_s)+(2/9)a_n
         <=2a_Q+(2/9)b_Q<=2m<=6e.                  (3)

This explicitly connects physical discrimination to a feasible learned-decoder comparator. Existence of a known-V inverse alone would not establish(3).

## Transfer through acquired relative learning

Use the low-trace SDP in low_trace_decoder_sdp_relative_learning_root.md:

 maximize Tr Hhat F subject to F>=0, Tr_A F<=I/3, TrF<=r.

All such F are accepted CP trace-nonincreasing decoders; add erasure. The received ordinary-copy acquired-relative estimator on T and omega supplies

 −eta(J+3omega+tI)<=Hhat−H<=eta(J+3omega+tI), t=p0/r.

This acquisition theorem holds for arbitrary state copies and does not need exact erasure. Use eta=nu²/100000 (individual state accuracy eta/10), with one joint training failure probability beta=nu p0/4. The deterministic source cap is the same O(sr/(p0 nu^4)) up to the stated logarithms as the frozen exact-erasure assembly.

For eta<1/6, root's robust variational inequality, including additive objective tolerance kappa, gives

 Lhat <=[(1+6eta)L_Q+(14/3)eta p+kappa]/(1−6eta).

Consequently, for eta<=1/12 and kappa<=eta p0,

    Lhat <=18e+12eta p.                              (4)

The learner needs p0 only, not actual p or e. The tolerance can be chosen from p0. This proof uses the already frozen conservative root inequality rather than requiring a sharper re-analysis.

## Complete error and explicit sufficient entropy regime

Root's operational loss identity gives, for every learned feasible decoder,

 ||Dhat E−G_p||_diamond <=6sqrt(3p Lhat/2)+9Lhat.      (5)

This includes accepted AND erased outputs, arbitrary logical input references, and all reset outcomes. It is not a conditional-on-acceptance fidelity claim. Combining(1),(4),(5) gives the useful risk-sensitive bound on the common good-training event, with e<=sqrt(648q Delta(J)).

As one deliberately conservative numerical sufficient promise, assume

    Delta(J)<=nu^4 p²/10^12.                         (6)

Then e<=sqrt(648)nu²p/10^6, so(4) gives Lhat<nu²p/1000. Equation(5) is below nu p/2. Averaging over the one-off bad-training event adds at most2beta<=nu p/2, proving complete training-averaged error<=nu p at FULL actual throughput p. The bad-training event need not be detected; a separately detected abort is completed by erasure. Future data use no fresh training samples.

## Scope and independent cross-check

The reset may overlap arbitrarily and be spectrally ill-conditioned; the promise is rank<=2 plus the supplied entropy deficit bound. No minimum flag eigenvalue, known reset, known support/eigenbasis, or physical whitening oracle is assumed. The error tolerance(6) is intentionally crude and not claimed necessary. The source remains a reversible main branch plus input-independent reset; arbitrary noisy main channels and higher-rank entropy stability are not received.

An independent nine-band calculation also supports the comparator mechanism: for success Bell blocks S_j (each trace p), N=q I_A tensor tau, H_j=S_j−sum_l S_l/3−2N/3. The rank-r effect (I tensor Q)Pi_j(I tensor Q) has positive-source miss<=2a_Q, other-band mass<=8a_Q and reset mass<=3b_Q, hence variational loss<=4m. This cross-check is weaker than(3) and is NOT a second competing canonical decoder. The low-trace SDP is the operational construction used here.
