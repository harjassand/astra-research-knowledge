# Structure and displacement of every optimal positive network

This is a corollary of FAMILY_THEOREM_v3.md, SHA256 e039c3a8a70181d9b123ae8e4af7b3a7394386512afb12ca89e0bdb55d19b052. Its governing proof and every earlier file remain unchanged. Read this alongside CONTINUATION.md: the necessary displacement-range cost stated there for the canonical pendant extends to EVERY exact optimal positive scalar mass/spring graph, as proved below. This is an equilibrium displacement result within the same ideal harmonic model, not a specimen or finite-contact transport claim.

## 1. Statement and resources

Fix the theorem's K>0, M>m0>0 and finite positive temperature T. Write r=r_* for its unique optimal positive internal frequency and

ms=M-m0,
mu_red=m0 ms/M,
k_*=mu_red r^2.

An arbitrary exact optimal cell can have any finite number of internal masses m_j>0 with sum ms. Let x_b denote its backbone displacement and x_j its internal displacements. Its backbone mass is necessarily m0 by the theorem's equality condition. Define the internal centre-of-mass displacement relative to the backbone,

Y=sum_j(m_j x_j)/ms-x_b.

Then:

1. The static compliance conjugate to Y is exactly1/k_* at EVERY Bloch wave number, using the translation-free pseudoinverse at q=0. The same local compliance is1/k_* on any finite periodic ring.
2. In the harmonic Gibbs state at temperature T, including the quantum Gibbs state, Var(Y)>=k_B T/k_*. This bound holds for every exact optimal topology, not just the one-pendant representative.
3. Within the positive pairwise scalar spring-graph contract, exact optimality is equivalent to each internal node having a direct total spring coupling to the backbone

   kappa_bj=r^2 m0 m_j/M.

   Arbitrary additional positive springs among internal nodes are allowed; they affect only dark modes. In particular sum_j kappa_bj=k_*.
4. In that Gibbs state EVERY internal relative coordinate obeys

   Var(x_j-x_b)>=Var(Y)>=k_B T/k_*.

Thus adding internal topology or dark modes cannot evade the common equilibrium displacement-range cost of exact attainment.

## 2. The optimal driving response fixes the bright subspace

Let Mass=diag(m0,m_1,...,m_n), H0 be the internal spring Laplacian and

D0=Mass^(-1/2) H0 Mass^(-1/2),
z=(sqrt(m0),sqrt(m_1),...,sqrt(m_n))^T/sqrt(M),
v=Mass^(-1/2)e_b.

Connectedness gives D0 z=0 and a one-dimensional nullspace. In mass-normalized coordinates eta=Mass^(1/2)x, the Bloch matrix is

D(q)=D0+s(q)vv^T, s(q)=4K sin^2(q/2).

For an exact optimum, the theorem's equality condition fixes the complete active passbands to[0,p] union[r,s_end], with

p^2+s_end^2-r^2=4K/m0,
p^2 s_end^2/r^2=4K/M.

After cancelling every zero-width dark factor, the determinant lemma therefore gives

1+4K q_*(t)=(t+p^2)(t+s_end^2)/[t(t+r^2)],
q_*(t)=v^T(D0+tI)^(-1)v
      =1/(Mt)+(1/m0-1/M)/(t+r^2).

This calculation uses spectral equality, not an assumed star realization. By the spectral theorem,

u=v-z/sqrt(M),
D0 u=r^2 u,
||u||^2=1/m0-1/M=ms/(m0 M).

Indeed the scalar resolvent is a positive sum of spectral residues; its only positive visible pole is r^2, so v has no projection onto any other positive eigenspace. Degenerate modes at r^2 that are orthogonal to v are harmless dark modes too.

The mass-normalized force vector for Y is

w=Mass^(-1/2)(-1,m_1/ms,...,m_n/ms)^T
 =-(M/ms)u.

Consequently

w^T z=0,
D0 w=r^2 w,
||w||^2=M/(m0 ms)=1/mu_red.

Let e=w/||w||. The two-dimensional bright subspace B=span(z,e) is invariant under D0 and under vv^T. Its orthogonal complement is dark and invariant under every D(q).

## 3. Exact compliance, with no omitted acoustic contribution

Set c=ms/(m0 M)>0. In the orthonormal basis(z,e),

D0|B=diag(0,r^2),
v=z/sqrt(M)-sqrt(c)e.

For s(q)>0 the bright block is

             [ s(q)/M             -s(q)sqrt(c/M) ]
D(q)|B =    [ -s(q)sqrt(c/M)       r^2+s(q)c     ].

Its determinant is s(q)r^2/M. Hence its inverse has(e,e) entry exactly1/r^2, even though the acoustic and optical coordinates mix. Therefore

w^T D(q)^(-1)w=||w||^2/r^2=1/k_*.

At q=0 use D0^+; since w is orthogonal to translation, the same identity holds. This is the response to the force pair conjugate to Y: unit total force distributed among internal nodes in proportion to their masses, and opposite unit force on the backbone. It has zero total force.

On an N-cell periodic ring, a force conjugate to the local observable Y_l has Fourier amplitude w/sqrt(N) in each Bloch sector. Its static compliance is the average of the N sector compliances and is exactly1/k_* for every N. Only the global translation is removed. Taking N to infinity does not use the divergent absolute displacement of a free one-dimensional acoustic field.

More strongly, the entire Gibbs covariance seen by Y is identical to that of the canonical two-mass cell: its bright matrix, observable vector and resources are identical at every q. Dark coordinates do not couple to Y.

## 4. Quantum and classical equilibrium variance

For one positive mass-normalized normal mode of frequency omega, the quantum Gibbs position variance is

(hbar/(2omega)) coth[hbar omega/(2k_B T)].

The elementary inequality x coth x>=1 gives the modewise operator inequality

Cov(eta)>=k_B T D^+

on the translation-free subspace. Here D is the complete ring matrix; its zero global translation is excluded. Applying it to the local relative observable and using Section3 gives

Var(Y_l)>=k_B T/k_*.

In the classical Gibbs state equality holds for this static-covariance comparison. At finite quantum temperature the displayed expression supplies a lower bound; zero-point motion has not been discarded from the actual covariance.

This is a Gibbs/equilibrium statement. It is not asserted for arbitrary driven, squeezed or nonequilibrium states, or inferred from the theorem's ideal-contact transport objective. A steady heat-current state need not be the Gibbs state used here.

## 5. Complete positive-graph classification

Put a=Mass^(-1/2)w. Its physical displacement pattern has

a_b=-1/m0,
a_j=1/ms for every internal j.

The eigenvector identity D0w=r^2w is equivalent to

H0 a=r^2 Mass a.

All internal nodes have identical displacement in this pattern, so every internal-to-internal spring has zero extension. At internal node j the force equation is therefore

kappa_bj(1/ms+1/m0)=r^2 m_j/ms,

where kappa_bj is the sum of any parallel direct backbone-to-j springs. It follows that

kappa_bj=r^2 m0 m_j/M>0.

Thus EVERY internal mass must directly couple to the backbone in an exact optimal positive graph. Summing gives total backbone incidence k_*.

Conversely, take arbitrary positive masses m_j summing to ms and these direct couplings, and add any positive springs among the internal nodes. The same vector a obeys H0a=r^2Mass a; all added edges annihilate it and the rigid translation. Hence the same two-dimensional bright subspace and q_*(t) follow, while the complementary dark subspace may change. The network is connected because each direct kappa_bj is positive. Its full transport spectrum is exactly the optimal two-band union plus zero-width dark intervals. This proves the stated if-and-only-if classification within the theorem's pairwise positive scalar graph model.

This is stronger than a mere incident-stiffness invariant. Splitting the side mass into many equal-natural-frequency branches is allowed; replacing all direct connections by a serial internal path cannot retain exact optimum. The result does not cover levers, additional holonomic constraints, generalized coordinate couplings or extra intercell links outside the admitted graph.

## 6. Every individual internal relative displacement carries the common mode

For y_j=x_j-x_b define

w_j=Mass^(-1/2)(e_j-e_b),
d_j=w_j-w.

Direct calculation gives

w_j^Tz=0,
w_j^Tw=1/m0+1/ms=||w||^2.

Thus d_j is in the invariant dark subspace B^perp. In a harmonic Gibbs state the covariance is a matrix function of D(q), so the bright and dark subspaces have zero cross covariance. Consequently on a finite ring and in its limit,

Var(y_j)=Var(Y)+Var(d_j^Teta)>=Var(Y).

Additional internal edges can alter the nonnegative second term, but cannot cancel the common bright displacement. This argument uses Gibbs block decorrelation; it does not assume decorrelation for arbitrary prepared states.

## 7. Consequence for the retuned low-temperature family

TEMPERATURE_RESOURCE_LIMITS.md establishes at fixed R=M/m0>1 that, as T tends to zero while the optimum is retuned,

r_*=2(k_B T/hbar)x_R[1+o(1)],
sinh(x_R)=R^(3/4)sinh(x_R/sqrt(R)).

The exact compliance result therefore extends its earlier pendant bound to ALL exact optimal positive graphs:

Var(Y), Var(x_j-x_b)
 >= hbar^2/[4mu_red k_B T x_R^2] [1+o(1)].

A fixed allowed rms displacement d_max for every internal mass relative to its backbone necessarily requires

mu_red T d_max^2>=hbar^2/[4k_B x_R^2] [1+o(1)].

The same necessary condition follows from an rms cap on Y alone. Thus internal topology and dark-mode additions cannot remove this equilibrium displacement-range cost at fixed total mass. This is not a universal local-strain or fabrication bound: spring geometry, material modulus, confinement, anharmonicity and the preparation/state contract need their own counted operations. It establishes neither a measured insulator nor historical novelty.
