# Positive pair endpoints do not supply positive returns or a high-occupation pair sector

29 October 2026. New analytic construction; independent review pending. This is a scoped failure of direct paired-boundary renewal and of bare/near-identity paired truncation. It is NOT a sign-problem hardness theorem or a lower bound on arbitrary canonical, tensor, squeezed-state or correlated-field algorithms.

## 1. Native class and the exact positive endpoint operation

For M sites, fix K>=1 particles of EACH flavor and

`H=b†Tb+c†conjugate(T)c+U sum_i(nb_i-nc_i)^2`, `T>=0`, `U>0`.

All one-body diagonal terms are retained. The q_i^2 operator includes its normal-order linear number term. There is no occupation cutoff or pair-creation term. All fixed-number spaces are finite, with one-flavor dimension `D_(M,K)=binom(K+M-1,M-1)`.

Identify `|n>_b|m>_c` with the matrix unit `|n><m|` on the one-flavor K-particle space. If T_K=dGamma(T), H becomes the positive self-adjoint Hilbert--Schmidt superoperator

`Hcal(A)=T_K A+A T_K+U sum_i[n_i,[n_i,A]]`.             (1)

The map Phi_t=exp(-t Hcal) is completely positive and trace nonincreasing: dephasing is trace preserving, and the other factor is A->exp(-sT_K)A exp(-sT_K) with T_K>=0. Finite-dimensional product convergence suffices. The finite-slice HS formula has Kraus operators Gamma_K(B), and therefore

`F_nm(t)=<n,n|exp(-tH)|m,m>`

`= <n|Phi_t(|m><m|)|n> >=0`.                          (2)

At finite slices it is exactly the Gaussian average of `|<n|Gamma_K(B)|m>|^2`; the finite-K limit preserves positivity. Each column of F has sum at most one. This is a genuine positive endpoint operation, not a claim that its individual permanent amplitudes are supplied efficiently.

Let P be the projector onto the BARE paired vectors |n,n>, and Q=I-P. The full canonical trace is `Z=Tr exp(-beta H)`, whereas the endpoint trace is only

`Z_P=Tr[P exp(-beta H)]=sum_n F_nn(beta)`.

They are different. In the matrix picture Z is the superoperator trace over ALL matrix units, not the trace restricted to diagonal matrix units or a sum of population transition probabilities. A preparation/dressing or discarded-weight theorem is required before using Z_P as Z.

## 2. The unique exact first-return interface

Write the Hamiltonian blocks as

`A=PHP`, `B=QHP`, `D=QHQ`.

For initial data supported on P, block elimination gives the exact Volterra equation

`F'(t)=-A F(t)+integral_0^t R(t-s)F(s)ds`,

`R(t)=B† exp(-tD)B`.                                 (3)

R(t) is a positive SEMIDEFINITE matrix. That does not imply entrywise nonnegative return weights. For z>0, block Schur complementation gives

`Fhat(z)=P(z+H)^(-1)P`,

`S(z)=Fhat(z)^(-1)=zI+A-Rhat(z)`.                     (4)

Thus the first-return kernel is fixed by the endpoint family and its actual initial derivative. It cannot be chosen independently to remove negative entries.

Here a POSITIVE BOUNDARY DILATION means a TIME-HOMOGENEOUS classical continuous-time Metzler generator G on the paired states plus any finite set of auxiliary states, with the paired states represented by literal individual boundary coordinates, initial injection into those coordinates and final restriction to the SAME coordinates. Killing is allowed. If its endpoint family equals F(t) for every t, then G_PP=F'(0)=-A. Eliminating its auxiliary coordinates gives

`R_classical(t)=G_PQ exp(tG_QQ)G_QP`,

which is entrywise nonnegative. Equations (3)--(4) imply equality with the exact R. Locally integrable Volterra kernels are already unique on every finite interval: differentiate the homogeneous convolution with F, use F(0)=I, and apply Gronwall. Thus an irrelevant growing hidden component cannot evade the argument by making its global Laplace transform undefined. Consequently one negative off-diagonal Rhat(z), or a negative R(t), forbids every such positive boundary dilation, regardless of the number of auxiliary states. The same argument excludes stationary renewal constructions whose whole first-return kernels are nonnegative locally integrable measures, including delay distributions with a nonnegative Laplace transform.

This does NOT exclude arbitrary classical HIDDEN encoders with several latent states per observed label, nontrivial coarse graining, externally time-inhomogeneous constructions, history-dependent global proposals or nonrenewal representations. Ordinary classical coarse graining can itself have signed memory kernels. It also does not exclude a general nonlocal change of the occupation basis, whose acquisition/output costs would be separate.

## 3. Exact native trimer: even the energy-dependent pair operator is frustrated

Use the SAME critical trimer as the frozen critical-occupation theorem:

```
T3 = [ 3  1 -4
       1  3 -4
      -4 -4  8 ].
```

Its eigenvalues are0,2,12, its zero mode is uniform, and its hopping triangle product is16>0. Work for the moment at K=1. The paired block is `A=diag(6,6,16)`. Only the three symmetric unpaired vectors `( |i,j>+|j,i> )/sqrt(2)` couple to P; the antisymmetric sector is not being discarded from a coupled calculation. In the order12,13,23 put

```
B0 = [ 1  1  0
      -4  0 -4
       0 -4 -4 ],

zI+D = [ w+6  -4    -4
          -4  w+11   1
          -4    1   w+11 ],   w=z+2U.
```

The actual coupling is sqrt(2)B0, so

`Rhat(z)=2 B0^T(zI+D)^(-1)B0`.

An exact3x3 inverse gives

`Rhat_12(z)=2(w^2-26w-40)/[(w+10)(w^2+18w+40)]`.       (5)

At U=1,z=1 this is `-218/1339`. In fact

```
S(1) = [6295/1339   218/1339   -224/103
         218/1339  6295/1339   -224/103
        -224/103   -224/103    1175/103].
```

The positive S12 and negative S13,S23 have positive triangle product. A diagonal phase change cannot make all three off-diagonal entries nonpositive real: that product is phase invariant, whereas three negative real entries have negative product. Endpoint positivity has therefore NOT supplied an exact stoquastic energy-dependent pair operator, even up to diagonal rephasing.

Since (5) is a negative integral of the continuous function exp(-zt)R12(t), R12(t) is negative on some nonempty interval. This is not inferred from a numerical mesh. At K=1 every unpaired vector costs the SAME2U. For fixed T,

`D_U=D_0+2U I`, `R_U(t)=exp(-2Ut)R_0(t)`.             (6)

The negative time-return interval persists for EVERY finite U>0. Its magnitude can be very small at large U; no lower bound against a qualified large-U APPROXIMATION is implied. The U=1 rational integral is enough to identify the sign once, and (6) transports it exactly.

## 4. A connected, bounded-range, positive-density-frustration family at ALL M

The obstruction is not left as a fixed-mode numerical fixture. Let M>=3, epsilon=1/100000, and partition the chain into consecutive complete trimer blocks, with a final remainder of at most two sites. Define T0 as the direct sum of T3 on the complete blocks and zero on the remainder. Add

`epsilon sum_(missing adjacent bonds i,i+1) (e_i-e_(i+1))(e_i-e_(i+1))^T`,

where “missing” means the adjacent bonds not already INTERNAL to a complete trimer. Call the resulting matrix T_M. Its input has O(M) rational nonzeros; the interaction range is at most two, graph degree is at most three, and the coefficients do not depend on M. There is a frustrated triangle in every complete block. This is not a density-zero impurity family.

The known source eigenvalues give T3>=2Q3 and `L_path,3<=3Q3`, hence T3>=(2/3)L_path,3. Since epsilon<2/3,

`T_M>=epsilon L_path,M`,

`lambda2(T_M)>=4epsilon/M^2`, `||T_M||<=12+4epsilon`.   (7)

Thus its only zero mode is the uniform mode, and both spectral bounds are ACQUIRED from the sparse input. No unspecified gap or numerical eigenvalue oracle is used.

At K=1,U=1, write H_M for the full two-flavor Hamiltonian. The bridge perturbation obeys `||H_M-H_0||<=8epsilon`, while `||H_0||<=26`, `||H_M||<=26+8epsilon`. With z=1, the resolvents are contractions. After compression to P,

`||Fhat_M(1)-Fhat_0(1)||<=8epsilon`.

The compressed resolvents are bounded below by `I/27` and `I/(27+8epsilon)` respectively. The inverse identity then gives the DIMENSION-INDEPENDENT bound

`||S_M(1)-S_0(1)||<=8epsilon*27*(27+8epsilon)`

`=9112527/156250000`.                                (8)

At zero bridges, a pair starting in the first trimer remains there; S0 restricted to that paired block is exactly Section3. Exact Fraction subtraction gives

`(S_M)12 >=21860826347/209218750000 >1/10`,

`(S_M)13,(S_M)23 <=-34061409719/16093750000 <-2`.      (9)

Consequently the exact Rhat_M,12(1)<-1/10 and its pair Schur operator has a gauge-frustrated triangle for EVERY M>=3, with no M^2 or many-body matrix enumeration. Equation (6) applies to every such M at K=1, so the signed time-return and the positive-boundary-dilation obstruction persist for every finite U>0.

This is also a finite-accuracy obstruction at U=1, not only an exact sign distinction. Any entrywise nonnegative return approximation Rtilde satisfies

`integral_0^infinity exp(-t)|R_M,12(t)-Rtilde_12(t)|dt >1/10`.

For a finite classical SUBMARKOV boundary dilation, let Ftilde_hat=P(I-G)^(-1)P. Its inverse Schur matrix has off-diagonal entries<=0, regardless of its initial holding rates. The exact Fhat has `||Fhat^(-1)||<28`. If `eta=||Ftilde_hat-Fhat||<1/28`, inverse perturbation gives

`||Ftilde_hat^(-1)-Fhat^(-1)|| <=784eta/(1-28eta)`.

Its12 entry must change by more than1/10. Thus in all cases

`||Ftilde_hat-Fhat|| >=1/7868`.                       (9a)

The same constant lower bounds a claimed uniform-in-t operator approximation to F(t), since the exp(-t) Laplace integral has unit total weight. This statement concerns an effective family/return process, NOT arbitrary sampling at one selected beta. Coarse-grained latent models and nonrenewal global representations remain outside the excluded class. At large U, no uniform constant like (9a) is asserted; the negative exact return can be exponentially small.

This is a many-mode representation obstruction, not computational hardness. In particular K=1 has an ordinary M^2-dimensional exact Hamiltonian, and all calculations made here grant that polynomial ordinary solution. The result does not assert the same Schur entry sign at K proportional to M.

## 5. These are actual finite-volume interacting critical sources

For completeness this section acquires the critical occupation scope on the same connected family, rather than granting it from a zero-mode label. More generally, let T>=0 have a unique uniform zero mode on M>=2 sites, gap lambda>0 on its complement, and norm at most Lambda. Uniform U>0 is fixed. For total particle count N, put D=N-n0b-n0c and d=<D>.

Use f=diag(1,-1,0,...), `s=||fu||=sqrt(2/M)` and v=fu/s. Define Q=q1-q2 and `J=i(b0†bv-bv†b0)-i(c0†cv-cv†c0)`. The exact two-mode identities used in the frozen critical proof give

`Q^2<=2sum_i q_i^2`, `J^2<=4N(2D+1)`,

`<i[Q,J]>=2sN-4sqrt(Nd)` as a lower bound.

For d<=N/(8M), Robertson implies

`<sum_i q_i^2>>=N/[16M(2d+1)]`.

Therefore

`<H>>=lambda d+UN/[16M(2d+1)]`

`>=sqrt(lambda U N/(8M))-lambda/2`.

For d>N/(8M), use `<H>>=lambda N/(8M)`, and complete the scalar square. Both cases imply

`H_N >=c_M sqrt(N)-C_M`,

`c_M=sqrt(lambda U/(8M))`, `C_M=max(lambda/2,U/4)`.    (10)

The vacuum is treated directly. Polynomial dimension `binom(N+2M-1,2M-1)` against exp(-beta c_M sqrt(N)) makes the EXACT r=1 grand trace finite for every fixed M and beta>0, including every finite number moment. For (7), lambda may conservatively be replaced by4epsilon/M^2. This finite-volume statement is not a uniform thermodynamic pressure or density theorem.

The other side of the fugacity endpoint also needs a paid variational construction. Let Omega_K be the two-flavor uniform product condensate and set

`a=K^((M+1)/(2(M+3)))`, `X=sum_i q_i^2`,

`F=exp[-X/(2a^2)]`, `p=<Omega_K,F^2 Omega_K>`,

`psi=F Omega_K/sqrt(p)`.

Each multinomial vector lies in `|n_i-K/M|<=sqrt(6K)` for ALL i with probability at least5/6: sum the exact variances and apply Chebyshev. Partition the first M-1 coordinates into integer cells of side floor(a). At most `(16sqrt(K)/a)^(M-1)` cells meet the box. If both vectors fall in the same cell, then X<=M(M-1)a^2. Cauchy--Schwarz and exp(-1)>1/4 give the explicit normalization bound

`p>=b_M a^(M-1) K^(-(M-1)/2)`,

`b_M=(25/36)*16^(-(M-1))*4^(-M(M-1))`.               (11)

No squeezed-state norm oracle is assumed. The global Lipschitz bound ||grad F||<=1/a and the exact annihilation identity imply

`<D>_psi<=2K(M-1)/(M a^2 p)<=2K/(a^2 p)`.

The entropy of the tilted classical occupation law gives `<X>_psi<=a^2 ln(1/p)`. With `p_M=(M+1)/(M+3)<1`,

`E_trial(M,K)<=K^(p_M) [2Lambda/b_M`

`+U(ln(1/b_M)+(M-1)ln(K)/2)] =o(K)`                 (12)

for every FIXED M. This is an actual normalized all-K trial with explicit constants. Thus every r>1 diverges on the balanced subsequence, and the exact positive common-fugacity range remains0<r<=1 for every finite member of the connected family.

The constants and exponents in (11)--(12) are poor in M. They are not uniform at K=rho M. Achieving a small depletion bound through them can require log K of order M^3 or worse. A supposed fixed-density phase result must not take the fixed-M occupation limit silently.

## 6. Bare paired states lose finite-temperature critical Gibbs mass

There is a general algebraic bound which does not require first-return analysis. At fixed K,K let

`A0=(n0b+n0c)/(2K)`, `D=2K(I-A0)`.

For a UNIFORM zero mode, off-diagonal single-flavor hops leave the paired subspace, so

`P A0 P=P/M`.                                       (13)

For a normalized pure state psi, or a purification of any mixed state rho, split

`Ppsi=P sqrt(A0)psi+P(I-sqrt(A0))psi`.

The first operator has norm1/sqrt(M), and `(I-sqrt(A0))^2<=I-A0`. Hence with d=Tr(D rho),

`Tr(P rho)<=[1/sqrt(M)+sqrt(d/(2K))]^2`.              (14)

This says nothing unless the actual depletion is acquired. Here it is: for the canonical Gibbs state, the variational principle and entropy bound give

`E_beta<=E_trial(M,K)+beta^(-1) ln(D_(M,K)^2)`,

`d<=E_beta/lambda`.

Using (12), for every fixed M,U,beta and the connected source family,

`limsup_(K->infinity) Z_P/Z <=1/M`.                   (15)

The same holds for ground-state paired weight. Thus even at arbitrarily large but FIXED U, bare paired endpoints do not approximate the high-occupation critical Gibbs trace. Here trace distance means one half the trace norm. A normalized state supported on P differs in trace distance by at least1-Tr(P rho) from the true rho, as the two-outcome P measurement already witnesses. No claim that the upper bound1/M is sharp is needed.

If a putative dressing W has ||W-I||<=eta, every state W sigma_P W† with sigma_P supported on P has paired weight at least1-eta^2. It therefore cannot match the limit (15) with eta tending to zero. More quantitatively, if it is within trace distance delta of rho, then

`eta^2+delta >=1-Tr(P rho)`.

A NONPERTURBATIVE dressed/squeezed description is not excluded. This is a precise reason not to promote a pair-breaking gap2U or a formal second-order hopping term to an occupation-uniform near-identity effective theory. Standard Schrieffer--Wolff conditions already require control of occupation-enhanced matrix elements; they are not contradicted.

## 7. Strong ordinary routes and the operation still missing

There is a paid ordinary positive approximation, so the exact obstruction must not be promoted into a blanket rejection of pair theory. Let `D0=Q V Q>=2U I`, `W=Q H_hop Q>=0`, `J_K=2K Lambda`, so `||B||,||W||<=J_K`. For z>0 define

`S2(z)=zI+A-B†(D0+z)^(-1)B`.

The resolvent identity directly gives

`||S(z)-S2(z)||<=J_K^3/(2U+z)^2`.                    (16)

Every one-hop excursion from P has charge energy2U. The off-diagonal coefficient of S2 for moving a pair j->i is therefore

`-2|T_ij|^2 n_j(n_i+1)/(2U+z)`.

Thus S2 is stoquastic and matrix-free coefficients are acquired from the native bonds, not from Gibbs elements. This is ordinary second-order Feshbach/strong-coupling theory with a conservative, explicit canonical error bound. A sufficient U for small ERROR in this norm can grow with K; (16) is not a necessary lower bound or the best possible local analysis. It qualifies a projected RESOLVENT, not the full Gibbs trace, a thermal dressing or an efficiently mixing worldline sampler. It does not pay the fixed-U critical occupation limit in Section6.

Pair Hamiltonians, rotor models and paired loop/current Monte Carlo are established. Kuklov--Prokof'ev--Svistunov, [cond-mat/0306662v2](https://arxiv.org/html/cond-mat/0306662), Eq.(2) and surrounding derivation, explicitly exhibit quadratic occupation enhancement of pair hopping and a stability requirement for the residual pair repulsion. Our U q^2 is at their gamma=0 interaction boundary (after translating their U_intra=2U and V=2U). Their controlled positive gamma regime is not acquired by keeping only its hopping formula; neither is their unfrustrated loop ensemble a free exact representation of our frustrated source.

Feshbach/Nakajima--Zwanzig/Schur elimination is ordinary machinery. The sign found here is a native exact consequence, not a new theory of memory. [Bravyi--DiVincenzo--Loss, arXiv:1105.0675](https://arxiv.org/html/1105.0675), explicitly defines the dressed low-energy subspace and qualifies perturbative and local spin-system results. We grant such a qualified effective operator, all number-conserving Bogoliubov/squeezed corrections, canonical ED, correlated AFQMC, tensor and signed-memory methods on the SAME input. No theorem shows those methods inefficient.

The exact positive paired endpoint DOES NOT acquire a positive-renewal return process, a permanent oracle, the full canonical trace, or a near-identity high-occupation pair manifold. An algorithm may still work by globally correlated/nonrenewal proposals, a useful latent coarse graining, or a genuinely nonperturbative dressing. Acquisition and complete costs of THAT resource remain the actual missing operation.

Historical priority of these explicit native bounds is UNKNOWN. This construction closes a particular proposed shortcut, not the broader civilisation-capability mission.
