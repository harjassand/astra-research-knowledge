# Independent sector-to-spectrum reconstruction

Parent derivation before reading the peer's final proof; no Gaussian law is
assumed. The separate cycle-affinity theorem and physical acquisition interface
must be supplied at their own scopes. This lemma does not estimate a rate.

Let the finite stationary centered state-observable generator, in a real
orthonormal stationary-L2 basis, be L=-S+A with S positive definite and A real
skew. Put kappa=||S^(-1/2) A S^(-1/2)||. A finite irreducible Markov chain
restricted to centered functions supplies such a representation. Its full
state-observable spectrum has

    C=2 G^-1 S G^(-*) ,  G=S-A-i omega I,
    C^-1=(1/2)[S-A S^-1 A+omega^2 S^-1
                    -i omega(A S^-1+S^-1 A)].

This follows from the two resolvent covariance integrals, or from
G^-1+G^(-*)=G^-1(G+G*)G^(-*). It is a second-moment identity for that generator,
not an assertion that its paths are Gaussian.

Congruence of C^-1 by S^-1/2 gives half the Hermitian matrix D-E where

    T=i S^-1/2 A S^-1/2, W=omega S^-1,
    D=I+T^2+W^2, E=TW+WT.

E is already Hermitian and purely imaginary; an additional factor i would be
incorrect. The sign of E reverses with the Fourier convention and is immaterial
to the absolute bound below.

For every complex vector v,

    |v* E v| <=2||Tv|| ||Wv||,
    v* D v=||v||^2+||Tv||^2+||Wv||^2.

Writing a=||Tv||/||v||<=kappa and b=||Wv||/||v||, the ratio is at most
2ab/(1+a^2+b^2)<=a/sqrt(1+a^2)<=kappa/sqrt(1+kappa^2). The middle maximum
over b is attained at b=sqrt(1+a^2). Hence the canonical imaginary radius of
C^-1 is bounded by r0=kappa/sqrt(1+kappa^2).

That radius is unchanged by matrix inversion. To see this, normalize a positive
Hermitian matrix as R^1/2(I+iB)R^1/2 with B real skew. Its inverse has central
real part(I+B^2)^-1 and imaginary part -B(I+B^2)^-1. These commute, so real-part
normalization leaves canonical skew matrix -B up to orthogonal equivalence.
Consequently C itself obeys the real-imaginary cone

    -r0 Re C <= i Im C <= r0 Re C.

The cone is linear and convex: it survives real observable projections,
addition of real PSD noise and positive frequency averages. A common real
finite gate produces exactly such an average of physical spectra. Unknown
channel filters factor outside this average only when the gate actually
PRECEDES them and the complete response or a justified error envelope is used.

For three positive-definite observed channels, real congruence normalizes C to
I+iB, whose real skew B has singular values(r,r,0). Then

    tr[(C^T)^-1 C]-3 =4r^2/(1-r^2)<=4kappa^2.

If unknown nonzero diagonal complex gains precede diagonal independent read
noise, removing their phases yields the physical matrix up to real diagonal
congruence plus real PSD noise. Thus the minimum of this trace functional over
diagonal phase gauges is also <=4kappa^2. Arbitrary cross-channel noise added
after distinct filters is a different contract and does not inherit this fact.
Singular covariances require an explicit support/real-regularization treatment;
an inverse is not silently granted.

The Ohga-Ito-Kolchinsky cycle theorem, if applied at its finite-state,
even-observable, dynamically reversible scope, bounds kappa<=Fmax/(2pi).
That separate established input then yields Fmax>=pi sqrt(F_phase_min).
Historical novelty of the composition is UNKNOWN. Readout gate, tails,
stationary independent repeats, noise and calibration remain physical inputs;
this proof does not acquire them. The root's independent primary-source search
also identified finite-time affinity bounds in PRE108 L062101 (2023), which
must receive the same acquired inputs in any ordinary-method comparison.

Root subsequently whole-read the peer's8009-byte SPECTRAL_AFFINITY_THEOREM.md,
SHA256daf190578184510915a88e2e81df6487474d06a45543e819d1dcb48005c0f679,
and completed an independent mathematical review. No error found in its
bilinear-sector input, precision/block-Cauchy-Schwarz proof, inversion and
projection/window/noise closure, phase minimum or affinity consequence at the
stated finite-state/even/bidirectional/stationary scope. This is substantive
internal acceptance of that theorem version; it does not review a subsequently
written photon confidence implementation or acquire a physical instrument.

An independent exact SymPy check at S=diag(1,4,9),
A=[[0,1,-1/2],[-1,0,2],[1/2,-2,0]],omega=3/2 verified the precision identity,
inversion radius equality,three-channel trace identity and cone. It gives
r^2=47729/253369,kappa^2=7/18,T(C)=47729/51410. This corroborates the algebra;
the proof above, not that finite matrix, establishes the general lemma.
