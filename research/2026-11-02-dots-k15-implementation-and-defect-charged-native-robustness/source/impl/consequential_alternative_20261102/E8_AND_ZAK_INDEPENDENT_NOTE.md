# Independent GKP seed attack and Zak-interface check

## Outcome

No beyond-hashing seed was found. A genuine four-mode correlated seed, the E8 qunaught, was constructed and tested rather than extrapolating tensor-product code size. Its two selected character types fail the sufficient rho>beta gate at v=1/e and at v=.37; all selected finite repetition lengths n=1,2,3,5,10 also have negative estimated coherent information at v=.37. A restricted diagonal symplectic-squeezing search found only coarse-sample false positives that became negative on fresh 2^18-point evaluations. These are numerical diagnostics, not rigorous converse/capacity certificates or globally exhaustive searches.

Two exact useful reductions were established: tensor-product seeds cannot improve the ratio rho/beta beyond their factors; and halfshift symmetry provides bounded Gaussian-sample estimators for beta and the full finite-block coherent information. The parent's compact-chart Zak regularization is valid as a finite-energy channel-existence argument with the stated caveats below; established subsystem-decomposition prior must be credited.

## Genuine correlated E8 seed

Write E8 = D8 union [D8+(1/2,...,1/2)], D8={z in Z8: sum z even}. It has Euclidean dual E8. The paired-coordinate complex structure J(x1,x2,...)=(-x2,x1,...) preserves E8: for integer vectors even sum is preserved modulo2; for half-integer vectors the integer-coordinate sum changes by an even number. Thus Lambda0=sqrt(2pi)E8 is symplectically selfdual for four canonical modes. This is a valid qunaught lattice, not an illegal homothetic dimension change.

For integer v0 in E8 define chi(lambda)=v0 dot lambda mod2 and halfshift t=Jv0/2 in lattice-normalized coordinates (an immaterial overall sign depends on Omega convention). Tested v0=(1,-1,0,...,0) and v0=(2,0,...,0). No exhaustive orbit statement under squeezed metrics is claimed.

Set c=pi/v. For h=0,1/2 let
 A_j(h)=sum_z exp[-c(x_j+z+h)^2],
 B_j(h)=sum_z (-1)^z exp[-c(x_j+z+h)^2].
Then the unnormalized wrapped density is
 G(x)=1/2 sum_h [product_j A_j(h)+product_j B_j(h)].
For parity p_j=v0_j mod2, replace A by B in coordinates with p_j=1, and B by A in the complementary product, multiplying each h term by exp(i pi h sum_j v0_j). This gives the signed theta sum F. The tested choices make the phase real. These products are exact infinite-sum formulas; scripts truncate 1D sums to z=-4,...,4.

Independent diagonal symplectic squeezes S=diag(exp(a1),exp(-a1),...,exp(a4),exp(-a4)) preserve validity and keep the formula separable after v_j=v/S_jj^2, x=S^-1 xi/sqrt(2pi). This is a restricted four-parameter family, not full Sp(8).

At v=1/e the unsqueezed QMC diagnostic gives rho-beta approximately -0.01855 (root type) and -0.02094 (norm4 type). At v=.4318 the differences are approximately -0.2326 and -0.2649. Thus even exceptional Euclidean packing does not supply the conditional logical-entropy benefit needed here.

## Exact tensor-product exclusion

If Lambda0 is an orthogonal direct sum of selfdual factors, every binary character factors and t decomposes. Hence G=product G_j, F=product F_j,
 rho=product rho_j, beta=product beta_j.
Trivial character factors contribute rho_j=beta_j=1. If every nontrivial factor has rho_j<=beta_j, the product cannot satisfy rho>beta. A passive symplectic orthogonal rotation leaves the Gaussian measure and all these integrals unchanged. Therefore passive optical mixing and tensoring failing rectangular/hexagonal seeds cannot open this gate. This is not a converse for active correlations, arbitrary lattices, finite-n positivity, or arbitrary bosonic codes.

## Bounded estimators: exact halfshift symmetrization

Let R(s)=g(s+t)/g(s), with 2t in Lambda0. Any function invariant under s->s+t has equal expectation under g and g_t. Therefore
 beta = E_g[ 2 sqrt(R)/(1+R) ] = E_g sech[(log R)/2].
This estimator lies in [0,1], unlike E_g sqrt(R). Because rho=E_g r^2 also lies in [0,1], rho-beta is the expectation of a random variable in [-1,1]. Ordinary independent Gaussian samples modulo the lattice permit Hoeffding concentration. Scrambled Sobol points in the scripts are diagnostics; their printed iid standard-error proxy is not a valid QMC confidence certificate.

For n copies draw S_j iid with wrapped density g, put U=product_j r(S_j) and L=sum_j log R(S_j). Global halfshift symmetry gives exactly
 I_c(n)=E[1-h2((1+U)/2)-h2(logistic(L))].
The integrand is bounded in [-1,1]. This avoids rare-tail error from the equivalent E_g log2(1+exp L) formula. It evaluates the actual finite-n information, not only the sufficient exponent gate.

## Parent's compact-chart Zak construction: independent check

The parent's suggestion is to use |b,s>=D(s)|b,0>, a normalized real smooth compactly supported phi inside one stabilizer syndrome chart, and the physical code isometry V_phi|b>=integral phi(s)|b,s>ds. This does not require Gram inversion: direct-integral fibers give exact orthogonality. Compact support avoids the bundle boundary twists.

For one canonical d-dimensional square code let a=sqrt(2pi/d), L=d a. A conventional Zak transform is
 Z_b psi(sq,sp)=a^-1/2 sum_m exp(-i L m sp) psi(sq+a b+L m).
The displacement-defined chart differs by the scalar phase exp[i sp(a b+sq/2)]. On the common chart function phi the quadrature operators are
 q = sq/2 + i partial_sp,
 p = sp/2 - i partial_sq.
They obey [q,p]=i. For real phi in C_c^infty, normalized, the cross terms vanish and
 <q^2+p^2> = ||grad phi||_2^2 + (1/4) E_phi[|s|^2].
Thus <n> = (1/2)||grad phi||²+(1/8)E|s|²-1/2. Smooth compact support yields finite energy; scaling phi_epsilon(s)=epsilon^-k phi(s/epsilon) in 2k dimensions gives the expected epsilon^-2 energy cost. For general lattice normal form, metaplectic transformation adds its singular-value/condition constants: <N+k/2> <= ||S||² <N_0+k/2>. One should prove the chosen symplectic normal-form connection explicitly, not suppress those constants.

For each displacement xi, the map s->sout=(s+xi) mod Lambda^perp is a bijective torus translation. Writing s+xi=sout+gamma, the action is a scalar Weyl phase times the logical W_gamma. Tracing the syndrome therefore sets s=s' and gives exactly the ideal Pauli-and-analog-syndrome channel for effective displacement density f_v*|phi|². No logical gauge phase remains because it is scalar in the displacement-defined chart.

Norm convention: (1/2)||implemented-ideal||_diamond <= TV(f_v*h,f_v) <= E_h ||s||/(2 sqrt(v)) <= epsilon/(2 sqrt(v)). Full diamond norm has twice this bound. An untouched entangled reference is preserved by the same random-unitary/data-processing argument.

This is a finite-energy existence construction, not yet a finite-resource physical decoder. The ideal stabilizer subsystem trace is established prior art, and exact syndrome measurement is not itself an acquired physical primitive. Finite input Fock truncation, finite syndrome discretization/output cutoff, and an implementable approximate decoder still need pricing if one claims a practical operation. For a capacity-existence witness a finite approximation plus a strict information margin should suffice, but no such beyond-hashing margin was found here.

## Primary prior inspected

1. Conrad–Eisert–Arzani, 'Gottesman–Kitaev–Preskill codes: A lattice perspective', https://arxiv.org/html/2109.14645v2 . Symplectic lattice classification, theta-function maximum-likelihood decoding, glued lattices and lattice tensor products are established machinery, not inventions of this note.
2. Burchards, 'Continuous Variable Quantum MacWilliams Identities', https://arxiv.org/html/2502.09514v1 . E8/Leech statements concern distance bounds; they do not prove a beyond-hashing channel-capacity advantage.
3. Hillmann–Eisert–Arzani, 'Quantum low-density lattice codes', https://arxiv.org/html/2609.03021v1 . Native lattice/decoder co-design and analog message passing exist; its abstract/introduction do not provide the target rho>beta or close additive-capacity gap.
4. Shaw–Doherty–Grimsmo, 'Stabilizer Subsystem Decompositions for Single- and Multimode Gottesman–Kitaev–Preskill Codes', PRX Quantum5,010331 (2024), https://arxiv.org/abs/2210.14919 , https://doi.org/10.1103/PRXQuantum.5.010331 . The subsystem trace equals ideal decoding. The Eq64 discussion explicitly states exact ideal decoding is not physically implementable via the ideal stabilizer-measurement procedure, whose ancilla is nonnormalizable; approximate EC is left separate.
5. Pantaleoni–Baragiola–Menicucci, 'The Zak transform: a framework for quantum computation with the Gottesman–Kitaev–Preskill code', https://arxiv.org/html/2210.09494v2 . Credits the Zak framework and error-correction logical–gauge twist.

## Executed artifacts

e8_seed.py, e8_results.json: unsqueezed theta/Gaussian-QMC diagnostics.
e8_squeezed_unbounded_historical.py: original unbounded estimator retained to expose false positive risk.
e8_squeezed.py, e8_squeeze_results.json: bounded-estimator squeeze search and independent higher-resolution reevaluation.
e8_finiteblock.py, e8_finiteblock_results.json: finite-n entropy diagnostics, all tested values at v=.37 negative.

No repository was mutated. No physical preparation, novelty, general no-go, certified positive rate, or practical advantage is claimed.
