# Weighted complete branch estimates for a repeated noise-adapted classifier

2026-10-27. New proof candidate, independent audit requested. This is NOT yet the full nine-label recovery theorem. It builds on the received local CQ cone estimates in `nine_label_interaction_picture_energy_lemmas.md`.

## Setup and notation

For one label, H=pPhi-D=4sigma-6rho has a unique positive eigenvalue lambda<=p and rank-one projector Pchi. Let H_-=(-H)_+, so

 D=H_-+pPhi-lambda Pchi, TrH_-=2+lambda<=3.

Programs sigma=T_j,rho=omega satisfy sigma,rho<=D. Let one coherent finite-QPE classifier have ideal acceptance probability at most eta on the negative/zero spectrum. It computes, classifies and uncomputes, so its exact-evolution Kraus operators are functions of H. Its actual implementation uses fresh mixed-program signed pairs, with every |delta|<=1/10 and total squared pair time h=sum delta². All ancillary registers are initialized independently. Rejection RETAINS the data; only the eventual receiver erases it.

A positive CQ state relative to the H eigenbasis has form sum_i R_i tensor|i><i|. Say its cap is k if

 Tr R_i<=k(-lambda_i)_+ for every i.

Consequently its trace is at most3k. A separate arbitrary positive remainder is charged as pR, with TrR=t. Every known ancillary gate and controlled ideal H evolution preserves the CQ cap. Ancillary outcome selection can only decrease it.

## 1. Local caps, including control attenuation

The received complete signed-pair inequality implies that an actual pair maps a positive CQ state of cap k to a state dominated by

 Q_new+pR_new,
 cap(Q_new)<=(1+25000delta²)k,
 TrR_new<=25000delta²k.

Indeed the local auxiliary error has trace at most8308 times the CQ trace, hence at most24924k. Split D<=H_-+pPhi, and include the delta²R0 term. Arbitrary trace-p remainders remain trace-p under the complete actual channel.

For local comparison with the IDEAL pair, control attenuation adds a signed CQ difference. With c=cos(4delta)cos(6delta),

 ||A R_i A*-R_i||1<=2(1-c)TrR_i<=52delta²TrR_i.

The same bound holds after the ideal ancillary unitary in that eigenspace. Its absolute value is a positive CQ majorant. Combining52 with24924+1 is still below25000. Therefore the signed local actual-minus-ideal error has a COMMON positive majorant Qerr+pRerr, for both signs, with

 cap(Qerr)<=25000delta²k, TrRerr<=25000delta²k.

This does not assume A R_i A*<=R_i. It explicitly pays the selected-branch interference of attenuation.

## 2. Whole-circuit CQ branch error

A positive cone pair(k,t) propagates through actual pairs with

 k'<=k(1+25000delta²), t'<=t+25000delta²k.

Thus k+t grows by at most exp(50000 sum delta²). Telescoping actual-minus-ideal circuits, using IDEAL prefixes and ACTUAL suffixes, is legitimate: each local signed error is bounded above and below by a positive cone majorant, and CP suffixes preserve both inequalities. No noncommuting Jordan-part domination is assumed.

For input H_- and ANY selected branch b of a circuit whose total squared pair time is Htot, define

 e(Htot)=100000 Htot exp(50000 Htot).

After discarding ancillary registers the branch difference satisfies

 +/-[Psi_b,actual(H_-)-Psi_b,ideal(H_-)]
 <=e(Htot) H_-+p R_b,
 R_b>=0, TrR_b<=e(Htot).                             (1)

The constants are conservative: summing local cap-plus-remainder budgets gives at most50000Htot exp(50000Htot). Intermediate ancillary measurements can equivalently be deferred; fresh program discards are already included in the local CP pair maps.

## 3. Repetition suppresses the accepted negative-spectrum coefficient

For ONE classifier let e=e(h) and beta=eta+e<1. Its actual accepted CP map A obeys, by(1),

 A(H_-)<=beta H_-+pR, TrR<=e.

With L fresh classifiers, accept only if all L accept; reject at the first failure, retaining the data. Positivity and trace-nonincreasingness give

 Tr A^L(H_-)<=3beta^L+p e/(1-beta).                  (2)

The positive trace-p remainder is not falsely assumed CQ or re-filtered geometrically; it is simply charged by its trace. The negative CQ coefficient contracts at every accepted classifier, including when a fresh error is created on the final test.

Let u bound the complete unhalved diamond distance of the full actual L-classifier binary retained-data instrument from the exact Lueders measurement {Pchi,Qchi}. One sufficient generic choice is

 u=L[4sqrt(eta)+256h].                              (3)

The ideal finite classifier has complete instrument error<=4sqrt(eta), and the received signed-pair simulator contributes<=256h. Telescoping is on the COMPLETE retained-data binary instrument, not just acceptance probabilities.

Since the exact accepted map annihilates H_-, decomposing D as above yields

 ||A^L_actual(D)-Pchi D Pchi||1
 <=3beta^L+p e/(1-beta)+2p u.                        (4)

The factor2p charges the signed terms pPhi-lambda Pchi using the generic instrument bound. Equation(4) is a weighted accepted-MAP estimate, not only a probability estimate.

## 4. Rejected branch error remains D-weighted

Let B_actual be the combined retained-data branch for at least one rejection, and B0(X)=Qchi X Qchi. The exact-evolution finite circuit maps H_- diagonally: its rejected weight at each eigenvalue is1-a(lambda)^L, with0<=a(lambda)<=eta. Therefore

 +/-[B_ideal(H_-)-H_-]<=eta^L H_-.

Apply(1) to the WHOLE L-classifier rejected branch, using Htot=Lh. Put

 eL=e(Lh), kappa=eL+eta^L.

The pPhi-lambda Pchi part is charged through(3), and H_-<=D+pPchi. Thus

 +/-[B_actual(D)-B0(D)]<=kappa D+pR_D,
 R_D>=0, TrR_D<=kappa+eL+2u.                        (5)

This is the weighted reject-error estimate needed by multi-label telescoping. It is NOT the coarse claim that all reset prefixes are merely O(D)+O(p).

## 5. Useful consequence for an actual future suffix

Exact rejection obeys B0(D)<=D+pS with S>=0, TrS<=4. This follows from

 B0(D)-D=-p(Pchi Phi+Phi Pchi)+(p Tr(Pchi Phi)+lambda)Pchi

and trace norm at most4p. Combining with(5),

 B_actual(D)<=(1+kappa)D+pS',
 TrS'<=4+kappa+eL+2u.                               (6)

Also(4) and Tr(Pchi D)<=p bound the actual accepted mass on D. Hence a finite sequential suffix of such classifiers accepts D with probability O(number_of_labels*p), with explicit constants from(4)-(6). This coarse suffix bound is used ONLY to charge the small signed D-weighted errors in(5). It must not replace the sharper ideal-prefix baseline when proving recovery accuracy.

## Resource and closure scope

For any desired small dimensionless xi, one can choose L logarithmic in1/(p0xi), eta polynomially small in xi/L, and Lh at most xi divided by a sufficiently large fixed constant. Then beta^L=O(p0xi), u=O(xi), eL=O(xi), and(4) is O(pxi), while(5) has kappa=O(xi) and trace remainder O(xi). Achieving these h budgets with the received signed-pair allocation changes constants, not the p0^-2 signal exponent or its logarithmic overhead.

A full theorem still requires the exact nine-label ideal Gram/receiver estimate, complete accepted logical-output versus erasure accounting, and explicit final multi-label constants/resource allocation. No such full-throughput result is claimed by this lemma alone.
