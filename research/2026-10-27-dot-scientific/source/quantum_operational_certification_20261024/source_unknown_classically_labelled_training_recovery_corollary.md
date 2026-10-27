# Receiver-local recovery from ordinary classically labelled qutrit training

Status: separate stronger access-model corollary, pending independent receipt. Root proposed the2-design reset cancellation. Depends on the complete error proof in `source_unknown_signed_choi_programmed_erasure_recovery_theorem.md`, with the EXACT training/time substitution below.

Keep its IID memoryless channel promise E=pV(.)V*+qTr(.)tau, supplied p>=p0>0, known receiver output interface, coherent controlled SWAPs and quantum memory. REMOVE the assumption that a retained sender half of a Choi state is available at the receiver. Training now uses only known qutrit input pure states and their classical labels, or equivalent prearranged shared randomness. No quantum return channel, sender quantum memory, entangled training input, or uncharged transport of a Choi half is used.

## 1. An exact finite labelled program

Choose uniformly from the12 states in four qutrit mutually unbiased bases: the computational basis, and for b,k in{0,1,2},
 |psi_bk>=sum_(x=0)^2 exp[2pi i(bx²+kx)/3]|x>/sqrt3.
This finite ensemble is a complex projective2-design. Its exact moment is
 E_psi[|psibar><psibar| tensor |psi><psi|]=(I9+3Phi3)/12.
The sender sends |psi> through one channel use and supplies its known label. The receiver locally prepares |psibar> in a qutrit register, pairs it with the received output, and ignores the label thereafter. The resulting program density is
 T=E_psi[|psibar><psibar| tensor E(|psi><psi|)]
  =(J+I3 tensor sigma)/4=(J+3omega)/4,
where sigma=E(I3/3), omega=(I3/3) tensor sigma and J is the mathematical Choi state. No physical access to J is presumed. One omega sample is obtained from one I3/3 input and a locally prepared independent mixed qutrit. All samples and labels are IID and independent of the eventual data input. The guarantee concerns the physical programmed instrument after the training labels/randomness are discarded. It is not a guarantee conditional on each realized label sequence, nor a cryptographic guarantee with a public transcript correlated with an adversarially selected data input. The data and its untouched reference are independent of the training preparation.

Consequently the same reset-free signed operator is
 A=J-omega=4(T-omega).
Its unique positive eigenspace remains Phi_V with eigenvalue8p/9; all other eigenvalues are nonpositive. Conjugating the locally prepared training state is load-bearing and is possible because it is selected from a known finite labelled ensemble, not an unknown quantum state to be universally conjugated.

## 2. Exact larger training charge

Use the SAME Hadamard classifier of controlled exp(i pi A). To simulate it from T and omega, run the signed collision simulation for time4pi. The section3 conservative bound becomes
 16(4pi)^2/N=256pi²/N.
For0<zeta<=1 choose
 eta=(zeta/16)^2,
 k=ceil[162 p0^-2 log(1/eta)],
 N_label=ceil[512pi² k/zeta].
The spectral classification contribution is at most zeta/2 and all controlled simulation errors sum to at most zeta/2. Thus the receiver's COMPLETE two-branch projector instrument has error at most zeta, exactly as before. Each of the k tests consumes N_label samples of T and N_label samples of omega, each requiring ONE original channel call. Total usage is therefore
 2k N_label TRAINING calls +1 DATA call per attempted logical input.
This is sixteen times the earlier leading collision-sample budget, not the unmodified J-program count. Labels for the T samples are12-valued; they may be transmitted classically or generated from prearranged shared randomness. No training quantum state is returned from sender to receiver except through the original channel itself.

## 3. Actual decoder and scope

A local known Bell pair plus the acquired positive projector gives the same ideal success Kraus V*/3. For epsilon=sqrt[5(p+3q)Delta], the complete actual instrument is within
 zeta+2epsilon/(3p)
of(p/9 id,(1-p/9)erasure), including arbitrary untouched references. All source trace/normalization and beta bounds are unchanged. Input-dependent acceptance of the approximate device is not silently normalized into a linear channel. The ideal identity throughput p/9 is per DATA attempt; a rate per ORIGINAL use must divide by2kN_label+1 and charge any further distillation losses.

The sample bound is dimension independent but potentially very large. Gate width, output-register storage and controlled-SWAP implementation costs depend on D. The protocol consumes fresh program states for every attempt; it does not output reusable classical decoder software. The channel-family, IID and entropy promises are not verified by this construction. There is no unassisted-capacity or practical-rate assertion.
