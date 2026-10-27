# Independent source-unknown quantum-programmed erasure receiving

27 October 2026. PASS for TWO explicit access models: the corrected receiver-local joint-Choi program theorem and the separate ordinary classically labelled-training corollary. Neither is a reusable learned classical decoder, free tomography, model verification, deterministic unknown inverse, practical implementation claim or unassisted rate.

## Exact source and access distinction

The known-register IID channel promise is E=pV(.)V*+qTr(.)tau, V an isometry, p>=p0>0. Parameters V,tau,p need not be known, but the family, IID assumption and entropy bound are supplied promises. Quantum output-register controls/memory and known local ancillas are required.

Exact cancellation J-omega=p Phi_V-(p/9)I3 tensor VV* gives eigenvalues8p/9 on the UNIQUE Phi_V, -p/9 on the eight remaining code modes, and0 outside. The complex-source symbolic checker was replayed. The original theorem now explicitly requires joint Choi programs, including the retained input half, physically local at the receiver or transferred with EXTRA quantum access. Ordinary remote channel calls alone do not provide this resource. This correction was made before this PASS.

## Controlled sample simulation and complete coherence payment

A controlled partial SWAP exp(ih |1><1| tensor S), with fresh independent program rho and discarded program, has first derivative i[|1><1| tensor rho,.] on the entire data/control channel. This includes off-diagonal control blocks, not just the controlled diagonal. Each true and ideal second derivative has diamond norm<=4, since commutator norm<=2 and all preparation/trace maps are CPTP. Integral Taylor remainders give4h^2 difference. Two signed samples cost8h^2; the ideal product-to-sum commutator estimate is at most4h^2, hence the stated16h^2 bound is conservative. Repeated steps telescope without a small-angle asymptotic assumption. Fresh program independence, not unknown classical descriptions, is the premise. Controlled partial SWAP itself can be constructed by coherently extracting the +/-1 full-SWAP eigenvalue, applying the known phase and uncomputing, with a constant number of controlled full-register SWAPs and ancillas.

For time pi, k tests with N steps have total simulation error<=16pi^2 k/N. On the positive eigenstate the Hadamard Y-test mean sin(8pi p/9)>=2p0/9; all other eigensectors have mean<=0. Threshold p0/9 and Hoeffding for[-1,1] give error exp(-k p0^2/162). Conditional-on-eigenstate outcomes are independent because each ideal Kraus operator is a scalar function of A; independence for a superposition is NOT assumed.

The accepted Stinespring operator restricted to Q=I-Phi has norm<=sqrt(eta), and its rank-one Phi block accepts with probability>=1-eta. Decomposing P/Q blocks yields accepted-map diamond error<=2eta+2sqrt(eta), including arbitrary untouched reference. Erasing all rejected outputs costs at most another copy of this bound. Thus8sqrt(eta)=zeta/2 for eta=(zeta/16)^2. Choosing k=ceil(162p0^-2 log(1/eta)), N=ceil(32pi^2 k/zeta) pays the other zeta/2. This is a complete two-branch quantum error, not merely classical classification accuracy.

## Actual inverse map and entropy charge

A receiver-local Bell pair followed by the Phi_V projector contracts exactly to V*/3. Thus the ideal accepted map on the original channel is(p/9)id+Tr(.)Bacc with Bacc=(q/9)V*tau V and beta=Tr(PY)/3. The complete instrument difference from(p/9 id,(1-p/9)erasure) is exactly2beta; the missing success factor9 is explicitly charged.

The already received e2 scalar clock anchor ell has e0=3(d-ell)<=epsilon=sqrt(5(p+3q)Delta), d=p/3. For ell>0, e2(K(ell))=3 implies TrK>=3, hence Tr[V*Y(Y+ell)^-1V]<=e0/d. Functional calculus Y<=(B+ell)Y(Y+ell)^-1 and B+ell<=B+d<=1/3 give Tr(PY)<=e0/p. For ell0, Tr(PY)<=3B<=1=e0/p gives the same result. Therefore beta<=epsilon/(3p). Contractive pre/post-composition of the projector instrument with the actual channel gives total error zeta+2epsilon/(3p). No scalar auxiliary bath is physically decoded.

Accepted probability is at least p/9-zeta. The approximate accepted branch may be input dependent; it is not normalized and mislabeled as a linear channel. The stated conditional state estimate follows by subtracting the accepted trace times the target state, charging2beta+2zeta and dividing by the positive lower acceptance. Source calibration is replaced by quantum training access, not by an uncharged verification or learning claim.

## Receiver-local classically labelled training

Independently verified all81 matrix entries of the exact12-state conjugated qutrit MUB moment using finite-field character orthogonality, and replayed the author's symbolic checker. The moment is(I9+3Phi3)/12. Applying id tensor E gives T=(J+I3 tensor sigma)/4=(J+3omega)/4, so A=4(T-omega). A T sample requires one known pure input and its classical label; the receiver prepares the KNOWN conjugate state locally. No universal conjugation of an unknown state is attempted. An omega sample uses one mixed input plus an independent local mixed qutrit. Labels and programs are fresh IID and independent of the data input.

This simulates time4pi for T-omega, so per test error is256pi^2/N. N_label=ceil(512pi^2 k/zeta) supplies the same total zeta instrument error. Each data attempt consumes2kN_label TRAINING channel calls and1 DATA call. The factor16 collision-budget increase is essential. No sender quantum memory, retained Choi-half transfer, entangled training input or quantum return link is required in this second access model. The receiver still needs coherent operations on the actual output register and local quantum memory.

Sample count is dimension independent, but gate width/storage/controlled-SWAP implementation costs are not. Every attempt consumes fresh programs; no reusable classical decoder is produced. Any per-original-use rate must divide by2kN_label+1 (or2kN+1 in the stronger original access model) and separately pay further postselection/communication. Unknown memoryful channels, inaccessible output registers, or unverified family/entropy promises are outside the theorem.

## Averaging and transcript scope

The diamond guarantee is for the implemented channel after fresh training labels/randomness are discarded, with data and its untouched reference independent of that preparation. It is NOT a guarantee for each realized public training transcript or for an adversarially transcript-conditioned input. This explicit scope sentence was appended by the author before the final receipt hash; the mathematical source/program/error checks are unchanged.
