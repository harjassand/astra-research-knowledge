# Rank, ambient dimension and signal in compiled recovery

2026-10-27. Root-proposed centered-effect argument, independently reconstructed here; frozen for receiving.

## Source and deployment contract
Known integers 1<=r<=D and s>=3D, p=r/D. Let V:C^(3D)->C^s be an unknown Haar embedding. The source is
E_V(X)=V[X tensor P_r/D+Tr(X) I_3/3 tensor (I_D-P_r)/D]V*.
Calibration makes at most n ordinary physical queries with arbitrary coherent adaptive operations. All calls precede the independent datum. At deployment allow arbitrary classical storage Z and at most m-dimensional retained source-dependent quantum storage Q; all other ancillas are fresh and source independent conditional on Z. The classical-only case is m=1. Uniform training-averaged complete unhalved diamond error is at most p/4 relative to G_p.

Write
Jinfo=ln(s/(3D))+2p ln3 >0.
Then classical-only deployment requires
n>=sr/(32 Jinfo).
With retained quantum dimension m,
nm>=sr/(64 Jinfo).
Independently, the uniform guarantee over embeddings permits restriction to a fixed known 3D-dimensional output support, giving the already received memory-unrestricted lower n>=D^2/128. These bounds may be combined; none asserts an optimal memory tradeoff or catalytic reuse.

## 1. Per-query information includes unknown support
Let Q_in denote the next qutrit input and M retained memory. Conditional on V, the output is the orthogonal mixture of a success state with weight p and a replacement state with weight1-p. Direct entropy evaluation gives
S(B|M,V)=ln(3D)-p[ln3-S(Q_in|M,V)].
This holds for arbitrary query entanglement and source-dependent conditional inputs. At p=1 it reduces to tensoring the r-dimensional mixed flag and an isometric embedding; at p<1 the binary mixing entropy is included in ln D.

Therefore the information increment is exactly
I(V:BM)-I(V:Q_in M)
 =S(B|M)-ln(3D)+p[ln3-S(Q_in|M,V)]-I(V:Q_in|M).
Using S(B|M)<=ln s, S(Q_in|M,V)>=-ln3 and I(V:Q_in|M)>=0 gives the bound Jinfo. Known calibration processing and final compression cannot increase information, so
I(V:ZQ)<=n Jinfo.
The term ln(s/(3D)) is essential: the unknown occupied support can itself reveal source information. It has not been dropped as if the entire ambient output were maximally mixed.

## 2. Center the decoding effects before transport
Realize V using the first3D columns of Haar U in SU(s). Let P_a(U) be the embedded rank-r projector for logical basis state a, and P=sum_a P_a. The three labeled physical data states consist of P_a/D plus a common replacement term.

For each classical z let T_a(z) be the decoder's accepted-correct-label effect on Q tensor B, with T_a>=0 and Ttot=sum_a T_a<=I. Define tildeT_a=T_a-Ttot/3. Then sum_a tildeT_a=0 and -I/3<=tildeT_a<=I, so each is a Hermitian contraction.

The actual centered success witness is
W=Pr(accepted correct label)-Pr(accepted)/3
 =E_U Tr[rho_U^(ZQ) f(U)],
f(U)|_z=(1/(3D))sum_a Tr_B[P_a(U) tildeT_a(z)].
All common reset and support terms cancel exactly, even though the physical datum marginal is not source independent. Haar averaging each P_a gives rI/s, so E_U f(U)=0 as an operator on the retained memory.

Complete error p/4 implies correct-label probability>=7p/8 and acceptance<=9p/8. Hence W>=p/2.

## 3. Scalar and operator gradients
For classical-only deployment the scalar HS square gradient is
Gamma(f_z)=||sum_a[P_a,tildeT_a]||_F^2/(9D^2)<=2r/D^2.
Indeed each rank-r projector commutator with a Hermitian contraction has HS square at most2r, and the three-term Cauchy inequality gives18r in the numerator.

For retained dimension m, operator Parseval and the legitimate rank-times-memory bound from bounded_quantum_memory_rank_ambient_tradeoff.md give
Gamma(f)|_z=Tr_B(X*X)/(9D^2)<=4mr I_Q/D^2,
X=sum_a[P_a,tildeT_a].
This explicitly retains the m factor from Tr_B(H P H); it does not use a false rank-only partial-trace bound. Classical Z is treated as a direct-sum algebra of m-dimensional blocks, not as an additional quantum dimension. Arbitrary classical alphabets follow by the received finite decoder-net approximation.

## 4. Heat transport and lower bounds
The received scalar/complete heat-transport lemma on HS SU(s), with entropy-decay rate s, bounds a centered test of square-gradient at most g by
|E Tr rho_U f(U)|<=2sqrt[g I(U:memory)/s].
Classically, p/2<=2sqrt[2r I/(sD^2)] gives I>=sr/32. With retained dimension m, p/2<=4sqrt[mr I/(sD^2)] gives I>=sr/(64m). Combining with the per-query Jinfo budget proves the stated bounds.

## Boundaries
The lower is for the specified canonical source embedded in a larger unknown support, known r,D,s,p, fixed query cap, and pre-datum calibration. It allows arbitrary coherent query entanglement during training. It does not cover interleaved post-datum calls, expected-cost algorithms, uncounted source-dependent ancillas, indefinite causal order, or an automatically reusable quantum program. No historical priority claim is made.

Dependencies: complete_mlsi_direct_heatflow_transport_lemma.md; variance_transport_joint_adaptive_lower_root.md; bounded_quantum_memory_rank_ambient_tradeoff.md; classical_compilation_rank_ambient_corollary.md.
