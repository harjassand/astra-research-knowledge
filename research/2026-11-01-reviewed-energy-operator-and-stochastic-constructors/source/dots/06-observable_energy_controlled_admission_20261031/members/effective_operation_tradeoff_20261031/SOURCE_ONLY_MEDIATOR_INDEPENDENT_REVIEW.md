# Independent review: source-only mediator tradeoff

31 October 2026. Reviewer: challenge_graph_profile_compiler.

**PASS as leading effective-operator algebra, not as a finite-rate theorem.** I read the entire `SOURCE_ONLY_MEDIATOR_TRADEOFF_CANDIDATE.md`, SHA-256 `a5dfb31c88cb9127149370c07fa1bd8bcfd86f682b7a5e8301de87d81306d8d0`, and checked each identity, inequality, normalization and counter-scope. The conclusion is restricted to the stated source-only F,D and direct-return geometry. It does not prove a new gate/noise theorem for arbitrary lossy mediators.

## 1. Source-only effective stack

D>0 and F=F* imply N=F-iD is invertible: a null vector would have zero imaginary quadratic form -v*Dv. Let the physical source jump-row stack be R, so R*R=2D. Direct return to a SINGLE dark source state identifies each physical effective jump as a data operator. Then

    U=R(2D)^(-1/2),  U*U=I,
    E_phys=U E,  E=sqrt(2D) N^(-1) B.

U is a source/jump-color isometry tensored with the data identity. Hence summing jump sandwiches and anticommutators gives exactly the same dissipator for E_phys and E. It also preserves the total squared scalar component, the stack norm of the residual, and its Hilbert-Schmidt norm. This is an algebraic invariance; it does not assert a free implementation of U or acquisition of the matrices/norms.

The identity

    Re(N^(-1))=N^(-dagger) F N^(-1)

follows by inserting F=(N+N*)/2. With X=N^(-1)B, it proves

    S=-X*FX=-E*KE/2,  K=D^(-1/2)FD^(-1/2).

Thus -chi E*E/2<=S<=chi E*E/2 when ||K||<=chi. That compares coherent strength with jump ACTIVITY, not automatically with logical noise. An identity-valued jump can have nonzero activity and zero dissipator.

## 2. Scalar centering and the gauge sign

For any numerical color vector e, write E=e tensor I+A. Since K acts only on color/source,

    s=-e*Ke/2

is a real scalar on data. Expanding S and applying the stack operator norm gives

    ||S-sI||<=chi sqrt(a) delta+chi delta²/2,
    a=||e||², delta=||A||.

The cross terms in D[eI+A] are

    (1/2)[e*A-A*e,rho].

Therefore the source's sign is correct:

    D[E]=D[A]-i[H_e,rho],
    H_e=(i/2)(e*A-A*e),  ||H_e||<=sqrt(a)delta.

For the actual Hamiltonian G=S+H_e in this representation, minimizing over an irrelevant real scalar gives exactly inequality (1). Omitting the interference term would be false. This is ordinary Lindblad gauge algebra; it does not remove the physical scalar jump flux or the resources used to realize B.

## 3. Entanglement-infidelity rate

Choose e_j=Tr(E_j)/d. Then every A_j is traceless and

    nu=sum_j Tr(A_j* A_j)/d.

For a normalized maximally entangled data-reference input, the derivative at zero of entanglement fidelity under a GKSL generator is

    sum_j (|Tr E_j|²/d² - Tr(E_j*E_j)/d).

The Hamiltonian derivative vanishes. Thus nu is exactly the derivative of one minus this fidelity, with no missing factor of d or two. The stack operator norm satisfies delta²<=||A||_HS²=d nu. Monotonicity of the nonnegative right-hand side in delta proves inequality (2).

For clarity, if chi>0 the inequality implies

    nu >= [ (sqrt((chi+1)² a+2chi h)-(chi+1)sqrt(a))/chi ]²/d.

For chi=0,a>0 it gives nu>=h²/(a d); if both vanish it requires h=0. These are consequences of the displayed bound, not strengthened finite-time error claims. Parameters must actually be bounded independently to obtain a nonzero uniform rate lower bound.

The scalar term a is tied to the specified physical effective jump stack (invariant under its source-only isometry), not to an arbitrarily free gauge shift accompanied by an uncharged Hamiltonian. For the maximally mixed data input, the total physical effective jump intensity is a+nu. Counts are not thermodynamic power.

## 4. Essential hypotheses and counterexample

If the excited Hamiltonian acts on data, e*Ke need not be scalar. The proposed example D=d0 I, F=Z_data, B=(F-iD)v, with scalar v, gives X=vI, E=sqrt(2d0)vI and S=-|v|²Z. Its effective dissipator is zero while its mediated Hamiltonian is nontrivial. This precisely defeats the scalar-centering step when F is not source-only. It does not contradict (1) or (2), and it does not furnish a finite-rate noiseless device: the desired data interaction and engineering resources already occur in F and B.

Direct return to one dark source state is also material to the stated data-only jump-stack interpretation. Multiple retained ground/source states or source-dependent jump maps require their own receiving argument. Externally supplied ground Hamiltonians are excluded from h and separately charged; adding an ideal direct drive cannot be advertised as beating this mediator tradeoff.

Finally, a derivative of entanglement infidelity is not a finite implemented-gate error bound. The note supplies no uniform elimination remainder, no adaptive error-correction lower bound, and no impossibility result for encoding, resets, varying detuning/drive resources or broader excited-state controls.

## 5. Ordinary prior and execution scope

I directly read Reiter and Sørensen's primary effective-operator equations (3)–(5) at https://arxiv.org/html/1112.2806. They are the appropriate ordinary baseline for the leading S and jump stack used here. Their application does not automatically supply finite-rate accuracy for this candidate. The present inequalities are elementary consequences of those effective equations and Lindblad gauge centering, not a claim of a new elimination method.

I also read `check_mediator_algebra.py`. Its random exact identities check the resolvent formula, gauge identity on a full matrix-unit basis, centered Hilbert-Schmidt expression and data-dependent counterexample. Such checks do not replace the operator norm proof above or earn finite-rate/hardware conclusions. I independently reran a copied script in `producer-workspace/mediator_review`, preserving author source/results: all 50 exact identity checks passed. The copied-run result is preserved as `mediator_independent_rerun.json`. This run is an algebraic regression test, not an experimental or finite-rate numerical certificate.
