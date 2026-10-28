# Reusable canonical receiver with quadratic rank/signal sample cost

2026-10-27. Frozen candidate for independent receiving. No claim for arbitrary noisy channels or arbitrary unknown spectra.

## 1. Contract and conclusion
Known integers 1<=r<=D, p=r/D. The unknown channel is
E_U(X)=U[X tensor P_r/D + Tr(X) I_3/3 tensor (I_D-P_r)/D]U*, U in U(3D).
The output register dimension and canonical reference model are known; U is not. Calibration uses independent normalized Choi copies, obtained by one physical source call each on half a known qutrit maximally entangled state. At deployment retain only a classical decoder description. No source-dependent quantum state or further source query is needed for any datum.

For any 0<nu<=1, the construction below produces a reusable decoder with training-averaged complete unhalved diamond error <=nu p relative to the accepted-logical/erasure target G_p. Its fixed sample cap is
N=O(D^2 nu^(-2) log(D/(nu p)))
with explicit constants below. Thus at fixed relative accuracy it costs O(r^2/p^2) up to logarithmic factors, matching the received pre-datum adaptive lower exponent on this canonical family. Collective measurements and ambient-dependent circuit descriptions are allowed and charged separately from source samples. The classical decoder optimization is a finite semidefinite program; no efficient quantum measurement or gate-synthesis claim is made.

## 2. Imported estimator facts, precisely scoped
Pelecanos–Spilecki–Wright, *The debiased Keyl's algorithm: a new unbiased estimator for full state tomography*, arXiv:2510.07788; author primary PDF https://people.eecs.berkeley.edu/~jswright/papers/debiased-keyl.pdf . Definition 1.2 and Theorems 1.3–1.4 give a unitarily covariant Hermitian estimator Y from n0 copies of a d-dimensional density matrix rho, with E Y=rho. In a rho eigenbasis, the second-moment consequence explicitly stated on page 10 is
E|Y_ij-rho_ij|^2 <= (alpha_i+alpha_j)/n0 + d/n0^2.
The eigenvalues of Y are donate(lambda)_i/n0, where lambda is the weak-Schur-sampling Young diagram and each donation shift has absolute value at most d. Hence ||Y||<=1+d/n0 and ||Y||<=lambda_1/n0+d/n0.

Unitary covariance under all diagonal phases preserving rho implies E(Y-rho)^2 is diagonal in this eigenbasis. Summing the entry bound over a row therefore proves
||E(Y-rho)^2|| <= (d alpha_max+1)/n0+d^2/n0^2.
For the canonical normalized Choi J, d=9D and alpha_max=1/D, this is <=10/n0+81D^2/n0^2.

A direct alternative derivation of the operator variance, independently checked from Theorem 1.4, contracts its second moment as Tr_2[(E Y tensor Y) SWAP]. The explicit subtracted Lower_rho terms become positive operators after this contraction. This gives the stronger bound
E(Y-rho)^2 <=(d rho+I-rho^2)/n0+d E[ell(lambda)] I/n0^2,
which implies the stated bound using ell(lambda)<=d. Thus covariance is not essential to the construction.

## 3. Spectral clipping gives bounded independent batches
Set epsilon=nu/4000, beta=nu p/8, n0=100D^2, and B=8/epsilon. From the imported variance bound and unbiasedness,
E Y^2 = J^2+E(Y-J)^2 <=[1+10/100+81/10000] I/D^2 <=2I/D^2.
Define X by spectrally clipping the observed Hermitian matrix Y to the interval [-B/D,B/D]. This is a classical operation on the estimator, requiring no unknown eigenbasis or physical whitening oracle.

The scalar clipping inequalities lift by functional calculus to
|Y-X|<=Y^2/(B/D), and X^2<=Y^2.
Consequently, with mu=E X,
||mu-J||<=2/(BD)=epsilon/(4D),
E(X-mu)^2=E X^2-mu^2 <=E X^2<=2I/D^2,
and ||X-mu||<=2B/D=16/(epsilon D).
No Schur-row concentration, random sample cap, or conditional rejection is needed.

## 4. Operator-norm estimation from independent batches
Take
k=ceil(64 epsilon^(-2) ln(18D/beta))
independent batches and let Jtilde be their average. The self-adjoint matrix Bernstein inequality with variance2/D^2 and centered bound16/(epsilon D) gives
Pr(||Jtilde-mu||>=epsilon/(2D))
 <=18D exp[-k epsilon^2/40] <=beta.
Indeed the denominator 2v+(2/3)Rt is at most (4+16/3)/D^2<10/D^2 at t=epsilon/(2D). Together with the bias this implies
||Jtilde-J||<=epsilon/D
except with probability beta. The total source cap is exactly N=k n0. All batches are independent and have a deterministic size.

Primary matrix concentration prerequisite: the standard self-adjoint Bernstein bound for independent mean-zero Hermitian matrices, with denominator 2v+(2/3)Rt and prefactor2d. This is the form in Tropp, *User-friendly tail bounds for sums of random matrices*, arXiv:1004.4389. The use here is finite-dimensional and independent-batch only.

## 5. Spectral rounding to a density estimate
Diagonalize the observed Hermitian Jtilde. Replace its r largest eigenvalues by 1/D, its next 9(D-r) eigenvalues by 1/(9D), and its last 8r eigenvalues by zero. Call the resulting density matrix Jbar. At D=r the middle list is empty. The eigenvectors are the observed ones; no unknown eigenbasis is used.

On the good event, Weyl's sorted eigenvalue inequality implies ||Jbar-Jtilde||<=epsilon/D, and hence
||Jbar-J||<=2epsilon/D.
Both J and Jbar have the canonical discrete spectrum. Each minus I/(9D) has rank9r, so rank(Jbar-J)<=18r and
||Jbar-J||_F^2<=72r epsilon^2/D^2.
Expansion in the two eigenbases gives
||sqrt(Jbar)-sqrt(J)||_F^2<=9D ||Jbar-J||_F^2;
the divided difference of sqrt is at most3sqrt(D) whenever the two eigenvalues differ, and equal-eigenvalue terms vanish. Consequently their root infidelity obeys
1-F(Jbar,J)<=delta0:=324p epsilon^2.
Here F is root fidelity; F>=Tr(sqrt(Jbar)sqrt(J)) and both matrices have trace one.

Jbar need NOT have a maximally mixed input marginal and need NOT be a physical channel Choi state. The next step only requires a density estimate.

## 6. Decoder SDP and complete recovery
Let K_p=J_(G_p), the known normalized Choi density of the accepted-logical/erasure target. Over CPTP decoders D from the physical register to a qutrit-plus-erasure register, maximize
F((id tensor D)(Jbar),K_p)
to additive tolerance delta0. Enforce classical accepted/erased output dephasing, either as a linear constraint or after optimization; K_p is invariant under it and fidelity cannot decrease. This is the same finite fidelity SDP received in reusable_rare_recovery_infidelity_tomography.md. It has the standard block-positive representation with objective Re Tr X and block diagonal entries (id tensor D)(Jbar),K_p.

An exact decoder D_* exists for the true canonical source. By monotonicity, it attains fidelity at least1-delta0 on Jbar. Thus the selected Dhat attains fidelity at least1-2delta0 on Jbar. Monotonicity between Jbar and J followed by the Bures triangle inequality gives actual recovered root infidelity at most
(1+sqrt(2))^2 delta0 <6delta0=1944p epsilon^2.
This is why no channel constraint or exact decoder for Jbar is required.

The received rare-throughput fidelity lemma therefore yields
||Dhat E_U-G_p||_diamond <=12sqrt(2p delta)+12delta,
where delta=1944p epsilon^2. With epsilon=nu/4000 this is less than nu p/4: use sqrt(3888)<63 and nu<=1. On the bad training event complete channel error is at most2. With beta=nu p/8, training-averaged error is less than nu p/2, in particular <=nu p.

The good classical decoder may be reused on any number of independent data without new source calibration. A joint M-use diamond guarantee incurs the usual at-most-M accumulation on the good event; the one-off bad-training event is charged separately, not independently resampled. This is classical reuse, not catalytic use of a quantum program.

## 7. Boundaries
Only the known canonical flat rank/signal orbit is covered. Unknown general reset spectra, arbitrary mixed flags, unknown p, entropy-only perturbations, and unknown ambient model are not inferred. Integer-grid p=r/D is used throughout. No all-real-p extension is imported before separate receiving. No historical novelty claim is made.
