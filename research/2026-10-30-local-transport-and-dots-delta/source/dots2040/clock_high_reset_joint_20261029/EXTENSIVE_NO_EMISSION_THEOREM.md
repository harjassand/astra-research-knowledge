# Extensive joint no-emission theorem via finite-support Lyapunov polynomials

**Status: constructive proof.** This establishes an extensive joint absence bound, not merely marginal mixing. It works for arbitrary positive g,kappa and arbitrary initial full-qubit states. Constants are catastrophically weak and do not establish the sharp weak-drive scaling c(D)g^2/kappa.

Model: full qubits, H=sum_z g X_z product_{y~z}(I-n_y), jumps sqrt(kappa)sigma^-_z, graph degree <=D. Let J_x^*(A)=kappa sigma_x^+ A sigma_x^-. For a marked set S define K_S=L^*-sum_{x in S}J_x^*. Then exp(tK_S)I is the effect of no emissions anywhere in S during [0,t]. These semigroups are completely positive and subunital.

## 1. Input: uniform local progress

The local-observability theorem gives, for every delta>0, a constant c=c(D,g,kappa,delta)>0 such that

 exp(delta K_{x})I <= (1-c)I

on every graph and for every x. The earlier proof was phrased on the independent-set subspace. IMPORTANT: to apply the product construction on the full tensor product, use its full-qubit extension: the same curvature estimate holds with a larger harmless constant, because Q L*²(n_x)Q=2g²G_xQ and the self-curvature on full qubits is 2g²G_x(1-2n_x). Its difference from 2g²G_x is bounded by 4g² n_x. Neighbor-count dissipative identities and all off-diagonal bounds are unchanged. Thus the same stated curvature constant and cutoff bound work on the full-qubit model too. No illegal-configuration loophole is present.

## 2. Finite local Taylor estimates

Put

 C0=4(g+kappa)(D+2)^2,
 delta=1/(4C0), q=C0 delta=1/4,
 a=(1-exp(-kappa delta))/kappa.

For K=K_{x}, locality and nested-generator counting give

 ||K^k I|| <= C0^k k!.

Proof: artificially include x in the support from the start. A nonzero Hamiltonian/dissipator term meets current support, and K has one additional local killing term at x. At most (D+3)|support| terms matter, each norm <=2(g+kappa), and support after j terms has size <=1+jD. The displayed C0 dominates the resulting product bound. Support radius grows at most two per term. The estimate is uniform in graph size.

Define the Hermitian finite-support polynomial

 F_x^(m)=sum_{k=0}^m delta^(k+1)/(k+1)! K_x^k(I).

It is supported in B_{2m}(x). Let F_x=integral_0^delta exp(sK_x)I ds. Bounded target intensity gives exp(sK_x)I>=exp(-kappa s)I, so

 aI <= F_x <= delta I.

The series bounds give

 ||F_x^(m)-F_x|| <= delta q^(m+1)/(1-q),
 ||K_x F_x^(m) - [exp(delta K_x)I-I]|| <= q^(m+2)/(1-q).

The second estimate follows EXACTLY by applying K to the polynomial and shifting its index; no extensive global generator norm is used.

Choose an integer m such that the first error <=a/2 and second error <=c/2. This choice depends only on D,g,kappa. Then

 (a/2)I <= F_x^(m) <= (3delta/2)I,
 K_x F_x^(m) <= -(c/2)I <= -r F_x^(m),
 r=c/(3delta)>0.

## 3. Buffered packing and product inequality

Given S, greedily choose S' subset S with pairwise center distances >4m+2. A degree bound gives

 |S'| >= |S|/B,
 B=(D+1)^(4m+3)

(a deliberately loose ball-volume bound). Write s=|S'| and F=product_{x in S'} F_x^(m). These positive factors have disjoint supports. The support of L^*(F_x^(m)) lies in B_{2m+2}(x), disjoint from every other factor's support by the chosen buffer.

The Hamiltonian obeys Leibniz, and each single-site dissipator acts on at most one factor. Therefore

 [L^*-sum_{x in S'}J_x^*]F
 =sum_{x in S'} [K_x F_x^(m)] product_{z!=x}F_z^(m)
 <= -rs F.

The ordering is valid because each local negative summand commutes with the remaining positive factors on disjoint supports. Additional killings x in S\S' subtract J_x^*(F)>=0, hence

 K_S F <= -rs F.

Positivity of the killed semigroup gives exp(tK_S)F<=exp(-rst)F. Using the bounds on F yields, for EVERY initial density matrix rho,

 P_rho[N_x(t)=0 for all x in S]
 <= (3delta/a)^s exp(-rst)
 <= C^|S| exp(-gamma |S| t),

 C=3delta/a,
 gamma=r/B=c/[3delta (D+1)^(4m+3)]>0.

The probability is also <=1, so take the minimum with one. Constants are independent of graph size, S, and rho.

## 4. Actual joint spacetime consequence

For nonoverlapping chronological time slabs j, with marked site sets S_j and durations T_j, the arbitrary-initial-state bound composes under conditioning on all preceding no-event records:

 P[every (x,j) with x in S_j has no event during slab j]
 <= product_j C^|S_j| exp[-gamma |S_j|T_j].

For a fixed slab length T this is a genuine local-stochastic upper bound p^(sum_j |S_j|), where p=C exp(-gamma T), whenever p<1. No independence assumption or multiplication of marginal bounds is used: each whole-slab marked-set event has its own extensive estimate.

## 5. What remains

This is a mathematically useful existence-level joint clock-stall law. Its rate gamma can be far smaller than g^2/kappa; obtaining gamma>=c(D)g^2/kappa with moderate C(D) remains open here. Also this theorem concerns the ideal clock only, not fault propagation under physical perturbations or a complete error-correction threshold.
