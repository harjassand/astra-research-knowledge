# Exact noisy-program conversion and the valid Choi interface

2026-10-29. Root construction and exact arithmetic; independent review pending. Depends on the accepted four-output transducer and the separately reviewed IID isotropic program source. No new universal programming algorithm is claimed.

## Input and operation
For one unknown real rotation program c_R=vec(R)/sqrt3, obtain TWO INDEPENDENT copies of
 tau_v=(1-v)|c_R><c_R|+(v/8)(I_9-|c_R><c_R|).
For the intended purification branch assume0<=v<=8/9. The exact matrix transfer also holds for0<=v<=1, but beyond8/9 the resulting Pauli channel is not a convex identity/depolarizing mixture.

Apply the fixed known Kraus contraction K=(4/sqrt3)T from the four-program extension. On success discard three of its four quaternion registers and retain only one. Fresh repetitions use independent acquisition/conversion batches. Within one successful four-program output the registers need not be independent when v>0; do not treat all four as IID ports.

## Exact covariance, not a fitted orientation claim
Let q be a quaternion and R(q) its homogeneous quadratic rotation matrix. Left and right unit-quaternion multiplication act orthogonally on q in R4; the corresponding two SO(3) rotations act orthogonally on vec(R) in R9. Their tensor squares and fourth powers are orthogonal representations. The span S of vec(R(q))^tensor2 has dimension35, and the polynomial identity defining T maps every spanning vector to q^tensor4. Thus this intertwining identity holds on S. T annihilates S-perp because its certificate is the Moore--Penrose left inverse of the coefficient embedding (with the correct monomial multiplicity mapping J on the output). S and S-perp are invariant under the orthogonal group action. Therefore T intertwines on the full81-dimensional input space.

At R=I, the stabilizer acts as the full SO(3) rotation of the quaternion imaginary3-space while fixing the scalar component. After discarding three output programs, Schur's lemma gives a scalar target block and an isotropic orthogonal block; covariance transports the result to every unknown R. The calculation below evaluates their exact values rather than inferring them numerically.

## Exact transfer law
Write tau_v=a I_9+b P_c with a=v/8,b=1-9v/8. The program pair is a² I_81+ab(I⊗P_c+P_c⊗I)+b²P_c⊗P_c. At c=vec(I)/sqrt3, exact rational contraction and partial trace give:
 C0=(9/2) I_4,
 C1=diag(41/18,31/54,31/54,31/54),
 C2=diag(16/27,0,0,0).
The unnormalized retained program is a²C0+abC1+b²C2. Hence conversion success is
 p(v)=(405v²-720v+512)/864,
and its normalized infidelity is
 w(v)=3v(62-9v)/(405v²-720v+512).
The retained state is exactly
 (1-w)|q_R><q_R|+(w/3)(I_4-|q_R><q_R|).
For small v, w(v)=(93/256)v+O(v²); the conversion itself suppresses this specific isotropic program error while consuming two programs and heralding. At v=0 it recovers16/27 success and a pure q program. At v=8/9 it has success2/9 and outputs I4/4: no orientation can be generated from isotropic input.

## Valid noisy Choi resource
The established fixed Bell-basis conversion sends |q_R> to the normalized Choi vector of V_R (or its inverse, with the separately fixed convention). It sends I4 to I4. Therefore the retained program is EXACTLY the Choi state of
 E_R=(1-4w/3) U_R+(4w/3) D_2,
for0<=w<=3/4. Its input marginal is I2/2. This is stronger than a generic trace-distance estimate on a noisy program: it is a physical trace-preserving channel resource with specified output noise. Its half-diamond distance from U_R is w, since halfdiamond(D2,id)=3/4.

## Port-based processor consequence and exclusions
For product Choi states of a fixed channel E, a deterministic port-based teleportation processor acts only on the input and A halves, so all E maps on B halves commute through its measurement; tracing unused B halves leaves exactly E after the corresponding ideal-port teleportation channel. Independent batches therefore incur the above output-noise cost ONCE per executed gate, rather than N times for N ports. The primary PBT fidelity/compiler bound is being received separately and is not proved by this transducer calculation.

One cannot use this factorization for generic correlated quartets or a generic non-Choi state. Noise between independent batches, correlated acquisition memory, finite-cap conditioning, protected control imperfections and finite circuit synthesis need explicit accounting. A public cap on stochastic program acquisition can bias the program state; one must retain its full failure flag/instrument and separately bound truncation error, not silently use the uncapped law after a cap.

## Reproduction and importance
check_noisy_transducer.py reconstructs T from the immutable four-program exact certificate, evaluates C0,C1 and the polynomial transfer, and writes check_noisy_transducer.json. This is exact rational arithmetic, not fitted Monte Carlo. The intended consequence is a paid approximate unknown-frame gate interface from a noisy irreversible source; it is not a quantum-memory advantage, a hardware result, or a demonstrated superiority to classical frame estimation.
