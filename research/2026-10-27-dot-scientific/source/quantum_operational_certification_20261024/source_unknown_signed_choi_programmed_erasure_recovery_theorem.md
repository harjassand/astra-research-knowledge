# Finite quantum-training recovery without learning the output isometry

Status: new self-contained construction, pending independent receipt. Root proposed the signed-Choi cancellation; the finite controlled-partial-swap/Hadamard implementation and entropy charge are acquired here. This is not free tomography, a programmable deterministic inverse, a reusable learned classical circuit, or verification of an unknown channel model.

## 1. Explicit access promise and output guarantee

There is an IID memoryless channel E(rho)=p V rho V*+q Tr(rho)tau, V:C3->C^D isometric, p+q=1, and a supplied lower bound p>=p0>0. V,tau and the actual p need not be known. The output-register interface and its finite dimension are known, with coherent controlled register SWAPs, quantum memory, known qutrit Bell pairs and ordinary ancilla gates available. In THIS first access model the joint Choi program, including the retained input half, must be available locally at the receiver (for example local training access or explicitly supplied quantum transfer of that half). Ordinary remote forward channel access alone does not supply that resource. The separate labelled-training corollary removes this extra quantum-access assumption with a larger charged sample budget. The model and entropy promise are assumed, not certified by this protocol.

Let Delta denote the original normalized source deficit and epsilon=sqrt[5(p+3q)Delta]. For any chosen0<zeta<=1 the construction below consumes a FIXED finite number2kN of training channel uses and one data channel use per attempt, where
 eta=(zeta/16)^2,
 k=ceil[162 p0^-2 log(1/eta)],
 N=ceil[32 pi^2 k/zeta].                                      (1)
It implements an actual two-branch received-system operation (accepted logical qutrit, erased failure) whose COMPLETE joint diamond distance from
 (p/9 id, (1-p/9) erasure)
is at most

 zeta+2epsilon/(3p).                                         (2)

All training states are consumed, and the factor9 identity-throughput cost is explicit. The number of channel samples is independent of D. Quantum storage, controlled-SWAP gate width and physical implementation costs are NOT independent of D. This is an ideal circuit/access-model theorem, not a hardware or finite-observation model-identification assertion.

## 2. An exactly reset-free signed Hamiltonian from obtainable states

One training channel call on half of a known Bell pair prepares
 J=p|Phi_V><Phi_V|+q(I3/3) tensor tau.
One channel call on I3/3, plus an independent known mixed qutrit label, prepares
 omega=(I3/3) tensor sigma,
 sigma=E(I3/3)=p P/3+q tau, P=VV*.
Both J and omega are density operators on the SAME known3D-dimensional register type. Their difference is
 A=J-omega=p|Phi_V><Phi_V|-(p/9) I3 tensor P.
Its spectrum is+8p/9 on the UNIQUE vector Phi_V, -p/9 on the other eight code modes, and zero off the code. This uses no unknown basis rotation or oracle. The task is to approximate its positive spectral projector using only copies of J and omega.

## 3. Controlled sample simulation, with explicit diamond cost

For any density operator rho, let S exchange a data register and one fresh program register in state rho. With a control qubit, apply exp(i h |1><1| tensor S), then discard the program. The induced channel and controlled exp(i h rho) have the SAME first-order generator, i[|1><1| tensor rho,.]. Each second derivative has diamond norm at most4, since the corresponding Hermitian generator has operator norm at most1. Taylor's integral remainder therefore bounds their diamond difference by4h^2. The argument includes arbitrary untouched reference systems and control coherences. Negative h is allowed at the same cost.

Use one J copy with+h and one omega copy with-h. Their two simulation errors total at most8h^2. The ideal controlled-unitary product differs from controlled exp(i h A) by at most4h^2 in diamond norm (the commutator Duhamel bound even gives2h^2). Thus the conservative bound16h^2 is valid for one signed step. Repeating N steps of h=pi/N gives controlled exp(i pi A) to diamond error at most16pi^2/N, using2N training calls. All bounds are dimension independent and require no classical descriptions of the two states.

Known controlled partial SWAPs can be implemented with a constant number of controlled full-register SWAPs and ancilla rotations using the two eigenspaces of S. Each full-register SWAP acts on O(log D) qubits when that encoding is used; this cost is charged rather than hidden. Programs can be supplied sequentially, so simultaneous large-register memory need not grow with the total sample count.

## 4. Finite spectral discrimination with coherent accepted-branch control

An ideal Hadamard test with the appropriate Y-basis sign, using controlled exp(i pi A), has outcome in{+1,-1} with mean sin(pi a) on an A eigenvector of eigenvalue a. On Phi_V, a=8p/9 and
 sin(8pi p/9)>=2p0/9.
Indeed sin(theta)>=(2/pi)min(theta,pi-theta) on[0,pi], and p0<=p<=1. On every other eigenspace a=-p/9 or0, the mean is<=0.

Perform k such tests, recording their outcomes, and accept exactly when the empirical mean is at least p0/9. Conditioned on an A eigenvector the tests are independent and preserve that eigenvector up to scalar amplitudes. Hoeffding's bound for variables in[-1,1] gives both the positive false-reject probability and the other-sector false-accept probability at most
 exp(-k p0^2/162)<=eta.

Misclassification alone is not the complete quantum error. Let Pphi=|Phi_V><Phi_V| and Q=I-Pphi. The accepted Stinespring map has Q operator norm at most sqrt(eta), while its Pphi acceptance probability is at least1-eta. Since Pphi is rank one, the accepted Pphi block is exactly a scalar multiple of Pphi(.)Pphi. Splitting an arbitrary reference-entangled input into its Pphi/Q blocks bounds the accepted-map diamond error from Pphi(.)Pphi by2eta+2sqrt(eta). Replacing all rejected outputs by one erasure flag at most doubles this bound. Thus the FULL erased instrument error is at most8sqrt(eta)=zeta/2.

Now replace each controlled unitary by section3's sample simulation. The k errors telescope through all measurements and classical processing to at most k16pi^2/N<=zeta/2. The actually implemented full erased projector instrument is therefore within zeta of the ideal one. No assumption of independent classical outcomes for a general superposition is made; independence was used only to bound spectral acceptance, and accepted coherences were charged separately.

## 5. Actual inverse map, source charge and entropy estimate

Prepare a known qutrit Bell pair |Phi3>_OC and use C together with the fresh received output as the DATA register for the preceding projector procedure. On acceptance discard C and the received output and retain O; on failure erase. The exact projector satisfies
 (<Phi_V|_CB tensor I_O)(|Phi3>_OC tensor |chi>_B)=V*|chi>/3.
Thus its ideal received-system success Kraus operator is V*/3, not V* and not a deterministic inverse. On the original channel its accepted map is exactly
 S(rho)=(p/9)rho+Tr(rho) Bacc,
 Bacc=(q/9)V*tau V,
 beta=TrBacc=Tr(PY)/3, Y=q tau/3.
The success probability is p/9+beta, input independent. Erasing failure, the complete joint distance from the reduced-rate ideal(p/9 id,(1-p/9)erasure) is EXACTLY2beta.

For completeness the entropy control of beta is acquired directly from the new scalar e2 clock, rather than an unimplemented auxiliary decoder. Put d=p/3 and B=||Y||. Let ell be its scalar anchor and e0=3(d-ell), as in `pure_success_entropy_only_polar_erasure_recovery_theorem.md`; that theorem proves e0<=epsilon. If ell>0, e2(K(ell))=3 implies TrK(ell)>=3, so
 Tr[V*Y(Y+ell I)^-1V]=3-(ell/d)TrK(ell)<=3(1-ell/d).
Functional calculus gives Y<=(B+ell)Y(Y+ell I)^-1. Consequently
 Tr(PY)<=(B+ell)e0/d<=e0/p,
using B+ell<=B+d<=(p+q)/3=1/3. If ell=0 the same conclusion follows from Tr(PY)<=3B and e0=3d. Hence beta<=epsilon/(3p).

The implemented projector instrument differs from the ideal projector instrument by at most zeta before the original channel is composed; composition cannot increase diamond distance. This proves(2), for arbitrary untouched references and with both acceptance and failure charged. The actual approximate accepted map may have input-dependent probability; no nonlinear normalized map is called a channel. If desired, a known input/output qutrit unitary twirl makes acceptance input independent, without increasing the joint error, but is not needed for(2).

For Delta=0 this gives arbitrarily accurate heralded inversion at ideal identity throughput p/9, with an explicit finite training budget for every zeta>0. More generally a positive lower acceptance bound is p/9-zeta, and a conservative conditional state error relative to the identity is at most[2epsilon/(3p)+2zeta]/(p/9-zeta), whenever the denominator is positive. No rate per original channel use may omit the2kN training calls: any communication or distillation protocol must divide by2kN+1 and charge its further postselection/classical communication separately.

## Provenance and remaining scope

The standard sample-Hamiltonian paradigm is described by Kimmel et al., https://arxiv.org/abs/1608.00281 and https://www.nature.com/articles/s41534-017-0013-7 . The controlled first-order identity and conservative finite diamond bounds used here are explicitly proved in section3, rather than imported numerical constants. The generic two-program antisymmetric inverse and its noisy-program failure are separately frozen in `two_program_unknown_isometry_inverse_and_noise_guard.md`; that simpler primitive does not supply this signed-projector theorem.

The protocol neither learns V classically nor verifies the IID isometry-plus-reset promise or Delta from a dimension-independent number of observations. It requires access to coherent operations on the known output registers. Ordinary classical-output training, inaccessible environment registers, unknown memoryful channels, and reusable software-only decoders are different models and are not covered.
