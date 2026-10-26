# Same covariances, arbitrarily little path irreversibility

27 October2026. A completed independent internal mathematical check of the web
peer's rare-cycle family. No worker implementation was imported. This is not an
experimental finding, novelty clearance or conclusion about a published proof's
full assumptions.

For0<e<1, take inactive state0 and a three-state active ring. Each active state
exits to0 at h=1-e;0 enters each active state at e/3. Ring forward and backward
rates are a=2+e/3 and b=1+e/3. This finite CTMC is irreducible. Its stationary
law is pi=(1-e,e/3,e/3,e/3). Each activation edge is detailed-balanced, whereas
the ring has path-KL rate

    sigma_e=e log[(2+e/3)/(1+e/3)] ->0.

Let X_j=1{state=j}-e/3 for the three active states. Exact generator action is
QX=X A^T, with

    A=[[-4,1,2],[2,-4,1],[1,2,-4]],
    Sigma_e=Cov(X)=(e/3)I-(e²/9)11^T.

Sigma_e commutes with A. Whitened observables Y=Sigma_e^(-1/2)X consequently
have Cov(Y(0),Y(t))=exp(A^T t) for EVERY lag, independently of e. A Gaussian OU
with drift A and diffusion D=-(A+A^T)/2 has exactly those covariances. Its
path-KL rate is tr(K^T D^(-1)K)=3/11, where K=(A-A^T)/2. Thus the covariance
Gaussian's positive rate cannot be a universal lower bound on non-Gaussian
path irreversibility. At e=.01 the actual rate is already<.007, while the
matched Gaussian rate is>.27.

The phenomenon also survives the phase-gauge witness at the population level:
the normalized three-channel spectral closure at omega1 has imaginary part
-1639726/190109375, independently checked exactly. A nonzero closure can reject
the reversible covariance null; it does not supply a universal positive
non-Gaussian rate. Since every whitened family member has the SAME complete
covariance function, the infimum valid covariance-only rate floor for that
function is zero.

The identical-covariance statement uses explicitly e-dependent whitening. Its
price is visible: E||Y||^4=9/e-6+e/(1-e), and the inactive waiting time is1/e.
No bounded-amplitude or free acquisition promise is granted. With the FIXED,
bounded raw indicator observables, the Gaussian covariance rate is still3/11:
invertible instantaneous real whitening preserves Gaussian path KL. The raw
covariances then vary with e. These are two different, precisely scoped claims;
the latter basic counterexample does not require unbounded detector outputs.

Consequences: quantitative inference needs a justified Gaussian/physical class
or information beyond these second moments, such as activity/higher moments.
Qualitative time-asymmetry detection and correctly scoped Gaussian inference
remain available. A claim about any particular paper requires reading its
complete theorem and supplementary assumptions; this check does not supply
that source review. `check.py` and `results.json` retain the executed exact
generator, covariance, Gaussian-rate, fourth-moment and closure identities.
