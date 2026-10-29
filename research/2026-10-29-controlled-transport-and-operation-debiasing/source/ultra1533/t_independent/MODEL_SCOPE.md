# Model acquisition and useful boundaries

The source is a SUPPLIED rational centered Gaussian ridge-mixture model. It is
not a learned universal interatomic potential. A graph geometry and stiffness
ratio do not by themselves qualify this constitutive law for a real material.

The class can genuinely be nonconvex; PROOF and CONTROLS give negative curvature
at q2,p99/100 and q4,p99/100. But every edge potential is centered and monotone in
the squared increment. Arbitrary multistable, shifted, quartic-hardening or
Lennard--Jones interactions are not represented by the theorem.

There is a sharp simple reason not to transfer the representation to positive
quartic hardening. Set t=s^2. Any positive mixture g(t)=integral exp(-k t/2)rho(dk)
obeys (log g)''>=0, since it is a tilted variance of k/2. In contrast,
g(t)=exp(-a t-b t^2), b>0, has (log g)''=-2b<0. Even arbitrarily weak positive
quartic hardening therefore fails this positive Gaussian-scale-mixture interface.
No signed mixture was silently substituted.

The current theorem assumes no linear source and zero tilt. Adding a force h
introduces exp[(1/2)h^T L_x^(-1)h] into the conductance law. Its conditional
derivatives include means in addition to squared transfer currents. The present
all-graph influence bound does not pay those terms. Linear response at zero source
can be estimated from the acquired equilibrium law, but finite forced-law output
is not thereby acquired.

Finally, conditional edge probabilities require a GLOBAL effective resistance.
The code pays dense exact rational algebra. The initial aspiration of an infinite
gapless medium's local observable at volume-independent expected work is still
NOT_ACHIEVED. An entrywise Dobrushin supremum cannot simply be swapped with a sum.
The finite global coupling avoids that swap; it does not provide a local infinite
background oracle or a measured continuum/material truncation error.
