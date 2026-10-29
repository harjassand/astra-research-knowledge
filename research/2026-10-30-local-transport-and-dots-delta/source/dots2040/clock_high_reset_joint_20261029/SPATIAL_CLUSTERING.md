# Uniform boundary locality and equal-time spatial clustering

Notation and high-reset hypotheses are those of COEFFICIENT_CONTRACTION.md. Choose a>0 with lambda_a=kappa/2-C_D g exp(2a)>0.

For observable A initially supported on X, let T_t^R denote dynamics in the induced radius-R ball about X, embedded in the full graph (outside dynamics can consist of damping only). The full and truncated Hamiltonian generators agree on every basis string contained in the radius-(R-2) ball. Their difference has coefficient-column norm <=2 C_D g |support|. Both full and truncated semigroups contract full coefficient l1 norm. Duhamel and weighted integrated support mass therefore give, uniformly for ALL t>=0,

 ||T_t A-T_t^R A||_coeff
 <= B_R q(A),
 B_R=(2 C_D g/lambda_a) exp[-a(R-2)].

One may replace q(A) by the full coefficient norm. This bound is insensitive to total graph size. It is exponentially small in R and uniform in evolution time; it is not just a finite-time light cone.

Let A,B have disjoint supports X,Y with dist(X,Y)>2R+1. The induced R-neighborhoods are disconnected, so their truncated dynamics and unique stationary state factorize. Applying the preceding approximation to A, B, and AB gives for the unique full stationary state omega

 |omega(AB)-omega(A)omega(B)|
 <= B_R [q(AB)+q(A)||B||+q(B)||A||]
 <= 3 B_R ||A||_coeff ||B||_coeff.

The same inequality holds at every time t when the initial state is a product across the graph (in particular all-ready), because the disconnected truncated evolutions preserve that factorization. The finite-time statement compares each evolution at the SAME time; no stationarity assumption is needed.

This is genuine uniform spatial clustering of local observables. It does not establish a multiplicative probability bound for a many-site family of absence-of-emission events: those observables live on the output record rather than only on the final clock state, and additive cluster errors do not automatically exponentiate into a fault law.
