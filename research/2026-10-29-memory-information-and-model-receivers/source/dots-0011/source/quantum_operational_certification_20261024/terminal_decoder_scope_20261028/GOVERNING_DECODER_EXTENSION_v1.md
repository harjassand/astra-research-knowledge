# Terminal recovery is an operation, not a choice of notation

28 October 2026. Author derivation and deterministic diagnostic. Independent review requested. This does not supersede the preserved clocked or cadence model: those models explicitly used ideal terminal recovery/decode for the metric. It identifies the operation needed to turn that metric into a physical output.

## The existing map

Let V be the received five-qubit encoding isometry, S its 16-element stabilizer, and E_a the identity plus the 15 single-qubit Pauli errors. Perfection and nondegeneracy give

    V† E_a† E_b V = delta_ab I_2.

The existing ideal decoder is D(rho)=sum_a V† E_a† rho E_a V. Its Kraus operators are not merely the rows of an arbitrary inverse encoding circuit. The 32 columns E_a V|l> form an orthonormal basis, so the unitary U_syn specified by

    U_syn E_a V|l> = |a>_syndrome tensor |l>_logical

implements D after discarding the four syndrome qubits. This is an actual finite unitary target, not free hardware. Compilation, gates, timing and noise must be charged. Equivalently one can measure the syndrome, apply the syndrome-conditioned Pauli correction, and decode. The nonlinear classical syndrome rule is itself part of that alternative operation.

## All bare Clifford decoder extensions

Write L_X=XXXXX, L_Z=ZZZZZ, and L_Y=i L_X L_Z=YYYYY. A Clifford unitary followed by discarding four qubits has output-Pauli adjoints which are one pair of anticommuting physical Pauli operators and their product. To agree with the intended logical identity on V, the pair must be

    A_X=L_X S_x,  A_Z=L_Z S_z,  A_Y=i A_X A_Z,

where S_x,S_z are independently chosen elements of S with their actual stabilizer signs. There are exactly 16^2=256 distinct reduced decoder maps of this type. Conversely, each pair commutes with S and anticommutes with its partner. Extend these vectors and a basis of S to a binary symplectic basis; a Clifford implements the resulting Pauli basis change. Pauli sign corrections fix the chosen signs. The reduced map has

    D_(Sx,Sz)^†(I)=I,  D_(Sx,Sz)^†(sigma_j)=A_j.

Thus every listed map is CPTP and has a Clifford-plus-discard implementation. This is an exhaustive classification of this restricted ideal decoder family, not of adaptive measurement circuits or general CPTP recoveries. Different circuit compilations of the same reduced ideal map can have different noisy performance.

The particular all-site decoder S_x=S_z=I is not automatically the inverse chosen by a separate encoder synthesis. An inverse encoder can use logical normalizers multiplied by stabilizers off the code. The 256 choices are identical on the exact code and generally different on residual syndrome population/coherences.

For the physical Pauli-coordinate convention used in clocked_channel_v1.py, the propagated column for logical input sigma_k is a_Pk=Tr[P N(V sigma_k V†)]. Hence a decoder row has a single coefficient sign(A_j)/2 at the Pauli word A_j; the identity row has 1/2 at I. The program checks D_(Sx,Sz) Enc=I for every pair before evaluating a noisy terminal state.

## Why a bare Clifford decoder cannot supply perfect single-error recovery

Any nonidentity logical output Z has a nonidentity physical Pauli representative A_Z. Pick a site where A_Z is not I, and a single-site Pauli E that anticommutes there. Then E† A_Z E=-A_Z. For the input E V|0><0| V† E†, this decoder's logical Z expectation is -1, whereas an exact single-error recovery must return expectation +1. Therefore no single Clifford unitary followed only by discard agrees with D on all correctable single-qubit errors. In particular U_syn above cannot be a Clifford implementing D in this interface. This elementary obstruction does not apply to Clifford gates WITH syndrome measurements and classically controlled nonlinear corrections.

This is standard stabilizer/decoding structure, used here to close a load-bearing physical interface. Primary background: D. Gottesman, *Stabilizer Codes and Quantum Error Correction*, arXiv:quant-ph/9705052 (1997), Chapter 4 discusses encoding/decoding and the need for an error-correction cycle before decode. https://arxiv.org/abs/quant-ph/9705052 . No historical novelty is claimed for the existence of Clifford encoders or the distinction between decoding and recovery.

## What the numerical comparison means

compare_decoder_extensions_v1.py recomputes the actual physical five-qubit terminal states of six previously declared clock/cadence cases (T=32, background .03/.1/.3 and r=1 or the prior selected r=2/4/8). It compares the old ideal D, the particular all-site bare decoder, and all 256 ideal Clifford extensions. It never inserts an ideal decoder or re-encoder between native uses or EC rounds. Every scheduled EC is still the actual coherent-noisy, background-exposed instrument, including the final one.

The highest scoring extension is a source-informed diagnostic, not an acquired choice. Selection could use a separately paid policy comparison, but no such new data have been generated here. Endpoint Clifford gates are ideal in this diagnostic; the separate noisy-boundary construction must execute them and charge their clock. The prior mandatory-channel/no-bypass, separate native/background phases, inherited frame acquisition, resource comparison and ideal input injection scopes remain unchanged.

The purpose is to determine whether a claimed physical output depends materially on free terminal correction and to expose the remaining operation. It does not revoke a correctly labelled ideal-decoder metric. An ideal output correction can always be used as a diagnostic, but not silently substituted for an executed receiver.

## Exact first-order obstruction under independent depolarizing noise

Suppose an exactly encoded state suffers independent single-site Pauli noise, with X,Y,Z each probability p/3, followed by any ideal bare Clifford decoder in the family. Put q=1−4p/3. For its three physical logical representatives A_X,A_Y,A_Z of weights w_X,w_Y,w_Z, the reduced logical transfer matrix is diagonal with entries q^w_X,q^w_Y,q^w_Z. Therefore

    F_e = [1+q^w_X+q^w_Y+q^w_Z]/4,
    1−F_e = (w_X+w_Y+w_Z) p/3 + O(p²).

Every representative is a nontrivial logical Pauli, so the code distance gives each weight at least 3. The first-order coefficient is consequently at least 3, and this is attained. Exact enumeration gives coefficient3 for70 extensions,11/3 for90,13/3 for90, and5 for6. Equivalently, if u counts sites where A_X or A_Z is nonidentity and v counts sites where both are different nonidentity Paulis, the coefficient is(2u+v)/3. Anticommutation forces v odd. This is an application of code distance and Pauli propagation, not a new QEC threshold theorem.

In contrast, the full ideal recovery D corrects all weight-zero and weight-one terms; its infidelity is at most the probability of two or more physical errors, bounded by10p² using a union over pairs. Thus choosing the best bare Clifford extension cannot preserve the distance-three quadratic cancellation of a true syndrome correction. Avoiding a physical nonlinear correction does not make that correction free. The independent checker exhaustively sums all4^5 Pauli errors at five rational p values for each of the256 extensions and verifies the exact polynomial formula.

## General distance bound

For any [[n,1,d]] stabilizer code, let a Clifford unitary followed by discarding n−1 qubits decode the exact codespace to the intended logical qubit. Its three output-Pauli pullbacks A_j are signed Pauli representatives of the nontrivial logical classes. Thus w_j>=d. Under independent physical depolarizing noise with each nonidentity Pauli probability p/3, the same calculation gives

    F_e = [1+sum_j (1−4p/3)^w_j]/4.

For0<=p<=3/4 the attenuation is nonnegative, so

    F_e <= [1+3(1−4p/3)^d]/4,
    1−F_e >= d p + O(p²) near p=0.

The displayed O(p²) statement expresses the lower bound's expansion; the exact first-order coefficient of every fixed extension is(sum_j w_j)/3>=d. No monotone power inequality is claimed when p>3/4. This is an obstruction for a specified ideal bare Clifford/discard operation after physical noise. A noisy physical decoder is a different channel and must be evaluated on its own; a strategically error-correcting operation is outside the bare-decoder family. Increasing code distance without actually performing syndrome-dependent correction cannot supply autonomous distance-d protection through this interface.
