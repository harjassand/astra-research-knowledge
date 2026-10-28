# Acquired Sylvester-filtered estimates give fast exact-source utility learning

27 October 2026. Local post-cutoff candidate theorem; independent receiving
requested before promotion. No historical novelty claim.

## Inputs and conclusion

Use the exact orthogonal-reset source, normalized qutrit Choi J, omega,
H=J-3omega and A=J+3omega, and the feasible decoder SDP in
`low_trace_decoder_sdp_relative_learning_root.md`. Let d be the dimension
of these matrices, and r bound the true Bell-projector rank and feasible
trace. For any supplied 0<t<=1 and failure probability beta, ordinary
state-copy measurements followed by classical processing acquire Hhat.
Its actual SDP optimizer has utility loss

                         L <= 140 r t                 (1)

with probability at least 1-beta. An additive SDP tolerance delta adds
2delta. The deterministic copy count is

 O((d/t) log(d/(beta t)) log(16/t)),                      (2)

plus the constant-relative pilot cost of the same order or smaller.
Consequently setting t=ell/(140r) gives L<=ell with
O(dr/ell) copies up to logarithms. The source-to-operational bridge then
allows the exact orthogonal-reset nu^-2 rather than nu^-4 utility-training
rate. This statement does not assert fast learning for overlapping reset.

## 1. Precise covariance input

For the ordinary unbiased debiased Keyl estimator Y_n of a state rho,
the PSW second-moment formula used in
`acquired_regularized_relative_operator_estimator.md` implies, for EVERY
Hermitian test X,

 E[Tr X(Y_n-rho)]^2
 <= (2/n) Tr rho X^2 + (d/n^2) Tr X^2.                 (3)

The rho-tensor-rho term is subtracted. Each other subtracted covariance
term contracts to Tr(P X P X)=Tr[(P^(1/2)X P^(1/2))^2]>=0 for P>=0.
Thus dropping those terms is legitimate even for indefinite X. This is
a REAL covariance quadratic-form domination on the Hermitian matrix
space, not merely a bound for positive tests.

## 2. A known pilot and its Sylvester filter

Acquire a constant-relative estimate of the state A/4 at regularization
t/4 and relative tolerance 1/8 by the received acquisition theorem.
A/4=T is the ACTUAL acquired labelled-two-design state. This is an
algebraic identity T=(J+3omega)/4, NOT a prescription to prepare a
physical J copy. Only ordinary labelled T and omega copies are available;
no entangled Choi-state preparation is assumed.
Set G=4(A/4)_hat+tI. On the successful pilot event,

 (7/8)(A+tI)<=G<=(9/8)(A+tI).

Abort if G fails (t/2)I<=G<=6I; successful pilot histories never abort.
The copy cap remains deterministic on all histories. Both physically available rho=T=A/4 and
rho=omega obey rho<=A<=2G. Put S=sqrt(G), a known classical matrix.
Define the known real-linear Hermitian Sylvester filter

 T_G(M)=Z where SZ+ZS=M,
        =integral_0^infinity exp(-uS) M exp(-uS)du.

In the computed G eigenbasis, its entries are M_ij/(sqrt(g_i)+sqrt(g_j)).
No physical whitening and no unknown eigenbasis are used.

## 3. Filtered covariance without a least source eigenvalue

Let E=Y_n-rho and put k_ij=1/(sqrt(g_i)+sqrt(g_j)) in the KNOWN
G eigenbasis. The full PSW matrix covariance is used here, not an
entrywise-to-operator inference. Its main covariance map before filtering
has terms rho TrW+I Tr(rho W)-rho W rho, divided by n.
After filtering, the first term has entries

 rho_ik sum_j k_ij k_jk.

This is rho Schur-multiplied by the positive Gram matrix of the rows of k.
As rho<=2G and G is diagonal in this computed basis, the Schur-product
order bounds it by the diagonal matrix

 diag_i[2g_i sum_j k_ij^2] <=2d I.

The second term becomes diag_i[sum_j rho_jj k_ij^2]<=2d I, since
rho_jj<=2g_j. The negative third term becomes -(T_G(rho))^2<=0.
Each other subtracted covariance term whose unfiltered contraction is
P Tr(PW), P>=0, becomes the matrix with entries

 -P_ik sum_j P_jj k_ij k_jk.

It is negative PSD: the sum is a weighted Gram matrix and the Schur
product with P is PSD. Thus every dropped correction has the correct
matrix sign even when rho, P and G do not commute.
Finally the white d/n^2 term becomes

 diag_i[(d/n^2)sum_j k_ij^2]
 <=[d^2/(4n^2 lambda_min(G))]I.

Consequently the actual filtered MATRIX variance satisfies

 E[T_G(E)^2]
 <=[4d/n+d^2/(4n^2 lambda_min(G))] I.                  (4)

Each actual contrast sample uses TWO INDEPENDENT fresh batches, one
of T and one of omega, each of n0=ceil(4096d/t) copies. Set

 Z_raw=4T_G(Y_T)-6T_G(Y_omega).

Its mean is M=T_G(4T-6omega)=T_G(H), using the ACTUAL labelled identity
H=J-3omega=4T-6omega. Independence cancels the cross covariance, so

 E[(Z_raw-M)^2]
 <=52[4d/n0+d^2/(4n0^2 lambda_min(G))]I
 <=52[4d/n0+d^2/(2n0^2 t)]I <t I.                     (5)

The factor 52=4^2+6^2 is charged explicitly; it is not a single-state
variance estimate.
There is no oracle source diagonalization or informal Gaussian
substitution in this proof.

The filtered CONTRAST mean M=T_G(H) is unknown but bounded. Since
-A<=H<=A and A<=(8/7)G, positivity of T_G gives
-T_G(A)<=M<=T_G(A), with T_G(A)<=(4/7)S. Thus ||M||<4
on every successful pilot history. This does not require H to be PSD.

## 4. Acquiring an unknown filtered mean by recentering and clipping

The following procedure uses two independent fresh batches of n0 copies
for every contrast sample at every stage, conditional on the preceding classical data.
Initialize C0=0 and R0=4. Let J_* be the smallest integer with
R_J*=4*2^(-J_*)<=sqrt(t). At stage j=0,...,J_*-1 assume the successful
history ||C_j-M||<=R_j, where R_j>sqrt(t).

For each fresh pair of Keyl batches form the known Hermitian matrix

 Z=4T_G(Y_T)-6T_G(Y_omega)-C_j,

and clip its eigenvalues to [-B_j,B_j], with B_j=64R_j. Because

 E Z^2=E[(Z_raw-M)^2]+(M-C_j)^2
       <=(t+R_j^2)I<=2R_j^2 I,

pointwise |Z-clip_B Z|<=Z^2/B gives clipping bias at most R_j/32.
Also E clip_B(Z)^2<=E Z^2<=2R_j^2 I. Thus its centered variance is at
most 2R_j^2 I and its centered norm at most 128R_j.

Average k independent clipped samples, with

 k=ceil[2048 log(4d J_*/beta_final)].

Two-sided Hermitian Bernstein at deviation R_j/4 gives failure at most
2d exp[-k/406], hence is more than sufficient for the allocated stage
failure beta_final/J_*. Put C_(j+1)=C_j+average(clip_B Z).
The new error is <=R_j/32+R_j/4<R_j/2=R_(j+1).

Induction and a union bound over first failed stages therefore yield
||C_J*-M||<=sqrt(t). The routine never uses the unknown mean, true
source basis, source eigenvalue floor, or a uniform empirical-process
assumption. Its copy cap is 2J_* k n0 on every path, counting both states.

There is ONE filtered-contrast routine, with the entire final-stage
failure budget beta_final. Its output C_final obeys
||C_final-T_G(H)||<=sqrt(t). No physical J copies are used.

## 5. Actual acquired H and deterministic risk receiving

Set

 Hhat=S C_final+C_final S.

By the defining Sylvester identity this estimates the ACTUAL H=4T-6omega.
Its error is S E0+E0 S, with E0=C_final-T_G(H) and ||E0||<=sqrt(t).
The known G satisfies G<=(9/8)(A+tI), hence the deterministic lemma
`low_trace_decoder_square_root_noise_localization_child.md` applies with
c=9/8 and epsilon=sqrt(t). It gives

 L <=[64*(9/8)+8*sqrt(9/8)]rt <140rt.

This includes the feasible optimizer even when it has rank larger than r.
The operational decoder is computed from the same finite SDP and is a
complete accepted-plus-erasure instrument; no postselection denominator
is introduced here.

## 6. Accounting and guards

Allocate beta/2 to the T-only pilot and beta/2 to the single
filtered-contrast routine. Every successful history meets all conditional
variance and radius hypotheses; first-failure union bounds handle arbitrary
behavior after a failure. The received pilot uses
O((d/t) log(d/(beta t))) copies with its dyadic logarithms, and the new
routine obeys (2), counting BOTH independent batches per sample.
All physical samples are the ACTUAL labelled T and omega states in the
ordinary unentangled source model. J is only an algebraic Choi operator;
there is no physical J-copy, entangled-probe, or Choi-preparation oracle.

The claimed fast rate depends essentially on exact-source commutation
[A,Pi]=0 and A<=2|H| in the deterministic localization lemma. This note
does not transfer those properties to a merely entropy-near source or
claim a general robust fast-rate theorem. The full PSW covariance, its Schur-product
filtering, the radius induction and the localization lemma must all be
independently received before final theorem promotion.

## Explicit physical and computational resource contract

Each fresh Keyl batch is a collective measurement on n0 physical source
output systems together with their locally prepared known-label reference
registers and the measurement's ancillas. The two contrast batches may be
measured separately, but this construction does not supply a constant-
quantum-memory realization or a cheap circuit for either collective POVM.
The pilot uses the same ordinary collective-tomography access model.

This is a concrete limitation of the imported primitive, not merely an
omitted efficiency assertion: Pelecanos--Spilecki--Wright explicitly state
in Section1.8, item4 of their [debiased Keyl paper](https://people.eecs.berkeley.edu/~jswright/papers/debiased-keyl.pdf)
that computationally efficient implementations of their sample-efficient
algorithms are not known in general; they identify n=1 as the exception.
That primary-source limitation was independently checked on27 October2026.
No general-n POVM circuit synthesis is acquired by this proof.

The known G, Sylvester operations and SDP are finite-dimensional classical
computations, but no bit/gate-complexity bound is asserted. A feasible SDP
solution with additive objective gap kappa contributes2kappa to the risk.
For example kappa<=rt gives L<=142rt using the conservative constant140
above; optimizer tolerance is not silently free. Numerical realization of
the mathematical POVMs or deployed CPTP decoder requires its own charged
implementation-error budget.

The nu^-2 statement is an UPPER source-query accuracy rate. The received
compilation lower bounds compare rank/ambient/throughput dependence at
fixed relative accuracy; they do not establish a matching nu^-2 lower
against arbitrary coherent adaptive training, which may have metrological
advantages on special query subclasses.
