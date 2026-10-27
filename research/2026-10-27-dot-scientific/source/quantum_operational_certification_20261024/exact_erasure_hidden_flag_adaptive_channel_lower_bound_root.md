# Hidden orthogonal flags force quadratic training even with adaptive channel access

27 October 2026. Root analytical construction; independent receipt requested. This extends the separately frozen T-program lower bound to actual channel calls by an explicit common teleportation simulation. No accuracy-exponent or all-p interpolation claim is made.

Let D>=2, p=1/D, and let the receiver output be C3 tensor CD. For a unit vector psi in CD write Ppsi=|psi><psi|. Choose U either I3 or the cyclic qutrit shift X3. Define

 E_(U,psi)(rho)=[U rho U* tensor Ppsi + Tr(rho) I3/3 tensor (I_D-Ppsi)]/D.

This is the promised isometry-plus-replacer family with Vx=Ux tensor psi and reset tau=I3/3 tensor (I-Ppsi)/(D-1). Reset and code supports are orthogonal; the entropy deficit is EXACTLY zero by the received equality classification. The source is fixed across every call; Haar mixing below is only a lower-bound prior over fixed sources.

## Claim
Any source-independent deterministic receiver that implements the inverse on code inputs with complete UNHALVED diamond error at most zeta<1 for EVERY member of this family, using at most n calls to that same unknown channel, must satisfy

 n >= (D^2/8) [1 - 1/sqrt(1+(1-zeta)^2)].

In particular zeta<=1/4 requires n>=D^2/40=1/(40p^2). The calls may be adaptive with arbitrary source-independent ancillas, quantum memory, and collective processing. This is a lower bound for the inverse on received code states, NOT for an unconditioned composed noisy-recovery channel or an accepted-only postselection claim.

## 1. Full normalized Choi programs
Let Phi_U=(I tensor U)Phi_3(I tensor U*) on C3 tensor C3, with Phi_3 normalized. The normalized Choi state is

 J_(U,psi)=I9 tensor I_D/(9D)+(Phi_U-I9/9) tensor Ppsi/D.

The maximally mixed-input output and corresponding omega are independent of both U and psi. Thus unlimited copies of these fixed states convey no additional parameter information.

Writing B_U=Phi_U-I9/9 gives TrB_U=0 and TrB_U^2=8/9. For t=|<psi,phi>|^2,

 Tr[J_(U,psi) J_(U,phi)]=(1/(9D))(1+8t/D).

## 2. One common deterministic teleportation simulation
Take the nine qutrit Weyls W. On an arbitrary channel input and the input-reference half of J, measure the orthonormal Bell vectors

 |Bell_W>=(I tensor conjugate(W))|Omega_3>/sqrt(3).

Before applying E to the resource output, contraction of this Bell bra with input x tensor |Omega_3>/sqrt(3) produces W x/3. Hence the unnormalized received output for outcome W is E(W rho W*)/9, including any untouched reference.

Both candidate U are Weyls. They commute with every W up to a scalar phase, while the replacement output has logical factor I3/3. Therefore exactly

 E_(U,psi)(W rho W*)=(W tensor I_D) E_(U,psi)(rho)(W* tensor I_D).

Applying W* tensor I_D corrects each outcome to E(rho)/9. Summing the nine outcomes simulates the channel exactly. The measurement and correction use neither U nor psi. No flag-basis measurement, spectral whitening, or source-dependent oracle is supplied.

Replacing every use in any adaptive strategy by this same simulator expresses its final output as ONE CPTP map Lambda of J_(U,psi)^tensor n and its supplied data/ancillas. Lambda is independent of U and psi. Strategies with fewer than n calls can be padded with discarded resource states. Classical measurement records are retained inside Lambda as needed; this does not assume parallel physical training.

## 3. Haar prior with an independent received code datum
Supply the SAME physical logical state |0><0| to the receiver under both hypotheses, together with the data flag Ppsi. This is a valid code datum: its required inverse is U*|0><0|U. For U=I and U=X3 these required logical states are orthogonal. The flag shares the fixed source parameter psi with the programs, but is a separate conditional product datum; this matches a fixed memoryless channel and independent data.

After Haar averaging psi, all source-dependent inputs to Lambda are

 S_U=E_psi[J_(U,psi)^tensor n tensor Ppsi].

A fixed logical |0> and other source-independent states may be suppressed. Let B be maximally mixed on dimension (9D)^n D. The exact second moment yields

 chi2(S_U||B)=((9D)^n D)Tr(S_U^2)-1
             =E_t[D t(1+8t/D)^n]-1.

For independent Haar vectors in CD, E[t^k]=k!/(D)_k. With x=8n/D^2<1, use (1+8t/D)^n<=exp(8nt/D) and (D)_(k+1)>=D^(k+1) to get

 E[D t exp(8nt/D)]
 =sum_(k>=0) (8n/D)^k D(k+1)/(D)_(k+1)
 <=sum_(k>=0)(k+1)x^k=(1-x)^(-2).

All terms are nonnegative, so the interchange is monotone convergence. Trace Cauchy-Schwarz against the maximally mixed B gives

 (1/2)||S_U-B||_1 <=(1/2)sqrt(chi2(S_U||B)).

Thus (1/2)||S_I-S_X||_1<=sqrt((1-x)^(-2)-1).

## 4. Contradiction with uniform inverse accuracy
The unhalved diamond guarantee implies each averaged final output is within trace norm zeta of its required pure logical state. Since these target states are orthogonal, their output half-distance is at least 1-zeta. CPTP contraction and the preceding bound imply

 1-zeta <=sqrt((1-8n/D^2)^(-2)-1)

whenever n<D^2/8. Rearrangement gives the claimed lower bound. If n>=D^2/8, that bound is automatic. At zeta=1/4 the bracket is 1-4/5=1/5, giving D^2/40.

## Scope and comparison
This proves a worst-case Omega(p^-2) channel-query obstruction along p=1/D, with growing receiver dimension3D and EXACT orthogonal erasure. It is consistent with every fixed separated pair having linear-p information: the hard instances use a many-source unknown-code prior. It does not contradict approximation bounds independent of raw output dimension at fixed p, since here D=1/p. It does not establish a 1/zeta factor in this promise family, a lower bound for known code/support, or impossibility of efficient recovery of the original noisy channel without the received-system inverse requirement. The same simulation covers arbitrary adaptive physical training, a stronger access model than the T-copy receiver.
