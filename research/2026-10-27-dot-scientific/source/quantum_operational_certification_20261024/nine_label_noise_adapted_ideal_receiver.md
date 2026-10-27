# Ideal nine-label noise-adapted receiver: conservative full-throughput bound

2026-10-27. Proof candidate, independent audit requested. The eigenvectors/projectors in this file are analytical ideal objects, not supplied source oracles. Learned implementation requires the separate weighted branch lemma.

Use the received discriminant notation H=pPhi_V-D, positive eigenvector chi, eigenvalue lambda, overlap f=|<Phi_V,chi>|², and

 t=(2p/3-lambda)/p, e<=5epsilon_ent.

Assume e<=p/160, so t<=5e/(3p)<=1/96. The received resolvent argument supplies a positive3x3 matrix G with

 TrG=3, ||G||<=1/(1-t)<=3/2,
 ||G-I||<=2t/(1-t)<=3t,
 f>=1-3t/2,
 K_chi V=sqrt(f)G/3,
 ||K_chi V-I/3||<=3t/2,
 q<chi|I_A tensor tau|chi><=5e/2.

Here K_chi is the physical Bell-contraction Kraus operator, including the normalized receiver Bell ancilla. The genuine input-to-output coefficient is1/3, not1.

## 1. The nine Weyl orbit vectors form an almost orthonormal frame

Let chi_j=(W_j tensor I)chi for the nine qutrit Weyl operators on A. Their code component is sqrt(f)(I tensor VG)Phi_3, up to the equivalent transpose convention, and their outside-code component is orthogonal on B. Consequently

 chi_A=(f/3)(G²)^T+K_out,
 K_out>=0, TrK_out=1-f TrG²/3<=1-f<=3t/2.

Thus

 ||chi_A-I/3||
 <=[||G²-I||+(1-f)||G²||]/3+||K_out||
 <=[7.5t+3.375t]/3+1.5t=5.125t.

The9x9 Gram matrix F of the chi_j has eigenvalues3 times the eigenvalues of chi_A, each repeated3, by Weyl twirling of the frame operator. Hence

 ||F-I_9||<=15.375t<=16t.                            (1)

This uses no physical whitening operation; it is a property of the ideal frame.

## 2. Sequential projectors and genuine-code error

Measure P_j=|chi_j><chi_j| sequentially, retain the data on rejection Q_j=I-P_j, stop at the first accepted label, apply its known Bell correction, and erase if all nine reject. For label j the unnormalized accepting row is

 r_j=<chi_j|Q_(j-1)...Q_1.

The exact telescoping identity gives

 r_j-<chi_j|=-sum_(k<j)<chi_j|chi_k> r_k.

Every r_k has norm at most1. By(1),

 ||r_j-<chi_j|||<=8(16t)=128t.

Bell contraction with the normalized local Bell ancilla maps a row perturbation of norm a to a logical Kraus perturbation of operator norm at most a/sqrt(3), and therefore certainly at most a. The Weyl correction maps the single-label code Kraus back to sqrt(f)G/3. Hence the corrected sequential code Kraus L_j satisfies

 ||L_j-I/3||<=130t.

Its norm is at most1/sqrt(3), since the accepting row has norm at most1. Therefore the unhalved diamond distance between rho->L_j rho L_j* and rho->rho/9 is at most130t: use (||L_j||+1/3)||L_j-I/3|| and1/sqrt(3)+1/3<1.

Summing the nine accepted maps costs at most1170t. Replacing the missing accepted trace by erasure costs at most the same amount. Thus the COMPLETE genuine-code instrument differs from identity (acceptance weight1) plus zero erasure by at most2340t. Its original-source contribution is at most2340pt.

## 3. Reset acceptance is O(e), not O(p)

For any purification of the reset marginal S=I_A/3 tensor tau, define

 a_j=||r_j sqrt(S)||_2, b_j=||<chi_j|sqrt(S)||_2.

The row identity implies a_j<=b_j+sum_(k<j)|F_jk|a_k. The strictly lower-triangular matrix of absolute off-diagonal Gram entries has operator norm at most its Frobenius norm, which is at most||F-I||_F<=3||F-I||<=48t<=1/2. Hence

 sum_j a_j²<=4sum_j b_j².

Every Weyl rotation has the same reset expectation, so q b_j²<=5e/6. The total reset acceptance probability, including its source weight q, is therefore at most

 4*9*(5e/6)=30e.

The complete accepted-plus-erased reset output differs from pure erasure by exactly twice its accepted mass, at most60e.

## Result and scope

The complete ideal nine-label receiver has target channel

 p identity+(1-p)erasure

and unhalved diamond error at most

 2340pt+60e<=3960e<=19800epsilon_ent.                 (2)

The constant is deliberately loose. For fixed relative accuracy this retains a sufficient entropy-deficit scale Delta=O(p²). It does not establish that the tolerance or constants are optimal.

This is an IDEAL receiver analysis. The projectors are not assumed physically known. A full source-unknown implementation at p0^-2 training cost still needs the weighted learned accepted/rejected branch estimates, their multi-label telescoping, and an explicit final budget. Generic uniform diamond simulation alone would require absolute error O(p) and revert to the previously known p0^-3 cost.
