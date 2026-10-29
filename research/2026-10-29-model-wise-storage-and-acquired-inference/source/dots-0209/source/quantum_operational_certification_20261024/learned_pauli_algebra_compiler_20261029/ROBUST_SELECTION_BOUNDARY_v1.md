# Robust selection boundary and a constructive large-gap escape
Date2026-10-29. New self-contained argument; independent review pending. All hardness statements are scoped reductions, not unproved impossibility claims.

## LPN reduction for the present mixed-gauge Clifford interface
Let a classical learning-parity-with-noise sample be x uniform in F_2^d, y=s·x+e with e Bernoulli(eta),0<eta<1/2, and unknown s. Let n=d+1 and define an n-qubit Pauli channel by sampling z=(x,y) and applying Z_z. The label distribution on F_2^n is

  p=(1-2eta) Uniform(S)+2eta Uniform(F_2^n),
  S={(x,y):s·x+y=0}.

A Clifford compiler knowing S keeps one qubit with Fe=1-eta by the mixed-gauge identity. Now suppose a polynomial-time learner from these samples outputs a mixed-gauge Clifford encoder/decoder keeping k>=1 qubits with Fe>1/2. Its corrected gauge-only symplectic space T has dimension2(n-k) and is nondegenerate. Intersection A=T∩Z_space is isotropic, hence dimA<=n-k<=n-1. If A is not S, then Uniform(S)(A)<=1/2 and Uniform(F_2^n)(A)<=1/2, so p(A)<=1/2. Therefore A=S. Compute the emitted Clifford's symplectic matrix, intersect by binary elimination, and take the one-dimensional orthogonal complement of S: its generator is(s,1), recovering the LPN secret.

Thus robust best-subsystem learning in this specified interface can solve LPN. No assertion is made that LPN is proven hard, that an unrestricted recovery learner outputs the secret, or that quantum example or coherent environment access is equivalent to Bell samples. A channel call can be simulated with a fresh classical LPN sample and a Pauli operation, but a quantum-computational learner would give a quantum algorithm for classical-sample LPN, not necessarily a classical one. A fixed known nonzero Pauli shift does not invalidate the reduction when the compiler's output includes that shift: the same mass argument applies to affine intersections and high-mass intersections recover the hidden homogeneous hyperplane.

Primary source: Chen, De, Vijayaraghavan, Learning a mixture of two subspaces over finite fields, ALT2021, https://proceedings.mlr.press/v132/chen21a.html and its linked24-page PDF. Proposition20 explicitly embeds LPN in nested subspace mixtures. Their Theorem2 also gives polynomial recovery when the dimension ratio is bounded below1, using a polynomial-feature lift. The transfer above specializes the basic obstruction to a *physical emitted recovery frame*. It is not a new LPN hardness principle.

## Simple large-gap dependency construction
The obstruction is not universal even for contaminated subspaces. Let ambient binary dimension D (D=2n for full Pauli labels). Consider iid labels from

  w Uniform(S)+(1-w) Uniform(F_2^D), dim S=m.

Take a batch of B samples, arranged as columns of X in F_2^(D×B). Compute a basis of ker X. Mark column j iff some kernel basis vector has nonzero j coordinate; equivalently j participates in some linear dependence among the sampled columns. Output the span of marked columns.

Conditional on I latent inlier draws and O=B-I latent ambient draws, assume

  I>=m+u+1, O<=D-m-u.

Ambient draws projected to F_2^D/S are iid uniform. With probability at least1-2^(-u), their O projected vectors are independent: sequential rank failure is bounded by sum_{j=0}^{O-1}2^(j-(D-m))<2^(O-(D-m))<=2^(-u). Therefore no dependence of all columns can involve an ambient-draw column. Conversely, deleting any particular inlier leaves I-1>=m+u uniform vectors in S, which fail to span S with probability at most2^(m-(I-1))<=2^(-u), by union over nonzero dual vectors. A union bound over I inliers implies every inlier participates in a dependence, and their span is S. Hence the marked-column output equals S with conditional failure probability at most(I+1)2^(-u).

The latent labels/counts are used only in the proof, never given to the algorithm. Binomial concentration supplies the probability that the displayed count event holds. In a scaling family with fixed w and m/D<=w-gamma for constant gamma>0, choose B=(1-c)D with fixed c sufficiently small relative gamma. Then expected I-m and (D-m)-expected O are both linear in D, and choosing u=Theta(D) gives exponentially small failure probability. The algorithm is ordinary binary elimination, polynomial time, with B=Theta(D) channel samples. For small D or stronger finite confidence, repeat candidate generation and use independent membership-mass validation; exact support recovery still depends on the distributional promise.

For the resulting Clifford with k=n-a-b, full ambient contamination contributes corrected mass 2^(-2k), giving exactly

  Fe = w+(1-w)4^(-k).

This remains valid for coherent CPTP channels whose diagonal process distribution has the specified mixture shape. No full physical Pauli-diagonal premise is needed for fidelity. The optional paid logical twirl gives half-diamond error (1-w)(1-4^(-k)). Conventional finite-field robust subspace learning can do the same; this construction is a concrete acquisition-to-gate bridge, not a claimed comparative breakthrough.

### Conditions and limitations
The useful polynomial regime is m<wD, with fixed slack for the simple dependency method. For a full symplectic gauge algebra m=2(n-k), D=2n, it suffices that protected fraction k/n exceeds contamination fraction1-w by fixed slack. For commuting error labels with ambient outliers confined to Z-space, the effective ambient dimension is n, not2n; using2n would silently invalidate the count argument. In particular the codimension-one LPN family fails the large-gap condition. Arbitrary adversarial outlier distributions can create dependencies themselves, so the uniform ambient-outlier assumption is load-bearing. The ALT2021 lifted method has a larger parameter regime but is not implemented here.
