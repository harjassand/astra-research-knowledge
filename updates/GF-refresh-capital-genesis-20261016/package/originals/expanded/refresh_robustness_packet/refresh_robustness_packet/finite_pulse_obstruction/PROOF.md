# Exact obstruction to treating compiled stabilizer pulses as free refresh

16 October 2026. A mathematical counterexample, not a measured device result or a general impossibility of physical refresh.

Let two qubits have stabilizer generators ZZ and XX, and good projector P=(I+ZZ)(I+XX)/4 onto Phi+=(|00>+|11>)/sqrt(2). Let S=ZZ, and let the otherwise free baseline be H=J(I-XX)/2. It commutes with every stabilizer and P, so its coarse good/bad-odd part is exactly zero. It acts trivially on the initial good state.

The ideal hidden fair choice of I versus S would leave that state good with probability one. S can be compiled into products of single-qubit Z rotations. However, the following allowed compilation exposes the failure of charging only the baseline's original odd component.

Apply R=exp(-i*pi*Z1/4), allow H to act for tau=pi/J, then apply S R^dagger. Every applied control segment is a product of single-qubit Z rotations. In the absence of H the total compiled pulse is exactly S. With H, the dwell propagator is U=exp(-i*pi*(I-XX)/2)=XX and the actual endpoint propagator is W=S R^dagger XX R. Direct exact multiplication shows <Phi+|W^dagger (I-P) W|Phi+>=1. In the unselected I branch the same baseline dwell leaves Phi+ unchanged. The privately averaged physical I/S implementation therefore has bad probability 1/2, whereas the ideal Schur refresh has zero.

The instantaneous control pieces here are idealized unitary segments; they expose a structural failure even before finite control inaccuracies are added. Finite sufficiently fast pieces approximate this example continuously and retain a positive failure bounded away from zero. This does not claim a mandatory 1/2 error for all implementations, optimal pulse design, or a duration-independent bound when J is actually bounded. For any small chosen dwell tau, choosing J=pi/tau gives this example; the old assumption permits arbitrarily large parity-preserving baseline. Thus duration and the original odd-action bound alone cannot qualify an arbitrary compiled path.

The issue is the parent coarse projector onto the complete syndrome. Each constituent Z rotation commutes with its own final S=ZZ, but need not commute with the other stabilizer XX. The intermediate state leaves P and the ostensibly free baseline can act there. Random physical Pauli endpoints and virtual Pauli-frame updates must both be distinguished from a trusted instantaneous full-joint Schur channel.

A repair must bound/charge baseline terms that fail to commute with the entire pulse path, prove a path that preserves the relevant joint sector, or qualify the actual complete implemented channel on the retained-system boundary. The existing theorem for an actual u(t)S Hamiltonian does not license arbitrary endpoint-equivalent product-pulse compilations. No external priority claim is made.

Run check_obstruction.py with SymPy. All equalities and the 1/2 probability are exact rational/algebraic checks.

## Fully finite, constant simultaneous pulse (stronger witness)

No impulsive idealization is needed. Set H_c=(Omega/2)(Z1+Z2), pulse for tau=pi/Omega, and keep H_0=J(I-XX)/2 active throughout, with J=sqrt(5) Omega. In the absence of H_0, exp(-i tau H_c)=-ZZ, the intended S up to a global phase. In the invariant basis (Phi+,Phi-), H_c=Omega X and H_0=diag(0,J). The actual two-level angular frequency is sqrt(Omega^2+J^2/4)=3 Omega/2. Starting in Phi+, the endpoint bad probability is therefore

    Omega^2/(Omega^2+J^2/4) * sin^2(tau sqrt(Omega^2+J^2/4)) = 4/9.

The I branch has H_c=0 for the same duration and remains good. A hidden fair I/S choice has endpoint bad probability 2/9. Every Hamiltonian is finite and constant within its branch. H_0 still commutes with both stabilizers and has zero coarse odd part. This sharpens the structural obstruction: a fully specified finite product-Pauli implementation can have nonzero failure while the old odd-only budget is identically zero. It does not disprove a theorem charging the entire pulse-induced drift or using the real actual channel.
