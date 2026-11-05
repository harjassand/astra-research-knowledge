# Coherent crossed flags: a carrier-discard obstruction

5 November 2026. This closes the payload-preservation gap for the unprimed crossed-filter architecture described in the earlier Schur record. It does not rule out arbitrary causal receivers, strong operations on incoming carriers, or a different physically established priming procedure. All flags may remain coherent throughout; no dephasing of flag histories is assumed.

## 1. Architecture and exact first update

Write c=cos(theta), s=sin(theta), D=1+3s^2 and let Phi be the normalized Bell projector on a payload qubit M and the incoming physical carrier E. The proposed isometry is

    W = |0> K + |1> L,
    K = (c I - 2 i s Phi)/sqrt(D),
    L = 2s (I-Phi)/sqrt(D).

After W, keep M and the coherent flag, and discard E. Any independent initial payload state is allowed, together with its purification in the receiver.

First specialize to the Bell initialization of M and a retained qubit P. The retained channel G:E -> M P flag is a complementary channel of the spent-E channel. Direct partial traces give exactly

    Tr_M[K(tau_M tensor X)K^dagger + L(tau_M tensor X)L^dagger]
      = t X +(1-t) tau_E Tr X,
    t=(1+s^2)/(1+3s^2).

A minimal complement of this depolarizing channel has Pauli Kraus weights

    p_0 = a=(2+3s^2)/(2D),
    p_x=p_y=p_z=b=s^2/(2D).

Its average output is diag(a,b,b,b). For an input Pauli sigma_mu/2, the two identity/Pauli off-diagonal entries have magnitude sqrt(ab), and the other two nonzero off-diagonal entries have magnitude b. Thus the balanced squared norm, and hence the Petz visibility of G, is

    lambda = 2sqrt(ab)+2b
           = [s sqrt(2+3s^2)+s^2]/D
           = sqrt(2) theta + O(theta^2).

This is an equality for the full coherent retained complement, not a statement about a measured version of its flags. Keeping a nonminimal Stinespring register changes G only by an output isometry.

Apply the exact acquisition ledger at the first collision. With r=1-s^4,

    a_1=lambda s^4,
    q_1=c^4+2lambda c^2s^2,
    ell_1^P=(1-lambda)s^4,
    ell_1^Q=2(1-lambda)c^2s^2.

Every continuation, including arbitrary processing of all coherent flags, therefore obeys

    a_N <= 1-r^N -(1-lambda)[s^4+2c^2s^2(1-r^(N-1))].

Combining with epsilon >= (3/4)(1-sqrt(a_N)) proves an order-theta^2 error floor for this initialization whenever r^N is small. In particular the leading necessary error is at least (3/4)theta^2+O(theta^3).

For any independent initial payload/workspace state, the isometry distance from doing nothing to M,E and appending a zero flag is exactly

    ||W - |0>I|| = sqrt[2(1-c/sqrt(D))] = 2theta+O(theta^3).

The corresponding retained channel G is within this half-diamond distance of a replacer. Its best entanglement fidelity is consequently at most 1/4+sqrt[2(1-c/sqrt(D))]. Its average Petz visibility lambda_bar is at most (4/3)sqrt[2(1-c/sqrt(D))]=O(theta). The same averaged first-step ledger formulas hold with lambda_bar, even without covariance. Thus an independent pure initialization cannot remove the leading first-step loss.

## 2. A nonzero weak-angle error floor over a diffusive prefix

The first-update obstruction alone leaves epsilon >> theta^2 open. A stronger argument examines the inaccessible purifiers of the fresh thermal carriers. It permits arbitrary additional controls on the retained registers between updates, provided each arriving carrier interacts with the receiver only through W before being discarded. History-dependent selection or basis changes of the payload register only change a bounded receiver observable below. No additional strong operation on the incoming E is included in this scope.

Purify each fresh carrier E_j with an inaccessible qubit F_j in Phi_(E_j F_j). The emitted carrier undergoes U_(S,E_j), then W_(M,E_j), and its spent E_j is inaccessible. On the inaccessible pair E_j F_j measure the bounded Hermitian observable

    O_j = i [sigma_z^(E_j), Phi_(E_j F_j)],     ||O_j||=1.

This is only a converse measurement on an environment; the receiver is not given any purifier or extra access. Different j give commuting observables. The effective observable before this collision, on S and the selected payload, is

    A_theta = <Phi_EF| U^dagger W^dagger O W U |Phi_EF>
            = theta(sigma_z^S - (sigma_z^M)^T) + O(theta^2),

The exact finite-angle expression is

    A_theta = [cs(1+s^2)/D] Z_S - [c^3s/D] Z_M
              + [c^2s^2/(2D)](X_S Y_M+Y_S X_M).

Here Z_M^T=Z_M. Its odd-parity block has eigenvalues +/-2cs/D; its even-parity block has eigenvalues +/-cs^2/sqrt(D). Therefore

    ||A_theta|| = h_theta = 2cs/D <= 2theta.

The expansion and its uniform operator-norm remainder follow directly. The exact expression was also independently checked by symbolic 16-dimensional contraction.

Consider logical inputs |0><0| and |1><1|. The source polarization before step j is exactly +/- c^(2(j-1)). For every receiver, the total accessible ledger visibility satisfies a_(j-1)<=1-r^(j-1)<=s^4(j-1). If B is any receiver observable with ||B||<=1, balanced Cauchy-Schwarz gives

    |Tr B [E_(j-1)(|0><0|)-E_(j-1)(|1><1|)]|
        <= 2 sqrt(3 a_(j-1)).

Indeed the balanced Pauli image has squared norm at most 3a, and ||sigma^(1/4) B sigma^(1/4)||_2<=1 by Schatten Holder. The bound applies to a history-controlled choice of B by including the complete classical record in the receiver. Consequently, uniformly for j<=n=floor(alpha/theta^2),

    E_+(O_j)-E_-(O_j)
      =2theta c^(2(j-1))+O_alpha(theta^2).

Let Y_j be the measurement result of O_j and Z_n=sum_j Y_j. Summing gives

    theta [E_+(Z_n)-E_-(Z_n)] -> 2(1-exp(-alpha)).

For either input, the conditional mean of Y_j, conditioned on all earlier converse measurement outcomes, is bounded by 2theta+O(theta^2), because the fresh E_jF_j pair is independent and ||A_theta|| has that bound. Decompose Z_n into its martingale differences and predictable means. The martingale part has second moment at most n, and the predictable part has magnitude at most n[2theta+O(theta^2)]. Thus

    E_+(Z_n^2)+E_-(Z_n^2)
       <=4n+4n^2[2theta+O(theta^2)]^2.

For any distributions P,Q and real statistic Z,

    TV(P,Q) >= |E_P Z-E_Q Z|^2 /
               [2(E_P Z^2+E_Q Z^2)].

This follows from Cauchy-Schwarz with weight p+q and (p-q)^2/(p+q)<=|p-q|. It follows that the inaccessible environment distinguishes the two logical inputs with limiting advantage at least

    liminf_(theta->0) D_env
      >= (1-exp(-alpha))^2 / [2alpha(1+4alpha)] >0.

If a final decoder has Bell fidelity at least 1-epsilon, purification and Uhlmann's theorem imply D_env<=2sqrt(epsilon). Indeed the complementary Choi state is within trace distance sqrt(epsilon) of a product with the maximally mixed logical reference; measuring that reference in the z basis gives the stated bound. A half-diamond recovery error <=epsilon implies this Bell-fidelity premise. Therefore

    liminf_(theta->0) epsilon
      >= (1-exp(-alpha))^4 / [16 alpha^2(1+4alpha)^2].

For example alpha=1/2 gives the explicit positive constant

    (1-exp(-1/2))^4 / 36  = 0.0006658... .

This lower bound applies whenever the available stream extends beyond floor(alpha/theta^2), in particular at the proposed theta^-4 log(1/epsilon) acquisition horizon. Later coherent flag processing cannot erase information already carried by the discarded E_jF_j environment.

## 3. Explicit finite-parameter form

Define

    u_theta=cs(1+s^2)/D,   v_theta=c^3s/D,
    w_theta=c^2s^2/D,     h_theta=2cs/D.

After any k exactly retained priming carriers, examine the next n W-only updates. The source term, the accessible-information upper bound, and the norm of the displayed cross term give

    B(theta,k,n) = 2u_theta c^(2k)(1-c^(2n))/s^2
                  -2sqrt(3) v_theta s^2 n sqrt(k+n)
                  -2w_theta n,
    E_+(Z_n)-E_-(Z_n) >= B(theta,k,n).

In particular, for every horizon N>=k+n and every continuation of this architecture,

    epsilon >= [max(B(theta,k,n),0)]^4 /
               [256 n^2 (1+n h_theta^2)^2].

This is an exact finite-parameter lower bound. It need not be sharp, and can be vacuous at larger angles. It uses no perturbative extrapolation in n. The earlier weak-angle constant is its k=0, n=floor(alpha/theta^2) limit.

## 4. Priming scope

Suppose the receiver first exactly retains k carriers, then switches to W-only processing and spent-carrier discard. The same proof applies to the next n=floor(alpha/theta^2) updates. If k theta^2 -> beta<infinity, accessible information during this prefix is still O(theta^2), while the source polarization contributes the factor exp(-beta). Thus the lower bound above is multiplied by exp(-4beta). In particular any k=o(theta^-2) priming prefix has the same nonzero limiting obstruction.

For beta growing with theta, the displayed limiting formula must not be extrapolated without remainder control. The exact finite-parameter bound in Section 3 determines its valid regime. This leaves a genuinely different, sufficiently long primed scheme open; no sufficiency theorem for such a scheme is supplied here.

## 5. Consequence and remaining endpoint

The coherent sparse flags have a valid occupation tail bound, but that bound cannot be combined with high-fidelity recovery for the stated unprimed spent-carrier-discarding architecture: the operation itself has a nonzero weak-angle recovery error floor. This argument retains all flag coherences.

The broader task remains open here. A receiver can interact strongly with an incoming carrier, retain it, use a different isometry, or attempt a proven priming/compression scheme. The general acquisition ledger allows all of these. This argument does not establish a width-dependent converse for that full class and does not produce a matching low-memory reader.
